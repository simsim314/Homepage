# Homepage continuation handoff

**Owner:** Michael Simkin (`simsim314`)
**Workspace:** `/home/simsim314/GitHub/Homepage`
**Snapshot:** October 13, 2026, after Golly-rendered gallery, Caterloopillar development story, and close ping-pong collisions
**Purpose:** give a new Codex chat enough context to continue without reconstructing the interview or repeating rejected designs.

This is a working handoff, not website copy. It records user instructions, confirmed recollections, implementation state, evidence, limits, and unfinished work. Read the latest user message before treating any task here as the immediate objective. Later user corrections supersede this snapshot.



## October 13: latest override — explain all bridges, not an eight-step compressed tour

The author explicitly requested: reflector → Caterloopillar-specific reflector → assembled reading head → how it reads → how it encodes slow salvos → how complete heads are created and die. Replaced the compressed8step account with17explicit stages. Stage3 has `CaterloopillarHead.astro`, a selectable component explorer displaying all244original source cells, with highlighted functional groups and enlarged original cells. Stage4 shows the whole original reading-only cycle before activation, inner turn, restoration/output, and cadence are explained separately. Full architecture is withheld until17. All stages have anchor links in the existing TOC and cumulative side context.

Corrected important encoding precision by reading the actual WSSStapler/RecipeManager literals: forward slots at base+250(i+1)+r_i, with command offsets selecting outgoing glider lane and timing; not merely arbitrary gaps. Native tests -4,+2,+6 restore the loaf, preserve the convoy, and produce northeast outputs with minx+miny anchors356,362,366. `SKIP` omits a symbol. The data path’s persistent construction output follows the final conversion. Transient signals from activation must not all be described as emitted recipe commands. Six reading-only convoys and five symbols ahead, offsets0,-4,2,2,-8, provide a native tape-to-salvo example; omission of helices/erasers is explicit.

New native renderer `scripts/render-caterloopillar-stages.py`; report `research/caterloopillar/intermediate-stages-validation.json`. Clips: basic-reflector, command-offsets, tape-to-salvo, whole-head-construction, whole-head-erasure, whole-tail-erasure. Existing full reading-head GIF restored within stage4, existing delicate insertion/reversal clips retained within their role in the sequence. Actual fullhead growth now follows every16ship addition; all16removed at forward erasure,13removed at backward erasure. Original whole c/8 pattern stays unchanged.

Fullhead construction ends at740000ticks. These states are determined exactly from the verified full2000tick /250cell native translation using Life’s translation invariance; intermediate phases use Golly macrocell states. A direct740000run was tried, was too slow, and stopped; DO NOT claim a direct long-run validation. Every one of16 additions is independently identified as an exact co-moving WSS in native states: milestones2000,28000,106000,192000,214000,246000,304000,358000,388000,484000,530000,562000,588000,624000,676000,740000. Unchanging travel between recipe sites is fast-forwarded, explicitly labelled. Whole-convoy overviews and zooms both use actual native cells; zoom reads its own crop so incoming gliders beyond overview edges are retained.

Native selected salvo now recovers0,-4,+2,+2,-8 in emission order at12000, using one nominal output band centred at lane anchor-1140. Other repeats are not counted as that construction program. Measured first crossings of x245 at sampled generations4480,5960,7440,8960,10480. Reader pitch750 gives a nominal1500tick command interval in this band; a repeated read of the SAME restored symbol takes2000ticks (750 reader spacing plus250 tape transfer, at c/2). These distinct cadences are explicitly explained. Native views/independent checks cover0,3000,12000.

Final verification: `npm run verify` passes,0errors/0warnings and one pre-existing hint,49HTMLpages,30canonicalarticles,2638internal links/assets. New assertions require all17stages and the reflector→assembledhead→encoding→salvo→wholehead bridges. Native source diagram component controls tested for reading, turn, and restore. Browser all16 GIF/fallback images load; stages3/10/13/17 update context; final architecture loads only at17, mobile390px has no overflow, native component controls work, and full architecture has its mobile/noJS fallback. Added translateZ(0) to sticky side context after measuring correct layout but missing browser paint; repaint now visibly correct. Playback/defaultviewport restored. Proofs detailed-head-explorer, five-command-salvo, whole-head-build, whole-head-erasure in `.editorial-private/reviews/`. Local only.

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

## October 13: FINAL late-stage Caterloopillar inserters and repaired 3D loading

**LATEST AUTHOR OVERRIDE:** the most interesting reactions are delicate inserters into the FORWARD and BACKWARD *WSS streams, only a few cells from passing ships. Do not substitute isolated edge shooters, glider-to-MWSS births, or early prototypes for those clips. The author explicitly answered that “the two inserters” means the two opposing streams. The article and main cover now LEAD with late insertion stages from the COMPLETE 2016 c/8 pattern. Early reader reactions follow only as explanatory background. Removed the dramatic early “realization / initially thought it would fail” narrative; the author says that incident was just a bug.

Main cover is now `/images/caterloopillar-mechanisms.gif`, 1100×760, 378 frames, about682KB. Original credited dvgrn schematic stays fixed on the LEFT; RIGHT cycles short labelled native clips, with holds and a progress indicator. Sequence: forward-stream insertion → backward-stream insertion → block-to-glider → glider reflection → glider-to-block → head deletion → tail deletion. Article cover is displayed at its natural aspect without the old height cap. All pause fallbacks exist. Renderer `scripts/render-caterloopillar-mechanisms.py`; report `research/caterloopillar/mechanisms-animation-check.json`.

Actual complete-ship insertion coordinates, not fabricated or finite-crop evolution:
- Forward/upward: old LWSS at bbox(145,433949)–(149,433954), 12cells. New LWSS offset(3,-9). Clip generations1040–1600 step8, camera follows the passing old ship and zooms from90 to60cells across. At1600 both exact ship sets match; independently evolved4generations move(0,-2), matching the full Golly run. Cyan marks the existing ship; amber appears ONLY when the newly inserted ship exactly matches actual cells.
- Backward/downward: old MWSS bbox(445,171961)–(450,171967), 11cells including detached sparks. New offset(-9,-15). Clip generations800–1400 step8. The dangerous transient is visible around1000; the new ship is complete by1200. At1400 both exact sets match; independent4generation motion(0,2) matches Golly. This is the other actual construction stream, not another isolated synthesis.
- Full source `research/caterloopillar/Caterloopillar_c8.rle` remains unchanged. Every frame evolves the entire original ship. For speed, Golly resumes saved full macrocell checkpoints; exact resumed state at1200 agrees cell-for-cell with a separate run from the original RLE. The whole ship’s existing exact238189-cell translation(0,-250)after2000 remains verified.

Both erasure clips NOW also come from the completed ship, superseding the early2014 deletion experiments:
- Head close-up: old upward LWSS bbox(145,449)–(149,454), generations920–1408.
- Tail close-up: old downward LWSS bbox(451,514315)–(455,514320), generations600–1056.
- Each starts with the exact old ship present and ends with the selected90×90camera region empty. These are close views of parts of used machinery; they do not claim every cell of a whole head fits in the camera.

The three explanatory reader clips use the first BLOCK from original November2014 p14297 forward reader. `research/caterloopillar/block-reading-head.rle` retains the entire101cell spaceship convoy plus one4cellblock at(42,130); six other tape blocks omitted. Native full-plane states independently checked. Block rebuilt at(42,189), displacement59; at416 all101originalshipcells survive translated(0,208), plus rebuiltblock and one5celloutputglider. Do not call this a loaf/250cell step. Old250cell loaf reader remains a historical separate asset, not the main cover/body.

Article explains tight lane/phase/clearance requirements and chronological research. Latest forum evidence `inserter-forum-evidence.json`, `insertion-library-forum.json`, `trailing-inserter-forum.json` under research/caterloopillar. Read p21742,21782,21825,21826,21841,21888: preliminary sparks, close pairs, construction order, transient honeyfarm, phase/parity coverage8→16, deeper search memory limits and pragmatic prototype restrictions. Sources and shared attribution preserved, including PatternoftheYear2016. No invented personal breakthrough or generic-insertion replacement.

**3D viewer repair:** actual failure was stale Vite optimized Three dependency URLs returning HTTP504 “Outdated Optimize Dep”, not model geometry. Restarted local Astro devserver; `astro.config.mjs` now excludes `three` from optimizeDeps, so lazy imports resolve directly during development. `LifeTileExplorer.astro` assembly has the real existing assembly preview during loading/failure/release and a Retry3Dview button. Real WebGL assembly verified after final build, ready=true with1canvas; both live blue tile faces verified with2canvases. Spacing0/40/200, Top/Underside, camera drag, and close tested. No console errors. Model coordinates/geometry unchanged; rejected LifeAPI/tile animations remain reverted.

Final verification: `npm run verify` passes, 0errors/0warnings (one pre-existing hint),49HTMLpages,30canonicalarticles,2632internallinks/assets. New assertions ensure late inserters precede prototypes, all7clips/cover exist, rejected breakthrough heading absent, assembly fallback and retry present. Browser confirms all8GIFs load, no desktop overflow, still fallback, and animation restored to playing. Screenshots `.editorial-private/reviews/caterloopillar-late-inserters-cover.png`, `caterloopillar-backward-tight-insertion.png`, `tile-viewer-repaired.png`. No fresh mobile check. Everything remains LOCAL; no publication/push authorized.

## October 13: definitive thematic-homepage correction and Caterloopillar reader

**LATEST HOMEPAGE OVERRIDE:** the author clarified that the main homepage chapter must show INTEREST THEMES, not individual articles. Recent articles is fine below. This supersedes the earlier misinterpretation that moved the whole journal to the top. Final structure: original introduction/gun hero → six image-backed interest cards → Recent articles → About/contact. Removed the separate Selected work article grid so the main chapter stays thematic. Hero action points to #interests. All articles remains a direct header link to the lower journal. Topic images/headings open /interests/<id>/, never the representative article; only the explicitly named-example caption remains a direct article link, as previously requested.

All nine thematic pages now display their introductions openly, rather than behind a collapsed About button. Added per-interest `articleOrder`, validated against membership/duplicates. Life starts with Gemini origin and construction themes; article order begins Remini, Caterloopillar, gun, LifeAPI, CatForce, ping-pong. Physical tiles follow those, regardless of newer article date. CA stays separate with its five non-Life/neural subjects. Cryptography and Engineering pages expanded into linked thematic introductions; the other topic/subtopic introductions remain visible. Each page includes all matching canonical articles once and retains topic/sidebar/subtopic navigation.

