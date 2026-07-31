#!/usr/bin/env python3
"""The book checks itself: Chapter III is the answer key to Chapter II.

    python3 lib/logic_diagrams/selfcheck.py [edition]

For every problem one side is a diagram, the other a sentence in words.  The
sentence is translated into counters by Carroll's rules and compared with the
diagram.  A mismatch means the problem contradicts the book's own answer —
which is exactly how the Ch. II §3 No. 16 defect was found.

Coverage: sections 2-5, the smaller Diagram and its halves.  Sections 6-7
(the larger, three-letter Diagram) are covered by selfcheck_tri.py -- there a
sentence does not translate into counters without working out the order in
which the premises are laid down.

Anything that fails to parse is printed with a '?' and does not count: a
silently skipped problem would look like a checked one.

**Exactly one mismatch is expected** -- Ch. II §5 No. 3: an error of the 1887
edition itself, left as printed, with an editor's note added to the text (see
the edition's README).  Any other mismatch is a regression.
"""
import argparse, re, sys
import compare_diagrams, notation

SECTIONS = ['2', '3', '4', '5']

# compartment from a pair of attributes
CELL = {('x', 'y'): 'c5', ('x', "y'"): 'c6', ("x'", 'y'): 'c7', ("x'", "y'"): 'c8'}
# the line bisecting one "half" of the diagram: "some A exist"
LINE = {'x': 'e56', "x'": 'e78', 'y': 'e57', "y'": 'e68'}


def other(a):
    return a[0] if a.endswith("'") else a + "'"


def cell(a, b):
    """The compartment where two attributes intersect, given in either order."""
    if a[0] == 'y':
        a, b = b, a
    return CELL.get((a, b))


# --------------------------------------------------------------- text parsing
ATTR = r"(?:\$(x'?|y'?)\$|not-\$(x|y)\$|\$(x|y)\$'|(x'?|y'?))"


def attrs(s):
    """All attributes of the sentence in order: $x$, $y'$, not-$y$ -> x, y', y'."""
    out = []
    for m in re.finditer(r"\$([xy]'?)\$|not-\$([xy])\$", s):
        if m.group(1):
            out.append(m.group(1))
        else:
            out.append(other(m.group(2)))
    return out


def parse(sentence):
    """Sentence -> set of counters, or None if the form is not recognized."""
    s = sentence
    s = re.sub(r'\bi\.e\..*$', '', s)          # plain-English restatement -- not needed
    s = re.sub(r',?\s*\bor,?\s.*$', '', s, flags=re.I)   # equivalent rephrasing
    s = s.strip().rstrip('.').strip()
    if not s:
        return None
    a = attrs(s)
    marks = {}

    def some(p, q):
        c = cell(p, q)
        if c is None:
            return False
        marks[c] = '1'
        return True

    def none(p, q):
        c = cell(p, q)
        if c is None:
            return False
        marks[c] = '0'
        return True

    # "Some A are B, and some A exist" -- the second half adds no counter.
    # Carroll works this case out himself (Ch. III §2 No. 7): to put a red
    # counter on the division-line "would only tell us 'ONE OF THE
    # compartments is occupied', which we know already".  A counter on the
    # line here would be redundant.
    if re.match(r'^Some .*? are .*?, and some .*? exist$', s) and len(a) == 3:
        return marks if a[2] in LINE and some(a[0], a[1]) else None

    # "Some A are B, and some are C" / "... and some C are D"
    m = re.match(r'^Some .*? are .*?, and some (?:\S+ )?are .*$', s)
    if m and len(a) >= 3:
        ok = some(a[0], a[1])
        ok &= some(a[0], a[-1]) if len(a) == 3 else some(a[2], a[3])
        return marks if ok else None

    # "No A exist, and no B exist"
    if re.match(r'^No .*? exist, and no .*? exist$', s) and len(a) == 2:
        for p in a:
            if p not in LINE:
                return None
            for q in ('y', "y'") if p[0] == 'x' else ('x', "x'"):
                if not none(p, q):
                    return None
        return marks

    # "No A are B, and none are C"
    if re.match(r'^No .*? are .*?, and none are .*$', s) and len(a) == 3:
        return marks if none(a[0], a[1]) and none(a[0], a[2]) else None

    # "All A are B, and all C are D"
    if re.match(r'^All .*? are .*?, and all .*? are .*$', s) and len(a) == 4:
        ok = some(a[0], a[1]) and none(a[0], other(a[1]))
        ok = ok and some(a[2], a[3]) and none(a[2], other(a[3]))
        return marks if ok else None

    # "Some A are B, and no C are D"
    m = re.match(r'^Some .*? are .*?, and no .*? are .*$', s)
    if m and len(a) == 4:
        return marks if some(a[0], a[1]) and none(a[2], a[3]) else None

    # single-proposition forms
    if re.match(r'^Some .*? exist$', s) and len(a) == 1:
        if a[0] not in LINE:
            return None
        marks[LINE[a[0]]] = '1'
        return marks
    if re.match(r'^No .*? exist$', s) and len(a) == 1:
        p = a[0]
        for q in ('y', "y'") if p[0] == 'x' else ('x', "x'"):
            if not none(p, q):
                return None
        return marks
    if re.match(r'^Some .*? are .*$', s) and len(a) == 2:
        return marks if some(a[0], a[1]) else None
    if re.match(r'^No .*? are .*$', s) and len(a) == 2:
        return marks if none(a[0], a[1]) else None
    if re.match(r'^All .*? are .*$', s) and len(a) == 2:
        ok = some(a[0], a[1]) and none(a[0], other(a[1]))
        return marks if ok else None
    return None


