# Website verification — October 12, 2026

The assembled site has 30 local-preview articles and ten interest categories.
The museum source remains a draft and is excluded from routes and indexes.
The sphere-packing article now uses the author’s interview and verified October 8
Gargava–Gröbner–Simkin preprint, rather than the obsolete private-manuscript summary.

`npm run verify` passes with zero Astro/TypeScript diagnostics, 49 generated
HTML pages (including a compatibility redirect), and 1,924 internal link/asset checks. The verifier checks Markdown
and MDX equations, local KaTeX fonts, canonical article coverage in search and
sitemap, image and diagram ownership by article, and animated-image pause fallbacks.

Browser checks passed:

- The new 3D Life article renders its equations, tile-count table, and exact forum
  post links. It connects to the distinct still-life printing article and MMG.
- CA Research contains 21 connected articles, including its Conway’s Life child.
  The Conway’s Life page contains five major construction/tool articles; the
  eight smaller discoveries are collected under CA Research.
- Search for `B2/S0` returns the Live Free or Die discovery; `GPU NNUE` returns
  Deep-Formix.
- The homepage, category page, and Serizawa article have no horizontal document
  overflow at a 375-pixel content width (a 390-pixel frame with a scrollbar).
- The Neural CA demo is absent until requested, then its embedded model reaches
  Ready. No browser errors were reported.
- The gun article now contains its animation. Pause held generation 135 across
  observations, and Step advanced it to 136. Reset and speed controls remain present.
  The original animated homepage hero is restored, and its canvas links to the
  animation on the gun article. The author explicitly permits a homepage preview
  and its own article to share a visual. Article pages now show their own covers.
- The restored hero and controls have no horizontal overflow at a 375-pixel
  content width; the highlighted cursor is also active on the clickable canvas.
- The Chess960×960 embed loads its board and Stockfish evaluator; a depth-12
  evaluation completed and displayed 1.53 pawns.
- Animated project previews have local still frames for pause/reduced motion.
- The highlighted cursor is active on the page and links.

GitHub Pages configuration is prepared for `simsim314/Homepage` and `/Homepage/`.
GitHub's repository metadata currently reports `has_pages: false`. The connected
GitHub tools can update source, but do not expose Pages settings; the browser is
signed out. Enable the GitHub Actions Pages source after browser sign-in.

The author approved all four revised visuals: LifeAPI code, CatForce placements,
Neural CA model outputs, and the 3D sphere illustration. Neural CA timing was then
adjusted as requested: input 3 seconds, intermediate frames 220 ms, final frame
1 second. Deployment has not been performed. Website uploads require the author’s explicit permission,
which has not been given. The raw convex-hull documents remain outside the repository.

The title is now “Independent researcher”; self-taught is in the biography.
The construction-piece viewer loads on request, supports part selection, top/base
separation and keyboard camera controls. CAD source and ten STL exports are local.
All ten meshes are closed, consistently wound, positive-volume single solids;
physical print/fit is untested. The nominal CAD pair has about 0.01 mm³ of overlap.
The package contains construction pieces, not the 26 compound Life tiles.
Thingiverse publication was requested, but account sign-in, cover approval and
a license selection are still pending. Website upload permission remains withheld.

The construction-piece viewer was checked at a 360-pixel content width inside a
375-pixel frame: no horizontal document overflow, the canvas resized to 278 pixels,
part selection worked and keyboard rotation responded. The header showed
“Independent researcher · Tbilisi, Georgia”.

## Tile article integration — October 13, 2026

The Life-in-3D article now presents the actual computational tiles: 26 types
plus six boundary types, in five complete colour-coded sets. The earlier
construction-piece selector has been removed from the article; its archived
assets and source remain available. Four existing Python SVG schematics
illustrate routing, both orange passes, classification, and the final tiles.

`npm run verify` passed: no Astro diagnostics; 49 HTML pages, 30 canonical
articles, 2,018 internal links/assets, equations, search, sitemap, and visual
ownership checked. The optional Three.js chunk triggers a size advisory; it
is loaded on request, not required to read the article.

Browser checks on the built site at localhost:4321 confirmed 32 visible tile
figures, five sets, no select elements, no broken loaded images, and successful
loading of all five whole-set 3D views with no console errors. At a 390-pixel
viewport, figures stack into one column with no horizontal page overflow.

