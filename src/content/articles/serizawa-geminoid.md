---
title: 'Serizawa Geminoid'
description: 'A working universal-constructor-based self-construction in Serizawa, announced in March 2014.'
type: research
topics: [other-cellular-automata]
status: demonstrated
showPreview: false
date: 2026-10-12
tags: [Serizawa, self-construction, Geminoid, universal constructor]
sources:
  - label: Original construction announcement, March 23, 2014
    url: https://conwaylife.com/forums/viewtopic.php?p=11354#p11354
  - label: Construction and terminology discussion
    url: https://conwaylife.com/forums/viewtopic.php?t=1346
---

On March 23, 2014, I posted a working universal-constructor-based pattern in Serizawa. The announcement presented it as the first explicit working example of this kind in the rule, with an attached pattern and a Golly construction script.

## Construction encoded in signals

The reported cycle takes **13,362,290 generations**, with a construction step of $(2444,3219)$. Glider streams encode instructions for construction arms that build the next circuitry.

The significance is applying Geminoid construction principles outside Conway’s Life, using Serizawa's own signals and reactions.

## What “Geminoid” means here

I called the pattern a Geminoid and later described it as a linear self-replicator. Dave Greene distinguished it from a self-cleaning spaceship: the released construction leaves old circuitry behind and carries one copy of its instruction stream forward.

The thread therefore also describes it as a **self-constructing puffer**. Construction, copying the instruction stream, and destroying old machinery are separate tasks.

## Connections

The discussion developed construction-arm recipes and explored transferring ideas between Serizawa and Life. See also [Remini](/articles/remini/) and [Serizawa quadratic growth](/articles/serizawa-quadratic-growth/).
