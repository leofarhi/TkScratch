import customtkinter as ctk
from ui.widgets.SmartCanvas import *
from ui.widgets.utils import *

class CodeArea(ctk.CTkFrame):
    Instance = None
    def __init__(self, app, master, **kwargs):
        super().__init__(master, **kwargs)
        if CodeArea.Instance is not None:
            raise Exception("CodeArea is a singleton, use CodeArea.Instance to access it.")
        CodeArea.Instance = self
        self.app = app
        #label
        self.canvas = SmartCanvas(self, bg="white", callback=self.update_canvas)
        self.canvas.pack(fill="both", expand=True)

    @property
    def code(self):
        """ Returns the code of the current object """
        obj = self.app.project.current_object
        if obj:
            return obj.code
        return []
    
    def drop_block(self, block, x, y):
        """Dépose un bloc sur le canevas à la position (x, y)"""
        obj = self.app.project.current_object
        if obj:
            obj.code.append((block, x, y))

    def update_canvas(self, widget):
        mode = self.app._get_appearance_mode() == "dark"
        widget.surface.fill(tk_color_to_hex(self, self.cget("fg_color")[int(mode)]))
        for code in self.code:
            block, x, y = code
            svg = block.build_svg()
            img = svg.draw(background_color=(255, 255, 255, 0))
            widget.surface.blit(img, (x, y))
        widget.surface.display()