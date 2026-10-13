const WINDOW = 1800;

function percentile(sorted: Float64Array, n: number, p: number): number {
  if (n === 0) return 0;
  return sorted[Math.min(n - 1, Math.floor((p / 100) * n))];
}

export class Metrics {
  private tickMs = new Float64Array(WINDOW);
  private lateMs = new Float64Array(WINDOW);
  private n = 0;
  private cursor = 0;
  private startedAt = performance.now();
  bytesOut = 0;
  messagesOut = 0;
  bytesIn = 0;
  private cpu0 = process.cpuUsage();
  private rss0 = process.memoryUsage().rss;

  recordTick(durationMs: number, latenessMs: number): void {
    this.tickMs[this.cursor] = durationMs;
    this.lateMs[this.cursor] = latenessMs;
    this.cursor = (this.cursor + 1) % WINDOW;
    if (this.n < WINDOW) this.n++;
  }

  reset(): void {
    this.n = 0;
    this.cursor = 0;
    this.bytesOut = 0;
    this.messagesOut = 0;
    this.bytesIn = 0;
    this.startedAt = performance.now();
    this.cpu0 = process.cpuUsage();
    this.rss0 = process.memoryUsage().rss;
  }

  snapshot(players: number, rooms: number) {
    const sortedTick = Float64Array.from(this.tickMs.subarray(0, this.n)).sort();
    const sortedLate = Float64Array.from(this.lateMs.subarray(0, this.n)).sort();
    const secs = (performance.now() - this.startedAt) / 1000;
    const cpu = process.cpuUsage(this.cpu0);
    const mem = process.memoryUsage();
    const mean = this.n ? sortedTick.reduce((a, b) => a + b, 0) / this.n : 0;
    return {
      windowSeconds: +secs.toFixed(1),
      players,
      rooms,
      tickMs: {
        samples: this.n,
        mean: +mean.toFixed(3),
        p50: +percentile(sortedTick, this.n, 50).toFixed(3),
        p95: +percentile(sortedTick, this.n, 95).toFixed(3),
        p99: +percentile(sortedTick, this.n, 99).toFixed(3),
        max: +(this.n ? sortedTick[this.n - 1] : 0).toFixed(3),
      },
      schedulerLatenessMs: {
        p50: +percentile(sortedLate, this.n, 50).toFixed(3),
        p99: +percentile(sortedLate, this.n, 99).toFixed(3),
        max: +(this.n ? sortedLate[this.n - 1] : 0).toFixed(3),
      },
      network: {
        bytesOut: this.bytesOut,
        bytesIn: this.bytesIn,
        outKbitPerSecTotal: +((this.bytesOut * 8) / 1000 / Math.max(secs, 0.001)).toFixed(1),
        outKbitPerSecPerPlayer: players ? +((this.bytesOut * 8) / 1000 / Math.max(secs, 0.001) / players).toFixed(2) : 0,
      },
      process: {
        cpuPercentOfOneCore: +((((cpu.user + cpu.system) / 1000) / (secs * 1000)) * 100).toFixed(1),
        rssMB: +(mem.rss / 1048576).toFixed(1),
        rssGrowthMB: +((mem.rss - this.rss0) / 1048576).toFixed(1),
        heapUsedMB: +(mem.heapUsed / 1048576).toFixed(1),
      },
    };
  }
}
