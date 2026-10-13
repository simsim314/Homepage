import fs from 'node:fs/promises';
import vm from 'node:vm';
import crypto from 'node:crypto';
import { format } from 'prettier';
import scad from '@jscad/scad-api';

// The source is the author's 2019 forum code, kept unchanged alongside the exports.
const sourcePath = new URL('../research/3d-tiles/original-2019.jscad', import.meta.url);
const source = await fs.readFile(sourcePath, 'utf8');
// This legacy library tests `instanceof Array`, so convert sandbox values to
// ordinary host arrays before passing them to primitives and vector methods.
function hostValue(value) {
  if (value instanceof scad.csg.CSG || value instanceof scad.csg.CAG) return value;
  if (Array.isArray(value)) return Array.from(value, hostValue);
  if (value && value.constructor?.name === 'Object')
    return Object.fromEntries(Object.entries(value).map(([k, v]) => [k, hostValue(v)]));
  return value;
}
const api = {
  ...scad.primitives2d,
  ...scad.primitives3d,
  ...scad.booleanOps,
  ...scad.extrusions,
};
for (const name of ['translate', 'scale']) {
  const method = scad.csg.CSG.prototype[name];
  scad.csg.CSG.prototype[name] = function (...args) {
    return method.apply(this, args.map(hostValue));
  };
}
const context = vm.createContext(
  Object.fromEntries(
    Object.entries(api).map(([name, fn]) => [name, (...args) => fn(...args.map(hostValue))]),
  ),
);
vm.runInContext(source, context, { timeout: 30_000 });
// The original all() assigns R2 through plain_top() before calling bottom_attach().
// Set that same value explicitly so individual exports are independent of call order.
context.R2 = context.R / 2;
const parts = [
  ['side-plain', 'Plain side', 'regular_side', 'side'],
  ['side-connecting', 'Connecting side', 'attach_side', 'side'],
  ['top-plain', 'Plain top', 'plain_top', 'top'],
  ['top-attachment', 'Attachment top', 'top_attach', 'top'],
  ['top-zero', 'Zero top', 'top0', 'top'],
  ['top-one', 'One top', 'top_plus', 'top'],
  ['bottom-attachment', 'Attachment base', 'bottom_attach', 'base'],
  ['bottom-one', 'One base', 'bottom_plus', 'base'],
  ['bottom-zero', 'Zero base', 'bottom0', 'base'],
  ['bottom-either', 'Either-value base', 'bottom_plus0', 'base'],
];
const output = new URL('../public/models/life-tile-kit/', import.meta.url);
await fs.mkdir(output, { recursive: true });
const manifest = {
  source: 'https://conwaylife.com/forums/viewtopic.php?p=73650#p73650',
  sourceSha256: crypto.createHash('sha256').update(source).digest('hex'),
  originalCoreSize: context.R,
  exportScale: 3,
  matingTopHeight: (context.R + context.v) * 3,
  units: 'mm',
  status: 'Historical CAD reconstruction; physical fit has not been tested.',
  parts: [],
};
function removeFlatFragments(triangles) {
  const parent = triangles.map((_, i) => i);
  const find = (i) => (parent[i] === i ? i : (parent[i] = find(parent[i])));
  const vertexOwners = new Map();
  for (let i = 0; i < triangles.length; i++) {
    for (const { pos } of triangles[i].vertices) {
      const key = [pos.x, pos.y, pos.z].map((v) => Math.round(v * 1e5)).join(',');
      if (vertexOwners.has(key)) parent[find(i)] = find(vertexOwners.get(key));
      else vertexOwners.set(key, i);
    }
  }
  const groups = new Map();
  triangles.forEach((triangle, i) => {
    const root = find(i);
    if (!groups.has(root)) groups.set(root, []);
    groups.get(root).push(triangle);
  });
  return [...groups.values()]
    .filter((group) => {
      const positions = group.flatMap((t) => t.vertices.map((v) => v.pos));
      return ['x', 'y', 'z'].every((axis) => {
        const values = positions.map((v) => v[axis]);
        return Math.max(...values) - Math.min(...values) > 1e-5;
      });
    })
    .flat();
}
for (const [id, name, fn, family] of parts) {
  const part = vm
    .runInContext(`${fn}()`, context, { timeout: 30_000 })
    .scale(3)
    .reTesselated()
    .canonicalized()
    .fixTJunctions();
  const bounds = part.getBounds().map((v) => [v.x, v.y, v.z]);
  const grounded = part.translate(bounds[0].map((v) => -v));
  const rawTriangles = grounded.toTriangles();
  // The legacy XOR export includes a detached, coplanar two-triangle fragment.
  // Discard only components with no thickness; solid geometry is preserved.
  const triangles = removeFlatFragments(rawTriangles);
  const data = Buffer.alloc(84 + triangles.length * 50);
  data.write(`Michael Simkin 2019 modular CA tiles: ${id}`, 0, 'ascii');
  data.writeUInt32LE(triangles.length, 80);
  triangles.forEach((triangle, index) => {
    let offset = 84 + index * 50;
    for (const vector of [triangle.plane.normal, ...triangle.vertices.map((v) => v.pos)]) {
      for (const axis of ['x', 'y', 'z']) {
        data.writeFloatLE(vector[axis], offset);
        offset += 4;
      }
    }
  });
  await fs.writeFile(new URL(`${id}.stl`, output), data);
  manifest.parts.push({
    id,
    name,
    family,
    file: `${id}.stl`,
    sourceBounds: bounds,
    dimensions: bounds[1].map((v, i) => Number((v - bounds[0][i]).toFixed(3))),
    triangles: triangles.length,
    removedFlatTriangles: rawTriangles.length - triangles.length,
  });
  console.log(`${id}: ${triangles.length} triangles`);
}
await fs.writeFile(
  new URL('manifest.json', output),
  await format(JSON.stringify(manifest), { parser: 'json' }),
);
