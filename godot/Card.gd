extends Node

var _name
var suit
var points
var priority
var _owner


func _init(_name, suit, points, priority):
	self._name = _name
	self.suit = suit
	self.points = points
	self.priority = priority

func _to_string():
	return "[%s] %s of %s" % [points, _name, suit.to_lower()]
