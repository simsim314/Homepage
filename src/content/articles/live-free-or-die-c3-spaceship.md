---
title: 'The c/3 spaceship in Live Free or Die'
description: 'A prize-winning period-six spaceship at a previously undiscovered speed in B2/S0.'
type: research
topics: [cellular-automata]
presentationOrder: -50
status: demonstrated
showPreview: true
imageSource: https://conwaylife.com/forums/viewtopic.php?p=13652#p13652
imageCredit: 'Golly HashLife evolution of my original October 5, 2014 spaceship, generations 0–60. Individual cells are shown; the loop returns to the initial position.'
imageAlt: 'The original period-six c/3 spaceship moving through the Live Free or Die rule B2/S0.'
image: /images/lfod-c3-spaceship.gif
date: 2026-10-12
tags: [B2/S0, Live Free or Die, spaceship, c/3, prize]
sources:
  - label: Original spaceship discovery, October 5, 2014
    url: https://conwaylife.com/forums/viewtopic.php?p=13652#p13652
  - label: Luke Bradford’s prize announcement
    url: https://conwaylife.com/forums/viewtopic.php?p=12513#p12513
  - label: My later challenge linking the prize-winning ship
    url: https://conwaylife.com/forums/viewtopic.php?p=13814#p13814
---

On October 5, 2014, I posted the first known **c/3, period-six spaceship in Live Free or Die**, the rule B2/S0.

## A very simple rule

A dead cell becomes alive with exactly two live neighbours. A live cell survives only when it has no live neighbours. Those are the birth and survival conditions represented by B2/S0.

The rule differs from Conway’s Life, B3/S23. Its patterns must be evolved under the correct rule.

## A new speed

The ship translates two cells every six generations:

$$
\frac{2c}{6}=\frac{c}{3}.
$$

The discovery post supplies its complete RLE. The forum subsequently discussed trimming the tail and extensions of the ship.

## The prize

Luke Bradford had offered a cash bounty for a spaceship at a previously undiscovered speed. My later challenge post explicitly links this ship as the solution that won the award.

I subsequently offered prize money toward another cellular-automaton challenge: a loop with universal construction and internal computation.

The original announcement and follow-up posts document both the pattern and its place in the challenge history.
