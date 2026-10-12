---
title: 'Multilayer Mutilated Gear'
description: 'A simulation of layered, selectively toothed gears as a representation of logic.'
type: 'project'
topics: ['simulation-visualization', 'experimental-engineering']
status: 'experimental'
visual: 'gear'
featured: false
image: /images/gear-3d.gif
imageAlt: Animated three-dimensional view of the multilayer mutilated gear simulation.
date: '2026-10-12'
tags: ['mechanical logic', 'simulation', 'gears']
github: 'https://github.com/simsim314/Multilayer-Mutilated-Gear'
sources:
  [
    {
      'label': 'Project README and documentation',
      'url': 'https://github.com/simsim314/Multilayer-Mutilated-Gear#readme',
    },
    {
      'label': 'Forum: mechanical logic, staged folding, delayed wires, and OR gates',
      'url': 'https://conwaylife.com/forums/viewtopic.php?p=205731',
    },
  ]
---

A mutilated gear has some teeth present and others missing. This project models a multilayer arrangement in which the tooth pattern becomes part of a computational structure.

## The idea

Each layer can encode a different pattern of present and absent teeth. A grid of these components is intended to represent logic. The repository presents the mechanism through a simulation and animated examples.

The work is a software model of a mechanical idea. It does not establish that a physical machine has been fabricated or tested.

## Implemented exploration tools

The README provides two Python entry points: `main.py` opens the user interface, and `grid_editor.py` opens the grid examples. The source includes the model and its visualization.

## Demonstrated examples

The repository supplies animations labeled **Wire** and **OR Gates**. They show the intended behavior of particular simulated configurations.

![Animated wire example from the gear project's documentation.](/images/gear-wire.gif)

![Animated OR-gate example from the gear project's documentation.](/images/gear-or.gif)

## Developments in the forum

The forum record adds work beyond the short README. In July 2024 I reported a binary adder and a grid emulator, with full Life or Rule 110 logic still unfinished. The broader motivation was mechanical computation where electronics may be impractical.

In December 2024 I proposed independently rotating stages on each rod and a folding argument to trade width for depth. The stated transformation was

$$
(2W)\times H\times D\quad\longrightarrow\quad(W+S)\times H\times(2D+S),
$$

where $S$ is the number of stages. This is a proposed construction argument in the forum, not a measured physical build.

A February 2025 animation demonstrated a delayed wire, addressing the timing needed for logic gates. The March update added the grid UI/editor and OR-gate examples with different timing arrangements. These are simulation developments; a complete mechanical Life machine remained a goal.

## Scope and next questions

These examples are a starting point for investigating information propagation and logic in the model. Physical tolerances, manufacturing, and measured hardware reliability are outside the demonstrated repository material.

Start with the documented Python interface and compare the grid arrangements with the animations. No performance or universality result is claimed here.
