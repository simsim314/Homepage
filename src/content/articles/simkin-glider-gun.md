---
title: 'Simkin Glider Gun'
description: 'The 29-cell gun: the smallest known by live-cell population when two glider output streams are allowed.'
type: 'research'
topics: ['game-of-life']
status: 'demonstrated'
showPreview: true
visual: 'life'
featured: true
homepageHero: true
image: /images/simkin-glider-gun.gif
imageAlt: Animated B3/S23 simulation of the 29-cell Simkin glider gun.
imageCredit: Exact B3/S23 simulation, rendered for this site from the documented pattern.
date: '2026-10-12'
tags: ['cellular automata', 'catalyst search', 'glider gun']
github: 'https://github.com/simsim314/CatForce'
sources:
  [
    {
      'label': 'LifeWiki: pattern, date, and construction',
      'url': 'https://conwaylife.com/wiki/Simkin_glider_gun',
    },
    {
      'label': 'CatForce search documentation',
      'url': 'https://github.com/simsim314/CatForce#readme',
    },
  ]
---

The starting point was a concern about the search tools themselves. I thought the older tools were too complex and might contain bugs. I wanted something simpler: place a few potential catalysts, then search their combinations.

That required infrastructure before it required a discovery. I built LifeAPI to make the search fast enough, and CatForce to do the combinatorial search. Three blocks were a particularly simple fit for a small search area.

## From the search to the pattern

A catalyst is a pattern that participates in a reaction and eventually returns to its original state. CatForce checks this recovery without requiring every catalyst to remain intact throughout the interaction.

The search produced the interaction that became one half of the gun. I posted it on the forum and continued posting results from the run. While that was happening, Scorbie recognized the full gun construction.

## How the gun works

The pattern runs a Herschel around a loop formed by two B60 conduits. Each conduit advances the reaction by 60 generations. The complete loop repeats after 120 generations and emits gliders.

**When two glider output streams are allowed, the 29-cell Simkin gun is the smallest known gun by live-cell population.** This is a population record, rather than a bounding-box record. [LifeWiki documents the record and both forms](https://conwaylife.com/wiki/Simkin_glider_gun).

Adding an eater to suppress one output gives a 36-cell single-barrelled form, tying the Gosper glider gun’s population. The [animation above](#glider-gun) shows the 29-cell pattern under the ordinary B3/S23 Life rule. Play/Pause, Step, Reset, and speed controls let you inspect the reaction; gliders leave the finite display at its edges.

## Discovery and attribution

LifeWiki attributes the discovery to Michael Simkin on **April 28, 2015**, using CatForce. The work also involved a community discussion about credit for the catalyst interaction and for recognizing the gun.

My view is that finding the interaction was the difficult part and deserves discovery attribution. At the same time, I see the question of credit for Scorbie's contribution as a real dilemma, and I would not dismiss it easily. I leave the community's naming and attribution decisions to the community.

## The tools behind it

The pattern and the infrastructure belong together. [CatForce](/articles/catforce/) describes the search approach; [LifeAPI](/articles/lifeapi/) describes the operations that made it practical.
