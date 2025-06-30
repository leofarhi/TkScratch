import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from functools import partial
from engine.GameObject import GameObject

class InfoArea(ctk.CTkFrame):
    def __init__(self, app, master, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.pack_propagate(False)
        self.setup_gameobject_info()
        self.setup_gameobject_list()
        self.bind_entries()

    def setup_gameobject_info(self):
        get_text = lambda p: self.app.language_manager.get(p)
        self.gameobject_info = ctk.CTkFrame(self, fg_color=["#f0f0f0", "#1a1a1a"])
        self.gameobject_info.grid(row=0, column=0, sticky="ew", padx=10, pady=(5, 2))
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self.gameobject_info.grid_columnconfigure(1, weight=1)
        self.gameobject_info.grid_columnconfigure(3, weight=1)
        self.gameobject_info.grid_columnconfigure(5, weight=1)

        self.gameobject_name_label = ctk.CTkLabel(self.gameobject_info, text=get_text("gameobject.name"))
        self.gameobject_name_label.grid(row=0, column=0, padx=5, pady=5)

        self.entry_gameobject_name = ctk.CTkEntry(self.gameobject_info, placeholder_text=get_text("gameobject.name_placeholder"))
        self.entry_gameobject_name.grid(row=0, column=1, padx=5, sticky="ew")

        self.label_x = ctk.CTkLabel(self.gameobject_info, text="x")
        self.label_x.grid(row=0, column=2)

        self.entry_x = ctk.CTkEntry(self.gameobject_info, placeholder_text="0")
        self.entry_x.grid(row=0, column=3, padx=5, sticky="ew")

        self.label_y = ctk.CTkLabel(self.gameobject_info, text="y")
        self.label_y.grid(row=0, column=4)

        self.entry_y = ctk.CTkEntry(self.gameobject_info, placeholder_text="0")
        self.entry_y.grid(row=0, column=5, padx=5, sticky="ew")

        self.show_checkbox = ctk.CTkCheckBox(self.gameobject_info, text=get_text("gameobject.show"), checkbox_width=18, checkbox_height=18)
        self.show_checkbox.grid(row=1, column=0, columnspan=2, pady=5)

        self.label_size = ctk.CTkLabel(self.gameobject_info, text=get_text("gameobject.size"))
        self.label_size.grid(row=1, column=2)

        self.entry_size = ctk.CTkEntry(self.gameobject_info, placeholder_text="100")
        self.entry_size.grid(row=1, column=3, padx=5, sticky="ew")

        self.label_direction = ctk.CTkLabel(self.gameobject_info, text=get_text("gameobject.direction"))
        self.label_direction.grid(row=1, column=4)

        self.entry_direction = ctk.CTkEntry(self.gameobject_info, placeholder_text="90")
        self.entry_direction.grid(row=1, column=5, padx=5, sticky="ew")

        self.app.add_refresh(self.refresh)

    def refresh(self):
        get_text = self.app.language_manager.get
        self.gameobject_name_label.configure(text=get_text("gameobject.name"))
        self.entry_gameobject_name.configure(placeholder_text=get_text("gameobject.name_placeholder"))
        self.show_checkbox.configure(text=get_text("gameobject.show"))
        self.label_size.configure(text=get_text("gameobject.size"))
        self.label_direction.configure(text=get_text("gameobject.direction"))
        self.refresh_fields()
        self.refresh_gameobject_list()



    def bind_entries(self):
        vcmd_int = (self.register(self.validate_int), "%P")

        self.entry_x.configure(validate="key", validatecommand=vcmd_int)
        self.entry_y.configure(validate="key", validatecommand=vcmd_int)
        self.entry_size.configure(validate="key", validatecommand=vcmd_int)
        self.entry_direction.configure(validate="key", validatecommand=vcmd_int)

        def bind_live(entry, attr, cast=str):
            entry.bind("<FocusOut>", lambda e: self.update_attr(attr, entry, cast))
            entry.bind("<KeyRelease>", lambda e: self.update_attr(attr, entry, cast))

        bind_live(self.entry_gameobject_name, "name", str)
        bind_live(self.entry_x, "x", int)
        bind_live(self.entry_y, "y", int)
        bind_live(self.entry_size, "size", int)
        bind_live(self.entry_direction, "direction", int)

        self.show_checkbox.configure(command=self.update_visibility)

    def validate_int(self, value):
        if value == "" or value == "-":
            return True
        try:
            int(value)
            return True
        except ValueError:
            return False

    def update_attr(self, attr, entry, cast=str):
        obj = self.app.project.current_object
        if obj:
            try:
                val = entry.get()
                if val == "" or val == "-":
                    return
                setattr(obj, attr, cast(val))
                if attr == "name":
                    # Mettre à jour le label dans la liste :
                    self.update_current_list_label(val)
            except ValueError:
                pass

    def update_current_list_label(self, new_name):
        obj = self.app.project.current_object
        for item, label in self.gameobject_items:
            if item._linked_object == obj:
                label.configure(text=new_name)

    def update_visibility(self):
        if self.app.project.current_object:
            self.app.project.current_object.visible = bool(self.show_checkbox.get())

    def refresh_fields(self):
        obj = self.app.project.current_object
        if obj:
            self.entry_gameobject_name.delete(0, tk.END)
            self.entry_gameobject_name.insert(0, obj.name)
            self.entry_x.delete(0, tk.END)
            self.entry_x.insert(0, str(obj.x))
            self.entry_y.delete(0, tk.END)
            self.entry_y.insert(0, str(obj.y))
            self.entry_size.delete(0, tk.END)
            self.entry_size.insert(0, str(obj.size))
            self.entry_direction.delete(0, tk.END)
            self.entry_direction.insert(0, str(obj.direction))
            self.show_checkbox.select() if obj.visible else self.show_checkbox.deselect()

            # Cacher/afficher info frame selon background :
            if obj.is_background:
                if self.gameobject_info.winfo_manager():
                    self.gameobject_info.grid_forget()
            else:
                if not self.gameobject_info.winfo_manager():
                    self.gameobject_info.grid(row=0, column=0, sticky="ew", padx=10, pady=(5, 2))

    def setup_gameobject_list(self):
        get_text = lambda p: self.app.language_manager.get(p)
        self.selected_item = None

        self.gameobject_stage_row = ctk.CTkFrame(self)
        self.gameobject_stage_row.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        gameobject_list_container = ctk.CTkFrame(self.gameobject_stage_row, fg_color=["#d7ccfc", "#2b2d42"])
        gameobject_list_container.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        gameobject_list_container.rowconfigure(0, weight=1)
        gameobject_list_container.rowconfigure(1, weight=0)
        gameobject_list_container.columnconfigure(0, weight=1)

        self.scrollable_gameobjects = ctk.CTkScrollableFrame(gameobject_list_container, fg_color=["#d7ccfc", "#2b2d42"])
        self.scrollable_gameobjects.grid(row=0, column=0, sticky="nsew", padx=5, pady=(5, 0))

        self.gameobject_items = []
        self.refresh_gameobject_list()

        add_gameobject_btn = ctk.CTkButton(
            gameobject_list_container,
            text=get_text("gameobjects.add"),
            command=self.add_gameobject
        )
        add_gameobject_btn.grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 10))
        self.app.add_refresh(lambda: add_gameobject_btn.configure(text=get_text("gameobjects.add")))

        stage_frame = ctk.CTkFrame(self.gameobject_stage_row)
        stage_frame.pack(side="right", fill="y", padx=5, pady=5)

        label_stage = ctk.CTkLabel(stage_frame, text=get_text("stage.label"))
        label_stage.pack()
        self.app.add_refresh(lambda: label_stage.configure(text=get_text("stage.label")))

        label_backdrops = ctk.CTkLabel(stage_frame, text=get_text("stage.backdrops") + "\n1")
        label_backdrops.pack()
        self.app.add_refresh(lambda: label_backdrops.configure(text=get_text("stage.backdrops") + "\n1"))

        add_stage_btn = ctk.CTkButton(stage_frame, text="＋", width=40)
        add_stage_btn.pack(pady=10)

    def refresh_gameobject_list(self):
        for widget in self.scrollable_gameobjects.winfo_children():
            widget.destroy()
        self.gameobject_items.clear()
        self.selected_item = None

        for obj in self.app.project.game_objects:
            if obj.is_background:
                continue#cas particulier pour le fond d'écran
            item = ctk.CTkFrame(self.scrollable_gameobjects, fg_color=["#c4b5fd", "#414361"], cursor="hand2")
            item.pack(padx=5, pady=5, fill="x")
            label_icon = ctk.CTkLabel(item, text="🔁", width=30)
            label_icon.pack(side="left", padx=5)
            label_name = ctk.CTkLabel(item, text=obj.name)
            label_name.pack(side="left")

            item._linked_object = obj

            def on_click(o=obj, i=item):
                self.app.project.current_object = o
                self.refresh_fields()
                self.set_selected_item(i)

            item.bind("<Button-1>", lambda e, o=obj, i=item: on_click(o, i))
            label_icon.bind("<Button-1>", lambda e, o=obj, i=item: on_click(o, i))
            label_name.bind("<Button-1>", lambda e, o=obj, i=item: on_click(o, i))

            def on_hover_enter(event, item=item):
                if self.selected_item != item:
                    item.configure(fg_color=["#b5aaf0", "#363654"])

            def on_hover_leave(event, item=item):
                if self.selected_item != item:
                    item.configure(fg_color=["#c4b5fd", "#414361"])

            item.bind("<Enter>", partial(on_hover_enter, item=item))
            item.bind("<Leave>", partial(on_hover_leave, item=item))
            label_icon.bind("<Enter>", partial(on_hover_enter, item=item))
            label_icon.bind("<Leave>", partial(on_hover_leave, item=item))
            label_name.bind("<Enter>", partial(on_hover_enter, item=item))
            label_name.bind("<Leave>", partial(on_hover_leave, item=item))

            settings_btn = ctk.CTkButton(item, text="⋮", width=20)
            functional_open_settings = partial(self.open_settings_popup, obj=obj, item=item, settings_btn=settings_btn)
            settings_btn.configure(command=functional_open_settings)
            settings_btn.pack(side="right", padx=5)
            item.bind("<Button-3>", functional_open_settings)
            label_icon.bind("<Button-3>", functional_open_settings)
            label_name.bind("<Button-3>", functional_open_settings)

            self.gameobject_items.append((item, label_name))
            if self.app.project.current_object == obj:
                self.set_selected_item(item)

    def set_selected_item(self, item):
        # Déselectionner l'ancien
        if self.selected_item:
            self.selected_item.configure(fg_color=["#c4b5fd", "#414361"])

        # Sélectionner le nouveau
        self.selected_item = item
        item.configure(fg_color=["#8b5cf6", "#5755a1"])


    def add_gameobject(self):
        index = 1
        while any(obj.name == f"Object ({index})" for obj in self.app.project.game_objects):
            index += 1
        new_obj = GameObject(f"Object ({index})")
        self.app.project.add_game_object(new_obj)
        self.app.project.current_object = new_obj
        self.refresh_gameobject_list()
        self.refresh_fields()

    def open_settings_popup(self, event=None, obj=None, item=None, settings_btn=None):
        get_text = lambda p: self.app.language_manager.get(p)
        for w in item.winfo_toplevel().winfo_children():
            if isinstance(w, tk.Toplevel) and hasattr(w, 'is_gameobject_popup'):
                w.destroy()

        popup = tk.Toplevel(bg=item.winfo_toplevel().cget("bg"))
        popup.overrideredirect(True)
        popup.is_gameobject_popup = True
        popup.attributes("-topmost", True)

        bx, by, bw, bh = settings_btn.winfo_rootx(), settings_btn.winfo_rooty(), settings_btn.winfo_width(), settings_btn.winfo_height()
        popup.geometry(f"280x400+{bx-(240//2)}+{by - 400}")

        popup_frame = ctk.CTkFrame(popup)
        popup_frame.pack(fill="both", expand=True)

        def make_command(text_key):
            return lambda: print(f"{get_text(text_key)} pressed")

        def confirm_delete():
            popup.destroy()
            if tk.messagebox.askyesno(get_text("gameobjects.popup.delete_confirm.title"), get_text("gameobjects.popup.delete_confirm.message")):
                item.focus_force()
                self.app.project.remove_game_object(obj)
                self.app.project.current_object = self.app.project.game_objects[-1] if len(self.app.project.game_objects) > 0 else None
                self.refresh_gameobject_list()
                self.refresh_fields()

        actions = [
            ("gameobjects.popup.bring_forward", make_command("gameobjects.popup.bring_forward")),
            ("gameobjects.popup.send_backward", make_command("gameobjects.popup.send_backward")),
            ("gameobjects.popup.front", make_command("gameobjects.popup.front")),
            ("gameobjects.popup.back", make_command("gameobjects.popup.back")),
            ("gameobjects.popup.delete", confirm_delete),
        ]

        for key, cmd in actions:
            b = ctk.CTkButton(popup_frame, text=get_text(key), command=cmd)
            b.pack(fill="x", padx=5, pady=2)

        def on_focus_out(event):
            popup.destroy()

        popup.bind("<FocusOut>", on_focus_out)
        popup.focus_force()
