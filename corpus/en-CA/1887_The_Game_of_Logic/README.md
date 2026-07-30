# The Game of Logic

**Lewis Carroll**, 1887

Introduction to syllogisms through a board game: on a diagram of intersecting regions, red and grey counters are placed by rules to determine what conclusion follows from two premises. Written so a schoolchild could work through it alone. Four chapters — theory, exercises, answers, and a final test.

---

## Table of Contents

| # | File | Section |
|---|------|---------|
| 0 | [00_preface.md](00_preface.md) | Title, dedication poem, preface |
| 1 | [01_new_lamps_for_old.md](01_new_lamps_for_old.md) | Chapter I. New Lamps for Old |
| 2 | [02_cross_questions.md](02_cross_questions.md) | Chapter II. Cross Questions |
| 3 | [03_crooked_answers.md](03_crooked_answers.md) | Chapter III. Crooked Answers |
| 4 | [04_hit_or_miss.md](04_hit_or_miss.md) | Chapter IV. Hit or Miss |

---

## Source

*The Game of Logic*, London, Macmillan, 1887 — the edition this one is made from, and the authority wherever anything is in doubt. It is read from a scan of the printing itself, `Lewis Carroll. The Game of Logic [1887].pdf`.

This is a present-day Canadian edition for a high-school reader, not a facsimile. The text is Carroll's, word for word, apart from the corrections and the modernized forms listed below. The diagrams are redrawn: Carroll's compartments are set as vector squares, and a counter is shown as the digit the 1887 book prints in its place — `1` where the reader is to put a red counter, `0` where a grey one, exactly as chapter I explains.

