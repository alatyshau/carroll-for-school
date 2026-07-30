#!/usr/bin/env python3
"""The title of a diagram: what the diagram holds, written out.

Every diagram in the folder is `![](media/02-004.svg "BIL c6=1 c8=0")` — the
title carries the whole content of the picture, and the picture is drawn from
it.  So the model of the book lives in the folder's own markdown, in plain
sight, and the SVG beside it is a derivative, like the PDF.

    kind      which Diagram, and which part of it (see carroll_svg.KINDS)
    cN        compartment N holds a counter: '1' red, '0' grey
    eNM       a counter astride the line dividing compartments N and M
    labels    the Diagram is lettered x / y / m
    numbers   the compartments are numbered, as on the frontispiece

The compartment numbers are Carroll's own and are printed in his book: 5-8 on
the smaller diagram, 9-16 on the larger.  So are the digits — chapter I sets
out that '1' stands where the reader is to put a red counter and '0' where a
grey one.  Nothing in this notation is an invention of this edition; it only
writes down what the page shows.

The name of a compartment does not depend on the part of the Diagram being
drawn: in BIL_R the compartments are still c6 and c8, though they are drawn
where 5 and 7 would sit on the whole diagram.  That is what lets one line be
read the same way everywhere.
"""
import re
import carroll_svg

FLAGS = ('labels', 'numbers')
_SLOT = re.compile(r'^(c|e)(\d+)$')


def _slot_order(slot):
    """Compartments before division-lines, each in Carroll's numbering."""
    m = _SLOT.match(slot)
    return (0 if m.group(1) == 'c' else 1, int(m.group(2)))


def encode(kind, counters, labels=False, numbers=False):
    parts = [kind]
    parts += [f for f, on in zip(FLAGS, (labels, numbers)) if on]
    parts += ['%s=%s' % (s, counters[s]) for s in sorted(counters, key=_slot_order)]
    return ' '.join(parts)


def decode(alt):
    """-> (kind, counters, labels, numbers).  Raises on anything unexpected.

    Everything is checked here, and the message names the line it choked on:
    this is read from markdown a person edits by hand, and a mistyped kind or
    a stray word must come back as a sentence, not as a KeyError somewhere
    inside the drawing code.
    """
    parts = alt.split()
    if not parts:
        raise ValueError('empty diagram title')
    kind, counters, flags = parts[0], {}, set()
    if kind not in carroll_svg.KINDS:
        raise ValueError('unknown diagram %r in %r — known are %s'
                         % (kind, alt, ', '.join(sorted(carroll_svg.KINDS))))
    for p in parts[1:]:
        if p in FLAGS:
            flags.add(p)
        elif '=' in p:
            slot, val = p.split('=', 1)
            if not _SLOT.match(slot) or val not in ('0', '1'):
                raise ValueError('bad counter %r in %r' % (p, alt))
            counters[slot] = val
        else:
            raise ValueError('bad word %r in %r' % (p, alt))
    return kind, counters, 'labels' in flags, 'numbers' in flags


# The line goes in the image's title, not its alt text.  Pandoc turns a
# paragraph holding one image with alt text into a figure and prints the alt
# underneath as a caption — the notation would appear on the page, under every
# diagram in the book.  A title raises no figure in pandoc or in CommonMark, so
# the folder renders the same anywhere, with no flag to remember and no rule in
# the stylesheet to suppress anything.
IMG = re.compile(r'!\[\]\(media/([^)"\s]+\.svg)\s+"([^"]*)"\)')


def images(md):
    """Every diagram of a markdown file, in the order it is printed."""
    return [(m.group(1), m.group(2)) for m in IMG.finditer(md)]