The preview had been serving an older build; rebuilding refreshed the article.
No website upload or deployment was performed.

### Compact tile presentation

Replaced the 32 separate tile figures with five shared-plane 3D set renders.
Only blue B1 has an optional rotatable example; browser checks confirmed five
set figures, one rotation button, one working canvas, and no broken loaded
images. Worked blue/orange/purple/final input-to-output examples are cropped
from the earlier SVG schematics; the full glider diagrams are expandable.
`npm run verify` passed again with 1,976 internal links/assets checked.
The new render script is `research/3d-tiles/render_compact_sets.py`.

### Individual tile rotation and assembly spacing

Each compact set now exposes buttons for every tile type. One viewer per set
opens on demand; the complete 286-piece assembly has its own viewer and a
0–40 mm layer-spacing control. Original mesh coordinates and stored rotation
centres are preserved for assembly placement. At zero extra spacing the
placements match the nominal model; changing spacing offsets each layer only
along z. Top/underside/reset, zoom, keyboard rotation, and close controls are
available. Underside lighting and an oblique underside view reveal socket depth.

Browser checks selected all 32 types successfully, loaded all six viewers,
exercised slider endpoints (0 and 40 mm), and found no console errors. At a
390-pixel viewport, every canvas resized to 306 pixels without page overflow.
Astro check reported zero errors/warnings; build and 1,976 link/asset checks
passed. All changes remain local.

### Dedicated viewers and overhanging boundary variants

Each of the 32 types now has its own visible viewer and controls, arranged in
two columns on desktop and one on mobile. Offscreen WebGL renderers are released
and camera state is restored on return. The complete assembly starts with
40 mm extra spacing per layer and allows 0–200 mm.

The six boundary variants were rebuilt with full 60×60 mm blue bodies, not
ordinary four-socket pieces shifted off the board. Edge variants have two
sockets; corners one. The other underside positions remain solid, and all
16 top data keys encode real inside bits and constant exterior zeros. The
blue layer spans [-30,330] mm in x/y; the input and final layers both span
[0,300] mm. This implements the author’s half-cell overhang proposal.

The regenerated 286-piece assembly passes 875 overlap checks; maximum measured
overlap is 0.000178 mm³ (numerical tolerance). Actual boundary STL checks verify
96 complete output keys, 10 correct sockets, wrong-bit rejection at every
socket, and solid undersides at all 14 exterior positions. All six new meshes
are connected and watertight. The final glider retains five live cells on 5×5.

Browser verification of this revision visited every one of the 32 dedicated
viewers and exercised its underside button, with 32 distinct live models and
no console errors. The assembly control starts at 40 mm, reaches 200 mm, and
returns to 40 mm. At 390 px, document width was 375 px with no horizontal
overflow. Only nearby viewers retain WebGL contexts. Astro diagnostics were
clean and the build verifier passed 2,009 internal links/assets.

### One rotatable example per set

Corrected the presentation to five individual viewers: one representative for
blue, orange, purple, black/white, and boundary blue. Each remains beneath its
compact whole-set image; the complete assembly retains its separate viewer.
Browser checks counted exactly five example viewers and loaded and turned over
each one. The assembly slider remains 0–200 mm, initially 40 mm. Astro check
reported no errors or warnings; build and 1,982 internal link/asset checks passed.

### Complete input/output explanations

Added expandable tables for all six blue, eight orange, eight purple, four final,
and six boundary types. Added a complete glider-cell trace distinguishing the
original centre channel from auxiliary C outputs, and explaining simultaneous
Life evolution. Tables were derived from the local logical definitions; the
512-neighbourhood verifier passes and the worked example returns category 4,
original centre 1, and next state 1. Browser inspection confirms table row counts
6/8/8/4/6 and the new walkthrough. Astro diagnostics and build verification pass
(1,983 internal links/assets). Geometry and the five representative viewers are
unchanged.

### Keep both faces visible after 3D loads