The author’s screenshot specifically pointed out **missing spaces around About-page links** (originalGemini, wasSerizawa, builtGeminoid, comma-separated titles). Added explicit Astro space nodes; browser confirms the full paragraphs have normal spaces and punctuation. About now also links directly to both Life and CA thematic pages. Build assertions cover the exact previously broken phrases.

Read the author-supplied inspiration, Gabriel Nivasch’s Caterpillar article: https://www.gabrielnivasch.org/fun/life/caterpillar . Follow its useful progression from animated components to whole construction; do not conflate Caterpillar with Caterloopillar, copy its prose, or attribute its reactions to this author.

**Caterloopillar main cover now `caterloopillar-reading-head.gif` (800×660)**. The author requested an actual reading-head mechanism/ship integration/deletion animation. Found the original forward reader in Code/WSSStapler.py, downloaded source preserved in research/caterloopillar/source-code/Code-WSSStapler.py. Renderer scripts/render-caterloopillar-reader.py reads literal RLEs without executing original Python or loading pickles. Reassembles exact frontFrontPart, frontReflectingPart, frontBackPart, frontSL placements for distance250, d76. Initial138cells include a seven-cell LOAF tape symbol, not a four-cell block. It activates, emits a glider, reflects it between spaceships, rebuilds the loaf250cells forward, and emits one construction glider. Full isolated mechanism evolved in Golly, no finite cropped simulation.

192frames generations0–1440; stages/holds at activation, travel, reflection, rebuild. Top overview rotates90degrees; actual enlarged zoom uses original orientation and follows exact detected gliders. Reference markers label original Start and +250 position; only real native cells are drawn. Loaf rebuilt by1408 and remains at2048. At2048 ALL131 original spaceship-convoy cells match initial convoy translated(0,-1024), plus the moved7cell loaf and exactly5cells of one output glider. Native states0,256,768,1408,1440,2048 agree with independent sparse B3/S23 cell for cell. Source/hash/cameras/positions in research/caterloopillar/reading-head-animation-check.json. Article starts with a short stepwise mechanism explanation and keeps the credited dvgrn architecture schematic separately at /images/caterloopillar-architecture.png. The old basic2014 forward-reaction GIF remains in the development story; the old hybrid schematic cover is superseded.

LifeAPI code preview, original exploded tile cover/viewers, and real printed-tile photographs remain as restored; do not reintroduce rejected animations.

Verification: npm run verify passes, zero Astro diagnostics;49HTML pages,30canonical articles,2623internal links/assets. Assertions cover themes before journal, visible thematic intros, Remini/Caterloopillar-first Life reading order, correct category membership, link spacing, every matching canonical article, and visual ownership/fallbacks. Python renderer compiles. Browser confirms all six topic image destinations, a real click into the Life thematic introduction, first four Remini/Caterloopillar/gun/LifeAPI, repaired About paragraphs, native readerGIF800×660 loaded, and no desktop overflow. Screenshots: .editorial-private/reviews/homepage-themes-first.png, life-theme-introduction.png, caterloopillar-reading-head.png, about-link-spacing.png. No fresh mobile check or publication.

## October 13: article-first navigation, classification, and native Life animations

Latest author requests supersede earlier grouping: **all B3/S23 discoveries and physical Life projects belong to Conway’s Game of Life**. CA Research now has exactly five published entries: Serizawa Geminoid, Geminoid Particles, neural CA, Serizawa quadratic growth, and the Live Free or Die c/3 spaceship. Life has sixteen. B60, BNE14T30, BRx46B, Ocellus, Simkin’s p60, 24/25-cell growth, ping-pong, both tile articles, and MMG moved from CA to Life. Engineering/computing cross-listing is preserved.

**All articles is the first section after the original introduction/gun hero**, ahead of topic images and Selected work. The main navigation and hero action link directly to it. Topic image/title links now open filtered topic collections; the explicit named-example caption still opens its individual article. Topic collections show matching articles once, parent/subtopic breadcrumbs, and a topic sidebar. Article sidebars contain Topics plus On this page. Homepage journal and Research/Projects collections also have topic navigation. Geometry is under Mathematical papers; programming and simulation are under engineering.

New native Golly covers: B60 (0–60), BNE14T30 (0–144), BRx46B (0–46), Ocellus (0–114), Simkin’s p60 (0–60), 24/25-cell growth (4194304–16777216). Original RLEs extracted from LifeWiki’s embedded original source or actual downloadable RLE; provenance in research/ca-visuals/lifewiki-pattern-sources.json. Five small endpoints agree exactly with independent sparse B3/S23. Ocellus and p60 return to the complete original state. Seed populations 24/25 and exact generation64 states independently checked. Full final populations 54564537 and 91253066; growth square side16384, fixed view, no finite simulation boundary. scripts/render-life-results.py and *validation.json record this.

Caterloopillar’s main new cover `life-caterloopillar.gif` pairs the credited LifeWiki architecture schematic (dvgrn, GFDL1.2) with the original November2014 forward-glider reaction evolved through140 generations. It is **not a whole-spaceship evolution clip**. Rebuild with scripts/render-ca-gallery.py caterloopillar then scripts/render-caterloopillar-cover.py. Full original c/8 also simulated through2000 and exact238189-cell translation(0,-250) rechecked. Experimental two-end crops proved too sparse; their renderer is separate and not used as the cover.

**LATEST VISUAL OVERRIDE:** the author rejected the new LifeAPI glider/column animation and tile animations, saying he liked the earlier versions. Restored LifeAPI’s static syntax-highlighted code image, the original exploded 3D tile cover and interactive viewers, and physical still-life photographs. Removed new animation explanations from those articles. These are explicit exceptions to the earlier blanket animation request. Do not reintroduce them. Rejected local experiments are archived under .editorial-private/rejected/lifeapi-and-tiles-animations, outside published assets. All other CA/Life results retain animations and pause fallbacks.

Verification after restoration: npm run verify passes, zero Astro diagnostics;49HTML pages,30canonical articles,2611internal links/assets. Verifier checks article-first order, correct Life membership, matching topic/subtopic collections, sidebar selection, canonical topic-image routing, article Topics+TOC, and animations with the author’s three explicit visual exceptions. Browser confirmed CA’s five GIF covers, restored LifeAPI image/body, geometry’s single hull article, article Topics+TOC, and no desktop overflow. No new mobile viewport verification or publication.

## Latest Geminoid visual corrections: October 13, 2026

The author rejected the 0–480 Serizawa circuit clip and asked for BOTH arms constructing complete heads, the other/lower end, the instruction tape, snake-like overall movement, and push/pull/shoot. Same treatment required for Geminoid Particles. Main covers now `serizawa-geminoid-whole.gif` and `geminoid-particles-whole.gif`: synchronized upper/lower end panels plus whole tape overview. End panels preserve geometry through rotation; tape overview explicitly compresses height, using exact occupied pixels and enlarged cells. Original full patterns evolved with Golly RuleLoader, not fabricated circuits or cropped finite simulations. Runs: Serizawa 0–25165824, Particles 0–49152. Each first-end close-up survives only as collapsed optional detail (`*-building.gif`).

Verified original lower-head offsets: Serizawa (1716,3338237), Particles (75,9002). New-head offsets: Serizawa (2444,-3219), Particles (148,-112). Exact head-circuitry matches at BOTH ends: Serizawa 755 fixed cells completed at 13107200 / 19660800; excludes startup targets/transient signals by comparing the operating original head. Particles 80 fixed-object cells completed at 18048 / 26880. Completion means head circuitry; tapes and moving targets are separate. Whole-plane canonical macrocell digests at generations 8388608 and25165824 agree between independent Serizawa runs; report `research/ca-visuals/geminoid-whole-validation.json`.

Renderer `scripts/render-geminoid-whole.py`; reports `research/ca-visuals/*-whole-check.json`. Serizawa arm targets verified as actual isolated state1 cells: initially (516,173)/(2154,878); at4194304 (516,-2975)/(4099,878); at8388608 (516,-2352)/(3514,878). They move on perpendicular axes. Amber ring markers select actual cells on those axes, and must not manufacture a predicted position if absent. Particles state7 movable targets enlarged blue. Render scripts use bgolly/Pillow, temp caches regenerate, all source patterns under research/ca-visuals. Everything remains local; no publication authorized.

## Latest overrides: full ping-pong and hull manuscript, October 13, 2026

- The author rejected the single-collision cover. The main ping-pong image is now `switch-engine-ping-pong-cycle.gif`, an entire actual exchange plus the next ping, generations 4685824–7012480. Both streams remain visible; 45-degree rotation, camera pans only along them. Exact detected signals get magnified amber markers. Coarse squares represent occupied 512-by-512-cell regions. Script `render-ping-pong-cycle.py`, report `cycle-animation-check.json`. 73 frames, 800x600, stage captions/holds. Collision is a collapsed optional detail; redundant crossings view removed from body. Growth fan remains secondary.
- Read `/home/simsim314/Downloads/read_only_convex_hull_batched_bridges_v7.tex` and its PDF. The hull article now describes this October2026 unpublished manuscript, replacing the earlier single n log^3 h claim with its two distinct bounds: sequential O(n log h log n D), shuffled-prefix replay O(n log^2 h D), D=min(h,log n), both O(h) words. Replay storage/shuffle costs external. General-position/exact-predicate assumptions, no optimality claim; prime-cycle generator is heuristic and does not prove uniform-service theorem.
- Author recalls methodology around2009, uncertain exact date. Interview: hard to recall; noticed n log h algorithms behave differently on read-only tape, then investigated actual memory/reading regimes and tried to prove something using bridges. Do not invent a more specific breakthrough.
- Figure1 page5 extracted as hull cover; all30 articles now have previews. Raw TeX/PDF remain outside repository. Everything remains local and unpublished.

## Latest visual and article corrections: October 13, 2026

This section supersedes the older animation and ordering descriptions below.

