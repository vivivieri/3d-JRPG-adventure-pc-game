extends Node
## Tab menu singleton — field pause + shop overlay host.

const MENU_SCENE = preload("res://scenes/ui/tab_menu.tscn")

var _menu: CanvasLayer = null


func _ready() -> void:
	call_deferred("_ensure_menu")


func _ensure_menu() -> void:
	if _menu:
		return
	_menu = MENU_SCENE.instantiate()
	get_tree().root.call_deferred("add_child", _menu)
	await get_tree().process_frame
	_menu.closed.connect(_on_closed)


func _on_closed() -> void:
	EventBus.scene_blocked_changed.emit(false)


func open_menu() -> void:
	_ensure_menu()
	if _menu:
		_menu.open_menu()
		EventBus.scene_blocked_changed.emit(true)


func open_shop(vendor_id: String) -> void:
	_ensure_menu()
	if _menu:
		_menu.open_shop(vendor_id)
		EventBus.scene_blocked_changed.emit(true)


func is_open() -> bool:
	return _menu != null and _menu.is_open()


func close_menu() -> void:
	if _menu and _menu.is_open():
		_menu.close_menu()