Each of the five representative tile examples now mounts two independently
controlled views of the same mesh: output/top and input/underside. Reset restores
the two initial camera poses; each pose survives offscreen release and remount.
The complete assembly retains its single viewer and 0–200 mm spacing control.
Browser checks loaded both canvases for every family, exercised keyboard rotation
in each, and returned to blue after visiting the other sets. No console errors.
At a 390 px viewport, the views stack and document width equals its 375 px client
width; the mobile article grid now permits shrinking to its available width.
Astro diagnostics and build verification pass (1,984 internal links/assets).

### Six illustrated main topics and source images — October 13, 2026

The author's new request supersedes the text-only topic/index layout. The ten
existing topic routes are grouped into six main interests and four nested
interests. All six main cards feature named work from their own collection.
The journal is a responsive image grid with 25 illustrated article previews;
category and related cards also show each article's own cover. The gun hero
remains the original interactive exhibit. Selected work contains four articles,
with the gun already represented by the lead exhibit.

Added eight source LifeWiki diagrams, an exact Remini constructor crop rendered
from the original macrocell, and three original 2016 printing photographs.
Credits and provenance are recorded; the new images remain local review material.
Remini now includes the author's October 13 answers and specific forum sources,
after reading both pages of thread 3836. The still-life print source is corrected
to post 31711; post 31727 discusses colours rather than reporting the first prints.

Astro check: zero errors, warnings, and hints. Final build and verifier pass:
49 HTML pages, 30 canonical articles, 2,326 internal links/assets, math, search,
sitemap, unique IDs, and article visual ownership. The lazy Three.js chunk retains
its pre-existing size advisory. The Remini decoder verifies all 779,984 source
cells, quadtree references and levels, and records the source hash and crop.

Browser checks: six illustrated topics, three desktop journal columns, 25
journal previews, all topic images loaded. At a 390 px viewport, document width
and scroll width are both 375 px; topics and journal stack in one column.
Mathematics filtering includes both sphere packing and the nested hull note;
Engineering includes its eleven direct/inherited articles. Remini and the
still-life article have no mobile overflow; the latter contains its two original
printer photographs beneath the printed-pieces cover. The viewport override
was restored. No upload, push, or deployment occurred.

### Papers, separate CA/Life topics, and Golly animation — October 13, 2026

Six main topics now read Papers, CA Research, Conway’s Game of Life,
Cryptography & Implementation, Chess, Engineering & Computing. There are nine
interest sources, including three nested interests. The retired AI source is
archived in docs/historical-interests/; its old route redirects to CA Research.
Neural CA belongs to CA Research, and Deep-Formix retains its AI theme/tag under
Chess/Computing. Papers includes explicitly labelled preprint and unpublished
research-note material; the grouping does not imply peer-reviewed publication.

Switch-engine ping-pong is featured and ordered before the 24/25-cell growth
seeds. Its cover uses 33 real Golly 3.3 HashLife snapshots at generations
33,554,432–67,108,864. A fixed crop of the growing fan was selected after
comparing wider and closer views. The full plane is simulated; pixels aggregate
32,768 × 32,768-cell regions. The final population is 124,270,961. The seed has
23 cells; the decoder agrees cell-for-cell with an independent sparse Life
implementation at generation 64 (163 cells). The final state is the static
pause/reduced-motion fallback. The renderer, seed hash, crop, frame generations,
and populations are preserved in research/switch-engine-ping-pong/.

`npm run verify` passes: zero Astro diagnostics, 49 HTML pages, 30 canonical
articles, 2,252 internal links/assets, equations, search, sitemap, unique IDs,
and article visual ownership. The existing lazy Three.js chunk advisory remains.
Browser filters show 16 CA articles including Neural CA, and five dedicated
Life construction/tool articles. Ping-pong appears in selected work and before
the 24/25-cell seeds in the journal. Its article has equal client/scroll widths
of 375 px at a 390 px requested viewport; the pause control loads the correct
800×520 static fallback. Everything remains local, without upload or deployment.

### Real pattern gallery and captioned ping-pong — October 13, 2026

The main mathematics title is now Mathematical papers. Caterloopillar and LifeAPI lead Selected work; topic representatives no longer repeat there, so each article appears at most twice on the homepage. All 30 articles remain in the journal, with 29 illustrated previews. The gun hero is preserved.

