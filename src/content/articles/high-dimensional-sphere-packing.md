---
title: 'High-Dimensional Sphere Packing'
description: 'A candidate lattice-packing lower bound, and the public commitments recording the work.'
type: 'research'
topics: ['mathematics']
status: 'candidate'
showPreview: true
visual: 'packing'
featured: true
date: '2026-10-12'
tags: ['sphere packing', 'lattices', 'candidate proof']
github: 'https://github.com/simsim314/math-proof-commitments'
sources:
  [
    {
      'label': 'Lattice sphere-packing claim and commitments',
      'url': 'https://github.com/simsim314/math-proof-commitments/tree/main/lattice-sphere-packing',
    },
  ]
---

How densely can equal spheres be packed in a space with many dimensions? The public material for this work records a candidate improvement to a lower bound for **lattice** sphere packing. The manuscripts are private; the repository publishes cryptographic commitments to particular versions.

## The mathematical question

A lattice packing places sphere centers on a lattice in $\mathbb{R}^d$. Let $\Delta_d^L$ denote the greatest possible density of such a packing. A lower bound asserts that a packing with at least that density exists.

The public project description states the candidate claim

$$
\Delta_d^L \ge c\,d^2\log\log d\,2^{-d}
$$

for universal constants $c>0$ and $d_0$, and every integer $d\ge d_0$. This is the claim under investigation, rather than an established theorem presented by this website.

## The proposed progression

The repository describes a progression from $\kappa=1/(1+e)$, through constructions approaching $\kappa=1-\varepsilon$, to a candidate full $\kappa=1$ logarithmic gain. Here $\kappa$ refers to the exponent in $(\log\log d)^\kappa$.

The public description supplies the statement, but not the argument needed to assess it. There is therefore no proof walkthrough or claim of independent verification here.

## What is public

The initial public commitment is dated **September 11, 2026**. The project folder lists SHA-256 digests and OpenTimestamps files for a preprint, appendices, and a simplified construction. Those commitments identify exact versions of files without publishing their contents.

If an original is later disclosed, its hash can be compared with the commitment and its timestamp proof checked. This can establish a relationship to a committed version; it cannot establish that a mathematical argument is correct.

## Current status

This is **candidate mathematical work**. Later revisions may differ from the committed files. The public repository does not supply a released manuscript, a peer-review result, or an arXiv identifier.
