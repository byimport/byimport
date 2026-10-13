export interface FrameStats {
  count: number;
  fps: number;
  meanMs: number;
  p50Ms: number;
  p95Ms: number;
  p99Ms: number;
  maxMs: number;
  over16Pct: number;
  over33Pct: number;
}

const pct = (sorted: number[], p: number) => (sorted.length ? sorted[Math.min(sorted.length - 1, Math.floor((p / 100) * sorted.length))] : 0);

export function summarize(frames: number[]): FrameStats {
  const s = [...frames].sort((a, b) => a - b);
  const total = frames.reduce((a, b) => a + b, 0);
  const n = frames.length;
  const r = (v: number) => +v.toFixed(2);
  return {
    count: n,
    fps: n ? r(1000 / (total / n)) : 0,
    meanMs: n ? r(total / n) : 0,
    p50Ms: r(pct(s, 50)),
    p95Ms: r(pct(s, 95)),
    p99Ms: r(pct(s, 99)),
    maxMs: r(s[n - 1] ?? 0),
    over16Pct: n ? r((frames.filter((f) => f > 16.9).length / n) * 100) : 0,
    over33Pct: n ? r((frames.filter((f) => f > 33.5).length / n) * 100) : 0,
  };
}

/** Rolling frame-time window shown live, plus an unbounded recorder for benchmark runs. */
export class FrameClock {
  private recent: number[] = [];
  private recording: number[] | null = null;

  push(dtMs: number): void {
    this.recent.push(dtMs);
    if (this.recent.length > 300) this.recent.shift();
    this.recording?.push(dtMs);
  }

  startRecording(): void {
    this.recording = [];
  }

  stopRecording(): number[] {
    const r = this.recording ?? [];
    this.recording = null;
    return r;
  }

  live(): FrameStats {
    return summarize(this.recent);
  }

  /** Mean/p95 over the last `n` frames, used by the adaptive-quality controller. */
  tail(n: number): { mean: number; p95: number } {
    const w = this.recent.slice(-n);
    if (!w.length) return { mean: 0, p95: 0 };
    const sorted = [...w].sort((a, b) => a - b);
    return { mean: w.reduce((a, b) => a + b, 0) / w.length, p95: pct(sorted, 95) };
  }
}

/** Lowers resolution (then shadows) when frames are slow, and cautiously probes upwards again. */
export class AdaptiveQuality {
  scale = 1;
  shadows = true;
  changes = 0;
  private goodWindows = 0;
  private needGood = 6;

  /** Call once per second. Returns true when quality changed. */
  tick(clock: FrameClock): boolean {
    const t = clock.tail(60);
    if (t.mean === 0) return false;
    const slow = t.mean > 21 || t.p95 > 28;
    const good = t.mean < 18.5 && t.p95 < 22;
    if (slow) {
      this.goodWindows = 0;
      if (this.scale > 0.5) this.scale = Math.max(0.5, +(this.scale - 0.125).toFixed(3));
      else if (this.shadows) this.shadows = false;
      else return false;
      this.needGood = Math.min(60, this.needGood * 2);
      this.changes++;
      return true;
    }
    if (good) {
      if (++this.goodWindows >= this.needGood) {
        this.goodWindows = 0;
        if (!this.shadows && this.scale >= 0.75) this.shadows = true;
        else if (this.scale < 1) this.scale = Math.min(1, +(this.scale + 0.125).toFixed(3));
        else return false;
        this.changes++;
        return true;
      }
    } else this.goodWindows = 0;
    return false;
  }
}
