---
title: 'LifeAPI'
description: 'A compact C++ library for manipulating, evolving, and searching Game of Life patterns.'
type: 'project'
topics: ['game-of-life', 'programming-computing']
status: 'implemented'
visual: 'life'
featured: false
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
  ]
---

A search needs to do more than evolve a pattern. It must place objects, vary their positions and phases, test for a target, and report what it found. LifeAPI gathers those operations into a C++ interface for Life searches.

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

Its documentation uses C-style function names and describes a C++ library. This article follows that technical description while preserving the original motivation for the tool.

## States, iterators, and targets

Life states can be parsed from RLE, moved, transformed, combined, and evolved. Iterators enumerate placements and phases without requiring the caller to write every nested loop.

Targets record both wanted live cells and surrounding dead cells. Testing a target is therefore more precise than checking only whether a set of live cells is present.

## The simulation domain

The documented implementation works on a **64×64 torus**, stored using 64 machine words. The coordinate convention runs from −32 to 31, with the Y direction matching Golly.

This domain matters: a finite torus is not the same as an infinite Life plane. The library also detects and removes gliders at its edges for the intended search use.

## Using it in a search

The README documents state operations, iterators, target matching, population counts, and RLE reporting. It is the practical reference for writing a search.

The purpose is comfortable search infrastructure with fast low-level operations. This article does not repeat a historical speed estimate as a benchmark on current machines.
