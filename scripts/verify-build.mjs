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
  const redirect = nodes.some(
    (n) =>
      n.tagName === 'meta' &&
      n.attrs?.some((a) => a.name === 'http-equiv' && a.value === 'refresh'),
  );
  if (!redirect)
    assert.equal(nodes.filter((n) => n.tagName === 'h1').length, 1, `Expected one h1: ${page}`);
  docs.set(page, { nodes, ids: new Set(ids), html });
}
// A visual belongs to one article. Homepage previews may repeat it on that same article.
const visualLocations = new Map();
const imageDigests = new Map();
const diagramDigests = new Map();
const attributes = (n) => Object.fromEntries((n.attrs || []).map((a) => [a.name, a.value]));
const recordVisual = (registry, key, owner, page) => {
  const previous = registry.get(key);
  assert(
    !previous || (owner && previous.owner === owner),
    `Visual reused by different articles/topics: ${key} in ${previous?.pages.join(', ')} and ${page}`,
  );
  if (previous) previous.pages.push(page);
  else registry.set(key, { owner, pages: [page] });
};
for (const [page, { nodes }] of docs) {
  const main = nodes.find((n) => n.tagName === 'main');
  const contentNodes = [];
  const owners = new WeakMap();
  const collect = (n, inheritedOwner) => {
    const owner = attributes(n)['data-article-id'] || inheritedOwner;
    owners.set(n, owner);
    contentNodes.push(n);
    n.childNodes?.forEach((child) => collect(child, owner));
  };
  if (main) collect(main);
  for (const n of contentNodes) {
    const attrs = attributes(n);
    if (attrs['data-visual-key']) {
      const key = attrs['data-visual-key'];
      recordVisual(visualLocations, key, owners.get(n), page);
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
      recordVisual(imageDigests, digest, owners.get(n), page);
    }
    if (n.tagName === 'svg') {
      const normalized = serializeOuter(n)
        .replace(/id="[^"]*"/g, 'id="reference"')
        .replace(/url\(#[^)]+\)/g, 'url(#reference)');
      const digest = createHash('sha256').update(normalized).digest('hex');
      recordVisual(diagramDigests, digest, owners.get(n), page);
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
const descendants = (node) => {
  const result = [];
  const visit = (n) => {
    result.push(n);
    n.childNodes?.forEach(visit);
  };
  visit(node);
  return result;
};
// Topic tiles open collections; their explicit example captions still open articles.
for (const page of [join(root, 'index.html'), join(root, 'interests/index.html')]) {
  const cards = docs
    .get(page)
    .nodes.filter((n) => attributes(n).class?.split(' ').includes('interest-card'));
  assert.equal(cards.length, 6, 'Six main topic cards must remain');
  for (const card of cards) {
    const nodes = descendants(card);
    const titleLink = nodes
      .find((n) => n.tagName === 'h3')
      ?.childNodes.find((n) => n.tagName === 'a');
    const imageLink = nodes.find((n) => attributes(n).class === 'interest-image');
    assert.equal(
      attributes(imageLink).href,
      attributes(titleLink).href,
      'Topic image must open its collection',
    );
    const example = nodes.find((n) => n.tagName === 'figure');
    const captionLink = descendants(example)
      .find((n) => n.tagName === 'figcaption')
      ?.childNodes.find((n) => n.tagName === 'a');
    assert.equal(
      attributes(captionLink).href,
      `${base}articles/${attributes(example)['data-article-id']}/`,
      'Named example must retain its own article link',
    );
  }
}
// Each topic/subtopic page lists every matching canonical article exactly once.
for (const [page, { nodes }] of docs) {
  const collection = nodes.find((n) => attributes(n)['data-topic-collection']);
  if (!collection) continue;
  const topic = attributes(collection)['data-topic-collection'];
  const introduction = nodes.find((n) => attributes(n)['data-topic-introduction'] === topic);
  assert(introduction, `Missing thematic introduction: ${topic}`);
  assert(
    nodes.indexOf(introduction) < nodes.indexOf(collection),
    `Introduction must lead ${topic}`,
  );
  let ancestor = introduction.parentNode;
  while (ancestor) {
    assert(ancestor.tagName !== 'details', `Thematic introduction must be visible: ${topic}`);
    ancestor = ancestor.parentNode;
  }
  const actual = descendants(collection)
    .filter((n) => n.tagName === 'article' && attributes(n)['data-article-id'])
    .map((n) => `${base}articles/${attributes(n)['data-article-id']}/`);
  if (topic === 'game-of-life') {
    assert.deepEqual(
      actual.slice(0, 2),
      [`${base}articles/remini/`, `${base}articles/caterloopilar/`],
      'Life reading order must begin with the main constructions',
    );
    assert(
      actual.indexOf(`${base}articles/life-in-3d-tiles/`) >
        actual.indexOf(`${base}articles/lifeapi/`),
      'Physical tiles must follow the Life research/tools',
    );
  }
  const expected = entries
    .filter((e) => e.topics.some((t) => t.startsWith(`${topic} `)))
    .map((e) => e.url);
  assert.deepEqual(actual.sort(), expected.sort(), `Incorrect topic collection: ${topic}`);
  assert.equal(new Set(actual).size, actual.length, `Duplicate articles in topic: ${topic}`);
  const navigation = nodes.find((n) => attributes(n)['aria-label'] === 'Browse by topic');
  assert(
    descendants(navigation).some(
      (n) =>
        attributes(n)['aria-current'] === 'page' &&
        attributes(n).href === `${base}interests/${topic}/`,
    ),
    `Current topic missing from sidebar: ${topic}`,
  );
}
for (const page of articlePages) {
  const { nodes } = docs.get(page);
  assert(
    nodes.some((n) => attributes(n)['aria-label'] === 'Browse by topic'),
    `Missing article topic navigation: ${page}`,
  );
  assert(
    nodes.some((n) => attributes(n)['aria-label'] === 'Article contents'),
    `Missing in-page article navigation: ${page}`,
  );
}
const homepageOccurrences = new Map();
for (const node of docs.get(join(root, 'index.html')).nodes) {
  const owner = node.attrs?.find((a) => a.name === 'data-article-id')?.value;
  if (!owner) continue;
  let parent = node.parentNode;
  let nestedInSameArticle = false;
  while (parent) {
    if (parent.attrs?.some((a) => a.name === 'data-article-id' && a.value === owner)) {
      nestedInSameArticle = true;
      break;
    }
    parent = parent.parentNode;
  }
  if (!nestedInSameArticle)
    homepageOccurrences.set(owner, (homepageOccurrences.get(owner) || 0) + 1);
}
for (const [owner, count] of homepageOccurrences) {
  assert(count <= 2, `Article appears a third time on the homepage: ${owner}`);
}
assert(
  home.indexOf('id="interests"') < home.indexOf('id="articles"'),
  'Interest themes must lead the homepage; recent articles follow them',
);
const textContent = (node) =>
  node.nodeName === '#text' ? node.value : (node.childNodes || []).map(textContent).join('');
const aboutText = textContent(
  docs.get(join(root, 'about/index.html')).nodes.find((n) => n.tagName === 'main'),
).replace(/\s+/g, ' ');
for (const phrase of [
  'original Gemini',
  'was Serizawa Geminoid',
  'built Geminoid Particles',
  'Glider Gun, Caterloopillar, Remini, and switch-engine ping-pong',
]) {
  assert(aboutText.includes(phrase), `Missing spaces around About links: ${phrase}`);
}

const caterloopillarPage = docs.get(join(root, 'articles/caterloopilar/index.html'));
const mechanismSteps = caterloopillarPage.nodes.filter((n) => attributes(n)['data-mechanism-step']);
assert(
  mechanismSteps.map((n) => attributes(n)['data-mechanism-step']).join(',') ===
    Array.from({ length: 17 }, (_, i) => i + 1).join(','),
  'Caterloopillar must build from small components to the whole loop',
);
assert(
  !caterloopillarPage.nodes.some((n) =>
    (attributes(n).class || '').split(' ').includes('article-preview'),
  ),
  'Do not reveal the whole Caterloopillar tour before its components',
);
assert(
  descendants(mechanismSteps[16]).some(
    (n) => n.tagName === 'img' && attributes(n).src.endsWith('caterloopillar-architecture.png'),
  ),
  'The complete architecture must remain available in the final stage on mobile and without JavaScript',
);
const caterloopillarStageTitles = mechanismSteps.map((step) =>
  textContent(descendants(step).find((n) => n.tagName === 'h2')),
);
assert(
  caterloopillarStageTitles[0].includes('reflector') &&
    caterloopillarStageTitles[2].includes('one reading head') &&
    caterloopillarStageTitles[8].includes('Encode a command') &&
    caterloopillarStageTitles[9].includes('slow salvo') &&
    caterloopillarStageTitles[12].includes('entire new reading head'),
  'Do not skip the reflector, assembled head, encoding, salvo and whole-head construction bridges',
);
assert(
  caterloopillarPage.nodes.some((n) => attributes(n)['data-head-explorer'] !== undefined),
  'Show an inspectable assembled reading head before explaining how it reads',
);
for (const clip of [
  'basic-reflector',
  'reading-head',
  'command-offsets',
  'tape-to-salvo',
  'whole-head-construction',
  'whole-head-erasure',
  'whole-tail-erasure',
  'working-reader',
  'glider-reversal',
  'signal-routing',
  'inner-reflector',
  'tape-rebuild',
  'insertion-clearance-failure',
  'mwss-beside-hwss',
  'forward-inserter',
  'backward-inserter',
]) {
  assert(
    caterloopillarPage.html.includes(`${base}images/caterloopillar-${clip}.gif`),
    `Missing Caterloopillar mechanism: ${clip}`,
  );
}
assert(
  !caterloopillarPage.html.includes('The idea I initially thought would fail'),
  'Do not inflate the early bug into a breakthrough narrative',
);
const assemblyExplorer = docs
  .get(join(root, 'articles/life-in-3d-tiles/index.html'))
  .nodes.find((n) => attributes(n)['data-assembly'] === 'true');
assert(
  descendants(assemblyExplorer).some((n) => n.tagName === 'img'),
  'Assembly must retain a visible preview when WebGL cannot load',
);
assert(
  descendants(assemblyExplorer).some(
    (n) => n.tagName === 'button' && textContent(n).includes('Retry 3D view'),
  ),
  'Assembly load failure must offer a retry',
);

const caResearch = docs.get(join(root, 'interests/cellular-automata/index.html')).html;
const lifeCategory = docs.get(join(root, 'interests/game-of-life/index.html')).html;
for (const id of [
  'b60',
  'bne14t30',
  'brx46b',
  'ocellus',
  'simkins-p60',
  '24-cell-quadratic-growth',
  '25-cell-quadratic-growth',
  'switch-engine-ping-pong',
  'still-life-tiles',
  'life-in-3d-tiles',
  'multilayer-mutilated-gear',
]) {
  assert(
    !caResearch.includes(`${base}articles/${id}/`),
    `Conway result incorrectly listed under CA Research: ${id}`,
  );
  assert(
    lifeCategory.includes(`${base}articles/${id}/`),
    `Conway result missing from Conway's Life: ${id}`,
  );
}
assert(
  caResearch.includes(`${base}articles/neural-ca-mnist/`),
  'Neural CA must appear in CA Research',
);
assert(
  lifeCategory.includes(`${base}articles/simkin-glider-gun/`) &&
    !lifeCategory.includes(`${base}articles/neural-ca-mnist/`),
  'Conway’s Life must retain its dedicated construction/tool collection',
);
for (const entry of entries.filter(
  (e) =>
    e.topics.some((t) => /^(game-of-life|cellular-automata) /.test(t)) &&
    !['LifeAPI', 'Making Still-Life Tiles Physical', 'Conway’s Life in 3D Tiles'].includes(e.title),
)) {
  const page = join(root, entry.url.slice(base.length), 'index.html');
  const { nodes } = docs.get(page);
  assert(
    nodes.some((n) => n.tagName === 'img' && /\.gif$/.test(attributes(n).src || '')),
    `CA/Life article must include its animation: ${entry.title}`,
  );
}
assert(
  !home.includes(`${base}interests/artificial-intelligence/`),
  'The removed AI topic must not appear in homepage navigation or filters',
);
assert(
  visualLocations
    .get('simkin-glider-gun')
    ?.pages.includes(join(root, 'articles/simkin-glider-gun/index.html')),
  'Gun animation must appear on its article',
);
assert(
  home.includes(`${base}articles/simkin-glider-gun/#glider-gun`),
  'Homepage gun exhibit must link to the article animation',
);
assert(
  visualLocations.get('simkin-glider-gun')?.pages.includes(join(root, 'index.html')),
  'Original gun hero must remain on the homepage',
);
for (const e of entries) {
  assert(home.includes(e.url), `Article missing from homepage: ${e.title}`);
  await access(join(root, e.url.slice(base.length), 'index.html'));
}
assert(
  docs.get(join(root, 'articles/neural-ca-mnist/index.html')).html.includes('katex-display'),
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
  `Verified ${pages.length} HTML pages, ${entries.length} canonical articles, ${checked} internal links/assets, Markdown/MDX equations, search index, sitemap, and visual ownership by article.`,
);
