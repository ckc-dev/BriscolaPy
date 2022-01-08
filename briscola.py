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
    "DANARI",
    "SPADE"
]


class Player:
    def __init__(self):
        self.name = ""
        self.cards = []
        self.stack = []
        self.points = 0

    def play_card(self):
        card = self.cards.pop(self.cards.index(random.choice(self.cards)))
        print(f"---- {self.name} plays a {card}!")
        return card

    def pick_card(self):
        card = DECK.pop(DECK.index(random.choice(DECK)))
        card.owner = self
        self.cards.append(card)
        print(f"++++ {self.name} picks a {card}!")

    def print_cards(self):
        if self.cards == 0:
            message = f"{self.name} has no cards left."
        else:
            message = (f"//// {self.name}'s cards:"
                       + ", ".join([str(card) for card in self.cards]))
        print(message)

    def declare_victory(self):
        print(f"{self.name} wins this round!")

    def add_cards_to_stack(self, cards):
        self.stack.extend(cards)
        for card in cards:
            self.points += card.points

    def __str__(self):
        return f"{self.name}"


class Card:
    def __init__(self, name, suit, value):
        self.name = name
        self.suit = suit
        self.points = value
        self.value = None
        self.owner = None

        if self.name == "1":
            self.value == self.points
        else:
            try:
                self.value = int(self.name)
            except ValueError:
                self.value = self.points

    def __str__(self):
        return f"{self.name} of {self.suit.lower()} ({self.points})"


def get_max_card(cards):
    max_points = max(cards, key=lambda card: card.points)
    cards = [c for c in cards if c.points == max_points.points]
    if len(cards) > 1:
        max_value = max(cards, key=lambda card: card.value)
        cards = [c for c in cards if c.value == max_value.value]
    return cards[0]


number_of_players = int(sys.argv[1])
assert MIN_NUMBER_OF_PLAYERS <= number_of_players <= MAX_NUMBER_OF_PLAYERS

players = [Player() for _ in range(number_of_players)]

for i, player in enumerate(players, 1):
    player.name = input(f"Player {i} name: ")

DECK = [Card(n, s, p) for s in SUITS for n, p in CARDS.items()]
random.shuffle(DECK)

if number_of_players == 3:
    for card in DECK:
        if card.name == "2":
            DECK.pop(DECK.index(card))

for player in players:
    for _ in range(CARDS_PER_PLAYER):
        card = DECK.pop(0)
        card.owner = player
        player.cards.append(card)

random.shuffle(players)

lead_card = DECK.pop(0)
DECK.append(lead_card)


total_player_cards = number_of_players * CARDS_PER_PLAYER
total_cards = len(DECK) + total_player_cards
round = 1
while total_cards > 0:
    print(
        f"//// Total cards: {total_cards} | Deck: {len(DECK)} | Hands: {total_player_cards}")
    print(f"//// Current lead card: {lead_card}")
    print("CURRENT PLAYER ORDER:" + ", ".join(str(p) for p in players))
    total_player_cards = 0
    played_cards = []
    for player in players:
        print(f"//// It's {player}'s turn!")
        card = player.play_card()
        played_cards.append(card)
        player.print_cards()

    matches = [c for c in played_cards if c.suit == lead_card.suit]
    secondary_lead = played_cards[0]
    print(f"//// Current secondary lead: {secondary_lead}")

    if not matches:
        matches = [c for c in played_cards[1:]
                   if c.suit == secondary_lead.suit]
        if not matches:
            winner = played_cards[0].owner
        else:
            max_card = get_max_card(matches)
            winner = max_card.owner
    else:
        max_card = get_max_card(matches)
        winner = max_card.owner

    winner.add_cards_to_stack(played_cards)
    winner.declare_victory()
    points = winner.points
    print(f"{winner} now has {points} points!")

    winner_index = players.index(winner)
    new_player_order = players[winner_index:]
    new_player_order.extend(players[:winner_index])
    players = new_player_order

    for player in players:
        if len(DECK) > 0:
            player.pick_card()
            player.print_cards()
        total_player_cards += len(player.cards)

    total_cards = len(DECK) + total_player_cards
    print(f"\nRound {round} over!\n")
    round += 1

game_winner = max(players, key=lambda player: player.points)
print(f"{game_winner} wins the game with {game_winner.points} points!")
