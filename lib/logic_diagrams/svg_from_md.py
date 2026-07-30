#!/usr/bin/env python3
"""Draw an edition's diagrams from the edition's own markdown.

    python3 lib/logic_diagrams/svg_from_md.py [edition] [--write]

Every markdown file in the edition folder is scanned for diagram images,
`![](media/02-025.svg "BIL c6=1 c8=0")`; the image title holds the whole
content of the picture (see notation.py), so the folder needs nothing but
itself to draw its diagrams again.

Without --write nothing is touched: the diagrams are drawn into memory and
compared with the files in media/, and every difference is reported -- a file
without a title, a title without a file, a picture that does not match its
title, or two mentions of the same file whose titles contradict each other.
With --write, media/ is rewritten from the titles.
"""
import argparse, os, sys
import carroll_svg, notation

DEFAULT_EDITION = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               '..', '..', 'corpus', 'en-CA', '1887_The_Game_of_Logic')


def drawn(book):
    """{file name -> SVG source}, drawn from the image titles of the folder."""
    out, seen_in = {}, {}
    for tag in sorted(f for f in os.listdir(book) if f.endswith('.md')):
        md = open(os.path.join(book, tag), encoding='utf-8').read()
        for name, title in notation.images(md):
            kind, counters, labels, numbers = notation.decode(title)
            svg = carroll_svg.render(kind, counters, labels=labels, numbers=numbers)
            if out.get(name, svg) != svg:
                raise SystemExit('%s: the title in %s contradicts the one in %s'
                                 % (name, tag, seen_in[name]))
            out[name] = svg
            seen_in[name] = tag
    return out


def main(book, write):
    new = drawn(book)
    media = os.path.join(book, 'media')
    have = sorted(f for f in os.listdir(media) if f.endswith('.svg'))

    missing = [f for f in have if f not in new]
    extra = [f for f in new if f not in set(have)]
    differ = [f for f in have if f in new
              and open(os.path.join(media, f), encoding='utf-8').read() != new[f]]

    print('%d diagrams in the titles, %d files in media/' % (len(new), len(have)))
    for label, lst in (('no title', missing), ('no file', extra),
                       ('differ', differ)):
        print('%-12s %d%s' % (label, len(lst), ('  ' + ', '.join(lst[:8])) if lst else ''))

    if write:
        if missing or extra:
            raise SystemExit('the sets do not match -- not rewriting')
        for f, svg in new.items():
            open(os.path.join(media, f), 'w', encoding='utf-8').write(svg)
        print('media/ redrawn from the titles: %d files' % len(new))
    elif missing or extra or differ:
        raise SystemExit(1)


if __name__ == '__main__':
    p = argparse.ArgumentParser(
        description="Draw an edition's diagrams from its image titles and "
                    'compare them with media/.')
    p.add_argument('edition', nargs='?', default=DEFAULT_EDITION,
                   help='edition folder: markdown files + media/ '
                        '(default: corpus/en-CA/1887_The_Game_of_Logic)')
    p.add_argument('--write', action='store_true',
                   help='rewrite media/ from the titles instead of only checking')
    args = p.parse_args()
    main(args.edition, args.write)
