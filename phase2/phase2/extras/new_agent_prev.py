import copy
import random
from main import  find_varys,make_move,make_companion_move
from random_agent import get_valid_moves ,get_valid_jon_sandor_jaqan ,get_valid_ramsay

# Constants for genetic algorithm
POPULATION_SIZE = 20
MUTATION_RATE = 0.1
GENERATIONS = 50

def generate_chromosome():
    return {key: random.randint(1, 10) for key in ['banners', 'strategic', 'block', 'rare', 'cards', 'flexibility','companion']}

def evaluate_move_heuristics(simulated_cards, selected_house, simulated_player, opponent, weights):
    score = 0
    
    # banners heuristic
    score += weights['banners'] * sum(simulated_player.get_banners().values())
    
    # house count heuristic
    house_counts = {house: sum(1 for card in simulated_cards if card.get_house() == house) for house in simulated_player.get_cards()}
    
    # strategic heuristic
    if selected_house in house_counts and house_counts[selected_house] == max(house_counts.values()):
        score += weights['strategic']
    
    # block heuristic
    if selected_house in opponent.get_cards() and len(opponent.get_cards().get(selected_house, [])) >= 2:
        score += weights['block']
    
    # cards collected heuristic
    collected_cards = len(simulated_player.get_cards().get(selected_house, []))
    score += weights['cards'] * collected_cards
    
    # rare house heuristic
    if house_counts.get(selected_house, 0) <= 2:
        score += weights['rare']
    
    # flexibility heuristic
    varys_row, varys_col = divmod(find_varys(simulated_cards), 6)
    if 1 <= varys_row <= 4 and 1 <= varys_col <= 4:
        score += weights['flexibility']
    
    return score


def evaluate_move(cards, move, player, opponent, weights, companion_cards=None):
    score = 0
    score1 = 0
    score2 = 0
    simulated_cards = copy.deepcopy(cards)
    simulated_player = copy.deepcopy(player)
    simulated_opponent = copy.deepcopy(opponent)

    if companion_cards and move[0] in companion_cards:
        score1 += evaluate_move_heuristics(simulated_cards, selected_house, simulated_player, simulated_opponent, weights)
        selected_house = make_companion_move(simulated_cards, companion_cards, move, simulated_player)
        score2 += evaluate_move_heuristics(simulated_cards, selected_house, simulated_player, simulated_opponent, weights)
    else:
        selected_house = make_move(simulated_cards, move, simulated_player)
        score += evaluate_move_heuristics(simulated_cards, selected_house, simulated_player, simulated_opponent, weights)

    # Call the new function for heuristics calculation
    #score += evaluate_move_heuristics(simulated_cards, selected_house, simulated_player, simulated_opponent, weights)

    # Companion Move Evaluation
    if companion_cards and move[0] in companion_cards:
        companion = move[0]
        choices = companion_cards[companion]['Choice']

        if choices == 1:  # Jon Snow, Sandor, Jaqen (single choice)
            valid_moves = get_valid_jon_sandor_jaqan(simulated_cards)
            if valid_moves:
                score += max(evaluate_move(simulated_cards, [companion, m], simulated_player, simulated_opponent, weights) for m in valid_moves)

        elif choices == 2:  # Ramsay (two choices)
            valid_moves = get_valid_ramsay(simulated_cards)
            if len(valid_moves) >= 2:
                move_combinations = [(m1, m2) for m1 in valid_moves for m2 in valid_moves if m1 != m2]
                score += max(evaluate_move(simulated_cards, [companion, m1, m2], simulated_player, simulated_opponent, weights) for m1, m2 in move_combinations)

        elif choices == 3:  # Jaqen (double move + another companion)
            valid_moves = get_valid_jon_sandor_jaqan(simulated_cards)
            if len(valid_moves) >= 2 and companion_cards:
                move_combinations = [(m1, m2) for m1 in valid_moves for m2 in valid_moves if m1 != m2]
                score += max(
                    evaluate_move(simulated_cards, [companion, m1, m2, random.choice(list(companion_cards.keys()))], simulated_player, simulated_opponent, weights)
                    for m1, m2 in move_combinations
                )

    return score



def fitness_function(weights, cards, player1, player2):
    """fitness of heuristic weights."""
    valid_moves = get_valid_moves(cards)
    return sum(evaluate_move(cards, move, player1, player2, weights) for move in valid_moves) / (len(valid_moves) or 1)

def crossover(parent1, parent2):
    """crossover between two parents."""
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
    # Train heuristic weights
    trained_agent_weights = evolve_weights(cards, player1, player2)

    if choose_companion and companion_cards:
        best_companion_move = None
        best_score = float('-inf')

        for companion in companion_cards.keys():
            choices = companion_cards[companion]['Choice']
            move = [companion]

            if choices == 1:
                valid_moves = get_valid_jon_sandor_jaqan(cards)
                if valid_moves:
                    print("valid_moves =", valid_moves)
                    best_submove = max(valid_moves, key=lambda m: evaluate_move(cards, [companion, m], player1, player2, trained_agent_weights, companion_cards))
                    move.append(best_submove)

            elif choices == 2:
                valid_moves = get_valid_ramsay(cards)
                if len(valid_moves) >= 2:
                    best_pair = max(
                        [(m1, m2) for m1 in valid_moves for m2 in valid_moves if m1 != m2],
                        key=lambda pair: evaluate_move(cards, [companion, pair[0], pair[1]], player1, player2, trained_agent_weights, companion_cards),
                        default=(None, None)
                    )
                    move.extend(best_pair)

            elif choices == 3:
                valid_moves = get_valid_jon_sandor_jaqan(cards)
                if len(valid_moves) >= 2:
                    best_pair = max(
                        [(m1, m2) for m1 in valid_moves for m2 in valid_moves if m1 != m2],
                        key=lambda pair: evaluate_move(cards, [companion, pair[0], pair[1]], player1, player2, trained_agent_weights, companion_cards),
                        default=(None, None)
                    )
                    move.extend(best_pair)
                    if companion_cards:
                        move.append(random.choice(list(companion_cards.keys())))

            score = evaluate_move(cards, move, player1, player2, trained_agent_weights, companion_cards)
            if score > best_score:
                best_score = score
                best_companion_move = move

        return best_companion_move if best_companion_move else []

    else:
        return make_best_move(cards, player1, player2, trained_agent_weights)
