#!/usr/bin/env python3
"""Render a corpus edition to HTML and PDF.

The pipeline is the one recorded in each edition's render.css:
markdown -> self-contained HTML (Quarto) -> PDF (headless Chrome).

The engine renders documents; which documents there are, what each is
made of and where it lands is the caller's decision.  A per-edition
script beside this file describes the printouts a teacher actually hands
out — its `Document` list names an output path for each and, when one
printout gathers several section files of a chapter, the run of sections
to merge.  The bare CLI has no such opinion: it renders every markdown
file of the folder, mirroring the folder structure.

A merged document is built the way the corpus splits chapters: the
chapter's index file contributes everything above its `#### Sections`
link block — the chapter heading and the epigraph — and each section
file follows with its breadcrumb dropped, everything from its first
`### ` heading on.  Merging a chapter's full run of sections reproduces
the chapter as it stood before it was split into files.

Rendering runs on a copy in a temporary directory: Quarto drops its
build artifacts next to the source, and the edition folder must stay
nothing but markdown + media.

Corpus conventions this engine relies on:

* An edition is one self-contained folder under `corpus/<locale>/`, with
  its print settings in `render.css` beside the markdown; the same file
  serves every folder of the edition.
* Diagrams live in a `media/` folder beside the files that use them, so
  a file renders from its own folder with no path rewriting.  A merged
  document is assembled inside the chapter's folder for the same reason.

Usage, from the repository root:

    python3 lib/render/render.py corpus/en-CA/1887_The_Game_of_Logic

or through the per-edition entry points beside this file, one per work.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

SECTIONS_MARKER = "#### Sections"

# Quarto settings shared by every document: a table of contents in the
# margin for on-screen reading, everything embedded so one HTML file is the
# whole document, and the edition's own render.css for print.
QUARTO_METADATA = [
    "toc:true",
    "toc-location:left",
    "toc-depth:3",
    "theme:litera",
    "embed-resources:true",
    "fontsize:1.05em",
    "css:render.css",
]

CHROME_FLAGS = [
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    "--generate-pdf-document-outline",
    "--virtual-time-budget=15000",
]


class RenderError(RuntimeError):
    """A pipeline stage failed, or a corpus convention was broken."""


@dataclass(frozen=True)
class Document:
    """One printable document.

    `out` is the output stem relative to the output folder — it decides
    both where the HTML and PDF land and what they are called.  `source`
    is a markdown path relative to the edition root: the file itself, or,
    when `sections` is given, the chapter index whose heading and epigraph
    open the merged document.  `sections` are the section files to merge,
    in order; all from that index's chapter.
    """

    out: Path
    source: Path
    sections: tuple[Path, ...] = ()


def find_quarto() -> str:
    """Quarto: $QUARTO, then PATH, then the per-user install."""
    candidates = [
        os.environ.get("QUARTO"),
        shutil.which("quarto"),
        str(Path.home() / "Applications/quarto/bin/quarto"),
    ]
    for c in candidates:
        if c and Path(c).is_file():
            return c
    raise RenderError("Quarto not found: install it or point $QUARTO at the binary")


def find_chrome() -> str:
    """Chrome: $CHROME, then the macOS app bundle, then PATH."""
    candidates = [
        os.environ.get("CHROME"),
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        shutil.which("google-chrome"),
        shutil.which("chromium"),
    ]
    for c in candidates:
        if c and Path(c).is_file():
            return c
    raise RenderError("Chrome not found: install it or point $CHROME at the binary")


def collect_documents(edition: Path) -> list[Document]:
    """Every markdown file of the edition, one document each, mirroring
    the folder structure.  Sorted by path, which puts a chapter's index
    right before the chapter's own sections; the edition README first.
    """
    paths = sorted(
        p.relative_to(edition)
        for p in edition.rglob("*.md")
        if "media" not in p.parts
    )
    readme = Path("README.md")
    if readme in paths:
        paths.remove(readme)
        paths.insert(0, readme)
    return [Document(out=p.with_suffix(""), source=p) for p in paths]


def assemble_merged(edition: Path, doc: Document) -> str:
    """The merged markdown for a document with sections.

    The chapter index contributes everything above its `#### Sections`
    link block; each section file follows from its first `### ` heading,
    its breadcrumb dropped.
    """
    index = edition / doc.source
    lines = index.read_text(encoding="utf-8").splitlines(keepends=True)
    marker = next(
        (i for i, line in enumerate(lines) if line.rstrip("\n") == SECTIONS_MARKER),
        None,
    )
    if marker is None:
        raise RenderError(f"{doc.source}: no '{SECTIONS_MARKER}' block found")
    parts = lines[:marker]
    for rel in doc.sections:
        body = (edition / rel).read_text(encoding="utf-8").splitlines(keepends=True)
        start = next((i for i, line in enumerate(body) if line.startswith("### ")), None)
        if start is None:
            raise RenderError(
                f"{rel}: no '### ' heading — cannot tell the breadcrumb "
                "from the section's content"
            )
        parts += body[start:]
    return "".join(parts)


def _check(doc: Document, edition: Path) -> None:
    for rel in (doc.source, *doc.sections):
        if not (edition / rel).is_file():
            raise RenderError(f"no such file in the edition: {rel}")
    parents = {rel.parent for rel in doc.sections}
    if len(parents) > 1:
        raise RenderError(f"{doc.out}: sections span several folders: {sorted(parents)}")


def _run(cmd: list[str], cwd: Path | None = None) -> None:
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RenderError(
            f"{Path(cmd[0]).name} exited with {proc.returncode}:\n"
            f"{proc.stderr.strip() or proc.stdout.strip()}"
        )


def _page_count(pdf: Path) -> str:
    """'NN pp.' via pdfinfo, or '' when poppler is not installed."""
    pdfinfo = shutil.which("pdfinfo")
    if not pdfinfo:
        return ""
    proc = subprocess.run([pdfinfo, str(pdf)], capture_output=True, text=True)
    match = re.search(r"^Pages:\s+(\d+)", proc.stdout, re.MULTILINE)
    return f"{match.group(1)} pp." if match else ""


def render_edition(edition: Path, out: Path, documents: list[Document] | None = None) -> None:
    """The whole pipeline: copy, assemble what merges, render, deliver."""
    edition = edition.resolve()
    if not edition.is_dir():
        raise RenderError(f"not an edition folder: {edition}")
    quarto = find_quarto()
    chrome = find_chrome()
    docs = documents if documents is not None else collect_documents(edition)
    if not docs:
        raise RenderError(f"no documents to render under {edition}")
    for doc in docs:
        _check(doc, edition)

    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t) / edition.name
        shutil.copytree(edition, tmp)

        # A merged document is assembled inside its chapter's folder, so
        # its `media/` references resolve to the chapter's own diagrams.
        sources: dict[Path, Path] = {}  # doc.out -> md path inside tmp
        for doc in docs:
            if doc.sections:
                folder = tmp / doc.sections[0].parent
                # The name must be unique within the chapter folder: several
                # documents may merge sections of the same chapter.
                merged = folder / ("_".join(doc.out.parts) + ".md")
                if merged.exists():
                    raise RenderError(f"{doc.out}: {merged.name} already exists in {folder.name}/")
                merged.write_text(assemble_merged(edition, doc), encoding="utf-8")
                sources[doc.out] = merged
            else:
                sources[doc.out] = tmp / doc.source

        # Quarto resolves the css relative to the file it renders, so every
        # folder holding a document gets the edition's render.css.
        css = tmp / "render.css"
        if css.is_file():
            for folder in {src.parent for src in sources.values()}:
                if not (folder / "render.css").is_file():
                    shutil.copy(css, folder / "render.css")

        for doc in docs:
            src = sources[doc.out]
            metadata = [a for m in QUARTO_METADATA for a in ("--metadata", m)]
            _run([quarto, "render", src.name, "--to", "html", *metadata], cwd=src.parent)
            html = src.with_suffix(".html")
            pdf = src.with_suffix(".pdf")
            # Chrome needs an absolute file:// URL — a relative path
            # silently yields an empty PDF.
            _run([chrome, *CHROME_FLAGS, f"--print-to-pdf={pdf}", html.as_uri()])
            if not pdf.is_file() or pdf.stat().st_size == 0:
                raise RenderError(f"Chrome produced no PDF for {doc.out}")
            dest = out / doc.out.parent
            dest.mkdir(parents=True, exist_ok=True)
            shutil.copy(html, dest / f"{doc.out.name}.html")
            shutil.copy(pdf, dest / f"{doc.out.name}.pdf")
            print(f"{str(doc.out):<28} {_page_count(pdf)}".rstrip())
    print(f"-> {out}")


def default_out(edition: Path) -> Path:
    """out/<locale>/<edition> beside this script; the folder is gitignored."""
    edition = edition.resolve()
    return Path(__file__).resolve().parent / "out" / edition.parent.name / edition.name


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render a corpus edition to HTML and PDF, one document per markdown file."
    )
    parser.add_argument(
        "edition",
        type=Path,
        help="edition folder, e.g. corpus/en-CA/1887_The_Game_of_Logic",
    )
    parser.add_argument(
        "-o",
        "--out",
        type=Path,
        default=None,
        help="output folder (default: lib/render/out/<locale>/<edition>)",
    )
    args = parser.parse_args(argv)
    try:
        render_edition(args.edition, args.out or default_out(args.edition))
    except RenderError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
