# Artificial Intelligence Projects - Hand of the King

This repository contains a two-phase implementation of an intelligent agent for the "Hand of the King" board game, developed for the Artificial Intelligence course. The project explores different AI paradigms, from adversarial search to evolutionary optimization.

## Project Overview

The goal of this project was to design an autonomous agent capable of playing "Hand of the King" strategically. The project was divided into two distinct phases, each focusing on a different AI methodology.

### Phase 1: Adversarial Search (Minimax)
In the first phase, our primary objective was to implement a decision-making engine based on classical AI search algorithms.
- **Core Task:** Developing the `my_agent.py` which utilizes the **Minimax Algorithm** enhanced with **Alpha-Beta Pruning**.
- **Key Feature:** Implementation of stage-aware heuristics and dynamic search depth to handle the game's complexity efficiently.

### Phase 2: Evolutionary Computing (Genetic Algorithm)
The second phase shifted the focus toward automated parameter optimization and heuristic evolution.
- **Core Task:** Developing the `genetic_heuristic.py` which implements an **Evolutionary Approach** to find optimal heuristic weights.
- **Key Feature:** Using a **Genetic Algorithm** (Population, Crossover, Mutation) to evolve a "chromosome" of scalar weights, replacing hand-tuned constants with evolved strategic parameters.

## Repository Structure

- `phase1/`: Contains the Minimax-based agent and Phase 1 documentation.
- `phase2/`: Contains the Genetic Algorithm-based agent and Phase 2 documentation.
- `assets/`: Game graphical assets and resources.

## Project Team
- **Armita Kamari**
- **Mehrsa Samiezadeh**

---
*University Project - Artificial Intelligence Course*