**How the text was keyed.** Not by hand: it was taken from a digital transcription, Project Gutenberg [#4763](https://www.gutenberg.org/ebooks/4763), from `Lewis Carroll. The Game of Logic.zip`. That saved the labour of typing the book out, and nothing more — the transcription is not the source, and has been caught both dropping a counter and adding one. Wherever it was found to differ from the printed page, the page was followed and the place is listed below. A page-by-page collation against the 1887 printing is not yet finished; until it is, that list is what has been found, not a guarantee of what is there.

---

## How a diagram is written

Open any chapter and a diagram looks like this:

```
![](media/02-013.svg "BIL c6=1 c8=0")
```

The line in quotation marks is the diagram itself, written out. The picture is drawn from it, so it is the line that is edited, never the drawing.

| | |
|---|---|
| `cN` | compartment N holds a counter |
| `1`, `0` | a red counter, a grey one |
| `eNM` | a counter sitting on the line that divides compartments N and M |
| `labels` | the board is lettered *x*, *y*, *m* |
| `numbers` | the compartments are numbered, as on the frontispiece |

Nothing here is this edition's invention. The compartment numbers are Carroll's own and are printed on his board — 5 to 8 on the smaller diagram, 9 to 16 on the larger. So are the digits: chapter I sets out that he writes `1` where the reader is to place a red counter and `0` where a grey one.

The first word says which board, and how much of it. Carroll prints only the part that is in play, so the halves have names of their own:

| | |
|---|---|
| `BIL` | the smaller diagram, compartments 5–8 |
| `BIL_T`, `BIL_L`, `BIL_R` | its top half (5, 6), left half (5, 7), right half (6, 8) |
| `TRI` | the larger diagram, compartments 9–16 |
| `TRI_T`, `TRI_B` | its top half (9–12), its bottom half (13–16) |
| `TRI_ROB` | its right-hand upright oblong (10, 12, 14, 16) |

A compartment keeps its number whichever part is drawn: in `BIL_R` the compartments are still 6 and 8, though they are printed where 5 and 7 stand on the whole diagram. So one line reads the same way everywhere in the book.

---

## Corrections

Twelve places have been corrected.

They were found two ways. Chapter III is the answer key to chapter II, so much of the book can be checked against itself: every exercise was read into words, marked on the diagram Carroll's rules call for, and matched against its printed answer — on the smaller diagram fifty of the fifty-one agree, and on the larger one, where the exercise is worked on both diagrams in turn, all hundred and two checks now agree. The rest came from reading the printed page against what had been keyed in.

Eleven of the twelve never were Carroll's: the transcription lost or added something, and the 1887 page shows what he wrote. Those are not really corrections at all — they are the printed book restored. One is: ch. III, §7, answer 23 is wrong on the page itself, and it is repaired rather than merely flagged because three separate things in the book settle which side is at fault. Where the printing goes wrong and nothing settles it, this edition does not choose for Carroll — see the last section.

**Diagrams and answers**

| Where | Keyed in as | Printed here | Why |
|---|---|---|---|
| Ch. II, §3, exercise 16 | one `0`, in the upper compartment | `0` in both compartments | The book's own answer — ch. III, §3, no. 16, "No *y*′ exist" — empties the whole *y*′ column, which takes two counters. The 1887 page has both. |
| Ch. III, §2, answer 7 | `1` in both compartments | `1` in the right-hand compartment only | The exercise is "some *x* are not-*y*, and some *x* exist", which occupies *xy*′ alone — and Carroll's own sentence beside the diagram is about "some *x* are *y*′" alone. The left-hand counter would assert "some *x* are *y*", which nothing in the exercise states. |
| Ch. III, §5, answer 12 | All *y* are *x*, and all *x*′ are *y* | …and all *x*′ are *y*′ | A lost prime. The exercise it answers is marked `1` in *xy*, `0` in *x*′*y*, `1` in *x*′*y*′ — that is "all *x*′ are *y*′" — and the sentence's own gloss agrees: "all thin ones are lazy". |
| Ch. II, §7, exercise 4 | one `0` in the lower half of the inner square | `0` in both of its compartments, 13 and 14 | The 1887 page has two counters here side by side and only one survived the copying. Without the second, the book's own answer — ch. III, §7, no. 4, "no *x*′ are *y*′" — does not follow, since a square of the smaller diagram is empty only when *both* its compartments are. With it, the transfer to the smaller diagram gives that answer and nothing else. |
| Ch. III, §6, answer 9 | three `0`s, in 11, 12 and 13 | `0` in 11 and 12 | "No *x* are *m*" empties the two compartments that are both *x* and *m*. Compartment 13 is *x*′, and nothing in the proposition touches it. The book answers the same proposition twice — no. 1 of this section is "no *x* are *m*" as well — and there it marks 11 and 12 only. The 1887 page has two counters, not three. |
| Ch. III, §2, last answer | numbered 15 | numbered 19 | §2 sets nineteen exercises and answers all nineteen; the 1887 page numbers this one 19. As keyed in there is no answer to exercise 19 and two answers numbered 15. |
| Ch. III, §4, last answer | numbered 17 | numbered 23 | The same fault in the same position: twenty-three exercises, twenty-three answers, the last duplicating a real 17 earlier in the section. It answers exercise 23 exactly. |

**Text**

| Where | Keyed in as | Printed here | Why |
|---|---|---|---|
| Half-title | By Lewis Carrol | By Lewis Carroll | The name is misspelt on the half-title only. The title page, the preface signature and the running heads all read *Carroll*. |
| Ch. I, on compartment No. 5 | …or, if we use letters, **the** must be "*x* *y*." | …**they** must be… | The same sentence uses "they must be" twice before this clause, in the same construction. |
| Ch. I, on the seven words | and **you** friend will go away | and **your** friend… | The 1887 page reads "your". |
| Ch. I, on the Conclusion | the rather **meager** piece of information | …**meagre**… | The 1887 page reads "meagre". The transcription americanized it — the only such spelling in the book. |

The first three diagram faults were also checked against the 2007 Russian translation of the same edition, which prints the restored reading in all three.

**And one place where the 1887 printing itself is wrong.** This is the only correction in the book that is a correction of Carroll rather than of the copying.

| Where | The 1887 page reads | Printed here | Why |
|---|---|---|---|
| Ch. III, §7, answer 23 | No *x* are *m*; All *y* are ***m*** | …All *y* are ***m***′ | A lost prime, and this one was lost by the printer of 1887. Three things settle which side is at fault: the exercise it answers is "no muffins are wholesome; all buns are *un*wholesome", which is "all *y* are *m*′"; the diagram printed beside this very answer is the diagram for *m*′; and the answer's own verdict, "there is 'no information' for the smaller diagram", holds only for *m*′ — with *m* the transfer would empty *xy* and give the conclusion "no *x* are *y*". |

## Modernized for this edition

Forms a reader would now take for misprints have been brought up to date. None of this changes what a sentence says. Canadian usage is not simply British usage: it keeps `-our` and `grey`, so **`colour`, `colours` and `grey` are left exactly as Carroll wrote them**, while `-ise` becomes `-ize`.

| Carroll wrote | Printed here | Count | Why |
|---|---|---|---|
| Premiss, Premisses | Premise, Premises | 47 | Carroll's spelling of the logical term. It is now spelt like the ordinary word. |
| civilised, uncivilised | civilized, uncivilized | 6 | Canadian usage takes `-ize`. |
| &c. | etc. | 8 | The Victorian form. The ampersand version is no longer read as an abbreviation. |
| to-day | today | 1 | The hyphen was dropped long ago. |
| `--` between words | — (em dash, closed up) | 41 | `--` is the transcriber's ASCII stand-in for a dash. Canadian book practice sets the em dash with no spaces around it. |
| this:--"a sentence… | this: "a sentence… | 17 | The colon-dash is a dead convention; today the colon does the work alone. |

**Twenty page references have been dropped.** Carroll sends the reader from an exercise to its answer by page — "[See pp. 55, 6]" at the foot of each group of exercises. This edition has no such pages: its chapters are separate files, meant to be printed one at a time. Every one of the twenty was checked against the 1887 pagination, and every one points into the section of chapter III that carries the same number and the same title as the section the reader is already in — §1 to pp. 55–59, which is §1; §6 to pp. 67–71, which is §6, and so on through all seven. They say "see the answers to this Section", which the shape of the book says already. Two more of the same kind, inside chapter II, point at pages 49 and 50, which are §6 — the section the surrounding sentence already names. The 2007 Russian translation drops all of them too.

**Three page references have been kept**, with the address changed from page to section: "[See remarks on No. 7, § 2.]" These are the exception that proves the rest are empty — they point *out* of their own section, from §6 and §7 back to the remark under answer 7 of §2, which explains why a counter is not to be placed on a division-line. That is something the reader would not otherwise think to look up.

**One footnote has been dropped.** The transcriber of the digital source added a note apologizing for writing the "therefore" sign as the text string `&there4`, because he could not count on a font that would draw it. This edition draws the sign itself — ∴ — so the note explained a substitution the reader cannot see. Carroll's own sentence introduces the sign in passing: "putting the symbol ∴ for 'therefore'".

Left alone: `sha'n't`, `plumpudding`, `Battledores` and the like. Those are Carroll's voice, not dated conventions.

## One error left for the reader

Chapter II, §5, exercise 3 is marked `1` in *xy*′ and `0` in *x*′*y*′, which reads "**All** not-*y* are *x*". Its answer, ch. III, §5, no. 3, says "**No** not-*y* are *x*" — the opposite. Exercise 8 of the same section, marked the same way in the other column, is answered "All *x*′ are *y*′", so it is the diagram that follows the section's pattern.

It has not been corrected. The 1887 pages carry both sides exactly as the transcription has them — the diagram on p. 46, the answer on p. 65 — so the fault is Carroll's own, not a slip in copying out. That alone would not stop a correction: the answer to §7 no. 23 is a fault of the 1887 printing too, and it *is* corrected, because three separate things in the book show which side is wrong. Here nothing does. It is one printed line against one printed diagram, and the book says no more. Choosing for Carroll, and saying nothing, would hide a real question behind a tidy page.

Instead there is a note beside the answer, in square brackets and italics, telling the reader the two disagree and asking them to work out which to believe. It is the only sentence in these files that is not Carroll's. Anyone who settles it is asked to say so.
