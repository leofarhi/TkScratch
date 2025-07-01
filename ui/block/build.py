#part
from PIL import Image, ImageDraw

hat = "m 0 0 c 25 -22 71 -22 96 0 h 43 a 4 4 0 0 1 4 4 v 5 H 0 z"

stack_top = "m 0 4 a 4 4 0 0 1 4 -4 h 8 c 2 0 3 1 4 2 l 4 4 c 1 1 2 2 4 2 h 12 c 2 0 3 -1 4 -2 l 4 -4 c 1 -1 2 -2 4 -2 h 127 a 4 4 0 0 1 4 4 v 4 H 0 z"
stack_bottom = "m 0 0 h 149 v 4 a 4 4 0 0 1 -4 4 H 48 c -2 0 -3 1 -4 2 l -4 4 c -1 1 -2 2 -4 2 h -12 c -2 0 -3 -1 -4 -2 l -4 -4 c -1 -1 -2 -2 -4 -2 H 4 a 4 4 0 0 1 -4 -4 z"

c_block = "m 0 0 h 160 v 4 a 4 4 0 0 1 -4 4 H 64 c -2 0 -3 1 -4 2 l -4 4 c -1 1 -2 2 -4 2 h -12 c -2 0 -3 -1 -4 -2 l -4 -4 c -1 -1 -2 -2 -4 -2 H 20 a 4 4 0 0 0 -4 4 v 16 a 4 4 0 0 0 4 4 h 8 c 2 0 3 1 4 2 l 4 4 c 1 1 2 2 4 2 h 12 c 2 0 3 -1 4 -2 l 4 -4 c 1 -1 2 -2 4 -2 h 92 a 4 4 0 0 1 4 4 v 4 H 0 z"

cap = "m 0 0 h 149 v 4 a 4 4 0 0 1 -4 4 H 4 a 4 4 0 0 1 -4 -4 z"
reporter = "m 55 0 H 55 a 20 20 0 0 1 0 40 H 20 A 20 20 0 0 1 20 0 z"
boolean = "M 120 0 L 140 20 L 120 40 H 20 L 0 20 L 20 0 Z"






from enum import Enum

class Shape(Enum):
    Hat = "hat"
    StackTop = "stack_top"
    StackBottom = "stack_bottom"
    CBlock = "c_block"
    Cap = "cap"
    Reporter = "reporter"
    Boolean = "boolean"

SHAPES = {
    Shape.Hat: "m 0 0 c 25 -22 71 -22 96 0 h $width a 4 4 0 0 1 4 4 v $height H 0 z",
    Shape.StackTop: "m 0 4 a 4 4 0 0 1 4 -4 h 8 c 2 0 3 1 4 2 l 4 4 c 1 1 2 2 4 2 h 12 c 2 0 3 -1 4 -2 l 4 -4 c 1 -1 2 -2 4 -2 h $width a 4 4 0 0 1 4 4 v $height H 0 z",
    Shape.StackBottom: "m 0 0 h 149 v 4 a 4 4 0 0 1 -4 4 H 48 c -2 0 -3 1 -4 2 l -4 4 c -1 1 -2 2 -4 2 h -12 c -2 0 -3 -1 -4 -2 l -4 -4 c -1 -1 -2 -2 -4 -2 H 4 a 4 4 0 0 1 -4 -4 z",
    Shape.CBlock: "m 0 0 h 160 v 4 a 4 4 0 0 1 -4 4 H 64 c -2 0 -3 1 -4 2 l -4 4 c -1 1 -2 2 -4 2 h -12 c -2 0 -3 -1 -4 -2 l -4 -4 c -1 -1 -2 -2 -4 -2 H 20 a 4 4 0 0 0 -4 4 v $space a 4 4 0 0 0 4 4 h 8 c 2 0 3 1 4 2 l 4 4 c 1 1 2 2 4 2 h 12 c 2 0 3 -1 4 -2 l 4 -4 c 1 -1 2 -2 4 -2 h $width a 4 4 0 0 1 4 4 v $height H 0 z",
    Shape.Cap: "m 0 0 h 149 v 4 a 4 4 0 0 1 -4 4 H 4 a 4 4 0 0 1 -4 -4 z",
    Shape.Reporter: "m 55 0 H 55 a 20 20 0 0 1 0 40 H 20 A 20 20 0 0 1 20 0 z",
    Shape.Boolean: "M 120 0 L 140 20 L 120 40 H 20 L 0 20 L 20 0 Z",
}