- Main mathematics heading is **Mathematical papers**, with the simple description “Work in mathematics and computational geometry.” Preserve honest article statuses and AI-related research history.
- Caterloopillar and LifeAPI lead Selected work; Remini, ping-pong, sphere packing, and illustrated CA stories are promoted in the journal. The 24/25-cell historical seeds are last. The gun hero is preserved.
- No article should appear a third time on the homepage. Main-topic representatives are omitted from Selected work, while remaining in the complete journal. Nested data-article-id attributes belonging to one hero are one appearance. The build verifier checks this limit.
- **29 of 30 articles have visual previews.** The unpublished hull research note remains text-only. Remini, Serizawa Geminoid, GeminoidParticles, Serizawa quadratic growth, and the B2/S0 c/3 spaceship now have real Golly animations, not invented CA art.
- Remini shows activation of the first unit’s still-life seeds into p30 circuitry at generations 0–2400. Its source crop includes a 2400-cell causal margin, and the displayed generation 2048 matches a full original-pattern run. Script: scripts/render-ca-gallery.py; source and reports in research/remini/ and research/ca-visuals/.
- The author rejected an early Serizawa growth clip. The current four-cell seed clip runs generations **262144–1048576**, showing the later triangular growth, at 2048 cells per pixel. Use the correct Serizawa rule from GollyGang’s official rule-table repository.
- Ping-pong now has three distinct views in its article: (1) the **cell-scale collision cover**, 15 image pixels per cell, generations 5454680–5455312, captions ABOVE the cells and deliberate holds at the approaching ship / collision / returning glider stages; (2) a slower moving overview of the exchange, generations 4456448–8126464, with exact detected signal markers and a cell inset; (3) the older 33–67 million generation growth fan as a secondary view. Scripts: render-ping-pong-collision.py, render-ping-pong-crossings.py, render-switch-engine-ping-pong.py. Each GIF has a motion fallback.
- The collision starts at generation 5454713 (last isolated MWSS at 5454712). Its close-up uses an exact source crop with a 2048-cell causal margin; the complete final search region matches a full-pattern Golly run. Camera follows an actual detected NW glider after the collision. Source records are in research/switch-engine-ping-pong/.
- The author remembers multiplication of large primes when calculating the **distance between the streams**, not the overall period. We factored the LifeWiki period as 384×73×83, but that DOES NOT establish the distance calculation. He is unsure whether they are related. The article deliberately states carefully tuned distances without claiming an unverified prime formula. A focused filename search in public LifeAPI, cuLifeAPI, and GreyGooTheory trees did not locate a generator; do not pretend one was found.
- LifeWiki’s current quadratic-growth history verifies the 23-cell record lasted from **October 29, 2014 to March 12, 2022** (more than seven years). 22-cell: dani/David Raucci March12; 21-cell: dani March15; 20-cell: dani April4,2022, still listed as current. The article credits the new discoveries and describes the record as historical.
- The Caterloopillar article has been rewritten around the research process. All eight pages of early thread t1448 were archived/read (some long late replies were excerpted); first page of completed construction thread t2151 read in full. Sources: research/caterloopillar/development-\*.json and construction-0.json. Key story: Nigin’s Nov12,2014 proposal; the author objected, tried to prove it wrong, then found the Nov14 forward reaction; slow edge-shooter searches and incomplete kits; two-week depth-eight search; Glue++/LifeAPI memory and speed improvements; timing debates with Chris Cain, Dave Greene, and codeholic; completion April9,2016. Do not attribute codeholic’s Escher comparison solely to the author.
- Caterloopillars won **Pattern of the Year 2016**, 49 stars, official results p44028 announced June3,2017. This is in the article and its preview description. The Nov14 basic forward-glider reaction has an additional real Golly GIF in the article.
- Downloaded the original Caterloopillar_c8.rle and verified ALL 238189 generation-zero live cells translate 250 cells upward after 2000 generations. Population is that supplied phase, not the LifeWiki minimum 232815. Source/hash/result in research/caterloopillar/validation.json.
- B2/S0 ship: all exact states agree with an independent sparse implementation at generations 0,1,6,60; period6 translates (-2,0). RuleLoader macrocell state/coordinate decoding for the Serizawa/GeminoidParticles generation-zero crops agrees with original multistate RLE. Reports in research/ca-visuals/validation.json.
- A restart killed background jobs and cleared /tmp caches; completed repo assets survived. Dev server was restarted on port4321. Renderers regenerate their own caches as needed. Source archive extraction folder research/ca-visuals/Serizawa1.1 contains unused reference files; only its Serizawa.rule is needed by the renderers.
- Final npm run verify passes: zero Astro diagnostics, 49 HTML pages, 30 canonical articles, 2320 internal links/assets; homepage maximum-two-appearances assertion passes. Python scripts compile. The fresh mobile viewport override did not apply after restart (desktop browser had no document overflow); avoid claiming a new mobile breakpoint check. Screenshot: .editorial-private/reviews/ping-pong-closeup.png.
- Everything remains local. “I might publish” was not deployment authorization. No upload, push, or deployment.

Final verification: zero Astro diagnostics; 49 HTML pages, 30 canonical articles, 2320 internal links/assets; maximum two distinct homepage appearances passes. Python render scripts compile. After restart the mobile viewport override did not apply, so only fresh desktop/no-overflow and image-pause checks are confirmed. Screenshot: `.editorial-private/reviews/ping-pong-closeup.png`.

## Latest topic corrections and Golly animation: October 13, 2026

These corrections supersede the six-topic grouping described immediately below.
The **six main topics** are now **Papers, CA Research, Conway’s Game of Life,
Cryptography & Implementation, Chess, Engineering & Computing**. There are
**nine topic sources/routes**: six main interests and three nested interests
(geometry under Papers; simulation and programming under engineering).
Conway’s Life no longer inherits CA Research. Existing major Life articles
remain in its focused collection; broader CA discoveries and Neural CA remain
in CA Research.

The standalone AI category has been removed. Its former source is archived at
`docs/historical-interests/artificial-intelligence.md`, and its old route
redirects to CA Research. Neural CA’s topic is CA Research. Deep-Formix remains
under Chess/Computing with an explicit artificial-intelligence tag and its
existing AI narrative. Sphere packing belongs to Papers, retaining its
AI-assisted-mathematics tag. Geometry is a mathematical branch, not a main
category. Papers includes a preprint and unpublished mathematical notes;
do not imply peer-reviewed publication of every entry.

The author values **switch-engine ping-pong over the 24/25-cell growth seeds**.
It is featured, with `presentationOrder: -9`, ahead of the seeds. He suggests
a long-running, zoomed Golly animation. Its new local cover is an actual
Golly 3.3 HashLife run of the original 23-cell seed, sampled at generations
**33,554,432–67,108,864**, with a fixed view of the growing fan. The full plane
is simulated; the displayed crop is not a finite simulation boundary. A
bright pixel aggregates a **32,768 × 32,768-cell** square containing live cells.
The full final population is **124,270,961**. The final state is the motion
fallback. This is sampled playback, not one frame per generation.

Renderer: `scripts/render-switch-engine-ping-pong.py`, using the installed
`bgolly` CLI and Pillow. Seed and exact generation/population/provenance report:
`research/switch-engine-ping-pong/`. Generation 64 was compared cell-for-cell
with an independent sparse B3/S23 update (163 live cells). New assets:
`public/images/switch-engine-ping-pong-growth.gif`, its `-still.png`, and the
original seed diagram shown in the article. The original gun hero stays.
All new images remain local review material; no website upload is authorized.

## Latest continuation: October 13, 2026

The author requests **fewer topics and much more imagery**, selecting relevant
images from each subject, and more interviews. This supersedes the earlier
text-only topic/category/related cards. The site now shows **six main topics**:
Mathematics & Geometry, Cellular Automata, Artificial Intelligence, Cryptography
& Implementation, Chess, and Engineering & Computing. The other four topic
routes remain as nested interests (geometry under mathematics; Life under CA;
simulation and programming under engineering). Article inheritance, filters,
footer links, and category coverage follow these parents. Articles still exist
once.

Each main topic features an image of a **named article from that topic**, with
its image linking to that article. This retains article ownership while making
topics visual. Category, related, and journal cards now show covers where
available; the journal is a responsive image grid. The original gun hero stays.

Added eight distinct LifeWiki source diagrams, a source-derived Remini
constructor detail, and three original 2016 tile-printing photographs. Ten
previously text-only articles now have covers. Credits and provenance are in
`docs/asset-sources.json`; these new images are for **local review**, with
publication approval pending. The printing photos are from post **31711**,
which corrects the earlier source pointer to 31727 (a colour discussion).

Both pages of Remini thread 3836 were read before the interview. The author
explains that Remini demonstrates the progress in understanding since Conway’s
early construction: retro circuitry can support new self-construction. The
turning point was realizing p30 streams could implement universal **push, pull,
and shoot** commands; after that, everything else was straightforward to him.
The article includes these answers, specific forum links, and the distinction
between the puffer and a cleaned-up spaceship. The historical comparison is
Winning Ways (confirmed in post 75028).

`research/remini/Remini.mc` is the original public pattern, kept with its
original assembly script. `scripts/render-remini-detail.py` decodes the
macrocell and renders a constructor crop at generation zero. Its report
checks population **779,984**, stores source SHA-256 and exact crop coordinates.
This cover is a detail, not the whole tape or an independently evolved demo.

The next interview question, after reading Mandelbrot CUDA’s README, asks what
prompted the author to build his own deep-zoom explorer. Check later messages
for his answer. Website upload permission is still withheld.

## 1. Ready-to-paste prompt for a new chat

Copy this into a new chat opened in the existing Homepage workspace:

```text
Continue working on my personal research website in
/home/simsim314/GitHub/Homepage.

Read CONTINUE-HERE.md completely, then README.md, docs/editorial-guide.md,
docs/verification.md, and the files relevant to my next request. The handoff
contains my decisions and corrections from the earlier conversation.

Continue the existing local implementation. Preserve the uncommitted work.
Do not restart the website, create another content system, or undo decisions
in the handoff. The homepage is the blog. Articles exist once and categories
are ways of exploring that same collection.

Do not upload, push, deploy, publish the website, or change GitHub Pages
settings without my explicit permission. I withheld permission to upload.
Do not modify other repositories or include Spirtuality. Thingiverse is a
separate request with its own incomplete publication prerequisites.

Use my confirmed biography and interview answers. Do not invent motivations,
research results, conversations, credentials, project maturity, or personal
claims. Ask me focused questions yourself when more personal context is
needed; do not make me choose which projects to discuss.

Keep the original clickable Simkin Glider Gun homepage hero and its article
animation. One image may appear in previews and the page of the SAME article,
but must never represent a different article or interest. New images need
my approval before publication.

For the Life-in-3D article, keep one rotatable representative per colour/set,
not a viewer for every variant. Each representative must keep BOTH top and
underside visible and independently rotatable after 3D loads. Keep the compact
whole-set images, input/output schematics, all-case explanation panels, and
full assembly viewer. Assembly spacing is 0–200 mm, starting at 40 mm.

Inspect the existing code and evidence before making claims. Use Python for
exact tile schematics/model generation. Do not substitute generated artwork
for actual geometry or conceal boundary problems by shifting ordinary tiles.

Work on my next request, run relevant checks, and show the local result.
My next request is: [WRITE THE NEXT CHANGE HERE]
```

