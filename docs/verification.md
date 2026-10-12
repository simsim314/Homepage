# Website verification — October 12, 2026

The assembled site has 26 published articles and nine interest categories.
The museum source remains a draft and is excluded from routes and indexes.

`npm run verify` passes with zero Astro/TypeScript diagnostics, 43 generated
HTML pages, and 1,600 internal link/asset checks. The verifier checks Markdown
and MDX equations, local KaTeX fonts, canonical article coverage in search and
sitemap, image and diagram uniqueness, and animated-image pause fallbacks.

Browser checks passed:

- Homepage interest filtering returns the three Other Cellular Automata articles.
- Search for `B2/S0` returns the Live Free or Die discovery; `GPU NNUE` returns
  Deep-Formix.
- The homepage, category page, and Serizawa article have no horizontal document
  overflow at a 375-pixel content width (a 390-pixel frame with a scrollbar).
- The Neural CA demo is absent until requested, then its embedded model reaches
  Ready. No browser errors were reported.
- The Simkin gun plays at the selected speed and pauses without resetting its
  generation. Step, reset, and speed controls are present.
- Animated project previews have local still frames for pause/reduced motion.
- The highlighted cursor is active on the page and links.

GitHub Pages configuration is prepared for `simsim314/Homepage` and `/Homepage/`.
GitHub's repository metadata currently reports `has_pages: false`. The connected
GitHub tools can update source, but do not expose Pages settings; the browser is
signed out. Enable the GitHub Actions Pages source after browser sign-in.

Image approval remains pending for the revised LifeAPI code image, CatForce
placement GIF, Neural CA model-output GIF, and 3D sphere preview, as recorded in
`docs/asset-sources.json`. Deployment has not been performed.
