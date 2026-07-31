#!/usr/bin/env python3
"""The book checks itself on the larger, three-letter Diagram: Ch. II §§6-7
against Ch. III §§6-7.

    python3 lib/logic_diagrams/selfcheck_tri.py [edition]

Companion to selfcheck.py (which covers §§2-5, the smaller diagram).  Here:

* §6: sentences with $m$ are translated into counters of the larger Diagram
  by Carroll's rules (Ch. I: negative parts of the premises first, then
  affirmative; "All A are B" = "Some A are B" + "No A are B'"; a red counter
  goes into a compartment when the other compartment is already grey,
  otherwise onto the division line) and compared with the answers' diagrams.
* §7: premises -> larger Diagram -> transfer onto the smaller one (Ch. I: a
  compartment of the smaller Diagram is red if at least one of its
  m/m'-halves is red; grey if both are; if only one half is grey and the
  other is unknown, nothing is known about the compartment; an unresolved
  red on a line does not transfer) -> compared with the answer's smaller
  diagram and with the stated conclusion.

Anything that fails to parse is printed with a '?' and does not count: a
silently skipped problem would look like a checked one.
"""
import argparse, re, sys
import compare_diagrams, selfcheck

# ------------------------------------------------------------------- model
# larger-Diagram compartment -> attribute triple (x-half, y-half, m-status)
ATTRS = {
    'c9':  ('x',  'y',  "m'"), 'c10': ('x',  "y'", "m'"),
    'c11': ('x',  'y',  'm'),  'c12': ('x',  "y'", 'm'),
    'c13': ("x'", 'y',  'm'),  'c14': ("x'", "y'", 'm'),
    'c15': ("x'", 'y',  "m'"), 'c16': ("x'", "y'", "m'"),
}
# larger-Diagram compartment -> smaller-Diagram compartment
SMALL_OF = {'c9': 'c5', 'c11': 'c5', 'c10': 'c6', 'c12': 'c6',
            'c13': 'c7', 'c15': 'c7', 'c14': 'c8', 'c16': 'c8'}
SMALL_LINE = {frozenset(p): s for p, s in [
    (('c5', 'c6'), 'e56'), (('c7', 'c8'), 'e78'),
    (('c5', 'c7'), 'e57'), (('c6', 'c8'), 'e68')]}


def cells_with(attrs):
    """Compartments that carry all the listed attributes (1-3 of them)."""
    return [c for c, a in ATTRS.items() if set(attrs) <= set(a)]


def line_slot(c1, c2):
    a, b = sorted(int(c[1:]) for c in (c1, c2))
    return 'e%d%d' % (a, b)


def neg(a):
    return a[:-1] if a.endswith("'") else a + "'"


# ------------------------------------------------------------- phrase parsing
def attrs_of(s):
    """'$xm$', "$m'$", 'not-$y$' -> list of attributes, or None."""
    s = re.sub(r'not-\$([xym])\$', lambda m: '$' + neg(m.group(1)) + '$', s)
    spans = re.findall(r'\$([^$]+)\$', s)
    rest = re.sub(r'\$[^$]+\$', '', s)
    if not spans or rest.strip():
        return None
    out = []
    for sp in spans:
        if not re.fullmatch(r"[xym]{1,2}'?", sp):
            return None
        negated = sp.endswith("'")
        for ch in sp.rstrip("'"):
            out.append(neg(ch) if negated else ch)
    return out


def parse_props(text):
    """'No $x$ are $m$; All $xm$ are $y$.' -> [(quant, subj, pred), ...]."""
    out = []
    for part in text.replace('\\\n', ' ').split(';'):
        part = ' '.join(part.split()).rstrip('.').strip()
        if not part:
            continue
        m = re.match(r'^(Some|No|All)\s+(.*?)\s+are\s+(.*?)$', part)
        if not m:
            return None
        quant, subj, pred = m.groups()
        sa, pa = attrs_of(subj), attrs_of(pred)
        if sa is None or pa is None:
            return None
        out.append((quant, sa, pa))
    return out or None


