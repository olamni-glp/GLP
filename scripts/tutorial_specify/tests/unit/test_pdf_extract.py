"""Unit tests for tutorial_specify.pdf_extract (T011)."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from tutorial_specify.pdf_extract import (
    build_book_page_map,
    collect_code_blocks,
    extract_pages,
    format_book_pages_citation,
)


@pytest.fixture
def mock_pdf(fixtures_dir, tmp_path):
    """Build the synthetic mock PDF if reportlab is available; else skip."""
    pytest.importorskip("reportlab")
    pytest.importorskip("pdfplumber")
    target = fixtures_dir / "glp_art_mock.pdf"
    if not target.exists():
        # Build via the fixture script
        import sys
        sys.path.insert(0, str(fixtures_dir))
        try:
            import build_mock_pdf  # type: ignore
            build_mock_pdf.build(target)
        finally:
            sys.path.pop(0)
    return target


def test_extract_pages_yields_pages(mock_pdf):
    pages = extract_pages(mock_pdf)
    assert len(pages) >= 4
    assert all(p.text for p in pages)


def test_book_page_map_is_built(mock_pdf):
    pages = extract_pages(mock_pdf)
    book_map = build_book_page_map(pages)
    # The mock has book pages 1..4 mapped 1:1 to PDF pages 1..4
    assert book_map.get(1) == 1
    assert book_map.get(4) == 4


def test_collect_code_blocks_finds_programs(mock_pdf):
    pages = extract_pages(mock_pdf)
    blocks = collect_code_blocks(pages, chapter_id="ch99")
    assert len(blocks) >= 1
    # At least one block should be tagged with a Program identifier
    assert any(b.program_id and b.program_id.startswith("Program") for b in blocks)
    # block_id format: ch99-...-block-NN
    assert all(b.block_id.startswith("ch99-") for b in blocks)


def test_format_book_pages_citation_canonical():
    assert format_book_pages_citation((37, 38, 39, 40), "4.3", "Program 1.1") == \
        "book pp 37–40 §4.3, Program 1.1"
    assert format_book_pages_citation((37,), "4.3", None) == "book p 37 §4.3"
    assert format_book_pages_citation((), "6.5", None) == "§6.5"


def test_format_no_pdf_pages_in_citation():
    out = format_book_pages_citation((37, 40), "4.3", "Program 1.1")
    # FR-003: PDF page numbers MUST NOT appear
    assert "PDF" not in out
