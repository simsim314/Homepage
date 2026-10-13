---
title: 'Remini'
description: 'Modern self-construction from retro Life circuitry: how new understanding made an old toolkit do much more.'
type: 'research'
topics: ['game-of-life']
status: 'demonstrated'
featured: true
presentationOrder: -90
showPreview: true
image: /images/remini-activation.gif
imageAlt: 'Remini’s original still-life seeds activate into working period-30 circuitry.'
imageCredit: 'Golly HashLife evolution, generations 0–2,400. First constructor detail; the instruction tape continues beyond the view.'
imageSource: https://github.com/simsim314/GreyGooTheory/blob/master/P30Gemini/Remini.mc
visual: 'life'
date: '2026-10-12'
updated: '2026-10-13'
tags: ['self-construction', 'puffer', 'slow salvo']
sources:
  - label: 'LifeWiki: Remini'
    url: https://conwaylife.com/wiki/Remini
  - label: 'Original forum discussion: P30 Self propagating Geminoid'
    url: https://conwaylife.com/forums/viewtopic.php?t=3836
  - label: 'Working Remini and source-code overview, April 14, 2019'
    url: https://conwaylife.com/forums/viewtopic.php?p=74984#p74984
  - label: 'My explanation of the project’s purpose, April 14, 2019'
    url: https://conwaylife.com/forums/viewtopic.php?p=75005#p75005
  - label: 'My clarification of the Conway comparison, April 15, 2019'
    url: https://conwaylife.com/forums/viewtopic.php?p=75028#p75028
  - label: 'Author interview, October 13, 2026'
github: https://github.com/simsim314/GreyGooTheory/tree/master/P30Gemini
---

Remini, short for **Retro Gemini**, is a self-constructing puffer I assembled on April 14, 2019.

It continues a line of work that began when an article about Andrew Wade’s original Gemini drew me into Conway’s Life. One of my first results was [Serizawa Geminoid](/articles/serizawa-geminoid/), a smaller, more efficient construction in another rule. I then built [Geminoid Particles](/articles/geminoid-particles/); much later, I used the same construction technique for Remini with Life’s classic period-30 components.

## Old circuitry, new understanding

I wanted to show how far our understanding of Life had progressed since Conway’s early construction ideas. Old, retro technology could now support a new self-construction design. The comparison mattered to me because the progress was visible even when the components stayed simple.

The breakthrough was realizing that period-30 glider streams could provide universal construction commands: **push, pull, and shoot**. Once I understood that, everything else felt straightforward.

In the [original discussion](https://conwaylife.com/forums/viewtopic.php?p=75028#p75028), I clarified that my historical comparison was with the self-copying gun described in _Winning Ways_. The point was the gap in understanding, rather than a claim that the complete Remini had already been built on an early computer.

## Push, pull, and shoot

An elbow is a small pattern used as the target of a construction arm. A recipe is a sequence of incoming gliders. Push and pull recipes reposition the elbow; shoot recipes produce an outgoing glider. Combining those operations lets a single input channel direct construction at different locations.

## Modern construction with older components

It uses the single-channel, slow-salvo construction mechanism associated with the 0E0P metacell, but builds the machinery from classic period-30 circuitry rather than stable Spartan circuits.

Presence or absence of gliders in an intermittent period-30 stream provides enough control for a construction-arm elbow. The stream encodes instructions through its timing and gaps.

## From still-life seeds to a gun array

The animation follows the opening 2,400 generations of the original pattern. The still-life seeds turn into active period-30 circuitry as the triggering gliders arrive. The view stays on the first constructor; the much longer instruction tape continues outside the frame.

## Building the constructor

The forum records the route from searched arm recipes to the assembled pattern. My search code found movements and glider outputs; scripts collected those recipes, and `Remini.py` combined them with construction instructions from `slmake`.

`slmake`, developed by Adam P. Goucher, supplied slow-salvo recipes for the seeds of the circuitry. Triggering the seeds turns them into the period-30 mechanisms. Synchronizing the two ends was a separate task: the April 13 attempt had a timing mismatch, followed by the working file on April 14.

## What the pattern demonstrates

The significance is the combination: a modern construction method implemented with components available in the 1970s. Remini demonstrates that single-channel self-construction can be realized with that older toolkit. The gaps in a glider stream provide the control; stable Spartan circuitry is not required for this particular construction.

That is the reason for “Retro Gemini”: modern self-construction, classic components.

The completed example is a **puffer**, not a cleaned-up Gemini spaceship: it leaves earlier circuitry behind. The thread also explores a more ambitious “grey goo” search approach. That proposed direction should be distinguished from the arm-and-`slmake` construction used for Remini.

This is a very large pattern. LifeWiki links the downloadable macrocell file for the assembled example. Its listed period and speed are unknown; this article does not supply estimates for them.

[Download the original Remini macrocell](https://conwaylife.com/forums/download/file.php?id=2367) to inspect it in Golly. The [source directory](https://github.com/simsim314/GreyGooTheory/tree/master/P30Gemini) includes the search tools and assembly scripts; the original scripts contain local paths that need adjustment before reuse.

For another approach to patterns that construct their own moving machinery, see [Caterloopillar](/articles/caterloopilar/).
