import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageOps
from functools import partial
from engine.Sprite import Sprite, random_sprite

class CostumesTab(ctk.CTkFrame):
    def __init__(self, app, master, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app

        self.data_list = []   # Données réelles
        self.widget_list = []  # Widgets visibles
        self.selected_index = None

        self.drag_data = {"index": None, "y": 0}

        self.scroll = ctk.CTkScrollableFrame(self, fg_color=["#dbe7f5", "#2b2d42"])
        self.scroll.pack(fill="both", expand=True, padx=5, pady=5)

        self.add_btn = ctk.CTkButton(
            self,
            text="🐱 +",
            width=60,
            height=60,
            corner_radius=30,
            fg_color=["#a46ff2", "#7c4cd8"],
            text_color="white",
            hover_color=["#7c4cd8", "#5b3db6"],
            font=ctk.CTkFont(size=20),
            command=self.add_sprite
        )
        self.add_btn.pack(pady=15)

        self.add_sprite()
        self.add_sprite()

        self.app.add_refresh(self.sync_widgets)

    def add_sprite(self):
        sprite = random_sprite()#Sprite(f"costume{len(self.data_list)+1}", Image.new("RGBA", (64, 64), (255, 0, 0)))
        self.data_list.append(sprite)
        self.sync_widgets()
        self.select_sprite(len(self.data_list)-1)

    def delete_sprite(self, index):
        if messagebox.askyesno("Confirm", f"Delete {self.data_list[index].name}?"):
            del self.data_list[index]
            self.sync_widgets()
            if self.data_list:
                self.select_sprite(min(index, len(self.data_list)-1))
            else:
                self.selected_index = None

    def sync_widgets(self):
        # Longueur : créer ou supprimer
        while len(self.widget_list) < len(self.data_list):
            w = self._create_sprite_widget(len(self.widget_list))
            self.widget_list.append(w)
        while len(self.widget_list) > len(self.data_list):
            old = self.widget_list.pop()
            old["frame"].destroy()

        # Mettre à jour contenu et re-binder drag/selection
        for idx, sprite in enumerate(self.data_list):
            w = self.widget_list[idx]
            w["num_label"].configure(text=str(idx+1))
            w["name_label"].configure(text=sprite.name)
            w["size_label"].configure(text=f"{sprite.image.width} x {sprite.image.height}")

            photo = sprite.get_icon()
            w["canvas"].itemconfig(w["image_id"], image=photo)
            w["canvas"].image = photo
            w["photo"] = photo

            

            # Binds
            for sub in ["frame", "num_label", "name_label", "size_label", "canvas"]:
                w[sub].bind("<Button-1>", lambda e, i=idx: self.select_sprite(i))
                w[sub].bind("<ButtonPress-1>", lambda e, i=idx: self.start_drag(i, e))
                w[sub].bind("<B1-Motion>", self.do_drag)
                w[sub].bind("<ButtonRelease-1>", self.stop_drag)

            # Correct bouton suppression
            w["delete_btn"].configure(command=lambda i=idx: self.delete_sprite(i))

            if idx == self.selected_index:
                self._apply_selected_style(w)
            else:
                self._apply_default_style(w)

    def _create_sprite_widget(self, index):
        sprite = self.data_list[index]
        frame = ctk.CTkFrame(
            self.scroll, fg_color=["#ffffff", "#3a3b3f"],
            corner_radius=15, border_width=2,
            border_color=["#cccccc", "#555555"]
        )
        frame.pack(padx=10, pady=10, fill="x")

        num_label = ctk.CTkLabel(frame, text=str(index+1), text_color=["#555", "#ddd"])
        num_label.pack(anchor="nw", padx=10, pady=(5, 0))

        bg_color = "#ffffff" if self._get_appearance_mode() == "light" else "#3a3b3f"
        canvas = tk.Canvas(frame, width=60, height=60, bg=bg_color, highlightthickness=0, bd=0)
        photo = sprite.get_icon()  # Obtenir l'icône du sprite
        image_id  = canvas.create_image(0, 0, anchor="nw", image=photo)
        canvas.image = photo  # garder la référence !
        canvas.pack(pady=5)
        def call_by_canvas(event, func):
            for idx, w in enumerate(self.widget_list):
                if w["canvas"] == event.widget:
                    return func(idx)
        canvas.tag_bind(image_id, "<Button-1>", partial(call_by_canvas, func=self.select_sprite))

        name_label = ctk.CTkLabel(frame, text=sprite.name, text_color=["#333", "#eee"])
        name_label.pack()

        size_label = ctk.CTkLabel(frame, text=f"{sprite.image.width} x {sprite.image.height}",
                                text_color=["#333", "#ccc"],
                                font=ctk.CTkFont(size=10))
        size_label.pack(pady=(0, 5))

        delete_btn = ctk.CTkButton(
            frame, text="✕", width=30, height=30,
            fg_color=["#ffffff", "#555555"],
            text_color=["black", "white"],
            corner_radius=15,
            hover_color=["#dddddd", "#333333"],
            font=ctk.CTkFont(size=12)
        )
        delete_btn.place(relx=1.0, rely=0.0, anchor="ne", x=-5, y=5)
        delete_btn.place_forget()

        return {
            "frame": frame,
            "num_label": num_label,
            "name_label": name_label,
            "size_label": size_label,
            "canvas": canvas,
            "image_id": image_id,
            "photo": photo,
            "delete_btn": delete_btn
        }

    def select_sprite(self, index):
        if self.selected_index is not None:
            self._apply_default_style(self.widget_list[self.selected_index])

        self.selected_index = index
        self._apply_selected_style(self.widget_list[index])

    def _apply_selected_style(self, w):
        w["canvas"].configure(bg="#a46ff2" if self._get_appearance_mode() == "light" else "#7c4cd8")
        w["frame"].configure(fg_color=["#a46ff2", "#7c4cd8"], border_color=["#a46ff2", "#7c4cd8"])
        w["num_label"].configure(text_color=["white", "white"])
        w["delete_btn"].place(relx=1.0, rely=0.0, anchor="ne", x=-5, y=5)

    def _apply_default_style(self, w):
        w["canvas"].configure(bg="#ffffff" if self._get_appearance_mode() == "light" else "#3a3b3f")
        w["frame"].configure(fg_color=["#ffffff", "#3a3b3f"], border_color=["#cccccc", "#555555"])
        w["num_label"].configure(text_color=["#555", "#ddd"])
        w["delete_btn"].place_forget()

    def start_drag(self, index, event):
        self.drag_data["index"] = index
        self.drag_data["y"] = event.y_root

    def do_drag(self, event):
        if self.drag_data["index"] is None:
            return

        from_idx = self.drag_data["index"]
        frames = [s["frame"] for s in self.widget_list]
        item = frames[from_idx]

        offset = self.scroll._parent_canvas.winfo_rooty()
        drag_center = event.y_root - offset

        h = item.winfo_height()
        fy = item.winfo_rooty() - offset
        item_center = fy + h // 2

        if abs(drag_center - item_center) < h * 0.3:
            return  # Pas assez de déplacement

        new_idx = from_idx

        for idx, w in enumerate(frames):
            if idx == from_idx:
                continue

            fy = w.winfo_rooty() - offset
            fh = w.winfo_height()
            other_center = fy + fh // 2

            if drag_center < other_center and idx < from_idx:
                new_idx = idx
                break
            elif drag_center > other_center and idx > from_idx:
                new_idx = idx
                break

        if new_idx != from_idx:
            self.data_list.insert(new_idx, self.data_list.pop(from_idx))
            self.drag_data["index"] = new_idx
            self.selected_index = new_idx
            self.sync_widgets()


    def stop_drag(self, event):
        self.drag_data = {"index": None, "y": 0}
