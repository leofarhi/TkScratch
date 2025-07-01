import customtkinter as ctk

class VerticalSegmentedButton(ctk.CTkSegmentedButton):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

    def _create_button_grid(self):
        # remove minsize from every grid cell in the first row
        number_of_columns, _ = self.grid_size()
        for n in range(number_of_columns):
            self.grid_rowconfigure(n, weight=1, minsize=0)
        self.grid_columnconfigure(0, weight=1)

        for index, value in enumerate(self._value_list):
            self.grid_rowconfigure(index, weight=1, minsize=self._current_height)
            self._buttons_dict[value].grid(row=index, column=0, sticky="nsew", padx=2, pady=2)
    @staticmethod
    def create_by(button: ctk.CTkSegmentedButton):
        """
        Create a VerticalSegmentedButton from an existing CTkSegmentedButton.
        This is useful to convert a horizontal segmented button to a vertical one.
        """
        new_button = VerticalSegmentedButton(button.master, values=button._value_list,
                                             fg_color=button._sb_fg_color, selected_color=button._sb_selected_color,
                                             selected_hover_color=button._sb_selected_hover_color,
                                             unselected_color=button._sb_unselected_color,
                                             unselected_hover_color=button._sb_unselected_hover_color,
                                             text_color=button._sb_text_color, text_color_disabled=button._sb_text_color_disabled,
                                             corner_radius=button._corner_radius, border_width=button._border_width,
                                             command=button._command, state=button._state, font=button._font)
        return new_button
    
    def _configure_button_corners_for_index(self, index: int):
        if self._background_corner_colors is None:
            self._buttons_dict[self._value_list[index]].configure(background_corner_colors=(self._bg_color, self._bg_color, self._bg_color, self._bg_color))
        else:
            self._buttons_dict[self._value_list[index]].configure(background_corner_colors=self._background_corner_colors)
