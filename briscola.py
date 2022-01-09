"""
The classic Mediterranean trick-taking game. Now in your terminal.

This program simulates a game of Briscola between a number of CPU players,
ranging from 2 to 4.
"""

import random
import sys

MIN_NUMBER_OF_PLAYERS = 2
MAX_NUMBER_OF_PLAYERS = 4
CARDS_PER_PLAYER = 3
CARDS = {
    "1": 11,
    "2": 0,
    "3": 10,
    "4": 0,
    "5": 0,
    "6": 0,
    "7": 0,
    "F": 2,
    "C": 3,
    "R": 4
}
SUITS = [
    "BASTONI",
    "COPPE",
    "DENARI",
    "SPADE"
]


class Player:
    """Defines a player object."""

    def __init__(self):
        """Initialize instance."""
        self.name = ""
        self.hand = []   # Player's hand of cards.
        self.stack = []  # Player's stack of won cards.
        self.points = 0

    def play_card(self):
        """
        Play a card.

        Removes a random card from the player's hand, prints and returns it.

        Returns:
            Card: Played card.
        """
        card = self.hand.pop(self.hand.index(random.choice(self.hand)))

        print(f"{self} plays a {card}!")

        return card

    def pick_card(self):
        """
        Pick a card from the deck.

        Picks a card from the deck, sets the player to be it's owner, adds it
        to the player's hand, and prints it.
        """
        card = DECK.pop(0)
        card.owner = self

        self.hand.append(card)
        print(f"{self} picks a {card}!")

    def print_cards(self):
        """Print the cards on the player's hand."""
        print(f"{self} has no cards left." if self.hand == 0 else
              f"{self}'s cards: " + ", ".join([str(c) for c in self.hand]))

    def declare_round_victory(self):
        """Print a message declaring the player won this round."""
        print(f"{self} wins this round!")

    def add_cards_to_stack(self, cards):
        """
        Add a list of cards to the player's stack.

        Adds a list of cards to the player's stack of won cards, then adds the
        points for those cards to the player's points.

        Args:
            cards (Card): List of cards.
        """
        self.stack.extend(cards)

        self.points += sum(c.points for c in cards)

    def __str__(self):
        """Define string representation of an instance."""
        return f"[{self.points}] {self.name}"


class Card:
    """Defines a card object."""

    def __init__(self, name, suit, value):
        """Initialize instance."""
        self.name = name
        self.suit = suit
        self.points = value
        self.value = 0
        self.owner = None

        if self.name == "1":
            self.value == self.points
        else:
            try:
                self.value = int(self.name)
            except ValueError:
                self.value = self.points

    def __str__(self):
        """Define string representation of an instance."""
        return f"{self.name} of {self.suit.lower()} ({self.points})"


def max_card(cards):
    """
    Get the max card from a list of cards.

    Returns the card with the highest number of points from a list of cards.
    If more than one card has that number of points then the card with the
    highest value among those is returned.

    Args:
        cards (Card): List of cards to get max card from.

    Returns:
        Card: Max card.
    """
    max_points_card = max(cards, key=lambda card: card.points)
    cards = [c for c in cards if c.points == max_points_card.points]

    if len(cards) > 1:
        max_value_card = max(cards, key=lambda card: card.value)
        cards = [c for c in cards if c.value == max_value_card.value]

    return cards[0]


def winning_card(cards, lead_card, secondary_lead=None):
    """
    Get a round's winning card.

    Returns the winning card of a round, by checking for cards in a list of
    cards played this round that match either the lead card suit, or, if no
    card matches it, the secondary lead card suit. If no card matches it
    either, then it is chosen as the winner.

    If at any point, multiple cards match, then the card with the highest value
    is chosen.

    Args:
        cards (Card): List of cards played on a round.
        lead_card (Card): Lead - or briscola - card.
        secondary_lead (Card, optional): Secondary lead card. Defaults to None.

    Returns:
        Card: Winner card.
    """
    matches = [c for c in cards if c.suit == lead_card.suit]

    # Since the secondary lead card is the first card to played on a round, and
    # thus, part of the list of cards, there will always be a winning card, by
    # recursively running this function and passing the secondary lead card as
    # the lead card. I.e., If no card matches either the lead card or the
    # secondary lead card, the secondary lead card will still match itself, and
    # be chosen as the winner.
    return max_card(matches) if matches else winning_card(cards, secondary_lead)


# Initialize and limit the number of players.
number_of_players = int(sys.argv[1])
assert MIN_NUMBER_OF_PLAYERS <= number_of_players <= MAX_NUMBER_OF_PLAYERS

# Generate a list of players.
players = [Player() for _ in range(number_of_players)]
for i, player in enumerate(players, 1):
    player.name = input(f"Player {i} name: ")

# Generate and shuffle a deck of cards.
DECK = [Card(n, s, p) for s in SUITS for n, p in CARDS.items()]
random.shuffle(DECK)

# Remove some cards from the deck if there are three players, as per the rules
# of the game.
if number_of_players == 3:
    DECK = [c for c in DECK if c.name != "2"]

# Deal plyers' hands.
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
    # Print round information.
    print()
    print(f"Starting round {round}!")
    print(f"Total cards: {total_card_count}"
          + f" | Deck: {len(DECK)}"
          + f" | Hands: {hand_card_count}")
    print(f"Lead card: {lead_card}")
    print("Player order: " + ", ".join(str(p) for p in players))
    print()

    # Reset the number of cards on players' hands and the list of cards played
    # on this round.
    hand_card_count = 0
    played_cards = []

    # Each player plays a card, which gets added to this round's played cards.
    for player in players:
        print(f"It's {player.name}'s turn!")
        card = player.play_card()
        played_cards.append(card)
        player.print_cards()

    # Pick the first card played on this round as a secondary lead card, which
    # is used instead of the main lead card if none of the played cards matched
    # with it.
    secondary_lead = played_cards[0]
    print(f"Secondary lead card: {secondary_lead}")

    # Pick this round's winner, add the cards played this round to their stack,
    # and make them declare a victory.
    round_winner = winning_card(played_cards, lead_card, secondary_lead).owner
    round_winner.add_cards_to_stack(played_cards)
    round_winner.declare_round_victory()

    # Reorder the player list so that this round's winner picks a card and
    # plays the next round first.
    winner_index = players.index(round_winner)
    new_player_order = players[winner_index:]
    new_player_order.extend(players[:winner_index])
    players = new_player_order

    # Each player picks a card, until there are no more cards in the deck.
    # Then, update the total number of cards in player's hands.
    for player in players:
        if len(DECK) > 0:
            player.pick_card()
            player.print_cards()
        hand_card_count += len(player.hand)

    # Update the total number of cards and add one to the round counter.
    total_card_count = len(DECK) + hand_card_count
    round += 1

# Once the game is done, pick and print the overall game winner.
game_winner = max(players, key=lambda player: player.points)
print(f"\n{game_winner.name} wins the game with {game_winner.points} points!")
