import { DT, GRAVITY, JUMP_SPEED, MOVE_SPEED, PLAYER_HEIGHT, PLAYER_RADIUS, TWO_PI, WORLD_HALF } from './config';
import type { Box, World } from './world';

export interface PlayerState {
  x: number;
  y: number;
  z: number;
  vy: number;
  yaw: number;
  grounded: boolean;
  moving: boolean;
}

export interface InputCmd {
  /** Strafe right = +1, in [-1, 1]. */
  mx: number;
  /** Forward = +1, in [-1, 1]. */
  mz: number;
  /** Camera yaw in radians; movement is relative to it. */
  camYaw: number;
  jump: boolean;
}

export function newPlayerState(x: number, z: number): PlayerState {
  return { x, y: 0, z, vy: 0, yaw: 0, grounded: true, moving: false };
}

export function cloneState(s: PlayerState): PlayerState {
  return { x: s.x, y: s.y, z: s.z, vy: s.vy, yaw: s.yaw, grounded: s.grounded, moving: s.moving };
}

export function wrapAngle(a: number): number {
  a %= TWO_PI;
  return a < 0 ? a + TWO_PI : a;
}

/**
 * Applies the exact quantisation the wire format uses, so client prediction and the
 * server consume bit-identical input values.
 */
export function quantizeInput(i: InputCmd): InputCmd {
  const q = (v: number) => Math.round(Math.max(-1, Math.min(1, v)) * 127) / 127;
  const yawU16 = Math.round((wrapAngle(i.camYaw) / TWO_PI) * 65536) & 0xffff;
  return { mx: q(i.mx), mz: q(i.mz), camYaw: (yawU16 * TWO_PI) / 65536, jump: i.jump };
}

const EPS = 1e-4;
const scratch: Box[] = [];

function overlaps(s: PlayerState, b: Box): boolean {
  return (
    s.x + PLAYER_RADIUS > b.minX &&
    s.x - PLAYER_RADIUS < b.maxX &&
    s.y + PLAYER_HEIGHT > b.minY &&
    s.y < b.maxY &&
    s.z + PLAYER_RADIUS > b.minZ &&
    s.z - PLAYER_RADIUS < b.maxZ
  );
}

function collect(s: PlayerState, world: World): void {
  const m = PLAYER_RADIUS + 0.05;
  world.query(s.x - m, s.x + m, s.z - m, s.z + m, scratch);
}

/** Advances one fixed tick (DT). Pure function of (state, input, world): deterministic on client and server. */
export function stepPlayer(s: PlayerState, inp: InputCmd, world: World): void {
  let ix = inp.mx;
  let iz = inp.mz;
  const len = Math.hypot(ix, iz);
  if (len > 1) {
    ix /= len;
    iz /= len;
  }
  const sin = Math.sin(inp.camYaw);
  const cos = Math.cos(inp.camYaw);
  // forward(yaw) = (-sin, -cos), right(yaw) = (cos, -sin)
  const wx = -sin * iz + cos * ix;
  const wz = -cos * iz - sin * ix;
  s.moving = len > 0.01;
  if (s.moving) s.yaw = wrapAngle(Math.atan2(-wx, -wz));

  const dx = wx * MOVE_SPEED * DT;
  if (dx !== 0) {
    s.x += dx;
    collect(s, world);
    for (const b of scratch) {
      if (!overlaps(s, b)) continue;
      s.x = dx > 0 ? b.minX - PLAYER_RADIUS - EPS : b.maxX + PLAYER_RADIUS + EPS;
    }
  }
  const dz = wz * MOVE_SPEED * DT;
  if (dz !== 0) {
    s.z += dz;
    collect(s, world);
    for (const b of scratch) {
      if (!overlaps(s, b)) continue;
      s.z = dz > 0 ? b.minZ - PLAYER_RADIUS - EPS : b.maxZ + PLAYER_RADIUS + EPS;
    }
  }
  const lim = WORLD_HALF - PLAYER_RADIUS;
  if (s.x > lim) s.x = lim;
  else if (s.x < -lim) s.x = -lim;
  if (s.z > lim) s.z = lim;
  else if (s.z < -lim) s.z = -lim;

  if (inp.jump && s.grounded) s.vy = JUMP_SPEED;
  s.vy -= GRAVITY * DT;
  s.y += s.vy * DT;
  let landed = false;
  if (s.y <= 0) {
    s.y = 0;
    if (s.vy < 0) s.vy = 0;
    landed = true;
  }
  collect(s, world);
  for (const b of scratch) {
    if (!overlaps(s, b)) continue;
    if (s.vy <= 0) {
      s.y = b.maxY;
      s.vy = 0;
      landed = true;
    } else {
      s.y = b.minY - PLAYER_HEIGHT - EPS;
      s.vy = 0;
    }
  }
  s.grounded = landed;
}
