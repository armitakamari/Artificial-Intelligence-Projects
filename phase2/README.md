# Hand of the King AI Agent (Phase 2) - Evolutionary Approach

This repository contains the second phase of the "Hand of the King" AI project. While Phase 1 focused on adversarial search (Minimax), Phase 2 shifts the paradigm toward **Evolutionary Computing** and **Real-Valued Heuristic Optimization**.

 ## Contributors
     **Armita Kamari** 
     **Mehrsa Samizadeh** 

## Paradigm Shift: Genetic Heuristics
Instead of manually tuning the importance of game factors, this agent uses a **Genetic Algorithm (GA)** to evolve the optimal scalar weights for its decision-making engine.

### Core Features
*   **Stochastic Optimization:** The agent models game strategies (banners, strategic blocking, house rarity, etc.) as an artificial **Chromosome**.
*   **Adaptive Learning:** Through iterative generations, the agent evolves these weights to maximize the fitness score, which is calculated based on immediate state transitions and move quality.
*   **Companion Logic:** Integrated handling for special companion cards (Jon Snow, Ramsay, Jaqen, etc.) with automated selection logic.

## Evolutionary Mechanism
The optimization process follows these GA steps:
1.  **Population Initialization:** Generates a diverse set of 20 random chromosomes.
2.  **Fitness Evaluation:** Uses a specialized function to score each weight-set based on its performance in simulated moves.
3.  **Selection & Crossover:** Combines the best-performing chromosomes to produce the next generation.
4.  **Mutation:** Introduces stochastic variations (10% rate) to prevent local optima and explore the heuristic space.
5.  **Evolution:** Runs for 50 generations to converge on a highly optimized weight vector.

## Project Structure
Based on the Phase 2 implementation:
- `genetic_heuristic.py`: The core evolutionary engine containing the GA, chromosome definitions, and fitness evaluation.
- `main.py`: The central game loop and environment manager.
- `random_agent.py`: Baseline agent used for move validation and comparative testing.
- `assets/`: Graphical assets for the game interface.
- `boards/`: Pre-defined board configurations for various test scenarios.
- `extras/`: Additional scripts, logs, or experimental data.
- `utils/`: Common helper functions for game state and card management.

## How to Run
1.  Ensure you have `pygame` installed:
```bash
pip install pygame

