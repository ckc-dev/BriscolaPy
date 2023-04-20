"""Player class and functions related to it."""

import random


class Player:
    """Defines a player object."""

    verbose = False

    def __init__(self, name, is_cpu):
        """Initialize instance."""
        self.name = name
        self.is_cpu = is_cpu
        self.hand = []   # Player's hand of cards.
        self.stack = []  # Player's stack of won cards.
        self.points = 0

    def play_card(self, index=None):
        """
        Remove a card from the player's hand and return it.

        Args:
            index (int, optional): Index of card to be returned. If this is not
            passed, a random card is returned instead. Defaults to None.

        Returns:
            Card: Played card.
        """
        return (self.hand.pop(index) if index
                else self.hand.pop(self.hand.index(random.choice(self.hand))))

    def pick_card(self, card):
        """
        Pick a card from the deck.

        Sets the player to be the owner of a card passed to this function and
        adds it to the player's hand.

        Args:
            card (Card): Card picked from the deck.
        """
        card.owner = self

        self.hand.append(card)

    def add_cards_to_stack(self, cards):
        """
        Add a list of cards to the player's stack.

        Adds a list of cards to the player's stack of won cards, and adds the
        points for those cards to the player's total number of points.

        Args:
            cards (Card): List of cards.
        """
        self.stack.extend(cards)

        self.points += sum(c.points for c in cards)

    def __str__(self):
        """Define string representation of an instance."""
        return (f"[{self.points}] " if self.verbose else "") + self.name
