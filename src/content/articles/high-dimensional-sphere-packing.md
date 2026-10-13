---
title: 'High-Dimensional Sphere Packing'
description: 'From a simple question and an AI-directed search to a collaborative preprint on lattice packing in every sufficiently large dimension.'
type: research
topics: [mathematics]
presentationOrder: -75
status: preprint
showPreview: true
visual: packing
featured: true
date: 2026-10-12
tags: [sphere packing, lattices, AI-assisted mathematics, cyclotomic gluing]
github: https://github.com/simsim314/math-proof-commitments
sources:
  - label: Gargava–Gröbner–Simkin, A cyclotomic gluing construction for lattice sphere packings
    url: https://arxiv.org/abs/2610.12619
  - label: The preprint and its AI-assisted development statement
    url: https://arxiv.org/html/2610.12619v1
  - label: Abuya–Gargava–Zhao, Stochastically evolving ellipsoids with symmetries
    url: https://arxiv.org/abs/2606.05105
  - label: Boaz Klartag’s stochastic ellipsoid paper
    url: https://arxiv.org/abs/2504.05042
  - label: Nihar Gargava’s research page
    url: https://nihargargava.com/
  - label: My September 2026 proof commitments
    url: https://github.com/simsim314/math-proof-commitments/tree/main/lattice-sphere-packing
---

## A simple question with difficult mathematics

What drew me to sphere packing was the simplicity of the problem. It is easy to explain, even in high dimensions: how densely can equal spheres fit without overlapping? Like many problems in number theory, the question is simple and the mathematics behind it is complex.

I first tried small-dimensional **kissing problems**—how many equal spheres can touch one central sphere without overlapping each other. I soon realized that I could not easily improve on the known results. I also wanted a mathematical result, rather than just a numerical solution. That led me toward large dimensions.

## Setting a direction for AI

I saw a promising direction in bringing together Boaz Klartag’s ellipsoid approach and the logarithmic gain in the work of Abuya–Gargava–Zhao, or AGZ. The goal was to extend that gain beyond the sparse dimensions covered by AGZ.

AI did the heavy lifting in the mathematical exploration. My role was to supervise it and keep it focused on the target. I do not want to describe this as a proof I worked out unaided.

## From an AI argument to human mathematics

Once AI had produced a proposed proof, I tried to have it validated independently. My mathematical skills are well below what this paper requires, so my own reading could not settle its correctness.

I contacted **Nihar Gargava**, a postdoctoral researcher at Université Paris-Saclay. He was willing to help with validation and guide the collaboration with **Matthias Gröbner**, who reworked the argument into a form accessible to human mathematicians.

The preprint’s development statement distinguishes the initial, weaker AI-assisted argument from the stronger result developed during the collaboration. Gargava and Gröbner checked and revised the mathematics and helped rebuild the exposition. The paper is jointly authored by **Nihar Gargava, Matthias Gröbner, and Michael Simkin**.

## What the preprint proves

Let $\Delta_d^L$ be the supremum of lattice sphere-packing densities in $\mathbb{R}^d$. The preprint establishes universal constants $c>0$ and $d_0$ such that, for **every integer** $d\ge d_0$,

$$
\Delta_d^L \ge c\,d^2\log\log d\,2^{-d}.
$$

Klartag’s method supplies the $d^2$ gain. AGZ combined stochastic ellipsoids with cyclotomic symmetry to obtain the additional $\log\log d$ factor along an infinite, sparse sequence of dimensions. The new construction extends that factor to every sufficiently large dimension.

The key is gluing several cyclotomic components together. A direct product leaves troublesome vectors confined to only a few components. Gluing imposes arithmetic conditions on those vectors, allowing the symmetry gain to survive the combination. The full argument is in the [preprint](https://arxiv.org/abs/2610.12619).

## The public record

_A cyclotomic gluing construction for lattice sphere packings_ was posted to arXiv on **October 8, 2026**. It is a research preprint.

Before that, I recorded cryptographic commitments to versions of the work on **September 11, 2026**. Those identify earlier manuscripts; the public preprint now provides the mathematical argument itself.
