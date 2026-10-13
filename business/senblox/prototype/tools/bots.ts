import { pathToFileURL } from 'node:url';
import WebSocket from 'ws';
import { TICK_HZ } from '../shared/config';
import { Msg, decodeSnapshot, decodeWelcome, encodeInput, encodePing } from '../shared/protocol';
import { quantizeInput } from '../shared/sim';

export interface BotOptions {
  url: string;
  room: string;
  count: number;
  durationSec: number;
  /** Bots steer back towards the origin when further than this (metres). 0 = free roaming. */
  clusterRadius?: number;
  rampMs?: number;
}

export interface BotReport {
  bots: number;
  connected: number;
  durationSec: number;
  perBotKbitPerSec: { mean: number; p50: number; p95: number; max: number };
  visibleOthers: { mean: number; max: number };
  snapshotsPerSecPerBot: number;
  pingMs: { p50: number; p95: number; max: number };
  disconnects: number;
  /** Server /metrics captured at the end of the window, while bots are still connected. */
  server: unknown;
}

const pct = (a: number[], p: number) => (a.length ? a[Math.min(a.length - 1, Math.floor((p / 100) * a.length))] : 0);

export async function runBots(opts: BotOptions): Promise<BotReport> {
  const { url, room, count, durationSec, clusterRadius = 0, rampMs = 15 } = opts;
  const bytes: number[] = new Array(count).fill(0);
  const snaps: number[] = new Array(count).fill(0);
  const visibleSum: number[] = new Array(count).fill(0);
  let visibleMax = 0;
  const pings: number[] = [];
  let connected = 0;
  let disconnects = 0;
  const sockets: WebSocket[] = [];
  const timers: NodeJS.Timeout[] = [];
  let measuring = false;

  const makeBot = (i: number) =>
    new Promise<void>((resolve) => {
      const ws = new WebSocket(`${url.replace(/^http/, 'ws')}/ws?room=${room}`);
      ws.binaryType = 'nodebuffer';
      sockets.push(ws);
      let seq = 0;
      let heading = Math.random() * Math.PI * 2;
      let nextTurn = 0;
      let x = 0;
      let z = 0;
      ws.on('open', () => {
        connected++;
        resolve();
        const t = setInterval(() => {
          const now = performance.now();
          if (now > nextTurn) {
            heading += (Math.random() - 0.5) * 2.2;
            nextTurn = now + 1000 + Math.random() * 2000;
          }
          if (clusterRadius > 0 && Math.hypot(x, z) > clusterRadius) heading = Math.atan2(x, z);
          const cmd = quantizeInput({ mx: 0, mz: 1, camYaw: heading, jump: Math.random() < 0.03 });
          ws.send(encodeInput(++seq, cmd));
        }, 1000 / TICK_HZ);
        timers.push(t);
        const pt = setInterval(() => ws.send(encodePing(performance.now())), 1000);
        timers.push(pt);
      });
      ws.on('message', (data: Buffer) => {
        const dv = new DataView(data.buffer, data.byteOffset, data.byteLength);
        const type = dv.getUint8(0);
        if (measuring) bytes[i] += data.byteLength;
        if (type === Msg.Welcome) decodeWelcome(dv);
        else if (type === Msg.Snapshot) {
          const s = decodeSnapshot(dv);
          if (s) {
            x = s.self.x;
            z = s.self.z;
            if (measuring) {
              snaps[i]++;
              visibleSum[i] += s.others.length;
              if (s.others.length > visibleMax) visibleMax = s.others.length;
            }
          }
        } else if (type === Msg.Pong && measuring) pings.push(performance.now() - dv.getFloat64(1, true));
      });
      ws.on('close', () => {
        if (measuring) disconnects++;
        resolve();
      });
      ws.on('error', () => resolve());
    });

  for (let i = 0; i < count; i++) {
    void makeBot(i);
    if (rampMs) await new Promise((r) => setTimeout(r, rampMs));
  }
  await new Promise((r) => setTimeout(r, 2000)); // let everyone settle before measuring
  await fetch(`${url}/metrics?reset=1`).catch(() => null);
  measuring = true;
  await new Promise((r) => setTimeout(r, durationSec * 1000));
  const server = await fetch(`${url}/metrics`).then((r) => r.json()).catch(() => null);
  measuring = false;

  for (const t of timers) clearInterval(t);
  for (const ws of sockets) ws.terminate();

  const kbit = bytes.map((b) => (b * 8) / 1000 / durationSec).sort((a, b) => a - b);
  const totalSnaps = snaps.reduce((a, b) => a + b, 0);
  const sortedPings = pings.sort((a, b) => a - b);
  const mean = (a: number[]) => (a.length ? a.reduce((s, v) => s + v, 0) / a.length : 0);
  return {
    bots: count,
    connected,
    durationSec,
    perBotKbitPerSec: {
      mean: +mean(kbit).toFixed(2),
      p50: +pct(kbit, 50).toFixed(2),
      p95: +pct(kbit, 95).toFixed(2),
      max: +(kbit[kbit.length - 1] ?? 0).toFixed(2),
    },
    visibleOthers: { mean: +(visibleSum.reduce((a, b) => a + b, 0) / Math.max(1, totalSnaps)).toFixed(1), max: visibleMax },
    snapshotsPerSecPerBot: +(totalSnaps / count / durationSec).toFixed(2),
    pingMs: { p50: +pct(sortedPings, 50).toFixed(2), p95: +pct(sortedPings, 95).toFixed(2), max: +(sortedPings[sortedPings.length - 1] ?? 0).toFixed(2) },
    disconnects,
    server,
  };
}

function arg(name: string, def: string): string {
  const i = process.argv.indexOf(`--${name}`);
  return i >= 0 && process.argv[i + 1] ? process.argv[i + 1] : def;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const url = arg('url', 'http://127.0.0.1:8787');
  const report = await runBots({
    url,
    room: arg('room', 'bench'),
    count: Number(arg('n', '100')),
    durationSec: Number(arg('duration', '30')),
    clusterRadius: Number(arg('cluster', '0')),
  });
  console.log(JSON.stringify(report, null, 2));
  process.exit(0);
}
