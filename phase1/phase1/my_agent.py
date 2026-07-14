import copy
from main import find_card,find_varys,make_move
from random_agent import get_valid_moves


# Define heuristic weights for each game stage
weights = {
    'early': {'banners': 5, 'strategic': 4, 'block': 2, 'rare': 3, 'cards': 3, 'flexibility': 2},
    'mid': {'banners': 4, 'strategic': 3, 'block': 3, 'rare': 4, 'cards': 2, 'flexibility': 2},
    'late': {'banners': 6, 'strategic': 2, 'block': 5, 'rare': 2, 'cards': 1, 'flexibility': 1},
}

def determine_game_stage(cards, player1, player2):
    '''
    Determines the current stage of the game.

    Parameters:
        cards (list): List of Card objects on the board.
        player1 (Player): The first player.
        player2 (Player): The second player.

    Returns:
        stage (str): The game stage ('early', 'mid', 'late').
    '''
    remaining_cards = len(cards)
    total_banners = sum(player1.get_banners().values()) + sum(player2.get_banners().values())
    valid_moves = len(get_valid_moves(cards))

    # Determine stage based on indicators
    if remaining_cards > 24 and total_banners <= 2 and valid_moves > 10:
        return 'early'
    elif 12 < remaining_cards <= 24 or (2 < total_banners <= 5) or (5 < valid_moves <= 10):
        return 'mid'
    else:
        return 'late'

def evaluate_move(cards, move, player, opponent, stage):
    '''
    Evaluates a potential move based on multiple heuristics, weighted by game stage.

    Parameters:
        cards (list): List of Card objects.
        move (int): Location of the potential move.
        player (Player): The current player making the move.
        opponent (Player): The opponent player.
        stage (str): The current game stage ('early', 'mid', 'late').

    Returns:
        score (float): The overall score for the move.
    '''
    # Retrieve weights for the current stage
    weight = weights[stage]

    # Initialize score
    score = 0

    # Simulate the move
    simulated_cards = copy.deepcopy(cards)
    simulated_player = copy.deepcopy(player)
    simulated_opponent = copy.deepcopy(opponent)
    selected_house = make_move(simulated_cards, move, simulated_player)

    # Heuristic 1: Maximize Banners Controlled
    banners_controlled = sum(simulated_player.get_banners().values())
    score += weight['banners'] * banners_controlled

    # Heuristic 2: Target Strategic Houses
    house_counts = {house: sum(1 for card in simulated_cards if card.get_house() == house)
                    for house in simulated_player.get_cards()}
    max_house = max(house_counts, key=house_counts.get, default=None)
    if selected_house == max_house:
        score += weight['strategic']

    # Heuristic 3: Block Opponent’s Opportunities
    opponent_house_counts = opponent.get_cards()
    if selected_house in opponent_house_counts and len(opponent_house_counts[selected_house]) >= 2:
        score += weight['block']

    # Heuristic 4: Maximize Cards Collected in One Move
    collected_cards = len(simulated_player.get_cards()[selected_house])
    score += weight['cards'] * collected_cards

    # Heuristic 5: Prioritize Rare Houses
    if house_counts[selected_house] <= 2:
        score += weight['rare']

    # Heuristic 7: Maintain Flexibility for Future Moves
    varys_location = find_varys(simulated_cards)
    varys_row, varys_col = varys_location // 6, varys_location % 6
    if 1 <= varys_row <= 4 and 1 <= varys_col <= 4:
        score += weight['flexibility']

    return score

def minimax(cards, player1, player2, depth, alpha, beta, maximizing_player, stage):
    '''
    Implements the Minimax algorithm with alpha-beta pruning.

    Parameters:
        cards (list): List of Card objects representing the board.
        player1 (Player): The agent's player object.
        player2 (Player): The opponent's player object.
        depth (int): The depth limit for recursion.
        alpha (float): The best value that the maximizing player can guarantee.
        beta (float): The best value that the minimizing player can guarantee.
        maximizing_player (bool): True if it's the agent's turn; False otherwise.
        stage (str): The current stage of the game ('early', 'mid', 'late').

    Returns:
        best_score (float): The best score for the current player.
        best_move (int): The best move leading to the best score.
    '''
    # Base case: depth limit or no valid moves
    valid_moves = get_valid_moves(cards)
    if depth == 0 or not valid_moves:
        return sum(evaluate_move(cards, move, player1, player2, stage) for move in valid_moves) / (len(valid_moves) or 1), None

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None

        for move in valid_moves:
            simulated_cards = copy.deepcopy(cards)
            simulated_player = copy.deepcopy(player1)
            simulated_opponent = copy.deepcopy(player2)
            make_move(simulated_cards, move, simulated_player)

            eval_score, _ = minimax(simulated_cards, simulated_player, simulated_opponent, depth - 1, alpha, beta, False, stage)

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move

            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break

        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None

        for move in valid_moves:
            simulated_cards = copy.deepcopy(cards)
            simulated_player = copy.deepcopy(player2)
            simulated_opponent = copy.deepcopy(player1)
            make_move(simulated_cards, move, simulated_player)

            eval_score, _ = minimax(simulated_cards, simulated_opponent, simulated_player, depth - 1, alpha, beta, True, stage)

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move

            beta = min(beta, eval_score)
            if beta <= alpha:
                break

        return min_eval, best_move

def get_move(cards, player1, player2):
    '''
    Gets the best move for the player using the Minimax algorithm.

    Parameters:
        cards (list): List of Card objects representing the board.
        player1 (Player): The agent's player object.
        player2 (Player): The opponent's player object.

    Returns:
        best_move (int): The best move for the player.
    '''
    stage = determine_game_stage(cards, player1, player2)

    # Set depth limit based on the stage
    depth = {'early': 2, 'mid': 3, 'late': 4}[stage]

    _, best_move = minimax(cards, player1, player2, depth, float('-inf'), float('inf'), True, stage)

    return best_move


