# Michael Simkin — Personal Research Journal

An Astro website at **https://simsim314.github.io/Homepage/**. The homepage is the
journal: interest themes first, followed by recent articles. There is no separate
blog. Thirty research/project articles share one collection and one
canonical URL each, across six main interests and three nested interest pages.

To continue this project in a new chat, read [CONTINUE-HERE.md](CONTINUE-HERE.md).
It records the author's instructions, interview evidence, current pages and tile
geometry, verification results, publication restrictions, and a ready-to-paste prompt.

## Development

Requires Node.js **22.12 or newer** (Node 22 LTS recommended) and npm.

```bash
npm ci
npm run dev
```

Open **http://localhost:4321/Homepage/**. Astro's repository base path applies in
both development and production.

```bash
npm run format      # format Astro, Markdown, TypeScript, and CSS
npm run check       # Astro and TypeScript diagnostics
npm run build       # static site in dist/
npm run preview     # inspect the production build at /Homepage/
npm run verify      # diagnostics, build, link/asset/anchor and content checks
```

The built-site verifier checks internal URLs, local images, scripts, KaTeX fonts,
canonical article coverage in the homepage/search/sitemap, duplicate element IDs,
and equations rendered from both Markdown and MDX. It also rejects repeated
content images and diagrams assigned to different articles or topics. Reuse for
the same article on its homepage preview and article page is allowed.

## Construction-piece CAD

The 3D Life article has an on-demand viewer for the original 2019 construction
pieces. These make cubes that can be combined into actual tiles; they are not
the 26-type Life tile set. Three.js and the models load only when requested.

`npm run export:construction-pieces` regenerates the ten STL files and manifest
from `research/3d-tiles/original-2019.jscad`, using a pinned legacy JSCAD API for
source compatibility. The original code is excluded from formatting to preserve
it unchanged. Exports use millimetres at 3× scale and remove one detached flat
fragment from the legacy boolean result. Digital mesh checks and physical-fit
limitations are recorded in `research/3d-tiles/`.

The Thingiverse package and description are prepared locally. Publication needs
a selected license and account sign-in. This is separate from permission to
upload or deploy the website.

## Adding an article

Copy `docs/article-template.md` into `src/content/articles/your-slug.md` or `.mdx`.
Edit the metadata, supply verified sources, and set `draft: false` to publish.
The file's slug becomes `/Homepage/articles/your-slug/`.

```yaml
title: 'A title about the work'
description: 'A concise introduction'
type: project
status: experimental
topics: [chess, artificial-intelligence]
tags: [neural evaluation]
featured: false
date: 2026-10-12
draft: false
visual: chess
github: https://github.com/simsim314/Deep-Formix
sources:
  - label: Project documentation
    url: https://github.com/simsim314/Deep-Formix
```

Required fields: title, description, type, topics, status, date, and sources.
A source has a label and normally a URL; author-supplied unpublished materials
may use a label without a public URL. `note` identifies a research note, while
`preprint` identifies work with a public preprint.
`showPreview`, `presentationOrder`, `updated`, `github`, `demo`, `demoNote`, `image`, `imageAlt`, `imageCredit`, and `imageSource` are optional.
`date` is this article's publication date, not the repository's creation date.
Initial articles were prepared on October 12, 2026; historical result dates are
stated in the article body with their sources. Change `updated` for substantial
revisions; don't alter publication dates just to promote an article.

Statuses: `demonstrated`, `implemented`, `experimental`, `candidate`, `ongoing`.
Types: `research`, `project`. Multiple topics refer to the same article; they do
not create copies. Metadata updates automatically flow to the homepage, interest
pages, research/project indexes, related articles, search, and sitemap.

### Mathematics, images, and demonstrations

Use `$...$` for inline LaTeX and `$$...$$` for display equations. KaTeX renders at
build time with locally bundled CSS/fonts. MDX uses the same math processor.

Use root-relative Markdown links such as `/articles/catforce/` or
`/images/gear-wire.gif`. A remark plugin adds `/Homepage` automatically. In Astro
and MDX components use the `href()` helper from `src/lib/content.ts` for local
URLs; raw HTML/component attributes are not rewritten by the Markdown plugin.

