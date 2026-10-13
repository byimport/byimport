import type { WebSocket } from 'ws';
import { MAX_INBOX, MAX_INPUTS_PER_TICK, SNAPSHOT_DIVISOR, TICK_HZ } from '../shared/config';
import { Msg, decodeInput, encodeSnapshot, encodeWelcome, pongFromPing, type EntityIn } from '../shared/protocol';
import { newPlayerState, stepPlayer, type InputCmd, type PlayerState } from '../shared/sim';
import { World, hashRoom } from '../shared/world';
import { SpatialHash, selectVisible } from './interest';
import type { Metrics } from './metrics';

export interface Player {
  id: number;
  ws: WebSocket;
  state: PlayerState;
  inbox: { seq: number; cmd: InputCmd }[];
  lastSeq: number;
  known: Set<number>;
  msgWindowStart: number;
  msgCount: number;
  /** Mirrors state for the spatial hash (needs `id`, `x`, `z`). */
  x: number;
  z: number;
}

const MAX_MSGS_PER_SEC = 150;
const BACKPRESSURE_BYTES = 64 * 1024;

export class Room {
  readonly world: World;
  readonly players = new Map<number, Player>();
  private nextId = 1;
  private tick = 0;
  private readonly hash = new SpatialHash<Player>();
  private readonly scratch: Player[] = [];
  private readonly visible: Player[] = [];

  constructor(readonly name: string, private readonly metrics: Metrics) {
    this.world = new World(hashRoom(name));
  }

  get size(): number {
    return this.players.size;
  }

  add(ws: WebSocket): Player {
    let id = this.nextId;
    while (this.players.has(id)) id = (id % 65535) + 1;
    this.nextId = (id % 65535) + 1;
    const a = Math.random() * Math.PI * 2;
    const r = 1 + Math.random() * 5;
    const state = newPlayerState(Math.cos(a) * r, Math.sin(a) * r);
    const p: Player = {
      id,
      ws,
      state,
      inbox: [],
      lastSeq: 0,
      known: new Set(),
      msgWindowStart: performance.now(),
      msgCount: 0,
      x: state.x,
      z: state.z,
    };
    this.players.set(id, p);
    this.send(p, encodeWelcome(id, this.world.seed, TICK_HZ));
    return p;
  }

  remove(p: Player): void {
    this.players.delete(p.id);
  }

  handle(p: Player, data: Buffer): void {
    this.metrics.bytesIn += data.byteLength;
    const now = performance.now();
    if (now - p.msgWindowStart > 1000) {
      p.msgWindowStart = now;
      p.msgCount = 0;
    }
    if (++p.msgCount > MAX_MSGS_PER_SEC) {
      p.ws.close(1008, 'rate limit');
      return;
    }
    if (data.byteLength < 1) return;
    const dv = new DataView(data.buffer, data.byteOffset, data.byteLength);
    switch (dv.getUint8(0)) {
      case Msg.Input: {
        const inp = decodeInput(dv);
        if (!inp) return;
        const newest = p.inbox.length ? p.inbox[p.inbox.length - 1].seq : p.lastSeq;
        if (inp.seq <= newest) return;
        if (p.inbox.length >= MAX_INBOX) p.inbox.shift();
        p.inbox.push(inp);
        break;
      }
      case Msg.Ping:
        if (dv.byteLength >= 9) this.send(p, pongFromPing(dv));
        break;
    }
  }

  private send(p: Player, data: Uint8Array): void {
    if (p.ws.readyState !== 1) return;
    if (p.ws.bufferedAmount > BACKPRESSURE_BYTES) return;
    p.ws.send(data, { binary: true });
    this.metrics.bytesOut += data.byteLength;
    this.metrics.messagesOut++;
  }

  step(): void {
    this.tick++;
    this.hash.clear();
    for (const p of this.players.values()) {
      for (let n = 0; n < MAX_INPUTS_PER_TICK && p.inbox.length; n++) {
        const inp = p.inbox.shift()!;
        stepPlayer(p.state, inp.cmd, this.world);
        p.lastSeq = inp.seq;
      }
      p.x = p.state.x;
      p.z = p.state.z;
      this.hash.insert(p);
    }
    for (const p of this.players.values()) {
      if (this.tick % SNAPSHOT_DIVISOR !== p.id % SNAPSHOT_DIVISOR) continue;
      selectVisible(p, this.hash, p.known, this.scratch, this.visible);
      const others: EntityIn[] = this.visible.map((o) => ({
        id: o.id,
        x: o.state.x,
        y: o.state.y,
        z: o.state.z,
        yaw: o.state.yaw,
        grounded: o.state.grounded,
        moving: o.state.moving,
      }));
      const s = p.state;
      this.send(
        p,
        encodeSnapshot(this.tick, p.lastSeq, { x: s.x, y: s.y, z: s.z, vy: s.vy, grounded: s.grounded }, others),
      );
    }
  }
}
