---
title: 'Geminoid Particles'
description: 'A custom nine-state cellular automaton for exploring construction and self-destruction.'
type: research
topics: [cellular-automata, programming-computing]
presentationOrder: -65
status: demonstrated
showPreview: true
imageSource: https://conwaylife.com/forums/viewtopic.php?p=11513#p11513
imageCredit: 'Original GeminoidParticles pattern evolved in Golly, generations 0–49,152. Both ends and the instruction tape share one timeline. End views follow successive heads; the whole-pattern overview compresses the tape vertically. Colored marks are enlarged actual cells.'
imageAlt: 'Both ends of Geminoid Particles build their next heads, then remove old circuitry, while the long instruction tape winds between them.'
image: /images/geminoid-particles-whole.gif
date: 2026-10-12
updated: 2026-10-13
tags: [GeminoidParticles, universal constructor, self-construction, self-destruction, Golly]
sources:
  - label: My rule and working construction, April 6, 2014
    url: https://conwaylife.com/forums/viewtopic.php?p=11513#p11513
  - label: Author interview, October 13, 2026
---

## A rule for designing constructions

On April 6, 2014, I introduced GeminoidParticles as a design environment for self-construction. Rather than search a complicated rule for useful reactions, I designed explicit particles and building blocks so the circuitry could be explored directly in Golly.

The immediate problem was self-destruction for my [Serizawa construction](/articles/serizawa-geminoid/). An earlier, roughly twenty-state experiment had helped with construction; this revision used nine states and made deletion easier to investigate.

It was the next step in an interest that began with reading about Andrew Wade’s original Gemini. Serizawa Geminoid was an early result; Geminoid Particles let me explore the construction technique in a rule I controlled. Years later, I used that same technique for [Remini](/articles/remini/) in Conway’s Life.

## The mechanism

Three particle types push, pull, or reflect a construction block. Other objects redirect or duplicate signals. Collisions between particles create temporary reflectors, permanent reflectors, or construction blocks. These operations provide the building vocabulary for a universal constructor.

## The working Geminoid

The main animation includes **both ends and the tape between them**. It runs to **generation 49,152**, continuing beyond the start of the second head: both ends complete their new circuitry, the old machinery is removed, and construction continues. The changing heads and tape routes make the whole pattern move like a snake.

The left overview compresses the tape vertically so its full extent fits. The two end views share the same generation and preserve the local geometry while following successive heads. Colored marks are enlarged actual cells from the full Golly simulation.

The instruction particles control the arms by pushing, pulling, and redirecting construction blocks. These are the simple operations behind the more elaborate sequence of building a head, transferring the instructions, and removing the old circuitry.

<details>
<summary>A closer view of the first head being constructed</summary>

![Two arms complete the first new Geminoid Particles head and remove the old circuitry.](/images/geminoid-particles-building.gif)

This first-end detail runs through generation 24,576. The main animation above also shows the lower end and the instruction tape.

</details>

The released pattern has period **18,092**. Two opposing constructors share the instruction streams to build the next machinery, with circuitry that destroys the old machinery. The thread includes the rule table and complete pattern.

This was a working demonstration, not an optimized construction. Shorter periods were proposals. Its purpose was to make construction, timing, and destruction easier to reason about before tackling more demanding rules. See also [Remini](/articles/remini/).
