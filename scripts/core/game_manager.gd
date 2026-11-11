extends Node
## Global game state entry point. Add this script as an Autoload when needed.

var current_level_id: StringName = &"starting_area"
var is_game_paused: bool = false

func set_game_paused(value: bool) -> void:
	is_game_paused = value
	get_tree().paused = value
