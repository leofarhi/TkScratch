from PIL import Image, ImageOps, ImageTk
from modules.history import HistoryManager

class Sprite:
    def __init__(self, name, image):
        self.name = name
        self.image = image
        self.history = HistoryManager()
        self.history.push_callback = self.push_history
        self.history.apply_callback = self.apply_history

    @staticmethod
    def create(name, width, height, color=(255, 0, 0, 255)):
        """Create a new sprite with a solid color."""
        sprite = Sprite(name, Image.new("RGBA", (width, height), color))
        sprite.history.clear()
        return sprite

    def push_history(self):
        if self.image is None:
            return None
        return self.image.copy()

    def apply_history(self, action):
        if self.image is None:
            return
        self.image = action

    def get_icon(self, size=(60, 60)):
        resized = ImageOps.contain(self.image, size, Image.LANCZOS)
        background = Image.new("RGBA", size, (0, 0, 0, 0))
        background.paste(resized, ((size[0] - resized.width) // 2, (size[1] - resized.height) // 2))
        photo = ImageTk.PhotoImage(background)
        return photo
