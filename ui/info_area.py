import customtkinter as ctk
import tkinter as tk

class InfoArea(ctk.CTkFrame):
    def __init__(self, app, master, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.pack_propagate(False)
        self.setup_gameobject_info()
        self.setup_gameobject_list()

    def setup_gameobject_info(self):
        get_text = lambda p: self.app.language_manager.get(p)
        self.gameobject_info = ctk.CTkFrame(self, fg_color=["#f0f0f0", "#1a1a1a"])
        self.gameobject_info.pack(fill="x", pady=(5, 2), padx=10)

        # Colonnes : 0=label, 1=entry, 2=label, 3=entry, 4=label, 5=entry
        # Seules les colonnes des ENTRY ont weight=1
        self.gameobject_info.grid_columnconfigure(1, weight=1)
        self.gameobject_info.grid_columnconfigure(3, weight=1)
        self.gameobject_info.grid_columnconfigure(5, weight=1)

        self.gameobject_name_label = ctk.CTkLabel(self.gameobject_info, text=get_text("gameobject.name"))
        self.gameobject_name_label.grid(row=0, column=0, padx=5, pady=5)
        self.app.add_refresh(lambda: self.gameobject_name_label.configure(text=get_text("gameobject.name")))

        self.entry_gameobject_name = ctk.CTkEntry(self.gameobject_info, placeholder_text=get_text("gameobject.name_placeholder"))
        self.entry_gameobject_name.grid(row=0, column=1, padx=5, sticky="ew")
        self.app.add_refresh(lambda: self.entry_gameobject_name.configure(placeholder_text=get_text("gameobject.name_placeholder")))

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
        self.app.add_refresh(lambda: self.show_checkbox.configure(text=get_text("gameobject.show")))

        self.label_size = ctk.CTkLabel(self.gameobject_info, text=get_text("gameobject.size"))
        self.label_size.grid(row=1, column=2)
        self.app.add_refresh(lambda: self.label_size.configure(text=get_text("gameobject.size")))

        self.entry_size = ctk.CTkEntry(self.gameobject_info, placeholder_text="100")
        self.entry_size.grid(row=1, column=3, padx=5, sticky="ew")

        self.label_direction = ctk.CTkLabel(self.gameobject_info, text=get_text("gameobject.direction"))
        self.label_direction.grid(row=1, column=4)
        self.app.add_refresh(lambda: self.label_direction.configure(text=get_text("gameobject.direction")))

        self.entry_direction = ctk.CTkEntry(self.gameobject_info, placeholder_text="90")
        self.entry_direction.grid(row=1, column=5, padx=5, sticky="ew")


    def setup_gameobject_list(self):
        get_text = lambda p: self.app.language_manager.get(p)
        # === Liste des gameobjects + Stage ===
        gameobject_stage_row = ctk.CTkFrame(self)
        gameobject_stage_row.pack(fill="both", expand=True, padx=5, pady=5)

        # === Liste des gameobjects ===
        gameobject_list_container = ctk.CTkFrame(gameobject_stage_row, fg_color=["#d7ccfc", "#2b2d42"])
        gameobject_list_container.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        gameobject_list_container.rowconfigure(0, weight=1)
        gameobject_list_container.rowconfigure(1, weight=0)  # fixe
        gameobject_list_container.columnconfigure(0, weight=1)

        scrollable_gameobjects = ctk.CTkScrollableFrame(gameobject_list_container, fg_color=["#d7ccfc", "#2b2d42"])
        scrollable_gameobjects.grid(row=0, column=0, sticky="nsew", padx=5, pady=(5,0))

        gameobject_counter = [1]  # compteur mutable

        def add_gameobject():
            index = gameobject_counter[0]
            gameobject_counter[0] += 1

            item = ctk.CTkFrame(scrollable_gameobjects, fg_color=["#c4b5fd", "#414361"], cursor="hand2")
            item.pack(padx=5, pady=5, fill="x")

            def on_item_click(event=None):
                print(f"Clicked on GameObject{index}")  # remplace par ta logique de sélection

            item.bind("<Button-1>", on_item_click)
            def on_hover_enter(event):
                item.configure(fg_color=["#b5aaf0", "#363654"])

            def on_hover_leave(event):
                item.configure(fg_color=["#c4b5fd", "#414361"])

            item.bind("<Enter>", on_hover_enter)
            item.bind("<Leave>", on_hover_leave)


            label_icon = ctk.CTkLabel(item, text="🔁", width=30)
            label_icon.pack(side="left", padx=5)
            label_icon.bind("<Button-1>", on_item_click)  # clic sur l'icône
            label_icon.bind("<Enter>", on_hover_enter)
            label_icon.bind("<Leave>", on_hover_leave)
            label_name = ctk.CTkLabel(item, text=f"GameObject {index}")
            label_name.pack(side="left")
            label_name.bind("<Button-1>", on_item_click)  # clic sur le nom
            label_name.bind("<Enter>", on_hover_enter)
            label_name.bind("<Leave>", on_hover_leave)

            def open_settings_popup(event=None):
                # Ferme d'autres popups potentiels
                for w in item.winfo_toplevel().winfo_children():
                    if isinstance(w, tk.Toplevel) and hasattr(w, 'is_gameobject_popup'):
                        w.destroy()

                popup = tk.Toplevel(bg=item.winfo_toplevel().cget("bg"))
                popup.overrideredirect(True)
                popup.is_gameobject_popup = True
                popup.attributes("-topmost", True)

                # Positionner le popup au-dessus du bouton
                bx, by, bw, bh = settings_btn.winfo_rootx(), settings_btn.winfo_rooty(), settings_btn.winfo_width(), settings_btn.winfo_height()
                popup.geometry(f"280x400+{bx-(240//2)}+{by - 400}")

                popup_frame = ctk.CTkFrame(popup)
                popup_frame.pack(fill="both", expand=True)

                def make_command(text_key):
                    return lambda: print(f"{get_text(text_key)} pressed")

                def confirm_delete():
                    popup.destroy()
                    if tk.messagebox.askyesno(get_text("gameobjects.popup.delete_confirm.title"), get_text("gameobjects.popup.delete_confirm.message")):
                        item.destroy()

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

            settings_btn = ctk.CTkButton(item, text="⋮", width=20, command=open_settings_popup)
            settings_btn.pack(side="right", padx=5)
            #add right-click on item/label_icon/label_name to open the popup
            item.bind("<Button-3>", open_settings_popup)
            label_icon.bind("<Button-3>", open_settings_popup)  # clic droit sur l'icône
            label_name.bind("<Button-3>", open_settings_popup)  # clic droit sur le nom

        # GameObject de base
        add_gameobject()

        # Bouton d'ajout
        add_gameobject_btn = ctk.CTkButton(
            gameobject_list_container,
            text=get_text("gameobjects.add"),
            command=add_gameobject
        )
        add_gameobject_btn.grid(row=1, column=0, sticky="ew", padx=5, pady=(0,10))
        self.app.add_refresh(lambda: add_gameobject_btn.configure(text=get_text("gameobjects.add")))


        # === Stage ===
        stage_frame = ctk.CTkFrame(gameobject_stage_row)
        stage_frame.pack(side="right", fill="y", padx=5, pady=5)

        label_stage = ctk.CTkLabel(stage_frame, text=get_text("stage.label"))
        label_stage.pack()
        self.app.add_refresh(lambda: label_stage.configure(text=get_text("stage.label")))

        label_backdrops = ctk.CTkLabel(stage_frame, text=get_text("stage.backdrops") + "\n1")
        label_backdrops.pack()
        self.app.add_refresh(lambda: label_backdrops.configure(text=get_text("stage.backdrops") + "\n1"))

        add_stage_btn = ctk.CTkButton(stage_frame, text="＋", width=40)
        add_stage_btn.pack(pady=10)