New animations were rendered with installed Golly 3.3 under B3/S23, B2/S0, Serizawa, and GeminoidParticles. Every animation has an equal-dimension still fallback. The captioned ping-pong cover shows individual cells at 15 pixels/cell, with holds between approach, collision, and return-glider stages. It lasts about 26 seconds. Its expanded source window and final search region were checked against the full source run; its camera follows an exact detected NW glider. The wider exchange and growth fan are secondary article images.

Remini shows activation at generations 0–2400, with a causal source margin and a generation2048 full-pattern comparison. Serizawa growth now runs 262144–1048576, after the author rejected the early transient. RuleLoader’s decoded initial states/coordinates agree with original RLE for both construction crops. The B2/S0 ship agrees with independent sparse updates at 0,1,6,60 and translates (-2,0) after six generations.

All 238189 live cells of the downloaded c/8 Caterloopillar match an exact upward250 translation after 2000 Golly generations. The rewritten article follows the archived eight-page development thread and the completed construction announcement, credits collaborators, and adds the verified 2016 Pattern of the Year award. It also animates the original Nov14 forward reaction.

Browser checks confirm the current collision cover and pause fallback load at800×600; the topic heading, selected order, all journal previews, and long-record chronology are present. The two updated articles have equal document client/scroll widths at the available desktop sizes. A requested390px viewport override did not apply in this restarted browser session; do not claim a fresh mobile breakpoint check from that attempt. Prior mobile checks remain documented above. The temporary override was reset and research tabs closed. A review screenshot is saved in .editorial-private/reviews/ping-pong-closeup.png. Everything remains local.

Final `npm run verify` passes with zero Astro diagnostics: 49 HTML pages, 30 canonical articles, and 2,320 internal links/assets. The homepage appearance limit also passes. Python render scripts compile successfully. The existing lazy Three.js bundle advisory remains.

## October 13: latest ping-pong and convex-hull corrections

The full-cycle ping-pong cover supersedes the rejected collision cover; both streams are visible. Exact original Golly states and detected signals are recorded by render-ping-pong-cycle.py. Collision is optional detail. The convex-hull article uses author-provided v7 TeX/PDF, both retained outside the repository, and Figure1 page5 for a local cover. Sequential and external shuffled-prefix replay bounds are stated separately with access costs and assumptions. The author tentatively dates the methodology to around2009 and recalls comparing algorithms under read-only tape constraints. All30 articles now have previews. Publication remains unauthorized.

Latest verification: npm run verify passes with zero Astro diagnostics, 49 HTML pages, 30 canonical articles, 2353 internal links/assets. New cycle fallback loads under image pause; both revised desktop pages have no overflow. Confirmed hull body and metadata use 2009. Screenshots: .editorial-private/reviews/ping-pong-cycle.png and convex-hull-v7.png. No fresh mobile check or publication.

Verified these editorial changes with npm run verify: zero Astro diagnostics, 49 HTML pages, 30 articles, 2362 internal links/assets. Browser confirms linked construction history and no desktop overflow; public hull text has no internal version tag. Screenshot .editorial-private/reviews/gemini-origin-story.png.

## Both ends of the Geminoids

The author rejected short circuitry clips: show two arms building completed heads, both ends and the long instruction tape, including the snake-like overall movement. Main animations now show synchronized end views and explicitly vertically compressed whole-pattern tape occupancy. Serizawa runs0–25165824, Particles0–49152. Native Golly full-pattern states under the correct rules. Both-end head-circuitry matching and full-plane Serizawa digests are in research/ca-visuals. Cell marks enlarged; actual Serizawa arm targets marked, Particles movable blocks highlighted blue. First-end construction clips are optional collapsed detail. No publication.

Final layout override: the two end views are UPRIGHT, side by side, preserving aspect ratio and following each successive operating head after the first replacement finishes. Earlier rotated-panel descriptions are superseded. This keeps both active arm targets visible; actual rings identify Serizawa elbows on perpendicular axes, blue highlights state7 movable blocks in Particles. Whole-pattern tape overview remains vertically compressed and explicitly labelled. Optimized tape renderer is exact: its occupancy matches independent aggregation of every cell at8388608. Reports include actual arm target positions. Scripts regenerate source checkpoints when temporary caches disappear.

