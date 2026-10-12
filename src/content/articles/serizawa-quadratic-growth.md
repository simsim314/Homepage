---
title: 'Serizawa quadratic growth'
description: 'Five-cell and later four-cell seeds with quadratic growth, posted in June 2014.'
type: research
topics: [other-cellular-automata]
status: demonstrated
showPreview: false
date: 2026-10-12
tags: [Serizawa, quadratic growth, small seeds]
sources:
  - label: Five-cell seed, June 3, 2014
    url: https://conwaylife.com/forums/viewtopic.php?p=12135#p12135
  - label: Clear four-cell example, June 4, 2014
    url: https://conwaylife.com/forums/viewtopic.php?p=12152#p12152
  - label: Search discussion with Dave Greene
    url: https://conwaylife.com/forums/viewtopic.php?p=12151#p12151
---

I posted a **five-cell quadratic-growth seed in Serizawa on June 3, 2014**. The following day, after discussing smaller candidates with Dave Greene, I posted a clear four-cell example.

## The five-cell seed

The original multistate RLE is:

```text
x = 0, y = 0, rule = Serizawa
B2$3.B2$B15$52.AB!
```

It contains five non-background cells. The original header uses zero dimensions; the cell data extends beyond them.

## Four cells

The later example is:

```text
x = 125, y = 18, rule = Serizawa
A13$121.B2$124.B2$121.B!
```

## Why the search needed care

Some candidates took millions of generations to reveal new behavior. In the discussion, I noted that my earlier 8,000-generation search horizon had missed late interactions.

The result concerns population growth from a small seed. It is distinct from the engineered [Serizawa Geminoid](/articles/serizawa-geminoid/), whose circuitry interprets construction instructions.

These are historical discoveries, with the original configurations supplied in the linked posts.
