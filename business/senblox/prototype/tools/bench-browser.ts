import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { chromium, type Browser } from 'playwright-core';
import { startServer } from '../server/index';
import { runBots } from './bots';

/**
 * Usage: tsx tools/bench-browser.ts [--bots 60] [--dur 15] [--runs 3]
 *
 * Measures, in the preinstalled headless Chromium:
 *  1. time to first playable frame under throttled mobile networks (HTTP assets only: CDP does not throttle WebSocket frames)
 *  2. in-page frame statistics with a crowd of bots in the room
 * IMPORTANT: headless Chromium here has no GPU (software rasteriser), so frame times are NOT evidence for H1.
 */
const arg = (n: string, d: string) => {
  const i = process.argv.indexOf(`--${n}`);
  return i >= 0 && process.argv[i + 1] ? process.argv[i + 1] : d;
};
const bots = Number(arg('bots', '60'));
const dur = Number(arg('dur', '15'));
const runs = Number(arg('runs', '3'));
const CHROMIUM = process.env.CHROMIUM_PATH ?? '/opt/pw-browsers/chromium';
const GL_ARGS = ['--no-sandbox', '--use-angle=swiftshader', '--use-gl=angle', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'];

if (!existsSync(CHROMIUM)) {
  console.error(`Chromium not found at ${CHROMIUM}; set CHROMIUM_PATH`);
  process.exit(2);
}

const PROFILES = {
  'unthrottled': null,
  'fast-4g': { down: 9_000_000, up: 1_500_000, latency: 40, cpu: 1 },
  'slow-4g': { down: 1_600_000, up: 750_000, latency: 150, cpu: 1 },
  'slow-4g+cpu4x': { down: 1_600_000, up: 750_000, latency: 150, cpu: 4 },
} as const;

const median = (a: number[]) => [...a].sort((x, y) => x - y)[Math.floor(a.length / 2)];

async function timeToFirstFrame(browser: Browser, base: string, name: keyof typeof PROFILES) {
  const times: number[] = [];
  let transfer = 0;
  for (let i = 0; i < runs; i++) {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 780 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
    const page = await ctx.newPage();
    const cdp = await ctx.newCDPSession(page);
    await cdp.send('Network.enable');
    await cdp.send('Network.setCacheDisabled', { cacheDisabled: true });
    const p = PROFILES[name];
    if (p) {
      await cdp.send('Network.emulateNetworkConditions', { offline: false, downloadThroughput: p.down / 8, uploadThroughput: p.up / 8, latency: p.latency });
      if (p.cpu > 1) await cdp.send('Emulation.setCPUThrottlingRate', { rate: p.cpu });
    }
    await page.goto(`${base}/w/ttff${i}`, { waitUntil: 'commit' });
    await page.waitForFunction(() => ((window as any).__senblox?.boot.firstFrameMs ?? 0) > 0, undefined, { timeout: 60000 });
    times.push(await page.evaluate(() => (window as any).__senblox.boot.firstFrameMs as number));
    transfer = await page.evaluate(() => {
      const res = performance.getEntriesByType('resource') as PerformanceResourceTiming[];
      const nav = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
      return res.reduce((a, r) => a + r.transferSize, 0) + nav.transferSize;
    });
    await ctx.close();
  }
  return { profile: name, medianMs: Math.round(median(times)), allMs: times.map(Math.round), transferBytes: transfer };
}

const server = await startServer({ port: 0, host: '127.0.0.1', quiet: true });
const base = `http://127.0.0.1:${server.port}`;
const browser = await chromium.launch({ executablePath: CHROMIUM, headless: true, args: GL_ARGS });
const result: Record<string, unknown> = { generatedAt: new Date().toISOString(), chromium: browser.version(), caveat: 'software rasteriser, localhost: not a real-device or real-network measurement' };

try {
  const ttff = [];
  for (const name of Object.keys(PROFILES) as (keyof typeof PROFILES)[]) {
    const r = await timeToFirstFrame(browser, base, name);
    ttff.push(r);
    console.log(`ttff ${name.padEnd(15)} median ${String(r.medianMs).padStart(5)} ms   runs ${r.allMs.join(', ')}   transfer ${(r.transferBytes / 1024).toFixed(0)} KiB`);
  }
  result.timeToFirstFrame = ttff;

  console.log(`\nframe benchmark: ${bots} bots in the room, ${dur}s recorded…`);
  const crowd = runBots({ url: base, room: 'crowd', count: bots, durationSec: dur + 14, clusterRadius: 30 });
  const ctx = await browser.newContext({ viewport: { width: 390, height: 780 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  const page = await ctx.newPage();
  await page.goto(`${base}/w/crowd?bench=1&dur=${dur}&warm=3`);
  await page.waitForFunction(() => (window as any).__senbloxReport, undefined, { timeout: (dur + 40) * 1000 });
  result.pageReport = await page.evaluate(() => (window as any).__senbloxReport);
  await ctx.close();
  result.serverDuringBench = (await crowd).server;
  const rep = result.pageReport as { frames: { fps: number; p50Ms: number; p95Ms: number }; h1: { valid: boolean; signal: string }; render: { resolutionScale: number; drawCalls: number }; net: { downKbitPerSec: number; visibleOthersMean: number } };
  console.log(`page: ${rep.frames.fps} fps  p50 ${rep.frames.p50Ms} ms  p95 ${rep.frames.p95Ms} ms  | ↓ ${rep.net.downKbitPerSec} kbit/s, ${rep.net.visibleOthersMean} visible | draw calls ${rep.render.drawCalls}`);
  console.log(`H1 signal: ${rep.h1.signal}  (valid=${rep.h1.valid})`);
} finally {
  await browser.close();
  await server.stop();
}

const dir = join(process.cwd(), 'reports');
mkdirSync(dir, { recursive: true });
const file = join(dir, `bench-${new Date().toISOString().replace(/[:.]/g, '-')}.json`);
writeFileSync(file, JSON.stringify(result, null, 2));
console.log(`\nsaved ${file}`);
process.exit(0);
