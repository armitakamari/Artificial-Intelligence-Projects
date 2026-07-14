# Hand of the King AI Agent (Phase 1)

This repository contains the implementation of an intelligent game agent for the "Hand of the King" board game, developed as part of an Artificial Intelligence course project. The agent is designed to control Varys and maximize the collection of valuable character cards and family flags.

## Project Team
*   **Armita Kamari**  
*   **Mehrsa Samizadeh**  

## Key Features & Implementation

The agent utilizes a sophisticated decision-making engine based on the following techniques:

### 1. Minimax Algorithm with Alpha-Beta Pruning
To ensure efficient decision-making within the game tree, the agent implements the **Minimax** algorithm optimized with **Alpha-Beta Pruning**. This significantly reduces the search space, allowing the agent to look ahead more effectively.

### 2. Dynamic Heuristic Evaluation
Instead of static scoring, the agent uses **Stage-Aware Heuristics**. It analyzes the game state and determines the current phase (**Early, Mid, or Late** game) to adjust its strategy dynamically:
- **Weights Adjustment:** The importance of factors like `banners`, `strategic houses`, `blocking`, and `rare cards` changes based on the game stage.
- **Adaptive Depth:** The search depth is adjusted dynamically based on the game stage to balance performance and strategic foresight.

### 3. Strategy Factors
The agent’s evaluation function considers multiple factors including Banner Control, Opponent Blocking, and Maintaining Move Flexibility.

## Project Structure

- `my_agent.py`: The core logic containing the Minimax algorithm and heuristic functions.
- `main.py`: The main entry point to run the game environment.
- `assets/`: Directory containing game graphical assets.
- `boards/`: Directory containing pre-defined game board configurations.
- `utils/`: Helper functions for game state management and move validation.

## How to Run
1. Ensure `pygame` is installed: `pip install pygame`
2. Run the game:
```bash
   python main.py
   