If there is no new change specified, first report the current state briefly and identify a concrete next step. Do not treat this handoff as permission to deploy or start an unrelated redesign.

## 2. Non-negotiable decisions and authorization

1. **Local work is authorized. Website upload is not.** The user explicitly said, “you should not upload the website without my permission.” This supersedes the initial deployment request. No website upload or deployment was performed in the work recorded here. Do not push, use an upload connector, create a public PR containing this work, trigger deployment, or enable Pages without permission.
2. Use the existing `simsim314/Homepage` repository. Target URL, once approved, is `https://simsim314.github.io/Homepage/`. Do not create a repository named `simsim314.github.io` based on the old specification.
3. Do not modify any other existing project repositories. Review their public documentation read-only. Keep `Spirtuality` entirely separate.
4. The homepage and blog are the same. No separate Blog navigation or blog home.
5. Use a single Markdown/MDX article collection. Mathematical results, Life discoveries, software, experiments, and substantial topics all use it. Multiple categories must not duplicate articles or URLs.
6. The homepage automatically shows interests, featured work, and recent articles from metadata. Each interest has an introduction and related articles. Research/Projects are filtered indexes of the same collection.
7. Preserve and build on the existing dirty working tree. Many modifications and untracked research/generated assets are intentional. Never reset, clean, or overwrite them to start over.
8. Get personal claims and motivations from the user. Public repositories and forums establish technical facts, not how he felt or why he made a choice.
9. Label experimental work, candidate results, unpublished notes, and preprints accurately. Do not describe simulation as printed hardware or a tested/deployed product.
10. New content images require user approval before publication. The user has approved several existing images; do not ask for that approval again unnecessarily.
11. Keep all calculations and tile geometry honest. A visually plausible placement is not evidence of full connector fit.
12. Do not introduce mechanical gates. The agreed tile convention requires a completed prior layer, supplied compatible inputs, and no bridging over missing internal pieces.
13. Interviews: choose a project yourself and ask one focused open question at a time. Do not make the user select projects or repeat information already supplied. Keep technical work moving while awaiting optional answers.
14. No separate research-methodology article merely because AI or a workflow was used; discuss methodology within the relevant actual work.

## 3. Current site and author presentation

### Public wording confirmed by the user

- Name: **Michael Simkin**.
- Header/profession: **Independent researcher**.
- Location: **Tbilisi, Georgia**.
- “Self-taught” belongs in the biography, not the public title or homepage header.
- Research is both professional work and a hobby; his focus changes over time.
- Career direction: computational geometry, then computer vision and AI research; more recently freelance work with several startups on medical research.
- Main Conway’s Life research phase: **2014–2019**, alongside other work.
- Bronze medal representing **Israel at the 1999 International Mathematical Olympiad**; subsequently worked in several startups on different ideas.
- Recent interest: AI-assisted mathematical proofs.
- Interests include computational geometry, cellular automata, AI-assisted mathematical proofs, cryptography implementation, programming, simulation, experimental engineering, and chess.
- Chess is a hobby. Lichess handle: `simsim314`.
- Public contact email: **simsim314@gmail.com**.
- No public arXiv profile URL has been supplied. Link a verified paper directly; do not invent a profile.
- Homepage phrase: **“Engaging curiosity. Making ideas work.”** The intended emphasis includes experimentation, engineering, building infrastructure, and obtaining results, not curiosity alone.

Do not infer employers, degrees, university affiliation, specific medical specialties, dates of employment, or professional certifications.

### Design and navigation

- Modern personal research journal, clear typography, readable equations, responsive layouts, fast loading, accessible controls.
- Avoid generic corporate portfolio language, excessive animation, and complex navigation.
- Navigation: Home, Interests, Research, Projects, About, plus search.
- The original **Simkin Glider Gun** is the homepage lead exhibit. Do not replace it with Deep-Formix or tile research just because those were edited recently.
- The gun hero is clickable and links to its own article; it uses the approved custom pointer styling.
- The gun article must show the gun animation/simulation, with play/pause, step, reset, and speed control.
- Current cards use article images, including a named representative article within each main topic. See the latest continuation above; the earlier typographic-only decision is superseded.
- Same article cover/simulation may appear on its homepage preview and its own article.
- Museum is a stub and excluded from publication as a draft.
- Remini is important and featured; the Conway’s Life landing page introduces it prominently.
- Chess category starts with chess as a hobby and Lichess, then Deep-Formix, then Chess960×960 with its evaluator. Chess960×960 is lower priority and placed last among same-date articles.

## 4. Content architecture and page inventory

The current source has **31 article files: 30 published locally and one museum draft**, and **10 interest pages**. “Published locally” means included in the built local website, not proof that the remote Pages site contains this work.

### Main routes

Every route below is under `/Homepage/`:

| Route                | Function                                                        | Source                             |
| -------------------- | --------------------------------------------------------------- | ---------------------------------- |
| `/`                  | Homepage/journal, hero, interests, featured and recent articles | `src/pages/index.astro`            |
| `/interests/`        | All interest categories                                         | `src/pages/interests/index.astro`  |
| `/interests/<id>/`   | Category introduction and related articles                      | `src/pages/interests/[id].astro`   |
| `/research/`         | Research articles from shared collection                        | `src/pages/research.astro`         |
| `/projects/`         | Project articles from shared collection                         | `src/pages/projects.astro`         |
| `/articles/<slug>/`  | One canonical page per non-draft article                        | `src/pages/articles/[...id].astro` |
| `/about/`            | Confirmed biography and email contact                           | `src/pages/about.astro`            |
| `/search/`           | Client-side search                                              | `src/pages/search.astro`           |
| `/search-index.json` | Generated article search data                                   | `src/pages/search-index.json.ts`   |
| `/sitemap.xml`       | Generated canonical page sitemap                                | `src/pages/sitemap.xml.ts`         |
| `/visual-review/`    | Links to article visual previews for review                     | `src/pages/visual-review.astro`    |
| `/404.html`          | Error page                                                      | `src/pages/404.astro`              |

There is a redirect from the superseded `other-cellular-automata` interest to `cellular-automata`.

### Interest IDs

| ID                         | Display title                   | Relationship                 |
| -------------------------- | ------------------------------- | ---------------------------- |
| `mathematics`              | AI-assisted Mathematical Proofs | Standalone                   |
| `computational-geometry`   | Computational Geometry          | Standalone                   |
| `cellular-automata`        | CA Research                     | Broad CA parent              |
| `game-of-life`             | Conway’s Game of Life           | Child of CA Research         |
| `artificial-intelligence`  | Artificial Intelligence         | Standalone                   |
| `cryptography`             | Cryptography & Implementation   | Standalone                   |
| `chess`                    | Chess                           | Standalone                   |
| `simulation-visualization` | Simulation & Visualization      | Standalone                   |
| `experimental-engineering` | Experimental Engineering        | Standalone                   |
| `programming-computing`    | Programming & Computing         | Explicitly approved addition |

Small CA discoveries belong to CA Research. The Life child concentrates on major constructions and infrastructure. Parent inheritance makes major Life articles discoverable from CA Research without duplicating content.

### Article inventory

Each slug maps to `src/content/articles/<slug>.md` or `.mdx` and `/Homepage/articles/<slug>/`. The museum draft has no published route.

| Slug                              | Title                                    | Status       | Direct topics                                                         | Visibility        |
| --------------------------------- | ---------------------------------------- | ------------ | --------------------------------------------------------------------- | ----------------- |
| `24-cell-quadratic-growth`        | 24-cell quadratic growth                 | demonstrated | cellular-automata                                                     | Published locally |
| `25-cell-quadratic-growth`        | 25-cell quadratic growth                 | demonstrated | cellular-automata                                                     | Published locally |
| `b60`                             | B60                                      | demonstrated | cellular-automata                                                     | Published locally |
| `bne14t30`                        | BNE14T30                                 | demonstrated | cellular-automata                                                     | Published locally |
| `brx46b`                          | BRx46B                                   | demonstrated | cellular-automata                                                     | Published locally |
| `caterloopilar`                   | Caterloopillar                           | demonstrated | game-of-life                                                          | Published locally |
| `catforce`                        | CatForce                                 | implemented  | game-of-life, programming-computing                                   | Published locally |
| `cgol-virtual-museum`             | CGOL Virtual Museum                      | ongoing      | game-of-life, simulation-visualization                                | Draft; excluded   |
| `chess960x960`                    | Chess960x960                             | implemented  | chess                                                                 | Published locally |
| `cryptocash`                      | CryptoCash                               | experimental | cryptography                                                          | Published locally |
| `cryptohanko`                     | CryptoHanko                              | experimental | cryptography                                                          | Published locally |
| `deep-formix`                     | Deep-Formix                              | implemented  | chess, artificial-intelligence, programming-computing                 | Published locally |
| `geminoid-particles`              | Geminoid Particles                       | demonstrated | cellular-automata, programming-computing                              | Published locally |
| `high-dimensional-sphere-packing` | High-Dimensional Sphere Packing          | preprint     | mathematics, artificial-intelligence                                  | Published locally |
| `life-in-3d-tiles`                | Conway’s Life in 3D Tiles                | experimental | cellular-automata, experimental-engineering                           | Published locally |
| `lifeapi`                         | LifeAPI                                  | implemented  | game-of-life, programming-computing                                   | Published locally |
| `live-free-or-die-c3-spaceship`   | The c/3 spaceship in Live Free or Die    | demonstrated | cellular-automata                                                     | Published locally |
| `mandelbrot-cuda`                 | Mandelbrot CUDA                          | implemented  | simulation-visualization, programming-computing                       | Published locally |
| `multilayer-mutilated-gear`       | Multilayer Mutilated Gear                | experimental | cellular-automata, simulation-visualization, experimental-engineering | Published locally |
| `neural-ca-mnist`                 | Neural CA MNIST                          | experimental | artificial-intelligence, cellular-automata                            | Published locally |
| `ocellus`                         | Ocellus                                  | demonstrated | cellular-automata                                                     | Published locally |
| `qr-wifi-scanner`                 | QR Wi-Fi Scanner                         | implemented  | experimental-engineering                                              | Published locally |
| `read-only-convex-hull`           | Convex hulls with limited working memory | note         | computational-geometry, programming-computing                         | Published locally |
| `remini`                          | Remini                                   | demonstrated | game-of-life                                                          | Published locally |
| `serizawa-geminoid`               | Serizawa Geminoid                        | demonstrated | cellular-automata                                                     | Published locally |
| `serizawa-quadratic-growth`       | Serizawa quadratic growth                | demonstrated | cellular-automata                                                     | Published locally |
| `simkin-glider-gun`               | Simkin Glider Gun                        | demonstrated | game-of-life                                                          | Published locally |
| `simkins-p60`                     | Simkin's p60                             | demonstrated | cellular-automata                                                     | Published locally |
| `still-life-tiles`                | Making Still-Life Tiles Physical         | demonstrated | cellular-automata, experimental-engineering                           | Published locally |
| `switch-engine-ping-pong`         | Switch engine ping-pong                  | demonstrated | cellular-automata                                                     | Published locally |
| `tqrng-webcam`                    | TQRNG Webcam                             | experimental | experimental-engineering                                              | Published locally |

