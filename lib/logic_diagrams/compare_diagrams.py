#!/usr/bin/env python3
"""Compare a chapter's diagrams in another edition against the English ones.

    python3 lib/logic_diagrams/compare_diagrams.py 2 path/to/ch2.diagrams.json [edition]

The JSON file lists the other edition's diagrams in print order, one
`[kind, counters, labels]` entry per diagram.  A match on the kind and on
every counter confirms that the page was read correctly.  A mismatch means
one of three things: a misprint in the other edition, a defect in the English
source, or a transcription error.

The other edition's chapter need not be complete -- the first N diagrams are
compared, where N is however many its file holds.

This script is specific to The Game of Logic: it knows the book's chapters
and their file names.
"""
import argparse, json, os, sys
import notation

DEFAULT_EDITION = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               '..', '..', 'corpus', 'en-CA', '1887_The_Game_of_Logic')
CHAPTER_FILE = {1: '01_new_lamps_for_old', 2: '02_cross_questions',
                3: '03_crooked_answers', 4: '04_hit_or_miss'}


def english_models(chapter, book=DEFAULT_EDITION):
    """The chapter's diagrams, in print order, from the folder's own image titles.

    Reads the delivered markdown, not the Gutenberg transcription: an image's
    title carries the diagram's whole content (see `notation.py`), with
    the source corrections already applied.  So the check speaks about the
    book the reader is actually holding.
    """
    md = open(os.path.join(book, CHAPTER_FILE[chapter] + '.md'), encoding='utf-8').read()
    out = []
    for _name, title in notation.images(md):
        kind, counters, _labels, _numbers = notation.decode(title)
        out.append((kind, counters))
    return out


def key(kind, counters):
    return kind, tuple(sorted(counters.items()))


def main(chapter, other_path, book):
    en = english_models(chapter, book)
    other = [(k, c) for k, c, _labels in json.load(open(other_path, encoding='utf-8'))]
    n = min(len(en), len(other))
    print('chapter %d: %d English diagrams, %d in the other edition, comparing the first %d'
          % (chapter, len(en), len(other), n))

    bad = 0
    for i in range(n):
        if key(*en[i]) != key(*other[i]):
            bad += 1
            print('  #%-3d  EN %-8s %-30s  OTHER %-8s %s'
                  % (i + 1, en[i][0], dict(sorted(en[i][1].items())),
                     other[i][0], dict(sorted(other[i][1].items()))))
    if len(other) > len(en):
        print('  WARNING: the other edition has more diagrams than the English one -- numbering shift')
    print('mismatches: %d' % bad)
    return 1 if bad else 0


if __name__ == '__main__':
    p = argparse.ArgumentParser(
        description="Compare another edition's diagrams with the English ones, "
                    'chapter by chapter.')
    p.add_argument('chapter', type=int, choices=sorted(CHAPTER_FILE),
                   help='chapter number')
    p.add_argument('diagrams_json',
                   help="the other edition's diagrams: a JSON list of "
                        '[kind, counters, labels] in print order')
    p.add_argument('edition', nargs='?', default=DEFAULT_EDITION,
                   help='the English edition folder '
                        '(default: corpus/en-CA/1887_The_Game_of_Logic)')
    args = p.parse_args()
    sys.exit(main(args.chapter, args.diagrams_json, args.edition))
