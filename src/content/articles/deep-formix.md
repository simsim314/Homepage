---
title: 'Deep-Formix'
description: 'Uniting two GPU chess codebases with deep NNUE evaluation and 32 position-dependent models.'
type: 'project'
topics: ['chess', 'artificial-intelligence', 'programming-computing']
status: 'implemented'
visual: 'neural'
featured: true
image: /images/deep-formix-gpu.png
imageAlt: Conceptual illustration of a chess knight on a GPU chip with parallel circuit paths.
imageCredit: AI-generated editorial illustration of GPU chess computation; not an actual hardware photograph.
date: '2026-10-12'
tags: ['CUDA', 'NNUE', 'neural evaluation']
github: 'https://github.com/simsim314/Deep-Formix'
sources:
  [
    {
      'label': 'Project README and documentation',
      'url': 'https://github.com/simsim314/Deep-Formix#readme',
    },
  ]
---

Deep-Formix brings two existing GPU chess approaches together and adds a new evaluation architecture. The integration is a central contribution: fast GPU move generation, a GPU engine framework, and a deep NNUE model become parts of the same engine.

The work also investigates how much chess evaluation can be carried by a learned model rather than a long search. It combines C++/CUDA engine code with Python training tools.

## The main idea

The README describes a 12-layer NNUE architecture with 32×32 layers and skip connections. It uses 32 model buckets selected by piece count, pawn count, and the presence of queens.

Instead of using one evaluation model across all positions, the bucket scheme chooses a model suited to the material configuration. The project is inspired by searchless chess, while the engine also includes search code.

## Implementation

The move generator refactors [GPU Perft](https://github.com/ankan-ban/perft_gpu), while the engine structure and minimax implementation draw on [Chess-Engine-GPU](https://github.com/dkozykowski/Chess-Engine-GPU). The project brings those components together and adds its deep evaluation architecture, new evaluation and position classes, and model training and conversion pipeline. The repository documents a UCI interface, PyTorch training and testing scripts, and conversion to the binary model used by C++.

The README identifies the upstream sources. Those links matter for understanding both the architecture and its provenance.

## Reported results

The author reports that searchless evaluation plays within approximately 40 Elo of Stockfish at one ply. That is a **repository-reported comparison**, not an independently reproduced benchmark by this website. It should not be read as a claim of parity with full-strength Stockfish.

The documentation also reports training on a searchless dataset and a multi-day training run on an RTX 3080 Ti. The practical result here is an engine and training experiment; strength depends on the model, hardware, and evaluation setup.

## Inspect the experiment

Start with the source and training documentation. There is no verified hosted demo linked in the README. The repository also flags uncertainty around the licensing of derivative portions, which should be checked there before redistribution.
