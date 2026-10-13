import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

type Placement = {
  name: string;
  xyz: [number, number, number];
  layer: number;
  turns: number;
  centre: [number, number, number] | null;
};
const models = new Map<string, Promise<Map<string, THREE.BufferGeometry>>>();
function loadModels(url: string) {
  if (!models.has(url)) {
    models.set(
      url,
      new GLTFLoader()
        .loadAsync(url)
        .then((gltf) => {
          const result = new Map<string, THREE.BufferGeometry>();
          gltf.scene.updateMatrixWorld(true);
          gltf.scene.traverse((object) => {
            if (!(object instanceof THREE.Mesh)) return;
            const g = object.geometry.clone();
            g.applyMatrix4(object.matrixWorld);
            g.deleteAttribute('color');
            g.computeVertexNormals();
            g.computeBoundingBox();
            // Keep original coordinates: the assembly placements depend on them.
            result.set(object.name, g);
          });
          return result;
        })
        .catch((error) => {
          models.delete(url);
          throw error;
        }),
    );
  }
  return models.get(url)!;
}

type CameraState = { position: number[]; zoom: number };

export async function mountLifeTileExplorer(root: HTMLElement) {
  const stage = root.querySelector<HTMLElement>('.explorer-stage')!;
  const assembly = root.dataset.assembly === 'true';
  const viewers: Awaited<ReturnType<typeof mountSingleView>>[] = [];
  const events = new AbortController();
  try {
    if (assembly) viewers.push(await mountSingleView(root));
    else {
      const pair = document.createElement('div');
      pair.className = 'tile-face-pair';
      stage.replaceChildren(pair);
      for (const [face, label] of [
        ['top', 'Output · top'],
        ['bottom', 'Input · underside'],
      ] as const) {
        const panel = document.createElement('div');
        panel.className = 'tile-face';
        Object.assign(panel.dataset, root.dataset);
        const heading = document.createElement('p');
        heading.className = 'tile-face-label';
        heading.textContent = label;
        const viewport = document.createElement('div');
        viewport.className = 'explorer-stage tile-face-stage';
        panel.append(heading, viewport);
        pair.append(panel);
        viewers.push(await mountSingleView(panel, face));
      }
      root.querySelectorAll<HTMLButtonElement>('[data-view]').forEach((button) => {
        button.addEventListener(
          'click',
          () => {
            viewers.forEach((viewer) => viewer.setView(button.dataset.view!));
          },
          { signal: events.signal },
        );
      });
    }
    return {
      show(name: string) {
        viewers.forEach((viewer) => viewer.show(name));
      },
      getState() {
        return { views: viewers.map((viewer) => viewer.getState()) };
      },
      setState(state: { views: CameraState[] }) {
        viewers.forEach((viewer, i) => {
          if (state.views[i]) viewer.setState(state.views[i]);
        });
      },
      dispose() {
        events.abort();
        viewers.forEach((viewer) => viewer.dispose());
      },
    };
  } catch (error) {
    events.abort();
    viewers.forEach((viewer) => viewer.dispose());
    throw error;
  }
}

