import {
  BoxGeometry,
  CanvasTexture,
  CapsuleGeometry,
  Color,
  ConeGeometry,
  CylinderGeometry,
  DirectionalLight,
  FogExp2,
  HemisphereLight,
  IcosahedronGeometry,
  InstancedMesh,
  Mesh,
  MeshStandardMaterial,
  Object3D,
  PCFShadowMap,
  PerspectiveCamera,
  PlaneGeometry,
  RepeatWrapping,
  SRGBColorSpace,
  Scene,
  WebGLRenderer,
} from 'three';
import { WORLD_HALF } from '../shared/config';
import type { Box, World } from '../shared/world';
import type { Avatar } from './net';

export type RendererMode = 'webgl' | 'webgpu';

export interface RendererLike {
  domElement: HTMLCanvasElement;
  shadowMap: { enabled: boolean; type: number };
  info: { render: { calls: number; triangles: number } };
  setPixelRatio(v: number): void;
  setSize(w: number, h: number, updateStyle?: boolean): void;
  render(scene: Scene, camera: PerspectiveCamera): void;
}

export interface RendererInfo {
  renderer: RendererLike;
  backend: 'webgl2' | 'webgpu' | 'webgl2-via-webgpu-renderer';
  gpu: string;
  note?: string;
}

export async function createRenderer(canvas: HTMLCanvasElement, mode: RendererMode): Promise<RendererInfo> {
  let note: string | undefined;
  if (mode === 'webgpu') {
    if (!('gpu' in navigator)) {
      note = 'WebGPU unavailable in this browser: fell back to the WebGL renderer';
    } else {
      try {
        // Separate chunk: only downloaded when WebGPU is explicitly requested.
        const mod = await import('three/webgpu');
        const r = new mod.WebGPURenderer({ canvas, antialias: false, powerPreference: 'high-performance' });
        await r.init();
        const isGpu = !!(r as unknown as { backend?: { isWebGPUBackend?: boolean } }).backend?.isWebGPUBackend;
        let gpu = 'unknown';
        try {
          const adapter = await (navigator as unknown as { gpu: { requestAdapter(): Promise<{ info?: Record<string, string> } | null> } }).gpu.requestAdapter();
          if (adapter?.info) gpu = [adapter.info.vendor, adapter.info.architecture, adapter.info.description].filter(Boolean).join(' ') || 'unknown';
        } catch {
          /* adapter info is best effort */
        }
        return {
          renderer: r as unknown as RendererLike,
          backend: isGpu ? 'webgpu' : 'webgl2-via-webgpu-renderer',
          gpu,
        };
      } catch (e) {
        note = `WebGPU init failed (${(e as Error).message}): fell back to the WebGL renderer`;
      }
    }
  }
  const r = new WebGLRenderer({ canvas, antialias: false, powerPreference: 'high-performance' });
  const gl = r.getContext();
  const dbg = gl.getExtension('WEBGL_debug_renderer_info');
  const gpu = dbg ? String(gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL)) : 'unknown';
  return { renderer: r as unknown as RendererLike, backend: 'webgl2', gpu, note };
}

