# Carroll for School

Lewis Carroll's math & logic books re-edited for high-school readers, in English and Russian: clean markdown, a chapter to a file, diagrams stored as text and drawn from it.

This is an open source product, not a working directory: everything in the
repository is finished work, held to publication quality. Drafts, research
notes and half-done chapters live outside it and arrive only when ready.

## Layout

* `corpus/<locale>/<edition>/` — the books, one self-contained folder per
  edition. The locale comes first: editions differ by their reader and that
  reader's typographic norm, not merely by language.
* `lib/logic_diagrams/` — the diagram tooling and the self-checks that let
  the book verify itself; see its [README](lib/logic_diagrams/README.md).

## License

Carroll's books are in the public domain and always were. Everything this project adds — the corrections and the evidence for them, the editorial apparatus, the redrawn diagrams and the tooling — is released under [CC0 1.0](LICENSE): no rights reserved. Copy it, print it, change it, sell it, put it in a textbook of your own; no permission needed and no attribution required. A note saying where it came from is welcome, never asked for.

