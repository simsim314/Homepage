---
title: 'Neural CA MNIST'
description: 'A 50-step neural digit refiner whose intermediate images carry the evolving state.'
type: 'project'
topics: ['artificial-intelligence']
status: 'experimental'
visual: 'neural'
featured: false
image: /images/neural-ca-evolution.gif
imageAlt: A hand-drawn digit input and the actual model outputs at steps 1, 10, 20, 35, and 50.
imageCredit: Actual outputs from the repository’s ONNX model on a synthetic hand-drawn input; an example, not a benchmark.
date: '2026-10-12'
tags: ['MNIST', 'local computation', 'ONNX', 'cellular automata']
github: 'https://github.com/simsim314/NeauralCA_MNIST'
demo: 'https://simsim314.github.io/NeauralCA_MNIST/'
demoNote: 'The ONNX model may take around 30 seconds to load. Wait for Ready before pressing Run.'
sources:
  [
    {
      'label': 'Project README and documentation',
      'url': 'https://github.com/simsim314/NeauralCA_MNIST#readme',
    },
  ]
---

This experiment processes a handwritten digit through 50 spatially local neural updates. Each step produces another 28×28 image, making the computation visible as a sequence rather than only a final label.

The [sequence on the homepage](/#article-neural-ca-mnist) was computed with the published ONNX model, using a synthetic hand-drawn 3 as input. It shows the actual images at steps 1, 10, 20, 35, and 50. It is one example of the evolving state, not an accuracy measurement.

## Images as state

The README describes no separate hidden state vector. At step $t$, the original input and previous output images are concatenated as channels. A local convolutional block produces the next image, squashed into $[0,1]$ by a sigmoid.

A schematic description is

$$
y_t=\sigma\!\left(f_t([x,y_1,\ldots,y_{t-1}])\right).
$$

The memory is the stack of produced images. The rule is step-specific: $f_1$ through $f_{50}$ are different learned updates.

## Why it is CA-like

The process operates through local neighborhoods and repeated grid updates. It differs from a classic cellular automaton because the updates are learned filters and the same rule is not repeated at every step.

The README specifies local processing with radius four. That locality describes an update; information can still propagate across multiple steps.

## What the demonstration shows

Draw a digit in the original app. The input is cropped, squared, and downscaled. The interface displays the 50 intermediate images, an animation, and a final digit verdict with a confidence score.

The verdict is a classifier's output. The documentation does not provide a benchmark here establishing a general recognition-accuracy claim.

## Training and inspection

The repository includes data preparation, training, local animation, and ONNX export scripts. The browser must load the ONNX model before Run becomes ready; the README suggests allowing roughly 30 seconds, though actual load time varies.
