---
title: 'Serizawa Geminoid'
description: 'One of my first construction results: a smaller, more efficient Geminoid design in Serizawa, following my interest in Andrew Wade’s Gemini.'
type: research
topics: [cellular-automata]
presentationOrder: -70
status: demonstrated
showPreview: true
imageSource: https://conwaylife.com/forums/viewtopic.php?p=11354#p11354
imageCredit: 'Original Serizawa pattern evolved in Golly, generations 0–25,165,824. Synchronized views of both ends and the instruction tape. End views follow successive heads; the whole-pattern overview compresses the tape vertically. Actual cells are enlarged for readability.'
imageAlt: 'Both ends of Serizawa Geminoid build their next heads while the instruction tape joins them into a moving chain. The animation continues until both new heads have their completed circuitry.'
image: /images/serizawa-geminoid-whole.gif
date: 2026-10-12
updated: 2026-10-13
tags: [Serizawa, self-construction, Geminoid, universal constructor]
sources:
  - label: Original construction announcement, March 23, 2014
    url: https://conwaylife.com/forums/viewtopic.php?p=11354#p11354
  - label: Construction and terminology discussion
    url: https://conwaylife.com/forums/viewtopic.php?t=1346
  - label: Andrew Wade’s original Gemini announcement
    url: https://conwaylife.com/forums/viewtopic.php?t=399
  - label: Author interview, October 13, 2026
---

On March 23, 2014, I posted a working universal-constructor-based pattern in Serizawa. The announcement presented it as the first explicit working example of this kind in the rule, with an attached pattern and a Golly construction script.

## Where my interest began

My interest in Conway’s Game of Life began with an article about **Andrew Wade’s original Gemini**, the self-constructing spaceship announced in 2010. Serizawa Geminoid was one of my first results after that introduction: I applied those construction ideas in another rule, making a much smaller, more efficient design.

This became a continuing line of work. I later built [Geminoid Particles](/articles/geminoid-particles/) to explore construction and self-destruction in a rule of my own. Much later, I used the same construction technique in [Remini](/articles/remini/), bringing it back into Conway’s Life with period-30 circuitry.

## Construction encoded in signals

The animation shows **both ends**, including the lower end that a close-up of the first head leaves out. Each end builds its next head. The long instruction tape joins them, and the successive heads and changing routes give the construction its snake-like appearance.

The left panel shows the whole pattern with the tape’s height compressed. The two larger panels show the upper and lower ends at the same generation, following successive heads. The run continues to **generation 25,165,824**, beyond the first completed head so the other end can finish its circuitry too. Enlarged marks make the actual cells readable.

The tape supplies recipes to the construction arms: **push and pull** reposition their targets, and **shoot** sends a construction signal toward the new circuitry. The animation uses the complete original pattern in Golly; the end panels are views of that full simulation.

<details>
<summary>A closer view of the first two-arm construction</summary>

![The two arms build the first new Serizawa head.](/images/serizawa-geminoid-building.gif)

This closer view covers generations 0–16,777,216. It isolates the first end; the main animation above also includes the other end and the tape.

</details>

The reported cycle takes **13,362,290 generations**, with a construction step of $(2444,3219)$. Glider streams encode instructions for construction arms that build the next circuitry.

The significance is applying Geminoid construction principles outside Conway’s Life, using Serizawa's own signals and reactions.

## What “Geminoid” means here

I called the pattern a Geminoid and later described it as a linear self-replicator. Dave Greene distinguished it from a self-cleaning spaceship: the released construction leaves old circuitry behind and carries one copy of its instruction stream forward.

The thread therefore also describes it as a **self-constructing puffer**. Construction, copying the instruction stream, and destroying old machinery are separate tasks.

## Connections

The discussion developed construction-arm recipes and explored transferring ideas between Serizawa and Life. This transfer between rules is the thread connecting Serizawa Geminoid, Geminoid Particles, and Remini. See also [Serizawa quadratic growth](/articles/serizawa-quadratic-growth/).
