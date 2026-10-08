# ---
# name: Rares QWERTY
# icon: keyboard
# summary: QWERTY with a period key right of the space bar
# version: 1.0
# author: Rares
# ---

# Same pattern as Clink's official Colemak-DH plugin: layouts() returns a
# layout whose right=[...] keys sit beside the space bar. Picking it in
# Layout > Arrangement installs it as an ordinary custom layout, so it stays
# (and stays editable) even if this plugin is removed. Shift, delete and the
# 123 / #+= pages come from Clink's stock ones.
def layouts(state):
    return [
        layout("rares-qwerty", "Rares QWERTY", icon="keyboard",
               rows=[list("qwertyuiop"), list("asdfghjkl"), list("zxcvbnm")],
               right=[layout_key(".")]),
    ]
