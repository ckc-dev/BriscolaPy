extends Node

var _name
var suit
var points
var priority
var _owner

onready var card_name_node = $VBoxContainer/CardName
onready var card_suit_node = $VBoxContainer/CardSuit

func setup(_name, suit, points, priority):
	self._name = _name
	self.suit = suit
	self.points = points
	self.priority = priority

func update_node():
	card_name_node.text = _name
	card_suit_node.text = suit

func _to_string():
	return "[%s] %s of %s" % [points, _name, suit]
