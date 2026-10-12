import { readFile, readdir, access } from 'node:fs/promises';
import { resolve, join, relative } from 'node:path';
import assert from 'node:assert/strict';
import { parse, serializeOuter } from 'parse5';
import { createHash } from 'node:crypto';

const root = resolve('dist');
const origin = 'https://simsim314.github.io';
const base = '/Homepage/';
const pages = [];
async function walk(dir) {
  for (const e of await readdir(dir, { withFileTypes: true })) {
    const p = join(dir, e.name);
    if (e.isDirectory()) await walk(p);
    else if (p.endsWith('.html')) pages.push(p);
  }
}
await walk(root);
const docs = new Map();
for (const page of pages) {
  const html = await readFile(page, 'utf8');
  const nodes = [];
  const collect = (n) => {
    nodes.push(n);
    n.childNodes?.forEach(collect);
  };
  collect(parse(html));
  const ids = nodes.flatMap((n) =>
    (n.attrs || []).filter((a) => a.name === 'id').map((a) => a.value),
  );
  assert.equal(ids.length, new Set(ids).size, `Duplicate element IDs: ${relative(root, page)}`);
  assert(!html.includes('katex-error'), `Invalid equation: ${page}`);
  assert.equal(nodes.filter((n) => n.tagName === 'h1').length, 1, `Expected one h1: ${page}`);
  docs.set(page, { nodes, ids: new Set(ids), html });
}
// Content visuals get one placement across the entire generated site.
const visualLocations = new Map();
const imageDigests = new Map();
const diagramDigests = new Map();
const attributes = (n) => Object.fromEntries((n.attrs || []).map((a) => [a.name, a.value]));
for (const [page, { nodes }] of docs) {
  const main = nodes.find((n) => n.tagName === 'main');
  const contentNodes = [];
  const collect = (n) => {
    contentNodes.push(n);
    n.childNodes?.forEach(collect);
  };
  if (main) collect(main);
  for (const n of contentNodes) {
    const attrs = attributes(n);
    if (attrs['data-visual-key']) {
      const key = attrs['data-visual-key'];
      assert(
        !visualLocations.has(key),
        `Repeated content visual ${key}: ${visualLocations.get(key)} and ${page}`,
      );
      visualLocations.set(key, page);
    }
    if (n.tagName === 'img' && attrs.src?.startsWith(base)) {
      const file = resolve(root, decodeURIComponent(attrs.src.slice(base.length)));
      if (attrs.src.endsWith('.gif')) {
        await access(file.replace(/\.gif$/, '-still.png')).catch(() => {
          throw new Error(`Missing animation pause fallback for ${attrs.src}`);
        });
      }
      const digest = createHash('sha256')
        .update(await readFile(file))
        .digest('hex');
      assert(
        !imageDigests.has(digest),
        `Image displayed twice: ${attrs.src} in ${imageDigests.get(digest)} and ${page}`,
      );
      imageDigests.set(digest, page);
    }
    if (n.tagName === 'svg') {
      const normalized = serializeOuter(n)
        .replace(/id="[^"]*"/g, 'id="reference"')
        .replace(/url\(#[^)]+\)/g, 'url(#reference)');
      const digest = createHash('sha256').update(normalized).digest('hex');
      assert(
        !diagramDigests.has(digest),
        `Diagram displayed twice in ${diagramDigests.get(digest)} and ${page}`,
      );
      diagramDigests.set(digest, page);
    }
  }
}
let checked = 0;
for (const [page, { nodes, html }] of docs) {
  const current = new URL(base + relative(root, page).replace(/index\.html$/, ''), origin);
  for (const node of nodes)
    for (const attr of node.attrs || []) {
      if (!['href', 'src', 'srcset'].includes(attr.name)) continue;
      const urls =
        attr.name === 'srcset'
          ? attr.value.split(',').map((s) => s.trim().split(/\s+/)[0])
          : [attr.value];
      for (const raw of urls) {
        if (!raw || /^(mailto:|tel:|data:|javascript:)/.test(raw)) continue;
        const url = new URL(raw, current);
        if (url.origin !== origin || (/^https?:/.test(raw) && !url.pathname.startsWith(base)))
          continue;
        assert(url.pathname.startsWith(base), `Missing ${base} prefix: ${raw} in ${page}`);
        let file = resolve(root, decodeURIComponent(url.pathname.slice(base.length)));
        if (url.pathname.endsWith('/')) file = join(file, 'index.html');
        assert(file === root || file.startsWith(root + '/'), 'Path outside build');
        await access(file).catch(() => {
          throw new Error(`Missing local target ${raw} in ${page}`);
        });
        if (url.hash && docs.has(file))
          assert(
            docs.get(file).ids.has(decodeURIComponent(url.hash.slice(1))),
            `Missing anchor ${raw} in ${page}`,
          );
        checked++;
      }
    }
  assert(!/href="[^"\s]*\/blog\//.test(html), `Separate blog route in ${page}`);
}
const entries = JSON.parse(await readFile(join(root, 'search-index.json'), 'utf8'));
const articlePages = pages.filter((p) => relative(root, p).startsWith('articles/'));
assert.equal(
  entries.length,
  articlePages.length,
  'Search index must include every published article exactly once',
);
assert.equal(
  new Set(entries.map((e) => e.url)).size,
  entries.length,
  'Duplicate canonical articles',
);
const home = docs.get(join(root, 'index.html')).html;
for (const e of entries) {
  assert(home.includes(e.url), `Article missing from homepage: ${e.title}`);
  await access(join(root, e.url.slice(base.length), 'index.html'));
}
assert(
  docs
    .get(join(root, 'articles/high-dimensional-sphere-packing/index.html'))
    .html.includes('katex-display'),
  'Markdown equations must render',
);
assert(
  docs.get(join(root, 'articles/mandelbrot-cuda/index.html')).html.includes('katex-display'),
  'MDX equations must render',
);
const sitemap = await readFile(join(root, 'sitemap.xml'), 'utf8');
for (const e of entries) assert(sitemap.includes(origin + e.url), 'Article missing from sitemap');
// KaTeX font paths must remain relative to the built CSS asset.
for (const file of await readdir(join(root, '_astro')))
  if (file.endsWith('.css')) {
    const css = await readFile(join(root, '_astro', file), 'utf8');
    for (const match of css.matchAll(/url\(\s*(?:"([^"]*)"|'([^']*)'|([^)]*))\s*\)/g)) {
      const path = (match[1] || match[2] || match[3]).trim();
      if (path.startsWith('data:') || path.startsWith('http')) continue;
      const target = path.startsWith(base)
        ? join(root, path.slice(base.length))
        : resolve(root, '_astro', path);
      await access(target).catch(() => {
        throw new Error(`Missing CSS asset ${path}`);
      });
    }
  }
console.log(
  `Verified ${pages.length} HTML pages, ${entries.length} canonical articles, ${checked} internal links/assets, Markdown/MDX equations, search index, sitemap, and unique visual placements.`,
);
