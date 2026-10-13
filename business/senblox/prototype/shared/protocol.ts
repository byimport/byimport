import { TWO_PI } from './config';
import { quantizeInput, wrapAngle, type InputCmd } from './sim';

export const Msg = { Input: 1, Welcome: 2, Snapshot: 3, Ping: 4, Pong: 5 } as const;

export const FLAG_GROUNDED = 1;
export const FLAG_MOVING = 2;

const POS_SCALE = 100;
const i16 = (v: number) => Math.max(-32768, Math.min(32767, Math.round(v * POS_SCALE)));
const yawToU16 = (yaw: number) => Math.round((wrapAngle(yaw) / TWO_PI) * 65536) & 0xffff;
const u16ToYaw = (v: number) => (v * TWO_PI) / 65536;

export const INPUT_BYTES = 10;
export const SNAPSHOT_HEADER_BYTES = 20;
export const SNAPSHOT_ENTITY_BYTES = 11;

export function encodeInput(seq: number, cmd: InputCmd): Uint8Array<ArrayBuffer> {
  const buf = new Uint8Array(INPUT_BYTES);
  const dv = new DataView(buf.buffer);
  dv.setUint8(0, Msg.Input);
  dv.setUint32(1, seq >>> 0, true);
  dv.setInt8(5, Math.round(cmd.mx * 127));
  dv.setInt8(6, Math.round(cmd.mz * 127));
  dv.setUint16(7, yawToU16(cmd.camYaw), true);
  dv.setUint8(9, cmd.jump ? 1 : 0);
  return buf;
}

export function decodeInput(dv: DataView): { seq: number; cmd: InputCmd } | null {
  if (dv.byteLength < INPUT_BYTES) return null;
  const cmd = quantizeInput({
    mx: dv.getInt8(5) / 127,
    mz: dv.getInt8(6) / 127,
    camYaw: u16ToYaw(dv.getUint16(7, true)),
    jump: (dv.getUint8(9) & 1) === 1,
  });
  return { seq: dv.getUint32(1, true), cmd };
}

export function encodeWelcome(id: number, seed: number, tickHz: number): Uint8Array {
  const buf = new Uint8Array(8);
  const dv = new DataView(buf.buffer);
  dv.setUint8(0, Msg.Welcome);
  dv.setUint16(1, id, true);
  dv.setUint32(3, seed >>> 0, true);
  dv.setUint8(7, tickHz);
  return buf;
}

export function decodeWelcome(dv: DataView): { id: number; seed: number; tickHz: number } {
  return { id: dv.getUint16(1, true), seed: dv.getUint32(3, true), tickHz: dv.getUint8(7) };
}

export function encodePing(t: number): Uint8Array<ArrayBuffer> {
  const buf = new Uint8Array(9);
  const dv = new DataView(buf.buffer);
  dv.setUint8(0, Msg.Ping);
  dv.setFloat64(1, t, true);
  return buf;
}

export function pongFromPing(ping: DataView): Uint8Array {
  const buf = new Uint8Array(9);
  buf.set(new Uint8Array(ping.buffer, ping.byteOffset, 9));
  buf[0] = Msg.Pong;
  return buf;
}

export interface SelfState {
  x: number;
  y: number;
  z: number;
  vy: number;
  grounded: boolean;
}

export interface Entity {
  id: number;
  x: number;
  y: number;
  z: number;
  yaw: number;
  flags: number;
}

export interface Snapshot {
  tick: number;
  lastSeq: number;
  self: SelfState;
  others: Entity[];
}

export interface EntityIn {
  id: number;
  x: number;
  y: number;
  z: number;
  yaw: number;
  grounded: boolean;
  moving: boolean;
}

export function encodeSnapshot(tick: number, lastSeq: number, self: SelfState, others: EntityIn[]): Uint8Array {
  const buf = new Uint8Array(SNAPSHOT_HEADER_BYTES + others.length * SNAPSHOT_ENTITY_BYTES);
  const dv = new DataView(buf.buffer);
  dv.setUint8(0, Msg.Snapshot);
  dv.setUint32(1, tick >>> 0, true);
  dv.setUint32(5, lastSeq >>> 0, true);
  dv.setInt16(9, i16(self.x), true);
  dv.setInt16(11, i16(self.y), true);
  dv.setInt16(13, i16(self.z), true);
  dv.setInt16(15, i16(self.vy), true);
  dv.setUint8(17, self.grounded ? FLAG_GROUNDED : 0);
  dv.setUint16(18, others.length, true);
  let o = SNAPSHOT_HEADER_BYTES;
  for (const e of others) {
    dv.setUint16(o, e.id, true);
    dv.setInt16(o + 2, i16(e.x), true);
    dv.setInt16(o + 4, i16(e.y), true);
    dv.setInt16(o + 6, i16(e.z), true);
    dv.setUint16(o + 8, yawToU16(e.yaw), true);
    dv.setUint8(o + 10, (e.grounded ? FLAG_GROUNDED : 0) | (e.moving ? FLAG_MOVING : 0));
    o += SNAPSHOT_ENTITY_BYTES;
  }
  return buf;
}

export function decodeSnapshot(dv: DataView): Snapshot | null {
  if (dv.byteLength < SNAPSHOT_HEADER_BYTES) return null;
  const count = dv.getUint16(18, true);
  if (dv.byteLength < SNAPSHOT_HEADER_BYTES + count * SNAPSHOT_ENTITY_BYTES) return null;
  const others: Entity[] = new Array(count);
  let o = SNAPSHOT_HEADER_BYTES;
  for (let i = 0; i < count; i++) {
    others[i] = {
      id: dv.getUint16(o, true),
      x: dv.getInt16(o + 2, true) / POS_SCALE,
      y: dv.getInt16(o + 4, true) / POS_SCALE,
      z: dv.getInt16(o + 6, true) / POS_SCALE,
      yaw: u16ToYaw(dv.getUint16(o + 8, true)),
      flags: dv.getUint8(o + 10),
    };
    o += SNAPSHOT_ENTITY_BYTES;
  }
  return {
    tick: dv.getUint32(1, true),
    lastSeq: dv.getUint32(5, true),
    self: {
      x: dv.getInt16(9, true) / POS_SCALE,
      y: dv.getInt16(11, true) / POS_SCALE,
      z: dv.getInt16(13, true) / POS_SCALE,
      vy: dv.getInt16(15, true) / POS_SCALE,
      grounded: (dv.getUint8(17) & FLAG_GROUNDED) !== 0,
    },
    others,
  };
}
