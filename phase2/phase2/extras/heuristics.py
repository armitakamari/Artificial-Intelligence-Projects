# Heuristic functions

def h_banner_gain(cards, player, move):
    """Evaluate if a move adds to our banners."""
    score = len(player.get_banners())
    make_move(cards, player, move, None, False)
    score -= len(player.get_banners())
    return score

def h_house_priority(house):
    """Prioritize certain houses based on predefined ranking."""
    return number_of_houses[house]

def h_secure_banner(player, selected_house):
    """Determine if a banner is secure based on cards from the selected house."""
    return len(player.get_cards().get(selected_house, [])) > number_of_houses[selected_house] // 2

def h_opp_house(opp, house):
    """Compare the number of cards the opponent has in a specific house."""
    return len(opp.get_cards().get(house, []))

def h_next_move(opp,weights, cards, player, move,companion_cards,choose_companion):
    """Evaluate how a move will affect the opponent's next move."""
    simulated_cards = copy.deepcopy(cards)
    simulated_player = copy.deepcopy(player)
    simulated_opponent = copy.deepcopy(opp)
    make_move(simulated_cards, move, simulated_player)
    evaluate_comp(move, weights, cards, simulated_player, simulated_opponent, companion_cards, choose_companion)
    
    

def h_house_loc(house, cards):
    """Evaluate if all the cards of a house are in the most common location (row or column)."""
    # Get all locations of the house's cards
    locations = [card.location for card in cards.get(house, [])]
    if not locations:
        return None 
    
    # Split the location into row and column
    rows = [loc[0] for loc in locations if isinstance(loc, tuple)]
    cols = [loc[1] for loc in locations if isinstance(loc, tuple)]
    
    most_common_row = Counter(rows).most_common(1)
    most_common_col = Counter(cols).most_common(1)
    
    return (most_common_row[0][0] if most_common_row else None,
            most_common_col[0][0] if most_common_col else None)

def h_companion(player, companion):
    """Evaluate if the companion card is useful (e.g., last card in the house)."""
    return companion.is_last_in_house() 

def h_winning_state(player, opp, w):
    """Evaluate if the player is ahead based on banners."""
    diff = len(player.get_banners()) - len(opp.get_banners())
    return w * diff if get_winner(player, opp) == 1 else -diff * w


# Initialize weights randomly for each heuristic
def initialize_weights():
    """Initialize weights randomly for each heuristic."""
    return {key: random.uniform(0, 1) for key in HEURISTIC_KEYS}



def h_house_loc(house, cards):
    """Evaluate if all the cards of a house are in the most common location (row or column)."""
    # Get all locations of the house's cards
    locations = [card.location for card in cards.get(house, [])]
    if not locations:
        return None 
    
    # Split the location into row and column
    rows = [loc[0] for loc in locations if isinstance(loc, tuple)]
    cols = [loc[1] for loc in locations if isinstance(loc, tuple)]
    
    most_common_row = Counter(rows).most_common(1)
    most_common_col = Counter(cols).most_common(1)
    
    return (most_common_row[0][0] if most_common_row else None,
            most_common_col[0][0] if most_common_col else None)