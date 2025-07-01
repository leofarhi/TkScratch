import customtkinter as ctk
from ui.widgets.VerticalSegmentedButton import VerticalSegmentedButton

class VerticalTabview(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        #self._segmented_button._font = ctk.CTkFont(size=10)  # Set a default font size for the segmented button
        old_segmented_button = self._segmented_button
        self._segmented_button = VerticalSegmentedButton.create_by(self._segmented_button)
        old_segmented_button.destroy()  # Remove the old horizontal segmented button

    def _configure_grid(self):
        self.grid_rowconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=0)  # colonne pour _segmented_button
        self.grid_columnconfigure(1, weight=1)  # colonne pour _canvas (prend l'espace restant)

    def _set_grid_canvas(self):
        self._canvas.grid(row=0, column=1, sticky="nsew")

    def _set_grid_segmented_button(self):
        self._segmented_button.grid(
            row=0,
            column=0,
            sticky="nsw"
        )

    def _set_grid_current_tab(self):
        self._tab_dict[self._current_name].grid(
            row=0,
            column=1,  # même colonne que le canvas
            sticky="nsew",
        )

