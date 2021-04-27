"""
Test parsing panes.
"""

from pathlib import Path

import pytest

from CreeDictionary.paradigm.panes import ParadigmTemplate


def test_parse_na_paradigm(na_layout_path: Path):
    """
    Parses the Plains Cree NA paradigm.

    This paradigm has three panes:
     - basic (no header)
     - diminutive (two rows: a header and one row of content)
     - possession

    With possession having the most columns.
    """
    with na_layout_path.open(encoding="UTF-8") as layout_file:
        na_paradigm_template = ParadigmTemplate.load(layout_file)

    assert count(na_paradigm_template.panes()) == 3
    basic_pane, diminutive_pane, possession_pane = na_paradigm_template.panes()

    assert basic_pane.header is None
    assert basic_pane.num_columns == 2
    assert diminutive_pane.num_columns == 2
    assert count(diminutive_pane.rows()) == 2
    assert possession_pane.header
    assert possession_pane.num_columns == 4


@pytest.fixture
def na_layout_path(shared_datadir: Path) -> Path:
    """
    Return the path to the NA layout in the test fixture dir.
    NOTE: this is **NOT** the NA paradigm used in production!
    """
    p = shared_datadir / "paradigm-layouts" / "NA.tsv"
    assert p.exists()
    return p


def count(it):
    """
    Returns the number of items iterated in the paradigm
    """
    return sum(1 for _ in it)