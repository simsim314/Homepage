---
title: 'Caterloopillar'
description: 'An engineered family of Life spaceships, with two halves that construct one another.'
type: 'research'
topics: ['game-of-life']
status: 'demonstrated'
visual: 'life'
featured: false
image: /images/caterloopillar-lifewiki.png
imageAlt: LifeWiki schematic showing the front and back reading heads and mutual construction of a Caterloopillar.
imageCredit: LifeWiki Caterloopillar schematic, uploaded by dvgrn; GNU Free Documentation License 1.2.
imageSource: https://conwaylife.com/wiki/File:Caterloopillar.png
date: '2026-10-12'
tags: ['spaceships', 'cellular automata', 'construction']
github: 'https://github.com/simsim314/Caterloopilar'
sources:
  [
    {
      'label': 'Construction thread: initial mechanism and working c/8 ship',
      'url': 'https://conwaylife.com/forums/viewtopic.php?f=2&t=2151',
    },
    {
      'label': 'Construction constraints and speed discussion',
      'url': 'https://conwaylife.com/forums/viewtopic.php?p=30110',
    },
    {
      'label': 'Completed RLE patterns and construction scripts',
      'url': 'https://github.com/simsim314/Caterloopilar',
    },
    {
      'label': 'LifeWiki: Caterloopillar history and mechanism',
      'url': 'https://conwaylife.com/wiki/Caterloopillar',
    },
    {
      'label': 'Schematic source and image history (dvgrn)',
      'url': 'https://conwaylife.com/wiki/File:Caterloopillar.png',
    },
    {
      'label': 'Image license: GNU FDL 1.2',
      'url': 'https://www.gnu.org/licenses/old-licenses/fdl-1.2.html',
    },
  ]
---

Caterloopillar is a family of engineered spaceships in Conway's Game of Life. The construction is a kind of strange loop: each half of the ship helps build the other. My comparison is to Escher's hands drawing one another. Understanding the moving pattern requires following that construction cycle, rather than treating it as a small oscillator with a simple displacement.

## The first working construction

The April 9, 2016 forum announcement reported a completed orthogonal $c/8$ spaceship. Here $c$ is one cell per generation, the usual speed-of-light convention in Life. The actual construction advances 250 cells in 2,000 generations:

$$
\frac{250c}{2000}=\frac{c}{8}.
$$

The discussion distinguishes that working example from the wider aim of supporting speeds below $c/4$.

## Reading heads and slow salvos

The mechanism uses front and back streams of lightweight, middleweight, or heavyweight spaceships, collectively called \*WSS. These salvos act as reading heads. They interact with a stream of still lifes, producing glider-based slow-salvo construction recipes.

The still-life stream provides the material that is effectively carried through the construction. The two ends reconstruct the machinery needed by one another, closing the loop. The linked forum thread includes the construction illustration and the detailed recipe discussion.

## Choosing a speed

Changing speed involves arranging reading-head distances and the timing of the recipes. It is not a speed slider on an already running ship. Each chosen speed requires a compatible construction.

The later forum discussion makes the constraints concrete: a requested speed above the design range causes the heads to overlap, while even valid speeds can require a search for suitable step and period values. Script support also has limits; a general design argument is not the same thing as a supplied pattern for every parameter choice.

## What the repository contains

The repository supplies Python/Golly construction scripts, recipe data, and many completed RLE patterns. Examples include `Caterloopillar_c8.rle`, `Caterloopillar_c17.rle`, `Caterloopillar_2c9.rle`, and `Caterloopillar_31c240.rle`.

The source scripts assemble reading heads, manipulate recipes, and validate intermediate arrangements. They use Golly's Python API and include Python 2-era syntax such as `xrange`; these are historical construction tools, not a newly verified modern installation.

## Where the design came from

LifeWiki traces the adjustable-speed idea to David Bell and Jason Summers, and the renewed forum discussion to Hartmut Holzwart. Alexey Nigin proposed the two streams constructing one another through slow salvos. My work developed that approach into a concrete construction, completed in April 2016.

The [schematic on the homepage](/#article-caterloopilar) is the actual image used in the LifeWiki article, showing how the two ends read and move the construction tape.

## The engineering work

The forum record emphasizes the number of interlocking details: recipe compatibility, backward salvos, placement, and supporting utilities. The completed RLE files are concrete results. Broader possibilities discussed in the thread should be read as proposals unless accompanied by an actual construction.

For inspection, start with a supplied RLE in Golly and then follow the forum discussion. The full-scale ships are far larger than the small Life demonstration on this website.
