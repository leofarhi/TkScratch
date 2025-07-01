from importlib.resources import path
from svgpathtools import parse_path, Line, CubicBezier, QuadraticBezier, Arc
from PIL import Image, ImageDraw, ImageFont

class ViewBox:
    def __init__(self, x, y, scaleW, scaleH):
        """
        :param x: Position X du coin supérieur gauche du ViewBox
        :param y: Position Y du coin supérieur gauche du ViewBox
        :param scaleW: Proportion de la largeur du ViewBox par rapport à l'élément SVG (0.0 à 1.0)
        :param scaleH: Proportion de la hauteur du ViewBox par rapport à l'élément SVG (0.0 à 1.0)
        """
        self.x = x
        self.y = y
        self.scaleW = scaleW
        self.scaleH = scaleH

class Region:
    def __init__(self, offset, size):
        self.offset = offset
        self.size = size

class WidgetSVG:
    def __init__(self):
        pass

    @property
    def region(self):
        raise NotImplementedError("Subclasses should implement this method.")
    
    def draw(self, canvas: ImageDraw):
        raise NotImplementedError("Subclasses should implement this method.")

class PathSVG(WidgetSVG):
    def __init__(self, path, border_color=(0, 0, 0), fill_color= None, viewbox=None, stroke_width=1, curve_resolution=20):
        super().__init__()
        self.path = parse_path(path)
        self.border_color = border_color
        self.fill_color = fill_color
        self.viewbox = viewbox if isinstance(viewbox, ViewBox) and viewbox != None else ViewBox(0, 0, 1, 1)
        self.stroke_width = stroke_width
        self.curve_resolution = curve_resolution
        self._region = self._get_region()
        if self.region.size[0] <= 0 or self.region.size[1] <= 0:
            self.subpaths = []
        else:
            self.subpaths = self._get_subpaths()

    @property
    def region(self):
        return self._region

    def _get_region(self, curve_resolution=20):
        min_x, min_y = float('inf'), float('inf')
        max_x, max_y = float('-inf'), float('-inf')
        for segment in self.path:
            points = [segment.point(t / curve_resolution) for t in range(curve_resolution + 1)]
            for pt in points:
                x, y = pt.real, pt.imag
                min_x, min_y = min(min_x, x), min(min_y, y)
                max_x, max_y = max(max_x, x), max(max_y, y)
        width, height = max_x - min_x, max_y - min_y
        #add border width to the region size
        width += self.stroke_width * 2
        height += self.stroke_width * 2
        min_x -= self.stroke_width
        min_y -= self.stroke_width
        return Region((min_x * self.viewbox.scaleW + self.viewbox.x, min_y * self.viewbox.scaleH + self.viewbox.y), (width * self.viewbox.scaleW, height * self.viewbox.scaleH))

    def _get_subpaths(self):
        subpaths = []
        for subpath in self.path.continuous_subpaths():
            points = []
            for segment in subpath:
                if isinstance(segment, (Line, CubicBezier, QuadraticBezier, Arc)):
                    segment_points = [
                        segment.point(t / self.curve_resolution)
                        for t in range(self.curve_resolution + 1)
                    ]
                else:
                    continue
                segment_points = [
                    (
                        (pt.real * self.viewbox.scaleW + self.viewbox.x),
                        (pt.imag * self.viewbox.scaleH + self.viewbox.y)
                    ) for pt in segment_points
                ]
                if not points or points[-1] != segment_points[0]:
                    points.extend(segment_points)
                else:
                    points.extend(segment_points[1:])
            subpaths.append(points)
        return subpaths
    
    def draw(self, canvas: ImageDraw):
        if not self.subpaths:
            return
        for points in self.subpaths:
            if self.fill_color:
                canvas.polygon(points, fill=self.fill_color)
            if self.border_color and self.stroke_width > 0:
                canvas.line(points + [points[0]], fill=self.border_color, width=self.stroke_width)

class TextSVG(WidgetSVG):
    def __init__(self, text, font_path=None, position=(0, 0),
                 font_size=12, font_color=(0, 0, 0),
                 border_color=None, border_width=0):
        super().__init__()
        self.text = text
        self.position = position
        self.font_size = font_size
        self.font_color = font_color

        self.border_color = border_color
        self.border_width = border_width

        if font_path is None:
            self.font = ImageFont.load_default()
        else:
            self.font = ImageFont.truetype(font_path, self.font_size)

    @property
    def region(self):
        bbox = self.font.getbbox(self.text)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        return Region(self.position, (width, height))

    def draw(self, canvas: ImageDraw.ImageDraw):
        if not self.text:
            return

        x, y = self.position

        # Dessiner un contour si demandé
        if self.border_color is not None and self.border_width > 0:
            # Pour simuler un contour, on dessine le texte plusieurs fois autour
            offsets = []
            bw = self.border_width
            for dx in range(-bw, bw + 1):
                for dy in range(-bw, bw + 1):
                    if dx == 0 and dy == 0:
                        continue
                    offsets.append((dx, dy))

            for dx, dy in offsets:
                canvas.text((x + dx, y + dy), self.text, font=self.font, fill=self.border_color)

        # Dessiner le texte principal
        canvas.text(self.position, self.text, fill=self.font_color, font=self.font)


