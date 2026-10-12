---
title: 'CryptoCash'
description: 'An NFC bearer-token proposal, explored through AES circuits and witness-generation experiments.'
type: 'project'
topics: ['cryptography']
status: 'experimental'
visual: 'crypto'
featured: false
date: '2026-10-12'
tags: ['NFC', 'Circom', 'zero knowledge']
github: 'https://github.com/simsim314/CryptoCash'
image: '/images/cryptocash.png'
imageAlt: 'Concept illustration of a physical CryptoCash token from the project README.'
sources:
  [
    {
      'label': 'Project README and documentation',
      'url': 'https://github.com/simsim314/CryptoCash#readme',
    },
  ]
---

CryptoCash asks how a physical NFC token might be authenticated publicly when its chip uses a symmetric AES secret. The repository combines that proposed system with a smaller, implemented circuit experiment.

## The problem

The proposed hardware is the NTAG 424 DNA. Its authentication workflow uses a secret AES key and read-specific data. In a conventional symmetric system, checking a message authentication code requires access to the secret.

The project investigates whether circuit-based proofs could help connect that hardware behavior to public verification.

## The circuit experiment

The supplied workflow generates a key and valid/invalid test inputs, writes an AES circuit with the key embedded, compiles it with Circom, and runs witness generation. A Python verifier script inspects the output for the two cases.

In schematic form, the experiment checks a relationship of the form

$$
\mathrm{mac}=\operatorname{AES}_{k}(\mathrm{data}).
$$

This describes the circuit test. It is not a complete specification of the NFC chip's deployed authentication protocol.

## What is implemented

The documentation supports **circuit compilation and witness generation**. It explicitly says that installing the AES key on the NFC chip is not implemented, and that a full ZK-SNARK system requires further setup and proof-generation work.

Witness calculation is not, by itself, a complete public zero-knowledge verification system. The project description's broader claims about a trustless bearer asset remain proposals.

## Open questions

The README discusses key deletion, a public verifier called `F_key`, minting, and smart-contract backing. This site does not assert that embedding a key in public circuit artifacts makes it unrecoverable. Those security properties need a concrete protocol and analysis beyond the demonstrated workflow.

The useful starting point is the actual experiment: follow the scripts, inspect the circuit, and distinguish its outputs from the proposed monetary system.
