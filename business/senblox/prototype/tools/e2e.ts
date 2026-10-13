import { existsSync } from 'node:fs';
import { chromium, type Page } from 'playwright-core';
import { startServer } from '../server/index';

const CHROMIUM = process.env.CHROMIUM_PATH ?? '/opt/pw-browsers/chromium';
// Headless CI has no GPU: force the software GL path so WebGL2 exists at all.
const GL_ARGS = ['--no-sandbox', '--use-angle=swiftshader', '--use-gl=angle', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'];

interface State {
  id: number;
  ready: boolean;
  x: number;
  y: number;
  z: number;
  remotes: number;
  snapshots: number;
  closed: boolean;
}

const failures: string[] = [];
const check = (name: string, ok: boolean, detail = '') => {
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${detail ? `  (${detail})` : ''}`);
  if (!ok) failures.push(name);
};

const state = (p: Page) => p.evaluate(() => (window as any).__senblox.state() as State);
const waitReady = (p: Page) => p.waitForFunction(() => (window as any).__senblox?.state().ready === true, undefined, { timeout: 20000 });

async function pixelVariety(page: Page): Promise<{ distinct: number; skyShare: number }> {
  const png = (await page.screenshot({ type: 'png' })).toString('base64');
  return page.evaluate(async (b64) => {
    const img = new Image();
    img.src = `data:image/png;base64,${b64}`;
    await img.decode();
    const c = document.createElement('canvas');
    c.width = img.width;
    c.height = img.height;
    const g = c.getContext('2d')!;
    g.drawImage(img, 0, 0);
    const seen = new Set<number>();
    let sky = 0;
    let total = 0;
    for (let y = 0; y < c.height; y += 8) {
      for (let x = 0; x < c.width; x += 8) {
        const [r, gg, b] = g.getImageData(x, y, 1, 1).data;
        seen.add(((r >> 3) << 10) | ((gg >> 3) << 5) | (b >> 3));
        total++;
        if (b > 170 && b > r + 20) sky++;
      }
    }
    return { distinct: seen.size, skyShare: sky / total };
  }, png);
}

if (!existsSync(CHROMIUM)) {
  console.error(`Chromium not found at ${CHROMIUM}; set CHROMIUM_PATH`);
  process.exit(2);
}

const server = await startServer({ port: 0, host: '127.0.0.1', quiet: true });
const base = `http://127.0.0.1:${server.port}`;
const browser = await chromium.launch({ executablePath: CHROMIUM, headless: true, args: GL_ARGS });
const errors: string[] = [];

try {
  const open = async () => {
    const ctx = await browser.newContext({ viewport: { width: 800, height: 500 } });
    const page = await ctx.newPage();
    page.on('pageerror', (e) => errors.push(`pageerror: ${e.message}`));
    page.on('console', (m) => m.type() === 'error' && errors.push(`console.error: ${m.text()}`));
    await page.goto(`${base}/w/e2e`);
    await waitReady(page);
    return page;
  };

  const a = await open();
  await a.waitForTimeout(800);
  const boot = await a.evaluate(() => (window as any).__senblox.boot as { firstFrameMs: number });
  const info = await a.evaluate(() => ({ backend: (window as any).__senblox.backend as string, gpu: (window as any).__senblox.gpu as string }));
  console.log(`renderer: ${info.backend} / ${info.gpu}`);
  check('client joins and receives first snapshot', (await state(a)).snapshots > 0);
  check('renders on WebGL2', info.backend === 'webgl2');

  const px = await pixelVariety(a);
  check('canvas is not blank', px.distinct > 40 && px.skyShare > 0.05, `distinct colours ${px.distinct}, sky ${(px.skyShare * 100).toFixed(0)}%`);

  const s0 = await state(a);
  await a.keyboard.down('KeyW');
  await a.waitForTimeout(1500);
  await a.keyboard.up('KeyW');
  await a.waitForTimeout(600);
  const s1 = await state(a);
  const moved = Math.hypot(s1.x - s0.x, s1.z - s0.z);
  check('keyboard moves the avatar', moved > 3, `${moved.toFixed(1)} m`);

  const serverPlayer = [...(server.rooms.get('e2e')?.players.values() ?? [])].find((p) => p.id === s1.id);
  const drift = serverPlayer ? Math.hypot(serverPlayer.state.x - s1.x, serverPlayer.state.z - s1.z) : Infinity;
  check('server position matches client prediction', drift < 1.0, `${drift.toFixed(2)} m apart`);

  let maxY = 0;
  await a.keyboard.down('Space');
  for (let i = 0; i < 8; i++) {
    await a.waitForTimeout(100);
    maxY = Math.max(maxY, (await state(a)).y);
  }
  await a.keyboard.up('Space');
  check('jump leaves the ground', maxY > 0.5, `peak ${maxY.toFixed(2)} m`);

  const b = await open();
  await a.waitForTimeout(1200);
  const [sa, sb] = [await state(a), await state(b)];
  check('two browsers see each other', sa.remotes >= 1 && sb.remotes >= 1, `A sees ${sa.remotes}, B sees ${sb.remotes}`);
  check('server holds both players', (server.rooms.get('e2e')?.size ?? 0) === 2);

  await b.close();
  await a.waitForTimeout(500);
  check('server drops a disconnected player', (server.rooms.get('e2e')?.size ?? 0) === 1);

  check('time to first frame under 15 s (localhost, software GL)', boot.firstFrameMs > 0 && boot.firstFrameMs < 15000, `${Math.round(boot.firstFrameMs)} ms`);
  check('no page or console errors', errors.length === 0, errors.slice(0, 3).join(' | '));
} finally {
  await browser.close();
  await server.stop();
}

console.log(failures.length ? `\n${failures.length} check(s) failed` : '\nall checks passed');
process.exit(failures.length ? 1 : 0);
