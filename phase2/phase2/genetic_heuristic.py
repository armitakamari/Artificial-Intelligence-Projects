
"""
Module: genetic_heuristic.py
Paradigm: Evolutionary Computing & Real-Valued Heuristic Search

Description:
    This agent implements an evolutionary approach to determine the optimal scalar weights 
    for evaluating immediate game states. Instead of relying on manually hand-tuned constants, 
    the agent models game strategies (e.g., banner acquisition velocity, tactical blocking, 
    house rarity, and board flexibility) as an artificial chromosome. This chromosome undergoes 
    stochastic evaluation to maximize immediate state transitions.

Research Significance:
    Demonstrates the application of parameter optimization over non-linear game heuristic 
    spaces. Serves as the evolutionary baseline for comparing static weight vectors against 
    iterative reinforcement learning agents.
"""


import copy
import random
from main import find_card, find_varys,make_move
from random_agent import get_valid_moves ,get_valid_jon_sandor_jaqan ,get_valid_ramsay

# Constants for genetic algorithm
POPULATION_SIZE = 20
MUTATION_RATE = 0.1
GENERATIONS = 50

def generate_chromosome():
    return {key: random.randint(1, 10) for key in ['banners', 'strategic', 'block', 'rare', 'cards', 'flexibility','companion']}
number_of_houses = {
    'Stark': 8, 'Greyjoy': 7, 'Lannister': 6,
    'Targaryen': 5, 'Baratheon': 4, 'Tyrell': 3, 'Tully': 2
}

def evaluate_move(cards, move, player, opponent, weights):
    # --- CRITICAL HEURISTIC EVALUATION ENGINE ---
    # Instead of hardcoding strategic preferences, we scale game features dynamically
    # using the evolved real-valued chromosome weights.
    
    
    score = 0
    simulated_cards = copy.deepcopy(cards)
    simulated_player = copy.deepcopy(player)
    simulated_opponent = copy.deepcopy(opponent)
    selected_house = make_move(simulated_cards, move, simulated_player)

    # [Strategic Weight Mapping]
    # Banners are prioritized to secure absolute point majorities
    score += weights['banners'] * sum(simulated_player.get_banners().values())
    # House counting evaluates house monopoly potential and blocking metrics
    house_counts = {house: sum(1 for card in simulated_cards if card.get_house() == house) for house in simulated_player.get_cards()}
    
    if selected_house in house_counts and house_counts[selected_house] == max(house_counts.values()):
        score += weights['strategic']
    if selected_house in opponent.get_cards() and len(opponent.get_cards()[selected_house]) >= 2:
        score += weights['block']
    
    collected_cards = len(simulated_player.get_cards().get(selected_house, []))
    score += weights['cards'] * collected_cards
    
    if house_counts.get(selected_house, 0) <= 2:
        score += weights['rare']
    
    varys_row, varys_col = divmod(find_varys(simulated_cards), 6)
    if 1 <= varys_row <= 4 and 1 <= varys_col <= 4:
        score += weights['flexibility']
        
    if house_counts.get(selected_house, 0)==number_of_houses[selected_house]:
        score+= weights['companion']
        

    return score

def fitness_function(weights, cards, player1, player2):
    """Calculates the fitness of heuristic weights."""
    valid_moves = get_valid_moves(cards)
    return sum(evaluate_move(cards, move, player1, player2, weights) for move in valid_moves) / (len(valid_moves) or 1)

def crossover(parent1, parent2):
    """Performs crossover between two parents."""
    return {key: random.choice([parent1[key], parent2[key]]) for key in parent1}
def mutate(chromosome):
    """Mutates a chromosome with a small probability."""
    for key in chromosome:
        if random.random() < MUTATION_RATE:
            chromosome[key] = random.randint(1, 10)
    return chromosome

def evolve_weights(cards, player1, player2):
    """Runs the evolutionary algorithm to optimize heuristic weights."""
    population = [generate_chromosome() for _ in range(POPULATION_SIZE)] 

    for _ in range(GENERATIONS):
        fitness_scores = [(chrom, fitness_function(chrom, cards, player1, player2)) for chrom in population]
        fitness_scores.sort(key=lambda x: x[1], reverse=True)
        
        top_half = [chrom for chrom, _ in fitness_scores[:POPULATION_SIZE // 2]]
        next_generation = [mutate(crossover(random.choice(top_half), random.choice(top_half))) for _ in range(POPULATION_SIZE)]
        population = next_generation

    return max(population, key=lambda chrom: fitness_function(chrom, cards, player1, player2))

def make_best_move(cards, player1, player2, optimized_weights=None):
    if optimized_weights is None:
        optimized_weights = evolve_weights(cards, player1, player2)

    valid_moves = get_valid_moves(cards)
    return max(valid_moves, key=lambda move: evaluate_move(cards, move, player1, player2, optimized_weights))

def get_move(cards, player1, player2, companion_cards, choose_companion):

    trained_agent_weights = evolve_weights(cards, player1, player2)

    if choose_companion:
        # If companion is chosen, choose a random companion card
        if companion_cards:
            selected_companion = random.choice(list(companion_cards.keys()))  # Randomly select a companion card
            move = [selected_companion]  # Add the companion card to the move list
            choices = companion_cards[selected_companion]['Choice']  # Get the number of choices required by the companion card

            # Logic for companion card with choices
            if choices == 1:  # For cards like Jon Snow
                move.append(random.choice(get_valid_jon_sandor_jaqan(cards)))

            elif choices == 2:  # For cards like Ramsay
                valid_moves = get_valid_ramsay(cards)

                if len(valid_moves) >= 2:
                    move.extend(random.sample(valid_moves, 2))  # Choose two random moves
                else:
                    move.extend(valid_moves)  # If fewer than 2, use available moves

            elif choices == 3:  # Special case for Jaqen with additional companion card selection
                valid_moves = get_valid_jon_sandor_jaqan(cards)

                if len(valid_moves) >= 2 and companion_cards:
                    move.extend(random.sample(valid_moves, 2))  # Choose two random valid moves
                    move.append(random.choice(list(companion_cards.keys())))  # Add another random companion card
                else:
                    move.extend(valid_moves)  # If not enough valid moves, just return what is possible
                    move.append(random.choice(list(companion_cards.keys())) if companion_cards else None)
            
            return move  # Return the companion-based move
    
        else:
            return []  # If no companion cards, return empty list for no action
    
    else:
        # Regular move logic if no companion is chosen
        return make_best_move(cards, player1, player2, trained_agent_weights)