# Rendering

Turns a book's markdown into printouts: one self-contained HTML file and
one PDF per document.

## Printing The Game of Logic (en-CA)

```
python3 lib/render/render_the_game_of_logic_en_ca.py
```

This prints the book the way it is handed out: three rounds, a folder
each, holding two or three documents — theory, exercises, answers. The
chapter index files, the preface and the edition README are navigation
and apparatus, not printouts, and are skipped.

That selection is the point of the per-edition script. Every work gets
one, named `render_<work>_<locale>.py`: it pins the edition folder and
says what is worth printing and how it is gathered; everything else is
the generic engine.

The result lands in `lib/render/out/en-CA/1887_The_Game_of_Logic/`. The
`out/` folder is build output and is not tracked by git; `--out` sends it
elsewhere.

### Handing the printouts out

The four chapters play four parts: chapter I teaches, chapter II sets the
work, chapter III answers it, chapter IV examines. Only chapter I is
meant to be read.

**The book is not meant to be read straight through.** §1 of chapter I
carries everything needed for §§1–5 of chapter II; the larger diagram is
not wanted until §6, and fallacies not until the end. So it goes out in
three rounds — one folder each — and each is small: a reader who has
finished the first has done a third of the book, and can already
represent and read back any proposition about two attributes.

**`round_1/` — the smaller diagram: two attributes.**

| | Made of | Pages |
|---|---|---|
| `01_theory.pdf` | ch. I §1, Propositions | 17 |
| `02_exercises.pdf` | ch. II §§1–5 | 9 |
| `03_answers.pdf` | ch. III §§1–5 | 13 |

**`round_2/` — the larger diagram: syllogisms.**

| | Made of | Pages |
|---|---|---|
| `01_theory.pdf` | ch. I §2, Syllogisms | 10 |
| `02_exercises.pdf` | ch. II §§6–7 | 5 |
| `03_answers.pdf` | ch. III §§6–7 | 17 |

**`round_3/` — what goes wrong, and the examination.**

| | Made of | Pages |
|---|---|---|
| `01_theory.pdf` | ch. I §3, Fallacies | 4 |
| `02_examination.pdf` | ch. IV, Hit or Miss | 9 |

Within a round the pairing is close: §2 and §4 of chapter II ask for a
proposition to be drawn, §3 and §5 for a drawing to be read back. They
are one skill in two directions, and are worth setting together rather
than one after the other.

**Hand the answers out separately, and afterwards.** Chapter III does not
merely answer: it works several of the exercises through, so a reader
holding it has been told more than the exercise meant to ask.

**Chapter IV has no answers** — not in this edition and not in Carroll's.
Its 101 pairs of premises are for the teacher to mark.

**Counters.** The 1887 book was sold with an envelope holding a card
diagram and nine counters, four red and five grey, and the text assumes
the reader has them to hand. They are not reproduced here, and the
diagrams print the digits `1` and `0` the book itself prints in their
place, so it can all be read without them. It is still a game: a board
and counters, cut out and made, are worth the half hour they cost.

One deliberate oddity to expect: the answer to chapter II §5, exercise 3
carries a note from the edition's editor asking the reader to settle a
contradiction in the 1887 printing. The edition's own README explains it,
under *One error left for the reader*.

## Rendering any edition

```
python3 lib/render/render.py corpus/en-CA/1887_The_Game_of_Logic
```

The generic engine has no opinion on what to print: called like this, it
renders every markdown file of the folder, mirroring its structure. Add
`-o some/folder` to send the output elsewhere.

## The pipeline

```
markdown  ->  Quarto  ->  self-contained HTML  ->  headless Chrome  ->  PDF
```

The HTML embeds everything — the diagrams go in as data URIs — so the one
file is the whole document and can be mailed or opened offline. Chrome
then prints it to PDF. Print settings (page size, the typeface, the
two-column exercise rows) are not in the scripts: they live in the
edition's own `render.css`, beside the markdown, so the book can be
rebuilt from its folder alone. The engine only picks that file up, for
every folder of the edition.

A document is either one markdown file, or a run of a chapter's section
files merged into one printout. A merged document opens with the chapter
heading and epigraph, taken once from the chapter's index file; each
section follows with its repeated heading dropped — everything from its
first `### ` heading on. Merging a chapter's full run of sections
reproduces the chapter as it stood before it was split into files.

Rendering runs on a copy in a temporary directory: Quarto drops its build
artifacts next to the source, and the edition folder must stay nothing
but markdown + media.

## What it needs installed

The pipeline is built for and tested on macOS only. Nothing in it is
macOS-specific in principle — Quarto, Chrome and Python run everywhere —
but the tool lookup below knows the macOS locations, and no other OS has
been tried. Adapting it is out of scope for now; on another OS, start by
pointing `QUARTO` and `CHROME` at the binaries.

| Tool | Found at | Override |
|---|---|---|
| [Quarto](https://quarto.org) | `PATH`, then `~/Applications/quarto/bin/quarto` | `QUARTO=/path/to/quarto` |
| Google Chrome | the macOS app bundle, then `PATH` | `CHROME=/path/to/chrome` |
| `pdfinfo` (poppler) | `PATH` | optional — only prints the page counts in the report |