function grassTexture(): CanvasTexture {
  const c = document.createElement('canvas');
  c.width = c.height = 256;
  const g = c.getContext('2d')!;
  g.fillStyle = '#5b8f3d';
  g.fillRect(0, 0, 256, 256);
  let seed = 1337;
  const rnd = () => ((seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296);
  for (let i = 0; i < 1800; i++) {
    const l = 38 + rnd() * 22;
    g.fillStyle = `hsl(${88 + rnd() * 18}, ${38 + rnd() * 14}%, ${l}%)`;
    g.fillRect(rnd() * 256, rnd() * 256, 2 + rnd() * 5, 2 + rnd() * 5);
  }
  const t = new CanvasTexture(c);
  t.wrapS = t.wrapT = RepeatWrapping;
  t.repeat.set(70, 70);
  t.colorSpace = SRGBColorSpace;
  t.anisotropy = 4;
  return t;
}

const MAX_AVATARS = 160;
const dummy = new Object3D();
const tmpColor = new Color();

export class GameRenderer {
  readonly scene = new Scene();
  readonly camera = new PerspectiveCamera(65, 1, 0.1, 400);
  private readonly sun = new DirectionalLight(0xfff1d6, 2.4);
  private readonly bodies: InstancedMesh;
  private readonly noses: InstancedMesh;
  private basePixelRatio = Math.min(devicePixelRatio || 1, 2);
  private scale = 1;
  shadows = true;

  constructor(
    private readonly r: RendererLike,
    world: World,
  ) {
    const bg = new Color(0x9ec6e8);
    this.scene.background = bg;
    this.scene.fog = new FogExp2(bg, 0.0055);

    this.scene.add(new HemisphereLight(0xcfe4ff, 0x4d6a38, 1.15));
    this.sun.position.set(60, 100, 40);
    this.sun.castShadow = true;
    this.sun.shadow.mapSize.set(1024, 1024);
    const sc = this.sun.shadow.camera;
    sc.left = sc.bottom = -48;
    sc.right = sc.top = 48;
    sc.near = 1;
    sc.far = 260;
    this.sun.shadow.bias = -0.0006;
    this.sun.shadow.normalBias = 0.05;
    this.scene.add(this.sun, this.sun.target);

    r.shadowMap.enabled = true;
    r.shadowMap.type = PCFShadowMap;

    const ground = new Mesh(
      new PlaneGeometry(WORLD_HALF * 2 + 8, WORLD_HALF * 2 + 8),
      new MeshStandardMaterial({ map: grassTexture(), roughness: 0.96, metalness: 0 }),
    );
    ground.rotation.x = -Math.PI / 2;
    ground.receiveShadow = true;
    this.scene.add(ground);

    this.buildProps(world);

    const bodyMat = new MeshStandardMaterial({ roughness: 0.55, metalness: 0.05 });
    this.bodies = new InstancedMesh(new CapsuleGeometry(0.4, 1.0, 3, 8), bodyMat, MAX_AVATARS);
    const noseMat = new MeshStandardMaterial({ color: 0xffffff, roughness: 0.6 });
    this.noses = new InstancedMesh(new BoxGeometry(0.3, 0.22, 0.36), noseMat, MAX_AVATARS);
    for (const m of [this.bodies, this.noses]) {
      m.frustumCulled = false;
      m.castShadow = true;
      m.count = 0;
      this.scene.add(m);
    }
    this.applySize();
    addEventListener('resize', () => this.applySize());
  }

  private buildProps(world: World): void {
    const rocks = world.props.filter((p) => p.kind === 'rock');
    const trees = world.props.filter((p) => p.kind === 'tree');
    const plats = world.props.filter((p) => p.kind === 'platform');

    const rockMesh = new InstancedMesh(
      new IcosahedronGeometry(0.5, 0),
      new MeshStandardMaterial({ flatShading: true, roughness: 0.92 }),
      Math.max(1, rocks.length),
    );
    rocks.forEach((p, i) => {
      if (p.kind !== 'rock') return;
      dummy.position.set(p.x, p.sy / 2, p.z);
      dummy.rotation.set(0, p.rot, 0);
      dummy.scale.set(p.sx, p.sy, p.sz);
      dummy.updateMatrix();
      rockMesh.setMatrixAt(i, dummy.matrix);
      rockMesh.setColorAt(i, tmpColor.setHSL(p.hue, 0.12, 0.42 + (i % 5) * 0.025));
    });

    const trunkGeo = new CylinderGeometry(0.25, 0.35, 1, 6);
    trunkGeo.translate(0, 0.5, 0);
    const trunks = new InstancedMesh(trunkGeo, new MeshStandardMaterial({ color: 0x6b4a2b, roughness: 1 }), Math.max(1, trees.length));
    const coneGeo = new ConeGeometry(1, 1, 7);
    coneGeo.translate(0, 0.5, 0);
    const canopies = new InstancedMesh(coneGeo, new MeshStandardMaterial({ roughness: 0.9, flatShading: true }), Math.max(1, trees.length));
    trees.forEach((p, i) => {
      if (p.kind !== 'tree') return;
      dummy.position.set(p.x, 0, p.z);
      dummy.rotation.set(0, 0, 0);
      dummy.scale.set(1, p.h * 0.6, 1);
      dummy.updateMatrix();
      trunks.setMatrixAt(i, dummy.matrix);
      dummy.position.set(p.x, p.h * 0.3, p.z);
      dummy.scale.set(p.r, p.h * 0.75, p.r);
      dummy.updateMatrix();
      canopies.setMatrixAt(i, dummy.matrix);
      canopies.setColorAt(i, tmpColor.setHSL(0.3 + (i % 7) * 0.01, 0.5, 0.28 + (i % 4) * 0.03));
    });

    const boxMesh = new InstancedMesh(new BoxGeometry(1, 1, 1), new MeshStandardMaterial({ roughness: 0.8 }), Math.max(1, plats.length));
    plats.forEach((p, i) => {
      if (p.kind !== 'platform') return;
      const b: Box = p.box;
      dummy.position.set((b.minX + b.maxX) / 2, (b.minY + b.maxY) / 2, (b.minZ + b.maxZ) / 2);
      dummy.rotation.set(0, 0, 0);
      dummy.scale.set(b.maxX - b.minX, b.maxY - b.minY, b.maxZ - b.minZ);
      dummy.updateMatrix();
      boxMesh.setMatrixAt(i, dummy.matrix);
      boxMesh.setColorAt(i, tmpColor.setHSL(p.hue, 0.45, 0.55));
    });

    for (const m of [rockMesh, trunks, canopies, boxMesh]) {
      m.castShadow = true;
      m.receiveShadow = true;
      m.frustumCulled = false;
      m.instanceMatrix.needsUpdate = true;
      if (m.instanceColor) m.instanceColor.needsUpdate = true;
      this.scene.add(m);
    }
  }

  setQuality(scale: number, shadows: boolean): void {
    this.scale = scale;
    if (this.shadows !== shadows) {
      this.shadows = shadows;
      this.sun.castShadow = shadows;
    }
    this.applySize();
  }

  get resolutionScale(): number {
    return this.scale;
  }

  private applySize(): void {
    this.r.setPixelRatio(this.basePixelRatio * this.scale);
    this.r.setSize(innerWidth, innerHeight, false);
    this.camera.aspect = innerWidth / innerHeight;
    this.camera.updateProjectionMatrix();
  }

  render(avatars: Avatar[], yaw: number, pitch: number): { calls: number; triangles: number } {
    let n = 0;
    for (const a of avatars) {
      if (n >= MAX_AVATARS) break;
      dummy.position.set(a.x, a.y + 0.9, a.z);
      dummy.rotation.set(0, a.yaw, 0);
      dummy.scale.set(1, 1, 1);
      dummy.updateMatrix();
      this.bodies.setMatrixAt(n, dummy.matrix);
      this.bodies.setColorAt(n, a.self ? tmpColor.setHSL(((a.id * 0.618034) % 1), 0.9, 0.62) : tmpColor.setHSL(((a.id * 0.618034) % 1), 0.6, 0.5));
      // Nose sits in front of the face (local -Z) so facing is readable at a glance.
      dummy.position.set(a.x - Math.sin(a.yaw) * 0.42, a.y + 1.25, a.z - Math.cos(a.yaw) * 0.42);
      dummy.updateMatrix();
      this.noses.setMatrixAt(n, dummy.matrix);
      n++;
    }
    this.bodies.count = this.noses.count = n;
    this.bodies.instanceMatrix.needsUpdate = this.noses.instanceMatrix.needsUpdate = true;
    if (this.bodies.instanceColor) this.bodies.instanceColor.needsUpdate = true;

    const self = avatars[0];
    if (self) {
      const dist = 6.5;
      const cp = Math.cos(pitch);
      this.camera.position.set(
        self.x + Math.sin(yaw) * cp * dist,
        self.y + 1.4 + Math.sin(pitch) * dist,
        self.z + Math.cos(yaw) * cp * dist,
      );
      this.camera.lookAt(self.x, self.y + 1.2, self.z);
      this.sun.position.set(self.x + 60, 100, self.z + 40);
      this.sun.target.position.set(self.x, 0, self.z);
    }
    this.r.render(this.scene, this.camera);
    return { calls: this.r.info.render.calls, triangles: this.r.info.render.triangles };
  }
}
