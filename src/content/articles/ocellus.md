---
title: 'Ocellus'
description: 'A period-114 relay oscillator built around a reduced 180-degree reflector.'
type: 'research'
topics: ['game-of-life']
status: 'demonstrated'
showPreview: false
visual: 'life'
date: '2026-10-12'
tags: ['oscillator', 'p114', 'shared credit']
sources: [{ 'label': 'LifeWiki: Ocellus', 'url': 'https://conwaylife.com/wiki/Ocellus' }]
---

Ocellus is a **period-114 oscillator** credited to Noam Elkies and me in 2015. It uses my reduction of Elkies' 180-degree reflector.

## A relay construction

The 92-cell form documented on LifeWiki uses period-six thumbs to support a glider relay. Its state repeats after 114 generations. The construction belongs to a family that supports periods $90+24n$.

The reflector turns a glider back toward the other end of the relay. The supporting oscillator supplies the spark needed for that interaction.

## The credits and later work

The underlying reflector and its reduction are distinct contributions. Jeremy Tan subsequently found a glider synthesis for Ocellus on September 5, 2021.

Ocellus was once the smallest known period-114 oscillator. A different construction surpassed it in 2022, so that claim describes its history rather than a current record.

LifeWiki includes the pattern and explains the related reflector reactions supported by different sparkers.
