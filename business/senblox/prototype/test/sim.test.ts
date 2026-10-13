import { describe, expect, it } from 'vitest';
import { DT, PLAYER_HEIGHT, PLAYER_RADIUS } from '../shared/config';
import { cloneState, newPlayerState, quantizeInput, stepPlayer, type InputCmd } from '../shared/sim';
import { World } from '../shared/world';

const world = new World(12345);
const walk: InputCmd = { mx: 0, mz: 1, camYaw: 0, jump: false };

function run(cmds: InputCmd[], start = newPlayerState(0, 0)) {
  const s = cloneState(start);
  for (const c of cmds) stepPlayer(s, quantizeInput(c), world);
  return s;
}

describe('world', () => {
  it('is deterministic for a given seed and differs across seeds', () => {
    const a = new World(7);
    const b = new World(7);
    const c = new World(8);
    expect(a.boxes).toEqual(b.boxes);
    expect(a.boxes).not.toEqual(c.boxes);
  });

  it('keeps the spawn area free of obstacles', () => {
    const out: unknown[] = [];
    world.query(-6, 6, -6, 6, out as never);
    expect(out.length).toBe(0);
  });
});

describe('stepPlayer', () => {
  it('is deterministic: identical inputs give identical state', () => {
    const cmds = Array.from({ length: 120 }, (_, i) => ({
      mx: Math.sin(i / 7),
      mz: Math.cos(i / 5),
      camYaw: i / 30,
      jump: i % 40 === 0,
    }));
    expect(run(cmds)).toEqual(run(cmds));
  });

  it('moves forward at the configured speed', () => {
    const s = run(Array.from({ length: 30 }, () => walk));
    // forward at yaw 0 is -Z; 30 ticks = 1 second at 7 m/s
    expect(s.z).toBeCloseTo(-7, 1);
    expect(Math.abs(s.x)).toBeLessThan(1e-6);
  });

  it('jumps and lands back on the ground', () => {
    const s = newPlayerState(0, 0);
    stepPlayer(s, { ...walk, mz: 0, jump: true }, world);
    expect(s.y).toBeGreaterThan(0);
    expect(s.grounded).toBe(false);
    for (let i = 0; i < 90; i++) stepPlayer(s, { ...walk, mz: 0 }, world);
    expect(s.y).toBe(0);
    expect(s.grounded).toBe(true);
  });

  it('cannot walk through a solid obstacle', () => {
    const rock = world.boxes.find((b) => b.minY === 0 && b.maxY < 3 && b.maxX - b.minX < 4 && Math.abs(b.minX) < 100 && Math.abs(b.minZ) < 100)!;
    const cx = (rock.minX + rock.maxX) / 2;
    const s = newPlayerState(cx, rock.maxZ + 3);
    for (let i = 0; i < 150; i++) stepPlayer(s, walk, world); // walk towards -Z into it
    const penetrates =
      s.x + PLAYER_RADIUS > rock.minX + 1e-3 &&
      s.x - PLAYER_RADIUS < rock.maxX - 1e-3 &&
      s.y + PLAYER_HEIGHT > rock.minY + 1e-3 &&
      s.y < rock.maxY - 1e-3 &&
      s.z + PLAYER_RADIUS > rock.minZ + 1e-3 &&
      s.z - PLAYER_RADIUS < rock.maxZ - 1e-3;
    expect(penetrates).toBe(false);
    // and it really was blocked: it started 3 m in front and walked 5 m
    expect(s.z).toBeGreaterThan(rock.minZ);
  });

  it('lands on top of a platform when jumping onto it', () => {
    const step = world.boxes.find((b) => b.minY === 0 && Math.abs(b.maxY - 0.8) < 1e-9)!;
    const s = newPlayerState((step.minX + step.maxX) / 2, (step.minZ + step.maxZ) / 2);
    s.y = step.maxY + 1.5;
    for (let i = 0; i < 60; i++) stepPlayer(s, { mx: 0, mz: 0, camYaw: 0, jump: false }, world);
    expect(s.y).toBeCloseTo(step.maxY, 3);
    expect(s.grounded).toBe(true);
    expect(PLAYER_HEIGHT).toBeGreaterThan(0);
  });
});

describe('client prediction vs authoritative server', () => {
  it('replaying unacknowledged inputs on a server state reproduces the predicted state', () => {
    const cmds = Array.from({ length: 90 }, (_, i) => ({
      mx: i % 50 < 25 ? 1 : -1,
      mz: 1,
      camYaw: 0.4,
      jump: i % 31 === 0,
    })).map(quantizeInput);

    // The client predicts everything; the server has only processed the first 60 inputs.
    const client = newPlayerState(1, 1);
    for (const c of cmds) stepPlayer(client, c, world);
    const server = newPlayerState(1, 1);
    for (const c of cmds.slice(0, 60)) stepPlayer(server, c, world);

    // Client reconciles: adopt server state, replay inputs 61..90.
    const reconciled = cloneState(server);
    for (const c of cmds.slice(60)) stepPlayer(reconciled, c, world);

    expect(reconciled.x).toBeCloseTo(client.x, 9);
    expect(reconciled.y).toBeCloseTo(client.y, 9);
    expect(reconciled.z).toBeCloseTo(client.z, 9);
    expect(DT).toBeGreaterThan(0);
  });
});
