from enum import Enum
from modules.svg import *

class BlockShape(Enum):
    Hat = "hat" # Forme chapeau (début de script)
    StackTop = "stack_top" # Début de pile
    StackBottom = "stack_bottom" # Bas de pile
    CBlock = "c_block" # Bloc conteneur
    Cap = "cap" # Fin de script (stop all)
    Reporter = "reporter" # Bloc arrondi (renvoie une valeur)
    Boolean = "boolean" # Bloc hexagonal (condition)

SHAPES = {
    BlockShape.Hat: "m 0 17 c 25 -22 71 -22 96 0 h $width a 4 4 0 0 1 4 4 v $height",
    BlockShape.StackTop: "m 0 4 a 4 4 0 0 1 4 -4 h 8 c 2 0 3 1 4 2 l 4 4 c 1 1 2 2 4 2 h 12 c 2 0 3 -1 4 -2 l 4 -4 c 1 -1 2 -2 4 -2 h $width a 4 4 0 0 1 4 4 v $height",
    BlockShape.StackBottom: "a 4 4 0 0 1 -4 4 H 48 c -2 0 -3 1 -4 2 l -4 4 c -1 1 -2 2 -4 2 h -12 c -2 0 -3 -1 -4 -2 l -4 -4 c -1 -1 -2 -2 -4 -2 H 4 a 4 4 0 0 1 -4 -4 z",
    BlockShape.CBlock: "a 4 4 0 0 1 -4 4 H 64 c -2 0 -3 1 -4 2 l -4 4 c -1 1 -2 2 -4 2 h -12 c -2 0 -3 -1 -4 -2 l -4 -4 c -1 -1 -2 -2 -4 -2 H 20 a 4 4 0 0 0 -4 4 v $space a 4 4 0 0 0 4 4 h 8 c 2 0 3 1 4 2 l 4 4 c 1 1 2 2 4 2 h 12 c 2 0 3 -1 4 -2 l 4 -4 c 1 -1 2 -2 4 -2 h $width a 4 4 0 0 1 4 4 v $height",
    BlockShape.Cap: "a 4 4 0 0 1 -4 4 H 4 a 4 4 0 0 1 -4 -4 z",
    BlockShape.Reporter: "m 55 0 H 55 a 20 20 0 0 1 0 40 H 20 A 20 20 0 0 1 20 0 z",
    BlockShape.Boolean: "M 120 0 L 140 20 L 120 40 H 20 L 0 20 L 20 0 Z",
}

base_config = {
    BlockShape.Hat: {"width": 43, "height": 8},
    BlockShape.StackTop: {"width": 127, "height": 8},
    BlockShape.CBlock: {"width": 92, "height": 8, "space": 16},
}

class BlockPartType(Enum):
    LABEL = "label"       # Texte statique
    REPORTER = "reporter" # Slot pour valeur ou bloc
    BOOLEAN = "boolean"   # Slot pour condition
    DROPDOWN = "dropdown" # Liste déroulante
    INPUT = "input"       # Champ texte / nombre

class Branch:
    def __init__(self, name, top=None, body=None):
        self.name = name
        self.top = top or []
        self.body = body or []

    def to_dict(self):
        return {
            "top": [(part.value, value) for part, value in self.top],
            "body": [b.to_dict() for b in self.body]  # Si sous-blocs
        }

class Block:
    def __init__(self, master):
        self.master = master
        self.id = "control_ifelse"
        self.shape = []
        self.fill_color = "#ffab19"
        self.stroke_color = "#cf8b17"
        self.branches = []
        self.next_block = None

    def add_shape(self, shape):
        if not isinstance(shape, BlockShape):
            raise ValueError("Shape must be an instance of BlockShape Enum")
        if (len(self.shape) > 1 and BlockShape.Reporter in self.shape or BlockShape.Boolean in self.shape) or \
            (shape in [BlockShape.Reporter, BlockShape.Boolean] and len(self.shape) != 0):
            raise ValueError("Reporter or Boolean can only be the single element in the shape list")
        if len(self.shape) == 0 and shape not in [BlockShape.Hat, BlockShape.StackTop]:
            raise ValueError("First shape must be Hat or StackTop")
        if len(self.shape) > 0 and shape in [BlockShape.Hat, BlockShape.StackTop]:
            raise ValueError("Hat or StackTop cannot be added after the first shape")
        if len(self.shape) > 0 and self.shape[-1] in [BlockShape.StackBottom, BlockShape.Cap]:
            raise ValueError("Cannot add shapes after StackBottom or Cap")
        self.shape.append(shape)
    
    def add_branch(self, branch):
        self.branches.append(branch)

    def build_svg(self, config=None):
        if len(self.shape) == 0:
            raise ValueError("Block must have at least one shape")
        if self.shape[-1] not in [BlockShape.StackBottom, BlockShape.Cap, BlockShape.Reporter, BlockShape.Boolean]:
            raise ValueError("Last shape must be StackBottom, Cap, Reporter or Boolean")
        parts = []
        config_idx = 0
        for idx, shape in enumerate(self.shape):
            raw = SHAPES[shape]
            part = raw.strip()
            if shape in base_config:
                shape_config = base_config[shape].copy()
                if config and config_idx < len(config):
                    for key in shape_config.keys():
                        if key in config[config_idx]:
                            shape_config[key] = config[config_idx][key]
                    config_idx += 1
                for key, value in shape_config.items():
                    value = max(value - 8, 0)
                    part = part.replace(f"${key}", str(value))
            parts.append(part)
        path_svg = " ".join(parts)
        svg = SVG()
        svg.add_widget(PathSVG(
            path=path_svg,
            fill_color=self.fill_color,
            border_color=self.stroke_color,
            stroke_width=2,
            viewbox=ViewBox(0, 0, 2, 2),
        ))
        return svg

if True :#__name__ == "__main__":
    # Example usage
    block_test = Block(None)
    block_test.add_shape(BlockShape.Hat)
    block_test.add_shape(BlockShape.CBlock)
    block_test.add_shape(BlockShape.CBlock)
    block_test.add_shape(BlockShape.StackBottom)
    block_test.add_branch(Branch("if", [(BlockPartType.LABEL, "if"), (BlockPartType.BOOLEAN, None), (BlockPartType.LABEL, "then")]))
    block_test.add_branch(Branch("else", [(BlockPartType.LABEL, "else")]))
    svg = block_test.build_svg(config=[{"width": 150, "height": 10, "space": 22}, {"width": 145, "height": 8, "space": 12}])
    img = svg.draw(background_color=(255, 255, 255, 0))  # Transparent background
    img.show()