For optimized project images, place a PNG/JPG in `src/assets/images/` and set
`image: /images/filename.png` plus an accurate `imageAlt`. A GIF can use a public `/images/` path and remains animated. The site generates WebP
variants at build time. Public GIFs or other files go in `public/images/`.
Record provenance in `docs/asset-sources.json`. Use `imageCredit` to distinguish
repository screenshots, licensed diagrams, and generated illustrations, and
`imageSource` for a direct credit link. The original LifeWiki schematic is stored
with its source credit and GFDL 1.2 license. Built-in SVG illustrations and
the computed Mandelbrot image are identified as subject illustrations.

The exact Simkin-gun animation can be regenerated with
`python scripts/render-life-gif.py` (optional Python/Pillow development tooling).
The Simkin Glider Gun article’s Life simulation runs at 10 generations per second by default,
with Play/Pause, step, reset and speed controls. It respects reduced motion.
GIF first frames provide a reduced-motion fallback; a footer control pauses
other animated images.

A `demo` URL adds an on-demand iframe with a direct-link fallback. External demos
load only after a reader requests them. The webcam experiment opens externally
because it requests camera access. Do not embed unverified demo URLs.

## Adding an interest

Add `src/content/interests/your-interest.md` with `title`, `description`, `order`,
frontmatter and an introductory body. Its filename is its topic ID.

```yaml
title: 'An interest'
description: 'The questions explored here.'
order: 8
visual: packing
```

Interest cards show a named representative article from their own collection.
Set `representative: article-slug` on a main interest; it must refer to a
non-draft, illustrated article connected to that interest. Main interests are
automatically numbered by display order; nested interests appear within them.
A `visual` field is accepted for compatibility but is optional.
The landing page, homepage card, filter, and footer navigation are generated.
Optional `parent: cellular-automata` makes an interest a child of Cellular Automata.
Articles inherit parent categories automatically; invalid parents and cycles fail the build.
Unknown or duplicate article topics fail the build rather than silently orphaning
content. Draft articles are excluded from every published index and route.

## Editing the author's voice and contact information

`docs/editorial-guide.md` records the writing style learned from the interview,
its factual contributions, and questions to continue. Use first person only for
motives and recollections the author supplies. Keep repository-based explanations
factual and distinguish implementation, experiments, and candidate claims.
`docs/content-sources.json` records the initial evidence review.

Edit `src/lib/site.ts` for verified contact details. The author supplied `simsim314@gmail.com` for public contact; no arXiv profile URL has been supplied. The sphere-packing article links the verified research preprint directly. The existing
`Spirtuality` repository is separate and is not imported or modified.

## GitHub Pages deployment

`astro.config.mjs` sets:

- `site: https://simsim314.github.io`
- `base: /Homepage`
- static output and trailing slashes

In **simsim314/Homepage → Settings → Pages → Build and deployment**, select
**GitHub Actions** as the source. Push to `main` or run **Deploy to GitHub Pages**
manually from Actions. The workflow installs the lockfile, runs `npm run verify`,
uploads `dist/`, and deploys it using GitHub's Pages environment and OIDC token.
Pull requests run validation/build without deploying. No secret is required.

If the GitHub Pages environment has reviewer restrictions, satisfy those in the
GitHub UI. The website is served at the repository path, not the domain root.

## Structure

```text
src/content/articles/   # one Markdown/MDX source per article
src/content/interests/  # metadata and introduction per interest
src/content.config.ts   # typed, validated metadata schemas
src/lib/                # shared collection, URL, and contact helpers
src/components/         # cards, visuals, Life simulation, opt-in embeds
src/layouts/            # navigation, SEO, accessibility, footer
src/pages/              # generated routes, indexes, search, sitemap
src/styles/             # responsive journal design
src/assets/images/      # original repository screenshots, optimized by Astro
public/                 # favicon, computed illustration, GIFs, robots.txt
scripts/                # Markdown base-path plugin and build verification
.github/workflows/      # validation and GitHub Pages deployment
```

## Image placement policy

Each content visual belongs to one article. Its homepage preview and its own
article page may show the same visual; different articles must never share it. A topic card may show a clearly named
article from that topic. Its picture and theme heading open the thematic interest page; the explicit named-example caption opens the article. Category indexes, the journal, and related articles use image previews where
available. Thematic pages have visible introductions and their own curated article order (`articleOrder`); the date of a recent article does not determine where a topic story begins.
The Simkin gun appears in the original homepage hero and on its own article,
with playback controls. The homepage canvas links directly to that article.
Other covers appear in the homepage preview and on their own article pages.
Set `homepageHero: true` on one article to select the lead exhibit. The build
verifier tracks article ownership and rejects images or diagrams reused by a
different article or topic, including identical file contents under different names.
The review page links to each article’s preview without adding a separate gallery.