Final checks: Verified 49 HTML pages, 30 canonical articles, 2364 internal links/assets, Markdown/MDX equations, search index, sitemap, and visual ownership by article. Python renderers compile. Both main covers and still fallbacks load at1100×760, with enlarged article display and no desktop overflow. Fresh screenshots: .editorial-private/reviews/serizawa-both-ends.png and particles-both-ends.png. Local only; no fresh mobile check.

## October 13: article-first navigation, classification, and native Life animations

Latest author requests supersede earlier grouping: **all B3/S23 discoveries and physical Life projects belong to Conway’s Game of Life**. CA Research now has exactly five published entries: Serizawa Geminoid, Geminoid Particles, neural CA, Serizawa quadratic growth, and the Live Free or Die c/3 spaceship. Life has sixteen. B60, BNE14T30, BRx46B, Ocellus, Simkin’s p60, 24/25-cell growth, ping-pong, both tile articles, and MMG moved from CA to Life. Engineering/computing cross-listing is preserved.

**All articles is the first section after the original introduction/gun hero**, ahead of topic images and Selected work. The main navigation and hero action link directly to it. Topic image/title links now open filtered topic collections; the explicit named-example caption still opens its individual article. Topic collections show matching articles once, parent/subtopic breadcrumbs, and a topic sidebar. Article sidebars contain Topics plus On this page. Homepage journal and Research/Projects collections also have topic navigation. Geometry is under Mathematical papers; programming and simulation are under engineering.

New native Golly covers: B60 (0–60), BNE14T30 (0–144), BRx46B (0–46), Ocellus (0–114), Simkin’s p60 (0–60), 24/25-cell growth (4194304–16777216). Original RLEs extracted from LifeWiki’s embedded original source or actual downloadable RLE; provenance in research/ca-visuals/lifewiki-pattern-sources.json. Five small endpoints agree exactly with independent sparse B3/S23. Ocellus and p60 return to the complete original state. Seed populations 24/25 and exact generation64 states independently checked. Full final populations 54564537 and 91253066; growth square side16384, fixed view, no finite simulation boundary. scripts/render-life-results.py and *validation.json record this.

Caterloopillar’s main new cover `life-caterloopillar.gif` pairs the credited LifeWiki architecture schematic (dvgrn, GFDL1.2) with the original November2014 forward-glider reaction evolved through140 generations. It is **not a whole-spaceship evolution clip**. Rebuild with scripts/render-ca-gallery.py caterloopillar then scripts/render-caterloopillar-cover.py. Full original c/8 also simulated through2000 and exact238189-cell translation(0,-250) rechecked. Experimental two-end crops proved too sparse; their renderer is separate and not used as the cover.

**LATEST VISUAL OVERRIDE:** the author rejected the new LifeAPI glider/column animation and tile animations, saying he liked the earlier versions. Restored LifeAPI’s static syntax-highlighted code image, the original exploded 3D tile cover and interactive viewers, and physical still-life photographs. Removed new animation explanations from those articles. These are explicit exceptions to the earlier blanket animation request. Do not reintroduce them. Rejected local experiments are archived under .editorial-private/rejected/lifeapi-and-tiles-animations, outside published assets. All other CA/Life results retain animations and pause fallbacks.

Verification after restoration: npm run verify passes, zero Astro diagnostics;49HTML pages,30canonical articles,2611internal links/assets. Verifier checks article-first order, correct Life membership, matching topic/subtopic collections, sidebar selection, canonical topic-image routing, article Topics+TOC, and animations with the author’s three explicit visual exceptions. Browser confirmed CA’s five GIF covers, restored LifeAPI image/body, geometry’s single hull article, article Topics+TOC, and no desktop overflow. No new mobile viewport verification or publication.

## October 13: definitive thematic-homepage correction and Caterloopillar reader

**LATEST HOMEPAGE OVERRIDE:** the author clarified that the main homepage chapter must show INTEREST THEMES, not individual articles. Recent articles is fine below. This supersedes the earlier misinterpretation that moved the whole journal to the top. Final structure: original introduction/gun hero → six image-backed interest cards → Recent articles → About/contact. Removed the separate Selected work article grid so the main chapter stays thematic. Hero action points to #interests. All articles remains a direct header link to the lower journal. Topic images/headings open /interests/<id>/, never the representative article; only the explicitly named-example caption remains a direct article link, as previously requested.

