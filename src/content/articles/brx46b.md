---
title: 'BRx46B'
description: 'A 46-generation conduit that carries a B-heptomino directly to another B-heptomino.'
type: 'research'
topics: ['game-of-life']
status: 'demonstrated'
showPreview: false
visual: 'life'
date: '2026-10-12'
tags: ['B-heptomino', 'conduit', 'signal transport']
sources: [{ 'label': 'LifeWiki: BRx46B', 'url': 'https://conwaylife.com/wiki/BRx46B' }]
---

I discovered BRx46B on April 25, 2015. It is an elementary conduit that takes a B-heptomino input to a B-heptomino output in **46 generations**, without passing through an intervening Herschel stage.

## Turning a signal

The output is turned right and flipped, with an offset of $(6,16)$ relative to the input. The supporting catalysts use 14 cells. LifeWiki classifies the conduit as Spartan, meaning it uses the small, standard still-life components of Spartan circuitry.

## Extending the chain

Copies can connect to one another to form a diagonal signal chain. The signal advances by $(11,11)$ every 46 generations, slightly slower than a glider's diagonal motion.

This is a circuit component rather than a freely moving spaceship. The moving signal depends on the stationary catalysts along its route.

LifeWiki provides the pattern, its output orientation and recovery timing, and the original discovery report. It is another example of finding useful reactions among a small collection of catalysts.
