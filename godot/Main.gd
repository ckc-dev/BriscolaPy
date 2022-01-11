extends Node

const Card = preload("res://Card.gd")
const Participant = preload("res://Participant.gd")

const CARDS = {
	"1": [11, 9],
	"2": [0,  0],
	"3": [10, 8],
	"4": [0,  1],
	"5": [0,  2],
	"6": [0,  3],
	"7": [0,  4],
	"F": [2,  5],
	"C": [3,  6],
	"R": [4,  7]
}

const SUITS = [
	"BASTONI",
	"COPPE",
	"DENARI",
	"SPADE"
]

const CARDS_PER_PLAYER = 3

func max_card(cards):
	var max_card_priority = -INF
	for c in cards:
		if c.priority > max_card_priority:
			max_card_priority = c.priority

	var max_card_arr = []
	for c in cards:
		if c.priority == max_card_priority:
			max_card_arr.push_back(c)

	return max_card_arr[0]

func winning_card(cards, lead_card, secondary_lead=null):
	var matches = []
	for c in cards:
		if c.suit == lead_card.suit:
			matches.push_back(c)

	if matches.size() > 0:
		return max_card(matches)
	return winning_card(cards, secondary_lead)

func get_game_winner(participants):
	var winner = participants[0]

	for p in participants:
		if p.points > winner.points:
			winner = p

	return winner

func _ready():
	randomize()

	var deck = []

	for suit in SUITS:
		for name in CARDS:
			var points = CARDS[name][0]
			var priority = CARDS[name][1]
			var card = Card.new(name, suit, points, priority)

			deck.append(card)

	deck.shuffle()

	var anne = Participant.new("Anne")
	var bob = Participant.new("Bob")
	var participants = [anne, bob]

	for p in participants:
		for i in range(CARDS_PER_PLAYER):
			var card = deck.pop_front()
			p.pick_card(card)

	var lead_card = deck.pop_front()
	deck.push_back(lead_card)

	participants.shuffle()

	var hand_card_count = participants.size() * CARDS_PER_PLAYER
	var total_card_count = hand_card_count + deck.size()
	var _round = 1

	while total_card_count > 0:
		var secondary_lead = null
		var played_cards = []

		hand_card_count = 0

		print()
		print("Starting round %s!" % _round)
		print("Lead card: %s" % lead_card)
		print()

		for p in participants:
			print("It's %s's turn!" % p)
			var played_card = p.play_card()
			played_cards.push_back(played_card)

			if p == participants[0]:
				secondary_lead = played_card

			print("%s plays a %s!" % [p, played_card])

		var round_winner = winning_card(played_cards, lead_card, secondary_lead)._owner
		round_winner.add_cards_to_stack(played_cards)
		print("%s wins this round!" % round_winner)

		var winner_index = participants.find(round_winner)
		var left = participants.slice(winner_index, -1)
		var right = participants.slice(0, winner_index)
		var right_winner_index = right.find(round_winner)
		right.pop_at(right_winner_index)
		left.append_array(right)

		participants = left

		for p in participants:
			if deck.size() > 0:
				var card = deck.pop_front()
				p.pick_card(card)

				print("%s picks a %s!" % [p, card])
			hand_card_count += p.hand.size()

		total_card_count = hand_card_count + deck.size()
		_round += 1

	var game_winner = get_game_winner(participants)
	print()
	print("%s won the game with %s points!" % [game_winner, game_winner.points])