# ------------------------------------------------------- Carroll's rules
def mark(props):
    """Premises -> counters of the larger diagram.  Negative parts of all
    premises first (in order), then the affirmative ones -- as in Ch. I §2."""
    counters = {}
    negatives, positives = [], []
    for quant, subj, pred in props:
        if quant == 'No':
            negatives.append((subj, pred))
        elif quant == 'Some':
            positives.append((subj, pred))
        else:  # All = Some + No with the opposite predicate
            negatives.append((subj, [neg(p) for p in pred]))
            positives.append((subj, pred))
    for subj, pred in negatives:
        for c in cells_with(subj + pred):
            counters[c] = '0'
    for subj, pred in positives:
        cells = cells_with(subj + pred)
        free = [c for c in cells if counters.get(c) != '0']
        if len(free) == 1:
            counters[free[0]] = '1'
        elif len(free) == 2:
            if any(counters.get(c) == '1' for c in free):
                continue        # the oblong is already known to be occupied (see below)
            counters[line_slot(*free)] = '1'
        else:
            return None         # contradiction: nowhere for the red counter to go
    # the "remarks on No. 7, p. 60" convention: a red counter on a line whose
    # meaning ("one of the two compartments is occupied") is already expressed
    # by a red counter in one of those compartments is not printed in the book
    # (Ch. III §7 Nos. 20 and 32 -- diagrams without such a counter)
    for slot in [s for s in counters if s.startswith('e')]:
        if any(counters.get(c) == '1' for c in slot_cells(slot)):
            del counters[slot]
    return counters


def slot_cells(slot):
    """'e915' -> ['c9', 'c15']: the compartment numbers are glued together, split by range."""
    s = slot[1:]
    for cut in (1, 2):
        a, b = int(s[:cut]), int(s[cut:])
        if 5 <= a < b <= 16:
            return ['c%d' % a, 'c%d' % b]
    raise KeyError('bad line slot ' + slot)


def transfer(counters):
    """Larger diagram -> smaller one (the m-divisions go away).

    Ch. I's rule, verbatim: a compartment of the smaller Diagram is occupied
    if at least one of its m/m'-halves is ("True, it is only ONE compartment
    of it that is so marked; but that is quite enough"); empty only if BOTH
    halves are ("wholly 'empty', since BOTH compartments are so marked").  If
    only one half is grey and nothing is known about the other, nothing can
    be said about the compartment -- "as we do not know WHICH is the case, we
    can say nothing about THIS Square".  The latter is what leaves the
    smaller diagrams of Nos. 23 and 25 empty: "There is 'no information' for
    the smaller Diagram".

    A red counter on a line one of whose sides is grey is first resolved
    into the free compartment.
    """
    cells = {s: v for s, v in counters.items() if s.startswith('c')}
    lines = [s for s in counters if s.startswith('e')]
    for slot in lines:
        pair = slot_cells(slot)
        grey = [c for c in pair if cells.get(c) == '0']
        if len(grey) == 1:
            cells[[c for c in pair if c != grey[0]][0]] = '1'
        # both grey -- contradictory premises; both free -- handled below
    small = {}
    for s in ('c5', 'c6', 'c7', 'c8'):
        halves = [cells.get(c) for c in SMALL_OF if SMALL_OF[c] == s]
        if '1' in halves:
            small[s] = '1'
        elif all(v == '0' for v in halves):
            small[s] = '0'
    for slot in lines:
        pair = slot_cells(slot)
        if any(cells.get(c) == '0' for c in pair):
            continue            # resolved -- already counted via its compartment
        sp, sq = (SMALL_OF[c] for c in pair)
        if sp == sq:            # a line inside one smaller-Diagram compartment:
            small[sp] = '1'     # that compartment is occupied
        # a line between two smaller-Diagram compartments ("one of the two
        # is occupied") does not transfer: that much is known anyway
    return small