### Adding content

- Article source: `src/content/articles/`.
- Interest source: `src/content/interests/`.
- Schema: `src/content.config.ts`.
- Shared collection/routing/related logic: `src/lib/content.ts`.
- Confirmed author details: `src/lib/site.ts`.
- Template: `docs/article-template.md`.
- `type`: `research` or `project`.
- `status`: `demonstrated`, `implemented`, `experimental`, `candidate`, `ongoing`, `preprint`, or `note`.
- Required metadata: title, description, type, topics, status, date, sources.
- Useful optional metadata: tags, featured, homepageHero, showPreview, presentationOrder, updated, draft, github, demo, demoNote, image, imageAlt, imageCredit, imageSource.
- Only one article may have `homepageHero: true`.
- Topics must exist, must not repeat, and parent relationships cannot cycle.
- Draft articles are excluded from routes, indexes, search, sitemap, and related listings.
- Article dates indicate the date this site’s text was prepared/published. Historical discovery dates belong in the body with sources. Do not change dates merely to promote content.
- New articles have no image preview unless configured. Image ownership is enforced by the built-site verifier.

## 5. Interview evidence and technical cautions

Use these as confirmed recollections, not invented quotations. Existing articles and `docs/editorial-guide.md` contain fuller wording.

### Simkin Glider Gun, LifeAPI, CatForce

Michael wanted a simple combinatorial search because older search tools seemed complex and might contain bugs. He built LifeAPI and CatForce as infrastructure before searching. Three blocks were particularly suitable for a small combinatorial search.

He published the catalytic interaction/half-gun and continued sharing outputs. Scorbie recognized the completed gun. Michael believes the difficult interaction discovery deserves his attribution, recognizes a genuine dilemma about Scorbie’s credit, and leaves community naming decisions to the community. Present his recollection separately from source-based attribution; do not turn this into an accusation about motives.

The gun is described as the **smallest known by live-cell population when two glider output streams are allowed**, using the 29-cell pattern. Preserve the qualification. Reverify current record claims if changing them.

LifeAPI is optimized C code for a **64×64** grid. Boolean operations encode the Life rule. The emphasis is a small, simple, fast engine for search utilities testing many possibilities, rather than large-grid support. Do not misinterpret “heavy” as an allegation about other programs’ code quality.

CatForce returns potentially useful interactions. Michael inspects them manually and selects useful results. Do not imply automatic usefulness ranking. p19 Cribbage was Riley’s discovery using a symmetric/custom CatForce version; distinguish a tool contribution from claiming the discovery.

Version-specific boundary caution: CatForce’s bundled 2014 LifeAPI uses wrapped column indices and circular bit shifts. Do not automatically apply that boundary behavior to later standalone LifeAPI code.

### Caterloopillar, Remini, CA discoveries

Caterloopillar is a complex mutual-construction mechanism; Michael referred to Escher’s hands drawing one another and directed us to the full forum thread. Read the actual construction before explaining its speed mechanism. Keep the canonical article slug `caterloopilar` even though display spelling is Caterloopillar.

Remini is an important finding: modern single-channel self-construction from classic period-30 circuitry. Personal motivation still needs an interview. Do not invent it.

`docs/life-discovery-coverage.json` tracks the 11 discoveries on the reviewed LifeWiki profile. This does not prove all forum contributions have been covered. Preserve shared credits: Tanner Jacobi for BNE14T30; Noam Elkies for Ocellus; source-based attributions for the other constructions.

Serizawa: Michael recalls the first Geminoid and a five-cell quadratic-growth seed. Forum records distinguish a self-constructing puffer from a self-cleaning Geminoid spaceship. Source-backed articles cover the March 23, 2014 announcement, the June 3 five-cell seed, and the June 4 four-cell example.

The elusive spaceship was identified as the **first c/3, period-six ship in Live Free or Die (B2/S0)**, posted October 5, 2014. The user remembered $50 and a claim that it was invested in Bitcoin in his name. Public records instead include a $25 new-speed bounty and his later post saying $25 was won. **Exact amount and Bitcoin custody/payment remain unresolved.** The article acknowledges the prize without publishing those uncertain details as fact.

Geminoid Particles has a dedicated source-backed article. Never evolve patterns from other rules under Conway’s B3/S23 simply to reuse the Life animation.

### Deep-Formix and chess

Deep-Formix started as a stress test of Gemini, considered the best model at that time by Michael. There were many bugs, but he obtained a working depth-four full-rules GPU chess search.

Its substantial contribution includes integrating GPU Perft and Chess-Engine-GPU and adding a custom evaluator. Michael emphasizes the evaluator most: a long sequence of 32×32 fully connected layers, relatively cheap per layer but expressive enough for complex position decisions, with potential for NNUE-style optimization. Do not claim it equals full-strength Stockfish or imply a verified tournament strength.

Do not claim an independent reproduction of all benchmark conditions unless actually performed. Keep repository-reported performance identified as such.

### Sphere packing

Michael was attracted to a simple-to-explain problem with difficult mathematics. He first tried low-dimensional kissing problems, found he could not easily improve known results, and wanted a pure mathematical result instead of merely numerical optimization. He moved toward large dimensions.

He directed AI toward combining Boaz Klartag’s stochastic ellipsoid approach with Abuya–Gargava–Zhao (AGZ), whose logarithmic gain held in sparse dimensions. His description is that AI did the mathematical heavy lifting while he supervised its focus.

After AI produced a proposed proof, he sought independent validation because his mathematical skills were below those required to judge the paper. Nihar Gargava helped validate and guide Matthias Gröbner’s reworking into a form accessible to human mathematicians.

Current article links **A cyclotomic gluing construction for lattice sphere packings**, Nihar Gargava, Matthias Gröbner, Michael Simkin, posted October 8, 2026: `https://arxiv.org/abs/2610.12619`. Michael confirmed it is his paper. The article distinguishes the earlier AI-assisted argument from the stronger collaborative result.

The recorded preprint bound is, for all sufficiently large integer dimensions:

```text
Delta_d^L >= c d^2 log(log d) 2^(-d)
```

Status is **preprint**, not merely an unpublished commitment and not a claim of peer-reviewed acceptance. Gargava’s title was verified as postdoctoral researcher at Université Paris-Saclay; reverify if updating a time-sensitive title. Cryptographic proof commitments identify earlier manuscript versions; they do not validate a theorem.

### Convex hull

User supplied unpublished documents:

- `/home/simsim314/Downloads/ConvexHull.doc`
- `/home/simsim314/Downloads/Kirkpatrick-Seidel.pdf`

The article describes a planar hull from read-only input, bridge finding, active regions/strips, and repeated scans. The manuscript states `O(h)` allocation and expected `O(n (log h)^3)` time, where `h` is hull size (called `k` in the interview). These are manuscript claims, not established current novelty or a reproduced implementation.

The user asked whether to put it on arXiv. Publication readiness and novelty review remain a possible follow-up; an arXiv account alone is not evidence of correctness/novelty. Do not submit or upload these raw documents. The raw documents were kept outside the repository.

### Cryptography

CryptoHanko: a phone-based digital hanko, with a key associated with a person, potentially by central registration, then signing with a QR output. Registration was not properly worked out; Michael did not use it beyond testing. Keep experimental status.

CryptoCash: cryptocurrency represented by a physical token, with a “real money feel” and an independent physical representation of value. It still uses a phone/app; Michael is uncertain how best to explain the appeal. Do not invent an established payment system or claim a physical NFC deployment that has not been confirmed.

Ask further questions about actual NFC tests, threat model, intended transfer/verification flow, and implemented versus proposed protocol when relevant. Distinguish signature experiments, witness calculations, and full deployed cryptographic systems.

### MMG and physical computation

Multilayer Mutilated Gear was inspired by Paul Callahan’s still-life tiling constraints and interest in a physical Life mechanism. Physical computation and self-replication recur in Michael’s CA work, but MMG does not establish a physically self-replicating machine.

Keep the original moving repository/forum GIF. A simulation is not a tested mechanical prototype.

### Other project content

- Mandelbrot preview was approved. Ask about precision implementation when expanding its story.
- Neural CA shows actual ONNX evolution outputs, not invented generated digit frames. Input is a synthetic hand-drawn 3 on 28×28. Hold the input longer, then advance the evolution faster. Provenance/model hash is in `docs/neural-ca-example.json`.
- TQRNG’s approved photon-arrival schematic is explanatory. Do not imply it establishes certified quantum entropy or complete randomness validation.
- QR Wi-Fi uses the original utility image; approved.
- CGOL Virtual Museum remains a draft stub, not a polished museum.

## 6. Visual policy and approved assets

Each content visual belongs to exactly one article. Reuse in that article’s homepage card, hero, or own page is permitted. Different articles/topics must not reuse it, even under renamed files with identical contents. The build verifier checks ownership and duplicates.

Approved existing visual directions:

- Exact animated Simkin gun, slow enough to follow, with playback controls.
- Caterloopillar’s LifeWiki schematic, with source/license attribution.
- Deep-Formix GPU-chess cover.
- CryptoCash, CryptoHanko, Mandelbrot, MMG, QR Wi-Fi, Chess960×960 covers.
- LifeAPI: static syntax-coloured code image, **no code scrollbar**.
- CatForce: animated still-life/block placements conveying combinatorial search; earlier generic diagrams were rejected.
- Sphere packing: 3D arrangement, not a flat 2D picture.
- Neural CA: genuine intermediate evolution frames, with explained input/timing.
- TQRNG photon-arrival schematic.
- Current tile diagrams and renders developed through user review.

