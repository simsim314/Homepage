---
title: 'Conway’s Game of Life'
description: 'Simple rules, engineered spaceships, and computational discovery.'
order: 2.1
visual: life
representative: remini
articleOrder:
  [
    remini,
    caterloopilar,
    simkin-glider-gun,
    lifeapi,
    catforce,
    switch-engine-ping-pong,
    b60,
    brx46b,
    bne14t30,
    ocellus,
    simkins-p60,
    life-in-3d-tiles,
    still-life-tiles,
    multilayer-mutilated-gear,
    24-cell-quadratic-growth,
    25-cell-quadratic-growth,
  ]
---

## Where my interest began

My interest in Life began with an article about [Andrew Wade’s original Gemini](https://conwaylife.com/forums/viewtopic.php?t=399): a pattern that constructs another copy of itself inside Conway’s simple grid. That possibility drew me into self-construction. One of my first results was [Serizawa Geminoid](/articles/serizawa-geminoid/), in another rule; I later built [Geminoid Particles](/articles/geminoid-particles/) and carried the same construction technique into Life with Remini.

## From local interactions to self-construction

[Remini](/articles/remini/) combines modern single-channel construction with classic period-30 circuitry. The key realization was that p30 glider streams could supply universal construction commands: push, pull, and shoot. [Caterloopillar](/articles/caterloopilar/) takes another route: two moving reading heads construct one another, using still lifes and gliders to carry the instructions.

These articles follow the mechanisms and the search work needed to make the complete constructions function.

## Building the search tools

The [Simkin Glider Gun](/articles/simkin-glider-gun/) grew from a search for useful catalyst interactions. [LifeAPI](/articles/lifeapi/) and [CatForce](/articles/catforce/) made those searches practical; [B60](/articles/b60/) is one of the reactions they found. The smaller conduits and oscillators below are parts of the same experimental work.

[Switch-engine ping-pong](/articles/switch-engine-ping-pong/) is a different kind of construction: carefully spaced streams turn a spaceship-and-glider exchange into continuing growth. Its 23-cell seed held the quadratic-growth population record for more than seven years.

## Making Life physical

Later experiments explore Life through [printed still-life tiles](/articles/still-life-tiles/), [layers that encode an evolving Life step](/articles/life-in-3d-tiles/), and [simulated mechanical logic](/articles/multilayer-mutilated-gear/). They follow the pattern discoveries and search tools in the reading order below.

Work in other rules and neural local updates has its own [CA Research page](/interests/cellular-automata/).
