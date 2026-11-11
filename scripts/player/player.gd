extends CharacterBody2D
## Basic top-down player controller. Replace the placeholder drawing with a 64x64 sprite.

@export var move_speed: float = 120.0

const BODY_SIZE := Vector2(16.0, 22.0)
const BODY_COLOR := Color("#70c7a2")
const OUTLINE_COLOR := Color("#203b3a")

func _physics_process(_delta: float) -> void:
	var input_direction := Input.get_vector(
		"move_left",
		"move_right",
		"move_up",
		"move_down"
	)

	velocity = input_direction * move_speed
	move_and_slide()

func _draw() -> void:
	var body_rect := Rect2(-BODY_SIZE.x * 0.5, -BODY_SIZE.y * 0.5, BODY_SIZE.x, BODY_SIZE.y)
	draw_rect(body_rect.grow(1.0), OUTLINE_COLOR)
	draw_rect(body_rect, BODY_COLOR)
	draw_rect(Rect2(-4.0, -8.0, 3.0, 3.0), Color("#ffffff"))
	draw_rect(Rect2(2.0, -8.0, 3.0, 3.0), Color("#ffffff"))