Provenance: `docs/asset-sources.json`. Initial content review: `docs/content-sources.json`.

Approved images do not imply blanket approval of future redesigned covers. Do not create AI bitmap art for exact tile mechanics; use Python/CAD-derived renders and diagrams.

## 7. Life-in-3D article: current required presentation

Canonical local page: `http://localhost:4321/Homepage/articles/life-in-3d-tiles/`.

### Four distinct construction levels

Keep these distinct; conflating them caused repeated user corrections:

1. Basic parts: cores/bottoms, sides, and top/input/output faces from March 21, 2019 OpenJSCAD.
2. Configurable cubes assembled from those parts.
3. Actual compound computational tile types (the 26-type Life construction).
4. Full assembled cellular-automaton computation.

The original ten CAD parts are **for constructing tiles**, not the actual 26 tile types. The website now displays Python-generated actual computational tiles. The earlier construction-piece assets/source are archived separately.

Also keep the earlier 2016 printable still-life project separate from the 2019 evolving-Life construction. The still-life forum has print reports; the current computational set has not been printed/tested.

### Final visual layout

- One compact whole-set 3D image for each set, with its pieces lying side by side on a common plane.
- **Exactly one representative example per set**, not 32 separate viewers and not a large page of tile variants.
- Five sets: Blue, Orange, Purple, Black/white, Boundary blue.
- Each example shows **both output/top and input/underside at the same time**, with independent rotation and keyboard controls.
- Both views persist when the static two-face fallback is replaced by WebGL. Do not reintroduce the bug that replaces them with a single face.
- Both cameras’ states survive scrolling away/back. Reset restores top and underside together.
- Side-by-side on desktop; stacked on mobile.
- Full assembly has its own single rotatable viewer.
- Assembly spacing: min 0 mm, max **200 mm**, default **40 mm**. No 40 mm maximum.
- The assembly cover is an actual exploded six-layer glider model.
- Four clear worked blue/orange/purple/final 2D schematics; full glider schematics are expandable.
- Additional expandable explanation panels list **all** 6/8/8/4/6 input/output cases and explain their connections.
- A worked glider-cell calculation explains all five added layers and Life’s simultaneous update.

Current representative IDs:

| Set           | Example      |
| ------------- | ------------ |
| Blue          | `blue-1`     |
| Orange        | `orange-010` |
| Purple        | `purple-P5a` |
| Black/white   | `final-2`    |
| Boundary blue | `corner-1`   |

### Key website files

| File                                        | Role                                                                 |
| ------------------------------------------- | -------------------------------------------------------------------- |
| `src/content/articles/life-in-3d-tiles.mdx` | Article, explanations, tables, worked trace, embeds                  |
| `src/components/LifeTileSet.astro`          | Whole-set image plus one chosen representative                       |
| `src/components/LifeTileExplorer.astro`     | Controls, fallback, paired-view layout, activation/disposal          |
| `src/scripts/life-tile-set.ts`              | GLB loading, cameras, independent rotation, assembly transformations |
| `src/components/TileSchematic.astro`        | Full-width SVG with caption and full-size link                       |
| `src/data/life-tile-catalogue.json`         | 32-type metadata and preview paths                                   |
| `public/images/life-tiles/`                 | Group renders, tile preview pairs, approved SVG schematics           |
| `src/assets/images/life-tiles-assembly.png` | Main optimized article cover                                         |
| `public/models/life-tiles/`                 | GLB, STL ZIP, placement JSON, checks, design notes                   |

## 8. Tile logic and geometry: authoritative reconstruction

### General interface and convention

- A complete Life cell has **one bit**, repeated at all four corner outputs. It must never show independent bits in its four corners.
- Circle/ring = 0; plus = 1.
- Previous layer outputs protrude upward; next layer inputs are recesses underneath. Top = output; bottom = input.
- A mixed 2×2 input is received by a blue piece **between four adjacent Life cells**, not inside a single Life cell.
- All defined input sockets require actual compatible supplied outputs. No bridging over omitted internal pieces. Complete the declared prior layer first.
- Logical “don’t care” accepts either supplied bit, not missing hardware.
- Designed separator gaps and clearance around unrelated connectors are not omitted required tiles.
- No moving gates or presence-detection machinery is part of this convention.
- Model body thicknesses, connector profiles and some heights are present-day prototype choices, not recovered 2019 production CAD.

### Blue

Six rotational equivalence classes cover all sixteen 2×2 bit inputs. For input:

```text
a b
c d
```

its logical 4×4 top is:

```text
a b a b
c d c d
a b a b
c d c d
```

Each output quadrant copies the entire input. Do not put four equal copies of one input into a quadrant.

For a Life cell/blue width `L=60 mm` in the current coordinate system:

- Uniform Life-cell corner centres: `L/6`, `5L/6` = 10, 50 mm.
- Blue input centres: `L/3`, `2L/3` = 20, 40 mm.
- The blue input **region** is a contiguous 2×2 of `L/3` squares, total side `2L/3`, inside an `L/6` border. The region’s side is not the centre-to-centre spacing.
- Blue pieces are centred at junctions of four Life cells.
- Blue top data centres: `0.1L, 0.3L, 0.7L, 0.9L` = 6, 18, 42, 54 mm.
- Four 2×2 output groups occupy the corners, with a **20% empty cross/separator region** between them.
- Current solids put **nine fixed raised X registration blockers**, one per separator square, in that cross. These are not purple wildcard data sockets.
- Earlier conversation considered one big X or small X/L registration options. Do not claim the current model implements a single big X; it uses nine fixed blockers. Revisit geometry explicitly if the user requests another option.

Do not replace thirds with quarters in input diagrams. Do not mistake the blank border/cross for a logical bit.

### Orange: same eight types, two physical passes

A strip receives `(x,y,y,z)` and outputs:

```text
unary(x+y+z), C_y
```

Unary outputs: 0 → `000`, 1 → `100`, 2 → `110`, 3 → `111`. Both middle input sockets exist and must fit the same bit. The duplicate middle is counted once and preserved through a distinct C key. C0 is a square ring and C1 a diamond ring in the current prototype.

| Type (`xyz`) | Input | Output  |
| ------------ | ----- | ------- |
| 000          | 0000  | 000, C0 |
| 001          | 0001  | 100, C0 |
| 010          | 0110  | 100, C1 |
| 011          | 0111  | 110, C1 |
| 100          | 1000  | 100, C0 |
| 101          | 1001  | 110, C0 |
| 110          | 1110  | 110, C1 |
| 111          | 1111  | 111, C1 |

Four strips process horizontal rows around each target. Three of the same types, rotated 90°, process the three ordinary data columns. The first pass’s C column stays exposed, including two copies of the original centre. The second pass’s extra C-shaped outputs are auxiliary values; they must not replace the original centre in the final rule.

After two passes, the central 3×3 contains an ordered packed shape with exactly as many ones as the original inclusive neighbourhood. Packing toward top/left versus bottom/right is a coordinate rotation; do not mix orientations without saying so.

### Purple

Eight masks classify the ordered 3×3 produced by orange. They are not general-purpose masks for any unordered nine bits. `X` is a combined bit-accepting recess. `/` separates rows. The forum reference orientation packs ones bottom/right:

| Type | Input mask      | Output            |
| ---- | --------------- | ----------------- |
| P0   | X00 / X00 / 0XX | other (total 0–2) |
| P3a  | 000 / 000 / 111 | 3                 |
| P3b  | 000 / 001 / 011 | 3                 |
| P4a  | 001 / 001 / 011 | 4                 |
| P4b  | 000 / 001 / 111 | 4                 |
| P4c  | 000 / 011 / 011 | 4                 |
| P5a  | XX1 / XX1 / 111 | other (total 5–9) |
| P5b  | XX1 / X11 / XX1 | other (total 5–9) |

Rotate masks as needed. Low and high totals produce the same `other` output category. Current output keys are annuli of different radii for `3`, `4`, and `other`, a new modelling choice. Purple outputs a category, not the next Life bit.

### Black/white final state

The stepped underside connects to two heights: the higher purple category and the lower original C channel from the first orange pass. Other C ports are cleared safely and are not additional inputs.

Let original centre be `s`, neighbours `n`, inclusive count `m=n+s`:

```text
s_next = (m == 3) OR (s AND m == 4)
```

| Category | Original centre input | Output at all four corners |
| -------- | --------------------- | -------------------------- |
| 3        | C0 or C1 (`C*`)       | 1,1,1,1                    |
| 4        | C0                    | 0,0,0,0                    |
| 4        | C1                    | 1,1,1,1                    |
| other    | C0 or C1 (`C*`)       | 0,0,0,0                    |

This is Conway’s B3/S23 rule expressed using an inclusive count. `C*` still requires a supplied C0/C1. The uniform four-corner output starts the next generation’s interface.

### Boundary geometry and unchanged final footprint

The user specifically authorized extending blue **half a cell outside the border**, then returning to the same final grid. Do not merely shift ordinary blue pieces and hide unsupported sockets.

The six current boundary types are full **60×60 mm** bodies:

- Four edge variants (`edge-00`, `01`, `10`, `11`) have only two recessed input sockets over real board cells, with the exterior pair encoded as constant zeros.
- Two corner variants (`corner-0`, `corner-1`) have only one real input socket, with three exterior zeros.
- Exterior underside positions are solid; no unsupported recesses are left to fill.
- All six retain full sixteen top bit keys and the registration cross.
- They are used only at the declared perimeter and rotated inward.
- Blue spans `[-30,330] mm` in both axes around a 300×300 mm Life board.
- Initial and final states remain `[0,300] mm`, **5×5 cells**, with no shrinking/clipping of the glider.
- All on-board cells, including padding, evolve. Only the outside is fixed zero.
- This equals the infinite-plane result only while sufficient padding prevents activity interacting with the fixed boundary.

Old half-width/quarter-width boundary descriptions are superseded.

### Counts and validation

- 26 computation types = 6 blue + 8 orange + 8 purple + 4 final.
- Five added layers per generation: blue, orange horizontal, orange vertical, purple, final.
- Initial state plus those layers = six physical layers in a one-step assembly.
- Six boundary types bring the downloadable catalogue to 32 types.
- Complete one-step glider assembly: 286 placements = 25 initial + 36 blue (16 interior, 16 edge, 4 corner) + 100 first-orange + 75 second-orange + 25 purple + 25 final.
- 512 possible binary 3×3 neighbourhoods checked against an independent Life rule.
- 875 assembled mesh intersection checks; recorded maximum overlap about `0.000178 mm³` (numerical tolerance).
- Boundary STL checks: 96 top keys, 10 real sockets accepting the correct bit/rejecting the opposite bit, solid undersides at 14 exterior sites.
- All 32 type meshes checked connected/watertight.
- Do not claim these checks prove arbitrary misplaced/rotated pieces impossible or that 26 is minimal.
- All current computational models have **zero mating clearance**. They are nominal prototypes, not print-tested hardware. Calibration/physical fitting remains.