base_config = {
    Shape.Hat: {"width": 43, "height": 8},
    Shape.StackTop: {"width": 127, "height": 8},
    Shape.CBlock: {"width": 92, "height": 8, "space": 16},
}

def clean_path(shape, path, is_first=False, is_last=False):
    path = path.strip()
    if shape == Shape.Hat:
        if "H 0 z" in path:
            path = path.replace("H 0 z", "").strip()
    elif shape == Shape.StackBottom:
        if path.startswith("m 0 0 h 149 v 4"):
            path = path[len("m 0 0 h 149 v 4"):].strip()
    elif shape == Shape.Cap:
        if path.startswith("m 0 0 h 149 v 4"):
            path = path[len("m 0 0 h 149 v 4"):].strip()
    elif shape == Shape.CBlock:
        if path.startswith("m 0 0 h 160 v 4"):
            path = path[len("m 0 0 h 160 v 4"):].strip()
    if not is_first:
        if path.startswith("m") or path.startswith("M"):
            path = path.split(" ", 2)[2]
    if not is_last:
        # pour StackTop et CBlock, remplacer fermeture par v 4
        if "H 0 z" in path:
            path = path.replace("H 0 z", "").strip()
        elif path.endswith("z"):
            path = path[:-1].strip()
    return path

def combine(shapes, config = None):
    config_idx = 0
    parts = []
    count = len(shapes)
    for idx, shape in enumerate(shapes):
        raw = SHAPES[shape]
        part = clean_path(
            shape,
            raw,
            is_first=(idx == 0),
            is_last=(idx == count - 1)
        )
        shape_config = base_config.get(shape, {})
        if config and config_idx < len(config):
            for key in shape_config.keys():
                if key in config[config_idx]:
                    shape_config[key] = config[config_idx][key]
            config_idx += 1
        for key, value in shape_config.items():
            value = max(value - 8, 0)
            part = part.replace(f"${key}", str(value))
        parts.append(part)
    return " ".join(parts)

config = [
    {"width": 150, "height": 10},
    {"width": 145, "height": 8, "space": 12}
]

# ✅ Test complexe :
print(combine([Shape.StackTop, Shape.CBlock, Shape.Cap], config))
print()

def sp_shape_size(shape, width, height):
    if shape == Shape.Reporter:
        width = max(width, 0) + 40
        height = max(height, 0) + 40
        r = 20
        x0 = max(r, (width - 40) / 2)
        x1 = width - x0
        w = x1 - x0
        translation_x = height/2
        return f"m {translation_x:.2f} 0 H {(w + translation_x):.2f} a {r} {r} 0 0 1 0 {height:.2f} H {translation_x:.2f} A {r} {r} 0 0 1 {translation_x:.2f} 0 z"
    elif shape == Shape.Boolean:
        point_depth = 20
        width = max(width, 0) + point_depth * 2
        height = max(height, 0) + point_depth * 2
        mid_height = height / 2

        start_x = width - point_depth
        tip_x = width
        base_x = point_depth

        return (
            f"M {start_x:.2f} 0 "
            f"L {tip_x:.2f} {mid_height:.2f} "
            f"L {start_x:.2f} {height:.2f} "
            f"H {base_x:.2f} "
            f"L 0 {mid_height:.2f} "
            f"L {base_x:.2f} 0 Z"
        )


# ✅ Exemples
print(sp_shape_size(Shape.Boolean, width=26, height=0))
print()
print(sp_shape_size(Shape.Boolean, width=0, height=0))
print()
print(sp_shape_size(Shape.Boolean, width=50, height=0))

quit()






