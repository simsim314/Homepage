---
title: 'Making Still-Life Tiles Physical'
description: 'Printable puzzle pieces whose connections encode Life’s stability constraints, developed with Paul Callahan and Adam Goucher.'
type: research
topics: [game-of-life, experimental-engineering]
status: demonstrated
showPreview: true
image: /images/still-life-tiles-cover.jpg
imageAlt: 'Blue printed still-life puzzle tiles held beside a ruler, photographed in June 2016.'
imageCredit: 'My original printed-tile photograph, June 3, 2016.'
imageSource: https://conwaylife.com/forums/viewtopic.php?p=31711#p31711
date: 2026-10-12
tags: [still life, tiling, 3D printing, physical computation, puzzle]
sources:
  - label: 'Paul Callahan’s original still-life tiling discussion, May 2016'
    url: https://conwaylife.com/forums/viewtopic.php?t=2188
  - label: 'My printable tile designs and attachment discussion, May 2016'
    url: https://conwaylife.com/forums/viewtopic.php?p=31135
  - label: 'My first reported working prints, June 3, 2016'
    url: https://conwaylife.com/forums/viewtopic.php?p=31711#p31711
---

## A rule enforced by the pieces

Paul Callahan’s still-life tiles were an inspiration for my interest in physical Conway’s Life mechanisms. If the pieces fit together according to their constraints, the represented pattern must be stable.

A still life has no changing cells. Every live cell must have two or three live neighbours, and every dead cell must have a neighbour count other than three. The puzzle turns these local conditions into compatible and incompatible connections. Finding a valid assembly becomes a way to work with the rule by hand.

## My contribution

Callahan introduced the planar tiling problem in May 2016, and Adam Goucher contributed a tile design. My work focused on printable models and practical assembly, including grooves and connections for the empty-cell pieces. The design was a collaboration; I did not originate the whole tile system.

In May I shared printable files and discussed attachment, fragility, and symmetry. On June 3, I reported my first working prints, with qualifications about their fit. I then discussed changes to their height and size. These were actual printing experiments, rather than just illustrations of a possible puzzle.

![The first blue still-life pieces being printed on my 3D printer.](/images/still-life-tiles-printer-front.jpg)

_My photograph from the [June 3, 2016 print report](https://conwaylife.com/forums/viewtopic.php?p=31711#p31711). The cover photograph shows the printed pieces beside a ruler._

![A second view of the blue tile pieces on the printer bed.](/images/still-life-tiles-printer-side.jpg)

_The same printing session, from another angle._

## Geometry has to work in your hands

The mathematical constraint and the physical connection solve different problems. A piece can enforce the right logical relationship and still be awkward to insert, too fragile, or difficult to separate. A puzzle also needs a way to complete an assembly without its last piece becoming impossible to place.

That practical side matters to my research: making the idea work includes the construction and its usability. The forum records the designs, print reports, and revisions, rather than establishing a finished commercial product.

## Beyond stability

I later explored [3D tiles for Life’s evolution](/articles/life-in-3d-tiles/), where successive layers represent generations. [Multilayer Mutilated Gear](/articles/multilayer-mutilated-gear/) takes a different route through simulated mechanical logic. Both connect to my broader interest in physical computation.
