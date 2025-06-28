import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from engine.Sound import Sound, test_sound

class SoundsTab(ctk.CTkFrame):
    def __init__(self, app, master, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app

        self.data_list = []   # Données Sound
        self.widget_list = []  # Widgets
        self.selected_index = None

        self.drag_data = {"index": None, "y": 0}

        self.scroll = ctk.CTkScrollableFrame(self, fg_color=["#dbe7f5", "#2b2d42"])
        self.scroll.pack(fill="both", expand=True, padx=5, pady=5)

        self.add_btn = ctk.CTkButton(
            self,
            text="🔊 +",
            width=60,
            height=60,
            corner_radius=30,
            fg_color=["#a46ff2", "#7c4cd8"],
            text_color="white",
            hover_color=["#7c4cd8", "#5b3db6"],
            font=ctk.CTkFont(size=20),
            command=self.add_sound
        )
        self.add_btn.pack(pady=15)

        self.add_sound()
        self.add_sound()

        self.app.add_refresh(self.sync_widgets)

    def add_sound(self):
        sound = test_sound
        self.data_list.append(sound)
        self.sync_widgets()
        self.select_sound(len(self.data_list)-1)

    def delete_sound(self, index):
        if messagebox.askyesno("Confirm", f"Delete {self.data_list[index].name}?"):
            del self.data_list[index]
            self.sync_widgets()
            if self.data_list:
                self.select_sound(min(index, len(self.data_list)-1))
            else:
                self.selected_index = None

    def sync_widgets(self):
        while len(self.widget_list) < len(self.data_list):
            w = self._create_sound_widget(len(self.widget_list))
            self.widget_list.append(w)
        while len(self.widget_list) > len(self.data_list):
            old = self.widget_list.pop()
            old["frame"].destroy()

        for idx, sound in enumerate(self.data_list):
            w = self.widget_list[idx]
            w["num_label"].configure(text=str(idx+1))
            w["name_label"].configure(text=sound.name)
            w["duration_label"].configure(text=sound.get_duration_str())

            # Binds
            for key in ["frame", "num_label", "name_label", "duration_label", "icon_label"]:
                w[key].bind("<Button-1>", lambda e, i=idx: self.select_sound(i))
                w[key].bind("<ButtonPress-1>", lambda e, i=idx: self.start_drag(i, e))
                w[key].bind("<B1-Motion>", self.do_drag)
                w[key].bind("<ButtonRelease-1>", self.stop_drag)

            w["delete_btn"].configure(command=lambda i=idx: self.delete_sound(i))

            if idx == self.selected_index:
                self._apply_selected_style(w)
            else:
                self._apply_default_style(w)

    def _create_sound_widget(self, index):
        sound = self.data_list[index]
        frame = ctk.CTkFrame(
            self.scroll, fg_color=["#ffffff", "#3a3b3f"],
            corner_radius=15, border_width=2,
            border_color=["#cccccc", "#555555"]
        )
        frame.pack(padx=10, pady=10, fill="x")

        num_label = ctk.CTkLabel(frame, text=str(index+1), text_color=["#555", "#ddd"])
        num_label.pack(anchor="nw", padx=10, pady=(5, 0))

        icon_label = ctk.CTkLabel(frame, text="🔊", font=ctk.CTkFont(size=30))
        icon_label.pack(pady=5)

        name_label = ctk.CTkLabel(frame, text=sound.name, text_color=["#333", "#eee"])
        name_label.pack()

        duration_label = ctk.CTkLabel(frame, text=sound.get_duration_str(),
                                      text_color=["#333", "#ccc"],
                                      font=ctk.CTkFont(size=10))
        duration_label.pack(pady=(0, 5))

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
            "icon_label": icon_label,
            "name_label": name_label,
            "duration_label": duration_label,
            "delete_btn": delete_btn
        }

    def select_sound(self, index):
        if self.selected_index is not None:
            self._apply_default_style(self.widget_list[self.selected_index])
        self.selected_index = index
        self._apply_selected_style(self.widget_list[index])

    def _apply_selected_style(self, w):
        w["frame"].configure(fg_color=["#a46ff2", "#7c4cd8"], border_color=["#a46ff2", "#7c4cd8"])
        w["num_label"].configure(text_color=["white", "white"])
        w["delete_btn"].place(relx=1.0, rely=0.0, anchor="ne", x=-5, y=5)

    def _apply_default_style(self, w):
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
            return

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