All nine thematic pages now display their introductions openly, rather than behind a collapsed About button. Added per-interest `articleOrder`, validated against membership/duplicates. Life starts with Gemini origin and construction themes; article order begins Remini, Caterloopillar, gun, LifeAPI, CatForce, ping-pong. Physical tiles follow those, regardless of newer article date. CA stays separate with its five non-Life/neural subjects. Cryptography and Engineering pages expanded into linked thematic introductions; the other topic/subtopic introductions remain visible. Each page includes all matching canonical articles once and retains topic/sidebar/subtopic navigation.

The author’s screenshot specifically pointed out **missing spaces around About-page links** (originalGemini, wasSerizawa, builtGeminoid, comma-separated titles). Added explicit Astro space nodes; browser confirms the full paragraphs have normal spaces and punctuation. About now also links directly to both Life and CA thematic pages. Build assertions cover the exact previously broken phrases.

Read the author-supplied inspiration, Gabriel Nivasch’s Caterpillar article: https://www.gabrielnivasch.org/fun/life/caterpillar . Follow its useful progression from animated components to whole construction; do not conflate Caterpillar with Caterloopillar, copy its prose, or attribute its reactions to this author.

**Caterloopillar main cover now `caterloopillar-reading-head.gif` (800×660)**. The author requested an actual reading-head mechanism/ship integration/deletion animation. Found the original forward reader in Code/WSSStapler.py, downloaded source preserved in research/caterloopillar/source-code/Code-WSSStapler.py. Renderer scripts/render-caterloopillar-reader.py reads literal RLEs without executing original Python or loading pickles. Reassembles exact frontFrontPart, frontReflectingPart, frontBackPart, frontSL placements for distance250, d76. Initial138cells include a seven-cell LOAF tape symbol, not a four-cell block. It activates, emits a glider, reflects it between spaceships, rebuilds the loaf250cells forward, and emits one construction glider. Full isolated mechanism evolved in Golly, no finite cropped simulation.

192frames generations0–1440; stages/holds at activation, travel, reflection, rebuild. Top overview rotates90degrees; actual enlarged zoom uses original orientation and follows exact detected gliders. Reference markers label original Start and +250 position; only real native cells are drawn. Loaf rebuilt by1408 and remains at2048. At2048 ALL131 original spaceship-convoy cells match initial convoy translated(0,-1024), plus the moved7cell loaf and exactly5cells of one output glider. Native states0,256,768,1408,1440,2048 agree with independent sparse B3/S23 cell for cell. Source/hash/cameras/positions in research/caterloopillar/reading-head-animation-check.json. Article starts with a short stepwise mechanism explanation and keeps the credited dvgrn architecture schematic separately at /images/caterloopillar-architecture.png. The old basic2014 forward-reaction GIF remains in the development story; the old hybrid schematic cover is superseded.

LifeAPI code preview, original exploded tile cover/viewers, and real printed-tile photographs remain as restored; do not reintroduce rejected animations.

Verification: npm run verify passes, zero Astro diagnostics;49HTML pages,30canonical articles,2623internal links/assets. Assertions cover themes before journal, visible thematic intros, Remini/Caterloopillar-first Life reading order, correct category membership, link spacing, every matching canonical article, and visual ownership/fallbacks. Python renderer compiles. Browser confirms all six topic image destinations, a real click into the Life thematic introduction, first four Remini/Caterloopillar/gun/LifeAPI, repaired About paragraphs, native readerGIF800×660 loaded, and no desktop overflow. Screenshots: .editorial-private/reviews/homepage-themes-first.png, life-theme-introduction.png, caterloopillar-reading-head.png, about-link-spacing.png. No fresh mobile check or publication.


## October13: late Caterloopillar construction tour and Three loading repair

The final cover leads with actual tight forward/backward inserters from the complete c/8 RLE. Old/new ship cell sets checked at generation1600(up) and1400(down); exact independent4generation motion confirms their identity. Both old ships remain intact, with relative new offsets(3,-9) and(-9,-15). Full native Golly clips also show head/tail erasure through empty final camera regions. The explanatory one-symbol block reader agrees with independent sparse Life at selected states and preserves the entire convoy; its block advances59cells. Resumed full checkpoint at1200 exactly matches a separate original-source run. See research/caterloopillar/mechanisms-animation-check.json.

