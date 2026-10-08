# ---
# name: Rares QWERTY
# icon: keyboard
# summary: QWERTY with emoji left and period right of the space bar
# version: 1.1
# author: Rares
# ---

# Same pattern as Clink's official Colemak-DH plugin: layouts() returns layouts
# whose left=[...] / right=[...] keys sit beside the space bar (up to three per
# side). Actions: insert, spacer, shift, delete, space, return, numbers, emoji,
# globe, tab, left, right, undo, redo, dismiss. Picking one in
# Layout > Arrangement installs it as an ordinary custom layout, so it stays
# (and stays editable) even if this plugin is removed.
#
# Two variants, because Clink doesn't document whether placing your own return
# replaces the stock one:
#   Rares QWERTY           emoji | space | .          (stock return untouched)
#   Rares QWERTY Compact   emoji | space | . | return (narrow, SwiftKey-like)
# If Compact shows two return keys, use the plain one and shrink return in the
# Layout editor instead.

ROWS = [list("qwertyuiop"), list("asdfghjkl"), list("zxcvbnm")]

def layouts(state):
    return [
        layout("rares-qwerty", "Rares QWERTY", icon="keyboard",
               rows=ROWS,
               left=[layout_key("😊", action="emoji", width=1.0)],
               right=[layout_key(".", width=1.0)]),
        layout("rares-qwerty-compact", "Rares QWERTY Compact", icon="keyboard",
               rows=ROWS,
               left=[layout_key("😊", action="emoji", width=1.0)],
               right=[layout_key(".", width=1.0),
                      layout_key("⏎", action="return", width=1.5)]),
    ]
