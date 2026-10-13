import { AdaptiveQuality, FrameClock, summarize } from './hud';
import { Input } from './input';
import { NetClient, type Avatar } from './net';
import { GameRenderer, createRenderer, type RendererMode } from './render';

const q = new URLSearchParams(location.search);
const bench = q.get('bench') === '1';
const benchDur = Number(q.get('dur') ?? 30);
const benchWarm = Number(q.get('warm') ?? 3);
const mode: RendererMode = q.get('renderer') === 'webgpu' ? 'webgpu' : 'webgl';
const adaptive = (q.get('adaptive') ?? (bench ? '0' : '1')) === '1';

const $ = <T extends HTMLElement>(id: string) => document.getElementById(id) as T;
const canvas = $<HTMLCanvasElement>('c');
const hudEl = $('hud');
const statusEl = $('status');

let room = location.pathname.startsWith('/w/') ? location.pathname.slice(3).split('/')[0] : '';
if (!room) {
  room = 'lobby';
  history.replaceState(null, '', `/w/${room}${location.search}`);
}

const boot: { firstSnapshotMs: number; firstFrameMs: number; connectedMs: number } = {
  firstSnapshotMs: 0,
  firstFrameMs: 0,
  connectedMs: 0,
};
const clock = new FrameClock();
const quality = new AdaptiveQuality();
const input = new Input(canvas, $('joy'), $('knob'), $('jump'));
const net = new NetClient();

$('invite').addEventListener('click', async () => {
  const url = `${location.origin}/w/${room}`;
  try {
    await navigator.clipboard.writeText(url);
    $('invite').textContent = 'Lien copié !';
  } catch {
    prompt('Lien à partager', url);
  }
  setTimeout(() => ($('invite').textContent = 'Copier le lien'), 1500);
});

async function main(): Promise<void> {
  const [info] = await Promise.all([createRenderer(canvas, mode), net.connect(room)]);
  boot.connectedMs = performance.now();
  const game = new GameRenderer(info.renderer, net.world!);
  if (info.note) console.warn(info.note);

  const avatars: Avatar[] = [];
  let last = performance.now();
  let netMark = { t: last, bytes: 0, snaps: 0, visible: 0 };
  let kbit = 0;
  let snapRate = 0;
  let visibleMean = 0;
  let lastQuality = last;
  let lastHud = 0;
  let recordingSince = 0;
  let benchStarted = false;
  let benchDone = false;
  let drawStats = { calls: 0, triangles: 0 };
  let firstFrameSeen = false;

  const frame = (now: number) => {
    const rawMs = now - last;
    const dtMs = Math.min(rawMs, 100); // simulation step is capped; the measured frame time is not
    last = now;
    if (rawMs > 0) clock.push(Math.min(rawMs, 1000));

    input.updateCamera(dtMs / 1000);
    net.update(dtMs, input);
    if (net.ready) {
      net.avatars(now, avatars);
      drawStats = game.render(avatars, input.yaw, input.pitch);
      if (!firstFrameSeen) {
        firstFrameSeen = true;
        boot.firstFrameMs = performance.now();
        boot.firstSnapshotMs = net.firstSnapshotAt;
        statusEl.style.display = 'none';
      }
    }

    if (now - netMark.t >= 1000) {
      const secs = (now - netMark.t) / 1000;
      kbit = ((net.bytesDown - netMark.bytes) * 8) / 1000 / secs;
      const ds = net.snapshots - netMark.snaps;
      snapRate = ds / secs;
      visibleMean = ds ? (net.visibleSum - netMark.visible) / ds : 0;
      netMark = { t: now, bytes: net.bytesDown, snaps: net.snapshots, visible: net.visibleSum };
    }

    if (adaptive && now - lastQuality >= 1000) {
      lastQuality = now;
      if (quality.tick(clock)) game.setQuality(quality.scale, quality.shadows);
    }

    if (now - lastHud > 250) {
      lastHud = now;
      const f = clock.live();
      hudEl.textContent =
        `SENBLOX  salle ${room}  (#${net.id})\n` +
        `rendu ${info.backend}${info.note ? ' (repli)' : ''}\n` +
        `fps ${f.fps.toFixed(0)}   ms p50 ${f.p50Ms} p95 ${f.p95Ms} p99 ${f.p99Ms}\n` +
        `ping ${net.pingMs.toFixed(0)} ms   ↓ ${kbit.toFixed(0)} kbit/s   snaps ${snapRate.toFixed(0)}/s\n` +
        `joueurs visibles ${visibleMean.toFixed(0)}   draw ${drawStats.calls}  tris ${(drawStats.triangles / 1000).toFixed(0)}k\n` +
        `échelle ${game.resolutionScale.toFixed(2)}  ombres ${game.shadows ? 'on' : 'off'}${adaptive ? '' : '  (adaptatif off)'}`;
    }

    if (bench && firstFrameSeen && !benchDone) {
      if (!benchStarted && now - boot.firstFrameMs >= benchWarm * 1000) {
        benchStarted = true;
        recordingSince = now;
        clock.startRecording();
      } else if (benchStarted && now - recordingSince >= benchDur * 1000) {
        benchDone = true;
        const frames = clock.stopRecording();
        void finishBench(frames, info, game, net, quality, { kbit, snapRate, visibleMean }, drawStats);
      }
    }
    requestAnimationFrame(frame);
  };
  requestAnimationFrame(frame);

  (window as unknown as Record<string, unknown>).__senblox = {
    boot,
    backend: info.backend,
    gpu: info.gpu,
    state: () => ({
      id: net.id,
      ready: net.ready,
      x: net.local.x,
      y: net.local.y,
      z: net.local.z,
      remotes: net.remoteCount,
      pingMs: net.pingMs,
      snapshots: net.snapshots,
      closed: net.closed,
    }),
  };
}

