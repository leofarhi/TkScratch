import customtkinter as ctk
from PIL import Image, ImageDraw, ImageTk
from tkinter import Canvas, colorchooser
from ui.widgets.SmartCanvas import *
from engine.Sprite import Sprite, random_sprite

def tk_color_to_hex(widget, color_name):
    """Prend un nom couleur (ex: 'gray86') et renvoie '#rrggbb'"""
    r, g, b = widget.winfo_rgb(color_name)
    # r,g,b sont sur 16 bits (0-65535) → convertir en 8 bits (0-255)
    r = r // 256
    g = g // 256
    b = b // 256
    return f'#{r:02x}{g:02x}{b:02x}'

def hex_to_rgb(hex_color):
    """Convertit une couleur hexadécimale en tuple RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb_color):
    """Convertit un tuple RGB en couleur hexadécimale"""
    return '#{:02x}{:02x}{:02x}'.format(*rgb_color)


class CostumesArea(ctk.CTkFrame):
    def __init__(self, app, master, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app

        self.sprite = random_sprite()
        self.active_tool = None
        self.tool_buttons = []
        self.brush_color = "#000000"
        self.zoom = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.pan_start = None

        self.default_brush_size = 25

        self.allow_overflow = True
        self.checker_image = None
        self.checker_size = (0, 0)

        self.last_x = None
        self.last_y = None

        # === TOP BAR ===
        top_bar = ctk.CTkFrame(self, height=40)
        top_bar.pack(fill="x", padx=10, pady=5)

        self.costume_label = ctk.CTkLabel(top_bar, text="Costume")
        self.costume_label.pack(side="left", padx=(5, 2), pady=5)
        self.costume_name = ctk.CTkEntry(top_bar, placeholder_text="costume1")
        self.costume_name.pack(side="left", padx=5, pady=5)

        self.undo_btn = ctk.CTkButton(top_bar, text="⟲", width=40, command=self._undo)
        self.redo_btn = ctk.CTkButton(top_bar, text="⟳", width=40, command=self._redo)
        self.undo_btn.pack(side="left", padx=5, pady=5)
        self.redo_btn.pack(side="left", padx=5, pady=5)

        self.overflow_switch = ctk.CTkSwitch(
            top_bar,
            text="Overflow",
            command=self.toggle_overflow
        )
        self.overflow_switch.select()  # Par défaut ON
        self.overflow_switch.pack(side="left", padx=5, pady=5)


        # === LEFT TOOLS ===
        tools_frame = ctk.CTkFrame(self, width=60)
        tools_frame.pack(side="left", fill="y", padx=5, pady=5)

        self.tools = ["🖌️", "🧽", "⏹", "⬤", "T", "⛶", "🧹", "✂️"]
        for t in self.tools:
            b = ctk.CTkButton(
                tools_frame,
                text=t,
                width=50,
                command=lambda btn=t: self.select_tool(btn)
            )
            b.pack(pady=5, padx=5)
            self.tool_buttons.append(b)

        # === RIGHT OPTIONS ===
        right_panel = ctk.CTkFrame(self, width=200)
        right_panel.pack(side="right", fill="y", padx=5, pady=5)

        self.color_label = ctk.CTkLabel(right_panel, text="Color")
        self.color_label.pack(pady=(10, 2), padx=5)
        self.color_btn = ctk.CTkButton(
            right_panel,
            text=" ",
            width=50,
            fg_color=self.brush_color,
            hover_color=self.brush_color,
            border_color=None,
            border_width=3,
            command=self.pick_color
        )
        self.color_btn.pack(padx=5)

        self.brush_size_label = ctk.CTkLabel(right_panel, text="Brush Size")
        self.brush_size_label.pack(pady=(20, 2), padx=5)
        self.brush_size = ctk.CTkEntry(right_panel, placeholder_text=str(self.default_brush_size), width=50)
        self.brush_size.pack(padx=5)
        self.brush_size.bind("<KeyRelease>", self.validate_brush_size)

        # === DRAWING AREA ===
        canvas_frame = ctk.CTkFrame(self)
        canvas_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.canvas = SmartCanvas(canvas_frame, cursor="cross", callback=self.update_canvas)
        self.canvas.pack(fill="both", expand=True)

        # === Bottom bar ===
        bottom_bar = ctk.CTkFrame(self, height=40)
        bottom_bar.pack(fill="x", padx=10, pady=5)

        get_text = self.app.language_manager.get
        self.zoom_label = ctk.CTkLabel(bottom_bar, text=get_text("costume.zoom")+f": {self.zoom:.2f}x")
        self.zoom_label.pack(side="right", padx=10)

        self.pos_label = ctk.CTkLabel(bottom_bar, text="X: 0 Y: 0")
        self.pos_label.pack(side="left", padx=10)

        self.reset_view_btn = ctk.CTkButton(
            bottom_bar,
            text="Recentrer",
            width=100,
            command=self.compute_initial_zoom
        )
        self.reset_view_btn.pack(side="left", expand=True, padx=10)

        zoom_out_btn = ctk.CTkButton(bottom_bar, text="➖", width=50, command=self.zoom_out)
        zoom_in_btn = ctk.CTkButton(bottom_bar, text="➕", width=50, command=self.zoom_in)
        zoom_out_btn.pack(side="right", padx=5, pady=5)
        zoom_in_btn.pack(side="right", padx=5, pady=5)

        self.compute_initial_zoom()
        self.check_if_can_undo_redo()
        self.select_tool("🖌️")
        self.app.add_refresh(self.refresh)

    def refresh(self):
        get_text = self.app.language_manager.get
        self.costume_label.configure(text=get_text("costume.name"))
        self.costume_name.configure(placeholder_text=get_text("costume.name_placeholder"))
        self.color_label.configure(text=get_text("costume.color"))
        self.brush_size_label.configure(text=get_text("costume.brush_size"))
        self.zoom_label.configure(text=f"{get_text('costume.zoom')}: {self.zoom:.2f}x")
        self.overflow_switch.configure(text=get_text("costume.overflow"))
        self.reset_view_btn.configure(text=get_text("costume.reset_view"))
        self.checker_size = (0, 0)  # Reset checker size to force redraw

    def _brush_size(self):
        """Retourne la taille du pinceau"""
        try:
            raw_size = int(self.brush_size.get())
        except ValueError:
            raw_size = self.default_brush_size
        return raw_size

    def _undo(self):
        self.sprite.history.undo()
        self.compute_initial_zoom()
        self.check_if_can_undo_redo()

    def _redo(self):
        self.sprite.history.redo()
        self.compute_initial_zoom()
        self.check_if_can_undo_redo()

    def check_if_can_undo_redo(self):
        """Vérifie si on peut annuler ou refaire une action"""
        can_undo = self.sprite.history.can_undo()
        can_redo = self.sprite.history.can_redo()
        self.undo_btn.configure(state="normal" if can_undo else "disabled")
        self.redo_btn.configure(state="normal" if can_redo else "disabled")

    def toggle_overflow(self):
        self.allow_overflow = self.overflow_switch.get() == 1

    def compute_initial_zoom(self):
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        if canvas_w <= 1 or canvas_h <= 1:
            self.after(100, self.compute_initial_zoom)
            return

        img_w, img_h = self.sprite.image.size
        zoom_w = canvas_w / img_w
        zoom_h = canvas_h / img_h
        self.zoom = min(zoom_w, zoom_h) * 0.5

        self.offset_x = (canvas_w - img_w * self.zoom) // 2
        self.offset_y = (canvas_h - img_h * self.zoom) // 2

    def zoom_in(self):
        self.zoom_at(1.1)

    def zoom_out(self):
        self.zoom_at(1 / 1.1)

    def zoom_at(self, factor, mouse=False):
        if mouse:
            mx, my = self.canvas.input.mouse_position()
        else:
            mx, my = self.canvas.surface.size()
            mx, my = mx // 2, my // 2

        before_x = (mx - self.offset_x) / self.zoom
        before_y = (my - self.offset_y) / self.zoom

        self.zoom *= factor

        self.offset_x = mx - before_x * self.zoom
        self.offset_y = my - before_y * self.zoom

    def compute_offset(self):
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        img_w, img_h = self.sprite.image.size
        self.offset_x = (canvas_w - img_w * self.zoom) // 2
        self.offset_y = (canvas_h - img_h * self.zoom) // 2

    def select_tool(self, tool):
        self.active_tool = tool
        for btn in self.tool_buttons:
            if btn.cget("text") == tool:
                btn.configure(fg_color="#5b9bd5", text_color="white")
            else:
                btn.configure(
                    fg_color=ctk.ThemeManager.theme["CTkButton"]["border_color"],
                    text_color=ctk.ThemeManager.theme["CTkButton"]["text_color"]
                )

    def pick_color(self):
        color_code = colorchooser.askcolor(title="Pick a color")
        if color_code and color_code[1]:
            self.brush_color = color_code[1]
            self.color_btn.configure(fg_color=self.brush_color, hover_color=self.brush_color)

    def validate_brush_size(self, event=None):
        val = self.brush_size.get()
        if not val.isdigit():
            self.brush_size.delete(0, "end")
            self.brush_size.insert(0, "10")

    def update_canvas(self, widget):
        if widget.input.mouse_is_inside() and widget.input.is_mouse_down(1):
            self.sprite.history.push()
            self.check_if_can_undo_redo()
        self._handle_scroll(widget)
        self._draw_background(widget)
        self._draw_sprite(widget)
        self._draw_border(widget)
        self._handle_panning(widget)
        self._handle_brush(widget)
        self._draw_preview(widget)
        self._update_labels(widget)
        widget.surface.display()


    def _handle_scroll(self, widget):
        scroll = widget.input.get_scroll()
        if scroll != 0:
            self.zoom_at(1.1 if scroll > 0 else 1 / 1.1, mouse=True)

    def _draw_background(self, widget):
        w, h = widget.surface.size()
        if (w, h) != self.checker_size:
            self.checker_size = (w, h)
            tile = 15
            mode = self.app._get_appearance_mode() == "dark"
            color1 = tk_color_to_hex(self, self.cget("bg_color")[mode])
            color2 = ["#d5d5d5", "#2b2d42"][mode]
            checker = Image.new("RGB", (w, h), color1)
            draw = ImageDraw.Draw(checker)
            for y in range(0, h, tile):
                for x in range(0, w, tile):
                    if (x // tile + y // tile) % 2 == 0:
                        draw.rectangle([x, y, x + tile, y + tile], fill=color2)
            self.checker_image = checker

        widget.surface.blit(self.checker_image, (0, 0))

    def _draw_sprite(self, widget):
        img_resized = self.sprite.image.resize(
            (int(self.sprite.image.width * self.zoom), int(self.sprite.image.height * self.zoom)),
            Image.NEAREST
        )
        widget.surface.blit(img_resized, (int(self.offset_x), int(self.offset_y)))

    def _draw_border(self, widget):
        img_w = int(self.sprite.image.width * self.zoom)
        img_h = int(self.sprite.image.height * self.zoom)
        widget.surface.rectangle(
            (
                int(self.offset_x),
                int(self.offset_y),
                int(self.offset_x) + img_w,
                int(self.offset_y) + img_h
            ),
            outline="red",
            width=1
        )

    def _handle_panning(self, widget):
        mx, my = widget.input.mouse_position()
        if widget.input.is_mouse_pressed(2):
            if self.pan_start is None:
                self.pan_start = mx, my
            else:
                dx = mx - self.pan_start[0]
                dy = my - self.pan_start[1]
                self.offset_x += dx
                self.offset_y += dy
                self.pan_start = mx, my
        else:
            self.pan_start = None

    def _calculate_expansion(self, x, y):
        # Rayon réel du brush
        brush_radius = int(self._brush_size() // 2)

        # Bordure de sécurité : on réserve toujours au moins brush_radius autour
        expand_x = max(0, x + brush_radius + 2 - self.sprite.image.width)
        expand_y = max(0, y + brush_radius + 2 - self.sprite.image.height)
        expand_left = max(0, -(x - brush_radius - 2))
        expand_top = max(0, -(y - brush_radius - 2))

        if self.allow_overflow and (expand_x > 0 or expand_y > 0 or expand_left > 0 or expand_top > 0):
            new_w = self.sprite.image.width + expand_x + expand_left
            new_h = self.sprite.image.height + expand_y + expand_top
            new_image = Image.new("RGBA", (new_w, new_h), (0, 0, 0, 0))
            new_image.paste(self.sprite.image, (expand_left, expand_top))
            self.sprite.image = new_image

            if expand_left > 0:
                if self.last_x is not None:
                    self.last_x += expand_left
                x += expand_left
                self.offset_x -= expand_left * self.zoom
            if expand_top > 0:
                if self.last_y is not None:
                    self.last_y += expand_top
                y += expand_top
                self.offset_y -= expand_top * self.zoom

        return x, y


    def _handle_brush(self, widget):
        mx, my = widget.input.mouse_position()
        if self.active_tool not in ["🖌️", "🧽"]:
            return

        if widget.input.mouse_is_inside() and widget.input.is_mouse_pressed(1):
            x = int((mx - self.offset_x) / self.zoom)
            y = int((my - self.offset_y) / self.zoom)

            if self.active_tool == "🖌️":
                x,y = self._calculate_expansion(x, y)

            draw = ImageDraw.Draw(self.sprite.image)
            brush_size = self._brush_size()
            color = self.brush_color if self.active_tool == "🖌️" else (0, 0, 0, 0)

            if self.last_x is not None and self.last_y is not None:
                dist = max(abs(x - self.last_x), abs(y - self.last_y))
                steps = dist + 1
                for i in range(steps):
                    ix = int(self.last_x + (x - self.last_x) * i / steps)
                    iy = int(self.last_y + (y - self.last_y) * i / steps)
                    draw.ellipse(
                        (ix - brush_size // 2, iy - brush_size // 2, ix + brush_size // 2, iy + brush_size // 2),
                        fill=color
                    )
            else:
                draw.ellipse(
                    (x - brush_size // 2, y - brush_size // 2, x + brush_size // 2, y + brush_size // 2),
                    fill=color
                )

            self.last_x, self.last_y = x, y

        elif not widget.input.is_mouse_pressed(1):
            self.last_x = None
            self.last_y = None

    def _draw_preview(self, widget):
        if self.active_tool in ["🖌️", "🧽"]:
            mx, my = widget.input.mouse_position()
            preview_size = int(self._brush_size() * self.zoom)
            widget.surface.ellipse(
                (
                    mx - preview_size // 2,
                    my - preview_size // 2,
                    mx + preview_size // 2,
                    my + preview_size // 2
                ),
                outline="black" if self.app._get_appearance_mode() == "light" else "white",
                width=1
            )

    def _update_labels(self, widget):
        get_text = self.app.language_manager.get
        mx, my = widget.input.mouse_position()
        self.pos_label.configure(text=f"X: {mx} Y: {my}")
        self.zoom_label.configure(text=get_text("costume.zoom")+f": {self.zoom:.2f}x")
