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

"""
sb3-motion { fill: #4c97ff; stroke: #3373cc; }
.sb3-motion-alt { fill: #4280d7; }    .sb3-motion-dark { fill: #4c97ff; }    
.sb3-looks { fill: #9966ff; stroke: #774dcb; }    .sb3-looks-alt { fill: #855cd6; }    
.sb3-looks-dark { fill: #bd42bd; }    .sb3-sound { fill: #cf63cf; stroke: #bd42bd; }    
.sb3-sound-alt { fill: #c94fc9; }    .sb3-sound-dark { fill: #bd42bd; }    
.sb3-control { fill: #ffab19; stroke: #cf8b17; }    .sb3-control-alt { fill: #ec9c13; }    
.sb3-control-dark { fill: #cf8b17; }    .sb3-events { fill: #ffbf00; stroke: #cc9900; }    
.sb3-events-alt { fill: #e6ac00; }    .sb3-events-dark { fill: #cc9900; }    
.sb3-sensing { fill: #5cb1d6; stroke: #2e8eb8; }    .sb3-sensing-alt { fill: #47a8d1; }    
.sb3-sensing-dark { fill: #2e8eb8; }    .sb3-operators { fill: #59c059; stroke: #389438; }    
.sb3-operators-alt { fill: #46b946; }    .sb3-operators-dark { fill: #389438; }    
.sb3-variables { fill: #ff8c1a; stroke: #db6e00; }    .sb3-variables-alt { fill: #ff8000; }    
.sb3-variables-dark { fill: #db6e00; }    .sb3-list { fill: #ff661a; stroke: #e64d00; }    
.sb3-list-alt { fill: #ff5500; }    .sb3-list-dark { fill: #e64d00; }    
.sb3-custom { fill: #ff6680; stroke: #ff3355; }    .sb3-custom-alt { fill: #ff4d6a; }    
.sb3-custom-dark { fill: #ff3355; }    .sb3-custom-arg { fill: #ff6680; stroke: #ff3355; }    
/* extension blocks, e.g. pen */    .sb3-extension { fill: #0fbd8c; stroke: #0b8e69; }    
.sb3-extension-alt { fill: #0da57a; }    .sb3-extension-line { stroke: #0da57a; }    
.sb3-extension-dark { fill: #0b8e69; }    /* obsolete colors: chosen by hand, indicates invalid blocks */     
.sb3-obsolete { fill: #ed4242; stroke: #ca2b2b; }    .sb3-obsolete-alt { fill: #db3333; }   
 .sb3-obsolete-dark { fill: #ca2b2b; }    /* grey: special color from the Scratch 3.0 design mockups */    
 .sb3-grey { fill: #bfbfbf; stroke: #909090; }    .sb3-grey-alt { fill: #b2b2b2; }    
 .sb3-grey-dark { fill: #909090; }    .sb3-input-color {      stroke: #fff;    }    
 .sb3-input-number,    .sb3-input-string {      fill: #fff;    }    .sb3-literal-number,    
 .sb3-literal-string,    .sb3-literal-number-dropdown,    
 .sb3-literal-dropdown {      word-spacing: 0;    }    .sb3-literal-number,   
   .sb3-literal-string {      fill: #575e75;    }    
   .sb3-comment {      fill: #ffffa5;      stroke: #d0d1d2;      stroke-width: 1;    }    
   .sb3-comment-line {      fill: #ffff80;    }
"""

colors = {
    "Events": ("#ffbf00", "#cc9900"),
    "Control": ("#ffab19", "#cf8b17"),
    "Motion": ("#4c97ff", "#3373cc"),
    "Looks": ("#9966ff", "#774dcb"),
    "Sound": ("#cf63cf", "#bd42bd"),
    "Sensing": ("#5cb1d6", "#2e8eb8"),
    "Operators": ("#59c059", "#389438"),
    "Variables": ("#ff8c1a", "#db6e00"),
    "My Blocks": ("#ff8c1a", "#db6e00"),
}

#Events
when_flag_clicked = Block("when_flag_clicked", None, *colors["Events"])
when_flag_clicked.add_shape(BlockShape.Hat)
when_flag_clicked.add_shape(BlockShape.StackBottom)
when_flag_clicked.add_branch(Branch("main", [(BlockPartType.LABEL, "when green flag clicked")]))
blocks_available["Events"].append(when_flag_clicked)

when_key_pressed = Block("when_key_pressed", None, *colors["Events"])
when_key_pressed.add_shape(BlockShape.Hat)
when_key_pressed.add_shape(BlockShape.StackBottom)
blocks_available["Events"].append(when_key_pressed)

when_broadcast_received = Block("when_broadcast_received", None, *colors["Events"])
when_broadcast_received.add_shape(BlockShape.Hat)
when_broadcast_received.add_shape(BlockShape.StackBottom)
blocks_available["Events"].append(when_broadcast_received)

when_backdrop_switches = Block("when_backdrop_switches", None, *colors["Events"])
when_backdrop_switches.add_shape(BlockShape.Hat)
when_backdrop_switches.add_shape(BlockShape.StackBottom)
blocks_available["Events"].append(when_backdrop_switches)

when_object_clicked = Block("when_object_clicked", None, *colors["Events"])
when_object_clicked.add_shape(BlockShape.Hat)
when_object_clicked.add_shape(BlockShape.StackBottom)
blocks_available["Events"].append(when_object_clicked)

sending_broadcast = Block("sending_broadcast", None, *colors["Events"])
sending_broadcast.add_shape(BlockShape.StackTop)
sending_broadcast.add_shape(BlockShape.StackBottom)
blocks_available["Events"].append(sending_broadcast)

#Control
wait_seconds = Block("wait_seconds", None, *colors["Control"])
wait_seconds.add_shape(BlockShape.StackTop)
wait_seconds.add_shape(BlockShape.StackBottom)
blocks_available["Control"].append(wait_seconds)

wait_until = Block("wait_until", None, *colors["Control"])
wait_until.add_shape(BlockShape.StackTop)
wait_until.add_shape(BlockShape.StackBottom)
blocks_available["Control"].append(wait_until)

repeat_until = Block("repeat_until", None, *colors["Control"])
repeat_until.add_shape(BlockShape.StackTop)
repeat_until.add_shape(BlockShape.CBlock)
repeat_until.add_shape(BlockShape.StackBottom)
blocks_available["Control"].append(repeat_until)