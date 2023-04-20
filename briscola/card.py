"""Card class and functions related to it."""


class Card:
    """Defines a card object."""

    verbose = False

    def __init__(self, name, suit, points, priority):
        """Initialize instance."""
        self.name = name
        self.suit = suit
        self.points = points
        self.priority = priority
        self.owner = None

    def __str__(self):
        """Define string representation of an instance."""
        return ((f"[{self.points}] " if self.verbose else "")
                + f"{self.name} of {self.suit.lower()}")


def max_card(cards):
    """
    Get the card with the highest priority from a list of cards.

    Args:
        cards (Card): List of cards to get highest priority card from.

    Returns:
        Card: Max priority card.
    """
    max_priority_card = max(cards, key=lambda card: card.priority)
    cards = [c for c in cards if c.priority == max_priority_card.priority]

    return cards[0]


def get_winning_card(cards, lead_card, secondary_lead=None):
    """
    Get a round's winning card.

    Returns the winning card of a round, by checking for cards in a list of
    cards played this round that match either the lead card suit, or, if no
    card matches it, the secondary lead card suit. If no card matches it
    either, then it (the secondary lead card suit) is chosen as the winner.

    If at any point, multiple cards match, then the card with the highest
    priority is chosen.

    Args:
        cards (Card): List of cards to get winning card from.
        lead_card (Card): Lead card used to compare other cards against.
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
    return (max_card(matches)
            if matches else get_winning_card(cards, secondary_lead))