type Info = Awaited<ReturnType<typeof createRenderer>>;

async function finishBench(
  frames: number[],
  info: Info,
  game: GameRenderer,
  netc: NetClient,
  quality: AdaptiveQuality,
  rates: { kbit: number; snapRate: number; visibleMean: number },
  draw: { calls: number; triangles: number },
): Promise<void> {
  const stats = summarize(frames);
  const software = /swiftshader|llvmpipe|softpipe|software|microsoft basic/i.test(info.gpu);
  const res = performance.getEntriesByType('resource') as PerformanceResourceTiming[];
  const nav = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming | undefined;
  const transfer = res.reduce((a, r) => a + (r.transferSize || 0), 0) + (nav?.transferSize ?? 0);
  const decoded = res.reduce((a, r) => a + (r.decodedBodySize || 0), 0) + (nav?.decodedBodySize ?? 0);
  const signal = stats.p50Ms <= 17.5 && stats.p95Ms <= 20 ? 'meets-60fps' : stats.p95Ms <= 36 ? 'playable-30fps' : 'below-30fps';
  const nav2 = navigator as unknown as { deviceMemory?: number };
  const report = {
    when: new Date().toISOString(),
    url: location.href,
    userAgent: navigator.userAgent,
    device: {
      devicePixelRatio,
      screen: `${screen.width}x${screen.height}`,
      viewport: `${innerWidth}x${innerHeight}`,
      cores: navigator.hardwareConcurrency,
      memoryGB: nav2.deviceMemory ?? null,
    },
    renderer: { backend: info.backend, gpu: info.gpu, note: info.note ?? null },
    h1: {
      valid: !software,
      reason: software ? 'software rendering (CPU rasteriser): frame times say nothing about a real mobile GPU' : null,
      signal: software ? 'not-measurable' : signal,
      thresholds: 'meets-60fps = p50<=17.5ms and p95<=20ms; playable-30fps = p95<=36ms',
    },
    frames: stats,
    bootTimings: {
      connectedMs: Math.round(boot.connectedMs),
      firstSnapshotMs: Math.round(boot.firstSnapshotMs),
      firstFrameMs: Math.round(boot.firstFrameMs),
      note: 'measured from navigation start (performance.now()); the <15 s promise is judged on firstFrameMs',
    },
    download: { transferBytes: transfer, decodedBytes: decoded, requests: res.length + 1 },
    net: {
      pingMs: +netc.pingMs.toFixed(1),
      downKbitPerSec: +rates.kbit.toFixed(1),
      snapshotsPerSec: +rates.snapRate.toFixed(1),
      visibleOthersMean: +rates.visibleMean.toFixed(1),
    },
    render: {
      drawCalls: draw.calls,
      triangles: draw.triangles,
      resolutionScale: game.resolutionScale,
      shadows: game.shadows,
      adaptiveQualityChanges: quality.changes,
      benchSeconds: frames.length ? +(frames.reduce((a, b) => a + b, 0) / 1000).toFixed(1) : 0,
    },
  };
  (window as unknown as Record<string, unknown>).__senbloxReport = report;
  const text = JSON.stringify(report, null, 2);
  $<HTMLTextAreaElement>('reportText').value = text;
  $('report').style.display = 'flex';
  $('copyReport').onclick = () => void navigator.clipboard?.writeText(text);
  $('closeReport').onclick = () => ($('report').style.display = 'none');
  try {
    await fetch('/report', { method: 'POST', headers: { 'content-type': 'application/json' }, body: text });
  } catch {
    /* the on-screen copy is the source of truth */
  }
}

main().catch((e: Error) => {
  statusEl.textContent = `Erreur : ${e.message}`;
  console.error(e);
});
