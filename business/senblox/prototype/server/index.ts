import { createServer, type IncomingMessage, type Server, type ServerResponse } from 'node:http';
import { existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import { extname, join, normalize, resolve, sep } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { gzipSync } from 'node:zlib';
import { WebSocketServer, type WebSocket } from 'ws';
import { DT_MS, MAX_PLAYERS_PER_ROOM } from '../shared/config';
import { Metrics } from './metrics';
import { Room, type Player } from './room';

const MIME: Record<string, string> = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.ico': 'image/x-icon',
};

const here = fileURLToPath(new URL('.', import.meta.url));
const defaultStaticDir = resolve(here, '../dist/client');
const defaultReportsDir = resolve(here, '../reports');

export interface ServerOptions {
  port?: number;
  host?: string;
  staticDir?: string;
  reportsDir?: string;
  quiet?: boolean;
}

export interface RunningServer {
  http: Server;
  port: number;
  rooms: Map<string, Room>;
  metrics: Metrics;
  stop(): Promise<void>;
}

interface CachedFile {
  raw: Buffer;
  gz: Buffer | null;
  mime: string;
  mtimeMs: number;
}

const ROOM_RE = /^[a-z0-9][a-z0-9-]{0,31}$/;

export function startServer(opts: ServerOptions = {}): Promise<RunningServer> {
  const staticDir = opts.staticDir ?? defaultStaticDir;
  const reportsDir = opts.reportsDir ?? defaultReportsDir;
  const metrics = new Metrics();
  const rooms = new Map<string, Room>();
  const cache = new Map<string, CachedFile>();
  const log = (...a: unknown[]) => {
    if (!opts.quiet) console.log(...a);
  };

  const loadFile = (path: string): CachedFile | null => {
    if (!existsSync(path) || !statSync(path).isFile()) return null;
    const st = statSync(path);
    const hit = cache.get(path);
    if (hit && hit.mtimeMs === st.mtimeMs) return hit;
    const raw = readFileSync(path);
    const mime = MIME[extname(path)] ?? 'application/octet-stream';
    const compressible = /^(text|application\/json|image\/svg)/.test(mime);
    const entry: CachedFile = { raw, gz: compressible ? gzipSync(raw, { level: 9 }) : null, mime, mtimeMs: st.mtimeMs };
    cache.set(path, entry);
    return entry;
  };

  const sendJson = (res: ServerResponse, code: number, body: unknown) => {
    const text = JSON.stringify(body, null, 2);
    res.writeHead(code, { 'content-type': 'application/json', 'cache-control': 'no-store' });
    res.end(text);
  };

  const serveStatic = (req: IncomingMessage, res: ServerResponse, pathname: string) => {
    let rel = normalize(decodeURIComponent(pathname)).replace(/^([/\\])+/, '');
    if (rel === '' || rel.endsWith(sep)) rel = join(rel, 'index.html');
    let file = resolve(staticDir, rel);
    if (file !== staticDir && !file.startsWith(staticDir + sep)) {
      res.writeHead(403).end('forbidden');
      return;
    }
    let entry = loadFile(file);
    if (!entry && extname(rel) === '') {
      file = join(staticDir, 'index.html');
      entry = loadFile(file);
    }
    if (!entry) {
      res.writeHead(404, { 'content-type': 'text/plain' });
      res.end(existsSync(staticDir) ? 'not found' : 'client not built: run `npm run build`');
      return;
    }
    const immutable = pathname.startsWith('/assets/');
    const headers: Record<string, string | number> = {
      'content-type': entry.mime,
      'cache-control': immutable ? 'public, max-age=31536000, immutable' : 'no-cache',
      vary: 'accept-encoding',
    };
    const acceptsGzip = /\bgzip\b/.test(String(req.headers['accept-encoding'] ?? ''));
    const body = acceptsGzip && entry.gz ? entry.gz : entry.raw;
    if (body === entry.gz) headers['content-encoding'] = 'gzip';
    headers['content-length'] = body.byteLength;
    res.writeHead(200, headers);
    res.end(req.method === 'HEAD' ? undefined : body);
  };

  const http = createServer((req, res) => {
    const url = new URL(req.url ?? '/', 'http://localhost');
    if (url.pathname === '/health') return void sendJson(res, 200, { ok: true });
    if (url.pathname === '/metrics') {
      let players = 0;
      for (const r of rooms.values()) players += r.size;
      const snap = metrics.snapshot(players, rooms.size);
      if (url.searchParams.get('reset') === '1') metrics.reset();
      return void sendJson(res, 200, snap);
    }
    if (url.pathname === '/report' && req.method === 'POST') {
      const chunks: Buffer[] = [];
      let size = 0;
      req.on('data', (c: Buffer) => {
        size += c.byteLength;
        if (size > 256 * 1024) req.destroy();
        else chunks.push(c);
      });
      req.on('end', () => {
        try {
          const parsed = JSON.parse(Buffer.concat(chunks).toString('utf8'));
          mkdirSync(reportsDir, { recursive: true });
          const name = `report-${new Date().toISOString().replace(/[:.]/g, '-')}.json`;
          writeFileSync(join(reportsDir, name), JSON.stringify(parsed, null, 2));
          log(`[report] saved ${name}`);
          sendJson(res, 200, { saved: name });
        } catch {
          sendJson(res, 400, { error: 'invalid json' });
        }
      });
      return;
    }
    if (req.method !== 'GET' && req.method !== 'HEAD') return void res.writeHead(405).end();
    serveStatic(req, res, url.pathname);
  });

  const wss = new WebSocketServer({ noServer: true, perMessageDeflate: false, maxPayload: 1024 });
  http.on('upgrade', (req, socket, head) => {
    const url = new URL(req.url ?? '/', 'http://localhost');
    if (url.pathname !== '/ws') return void socket.destroy();
    wss.handleUpgrade(req, socket, head, (ws) => onConnection(ws, url.searchParams.get('room') ?? 'lobby'));
  });

  const onConnection = (ws: WebSocket, roomName: string) => {
    if (!ROOM_RE.test(roomName)) return void ws.close(1008, 'bad room');
    let room = rooms.get(roomName);
    if (!room) rooms.set(roomName, (room = new Room(roomName, metrics)));
    if (room.size >= MAX_PLAYERS_PER_ROOM) return void ws.close(1013, 'room full');
    const player: Player = room.add(ws);
    const r = room;
    ws.on('message', (data: Buffer) => r.handle(player, data));
    ws.on('close', () => {
      r.remove(player);
      if (r.size === 0) rooms.delete(r.name);
    });
    ws.on('error', () => ws.terminate());
  };

  // One drift-corrected loop steps every room.
  let running = true;
  let next = performance.now() + DT_MS;
  let timer: NodeJS.Timeout;
  const loop = () => {
    const t0 = performance.now();
    const lateness = Math.max(0, t0 - next);
    for (const room of rooms.values()) room.step();
    metrics.recordTick(performance.now() - t0, lateness);
    next += DT_MS;
    const now = performance.now();
    if (now > next + DT_MS * 5) next = now + DT_MS;
    if (running) timer = setTimeout(loop, Math.max(0, next - now));
  };
  timer = setTimeout(loop, DT_MS);

  return new Promise((resolveStart) => {
    http.listen(opts.port ?? 8787, opts.host ?? '0.0.0.0', () => {
      const addr = http.address();
      const port = typeof addr === 'object' && addr ? addr.port : (opts.port ?? 8787);
      log(`Senblox prototype server on http://${opts.host ?? '0.0.0.0'}:${port}  (static: ${staticDir})`);
      resolveStart({
        http,
        port,
        rooms,
        metrics,
        stop: () =>
          new Promise<void>((done) => {
            running = false;
            clearTimeout(timer);
            for (const c of wss.clients) c.terminate();
            wss.close();
            http.closeAllConnections();
            http.close(() => done());
          }),
      });
    });
  });
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const port = Number(process.env.PORT ?? 8787);
  void startServer({ port, host: process.env.HOST ?? '0.0.0.0' });
}