Current 5×5 glider input and one-step output:

```text
Input      Output
00000      00000
00100      00000
00010      01010
01110      00110
00000      00100
```

The article’s worked target has neighbourhood `001 / 111 / 000`: inclusive total 4, original C1, final live. After the second orange pass it has packed ordinary bits `111 / 100 / 000`, with the original C1 preserved separately.

## 9. Research/model source map and regeneration

Primary research directory: `research/3d-tiles/`.

| File/directory                                                                              | Role                                                                                        |
| ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `cgol_computational_tiles.py`                                                               | Pure-Python logical routing, orange transforms, purple masks, final rule, exhaustive checks |
| `blue_tiles_3d.py`                                                                          | Ring/plus keys, uniform Life cells, blue solids, third-based coordinate geometry            |
| `all_tiles_3d.py`                                                                           | Original 26 computational meshes and stepped final pieces                                   |
| `bounded_tiles_3d.py`                                                                       | Current full-width boundary variants and complete 5×5 assembly                              |
| `check_boundary_ports.py`                                                                   | Tests actual exported boundary STL interfaces                                               |
| `export_homepage_tiles.py`                                                                  | Copies current models, metadata, renders and placement data into website                    |
| `render_compact_sets.py`                                                                    | Compact whole-set images and cropped approved SVG examples                                  |
| `render_assembly_cover.py`                                                                  | Main cover from the actual 286-piece assembly                                               |
| `orange_2d_schematics.py`, `orange_connections.py`                                          | Orange case diagrams and original versus auxiliary C channels                               |
| `glider_blue_orange.py`, `glider_second_orange.py`, `glider_purple.py`, `final_bw_tiles.py` | Worked-stage schematics                                                                     |
| `blue-schematics/`, `computational-schematics/`                                             | Earlier approved diagrams plus historical draft/audit files                                 |
| `all-solids/`                                                                               | Original 26-type models                                                                     |
| `bounded-solids/`                                                                           | Current 32-type models, placement data, validation, ZIP, GLB                                |
| `original-2019.jscad`                                                                       | Unchanged public source for modular construction pieces                                     |
| `thingiverse-upload/`                                                                       | Earlier ten-part modular-kit package, not the 32 computational set                          |

Do not assume every older research script/report is the current design. Some preserve rejected proposals and incomplete historical stages.

If logical content alone changes, do not regenerate all meshes. If UI alone changes, do not regenerate assets. If the geometry changes, update source, recheck fits, regenerate models/images/metadata, then rebuild.

Python runtime previously prepared in `/tmp/homepage-mesh-runtime` includes optional modelling dependencies. It is temporary and may disappear. Inspect availability before relying on it. Geometry generation uses NumPy, trimesh, manifold3d, matplotlib, and Pillow. Site builds do not require Python.

Example commands, from the workspace, if that runtime still exists:

```bash
python -c "import sys; sys.path.insert(0, 'research/3d-tiles'); import cgol_computational_tiles as t; print(t.verify())"

PYTHONPATH=/tmp/homepage-mesh-runtime python research/3d-tiles/bounded_tiles_3d.py
PYTHONPATH=/tmp/homepage-mesh-runtime python research/3d-tiles/check_boundary_ports.py
PYTHONPATH=/tmp/homepage-mesh-runtime python research/3d-tiles/export_homepage_tiles.py
PYTHONPATH=/tmp/homepage-mesh-runtime python research/3d-tiles/render_compact_sets.py
PYTHONPATH=/tmp/homepage-mesh-runtime python research/3d-tiles/render_assembly_cover.py
npm run verify
```

If original 26 solids must be rebuilt, inspect/run `all_tiles_3d.py` first; the bounded generator reads those originals. Asset rendering can take a minute. Keep progress updates while it runs.

Legacy construction-piece regeneration: `npm run export:construction-pieces`. Its JSCAD source is excluded from formatting intentionally. Ten exports use 3× scale; only a detached flat boolean artifact was removed from one exported result. Do not conflate this export with rebuilding the computational tiles.

## 10. Development, URLs, checks, and browser behavior

### Stack

Snapshot package versions: Astro 7.3.8, MDX 8.0.3, Three.js 0.186.1, KaTeX 0.16.22 range. Node must be at least 22.12.0. Use the existing lockfile; inspect versions before upgrading. Do not upgrade merely to continue work.

Astro config:

```text
site = https://simsim314.github.io
base = /Homepage
trailingSlash = always
output = static
```

Markdown and MDX both use remark-math and rehype-katex. `scripts/remark-base-paths.mjs` prefixes root-relative Markdown links/assets. Raw HTML/component attributes must use `href()` from `src/lib/content.ts`; they are not rewritten by that plugin.

### Commands

```bash
cd /home/simsim314/GitHub/Homepage
npm ci                 # when dependencies need installation
npm run dev            # live source development server
npm run check          # Astro/TypeScript diagnostics
npm run build          # writes dist/
npm run preview        # production build preview
npm run verify         # check + build + built-site verifier
```

Avoid whole-repository formatting because unrelated changes and historical source exist. Format only files changed for the current request, then run `git diff --check`.

### Current local server caveat

At the snapshot, port 4321 was running **Astro preview**, serving `dist/`, not live source. Source changes only appeared after rebuilding. Inspect the current process before assuming this remains true. Do not open another server on the same port unnecessarily.

Local homepage: `http://localhost:4321/Homepage/`.
Local tile article: `http://localhost:4321/Homepage/articles/life-in-3d-tiles/`.

### Verification scope and latest result

Latest completed check after the paired-face and mobile fix:

- Astro diagnostics: 0 errors, 0 warnings, 0 hints.
- Built-site verifier: 49 HTML pages, 30 canonical articles, 1,984 internal links/assets, math rendering, search, sitemap, duplicate IDs, and article visual ownership.
- All five representative examples load two canvases, permit keyboard rotation independently, and restore paired views after returning to the section.
- Assembly still loads, starts at 40 mm and allows 0–200 mm.
- At a 390 px requested viewport, document client width/scroll width both 375 px; paired mobile panes are about 306 px wide and stack.
- No errors in the tested fresh preview tab’s console.
- A lazy Three.js bundle size advisory is expected. This is not an Astro diagnostic failure; Three.js is loaded on demand.

These are completed checks, not a guarantee every future edit is safe. Run relevant verification after changes; do not repeatedly rerun broad tests without new changes or concerns.

### Viewer implementation and regression traps

- GLB geometry is cached and transformed using original mesh/world coordinates.
- Assembly translations and rotation centres are significant. Preserve them; centring each tile independently breaks placements.
- Layer spacing changes Z by `layer * gap`; geometry/X/Y are preserved.
- `LifeTileExplorer.astro` activates near viewport and releases WebGL contexts offscreen.
- Current `mountLifeTileExplorer` wraps one renderer for assembly or two single-face renderers for each representative.
- Two camera states are saved/restored. Independent keyboard input is bound to each canvas.
- Avoid treating static fallback as proof that WebGL works: wait for both live canvases and inspect the result.
- Current mobile article grid uses `minmax(0, 1fr)` to prevent minimum-content overflow.
- Activation failure restores the static fallback rather than leaving an empty pane.
- A stale browser tab once timed out; a fresh tab in the same browser worked. Do not report that as a verified site failure without inspecting a current tab.

Use the available browser-control tool to interact with the browser; do not bypass it with shell automation. After a compacted chat, restore its documentation. Browser tab IDs/bindings from this chat are temporary; rediscover the local tab. Scrolling over a canvas zooms it; scroll in the outside margin to move the page.

## 11. GitHub Pages configuration and publication limits

`.github/workflows/deploy.yml` is configured for pushes to `main`, pull requests, and manual dispatch. It installs the lockfile and runs `npm run verify`; non-PR runs upload the Pages artifact and deploy with Pages/OIDC permissions.

**This means a push to main could publish. Do not push without approval.** A configured workflow is not proof that GitHub’s Pages source is enabled or that the current local work is live.

When website publication is explicitly authorized, inspect repository state and Pages settings, prepare the reviewed content, and then use the existing workflow/base path. Do not ask the user to sign in merely to configure deployment before approval to upload has been given.

Thingiverse is separate: the user explicitly requested posting printable files. At this snapshot no upload occurred. The prepared ten-part package still needs account access, a user-selected publication license, and confirmation that the package corresponds to the intended construction level. Do not silently assign a license or upload the wrong kit. The newer 32 computational prototypes also need clear zero-clearance/print-test status if packaged for printing.

## 12. Outstanding work and sensible continuation

No immediate viewer bug was left knowingly unresolved at the end of the recorded turn. The user’s next request controls what to do next.

Possible follow-ups, not blanket authorization to change everything:

1. Continue improving the tile article and assembly under the agreed geometry/convention; use real model calculations, not cosmetic arrangements.
2. Print calibration and physical fit tests remain. Choose tolerances with the user before describing a printable working machine.
3. Prepare the correct Thingiverse package/license/account workflow for the set the user wants published.
4. Continue interviews across Remini, cryptography, Chess960×960, Mandelbrot, neural CA, randomness, and other projects. Do not keep asking only about sphere packing.
5. Review shallow article sections with the author. Public descriptions can explain technical facts; first-person motivation requires his answers.
6. Resolve the Live Free or Die bounty amount/Bitcoin recollection if the user wants that story included.
7. Consider a careful manuscript/novelty review for the unpublished convex-hull work before any arXiv submission discussion.
8. Preserve source-backed shared attribution and expand CA coverage only when new evidence exists.
9. Website deployment remains pending explicit permission.
10. Documentation consistency: some chronological docs still contain superseded stages. `research/3d-tiles/ASSEMBLY-RULES.txt` mentions an older central-3×3 assembly and half/quarter boundary pieces; `PRINT-NOTES.txt` describes the older ten-part kit/viewer. README’s early construction-piece section also describes the archived viewer. Do not follow those as current article layout. Reconcile them when documentation maintenance is requested; keep historical provenance explicit.

### Recommended first reads in a new chat

