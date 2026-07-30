# logic_diagrams

Tools for the diagrams in Carroll's *The Game of Logic* (`corpus/`).
In the book's markdown every diagram image carries a title string like this:

```markdown
![](media/02-025.svg "BIL c6=1 c8=0")
```

`"BIL c6=1 c8=0"` says everything the picture shows: the smaller, two-letter
Diagram (`BIL`), a red counter (the digit `1`) in compartment 6, a grey one
(`0`) in compartment 8 — Carroll's own terms throughout.
The SVG file is generated from its title string and never edited by hand, so
a picture cannot quietly disagree with the text. The scripts here draw the
pictures from the title strings and use them to proof-read the book; several
misprints of the 1887 printing and of its modern transcriptions were caught
this way, and every shipped correction is documented in the edition's own
README.

## The scripts

**`notation.py`** reads and writes the image title strings. `decode()` parses
`"BIL c6=1 c8=0"` into Diagram kind and counters, `encode()` builds such a
string back from them, `images()` lists every diagram image in a markdown
file. Its opening docstring defines the whole vocabulary: the Diagram kinds
(`BIL` and `TRI` — Carroll's smaller and larger Diagram — and their parts),
`cN=1`/`cN=0` for a counter in compartment N, `eNM=1` for a counter astride
the line dividing compartments N and M, `labels`/`numbers` for Diagrams
lettered $x$/$y$/$m$ or numbered as on the frontispiece.

**`carroll_svg.py`** draws one diagram: Diagram kind and counters in, SVG
text out. Pure geometry — no imports, no file paths, no knowledge of any
edition.

**`svg_from_md.py`** regenerates an edition's pictures. It scans every
markdown file in the edition folder — the chapters and the edition's README
alike — draws each title string with the two modules above, and compares the
results with the files in `media/`. Without `--write` nothing is touched:
all zeros in the report means every picture matches its title, and the
script also fails if two mentions of one file carry contradicting titles.
With `--write` it rewrites the SVG files. Run it after any edit to a title
string.

**`selfcheck.py`** proof-reads the book against itself on the smaller
Diagram. *The Game of Logic* contains its own answer key — Chapter III
answers the problems of Chapter II — so nearly every fact is stated twice:
once as a diagram, once as an English sentence. The script translates the
sentences into counters by the rules Carroll lays down in Chapter I and
demands they match the diagrams, counter for counter. Covers §§2–5. Expected
output: 51 checks, 50 matched; the one mismatch is a genuine misprint of the
1887 edition, kept as printed and flagged in the text by an editor's note.
Any other mismatch is a regression.

**`selfcheck_tri.py`** is the same proof-reading on the larger, three-letter
Diagram, §§6–7, following Carroll's full procedure: premises onto the larger
Diagram, transfer onto the smaller one, then the worded conclusion. Expected
output: 102 matched, 0 mismatched, 0 unparsed.

**`compare_diagrams.py`** checks a translated edition against the English
one: takes a chapter number and a JSON file listing the translation's
diagrams, and compares the two sets pairwise in print order. This is how a
translation in progress is verified page by page.

The two selfchecks and `compare_diagrams.py` are specific to *The Game of
Logic* — they know its chapters and their file names. `notation.py`,
`carroll_svg.py` and `svg_from_md.py` work for any edition that stores its
diagrams in title strings.

## Running

Every script takes the edition folder — markdown files plus `media/` — as an
optional argument, defaulting to the one edition in the repository today;
`--help` shows the exact usage. From the repository root:

```
python3 lib/logic_diagrams/selfcheck.py
python3 lib/logic_diagrams/svg_from_md.py corpus/en-CA/1887_The_Game_of_Logic
python3 lib/logic_diagrams/compare_diagrams.py 2 path/to/ch2.diagrams.json
```