# ------------------------------------------------------------------ material
def sections_of(book, chapter):
    """{section number: section text} of a chapter, from its section files."""
    txt = compare_diagrams.chapter_markdown(chapter, book)
    parts = re.split(r'^### (\d+)\.\s*', txt, flags=re.M)
    return {parts[i]: parts[i + 1] for i in range(1, len(parts), 2)}


def numbered_text(block):
    """The section's numbered items that are sentences."""
    out = {}
    for m in re.finditer(r'^(\d+)\.\s+(.*?)$', block, flags=re.M):
        body = m.group(2).strip()
        if re.search(r'!\[\]\(media/', body):
            continue
        # the editor's note is not part of Carroll's answer; left in place it
        # would hide the very contradiction it was written about, and the
        # problem would silently count as unparsed
        body = re.sub(r'\*\[A note from the editor.*?\]\*', '', body).strip()
        out[int(m.group(1))] = body
    return out


def numbered_figs(block, models=None):
    """The section's numbered items that are diagrams -> (kind, counters).

    The diagram is read straight from the image title (`notation.py`), not
    by file number: a problem's number and its diagram sit next to each other
    in the markdown, and the link between them rests on nothing else.
    """
    out = {}
    for m in re.finditer(r'\*\*(\d+)\.\*\*\s+!\[\]\(media/[^)"]+"([^"]*)"\)', block):
        kind, counters, _labels, _numbers = notation.decode(m.group(2))
        out[int(m.group(1))] = (kind, counters)
    return out


def main(book):
    ch2 = sections_of(book, 2)
    ch3 = sections_of(book, 3)
    m2 = compare_diagrams.english_models(2, book)
    m3 = compare_diagrams.english_models(3, book)

    total = ok = bad = unparsed = 0
    for sec in SECTIONS:
        q_fig = numbered_figs(ch2[sec], m2)
        a_fig = numbered_figs(ch3[sec], m3)
        q_txt = numbered_text(ch2[sec])
        a_txt = numbered_text(ch3[sec])
        # one side holds the diagrams, the other the words
        figs, texts = (q_fig, a_txt) if q_fig else (a_fig, q_txt)
        kindname = 'diagrams in problems' if q_fig else 'diagrams in answers'
        print('--- section %s (%s), %d problems' % (sec, kindname, len(figs)))
        for n in sorted(figs):
            total += 1
            kind, counters = figs[n]
            sentence = texts.get(n)
            want = parse(sentence) if sentence else None
            if want is None:
                unparsed += 1
                print('   ?%-3d  unparsed: %s' % (n, sentence))
                continue
            if want != counters:
                bad += 1
                print('   !%-3d  diagram %-6s %-34s text %-34s  << %s'
                      % (n, kind, dict(sorted(counters.items())),
                         dict(sorted(want.items())), sentence))
            else:
                ok += 1
    print('\ntotal %d: matched %d, mismatched %d, unparsed %d'
          % (total, ok, bad, unparsed))
    return 1 if bad else 0


if __name__ == '__main__':
    p = argparse.ArgumentParser(
        description='The book against its own answer key, on the smaller Diagram.')
    p.add_argument('edition', nargs='?', default=compare_diagrams.DEFAULT_EDITION,
                   help='edition folder (default: corpus/en-CA/1887_The_Game_of_Logic)')
    sys.exit(main(p.parse_args().edition))
