---
title: 'CGOL Virtual Museum'
description: 'An early browser-based museum prototype with live exhibits and unfinished pattern coverage.'
type: 'project'
topics: ['game-of-life', 'simulation-visualization']
status: 'ongoing'
visual: 'life'
featured: false
draft: true
date: '2026-10-12'
tags: ['Three.js', 'cellular automata', 'virtual museum']
github: 'https://github.com/simsim314/CGOL_Virtual_Museum'
sources:
  [
    {
      'label': 'Project README and documentation',
      'url': 'https://github.com/simsim314/CGOL_Virtual_Museum#readme',
    },
  ]
---

A pattern file is useful for simulation, but it does not provide much of a setting. The CGOL Virtual Museum explores that idea as a browser-based, first-person prototype. The museum content is unfinished.

## The prototype

The README describes themed rooms across Stages 0–3. Exhibits evolve with the B3/S23 rule rather than remaining static images. The main hall includes an animated glider sculpture and a museum map. Room labels outline a larger intended collection.

## What remains unfinished

The source catalog uses stand-in patterns for some advanced exhibits: the self-construction room displays an LWSS, and the panoramic Caterpillar wall is seeded with a Gosper gun. Those rooms do not yet demonstrate their named subjects. This is an early museum shell, not a completed historical collection.

## How it is built

The project is a static module site. Three.js supplies the 3D scene, with separate modules for room generation, the pattern library, Life simulation, and first-person interaction.

The rooms and exhibit catalogs are data-driven. The Life engine updates textures used by the exhibits, connecting the discrete simulation to its 3D presentation.

## Controls

The documented controls are WASD for movement, mouse look, and Shift to sprint. Press E to focus an exhibit, R to reset it, and Space to pause or resume all exhibits. Arrow keys adjust the focused exhibit's speed.

## Running the museum

The verified README gives a local run procedure: serve the repository with a static HTTP server, open the page, and click the canvas to lock the pointer. Three.js is imported from jsDelivr, so the module must be reachable.

No hosted museum URL is asserted here because the README does not link one. The repository is the starting point for inspecting the prototype and its unfinished catalog.
