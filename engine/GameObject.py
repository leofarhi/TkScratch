class GameObject:
    def __init__(self, name, x=0, y=0, visible=True, direction=90, size=100, is_background=False):
        self.name = name
        self.x = x
        self.y = y
        self.visible = visible
        self.direction = direction
        self.size = size
        self.is_background = is_background
        self.sprites = []
        self.current_sprite = 0
        self.code = []