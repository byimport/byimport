import { INTEREST_IN, INTEREST_OUT, MAX_VISIBLE } from '../shared/config';

export interface Positioned {
  id: number;
  x: number;
  z: number;
}

const CELL = 32;

/** Uniform grid rebuilt every tick; cheap enough for a few hundred players per room. */
export class SpatialHash<T extends Positioned> {
  private cells = new Map<number, T[]>();

  private key(cx: number, cz: number): number {
    return (cx + 512) * 1024 + (cz + 512);
  }

  clear(): void {
    for (const arr of this.cells.values()) arr.length = 0;
  }

  insert(p: T): void {
    const k = this.key(Math.floor(p.x / CELL), Math.floor(p.z / CELL));
    let arr = this.cells.get(k);
    if (!arr) this.cells.set(k, (arr = []));
    arr.push(p);
  }

  query(x: number, z: number, r: number, out: T[]): void {
    const x0 = Math.floor((x - r) / CELL);
    const x1 = Math.floor((x + r) / CELL);
    const z0 = Math.floor((z - r) / CELL);
    const z1 = Math.floor((z + r) / CELL);
    for (let cz = z0; cz <= z1; cz++) {
      for (let cx = x0; cx <= x1; cx++) {
        const arr = this.cells.get(this.key(cx, cz));
        if (arr) for (const p of arr) out.push(p);
      }
    }
  }
}

/**
 * Picks the entities `self` should receive. An entity enters at INTEREST_IN and stays until
 * INTEREST_OUT (hysteresis). Capped at MAX_VISIBLE, nearest first. Updates `known` in place.
 */
export function selectVisible<T extends Positioned>(
  self: Positioned,
  hash: SpatialHash<T>,
  known: Set<number>,
  scratch: T[],
  out: T[],
): void {
  scratch.length = 0;
  out.length = 0;
  hash.query(self.x, self.z, INTEREST_OUT, scratch);
  const inSq = INTEREST_IN * INTEREST_IN;
  const outSq = INTEREST_OUT * INTEREST_OUT;
  for (const p of scratch) {
    if (p.id === self.id) continue;
    const dx = p.x - self.x;
    const dz = p.z - self.z;
    const d2 = dx * dx + dz * dz;
    if (d2 <= inSq || (d2 <= outSq && known.has(p.id))) out.push(p);
  }
  if (out.length > MAX_VISIBLE) {
    const d2 = (p: T) => (p.x - self.x) ** 2 + (p.z - self.z) ** 2;
    out.sort((a, b) => d2(a) - d2(b));
    out.length = MAX_VISIBLE;
  }
  known.clear();
  for (const p of out) known.add(p.id);
}