class SVG:
    def __init__(self):
        self.widgets = []
        self.region = Region((0, 0), (0, 0))  # Initial region

    def add_widget(self, widget):
        if isinstance(widget, WidgetSVG):
            self.widgets.append(widget)
        else:
            raise TypeError("Widget must be an instance of WidgetSVG or its subclasses.")
        self._update_dimensions()
    def _update_dimensions(self):
        if not self.widgets:
            self.region = Region((0, 0), (0, 0))
            return
        min_x, min_y = float('inf'), float('inf')
        max_x, max_y = float('-inf'), float('-inf')
        for widget in self.widgets:
            region = widget.region
            min_x = min(min_x, region.offset[0])
            min_y = min(min_y, region.offset[1])
            max_x = max(max_x, region.offset[0] + region.size[0])
            max_y = max(max_y, region.offset[1] + region.size[1])
        self.region.size = (int(max_x - min_x), int(max_y - min_y))
        if self.region.size[0] < 0:
            self.region.size = (0, self.region.size[1])
        if self.region.size[1] < 0:
            self.region.size = (self.region.size[0], 0)

    def draw(self, background_color=(255, 255, 255, 0)):
        canvas = Image.new("RGBA", (self.region.size[0], self.region.size[1]), background_color)
        draw = ImageDraw.Draw(canvas)
        for widget in self.widgets:
            widget.draw(draw)
        return canvas

if __name__ == "__main__":
    # Example usage
    d = "M 0 4 A 4 4 0 0 1 4 0 H 12 c 2 0 3 1 4 2 l 4 4 c 1 1 2 2 4 2 h 12 c 2 0 3 -1 4 -2 l 4 -4 c 1 -1 2 -2 4 -2 L 319 0 a 4 4 0 0 1 4 4 L 323 52 a 4 4 0 0 1 -4 4 L 64 56 c -2 0 -3 1 -4 2 l -4 4 c -1 1 -2 2 -4 2 h -12 c -2 0 -3 -1 -4 -2 l -4 -4 c -1 -1 -2 -2 -4 -2 L 20 56 a 4 4 0 0 0 -4 4 L 16 164 a 4 4 0 0 0 4 4 L 28 168 c 2 0 3 1 4 2 l 4 4 c 1 1 2 2 4 2 h 12 c 2 0 3 -1 4 -2 l 4 -4 c 1 -1 2 -2 4 -2 L 319 168 a 4 4 0 0 1 4 4 L 323 196 a 4 4 0 0 1 -4 4 L 48 200 c -2 0 -3 1 -4 2 l -4 4 c -1 1 -2 2 -4 2 h -12 c -2 0 -3 -1 -4 -2 l -4 -4 c -1 -1 -2 -2 -4 -2 L 4 200 a 4 4 0 0 1 -4 -4 Z"
    d= "m 0,0 c 25,-22 71,-22 96,0 H 139.15625 a 4,4 0 0,1 4,4 v 40  a 4,4 0 0,1 -4,4 H 48\
        c -2,0 -3,1 -4,2 l -4,4 c -1,1 -2,2 -4,2 h -12 c -2,0 -3,-1 -4,\
            -2 l -4,-4 c -1,-1 -2,-2 -4,-2 H 4 a 4,4 0 0,1 -4,-4 z"
    d = "m 0 17 c 25 -22 71 -22 96 0 h 142 a 4 4 0 0 1 4 4 v 2 a 4 4 0 0 1 -4 4 H 64 c -2 0 -3 1 -4 2 l -4 4 c -1 1 -2 2 -4 2 h -12 c -2 0 -3 -1 -4 -2 l -4 -4 c -1 -1 -2 -2 -4 -2 H 20 a 4 4 0 0 0 -4 4 v 4 a 4 4 0 0 0 4 4 h 8 c 2 0 3 1 4 2 l 4 4 c 1 1 2 2 4 2 h 12 c 2 0 3 -1 4 -2 l 4 -4 c 1 -1 2 -2 4 -2 h 137 a 4 4 0 0 1 4 4 v 0 a 4 4 0 0 1 -4 4 H 64 c -2 0 -3 1 -4 2 l -4 4 c -1 1 -2 2 -4 2 h -12 c -2 0 -3 -1 -4 -2 l -4 -4 c -1 -1 -2 -2 -4 -2 H 20 a 4 4 0 0 0 -4 4 v 7 a 4 4 0 0 0 4 4 h 8 c 2 0 3 1 4 2 l 4 4 c 1 1 2 2 4 2 h 12 c 2 0 3 -1 4 -2 l 4 -4 c 1 -1 2 -2 4 -2 h 84 a 4 4 0 0 1 4 4 v 0 a 4 4 0 0 1 -4 4 H 48 c -2 0 -3 1 -4 2 l -4 4 c -1 1 -2 2 -4 2 h -12 c -2 0 -3 -1 -4 -2 l -4 -4 c -1 -1 -2 -2 -4 -2 H 4 a 4 4 0 0 1 -4 -4 z"
    svg = SVG()
    svg.add_widget(PathSVG(
        d,
        border_color= "#cf8b17",
        fill_color="#ffab19",  # Semi-transparent red
        viewbox=ViewBox(1, 0, 3, 3),
        stroke_width=2,
        curve_resolution=20
        )
    )
    svg.add_widget(TextSVG(
        text="repeat until",
        font_path="assets/fonts/HelveticaNeueMedium.otf",  # Adjust the path to your font file
        position=(10, 21),
        font_size=20,
        font_color=(0, 0, 0),  # Black text
    ))

    print([(round(x, 3), round(y, 3)) for x, y in svg.widgets[0].subpaths[0]])
    img = svg.draw(background_color=(255, 255, 255, 0))  # Transparent background
    img.show()