1. This file, then the new user request.
2. `README.md` for commands/architecture.
3. `docs/editorial-guide.md` for interview voice and confirmed facts, reading latest corrections after earlier entries.
4. Latest entries in `docs/verification.md`; older entries are chronological history, not final layout requirements.
5. For tile tasks: article, `LifeTileSet.astro`, `LifeTileExplorer.astro`, `life-tile-set.ts`, relevant Python source and current bounded validation.
6. For another article: its source/frontmatter, relevant repository/forum sources, and provenance records.

## 13. Historical specification and superseding corrections

The original nine-point specification is reproduced below so a new chat does not need an ephemeral attachment. It is source history. The current user clarifications above supersede conflicting items, especially:

- No separate Blog page/nav; homepage is the blog.
- Repository is Homepage, not simsim314.github.io.
- No website upload/deployment without later explicit permission.
- Ten interests now, including CA Research, computational geometry, and programming.
- Interest cards use typography, not reused article images.
- Museum is excluded as a draft.
- 30 locally published articles now, rather than the initial 15.
- Independent researcher is the title; self-taught belongs in biography.
- Current paired tile examples and overhanging boundary variants supersede all earlier viewer/geometry proposals.

<details>
<summary>Original specification v1 (historical source)</summary>

# Personal Research Website — Specification v1

**Michael Simkin — Independent Researcher**

The website should present your interests, research, discoveries, and software projects. It should feel like a personal research journal combined with a portfolio, rather than a conventional academic CV.

## 1. Homepage

The homepage has five main sections:

| Section               | Purpose                                               |
| --------------------- | ----------------------------------------------------- |
| **Introduction**      | Brief description of who you are and what you work on |
| **Areas of Interest** | Visual cards representing your main interests         |
| **Featured Work**     | Selected research results and projects                |
| **Recent Articles**   | Latest published writing                              |
| **About & Contact**   | Background, GitHub, arXiv, email                      |

### Areas of Interest

This should be the central feature of the homepage.

| Interest                       | Content                                                         |
| ------------------------------ | --------------------------------------------------------------- |
| **Mathematics**                | Sphere packing, mathematical discoveries, AI-assisted proofs    |
| **Conway's Game of Life**      | Simkin Glider Gun, Caterloopilar, search algorithms             |
| **Artificial Intelligence**    | Neural networks, machine learning experiments                   |
| **Cryptography**               | Digital signatures, secure hardware, cryptographic applications |
| **Chess**                      | Engines, neural evaluation, chess variants                      |
| **Simulation & Visualization** | Fractals, virtual environments, computational simulations       |
| **Experimental Engineering**   | Hardware, unconventional computation, utilities                 |

Each card leads to an **interest page** explaining the subject and presenting your related work.

For example:

**Conway's Game of Life →**

An introductory article about your involvement in the field, followed by links to Simkin Glider Gun, Caterloopilar, LifeAPI, CatForce, and other related projects.

## 2. Research articles

Initially:

| Article                             | Subject                                        |
| ----------------------------------- | ---------------------------------------------- |
| **High-Dimensional Sphere Packing** | Your recent mathematical research              |
| **Simkin Glider Gun**               | Construction, discovery, significance          |
| **Caterloopilar**                   | Spaceship construction and related discoveries |

The sphere-packing article can discuss AI assistance where relevant. No separate research-methodology article is needed.

Additional research articles can be added when there is material ready for publication.

## 3. Project articles

The ten projects selected previously should each have their own dedicated page.

| Project                   | Main category                     |
| ------------------------- | --------------------------------- |
| CryptoHanko               | Cryptography                      |
| CryptoCash                | Cryptography                      |
| Chess960x960              | Chess                             |
| Deep-Formix               | Chess / AI                        |
| Mandelbrot CUDA           | Simulation & Visualization        |
| CGOL Virtual Museum       | Simulation & Visualization / CGOL |
| Neural CA MNIST           | Artificial Intelligence           |
| TQRNG Webcam              | Experimental Engineering          |
| Multilayer Mutilated Gear | Simulation & Engineering          |
| QR Wi-Fi Scanner          | Software Utilities                |

Additionally, LifeAPI and CatForce should be accessible from the Conway's Game of Life interest page.

Each project should link to its GitHub repository and, where available, its live demonstration.

## 4. Individual article format

**Every research result and project should have a full article-style page.**

Standard structure:

1. **Title and short introduction** — what the work is about.
2. **Background and motivation** — why you developed it.
3. **The main idea** — explanation accessible to interested readers.
4. **Implementation or mathematical details** — technical discussion.
5. **Results** — discoveries, performance, demonstrations, or conclusions.
6. **Images and interactive content** — screenshots, animations, simulations, equations.
7. **Links** — GitHub, papers, live demos, references.

Not every article needs all seven parts.

For mathematical research, the article should distinguish established results from conjectures and work in progress.

For software, it should distinguish implemented functionality from experimental ideas.

## 5. Blog

The blog provides a chronological view of your writing.

It should support:

- Mathematical articles with LaTeX equations.
- Technical explanations and code.
- Images, animations, and embedded interactive demonstrations.
- Publication and update dates.
- Categories and tags.
- Links between related articles.

**An article should exist only once.**

For example, the Caterloopilar article can appear under Conway's Game of Life and in the blog index without duplicating its content.

Your existing `Spirtuality` repository remains separate.

## 6. Navigation

The proposed navigation is:

**Home | Interests | Research | Projects | Blog | About**

The distinctions are:

| Page      | Content                                   |
| --------- | ----------------------------------------- |
| Home      | Overview and highlights                   |
| Interests | All your areas of interest                |
| Research  | Mathematical and scientific contributions |
| Projects  | Software, tools, interactive applications |
| Blog      | Chronological collection of articles      |
| About     | Biography, background, contact            |

An article can appear in multiple indexes, but maintains a single canonical URL.

## 7. Design

I recommend a modern, visually oriented design.

The homepage should feature large visual cards for interests, using images from your actual work.

Project pages should prioritize live demonstrations wherever available. In particular, the Mandelbrot explorer, chess tools, and Game of Life museum are suitable for interactive links.

The design should remain appropriate for mathematical research: clear typography, readable equations, and distraction-free long-form articles.

## 8. Technical implementation

| Component       | Choice                          |
| --------------- | ------------------------------- |
| Repository      | `simsim314.github.io`           |
| Framework       | Astro                           |
| Hosting         | GitHub Pages                    |
| Articles        | Markdown / MDX                  |
| Mathematics     | KaTeX                           |
| Styling         | CSS                             |
| Images          | Local assets, optimized for web |
| Search          | Client-side search              |
| Version control | GitHub                          |

Pages and indexes should be generated from article metadata, so adding a new article does not require manually editing the homepage.

### Content metadata

Each article should contain:

```yaml
title: 'CryptoHanko'
description: 'Hardware-backed digital signatures on Android'
type: project
topics:
  - cryptography
status: implemented
featured: true
date: 2025-09-23
github: https://github.com/simsim314/CryptoHanko
image: /images/cryptohanko.jpg
```

Dates, descriptions, and statuses should come from the project documentation and be verified before publication.

## 9. Initial content and scope

| Content                          | Initial coverage |
| -------------------------------- | ---------------: |
| Homepage                         |                1 |
| Interest categories              |                7 |
| Research articles                |                3 |
| Selected project articles        |               10 |
| Additional CGOL tooling articles |                2 |
| About page                       |                1 |
| Blog index                       |                1 |

**Total: 15 individual research/project articles**, plus the homepage, category pages, and supporting pages.

We can start these articles from your existing repositories and documentation rather than writing everything from scratch.

### Guiding principles

The website should be organized around **your actual work and interests**, not GitHub repository names.

It should:

- Showcase your most interesting work rather than all 79 repositories.
- Allow an interest to contain multiple research results and projects.
- Give each significant contribution its own substantial article.
- Clearly distinguish research results, implemented projects, and experiments.
- Be easy to expand as you publish new work.
- Preserve your existing repositories without modifications.

This gives us a defined initial website while leaving room for additional interests, research, and projects.

</details>

---

**Continuation rule:** preserve the author’s decisions, inspect current source/evidence, make the next requested change locally, verify it, and keep this handoff current after substantial new decisions. Do not claim publication or physical fabrication that has not happened.

Latest verification: npm run verify passes with zero Astro diagnostics, 49 HTML pages, 30 canonical articles, 2353 internal links/assets. New cycle fallback loads under image pause; both revised desktop pages have no overflow. Confirmed hull body and metadata use 2009. Screenshots: .editorial-private/reviews/ping-pong-cycle.png and convex-hull-v7.png. No fresh mobile check or publication.

## October 13: Gemini origin and public manuscript wording

The author confirms an article about Andrew Wade’s ORIGINAL Gemini (2010), not Dave Greene’s 2013 Geminoid, sparked his interest in Life. Serizawa Geminoid was one of his first results, much smaller and more efficient; then Geminoid Particles; much later the same construction technique in Remini. Biography, Life interest, and those three articles now connect this history. No quantified cross-rule comparison or exact identification of the remembered news article has been supplied. Original announcement p2323 (May18,2010), t399 read in browser, archived research/gemini/announcement.json. Public convex-hull article must not mention v7/version7; these are internal file identifiers. Removed from caption, source label, heading. Raw manuscript filenames remain internal.

Verified these editorial changes with npm run verify: zero Astro diagnostics, 49 HTML pages, 30 articles, 2362 internal links/assets. Browser confirms linked construction history and no desktop overflow; public hull text has no internal version tag. Screenshot .editorial-private/reviews/gemini-origin-story.png.

Final layout override: the two end views are UPRIGHT, side by side, preserving aspect ratio and following each successive operating head after the first replacement finishes. Earlier rotated-panel descriptions are superseded. This keeps both active arm targets visible; actual rings identify Serizawa elbows on perpendicular axes, blue highlights state7 movable blocks in Particles. Whole-pattern tape overview remains vertically compressed and explicitly labelled. Optimized tape renderer is exact: its occupancy matches independent aggregation of every cell at8388608. Reports include actual arm target positions. Scripts regenerate source checkpoints when temporary caches disappear.

Final checks: Verified 49 HTML pages, 30 canonical articles, 2364 internal links/assets, Markdown/MDX equations, search index, sitemap, and visual ownership by article. Python renderers compile. Both main covers and still fallbacks load at1100×760, with enlarged article display and no desktop overflow. Fresh screenshots: .editorial-private/reviews/serizawa-both-ends.png and particles-both-ends.png. Local only; no fresh mobile check.
