#!/usr/bin/env python3
"""Render Carroll's Game-of-Logic diagrams as standalone SVG.

Model: (kind, counters) where counters maps a slot name to '1' (red) or '0' (grey).
Slot names: 'c5'..'c16' for compartments, 'eAB' for a counter lying on the division
line between compartments A and B.

Counters are drawn as the digits the 1887 book prints in place of them: "I shall
put '1' (meaning 'one or more') where you are to put a RED counter, and '0'
(meaning 'none') where you are to put a GREY one."
"""

INK = '#000000'
LW = 2.0          # structural line width
DIGIT = 24.0      # counter glyph size; the 1887 book prints '1' and '0', not counters
MASK = 13.5       # white disc under a digit, so a division-line does not cross it
RING = 0.4        # hairline round the disc: without it a '1' lying on a vertical
                  # division-line merges into the line and disappears.  Carroll met
                  # the same problem and solved it by printing a horizontal bar
                  # instead of the digit; the ring keeps the digit and separates it.
SCALE = 0.72      # printed size against the drawing units.  The 1887 book sets a
                  # diagram about a third of the text measure; at 1.0 ours came out
                  # nearly twice that, eleven lines of type tall against the book's
                  # six or seven.  The viewBox is untouched, so only the size on the
                  # page changes — in VS Code's preview as well as in the PDF.
FONT = "Georgia, 'Times New Roman', 'Nimbus Roman', serif"
# Georgia's figures are old-style: its '0' sits at x-height and reads as the letter
# 'o'.  The digits here are the content of the diagram, so they are set in a face
# with lining figures.
FIGFONT = "'Times New Roman', 'Nimbus Roman', Times, serif"

# ---------------------------------------------------------------- geometry
# Biliteral (smaller) square: 200x200, origin (0,0).
# Triliteral (larger) square: 240x240, inner square (60,60)-(180,180).

def _bil():
    return dict(
        lines=[(0, 0, 200, 0), (200, 0, 200, 200), (200, 200, 0, 200), (0, 200, 0, 0),
               (0, 100, 200, 100), (100, 0, 100, 200)],
        cells={'c5': (50, 50), 'c6': (150, 50), 'c7': (50, 150), 'c8': (150, 150)},
        edges={'e56': (100, 50), 'e78': (100, 150), 'e57': (50, 100), 'e68': (150, 100)},
        labels={'x': (100, 50), "x'": (100, 150), 'y': (50, 100), "y'": (150, 100)},
        numbers={'5': (6, 6, 'start', 'hanging'), '6': (194, 6, 'end', 'hanging'),
                 '7': (6, 194, 'start', 'auto'), '8': (194, 194, 'end', 'auto')},
        box=(0, 0, 200, 200))

def _bil_top():
    return dict(
        lines=[(0, 0, 200, 0), (200, 0, 200, 100), (200, 100, 0, 100), (0, 100, 0, 0),
               (100, 0, 100, 100)],
        cells={'c5': (50, 50), 'c6': (150, 50)},
        edges={'e56': (100, 50)},
        labels={'x': (100, 50), 'y': (50, 100), "y'": (150, 100)},
        numbers={}, box=(0, 0, 200, 100))

def _bil_left():
    return dict(
        lines=[(0, 0, 100, 0), (100, 0, 100, 200), (100, 200, 0, 200), (0, 200, 0, 0),
               (0, 100, 100, 100)],
        cells={'c5': (50, 50), 'c7': (50, 150)},
        edges={'e57': (50, 100)},
        labels={'x': (100, 50), "x'": (100, 150), 'y': (50, 100)},
        numbers={}, box=(0, 0, 100, 200))

def _bil_right():
    return dict(
        lines=[(0, 0, 100, 0), (100, 0, 100, 200), (100, 200, 0, 200), (0, 200, 0, 0),
               (0, 100, 100, 100)],
        cells={'c6': (50, 50), 'c8': (50, 150)},
        edges={'e68': (50, 100)},
        labels={'x': (0, 50), "x'": (0, 150), "y'": (50, 100)},
        numbers={}, box=(0, 0, 100, 200))

def _tri():
    return dict(
        lines=[(0, 0, 240, 0), (240, 0, 240, 240), (240, 240, 0, 240), (0, 240, 0, 0),
               (0, 120, 240, 120), (120, 0, 120, 240),
               (60, 60, 180, 60), (180, 60, 180, 180), (180, 180, 60, 180), (60, 180, 60, 60)],
        cells={'c9': (30, 30), 'c10': (210, 30), 'c15': (30, 210), 'c16': (210, 210),
               'c11': (90, 90), 'c12': (150, 90), 'c13': (90, 150), 'c14': (150, 150)},
        edges={'e1112': (120, 90), 'e1314': (120, 150), 'e1113': (90, 120), 'e1214': (150, 120),
               'e915': (30, 120), 'e1016': (210, 120), 'e910': (120, 30), 'e1516': (120, 210)},
        labels={'x': (120, 60), "x'": (120, 180), 'y': (60, 120), "y'": (180, 120),
                'm': (120, 120)},
        numbers={'9': (6, 6, 'start', 'hanging'), '10': (234, 6, 'end', 'hanging'),
                 '15': (6, 234, 'start', 'auto'), '16': (234, 234, 'end', 'auto'),
                 '11': (66, 66, 'start', 'hanging'), '12': (174, 66, 'end', 'hanging'),
                 '13': (66, 174, 'start', 'auto'), '14': (174, 174, 'end', 'auto')},
        box=(0, 0, 240, 240))