async function mountSingleView(root: HTMLElement, initialView = 'reset') {
  const assembly = root.dataset.assembly === 'true';
  const events = new AbortController();
  const geometry = await loadModels(root.dataset.modelUrl!);
  let placements: Placement[] = [];
  if (assembly) {
    const response = await fetch(root.dataset.assemblyUrl!);
    if (!response.ok) throw new Error(`Assembly data: ${response.status}`);
    placements = await response.json();
    for (const p of placements)
      if (!geometry.has(p.name)) throw new Error(`Missing tile ${p.name}`);
  }
  const stage = root.querySelector<HTMLElement>('.explorer-stage')!;
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.setClearColor(assembly ? 0x191918 : 0xf3f3ec);
  const canvas = renderer.domElement;
  canvas.tabIndex = 0;
  stage.replaceChildren(canvas);
  const scene = new THREE.Scene();
  scene.add(new THREE.HemisphereLight(0xffffff, 0x52606a, 2.4));
  const light = new THREE.DirectionalLight(0xffffff, 3);
  light.position.set(-130, -160, 330);
  scene.add(light);
  const undersideLight = new THREE.DirectionalLight(0xffffff, 2.3);
  undersideLight.position.set(80, 100, -220);
  scene.add(undersideLight);
  const camera = new THREE.OrthographicCamera(-100, 100, 100, -100, 0.1, 3000);
  camera.up.set(0, 0, 1);
  const controls = new OrbitControls(camera, canvas);
  controls.enableDamping = false;
  controls.enablePan = false;
  controls.minZoom = 0.5;
  controls.maxZoom = 5;
  const group = new THREE.Group();
  scene.add(group);
  const materials = new Map<string, THREE.MeshStandardMaterial>();
  function material(name: string) {
    let colour = name.startsWith('orange')
      ? '#d89747'
      : name.startsWith('purple')
        ? '#9772b4'
        : '#588bb2';
    if (name.startsWith('final') || name.startsWith('start')) {
      const live = ['start-1', 'final-0', 'final-2'].includes(name);
      colour = assembly ? (live ? '#d5d5cf' : '#434340') : live ? '#465457' : '#e7e5d5';
    } else if (assembly) {
      colour = name.startsWith('orange')
        ? '#f87923'
        : name.startsWith('purple')
          ? '#a873e6'
          : '#5694fa';
    }
    if (!materials.has(colour))
      materials.set(
        colour,
        new THREE.MeshStandardMaterial({ color: colour, roughness: 0.7, flatShading: true }),
      );
    return materials.get(colour)!;
  }
  let radius = 46;
  let selected = '';
  const spacing = root.querySelector<HTMLInputElement>('input[type="range"]');
  const render = () => renderer.render(scene, camera);
  function resize() {
    const w = stage.clientWidth,
      h = stage.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    const half = Math.max(radius, (radius * h) / w);
    camera.left = (-half * w) / h;
    camera.right = (half * w) / h;
    camera.top = half;
    camera.bottom = -half;
    camera.updateProjectionMatrix();
    render();
  }
  function pose(view = initialView) {
    if (view === 'reset') view = initialView;
    camera.zoom = 1;
    camera.position.set(
      ...((view === 'top'
        ? [80, -100, 700]
        : view === 'bottom'
          ? [240, -320, -510]
          : [360, -480, 510]) as [number, number, number]),
    );
    controls.target.set(0, 0, 0);
    controls.update();
    camera.updateProjectionMatrix();
    render();
  }
  function rebuild() {
    group.clear();
    group.position.set(0, 0, 0);
    if (assembly) {
      const gap = Number(spacing!.value);
      for (const item of placements) {
        const mesh = new THREE.Mesh(geometry.get(item.name), material(item.name));
        const matrix = new THREE.Matrix4().makeTranslation(
          item.xyz[0],
          item.xyz[1],
          item.xyz[2] + item.layer * gap,
        );
        if (item.turns) {
          const [x, y, z] = item.centre!;
          matrix
            .multiply(new THREE.Matrix4().makeTranslation(x, y, z))
            .multiply(new THREE.Matrix4().makeRotationZ((item.turns * Math.PI) / 2))
            .multiply(new THREE.Matrix4().makeTranslation(-x, -y, -z));
        }
        mesh.applyMatrix4(matrix);
        group.add(mesh);
      }
      root.querySelector('output')!.textContent = `${gap} mm`;
      spacing!.setAttribute(
        'aria-valuetext',
        gap === 0 ? '0 millimetres, assembled' : `${gap} millimetres between layers`,
      );
    } else {
      if (!geometry.has(selected)) throw new Error(`Missing tile ${selected}`);
      group.add(new THREE.Mesh(geometry.get(selected), material(selected)));
    }
    const bounds = new THREE.Box3().setFromObject(group);
    const centre = bounds.getCenter(new THREE.Vector3());
    group.position.copy(centre.negate());
    radius = Math.max(30, bounds.getBoundingSphere(new THREE.Sphere()).radius * 1.12);
    canvas.setAttribute(
      'aria-label',
      assembly
        ? 'Complete glider assembly. Drag or use arrow keys to rotate.'
        : `${selected}, ${initialView === 'bottom' ? 'input underside' : 'output top'}. Drag or use arrow keys to rotate.`,
    );
    resize();
  }
  spacing?.addEventListener('input', rebuild, { signal: events.signal });
  function setView(view: string) {
    if (view === 'close') return;
    if (view === 'in' || view === 'out') {
      camera.zoom = THREE.MathUtils.clamp(camera.zoom * (view === 'in' ? 1.2 : 1 / 1.2), 0.5, 5);
      camera.updateProjectionMatrix();
      render();
    } else pose(view);
  }
  root.querySelectorAll<HTMLButtonElement>('[data-view]').forEach((button) => {
    button.addEventListener('click', () => setView(button.dataset.view!), {
      signal: events.signal,
    });
  });
  controls.addEventListener('change', render);
  canvas.addEventListener(
    'keydown',
    (event) => {
      if (!['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', '+', '=', '-'].includes(event.key))
        return;
      event.preventDefault();
      if (['+', '=', '-'].includes(event.key))
        camera.zoom = THREE.MathUtils.clamp(
          camera.zoom * (event.key === '-' ? 0.85 : 1.15),
          0.5,
          5,
        );
      else {
        const spherical = new THREE.Spherical().setFromVector3(
          camera.position.clone().applyAxisAngle(new THREE.Vector3(1, 0, 0), -Math.PI / 2),
        );
        if (event.key === 'ArrowLeft') spherical.theta -= 0.12;
        if (event.key === 'ArrowRight') spherical.theta += 0.12;
        if (event.key === 'ArrowUp') spherical.phi -= 0.12;
        if (event.key === 'ArrowDown') spherical.phi += 0.12;
        spherical.makeSafe();
        camera.position.copy(
          new THREE.Vector3()
            .setFromSpherical(spherical)
            .applyAxisAngle(new THREE.Vector3(1, 0, 0), Math.PI / 2),
        );
      }
      camera.updateProjectionMatrix();
      controls.update();
      render();
    },
    { signal: events.signal },
  );
  const observer = new ResizeObserver(resize);
  observer.observe(stage);
  return {
    setView,
    getState() {
      return { position: camera.position.toArray(), zoom: camera.zoom };
    },
    setState(state: { position: number[]; zoom: number }) {
      camera.position.fromArray(state.position);
      camera.zoom = state.zoom;
      camera.updateProjectionMatrix();
      controls.update();
      render();
    },
    dispose() {
      events.abort();
      observer.disconnect();
      controls.dispose();
      for (const material of materials.values()) material.dispose();
      renderer.dispose();
      renderer.forceContextLoss();
    },
    show(name: string) {
      const changed = selected !== name;
      selected = name;
      rebuild();
      if (changed) pose();
    },
  };
}
