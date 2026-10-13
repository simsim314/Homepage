---
title: 'Convex hulls with limited working memory'
description: 'Batched bridge searches for read-only point sets: a current manuscript developing a methodology I recall working on around 2009.'
type: research
topics: [computational-geometry, programming-computing]
presentationOrder: 90
status: note
showPreview: true
image: /images/convex-hull-batched-bridges.png
imageAlt: 'Figure from the manuscript: two active hull gaps split into four after their supporting bridges are certified.'
imageCredit: 'Figure 1 from my October 2026 manuscript, Batched Bridges for Planar Convex Hulls in Two Memory Access Regimes. Colored segments are newly certified bridges; black segments are previously certified hull edges.'
date: 2026-10-12
updated: 2026-10-13
tags: [convex hull, read-only input, memory constraints, bridge finding, randomized algorithms]
sources:
  - label: 'Michael Simkin, Batched Bridges for Planar Convex Hulls in Two Memory Access Regimes, October 2026; unpublished manuscript'
  - label: 'Earlier author-provided manuscript, ConvexHull.doc, and teaching notes on Kirkpatrick–Seidel'
  - label: 'Author recollection: methodology from around 2009 and interest in read-only tape access; interview on October 13, 2026'
  - label: 'Kirkpatrick and Seidel, The Ultimate Planar Convex Hull Algorithm?, SIAM Journal on Computing, 1986'
    url: https://epubs.siam.org/doi/10.1137/0215021
---

## An older idea, written out more precisely

This is **unpublished research**. The October 2026 manuscript develops a methodology I recall working on around **2009**, though I am uncertain of the exact year.

My recollection is that the starting point was a read-only tape: algorithms with $n\log h$ running-time bounds could behave differently once their reading and memory requirements mattered. Noticing that difference led me to investigate explicit access regimes and try to prove what could be achieved using bridge construction.

For $n$ points in the plane, the convex hull is the smallest convex region containing them. Write $h$ for its number of vertices. A huge point set can have a small hull: how much working memory is needed to recover that boundary when the input cannot be rearranged?

The current manuscript, *Batched Bridges for Planar Convex Hulls in Two Memory Access Regimes*, gives two versions of the method. Both retain $O(h)$ writable words. Their running times depend on which input operations are available.

## A bridge reveals an edge

The construction adapts Kirkpatrick–Seidel’s bridge decomposition. Divide a region’s points at a vertical separator and find the upper hull edge crossing it. This **supporting bridge** has one endpoint on each side, with every relevant point on or below its line.

Once that edge is certified, only the portions to its left and right remain unresolved. Each portion is stored as a **gap** between known hull vertices. The algorithm recognizes a gap’s relevant points during a scan using its endpoints and a geometric test; it does not keep a copy of that point set.

The cover shows two gaps becoming four. Newly found bridges are colored, and previously certified edges are black. The faint complete hull is drawn to explain the subdivision; the algorithm has not already stored that boundary.

## Many searches share each scan

The organizing step is to advance all active bridge searches together. One input traversal updates the small record for whichever gap contains the observed point. A gap that finishes keeps its bridge while the others continue.

At each refinement level, the algorithm:

1. Counts the relevant points in every gap.
2. Samples and checks balanced separators through shared scans.
3. Finds all the current supporting bridges.
4. Records those hull edges and replaces the remaining portions with child gaps.

There are $O(h)$ gap records, each with constant-size state. Balanced subdivision limits the number of levels to $O(\min\{h,\log n\})$. Reflecting the points vertically gives the lower hull by the same method.

## Two ways to read the input

**Sequential scans.** The input can be rewound and read in its original order. For each bridge candidate, one scan finds its best partner on the right. Another uses reservoir sampling to choose a left point above that line, if one exists. Such a point improves the candidate. A scan finding no violating point certifies the bridge. All gaps share these rounds.

**Shuffled prefix replay.** An external service supplies a fresh uniform shuffle at each refinement level and can replay any prefix as point records in time proportional to its length. The algorithm maintains bridges incrementally, locating their first violations and repairing them through shared replays. Prefix lengths double, so their total length stays linear in $n$.

Neither client asks for an input point by index. The replay version does assume a stronger external service; its shuffle construction and storage are excluded from the client bounds.

## Time and working memory

Let $D=\min\{h,\log n\}$. The manuscript states these expected bounds:

| Input access | Expected running time | Writable space |
| --- | --- | --- |
| Rewindable original-order stream | $O(n\log h\,\log n\,D)$ | $O(h)$ words |
| External uniform shuffled prefix replay | $O(n\log^2 h\,D)$ | $O(h)$ client words |

The sequential version uses $O(\log n\,D)$ expected full passes. Randomness affects the running time; bridges and separators are checked before they are accepted, so the manuscript’s algorithms return the exact hull under their assumptions.

The faster replay guarantee depends on the external input service. Separating the access regimes makes that assumption explicit.

## What the assumptions leave open

The analysis assumes distinct $x$-coordinates, no three collinear points, and exact geometric predicates with constant cost. Degenerate inputs and coordinate bit complexity require further treatment. The manuscript does not claim optimality or a matching lower bound.

Its appendix also gives a compact prime-cycle permutation family for reproducible experiments. Generating an index order alone does not deliver shuffled point records, and this family does not establish the uniform randomness required by the replay theorem. It is an experimental direction, separate from the two stated guarantees.

The method stores small summaries of the unresolved boundary and revisits the read-only data when more information is needed. Its guarantees account for the way those revisits can actually be performed.
