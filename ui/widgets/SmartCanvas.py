import tkinter as tk
from PIL import Image, ImageDraw, ImageTk, ImageFont

class CanvasFont:
    def __init__(self, font=None, size=20):
        """
        :param font: None pour police système par défaut, ou chemin vers un fichier .ttf
        :param size: Taille de la police
        """
        if font is None:
            self.font = ImageFont.load_default()
        else:
            self.font = ImageFont.truetype(font, size)

    def get_pil_font(self):
        return self.font


class CanvasInput:
    def __init__(self, widget):
        self._widget = widget
        self._pressed_keys = set()
        self._just_pressed = set()
        self._just_released = set()
        self._mouse_pos = (0, 0)
        self._mouse_inside = False
        self._pressed_buttons = set()
        self._just_button_down = set()
        self._just_button_up = set()

        widget.bind("<KeyPress>", self._on_key_press)
        widget.bind("<KeyRelease>", self._on_key_release)
        widget.bind("<Enter>", self._on_enter)
        widget.bind("<Leave>", self._on_leave)
        widget.bind("<Motion>", self._on_motion)
        widget.bind("<ButtonPress>", self._on_mouse_down)
        widget.bind("<ButtonRelease>", self._on_mouse_up)
        self._scroll_delta = (0, 0)  # (dx, dy)
        widget.bind("<MouseWheel>", self._on_scroll)       # Windows / macOS
        widget.bind("<Button-4>", self._on_scroll_linux)   # Linux (up)
        widget.bind("<Button-5>", self._on_scroll_linux)   # Linux (down)

    def _on_key_press(self, event):
        key = event.keysym.lower()
        if key not in self._pressed_keys:
            self._just_pressed.add(key)
        self._pressed_keys.add(key)

    def _on_key_release(self, event):
        key = event.keysym.lower()
        self._pressed_keys.discard(key)
        self._just_released.add(key)

    def is_key_pressed(self, key):
        return key.lower() in self._pressed_keys

    def is_key_down(self, key):
        return key.lower() in self._just_pressed

    def is_key_up(self, key):
        return key.lower() in self._just_released

    # ==== SOURIS ====

    def _on_mouse_down(self, event):
        self._pressed_buttons.add(event.num)
        self._just_button_down.add(event.num)

    def _on_mouse_up(self, event):
        self._pressed_buttons.discard(event.num)
        self._just_button_up.add(event.num)

    def is_mouse_pressed(self, button):
        return button in self._pressed_buttons

    def is_mouse_down(self, button):
        return button in self._just_button_down

    def is_mouse_up(self, button):
        return button in self._just_button_up

    def mouse_position(self):
        return self._mouse_pos

    def mouse_is_inside(self):
        return self._mouse_inside

    def mouse_button_name(self, button_id):
        return {1: "left", 2: "middle", 3: "right"}.get(button_id, f"button{button_id}")

    def _on_enter(self, event):
        self._widget.focus_set()
        self._mouse_inside = True

    def _on_leave(self, event):
        self._mouse_inside = False

    def _on_motion(self, event):
        self._mouse_pos = (event.x, event.y)

    def _on_scroll(self, event):
        dx, dy = self._scroll_delta
        self._scroll_delta = (dx, dy + int(event.delta / 120))

    def _on_scroll_linux(self, event):
        dx, dy = self._scroll_delta
        if event.num == 4:
            self._scroll_delta = (dx, dy + 1)
        elif event.num == 5:
            self._scroll_delta = (dx, dy - 1)

    def get_scroll(self):
        #return -x, 0, x for down, no scroll, up
        dx, dy = self._scroll_delta
        if dy > 0:
            self._scroll_delta = (dx, 0)
            return 1  # Scroll up
        elif dy < 0:
            self._scroll_delta = (dx, 0)
            return -1  # Scroll down
        else:
            return 0

    def reset(self):
        self._just_pressed.clear()
        self._just_released.clear()
        self._just_button_down.clear()
        self._just_button_up.clear()
        self._scroll_delta = (0, 0)

class CanvasDrawer:
    def __init__(self, image, tk_image, bg_color):
        self._image = image
        self._tk_image = tk_image
        self._draw = ImageDraw.Draw(image)
        self._bg_color = bg_color

    def size(self):
        return self._image.size

    def clear(self):
        self._draw.rectangle((0, 0, self._image.width, self._image.height), fill=self._bg_color)

    def display(self):
        self._tk_image.paste(self._image)

    def fill(self, color):
        self._draw.rectangle((0, 0, self._image.width, self._image.height), fill=color)

    # Redirection vers les méthodes de dessin
    def __getattr__(self, name):
        return getattr(self._draw, name)
    
    def blit(self, image, position):
        if not isinstance(image, Image.Image):
            raise TypeError("blit() requires a PIL.Image as argument")
        self._image.paste(image, position, image if image.mode == 'RGBA' else None)

    def text(self, text, position, font: CanvasFont, color="black"):
        self._draw.text(position, text, fill=color, font=font.get_pil_font())


class SmartCanvas(tk.Canvas):
    def __init__(self, master, callback=None, bg_color="white", **kwargs):
        super().__init__(master, highlightthickness=0, takefocus=True, **kwargs)

        self.bg_color = bg_color
        self.callback = callback

        self.image = None
        self.tk_image = None
        self.surface = None
        self.img_id = None

        self.bind("<Configure>", self._on_resize)
        self.input = CanvasInput(self)

        self.after(16, self._update_loop)

    def _on_resize(self, event):
        w, h = event.width, event.height
        if w > 0 and h > 0:
            self._create_surface(w, h)

    def _create_surface(self, w, h):
        self.image = Image.new("RGB", (w, h), self.bg_color)
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.surface = CanvasDrawer(self.image, self.tk_image, self.bg_color)

        if self.img_id is None:
            self.img_id = self.create_image(0, 0, anchor="nw", image=self.tk_image)
        else:
            self.itemconfig(self.img_id, image=self.tk_image)


    def _update_loop(self):
        if self.image is None or self.surface is None:
            return self.after(16, self._update_loop)
        if self.callback:
            self.callback(self)
        self.input.reset()
        self.after(16, self._update_loop)