The museum article is retained as a draft and excluded from published routes,
search and indexes. `presentationOrder` sorts articles sharing a publication
date; Chess960x960 is placed last without changing its date.

`docs/neural-ca-example.json` records the original ONNX model SHA-256, the
synthetic input, and five genuine intermediate outputs. The optional Python
renderer `scripts/render-neural-animation.py` recreates the animated preview using Pillow.
LifeAPI’s static code image and CatForce’s placement animation can be regenerated
with `scripts/render-code-preview.py` and `scripts/render-catforce-preview.py`.
New articles are text-only unless they have an `image`, which automatically
enables their preview. Use `showPreview: false` to hide a preview, or explicitly
set it to `true` for one of the unique diagrams in `ArticleVisual.astro`. Each
new preview needs a distinct image and the author’s approval before publication.
`docs/life-discovery-coverage.json` records the 11 discoveries listed on the
author’s LifeWiki profile and their corresponding source-backed articles.
No inference package or model download is required to build the website.

## Life tile article and models

`src/content/articles/life-in-3d-tiles.mdx` is the normal article at
`/Homepage/articles/life-in-3d-tiles/`. Its metadata adds it to the homepage,
Cellular Automata, search, and related articles. `LifeTileSet.astro` displays every
type in each family in one compact shared-plane 3D image. Four worked 2D
input/output examples reuse the earlier schematics; full glider drawings are
expandable. Each set (blue, orange, purple, black/white, and boundary blue) has
one visible rotatable example beneath its group image, with independently rotatable
top and underside views shown together (stacked on mobile). Reset restores both
faces. Viewers activate near the viewport, release WebGL
resources offscreen, and preserve their camera state when revisited. The
complete assembly has a separate viewer with a 0–200 mm layer-spacing slider,
starting at 40 mm. Top, underside, reset, zoom, and keyboard controls are
available. Three.js, the shared GLB, and assembly data load on demand.

The full-width edge and corner blue variants overhang by half a cell and
contain only two or one underside sockets over real cells. Exterior zeros
are encoded in the output keys; the final grid returns to the input footprint.
`research/3d-tiles/check_boundary_ports.py` tests the actual exported sockets,
wrong-bit rejection, output keys, and exterior solid undersides.

`research/3d-tiles/export_homepage_tiles.py` renders the existing STL meshes
from `research/3d-tiles/bounded-solids/`, copies models and approved schematics
into `public/`, and updates `src/data/life-tile-catalogue.json` and the cover.
Regenerate with Python, NumPy, Pillow, and trimesh installed:

```sh
python research/3d-tiles/export_homepage_tiles.py
python research/3d-tiles/render_compact_sets.py
python research/3d-tiles/render_assembly_cover.py
npm run verify
```

Python is only needed to regenerate these assets, not to build the website.
The 32 exported types are nominal prototypes with zero mating clearance; see
the included design notes before preparing physical prints.

`npm run preview -- --port 4321` serves the last build. After editing, rebuild
or use `npm run dev -- --port 4321` for live updates (stop the preview first).

## Current topic grouping and switch-engine animation

The main interests are Papers, CA Research, Conway’s Game of Life, Cryptography
& Implementation, Chess, and Engineering & Computing. Computational geometry
remains nested within Papers (which includes preprints and unpublished notes);
Life is a separate main collection rather than a child of CA Research. Neural
CA belongs to CA Research. AI remains an article theme/tag in Deep-Formix and
other relevant work, without a separate AI topic. The old AI route redirects
to CA Research; its former introduction is archived in docs/historical-interests/.

Switch-engine ping-pong is featured and ordered before the 24/25-cell growth
seeds. Its cover is an actual Golly HashLife animation with a fixed close view
of the growing fan at sampled generations 33,554,432–67,108,864. The simulation
uses the full plane; only the displayed view is cropped. Each lit image pixel
represents a square containing live cells. The last sampled state is the
pause/reduced-motion fallback. Regenerate with installed bgolly and Pillow:

```sh
python scripts/render-switch-engine-ping-pong.py
```

The renderer verifies the 23-cell seed and compares decoded generation 64 with
an independent sparse B3/S23 implementation. Source and frame-generation
provenance are in research/switch-engine-ping-pong/animation-check.json. New
visuals remain local review material; website publication still needs permission.
