"""PDF text + code-block extraction (FR-002, FR-003).

Implements Decision 1 (pdfplumber) and Decision 5 (book↔PDF page mapping).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from tutorial_specify.errors import PdfMissingError


@dataclass
class PdfPage:
    pdf_page: int  # 1-indexed
    book_page: int | None
    text: str
    monospace_lines: list[str]  # subset of text lines rendered in a monospace font


@dataclass
class CodeBlock:
    """A contiguous monospace text region from one or more PDF pages."""

    block_id: str
    book_pages: tuple[int, ...]
    pdf_pages: tuple[int, ...]
    text: str
    program_id: str | None = None  # e.g. "Program 1.1" if labelled in the book


# Heuristic: page footer is a short line of digits (no letters).
_BOOK_PAGE_FOOTER_RE = re.compile(r"^\s*([0-9]+)\s*$")
_PROGRAM_LABEL_RE = re.compile(r"^\s*(Program\s+[0-9]+(?:\.[0-9]+)?)\s*$")


def open_pdf(path: Path):
    """Open a PDF via pdfplumber. Lazy-import so the package install is the only dep gate."""
    if not path.exists():
        raise PdfMissingError(f"GLP_ART.pdf not found at {path}")
    try:
        import pdfplumber
    except ImportError as exc:
        raise PdfMissingError(
            "pdfplumber is not installed; run `pip install -e .` from "
            "scripts/tutorial_specify/"
        ) from exc
    return pdfplumber.open(str(path))


def extract_pages(pdf_path: Path) -> list[PdfPage]:
    """Extract every page's text + book-page footer + monospace lines."""
    pages: list[PdfPage] = []
    with open_pdf(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            mono = _extract_monospace_lines(page)
            book_page = _detect_book_page(text)
            pages.append(
                PdfPage(pdf_page=i, book_page=book_page, text=text, monospace_lines=mono)
            )
    return pages


def _detect_book_page(text: str) -> int | None:
    """The book footer is typically the last short numeric line on the page."""
    candidates: list[int] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        m = _BOOK_PAGE_FOOTER_RE.match(line)
        if m:
            candidates.append(int(m.group(1)))
    return candidates[-1] if candidates else None


def _extract_monospace_lines(page) -> list[str]:
    """Return the text lines rendered in a monospace font (Courier-family).

    pdfplumber exposes per-character font metadata; we group by line and tag a
    line as monospace if any of its characters use a Courier-derived font.
    """
    chars = page.chars or []
    if not chars:
        return []
    by_line: dict[int, list[dict]] = {}
    for ch in chars:
        # Round y0 to nearest unit to bin into lines
        line_key = int(round(ch.get("top", 0)))
        by_line.setdefault(line_key, []).append(ch)

    out: list[str] = []
    for key in sorted(by_line):
        line_chars = by_line[key]
        is_mono = any(_is_monospace(c.get("fontname", "")) for c in line_chars)
        if is_mono:
            text = "".join(c.get("text", "") for c in line_chars)
            out.append(text.rstrip())
    return out


def _is_monospace(fontname: str) -> bool:
    name = (fontname or "").lower()
    return "courier" in name or "mono" in name or "ttype" in name or "tttf" in name


def build_book_page_map(pages: list[PdfPage]) -> dict[int, int]:
    """Map book page number -> PDF page number (FR-003 / Decision 5)."""
    out: dict[int, int] = {}
    for p in pages:
        if p.book_page is not None and p.book_page not in out:
            out[p.book_page] = p.pdf_page
    return out


def find_pdf_page_for_book_page(book_to_pdf: dict[int, int], book_page: int) -> int | None:
    return book_to_pdf.get(book_page)


def collect_code_blocks(
    pages: list[PdfPage], chapter_id: str, book_page_range: tuple[int, int] | None = None
) -> list[CodeBlock]:
    """Collect contiguous monospace lines as code blocks across the given page range.

    Args:
        pages: all pages from `extract_pages`.
        chapter_id: e.g. "ch04"; used to construct stable block_ids.
        book_page_range: inclusive (low, high) book-page range; None = all pages.
    """
    blocks: list[CodeBlock] = []
    current_lines: list[str] = []
    current_pdf_pages: list[int] = []
    current_book_pages: list[int] = []
    current_program: str | None = None
    block_counter = 0

    def flush():
        nonlocal current_lines, current_pdf_pages, current_book_pages
        nonlocal current_program, block_counter
        if not current_lines:
            return
        block_counter += 1
        bp_str = (
            f"pp{current_book_pages[0]}-{current_book_pages[-1]}"
            if current_book_pages and current_book_pages[0] != current_book_pages[-1]
            else f"p{current_book_pages[0]}" if current_book_pages else "pUNK"
        )
        bid = f"{chapter_id}-{bp_str}-block-{block_counter:02d}"
        blocks.append(
            CodeBlock(
                block_id=bid,
                book_pages=tuple(sorted(set(current_book_pages))),
                pdf_pages=tuple(sorted(set(current_pdf_pages))),
                text="\n".join(current_lines),
                program_id=current_program,
            )
        )
        current_lines = []
        current_pdf_pages = []
        current_book_pages = []
        current_program = None

    for page in pages:
        if book_page_range is not None and page.book_page is not None:
            lo, hi = book_page_range
            if not (lo <= page.book_page <= hi):
                if current_lines:
                    flush()
                continue

        # Walk through the full text (not just monospace) so we can pick up
        # `Program N.N` headers that precede a code block.
        text_lines = page.text.splitlines() if page.text else []
        mono_set = set(page.monospace_lines)

        for line in text_lines:
            stripped = line.strip()
            mp = _PROGRAM_LABEL_RE.match(stripped)
            if mp:
                if current_lines:
                    flush()
                current_program = mp.group(1)
                continue
            if line in mono_set or stripped in {ln.strip() for ln in mono_set}:
                current_lines.append(line.rstrip())
                if page.book_page is not None:
                    current_book_pages.append(page.book_page)
                current_pdf_pages.append(page.pdf_page)
            else:
                if current_lines:
                    flush()
    flush()
    return blocks


def format_book_pages_citation(book_pages: tuple[int, ...], section_id: str | None,
                                program_id: str | None) -> str:
    """Render canonical citation per FR-003: `book pp X–Y §A.B[, Program N.N]`."""
    if not book_pages:
        if section_id and program_id:
            return f"§{section_id}, {program_id}"
        return section_id or program_id or "(uncited)"

    if len(book_pages) == 1:
        page_part = f"book p {book_pages[0]}"
    else:
        page_part = f"book pp {book_pages[0]}–{book_pages[-1]}"

    parts = [page_part]
    if section_id:
        parts.append(f"§{section_id}")
    out = " ".join(parts)
    if program_id:
        out += f", {program_id}"
    return out
