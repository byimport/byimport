export interface MoveInput {
  mx: number;
  mz: number;
  jump: boolean;
}

const MOUSE_SENS = 0.0025;
const TOUCH_LOOK_SENS = 0.006;
const JOY_RADIUS = 56;

/** Keyboard + mouse (pointer lock) + floating touch joystick. Sampled once per fixed tick. */
export class Input {
  yaw = 0;
  pitch = 0.4;
  readonly isTouch = matchMedia('(pointer: coarse)').matches || 'ontouchstart' in window;

  private keys = new Set<string>();
  private joyId = -1;
  private joyOrigin = { x: 0, y: 0 };
  private joyVec = { x: 0, y: 0 };
  private lookId = -1;
  private lookLast = { x: 0, y: 0 };
  private touchJump = false;

  constructor(
    private canvas: HTMLCanvasElement,
    private joy: HTMLElement,
    private knob: HTMLElement,
    jumpBtn: HTMLElement,
  ) {
    if (this.isTouch) document.body.classList.add('touch');

    addEventListener('keydown', (e) => {
      this.keys.add(e.code);
      if (e.code === 'Space' || e.code.startsWith('Arrow')) e.preventDefault();
    });
    addEventListener('keyup', (e) => this.keys.delete(e.code));
    addEventListener('blur', () => this.keys.clear());

    canvas.addEventListener('click', () => {
      if (!this.isTouch && document.pointerLockElement !== canvas) void canvas.requestPointerLock?.();
    });
    addEventListener('mousemove', (e) => {
      if (document.pointerLockElement !== canvas) return;
      this.yaw -= e.movementX * MOUSE_SENS;
      this.pitch = clamp(this.pitch + e.movementY * MOUSE_SENS, -0.15, 1.25);
    });

    canvas.addEventListener('pointerdown', (e) => this.onDown(e));
    canvas.addEventListener('pointermove', (e) => this.onMove(e));
    const up = (e: PointerEvent) => this.onUp(e);
    canvas.addEventListener('pointerup', up);
    canvas.addEventListener('pointercancel', up);

    jumpBtn.addEventListener('pointerdown', (e) => {
      this.touchJump = true;
      e.stopPropagation();
    });
    const jumpUp = () => (this.touchJump = false);
    jumpBtn.addEventListener('pointerup', jumpUp);
    jumpBtn.addEventListener('pointercancel', jumpUp);
  }

  private onDown(e: PointerEvent): void {
    if (e.pointerType === 'mouse') return;
    this.canvas.setPointerCapture(e.pointerId);
    if (e.clientX < innerWidth / 2 && this.joyId < 0) {
      this.joyId = e.pointerId;
      this.joyOrigin = { x: e.clientX, y: e.clientY };
      this.joyVec = { x: 0, y: 0 };
      this.joy.style.display = 'block';
      this.joy.style.left = `${e.clientX}px`;
      this.joy.style.top = `${e.clientY}px`;
      this.knob.style.transform = 'translate(0,0)';
    } else if (this.lookId < 0) {
      this.lookId = e.pointerId;
      this.lookLast = { x: e.clientX, y: e.clientY };
    }
  }

  private onMove(e: PointerEvent): void {
    if (e.pointerId === this.joyId) {
      let dx = e.clientX - this.joyOrigin.x;
      let dy = e.clientY - this.joyOrigin.y;
      const len = Math.hypot(dx, dy);
      if (len > JOY_RADIUS) {
        dx = (dx / len) * JOY_RADIUS;
        dy = (dy / len) * JOY_RADIUS;
      }
      this.joyVec = { x: dx / JOY_RADIUS, y: dy / JOY_RADIUS };
      this.knob.style.transform = `translate(${dx}px, ${dy}px)`;
    } else if (e.pointerId === this.lookId) {
      this.yaw -= (e.clientX - this.lookLast.x) * TOUCH_LOOK_SENS;
      this.pitch = clamp(this.pitch + (e.clientY - this.lookLast.y) * TOUCH_LOOK_SENS, -0.15, 1.25);
      this.lookLast = { x: e.clientX, y: e.clientY };
    }
  }

  private onUp(e: PointerEvent): void {
    if (e.pointerId === this.joyId) {
      this.joyId = -1;
      this.joyVec = { x: 0, y: 0 };
      this.joy.style.display = 'none';
    } else if (e.pointerId === this.lookId) {
      this.lookId = -1;
    }
  }

  /** Keyboard camera turning, applied per rendered frame. */
  updateCamera(dtSec: number): void {
    const turn = (this.keys.has('KeyQ') ? 1 : 0) - (this.keys.has('KeyE') ? 1 : 0);
    this.yaw += turn * 2.2 * dtSec;
  }

  sample(): MoveInput {
    const k = this.keys;
    let mx = (k.has('KeyD') || k.has('ArrowRight') ? 1 : 0) - (k.has('KeyA') || k.has('ArrowLeft') ? 1 : 0);
    let mz = (k.has('KeyW') || k.has('ArrowUp') ? 1 : 0) - (k.has('KeyS') || k.has('ArrowDown') ? 1 : 0);
    if (this.joyId >= 0) {
      mx += this.joyVec.x;
      mz += -this.joyVec.y;
    }
    return { mx: clamp(mx, -1, 1), mz: clamp(mz, -1, 1), jump: k.has('Space') || this.touchJump };
  }
}

const clamp = (v: number, a: number, b: number) => (v < a ? a : v > b ? b : v);
