extends Node

var _name
var hand = []
var stack = []
var points = 0

onready var card_container = $CardContainer

func setup(_name):
	self._name = _name

func pick_card(card):
	card._owner = self
	card_container.add_child(card)
	card.update_node()
	hand.append(card)

func play_card():
	var card =  hand.pop_at(randi() % hand.size())
	card.hide()
	return card

func add_cards_to_stack(cards):
	for c in cards:
		points += c.points
		stack.push_back(c)

func _to_string():
	return "[%s] %s" % [points, _name]
