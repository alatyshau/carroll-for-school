#!/usr/bin/env python3
"""Print The Game of Logic, en-CA edition, as the teacher hands it out.

What gets printed — and this script's whole reason to exist — is the
edition's own selection.  The book is not meant to be read straight
through: it goes out in three rounds, and the output is three folders,
two or three documents each — theory, exercises, answers.

* `round_1/` — the smaller diagram: two attributes.  §1 of chapter I,
  then §§1–5 of chapters II and III, each run merged into one document.
* `round_2/` — the larger diagram: syllogisms.  §2 of chapter I, then
  §§6–7 of chapters II and III.
* `round_3/` — what goes wrong, and the examination.  §3 of chapter I
  and chapter IV, which has no sections.

The chapter index files, the preface and the edition README are
navigation and apparatus, not printouts, and are skipped.

    python3 lib/render/render_the_game_of_logic_en_ca.py

The result lands in lib/render/out/en-CA/1887_The_Game_of_Logic/ — one
self-contained HTML file and one PDF per document.  The output is not
tracked by git; override it with --out.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render
from render import Document

EDITION = Path(__file__).resolve().parents[2] / "corpus" / "en-CA" / "1887_The_Game_of_Logic"

THEORY = "01_new_lamps_for_old"
EXERCISES = "02_cross_questions"
ANSWERS = "03_crooked_answers"

# Chapters II and III run section for section in parallel: II sets the
# work, III answers it.  Their first five sections need only the smaller
# diagram, taught by §1 of chapter I; the larger diagram arrives with §2
# of chapter I and is not wanted until §6.
SMALLER_DIAGRAM_SECTIONS = 5


def _sections(chapter: str) -> list[Path]:
    found = sorted((EDITION / chapter).glob("*.md"))
    if len(found) != 7:
        raise render.RenderError(f"{chapter}/: expected 7 section files, found {len(found)}")
    return [p.relative_to(EDITION) for p in found]


def documents() -> list[Document]:
    exercises = _sections(EXERCISES)
    answers = _sections(ANSWERS)
    smaller, larger = slice(None, SMALLER_DIAGRAM_SECTIONS), slice(SMALLER_DIAGRAM_SECTIONS, None)
    return [
        Document(Path("round_1/01_theory"), Path(f"{THEORY}/01_propositions.md")),
        Document(Path("round_1/02_exercises"), Path(f"{EXERCISES}.md"), tuple(exercises[smaller])),
        Document(Path("round_1/03_answers"), Path(f"{ANSWERS}.md"), tuple(answers[smaller])),
        Document(Path("round_2/01_theory"), Path(f"{THEORY}/02_syllogisms.md")),
        Document(Path("round_2/02_exercises"), Path(f"{EXERCISES}.md"), tuple(exercises[larger])),
        Document(Path("round_2/03_answers"), Path(f"{ANSWERS}.md"), tuple(answers[larger])),
        Document(Path("round_3/01_theory"), Path(f"{THEORY}/03_fallacies.md")),
        Document(Path("round_3/02_examination"), Path("04_hit_or_miss.md")),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print The Game of Logic (en-CA) in three hand-out rounds."
    )
    parser.add_argument(
        "-o",
        "--out",
        type=Path,
        default=render.default_out(EDITION),
        help="output folder (default: lib/render/out/en-CA/1887_The_Game_of_Logic)",
    )
    args = parser.parse_args()
    try:
        render.render_edition(EDITION, args.out, documents())
    except render.RenderError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
