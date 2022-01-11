extends Node

var _name
var hand = []
var stack = []
var points = 0

func _init(_name):
	self._name = _name

func pick_card(card):
	card._owner = self
	hand.append(card)

func play_card():
	return hand.pop_at(randi() % hand.size())

func add_cards_to_stack(cards):
	for c in cards:
		points += c.points
		stack.push_back(c)

func _to_string():
	return "[%s] %s" % [points, _name]
