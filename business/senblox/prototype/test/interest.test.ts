import { describe, expect, it } from 'vitest';
import { INTEREST_IN, INTEREST_OUT, MAX_VISIBLE } from '../shared/config';
import { SpatialHash, selectVisible, type Positioned } from '../server/interest';

function setup(points: Positioned[]) {
  const hash = new SpatialHash<Positioned>();
  for (const p of points) hash.insert(p);
  return hash;
}

describe('interest management', () => {
  it('excludes self and far players, includes near players', () => {
    const me = { id: 1, x: 0, z: 0 };
    const near = { id: 2, x: INTEREST_IN - 5, z: 0 };
    const far = { id: 3, x: INTEREST_IN + 30, z: 0 };
    const hash = setup([me, near, far]);
    const out: Positioned[] = [];
    selectVisible(me, hash, new Set(), [], out);
    expect(out.map((p) => p.id)).toEqual([2]);
  });

  it('applies hysteresis: a known entity stays visible between IN and OUT', () => {
    const me = { id: 1, x: 0, z: 0 };
    const edge = { id: 2, x: (INTEREST_IN + INTEREST_OUT) / 2, z: 0 };
    const hash = setup([me, edge]);
    const out: Positioned[] = [];
    const known = new Set<number>();
    selectVisible(me, hash, known, [], out);
    expect(out).toHaveLength(0);
    known.add(2);
    selectVisible(me, hash, known, [], out);
    expect(out.map((p) => p.id)).toEqual([2]);
  });

  it('caps at MAX_VISIBLE keeping the nearest', () => {
    const me = { id: 0, x: 0, z: 0 };
    const crowd = Array.from({ length: MAX_VISIBLE + 20 }, (_, i) => ({ id: i + 1, x: 1 + i * 0.5, z: 0 }));
    const hash = setup([me, ...crowd]);
    const out: Positioned[] = [];
    selectVisible(me, hash, new Set(), [], out);
    expect(out).toHaveLength(MAX_VISIBLE);
    expect(Math.max(...out.map((p) => p.x))).toBeLessThan(1 + MAX_VISIBLE * 0.5);
  });
});
