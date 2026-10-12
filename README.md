# Michael Simkin — Personal Research Journal

An Astro website at **https://simsim314.github.io/Homepage/**. The homepage is the
journal: interests, featured work, and all recent articles. There is no separate
blog. Twenty-six published research/project articles share one collection and one
canonical URL each, across nine interest landing pages.

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
content images and diagrams across all pages.

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
The homepage Life simulation runs at 10 generations per second by default,
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

Interest cards are typographic and automatically numbered by display order.
A `visual` field is accepted for compatibility but is optional.
The landing page, homepage card, filter, and footer navigation are generated.
Unknown or duplicate article topics fail the build rather than silently orphaning
content. Draft articles are excluded from every published index and route.

## Editing the author's voice and contact information

`docs/editorial-guide.md` records the writing style learned from the interview,
its factual contributions, and questions to continue. Use first person only for
motives and recollections the author supplies. Keep repository-based explanations
factual and distinguish implementation, experiments, and candidate claims.
`docs/content-sources.json` records the initial evidence review.

Edit `src/lib/site.ts` for verified email and arXiv URLs. They are currently empty,
so invented contact details and publications are never shown. The existing
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

A content image appears exactly once across the entire site. Interest cards,
category indexes and related-article links use text cards. Homepage featured
work and recent articles share the visual placements: a featured cover is never
repeated in recent articles.
The Simkin gun appears only on the homepage, with playback controls; its article
links there. All covers appear only on the homepage; article pages link back to their cover. The build
verifier rejects repeated image contents or visual identifiers across pages.
The review page links to each unique homepage placement and does not reproduce
images.

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
