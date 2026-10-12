---
title: 'Switch engine ping-pong'
description: 'A 23-cell seed that generates quadratic growth through repeated spaceship interactions.'
type: 'research'
topics: ['game-of-life']
status: 'demonstrated'
showPreview: false
visual: 'life'
date: '2026-10-12'
tags: ['quadratic growth', 'breeder', 'switch engine']
sources:
  [
    {
      'label': 'LifeWiki: Switch engine ping-pong',
      'url': 'https://conwaylife.com/wiki/Switch_engine_ping-pong',
    },
  ]
---

Switch engine ping-pong starts with just **23 live cells**, yet its population grows quadratically. I found it on October 29, 2014. LifeWiki records it as the first quadratic-growth pattern using only two switch engines.

## The repeated interaction

The initial seed includes gliders, an R-pentomino, an R-pentomino predecessor, and a pre-block. Their interactions produce two parallel switch engines and a middleweight spaceship. The spaceship repeatedly collides with the engines, producing further switch engines traveling in another direction.

This is a breeder: the evolving pattern keeps making additional growing components. Quadratic growth describes its long-term population, rather than a large initial pattern.

## A historical record

At discovery, its 23-cell seed was the smallest known quadratic-growth pattern. It followed my [25-cell](/articles/25-cell-quadratic-growth/) and [24-cell](/articles/24-cell-quadratic-growth/) discoveries earlier that month. Smaller 22-, 21-, and 20-cell patterns superseded it in 2022.

LifeWiki includes the pattern file and the original discovery discussion. The name describes the repeating spaceship interaction; it does not imply a different cellular-automaton rule.