# ------------------------------------------------------------------ material
def items(block):
    """Section -> {item number: item body} (items of the form **N.** or N.)."""
    parts = re.split(r'^(?:\*\*(\d+)\.\*\*|(\d+)\.)\s+', block, flags=re.M)
    out = {}
    for i in range(1, len(parts), 3):
        out[int(parts[i] or parts[i + 1])] = parts[i + 2]
    return out


def figs_of(body):
    return [int(g) for g in re.findall(r'!\[\]\(media/\d\d-(\d+)\.svg', body)]


def restatement(body):
    """The symbolic restatement in a §6 answer: text before the image, minus 'i.e.'."""
    text = body.split('![](')[0]
    text = re.sub(r'\bi\.e\.', '', text)
    text = re.sub(r'\[See[^\]]*\]', '', text)
    return ' '.join(text.split())


def premises_conclusion(body):
    """§7 Nos. 13-32: '…; $\\therefore$ …' -> (premises, conclusions) or None.

    Two-column layout: the first premise and the first conclusion share a
    line; the second premise (and a possible second conclusion) sit on the
    next one.
    """
    m = re.search(r'^(.*?);\s*\$\\therefore\$\s*(.*?)$', body, flags=re.M)
    if not m:
        m2 = re.search(r'\n\n((?:Some|No|All) [^\n]*(?:\n[^\n]+)*?)\.\s*\n\n'
                       r"There is 'no information'", body)
        if m2:
            return m2.group(1).rstrip('.'), []
        return None
    prem = m.group(1)
    concl = [m.group(2).rstrip('.')]
    rest = body[m.end():].lstrip()
    line = rest.split('\n', 1)[0].strip()
    if line:
        parts = re.split(r'\.\s{2,}', line)
        prem += '; ' + parts[0].rstrip('.')
        if len(parts) > 1:
            concl.append(parts[1].rstrip('.'))
    return prem, concl


# ------------------------------------------------------------------ checking
def fmt(d):
    return str(dict(sorted(d.items())))


def compare(tag, want, have, stats):
    if want is None:
        stats['unparsed'] += 1
        print('   ?%-9s unparsed' % tag)
        return
    if want != have:
        stats['bad'] += 1
        print('   !%-9s expected %-40s diagram has %s' % (tag, fmt(want), fmt(have)))
    else:
        stats['ok'] += 1


def compare_small(tag, transferred, have, stats):
    """The §7 answer's smaller diagram against the transfer -- strict equality.

    Carroll draws the transfer in full, omitting nothing: verified on all 32
    smaller diagrams in the book, every one matched to the counter.  So a
    missing counter is as much a mismatch as an extra one, and checking only
    what is drawn would leave half the diagram unchecked (which is exactly
    how the Ch. II §7 No. 4 defect slipped through)."""
    if transferred != have:
        stats['bad'] += 1
        print('   !%-9s transfer gives %-40s diagram has %s'
              % (tag, fmt(transferred), fmt(have)))
    else:
        stats['ok'] += 1


def compare_concl(tag, sentences, small, stats):
    """The worded conclusion against the smaller diagram: a full match or a
    subset (Carroll does not always read off every consequence) -- anything
    else is a mismatch."""
    want = {}
    for s in sentences:
        marks = selfcheck.parse(s)
        if marks is None:
            stats['unparsed'] += 1
            print('   ?%-9s conclusion unparsed: %s' % (tag, s))
            return
        want.update(marks)
    if want == small:
        stats['ok'] += 1
    elif all(small.get(k) == v for k, v in want.items()):
        extra = {k: v for k, v in small.items() if k not in want}
        stats['ok'] += 1
        print('   .%-9s conclusion narrower than the diagram (which adds %s): %s'
              % (tag, fmt(extra), ' / '.join(sentences)))
    else:
        stats['bad'] += 1
        print('   !%-9s conclusion %-30s diagram %-30s  << %s'
              % (tag, fmt(want), fmt(small), ' / '.join(sentences)))


