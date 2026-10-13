import { DT_MS, TICK_HZ } from '../shared/config';
import {
  FLAG_MOVING,
  Msg,
  decodeSnapshot,
  decodeWelcome,
  encodeInput,
  encodePing,
  type Snapshot,
} from '../shared/protocol';
import { cloneState, newPlayerState, quantizeInput, stepPlayer, type InputCmd, type PlayerState } from '../shared/sim';
import { World } from '../shared/world';
import type { Input } from './input';

/** Remote entities are rendered this far in the past so there are always two snapshots to blend. */
export const INTERP_DELAY_MS = 150;
const MAX_STEPS_PER_FRAME = 5;
const SNAP_ERR = 3; // metres: beyond this, teleport instead of smoothing
const IGNORE_ERR = 0.02; // metres: below this, keep the prediction untouched

interface Sample {
  t: number;
  x: number;
  y: number;
  z: number;
  yaw: number;
  flags: number;
}

interface Remote {
  id: number;
  samples: Sample[];
}

export interface Avatar {
  id: number;
  x: number;
  y: number;
  z: number;
  yaw: number;
  self: boolean;
  moving: boolean;
}

export class NetClient {
  id = 0;
  world: World | null = null;
  local: PlayerState = newPlayerState(0, 0);
  pingMs = 0;
  bytesDown = 0;
  snapshots = 0;
  visibleSum = 0;
  firstSnapshotAt = 0;
  closed = false;

  private ws!: WebSocket;
  private prev: PlayerState = cloneState(this.local);
  private err = { x: 0, y: 0, z: 0 };
  private pending: { seq: number; cmd: InputCmd }[] = [];
  private seq = 0;
  private acc = 0;
  private remotes = new Map<number, Remote>();
  private clockOffset: number | null = null;
  private haveState = false;
  private pool: Avatar[] = [];
  private pingTimer = 0;

  connect(room: string): Promise<void> {
    return new Promise((resolve, reject) => {
      const proto = location.protocol === 'https:' ? 'wss' : 'ws';
      this.ws = new WebSocket(`${proto}://${location.host}/ws?room=${encodeURIComponent(room)}`);
      this.ws.binaryType = 'arraybuffer';
      this.ws.onerror = () => reject(new Error('websocket error'));
      this.ws.onclose = () => {
        this.closed = true;
        clearInterval(this.pingTimer);
        reject(new Error('websocket closed'));
      };
      this.ws.onmessage = (ev) => {
        const buf = ev.data as ArrayBuffer;
        this.bytesDown += buf.byteLength;
        const dv = new DataView(buf);
        switch (dv.getUint8(0)) {
          case Msg.Welcome: {
            const w = decodeWelcome(dv);
            this.id = w.id;
            this.world = new World(w.seed);
            this.pingTimer = window.setInterval(() => this.send(encodePing(performance.now())), 1000);
            resolve();
            break;
          }
          case Msg.Snapshot: {
            const s = decodeSnapshot(dv);
            if (s) this.onSnapshot(s);
            break;
          }
          case Msg.Pong: {
            const rtt = performance.now() - dv.getFloat64(1, true);
            this.pingMs = this.pingMs === 0 ? rtt : this.pingMs * 0.8 + rtt * 0.2;
            break;
          }
        }
      };
    });
  }

  private send(data: Uint8Array<ArrayBuffer>): void {
    if (this.ws.readyState === WebSocket.OPEN) this.ws.send(data);
  }

  get ready(): boolean {
    return this.haveState;
  }

  /** Runs the fixed-timestep prediction. Call once per rendered frame. */
  update(frameMs: number, input: Input): void {
    if (!this.world || !this.haveState) return;
    this.acc += frameMs;
    let steps = 0;
    while (this.acc >= DT_MS && steps < MAX_STEPS_PER_FRAME) {
      const m = input.sample();
      const cmd = quantizeInput({ mx: m.mx, mz: m.mz, camYaw: input.yaw, jump: m.jump });
      this.seq++;
      this.prev = cloneState(this.local);
      stepPlayer(this.local, cmd, this.world);
      this.pending.push({ seq: this.seq, cmd });
      if (this.pending.length > 120) this.pending.shift();
      this.send(encodeInput(this.seq, cmd));
      this.acc -= DT_MS;
      steps++;
    }
    if (steps === MAX_STEPS_PER_FRAME) this.acc = 0;
    const decay = Math.exp(-frameMs / 100);
    this.err.x *= decay;
    this.err.y *= decay;
    this.err.z *= decay;
  }

