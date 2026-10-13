import { WORLD_HALF } from './config';

export interface Box {
  minX: number;
  maxX: number;
  minY: number;
  maxY: number;
  minZ: number;
  maxZ: number;
}

export type Prop =
  | { kind: 'rock'; x: number; y: number; z: number; sx: number; sy: number; sz: number; rot: number; hue: number }
  | { kind: 'tree'; x: number; z: number; h: number; r: number }
  | { kind: 'platform'; box: Box; hue: number };

const CELL = 8;

export class World {
  readonly half = WORLD_HALF;
  readonly boxes: Box[] = [];
  readonly props: Prop[] = [];
  private readonly dim = Math.ceil((WORLD_HALF * 2) / CELL);
  private readonly cells: number[][];
  private readonly stamp: Uint32Array;
  private queryId = 0;

  constructor(readonly seed: number) {
    this.cells = Array.from({ length: this.dim * this.dim }, () => []);
    generate(this, seed);
    this.stamp = new Uint32Array(this.boxes.length);
  }

  addBox(b: Box): number {
    const idx = this.boxes.push(b) - 1;
    const x0 = this.cellOf(b.minX);
    const x1 = this.cellOf(b.maxX);
    const z0 = this.cellOf(b.minZ);
    const z1 = this.cellOf(b.maxZ);
    for (let cz = z0; cz <= z1; cz++) for (let cx = x0; cx <= x1; cx++) this.cells[cz * this.dim + cx].push(idx);
    return idx;
  }

  private cellOf(v: number): number {
    const c = Math.floor((v + WORLD_HALF) / CELL);
    return c < 0 ? 0 : c >= this.dim ? this.dim - 1 : c;
  }

  /** Appends every box overlapping the XZ rectangle to `out` (deduplicated). */
  query(minX: number, maxX: number, minZ: number, maxZ: number, out: Box[]): void {
    out.length = 0;
    const id = ++this.queryId;
    const x0 = this.cellOf(minX);
    const x1 = this.cellOf(maxX);
    const z0 = this.cellOf(minZ);
    const z1 = this.cellOf(maxZ);
    for (let cz = z0; cz <= z1; cz++) {
      for (let cx = x0; cx <= x1; cx++) {
        for (const idx of this.cells[cz * this.dim + cx]) {
          if (this.stamp[idx] !== id) {
            this.stamp[idx] = id;
            out.push(this.boxes[idx]);
          }
        }
      }
    }
  }
}

function mulberry32(seed: number): () => number {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export function hashRoom(name: string): number {
  let h = 2166136261;
  for (let i = 0; i < name.length; i++) {
    h ^= name.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

const SPAWN_CLEAR = 9;

function generate(w: World, seed: number): void {
  const rnd = mulberry32(seed);
  const range = (a: number, b: number) => a + rnd() * (b - a);
  const place = () => range(-(WORLD_HALF - 8), WORLD_HALF - 8);
  const clearOfSpawn = (x: number, z: number, pad = 0) => Math.hypot(x, z) > SPAWN_CLEAR + pad;

  const H = WORLD_HALF;
  const wallH = 4;
  const wallT = 2;
  const walls: Box[] = [
    { minX: -H - wallT, maxX: H + wallT, minY: 0, maxY: wallH, minZ: -H - wallT, maxZ: -H },
    { minX: -H - wallT, maxX: H + wallT, minY: 0, maxY: wallH, minZ: H, maxZ: H + wallT },
    { minX: -H - wallT, maxX: -H, minY: 0, maxY: wallH, minZ: -H, maxZ: H },
    { minX: H, maxX: H + wallT, minY: 0, maxY: wallH, minZ: -H, maxZ: H },
  ];
  for (const b of walls) {
    w.addBox(b);
    w.props.push({ kind: 'platform', box: b, hue: 0.08 });
  }

  for (let i = 0; i < 220; i++) {
    const x = place();
    const z = place();
    if (!clearOfSpawn(x, z, 2)) continue;
    const sx = range(0.8, 3.2);
    const sz = range(0.8, 3.2);
    const sy = range(0.6, 2.4);
    w.addBox({ minX: x - sx / 2, maxX: x + sx / 2, minY: 0, maxY: sy, minZ: z - sz / 2, maxZ: z + sz / 2 });
    w.props.push({ kind: 'rock', x, y: 0, z, sx, sy, sz, rot: range(0, Math.PI), hue: range(0.05, 0.12) });
  }

  for (let i = 0; i < 160; i++) {
    const x = place();
    const z = place();
    if (!clearOfSpawn(x, z, 2)) continue;
    const h = range(3, 6);
    const r = range(0.9, 1.6);
    w.addBox({ minX: x - 0.35, maxX: x + 0.35, minY: 0, maxY: h, minZ: z - 0.35, maxZ: z + 0.35 });
    w.props.push({ kind: 'tree', x, z, h, r });
  }

  const stepH = 0.8;
  for (let s = 0; s < 6; s++) {
    const cx = place();
    const cz = place();
    if (!clearOfSpawn(cx, cz, 14)) continue;
    const dir = Math.floor(rnd() * 4);
    const hue = range(0.55, 0.75);
    const steps = 6;
    for (let i = 0; i < steps; i++) {
      const along = i * 2;
      const top = stepH * (i + 1);
      const b = stairBox(cx, cz, dir, along, along + 2, 4, top);
      w.addBox(b);
      w.props.push({ kind: 'platform', box: b, hue });
    }
    const topB = stairBox(cx, cz, dir, steps * 2, steps * 2 + 6, 6, stepH * steps);
    w.addBox(topB);
    w.props.push({ kind: 'platform', box: topB, hue });
  }

  for (let i = 0; i < 20; i++) {
    const x = place();
    const z = place();
    if (!clearOfSpawn(x, z, 4)) continue;
    const top = range(1, 3.5);
    const b: Box = { minX: x - 1.5, maxX: x + 1.5, minY: top - 0.5, maxY: top, minZ: z - 1.5, maxZ: z + 1.5 };
    w.addBox(b);
    w.props.push({ kind: 'platform', box: b, hue: range(0.85, 0.98) });
  }
}

function stairBox(cx: number, cz: number, dir: number, a0: number, a1: number, width: number, top: number): Box {
  const hw = width / 2;
  switch (dir) {
    case 0:
      return { minX: cx - hw, maxX: cx + hw, minY: 0, maxY: top, minZ: cz + a0, maxZ: cz + a1 };
    case 1:
      return { minX: cx - hw, maxX: cx + hw, minY: 0, maxY: top, minZ: cz - a1, maxZ: cz - a0 };
    case 2:
      return { minX: cx + a0, maxX: cx + a1, minY: 0, maxY: top, minZ: cz - hw, maxZ: cz + hw };
    default:
      return { minX: cx - a1, maxX: cx - a0, minY: 0, maxY: top, minZ: cz - hw, maxZ: cz + hw };
  }
}
