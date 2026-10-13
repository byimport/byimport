import { chromium } from 'playwright-core';
import { startServer } from '../server/index';
import { runBots } from './bots';

/** Usage: tsx tools/screenshot.ts <out.png> [bots=25] [width=960] [height=540] */
const out = process.argv[2];
if (!out) {
  console.error('usage: tsx tools/screenshot.ts <out.png> [bots] [width] [height]');
  process.exit(2);
}
const botCount = Number(process.argv[3] ?? 25);
const width = Number(process.argv[4] ?? 960);
const height = Number(process.argv[5] ?? 540);

const server = await startServer({ port: 0, host: '127.0.0.1', quiet: true });
const base = `http://127.0.0.1:${server.port}`;
const bots = runBots({ url: base, room: 'shot', count: botCount, durationSec: 8, clusterRadius: 14 });
const browser = await chromium.launch({
  executablePath: process.env.CHROMIUM_PATH ?? '/opt/pw-browsers/chromium',
  headless: true,
  args: ['--no-sandbox', '--use-angle=swiftshader', '--use-gl=angle', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'],
});
const page = await (await browser.newContext({ viewport: { width, height } })).newPage();
await page.goto(`${base}/w/shot`);
await page.waitForFunction(() => (window as any).__senblox?.state().ready, undefined, { timeout: 20000 });
await page.waitForTimeout(3500);
await page.screenshot({ path: out });
await browser.close();
await bots;
await server.stop();
console.log(`saved ${out}`);
process.exit(0);
