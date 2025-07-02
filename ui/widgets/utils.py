def tk_color_to_hex(widget, color_name):
    """Prend un nom couleur (ex: 'gray86') et renvoie '#rrggbb'"""
    r, g, b = widget.winfo_rgb(color_name)
    # r,g,b sont sur 16 bits (0-65535) → convertir en 8 bits (0-255)
    r = r // 256
    g = g // 256
    b = b // 256
    return f'#{r:02x}{g:02x}{b:02x}'

def hex_to_rgb(hex_color):
    """Convertit une couleur hexadécimale en tuple RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb_color):
    """Convertit un tuple RGB en couleur hexadécimale"""
    return '#{:02x}{:02x}{:02x}'.format(*rgb_color)