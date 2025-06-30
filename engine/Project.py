from engine.GameObject import GameObject

class Project:
    def __init__(self):
        self.name = "New Project"
        self.game_objects = [GameObject("Background", 0, 0, is_background=True)]
        self.current_object = self.game_objects[0]  # Default to the background object

    def add_game_object(self, obj):
        self.game_objects.append(obj)

    def remove_game_object(self, obj):
        self.game_objects.remove(obj)
