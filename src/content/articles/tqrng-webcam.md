---
title: 'TQRNG Webcam'
description: 'An experiment extracting bits from webcam pixel noise, with partial validation of its physical model.'
type: 'project'
topics: ['experimental-engineering']
status: 'experimental'
showPreview: true
visual: 'neural'
featured: false
date: '2026-10-12'
tags: ['sensor noise', 'randomness', 'webcam']
github: 'https://github.com/simsim314/TQRNG_WebCam'
demo: 'https://simsim314.github.io/TQRNG_WebCam/'
demoNote: 'Load the original project on demand, or open it in a separate tab.'
sources:
  [
    {
      'label': 'Project README and documentation',
      'url': 'https://github.com/simsim314/TQRNG_WebCam#readme',
    },
  ]
---

Can an ordinary webcam provide a useful physical source of random bits? This project includes Python and JavaScript libraries that combine least significant bits from batches of RGB pixels.

The repository calls the project a True Quantum Random Generator. Its own notes also describe only partial success in establishing the scientific model. This article preserves that distinction.

## The extraction idea

The libraries XOR low-order bits across pixel channels and batches. The motivation is to reduce bias while collecting sensor variation into an output bitstream. The browser demo exposes bit generation, integers, floating-point values, sampling, and shuffling.

## The physical investigation

The author describes recordings and simulations aimed at estimating photon counts from pixel statistics, fitting distributions, and studying bias. The repository includes calibration and test code alongside the usable library.

Its proposed photon-noise explanation depends on the sensor and recording conditions. An XOR operation alone does not establish that the resulting bits are independent, quantum-origin, or suitable for cryptographic use.

## What is demonstrated

The project supplies code to read webcam frames and extract an output stream. The README provides a throughput estimate for a 640×480, 30 fps input, rather than a portable benchmark for arbitrary webcams.

The theoretical bias estimates are author-reported modeling claims. This site does not present them as independently validated properties of the output.

## Try the experiment

Open the original demo in a separate tab. Camera access begins with its Start RNG control and browser permission. Keeping it outside an iframe avoids requesting access from this site and gives the original app room for its controls.

For closer inspection, read the library and the measurement scripts rather than relying solely on how random the displayed numbers look.
