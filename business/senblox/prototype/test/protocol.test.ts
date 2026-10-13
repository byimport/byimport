import { describe, expect, it } from 'vitest';
import {
  FLAG_GROUNDED,
  FLAG_MOVING,
  SNAPSHOT_ENTITY_BYTES,
  SNAPSHOT_HEADER_BYTES,
  decodeInput,
  decodeSnapshot,
  decodeWelcome,
  encodeInput,
  encodeSnapshot,
  encodeWelcome,
} from '../shared/protocol';
import { quantizeInput } from '../shared/sim';

const view = (b: Uint8Array) => new DataView(b.buffer, b.byteOffset, b.byteLength);

describe('protocol', () => {
  it('round-trips an input and matches the client-side quantisation exactly', () => {
    const raw = { mx: 0.37, mz: -0.81, camYaw: 5.9, jump: true };
    const decoded = decodeInput(view(encodeInput(4242, quantizeInput(raw))))!;
    expect(decoded.seq).toBe(4242);
    expect(decoded.cmd).toEqual(quantizeInput(raw));
  });

  it('rejects truncated input and snapshot buffers', () => {
    expect(decodeInput(view(new Uint8Array(4)))).toBeNull();
    expect(decodeSnapshot(view(new Uint8Array(5)))).toBeNull();
    const snap = encodeSnapshot(1, 1, { x: 0, y: 0, z: 0, vy: 0, grounded: true }, [
      { id: 1, x: 1, y: 0, z: 1, yaw: 0, grounded: true, moving: false },
    ]);
    expect(decodeSnapshot(view(snap.subarray(0, snap.length - 3)))).toBeNull();
  });

  it('round-trips welcome and snapshot with centimetre precision', () => {
    expect(decodeWelcome(view(encodeWelcome(77, 0xdeadbeef, 30)))).toEqual({ id: 77, seed: 0xdeadbeef, tickHz: 30 });
    const snap = decodeSnapshot(
      view(
        encodeSnapshot(
          99,
          1234,
          { x: -12.345, y: 3.21, z: 100.5, vy: -4.2, grounded: false },
          [
            { id: 5, x: 1.234, y: 0, z: -7.891, yaw: 1.5, grounded: true, moving: true },
            { id: 9, x: -100, y: 2.5, z: 100, yaw: 6, grounded: false, moving: false },
          ],
        ),
      ),
    )!;
    expect(snap.tick).toBe(99);
    expect(snap.lastSeq).toBe(1234);
    expect(snap.self.x).toBeCloseTo(-12.345, 1);
    expect(snap.self.grounded).toBe(false);
    expect(snap.others).toHaveLength(2);
    expect(snap.others[0].id).toBe(5);
    expect(snap.others[0].z).toBeCloseTo(-7.891, 1);
    expect(snap.others[0].flags).toBe(FLAG_GROUNDED | FLAG_MOVING);
    expect(snap.others[1].flags).toBe(0);
  });

  it('has the documented wire size', () => {
    const n = 20;
    const others = Array.from({ length: n }, (_, id) => ({ id, x: 0, y: 0, z: 0, yaw: 0, grounded: true, moving: false }));
    const snap = encodeSnapshot(1, 1, { x: 0, y: 0, z: 0, vy: 0, grounded: true }, others);
    expect(snap.byteLength).toBe(SNAPSHOT_HEADER_BYTES + n * SNAPSHOT_ENTITY_BYTES);
  });
});
