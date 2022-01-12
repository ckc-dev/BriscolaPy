extends Node

var hand = []
var stack = []
var points = 0
var _name

onready var card_container = $CardContainer


func _to_string():
	return _name


func setup(_name):
	self._name = _name


func pick_card(card):
	card._owner = self
	card_container.add_child(card)
	card.update_node()
	hand.push_back(card)


func play_card():
	var card = hand.pop_at(randi() % hand.size())
	card.hide()
	return card


func add_cards_to_stack(cards):
	for c in cards:
		points += c.points
		stack.push_back(c)
		$PointsBackground/Points.text = str(points)