Reproduced blank assembly as stale optimized Three dependency URLs (HTTP504 OutdatedOptimizeDep), fixed by excluding Three from dev optimization and refreshing Astro. Added the actual assembly preview and retry button for load failures. Browser confirms assembly ready=true/live canvas after final verify, both blue faces live, range0/40/200, camera controls, drag and close, no console errors.

Final npmrunverify: zero errors/warnings, one existing hint;49HTMLpages,30articles,2632internallinks/assets. Assertions cover final clip sequence/late-first body, no inflated breakthrough section, assembly fallback/retry, and all existing thematic constraints. Browser confirms8loadedGIFs, pause stills, restored playback, no desktop overflow. Screenshotproof in .editorial-private/reviews/caterloopillar-late-inserters-cover.png, caterloopillar-backward-tight-insertion.png, tile-viewer-repaired.png. No mobile verification or publication.

## October 13: latest Caterloopillar correction — components accumulate into a loop

The author rejected the early/simple reactions and the rotating tour as the main explanation. The latest design supersedes the previous “late inserters lead” article order: small components lead, but the difficult later mechanisms supply the examples. The main article is now `src/content/articles/caterloopilar.mdx`, same canonical route; `showPreview:false` keeps the whole-loop card animation from jumping ahead of the explanation.

Eight stages: working loaf activation → later glider reversal/splitting and routing → reader reflection + 250-cell tape restoration → spacing/slow-salvo instructions → forward close insertions → backward close insertion → head/tail erasure → complete architecture. `CaterloopillarBuild.astro` accumulates a functional connection diagram beside the explanation, then reveals the credited dvgrn architecture at stage8. `CaterloopillarStep.astro` defines the numbered sections. Mobile uses the stacked explanation, with the full original architecture in the last stage even without JavaScript. The logical connection map is conceptual; animated Life cells are never invented.

New original-source clips, rendered by `scripts/render-caterloopillar-difficult-parts.py`:
- `glider-reversal`: later 244-cell forward head assembled from literal components of original WSSStapler, g712–832 step2. Southwest glider present at720; northeast return plus southeast output at800. Independent full-plane Life matches at0,712,760,800,832. This is the timing/erasure branch, distinct from tape data.
- `signal-routing`: same head, g480–920, tracks preceding split, turn and return-output split. Separate actual tape reflection/restoration clips also retained to explain the data path.
- `insertion-clearance-failure`: original dvgrn p21826 eight-case gallery. Selected passing LWSS destroyed by5600. Explicit REJECTED TEST, not a finished-ship mechanism; independent full-plane checks.
- `mwss-beside-hwss`: complete unchanged c/8 pattern, g1280–1760. Old HWSS bbox(282,260534)–(287,260541),13cells; new MWSS11cells reference offset(11,-9). Old preserved and new exact; independent4tick upward motion. View enlarged around actual close pair.
- `working-reader`: same later head, g72–280; seven-cell loaf activation, not a four-cell block.
- Existing forward/backward stream insertions regenerated with much tighter cameras around the pairs (44×48cells). Their exact preserved-old/constructed-new checks remain intact. Full-plane simulation, only camera changes.

Validation report `research/caterloopillar/difficult-parts-validation.json`. Card composite `caterloopillar-mechanisms.gif` updated with later reversal, HWSS/MWSS close insertion, both constructors, tape restoring and erasure; no early2014 block clips in that card tour. First render `scripts/render-caterloopillar-mechanisms.py` would overwrite the detail assets/card with historical examples; the new difficult-parts renderer is the final renderer for these assets.

Research: reread Nivasch Caterpillar progression; downloaded and read later construction thread pages3–7 into `research/caterloopillar/late-construction-thread.json`; original latest generator retained in source-code directory and never executed/unpickled. Full-head RLEs assembled from literal components; `head-signal-survey.json` records measured signal directions. Actual later finished-ship cases and 2015 clearance tests supplied the useful constrained interactions. Preserve sourced slow search history, shared contributions, practical speed/memory limits, and Pattern of the Year2016. No dramatic “realization” story about a bug.

