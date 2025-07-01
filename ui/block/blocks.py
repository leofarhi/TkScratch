from ui.block.block import *

blocks_available = {
    "Events": [],
    "Control": [],
    "Motion": [],
    "Looks": [],
    "Sound": [],
    "Sensing": [],
    "Operators": [],
    "Variables": [],
    "My Blocks": [],
}

#Events
when_flag_clicked = Block("when_flag_clicked", None)
when_flag_clicked.add_shape(BlockShape.Hat)
when_flag_clicked.add_shape(BlockShape.StackTop)
blocks_available["Events"].append(when_flag_clicked)