  private onSnapshot(s: Snapshot): void {
    const now = performance.now();
    this.snapshots++;
    this.visibleSum += s.others.length;
    if (!this.firstSnapshotAt) this.firstSnapshotAt = now;

    const serverT = s.tick * DT_MS;
    const delta = now - serverT;
    this.clockOffset =
      this.clockOffset === null || delta < this.clockOffset ? delta : this.clockOffset + (delta - this.clockOffset) * 0.02;

    if (!this.haveState) {
      this.local = { x: s.self.x, y: s.self.y, z: s.self.z, vy: s.self.vy, yaw: 0, grounded: s.self.grounded, moving: false };
      this.prev = cloneState(this.local);
      this.haveState = true;
    } else if (this.world) {
      this.reconcile(s);
    }

    const seen = new Set<number>();
    for (const e of s.others) {
      seen.add(e.id);
      let r = this.remotes.get(e.id);
      if (!r) this.remotes.set(e.id, (r = { id: e.id, samples: [] }));
      r.samples.push({ t: serverT, x: e.x, y: e.y, z: e.z, yaw: e.yaw, flags: e.flags });
      if (r.samples.length > 10) r.samples.shift();
    }
    for (const id of this.remotes.keys()) if (!seen.has(id)) this.remotes.delete(id);
  }

  private reconcile(s: Snapshot): void {
    const world = this.world!;
    const before = cloneState(this.local);
    const keep = this.pending.findIndex((p) => p.seq > s.lastSeq);
    this.pending = keep < 0 ? [] : this.pending.slice(keep);

    const st = this.local;
    st.x = s.self.x;
    st.y = s.self.y;
    st.z = s.self.z;
    st.vy = s.self.vy;
    st.grounded = s.self.grounded;
    for (const p of this.pending) stepPlayer(st, p.cmd, world);

    const dx = before.x - st.x;
    const dy = before.y - st.y;
    const dz = before.z - st.z;
    const dist = Math.hypot(dx, dy, dz);
    if (dist < IGNORE_ERR) {
      this.local = before;
      return;
    }
    if (dist > SNAP_ERR) {
      this.prev = cloneState(st);
      this.err = { x: 0, y: 0, z: 0 };
      return;
    }
    // Keep the rendered position continuous: shift prev by the correction, store it as a decaying visual error.
    this.prev.x += st.x - before.x;
    this.prev.y += st.y - before.y;
    this.prev.z += st.z - before.z;
    this.err.x += dx;
    this.err.y += dy;
    this.err.z += dz;
  }

  /** Fills `out` (self first) with avatars to draw this frame; returns the count. */
  avatars(nowMs: number, out: Avatar[]): number {
    let n = 0;
    const take = (): Avatar => this.pool[n] ?? (this.pool[n] = { id: 0, x: 0, y: 0, z: 0, yaw: 0, self: false, moving: false });
    const alpha = Math.min(1, this.acc / DT_MS);
    const a = take();
    a.id = this.id;
    a.x = this.prev.x + (this.local.x - this.prev.x) * alpha + this.err.x;
    a.y = this.prev.y + (this.local.y - this.prev.y) * alpha + this.err.y;
    a.z = this.prev.z + (this.local.z - this.prev.z) * alpha + this.err.z;
    a.yaw = this.local.yaw;
    a.self = true;
    a.moving = this.local.moving;
    out[n++] = a;

    if (this.clockOffset !== null) {
      const renderT = nowMs - this.clockOffset - INTERP_DELAY_MS;
      for (const r of this.remotes.values()) {
        const s = r.samples;
        if (s.length === 0) continue;
        let i = s.length - 1;
        while (i > 0 && s[i - 1].t > renderT) i--;
        const b = s[i];
        const prev = i > 0 ? s[i - 1] : b;
        const span = b.t - prev.t;
        const f = span > 0 ? Math.max(0, Math.min(1, (renderT - prev.t) / span)) : 1;
        const av = take();
        av.id = r.id;
        av.x = prev.x + (b.x - prev.x) * f;
        av.y = prev.y + (b.y - prev.y) * f;
        av.z = prev.z + (b.z - prev.z) * f;
        let dyaw = b.yaw - prev.yaw;
        if (dyaw > Math.PI) dyaw -= Math.PI * 2;
        else if (dyaw < -Math.PI) dyaw += Math.PI * 2;
        av.yaw = prev.yaw + dyaw * f;
        av.self = false;
        av.moving = (b.flags & FLAG_MOVING) !== 0;
        out[n++] = av;
      }
    }
    out.length = n;
    return n;
  }

  get remoteCount(): number {
    return this.remotes.size;
  }

  get tickHz(): number {
    return TICK_HZ;
  }

  close(): void {
    this.ws?.close();
  }
}
