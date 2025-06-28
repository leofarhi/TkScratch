from PIL import Image, ImageOps, ImageTk
from modules.history import HistoryManager

class Sprite:
    def __init__(self, name, image):
        self.name = name
        self.image = image
        self.history = HistoryManager()
        self.history.push_callback = self.push_history
        self.history.apply_callback = self.apply_history

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
    
############### TEST ###############
import random
import string
from PIL import ImageDraw

def random_sprite():
    w, h = random.randint(200, 400), random.randint(200, 400)
    color = tuple(random.randint(0, 255) for _ in range(3)) + (255,)
    name = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    image = Image.new("RGBA", (w, h), color)
    draw = ImageDraw.Draw(image)
    draw.text((w//4, h//4), "🐱", fill=(255, 255, 255, 255))

    sprite = Sprite(name, image)
    return sprite
####################################
