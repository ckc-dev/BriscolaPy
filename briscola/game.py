"""
The classic Mediterranean trick-taking game. Now in your terminal.

This program simulates a game of Briscola between a number of players, ranging
from 2 to 4, including CPU players.
"""

import argparse
import random

from card import Card, get_winning_card
from player import Player

# Game options.
MIN_NUMBER_OF_PLAYERS = 2
MAX_NUMBER_OF_PLAYERS = 4
CARDS_PER_PLAYER = 3

# Argument parsing options.
PARSER = argparse.ArgumentParser(description=__doc__)
PARSER.add_argument(
    'players',
    metavar='Player names.',
    type=str,
    nargs='*',
    help='A list of names for players.'
)
PARSER.add_argument(
    '-c',
    '--cpu',
    metavar='CPU player names.',
    type=str,
    nargs='+',
    help='A list of names for CPU players.'
)
PARSER.add_argument(
    '-v',
    '--verbose',
    action='store_true',
    help='Show detailed information about what is happening.'
)

args = PARSER.parse_args()

# Set verbosity on classes.
Card.verbose = args.verbose
Player.verbose = args.verbose

# Limit number of players and initialize a list of those.
player_names = args.players
cpu_player_names = args.cpu
number_of_players = 0

if player_names:
    number_of_players += len(player_names)
if cpu_player_names:
    number_of_players += len(cpu_player_names)

try:
    assert MIN_NUMBER_OF_PLAYERS <= number_of_players <= MAX_NUMBER_OF_PLAYERS
except AssertionError:
    print("Number of players must be between"
          + f" {MIN_NUMBER_OF_PLAYERS} and {MAX_NUMBER_OF_PLAYERS}.")
    quit()

players = []
if player_names:
    players.extend([Player(name, False) for name in player_names])
if cpu_player_names:
    players.extend([Player(name, True) for name in cpu_player_names])

# Generate and shuffle a deck of `Card`s.
# Cards use the following format: `"NAME": (POINTS, PRIORITY)`, where `POINTS`
# is the number of points that go to players, and `PRIORITY` is the card
# priority, used to compare cards and decide which should win a round.
CARDS = {
    "1": (11, 9),
    "2": (0,  0),
    "3": (10, 8),
    "4": (0,  1),
    "5": (0,  2),
    "6": (0,  3),
    "7": (0,  4),
    "F": (2,  5),  # Fante.
    "C": (3,  6),  # Cavallo.
    "R": (4,  7),  # Re.
}
SUITS = [
    "BASTONI",
    "COPPE",
    "DENARI",
    "SPADE",
]
DECK = [Card(name, suit, points, priority)
        for suit in SUITS for name, (points, priority) in CARDS.items()]
random.shuffle(DECK)

# Remove some cards from the deck if there are three players, as per the rules
# of the game.
if number_of_players == 3:
    DECK = [c for c in DECK if c.name != "2"]

# Deal players' hands.
for player in players:
    for _ in range(CARDS_PER_PLAYER):
        card = DECK.pop(0)
        card.owner = player
        player.hand.append(card)

# Pick a lead - or briscola - card, then put it back on the end of the deck.
lead_card = DECK.pop(0)
DECK.append(lead_card)

# For the first round, the order of players is random.
random.shuffle(players)

# Initialize the number of cards on players' hands and in total.
hand_card_count = number_of_players * CARDS_PER_PLAYER
total_card_count = len(DECK) + hand_card_count

# As long as there are cards available, play rounds.
round = 1
while total_card_count:
    # Reset round variables.
    secondary_lead = None
    hand_card_count = 0
    played_cards = []

    # Print round information.
    print()
    print(f"Starting round {round}!")

    if args.verbose:
        print(f"Total cards: {total_card_count}"
              + f" | Deck: {len(DECK)}"
              + f" | Hands: {hand_card_count}")
        print("Player order: " + ", ".join(str(p) for p in players))

    print(f"Lead card: {lead_card}")
    print()

    # Each player plays a turn.
    for player in players:
        # Print turn information.
        print(f"It's {player}'s turn!")

        player_cards = ", ".join([str(c) for c in player.hand])

        if args.verbose:
            if secondary_lead:
                print(f"Secondary lead card: {secondary_lead}")

            print(f"{player} has no cards left." if not player_cards else
                  f"{player}'s cards: {player_cards}")
        elif not player.is_cpu:
            print(f"Cards: {player_cards}")

        # Play a card.
        played_card = None
        if player.is_cpu:
            played_card = player.play_card()
        else:
            while not played_card:
                try:
                    index = int(input("Pick a card (use 1,2,3...): ")) - 1
                    played_card = player.play_card(index)
                except (IndexError, ValueError):
                    print("Invalid value.")

        # Append played card to list of player cards.
        played_cards.append(played_card)

        # Pick the first card played on this round as a secondary lead card,
        # which is used instead of the main lead card if none of the played
        # cards matched with it.
        if player == players[0]:
            secondary_lead = played_card

        # If this player is a CPU, print to the user which card was picked.
        if player.is_cpu:
            print(f"{player} plays a {played_card}!")

    # Pick this round's winner, add the cards played this round to their stack.
    round_winner = get_winning_card(
        played_cards, lead_card, secondary_lead).owner
    round_winner.add_cards_to_stack(played_cards)
    print(f"{round_winner} wins this round!")

    # Reorder the player list so that this round's winner is the first to pick
    # a card and play the next round.
    winner_index = players.index(round_winner)
    new_player_order = players[winner_index:]
    new_player_order.extend(players[:winner_index])
    players = new_player_order

    # Each player picks a card, until there are no more cards in the deck.
    # Then, the total number of cards in player's hands is updated.
    for player in players:
        if len(DECK) > 0:
            card = DECK.pop(0)
            player.pick_card(card)

            if args.verbose:
                print(f"{player} picks a {card}!")

        hand_card_count += len(player.hand)

    # Update the total number of cards and add one to the round counter.
    total_card_count = len(DECK) + hand_card_count
    round += 1

# Once the game is done, pick the overall game winner.
game_winner = max(players, key=lambda player: player.points)
print(f"\n{game_winner} wins the game with {game_winner.points} points!")
