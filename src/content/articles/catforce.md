---
title: 'CatForce'
description: 'Brute-force catalyst searches that test recovery without prescribing the interaction.'
type: 'project'
topics: ['game-of-life', 'programming-computing']
status: 'implemented'
visual: 'life'
featured: false
image: /images/catforce-combinations.gif
imageAlt: Animated enumeration of different block and beehive catalyst placements.
imageCredit: Illustrative enumeration of 24 still-life configurations; not outputs of a completed catalyst search.
date: '2026-10-12'
tags: ['C++', 'catalyst search', 'combinatorics']
github: 'https://github.com/simsim314/CatForce'
sources:
  [
    {
      'label': 'Project README and documentation',
      'url': 'https://github.com/simsim314/CatForce#readme',
    },
    {
      'label': 'p19 discovery report: Mitchell Riley and symmetric CatForce',
      'url': 'https://conwaylife.com/forums/viewtopic.php?p=172492',
    },
    { 'label': 'LifeWiki: Cribbage', 'url': 'https://conwaylife.com/wiki/Cribbage' },
  ]
---

CatForce is a catalyst-search utility built on [LifeAPI](/articles/lifeapi/). Its search strategy matches the idea behind my glider-gun work: place a small number of potential catalysts in a bounded area and test their combinations.

## A simple search condition

The important condition is that the catalysts return to their positions after the reaction and remain stable for the requested interval. The tool does not require them to remain intact throughout the reaction; they can be disturbed and later recovered.

That allows the search to find interactions without prescribing their internal sequence.

## Combinatorial search space

Each catalyst has possible positions and orientations. A configuration chooses one placement for every catalyst; the utility evolves that configuration and checks whether the catalysts recover.

If catalyst $i$ has $N_i$ candidate placements, the unconstrained configuration count is

$$
N_1\,N_2\,\cdots\,N_k.
$$

This is a description of the search space, not a runtime benchmark. Symmetry, bounding-box restrictions, and early rejection can reduce the configurations that need full evaluation.

## Configuring a run

An input file specifies the active pattern, candidate catalysts and their symmetries, a rectangular search area, generation limits, and stability conditions. Optional filters select desired outputs or reject unwanted interactions.

The README also describes combining candidate results and limiting catalyst arrangements by bounding width and height. The supplied `.in` files are the concrete examples for the configuration format.

## Finding the useful interactions

CatForce returns the interactions that might be useful within the configured search. I then go through the potential solutions **by hand**, inspect what happens, and select the best ones.

Finding a reaction that meets the search condition is one stage; understanding whether it does something useful is another. The search explores combinations quickly, while the next step is looking closely at the results.

## Implementation constraints

The utility uses brute-force spatial search, with optimizations and a structure amenable to parallelization. The bundled LifeAPI version uses a 64×64 torus with edge-glider removal. This describes the engine shipped with CatForce; boundary handling differs from the later standalone LifeAPI code.

Those constraints should be considered when interpreting any search output. A finite-domain reaction must still be checked in the intended Life setting.

## A custom version and the first p19

The tool also became a basis for other researchers' searches. Mitchell Riley found **Cribbage**, the first period-19 oscillator, on July 14, 2023 using his symmetric CatForce version. The discovery report explicitly credits Riley and identifies that custom search program.

This is a result found by Riley with a development of the tool, rather than a pattern discovery attributed to me. It illustrates the value of infrastructure that other researchers can extend.

## A discovery pipeline

The [Simkin glider gun](/articles/simkin-glider-gun/) article connects this utility to the discovery of its underlying catalyst interaction. CatForce is the reusable tool; the gun is one specific result.

The repository documents compilation with g++ and use of an input file passed to the executable. It supplies the code and search controls without claiming a current-machine performance benchmark here.