def main(book):
    ch2s = selfcheck.sections_of(book, 2)
    ch3s = selfcheck.sections_of(book, 3)
    m2 = compare_diagrams.english_models(2, book)
    m3 = compare_diagrams.english_models(3, book)
    q6 = selfcheck.numbered_text(ch2s['6'])
    a6, a7 = items(ch3s['6']), items(ch3s['7'])
    q7 = items(ch2s['7'])
    stats = {'ok': 0, 'bad': 0, 'unparsed': 0}

    print('--- Ch. II §6 Nos. 1-8 (words) against Ch. III §6 (diagrams)')
    for n in range(1, 9):
        figs = figs_of(a6[n])
        props = parse_props(q6.get(n, ''))
        want = mark(props) if props else None
        compare('§6 No.%d' % n, want, m3[figs[0] - 1][1], stats)

    print('--- Ch. III §6 Nos. 9-20: symbolic restatement against its own diagram')
    rest6 = {}
    for n in range(9, 21):
        figs = figs_of(a6[n])
        if n == 20:
            m = re.search(r'Hence,\s*(.*?)\s+and the required Diagram', a6[n], re.S)
            text = m.group(1) if m else None
        else:
            text = restatement(a6[n])
        props = parse_props(text) if text else None
        rest6[n] = props
        want = mark(props) if props else None
        compare('§6 No.%d' % n, want, m3[figs[0] - 1][1], stats)

    print('--- Ch. II §7 Nos. 1-4: larger diagram transferred to the smaller + conclusion')
    for n in range(1, 5):
        large = m2[figs_of(q7[n])[0] - 1][1]
        want = transfer(large)
        have = m3[figs_of(a7[n])[0] - 1][1]
        compare_small('§7 No.%d' % n, want, have, stats)
        parts = re.split(r'\bi\.e\.', a7[n].split('\n')[0])
        concl = [parts[1].strip().rstrip('.')] if len(parts) > 1 else []
        compare_concl('§7 No.%d concl' % n, concl, have, stats)

    print('--- Ch. II §7 Nos. 5-12: premises of §6 Nos. 13-20 -> smaller diagram + conclusion')
    for n in range(5, 13):
        props = rest6.get(n + 8)
        want = transfer(mark(props)) if props else None
        have = m3[figs_of(a7[n])[0] - 1][1]
        if want is None:
            compare('§7 No.%d' % n, None, have, stats)
        else:
            compare_small('§7 No.%d' % n, want, have, stats)
        parts = re.split(r'\bi\.e\.', a7[n].split('\n')[0])
        concl = [parts[1].strip().rstrip('.')] if len(parts) > 1 else []
        compare_concl('§7 No.%d concl' % n, concl, have, stats)

    print('--- Ch. III §7 Nos. 13-32: premises -> larger -> smaller + conclusion')
    for n in range(13, 33):
        figs = figs_of(a7[n])
        pc = premises_conclusion(a7[n])
        if pc is None:
            compare('§7 No.%d' % n, None, {}, stats)
            continue
        prem, concl = pc
        props = parse_props(prem)
        want_large = mark(props) if props else None
        have_large = m3[figs[0] - 1][1]
        compare('§7 No.%d large' % n, want_large, have_large, stats)
        want_small = transfer(have_large)
        have_small = m3[figs[1] - 1][1]
        compare_small('§7 No.%d small' % n, want_small, have_small, stats)
        if concl:
            compare_concl('§7 No.%d concl' % n, concl, have_small, stats)

    print('\nmatched %d, mismatched %d, unparsed %d'
          % (stats['ok'], stats['bad'], stats['unparsed']))
    return 1 if stats['bad'] or stats['unparsed'] else 0


if __name__ == '__main__':
    p = argparse.ArgumentParser(
        description='The book against its own answer key, on the larger Diagram.')
    p.add_argument('edition', nargs='?', default=compare_diagrams.DEFAULT_EDITION,
                   help='edition folder (default: corpus/en-CA/1887_The_Game_of_Logic)')
    sys.exit(main(p.parse_args().edition))
