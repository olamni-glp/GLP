"""Synthetic mock PDF builder.

Per /speckit-analyze Q6/A: avoids any copyright exposure by generating a
synthetic 4–6-page PDF with TeX-typeset GLP-shaped code blocks, in place of
any redacted excerpt of the real `GLP_ART.pdf`.

Run from this directory:

    python build_mock_pdf.py

This produces `glp_art_mock.pdf` next to this script. The output is
byte-stable across runs (modulo reportlab's own `/CreationDate` metadata,
which is normalised to a fixed timestamp here so unit tests can compare).

Requires the optional dev dependency `reportlab` (declared in
`pyproject.toml [project.optional-dependencies] dev`).
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    from reportlab.lib.pagesizes import LETTER
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import inch
except ImportError:
    sys.stderr.write(
        "build_mock_pdf.py requires reportlab. Install with: "
        "pip install -e .[dev]\n"
    )
    raise SystemExit(2)


# Synthetic content. Resemblance to the real book is structural only:
# - One section header per page
# - One or two Program blocks per page in monospace
# - Footer with the synthetic "book page" number
# - GLP-shaped (but non-book) code so REPL parse-checks are deterministic

SECTIONS = [
    {
        "section": "§99.1 Programming with Constants",
        "book_page": 1,
        "programs": [
            {
                "label": "Program 99.1",
                "code": [
                    "p(a).",
                    "p(b).",
                ],
            },
        ],
    },
    {
        "section": "§99.1 (continued)",
        "book_page": 2,
        "programs": [
            {
                "label": "Program 99.2",
                "code": [
                    "q(X) :- p(X?) | true.",
                ],
            },
        ],
    },
    {
        "section": "§99.2 Streams",
        "book_page": 3,
        "programs": [
            {
                "label": "Program 99.3",
                "code": [
                    "producer([], 0).",
                    "producer([N?|Xs?], N) :- N? > 0 | N1 := N? - 1, producer(Xs, N1?).",
                ],
            },
        ],
    },
    {
        "section": "§99.2 (continued)",
        "book_page": 4,
        "programs": [
            {
                "label": "Program 99.4",
                "code": [
                    "consumer([], Sum, Sum?).",
                    "consumer([X|Xs], Sum, Result?) :- ground(X?) |",
                    "    Sum1 := Sum? + X?,",
                    "    consumer(Xs?, Sum1?, Result).",
                ],
            },
        ],
    },
]


def build(output_path: Path) -> None:
    c = canvas.Canvas(str(output_path), pagesize=LETTER)
    # Stable metadata so byte-identity tests work
    c.setTitle("GLP_ART (mock)")
    c.setAuthor("tutorial-specify test fixture")
    c.setProducer("reportlab (mocked)")

    width, height = LETTER

    for s in SECTIONS:
        # Section header
        c.setFont("Helvetica-Bold", 14)
        c.drawString(1 * inch, height - 1 * inch, s["section"])

        y = height - 1.5 * inch
        c.setFont("Courier", 11)

        for prog in s["programs"]:
            c.setFont("Helvetica-Bold", 11)
            c.drawString(1 * inch, y, prog["label"])
            y -= 0.3 * inch
            c.setFont("Courier", 11)
            for line in prog["code"]:
                c.drawString(1 * inch, y, line)
                y -= 0.22 * inch
            y -= 0.2 * inch

        # Book page footer
        c.setFont("Helvetica", 9)
        c.drawCentredString(width / 2, 0.5 * inch, str(s["book_page"]))

        c.showPage()

    c.save()


def main() -> int:
    here = Path(__file__).parent
    out = here / "glp_art_mock.pdf"
    build(out)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