Final checks: `npm run verify` passes (0errors/0warnings, one pre-existing hint),49HTMLpages,30canonicalarticles,2622internal links/assets. Browser confirmed stages2/5/8 update the side diagram; all11native GIFs and their still fallbacks load; desktop and390px mobile have no horizontal overflow. Complete architecture is in the sticky side diagram on enhanced desktop, with an in-body fallback on mobile or without JavaScript, avoiding duplicate desktop pictures. Restored animation playback and default viewport. Proofs `.editorial-private/reviews/caterloopillar-late-glider-reversal.png`, `caterloopillar-mwss-hwss-insertion.png`, `caterloopillar-complete-loop-reveal.png`, `caterloopillar-components-mobile.png`. Cover now220frames. Local only.


## October 13: latest override — explain all bridges, not an eight-step compressed tour

The author explicitly requested: reflector → Caterloopillar-specific reflector → assembled reading head → how it reads → how it encodes slow salvos → how complete heads are created and die. Replaced the compressed8step account with17explicit stages. Stage3 has `CaterloopillarHead.astro`, a selectable component explorer displaying all244original source cells, with highlighted functional groups and enlarged original cells. Stage4 shows the whole original reading-only cycle before activation, inner turn, restoration/output, and cadence are explained separately. Full architecture is withheld until17. All stages have anchor links in the existing TOC and cumulative side context.

Corrected important encoding precision by reading the actual WSSStapler/RecipeManager literals: forward slots at base+250(i+1)+r_i, with command offsets selecting outgoing glider lane and timing; not merely arbitrary gaps. Native tests -4,+2,+6 restore the loaf, preserve the convoy, and produce northeast outputs with minx+miny anchors356,362,366. `SKIP` omits a symbol. The data path’s persistent construction output follows the final conversion. Transient signals from activation must not all be described as emitted recipe commands. Six reading-only convoys and five symbols ahead, offsets0,-4,2,2,-8, provide a native tape-to-salvo example; omission of helices/erasers is explicit.

New native renderer `scripts/render-caterloopillar-stages.py`; report `research/caterloopillar/intermediate-stages-validation.json`. Clips: basic-reflector, command-offsets, tape-to-salvo, whole-head-construction, whole-head-erasure, whole-tail-erasure. Existing full reading-head GIF restored within stage4, existing delicate insertion/reversal clips retained within their role in the sequence. Actual fullhead growth now follows every16ship addition; all16removed at forward erasure,13removed at backward erasure. Original whole c/8 pattern stays unchanged.

Fullhead construction ends at740000ticks. These states are determined exactly from the verified full2000tick /250cell native translation using Life’s translation invariance; intermediate phases use Golly macrocell states. A direct740000run was tried, was too slow, and stopped; DO NOT claim a direct long-run validation. Every one of16 additions is independently identified as an exact co-moving WSS in native states: milestones2000,28000,106000,192000,214000,246000,304000,358000,388000,484000,530000,562000,588000,624000,676000,740000. Unchanging travel between recipe sites is fast-forwarded, explicitly labelled. Whole-convoy overviews and zooms both use actual native cells; zoom reads its own crop so incoming gliders beyond overview edges are retained.


Native selected salvo now recovers0,-4,+2,+2,-8 in emission order at12000, using one nominal output band centred at lane anchor-1140. Other repeats are not counted as that construction program. Measured first crossings of x245 at sampled generations4480,5960,7440,8960,10480. Reader pitch750 gives a nominal1500tick command interval in this band; a repeated read of the SAME restored symbol takes2000ticks (750 reader spacing plus250 tape transfer, at c/2). These distinct cadences are explicitly explained. Native views/independent checks cover0,3000,12000.

Final verification: `npm run verify` passes,0errors/0warnings and one pre-existing hint,49HTMLpages,30canonicalarticles,2638internal links/assets. New assertions require all17stages and the reflector→assembledhead→encoding→salvo→wholehead bridges. Native source diagram component controls tested for reading, turn, and restore. Browser all16 GIF/fallback images load; stages3/10/13/17 update context; final architecture loads only at17, mobile390px has no overflow, native component controls work, and full architecture has its mobile/noJS fallback. Added translateZ(0) to sticky side context after measuring correct layout but missing browser paint; repaint now visibly correct. Playback/defaultviewport restored. Proofs detailed-head-explorer, five-command-salvo, whole-head-build, whole-head-erasure in `.editorial-private/reviews/`. Local only.
