export const TICK_HZ = 30;
export const DT = 1 / TICK_HZ;
export const DT_MS = 1000 / TICK_HZ;

/** A client receives a snapshot every SNAPSHOT_DIVISOR ticks (30 / 2 = 15 Hz). */
export const SNAPSHOT_DIVISOR = 2;
export const SNAPSHOT_HZ = TICK_HZ / SNAPSHOT_DIVISOR;

export const WORLD_HALF = 120;

export const PLAYER_RADIUS = 0.4;
export const PLAYER_HEIGHT = 1.8;
export const MOVE_SPEED = 7;
export const GRAVITY = 25;
export const JUMP_SPEED = 9;

/** Interest management: enter at IN metres, leave beyond OUT (hysteresis avoids edge flicker). */
export const INTEREST_IN = 70;
export const INTEREST_OUT = 80;
export const MAX_VISIBLE = 63;

export const MAX_PLAYERS_PER_ROOM = 128;
export const MAX_INPUTS_PER_TICK = 2;
export const MAX_INBOX = 8;

export const TWO_PI = Math.PI * 2;
