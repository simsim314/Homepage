---
title: '24-cell quadratic growth'
description: 'A 24-cell breeder discovered between the 25-cell seed and switch engine ping-pong.'
type: 'research'
topics: ['game-of-life']
presentationOrder: 1000
status: 'demonstrated'
showPreview: true
image: /images/life-24-cell-quadratic-growth.gif
imageAlt: Later evolution of the original 24-cell seed, generations 4,194,304–16,777,216.
imageCredit: Original pattern evolved with Golly 3.3; local animation with a still fallback.
imageSource: https://conwaylife.com/wiki/24-cell_quadratic_growth
visual: 'life'
date: '2026-10-12'
tags: ['quadratic growth', 'breeder', '2014']
sources:
  [
    {
      'label': 'LifeWiki: 24-cell quadratic growth',
      'url': 'https://conwaylife.com/wiki/24-cell_quadratic_growth',
    },
  ]
---

I found **24-cell quadratic growth on October 23, 2014**, two days after my [25-cell pattern](/articles/25-cell-quadratic-growth/).

The animation shows the original seed after 4,194,304–16,777,216 generations. Each lit square contains live cells within a 16,384 × 16,384-cell region; the entire pattern is simulated. The view stays fixed as the structure grows, then the clip resets.

## What the cell count means

Twenty-four is the initial number of live cells, not the size of the eventual population. LifeWiki classifies this pattern as a breeder with quadratic growth. Its sparse starting configuration occupies a long bounding box.

The interesting property is what the seed produces as Life evolves: continuing growth from a finite initial population, under the usual B3/S23 rule.

## One step in the sequence

This was a historical minimum-population result. A week later, [switch engine ping-pong](/articles/switch-engine-ping-pong/) lowered the initial population to 23 cells. Subsequent discoveries by other researchers lowered it further.

The LifeWiki article provides this pattern's RLE file and links the discovery report. It should be explored as its own construction, alongside the other two October 2014 results.
