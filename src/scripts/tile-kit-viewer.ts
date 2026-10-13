import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { STLLoader } from 'three/addons/loaders/STLLoader.js';

interface Part {
  id: string;
  name: string;
  family: 'side' | 'top' | 'base';
  file: string;
  dimensions: number[];
  sourceBounds: number[][];
}
interface Manifest {
  parts: Part[];
  matingTopHeight: number;
}

export async function mountTileKit(root: HTMLElement) {
  const manifestUrl = new URL(root.dataset.kitUrl!, location.href);
  const response = await fetch(manifestUrl);
  if (!response.ok) throw new Error('Tile manifest could not load');
  const manifest: Manifest = await response.json();
  const loader = new STLLoader();
  const geometries = await Promise.all(
    manifest.parts.map(async (part) => {
      const geometry = await loader.loadAsync(new URL(part.file, manifestUrl).href);
      geometry.computeVertexNormals();
      return geometry;
    }),
  );
  root.querySelector<HTMLElement>('.viewer-loaded')!.hidden = false;
  const stage = root.querySelector<HTMLElement>('.kit-stage')!;
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.setClearColor(0xe1e8df);
  stage.append(renderer.domElement);
  renderer.domElement.tabIndex = 0;
  renderer.domElement.setAttribute(
    'aria-label',
    'Interactive 3D tile kit. Arrow keys rotate; plus and minus zoom.',
  );
  const scene = new THREE.Scene();
  scene.add(new THREE.HemisphereLight(0xfff9e6, 0x485749, 2.7));
  const key = new THREE.DirectionalLight(0xffffff, 3.5);
  key.position.set(-60, -90, 150);
  scene.add(key);
  const camera = new THREE.PerspectiveCamera(38, 1, 0.1, 3000);
  camera.up.set(0, 0, 1);
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = false;
  controls.minDistance = 35;
  controls.maxDistance = 1300;
  const objects = new THREE.Group();
  scene.add(objects);
  const colors = { side: 0x4b977b, top: 0xd5ac52, base: 0xc66d5b };
  const materials = manifest.parts.map(
    (part) =>
      new THREE.MeshStandardMaterial({
        color: colors[part.family],
        roughness: 0.72,
        metalness: 0.03,
      }),
  );
  const meshes = manifest.parts.map((_, i) => new THREE.Mesh(geometries[i], materials[i]));
  meshes.forEach((mesh) => objects.add(mesh));
  const mode = root.querySelector<HTMLSelectElement>('.kit-mode')!;
  const separation = root.querySelector<HTMLInputElement>('.kit-separation')!;
  const details = root.querySelector<HTMLElement>('.kit-details')!;
  const render = () => renderer.render(scene, camera);
  controls.addEventListener('change', render);
  const fit = () => {
    const bounds = new THREE.Box3();
    meshes.filter((m) => m.visible).forEach((mesh) => bounds.expandByObject(mesh));
    const center = bounds.getCenter(new THREE.Vector3());
    const span = bounds.getSize(new THREE.Vector3()).length();
    const distance = Math.max(span * 1.55, 110);
    controls.target.copy(center);
    camera.position.copy(center).add(new THREE.Vector3(distance * 0.8, -distance, distance * 0.7));
    controls.update();
    render();
  };
  const show = (resetCamera = true) => {
    meshes.forEach((mesh) => {
      mesh.visible = false;
      mesh.position.set(0, 0, 0);
    });
    root.querySelector<HTMLElement>('.separation-control')!.hidden = mode.value !== 'pair';
    if (mode.value === 'pair') {
      ['bottom-zero', 'top-one'].forEach((id) => {
        const i = manifest.parts.findIndex((part) => part.id === id);
        const part = manifest.parts[i];
        meshes[i].visible = true;
        meshes[i].position.fromArray(part.sourceBounds[0]);
        if (id === 'top-one')
          meshes[i].position.z += manifest.matingTopHeight + Number(separation.value);
      });
      details.textContent = `Two construction pieces: a base with the core, and an output face. Separation: ${separation.value} mm. Side panels complete a configurable cube; cubes are then combined into tiles. Physical fit remains to be tested.`;
    } else if (mode.value === 'all') {
      meshes.forEach((mesh, i) => {
        mesh.visible = true;
        mesh.position.set((i % 5) * 70, Math.floor(i / 5) * 75, 0);
      });
      details.textContent =
        'All ten construction-piece designs: two sides, four tops, and four bases with the core built in. This is the basic construction level.';
    } else {
      const i = manifest.parts.findIndex((part) => part.id === mode.value);
      meshes[i].visible = true;
      const part = manifest.parts[i];
      details.textContent = `${part.name} · ${part.dimensions.join(' × ')} mm · View both faces to see the connections.`;
    }
    if (resetCamera) fit();
    else render();
  };
  mode.addEventListener('change', () => show());
  separation.addEventListener('input', () => show(false));
  root.querySelector<HTMLButtonElement>('.kit-reset')!.addEventListener('click', fit);
  renderer.domElement.addEventListener('keydown', (event) => {
    const directions: Record<string, [number, number]> = {
      ArrowLeft: [-0.15, 0],
      ArrowRight: [0.15, 0],
      ArrowUp: [0, -0.12],
      ArrowDown: [0, 0.12],
      '+': [0, 0],
      '-': [0, 0],
      '=': [0, 0],
    };
    if (!(event.key in directions)) return;
    event.preventDefault();
    const offset = camera.position.clone().sub(controls.target);
    // Z is up for the STL models; spherical coordinates use Y as up.
    offset.set(offset.x, offset.z, -offset.y);
    const spherical = new THREE.Spherical().setFromVector3(offset);
    spherical.theta += directions[event.key][0];
    spherical.phi = THREE.MathUtils.clamp(
      spherical.phi + directions[event.key][1],
      0.08,
      Math.PI - 0.08,
    );
    if (event.key === '+' || event.key === '=') spherical.radius *= 0.9;
    if (event.key === '-') spherical.radius *= 1.1;
    spherical.radius = THREE.MathUtils.clamp(spherical.radius, 35, 1300);
    offset.setFromSpherical(spherical);
    camera.position.set(offset.x, -offset.z, offset.y).add(controls.target);
    controls.update();
  });
  const observer = new ResizeObserver(() => {
    camera.aspect = stage.clientWidth / stage.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(stage.clientWidth, stage.clientHeight);
    render();
  });
  observer.observe(stage);
  show();
  window.addEventListener(
    'pagehide',
    () => {
      observer.disconnect();
      controls.dispose();
      geometries.forEach((g) => g.dispose());
      materials.forEach((m) => m.dispose());
      renderer.dispose();
    },
    { once: true },
  );
}
