---
title: 'LifeAPI'
description: 'Optimized 64×64, bit-packed Game of Life evolution, with the operations needed for combinatorial searches.'
type: 'project'
topics: ['game-of-life', 'programming-computing']
presentationOrder: -95
status: 'implemented'
visual: 'life'
featured: true
image: /images/lifeapi-code.png
imageAlt: A syntax-colored LifeAPI code example initializing and evolving a glider.
imageCredit: Static rendering of a documented API example, with no editor interface or scrollbar.
date: '2026-10-12'
tags: ['C++', 'cellular automata', 'catalyst search']
github: 'https://github.com/simsim314/LifeAPI'
sources:
  [
    {
      'label': 'Project README and documentation',
      'url': 'https://github.com/simsim314/LifeAPI#readme',
    },
    {
      'label': 'LifeAPI.h: the bitwise evolution kernel',
      'url': 'https://github.com/simsim314/LifeAPI/blob/master/LifeAPI.h#L1176',
    },
  ]
---

LifeAPI’s core is a **64×64 Game of Life evolution engine**, packing the grid into 64 machine words. The optimized, C-style code works on many cells at once through bitwise operations. Around that engine are the operations needed to place patterns, enumerate combinations, test reactions, and report discoveries.

I built it because my searches needed faster evolution than the Golly-based approach I was using. [CatForce](/articles/catforce/) then used that infrastructure to explore catalyst combinations.

The goal was a small, simple, fast engine for search utilities that test many possible configurations. A compact grid is enough for many of those searches, so I focused the implementation on that job.

## Evolving 64 cells at a time

The important idea is that **Boolean operations encode the Life rule itself**. The optimization is in how the rule is evaluated over the packed grid, not just in an interface around a cell-by-cell simulation.

Each column is stored as a `uint64_t`: one bit per cell. Shifts align neighbouring cells, and Boolean operations accumulate neighbour-count masks across an entire column. The Life rule is applied through those masks instead of visiting every cell and counting its neighbours individually.

The kernel’s final selection is:

```cpp
return ~sum2 & sum1 & (temp | sum0);
```

This selects births with three neighbours and survival with two or three. The engine also tracks the active column range, avoiding work across the whole grid when the pattern occupies only a small part of it. Its layout is designed to let the compiler vectorize the loops.

The fixed grid is a deliberate constraint: it supports compact reaction searches, rather than being a general simulation of an unbounded Life universe.

## A small example

These documented operations initialize a state, load an RLE glider, evolve it, and print the result. This is an illustrative use of the API, rather than a screenshot of a search result.

```cpp
#include "LifeAPI.h"

int main() {
    New();
    char glider[] = "bo$2bo$3o!";
    PutState(glider);
    Run(4);
    PrintRLE();
}
```

## The role of the library

I built the infrastructure because I wanted a simple combinatorial search that ran fast enough to be practical. The resulting library provides the operations used by tools such as [CatForce](/articles/catforce/).

The header uses C-style structures and functions, with C++ overloading for convenient calls. It requires a C++ compiler; the low-level work remains bitwise evolution and pattern operations.

## States, iterators, and targets

Life states can be parsed from RLE, moved, transformed, combined, and evolved. Iterators enumerate placements and phases without requiring the caller to write every nested loop.

Targets record both wanted live cells and surrounding dead cells. Testing a target is therefore more precise than checking only whether a set of live cells is present.

## The simulation domain

The states have a **64×64 grid**, stored using 64 machine words. The coordinate convention runs from −32 to 31, with the Y direction matching Golly.

This domain matters: the engine is not an infinite Life plane. The library also detects and removes gliders at its edges for the intended search use.

## Using it in a search

The README documents state operations, iterators, target matching, population counts, and RLE reporting. It is the practical reference for writing a search.

The purpose is comfortable search infrastructure with fast low-level operations. This article does not repeat a historical speed estimate as a benchmark on current machines.
