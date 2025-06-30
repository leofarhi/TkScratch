from enum import Enum

class BlockShape(Enum):
    STACK = "stack"        # Rectangle à bords plats/ondulés (action)
    HAT = "hat"            # Forme chapeau (début script)
    C_BLOCK = "c-block"    # Conteneur (boucle, if…)
    REPORTER = "reporter"  # Arrondi (renvoie une valeur)
    BOOLEAN = "boolean"    # Hexagonal (condition)
    CAP = "cap"            # Fin de script (stop all)

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
        self.shape = [BlockShape.STACK]
        self.color = "#4C97FF"
        self.branches = [
            Branch(
                "if",
                top=[
                    (BlockPartType.LABEL, "if"),
                    (BlockPartType.BOOLEAN, None),
                    (BlockPartType.LABEL, "then")
                ],
                next_block=None
            ),
            Branch(
                "else",
                top=[
                    (BlockPartType.LABEL, "else")
                ],
                next_block=None
            ),
        ]
        self.next_block = None