p1 = [(1.0, 0.0), (9.088, -5.94), (18.184, -10.56), (28.036, -13.86), (38.392, -15.84), (49.0, -16.5), (59.608, -15.84), (69.964, -13.86), (79.816, -10.56), (88.912, -5.94), (97.0, 0.0), (101.316, 0.0), (105.631, 0.0), (109.947, 0.0), (114.263, 0.0), (118.578, 0.0), (122.894, 0.0), (127.209, 0.0), (131.525, 0.0), (135.841, 0.0), (140.156, 0.0), (140.782, 0.049), (141.392, 0.196), (141.972, 0.436), (142.507, 0.764), (142.985, 1.172), (143.392, 1.649), (143.72, 2.184), (143.96, 2.764), (144.107, 3.374), (144.156, 4.0), (144.156, 8.0), (144.156, 12.0), (144.156, 16.0), (144.156, 20.0), (144.156, 24.0), (144.156, 28.0), (144.156, 32.0), (144.156, 36.0), (144.156, 40.0), (144.156, 44.0), (144.107, 44.626), (143.96, 45.236), (143.72, 45.816), (143.392, 46.351), (142.985, 46.828), (142.507, 47.236), (141.972, 47.564), (141.392, 47.804), (140.782, 47.951), (140.156, 48.0), (131.041, 48.0), (121.925, 48.0), (112.809, 48.0), (103.694, 48.0), (94.578, 48.0), (85.463, 48.0), (76.347, 48.0), (67.231, 48.0), (58.116, 48.0), (49.0, 48.0), (48.429, 48.029), (47.912, 48.112), (47.443, 48.243), (47.016, 48.416), (46.625, 48.625), (46.264, 48.864), (45.927, 49.127), (45.608, 49.408), (45.301, 49.701), (45.0, 50.0), (44.6, 50.4), (44.2, 50.8), (43.8, 51.2), (43.4, 51.6), (43.0, 52.0), (42.6, 52.4), (42.2, 52.8), (41.8, 53.2), (41.4, 53.6), (41.0, 54.0), (40.699, 54.299), (40.392, 54.592), (40.073, 54.873), (39.736, 55.136), (39.375, 55.375), (38.984, 55.584), (38.557, 55.757), (38.088, 55.888), (37.571, 55.971), (37.0, 56.0), (35.8, 56.0), (34.6, 56.0), (33.4, 56.0), (32.2, 56.0), (31.0, 56.0), (29.8, 56.0), (28.6, 56.0), (27.4, 56.0), (26.2, 56.0), (25.0, 56.0), (24.429, 55.971), (23.912, 55.888), (23.443, 55.757), (23.016, 55.584), (22.625, 55.375), (22.264, 55.136), (21.927, 54.873), (21.608, 54.592), (21.301, 54.299), (21.0, 54.0), (20.6, 53.6), (20.2, 53.2), (19.8, 52.8), (19.4, 52.4), (19.0, 52.0), (18.6, 51.6), (18.2, 51.2), (17.8, 50.8), (17.4, 50.4), (17.0, 50.0), (16.699, 49.701), (16.392, 49.408), (16.073, 49.127), (15.736, 48.864), (15.375, 48.625), (14.984, 48.416), (14.557, 48.243), (14.088, 48.112), (13.571, 48.029), (13.0, 48.0), (12.2, 48.0), (11.4, 48.0), (10.6, 48.0), (9.8, 48.0), (9.0, 48.0), (8.2, 48.0), (7.4, 48.0), (6.6, 48.0), (5.8, 48.0), (5.0, 48.0), (4.374, 47.951), (3.764, 47.804), (3.184, 47.564), (2.649, 47.236), (2.172, 46.828), (1.764, 46.351), (1.436, 45.816), (1.196, 45.236), (1.049, 44.626), (1.0, 44.0), (1.0, 39.6), (1.0, 35.2), (1.0, 30.8), (1.0, 26.4), (1.0, 22.0), (1.0, 17.6), (1.0, 13.2), (1.0, 8.8), (1.0, 4.4), (1.0, 0.0)]
img = img = Image.new("RGBA", (200, 200), (255, 255, 255, 0))
draw = ImageDraw.Draw(img)

p1 = [(x, y +20) for x, y in p1]  # Scale points for better visibility

draw.polygon(p1+[p1[0]], fill=(0, 255, 0))
img.show()

class BlockBuilder:
    def __init__(self, block):
        self.block = block

    def build(self):
        # Placeholder for the actual build logic
        # This should return a UI component or a representation of the block
        return f"Building block: {self.block}"