def _tri_top():
    return dict(
        lines=[(0, 0, 240, 0), (240, 0, 240, 120), (240, 120, 0, 120), (0, 120, 0, 0),
               (120, 0, 120, 120),
               (60, 60, 180, 60), (60, 60, 60, 120), (180, 60, 180, 120)],
        cells={'c9': (30, 30), 'c10': (210, 30), 'c11': (90, 90), 'c12': (150, 90)},
        edges={'e1112': (120, 90), 'e910': (120, 30)},
        labels={'x': (120, 60), 'y': (60, 120), "y'": (180, 120)},
        numbers={}, box=(0, 0, 240, 120))

def _tri_bottom():
    return dict(
        lines=[(0, 0, 240, 0), (240, 0, 240, 120), (240, 120, 0, 120), (0, 120, 0, 0),
               (120, 0, 120, 120),
               (60, 60, 180, 60), (60, 0, 60, 60), (180, 0, 180, 60)],
        cells={'c13': (90, 30), 'c14': (150, 30), 'c15': (30, 90), 'c16': (210, 90)},
        edges={'e1314': (120, 30), 'e1516': (120, 90)},
        labels={"x'": (120, 60), 'y': (60, 0), "y'": (180, 0)},
        numbers={}, box=(0, 0, 240, 120))

def _tri_right_oblong():
    # right-hand upright oblong of the larger diagram: compartments 10, 12, 14, 16
    return dict(
        lines=[(0, 0, 120, 0), (120, 0, 120, 240), (120, 240, 0, 240), (0, 240, 0, 0),
               (0, 120, 120, 120),
               (0, 60, 60, 60), (60, 60, 60, 180), (0, 180, 60, 180)],
        cells={'c10': (30, 30), 'c12': (30, 90), 'c14': (30, 150), 'c16': (30, 210)},
        edges={'e1016': (90, 120), 'e1214': (30, 120)},
        labels={}, numbers={}, box=(0, 0, 120, 240))

KINDS = {'BIL': _bil, 'BIL_T': _bil_top, 'BIL_L': _bil_left, 'BIL_R': _bil_right,
         'TRI': _tri, 'TRI_T': _tri_top, 'TRI_B': _tri_bottom, 'TRI_ROB': _tri_right_oblong}


def render(kind, counters, labels=False, numbers=False, pad=14):
    """counters: dict slot -> '0' | '1'.  Returns SVG source."""
    g = KINDS[kind]()
    x0, y0, x1, y1 = g['box']
    W, H = x1 - x0 + 2 * pad, y1 - y0 + 2 * pad
    out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="%g %g %g %g" width="%g" height="%g" '
           'role="img">' % (x0 - pad, y0 - pad, W, H, W * SCALE, H * SCALE)]
    out.append('<g fill="none" stroke="%s" stroke-width="%g" stroke-linecap="square">' % (INK, LW))
    for a, b, c, d in g['lines']:
        out.append('<line x1="%g" y1="%g" x2="%g" y2="%g"/>' % (a, b, c, d))
    out.append('</g>')

    if labels and g['labels']:
        out.append('<g font-family="%s" font-style="italic" font-size="21" fill="%s" '
                   'text-anchor="middle" dominant-baseline="central">' % (FONT, INK))
        for t, (lx, ly) in g['labels'].items():
            out.append('<circle cx="%g" cy="%g" r="12" fill="#ffffff" stroke="none"/>' % (lx, ly))
            out.append('<text x="%g" y="%g">%s</text>' % (lx, ly, t.replace("'", '&#8242;')))
        out.append('</g>')

    if numbers and g['numbers']:
        out.append('<g font-family="%s" font-size="15" fill="%s">' % (FIGFONT, INK))
        for t, (nx, ny, anchor, base) in g['numbers'].items():
            out.append('<text x="%g" y="%g" text-anchor="%s" dominant-baseline="%s">%s</text>'
                       % (nx, ny, anchor, base, t))
        out.append('</g>')

    if counters:
        out.append('<g font-family="%s" font-size="%g" fill="%s" text-anchor="middle" '
                   'dominant-baseline="central">' % (FIGFONT, DIGIT, INK))
        # Compartments first, then division-lines, each in Carroll's numbering —
        # the same order the title string is written in.  Counters never overlap,
        # so the order does not change the picture; fixing it makes the file
        # itself canonical, and a redraw from the title string comes out byte
        # for byte the same as the file beside it.
        for slot in sorted(counters, key=lambda s: (s[0], int(s[1:]))):
            val = counters[slot]
            pos = g['cells'].get(slot) or g['edges'].get(slot)
            if pos is None:
                raise KeyError('slot %r not defined for kind %s' % (slot, kind))
            cx, cy = pos
            out.append('<circle cx="%g" cy="%g" r="%g" fill="#ffffff" stroke="%s" '
                       'stroke-width="%g"/>' % (cx, cy, MASK, INK, RING))
            out.append('<text x="%g" y="%g">%s</text>' % (cx, cy, val))
        out.append('</g>')
    out.append('</svg>')
    return '\n'.join(out) + '\n'
