"""
Test parsing panes.
"""

from pathlib import Path

import pytest
from more_itertools import first
from more_itertools import ilen as count

from CreeDictionary.paradigm.panes import (
    ColumnLabel,
    ContentRow,
    EmptyCell,
    HeaderRow,
    InflectionTemplate,
    MissingForm,
    Pane,
    ParadigmIsNotStaticError,
    ParadigmLayout,
    RowLabel,
    WordformCell,
)


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
        na_paradigm_template = ParadigmLayout.load(layout_file)

    assert count(na_paradigm_template.panes) == 3
    basic_pane, diminutive_pane, possession_pane = na_paradigm_template.panes

    assert basic_pane.header is None
    assert basic_pane.num_columns == 2
    assert diminutive_pane.num_columns == 2
    assert count(diminutive_pane.rows) == 2
    assert possession_pane.header
    assert possession_pane.num_columns == 4

    assert na_paradigm_template.max_num_columns == 4


def test_parse_demonstrative_pronoun_paradigm(pronoun_paradigm_path: Path):
    """
    Test that the static layout for demonstrative pronouns can be parsed.
    Note: the fixture was (sloppily) written by me, Eddie, and it is probably not
    representative of the actual demonstrative pronoun paradigm we'll have on the
    production site... buuuuuuuuut, it's useful as a test fixture!
    """
    with pronoun_paradigm_path.open(encoding="UTF-8") as layout_file:
        pronoun_paradigm_layout = ParadigmLayout.load(layout_file)

    pronoun_paradigm = pronoun_paradigm_layout.as_static_paradigm()

    assert count(pronoun_paradigm.panes) == 1

    basic_pane = first(pronoun_paradigm.panes)
    assert basic_pane.num_columns == 3
    assert count(basic_pane.rows) == 4


def test_as_static_paradigm_raises_on_dynamic_paradigm():
    dynamic_layout = ParadigmLayout.loads("_ Prox\t${lemma}+Pron+I+Prox+Sg\n")
    static_layout = ParadigmLayout.loads("_ Prox\tôma\n")

    assert static_layout.as_static_paradigm()

    with pytest.raises(ParadigmIsNotStaticError):
        dynamic_layout.as_static_paradigm()


def test_dump_equal_to_file_on_disk(na_layout_path: Path):
    """
    Dumping the file should yield the same file, modulo a trailing newline.
    """
    text = na_layout_path.read_text(encoding="UTF-8").rstrip("\n")
    paradigm = ParadigmLayout.loads(text)
    assert paradigm.dumps() == text


@pytest.mark.parametrize("cls", [EmptyCell, MissingForm])
def test_singleton_classes(cls):
    """
    A few classes should act like singletons.
    """
    assert cls() is cls()
    assert cls() == cls()


def test_wordform_cell():
    """
    WordformCell should not act like an InflectionTemplate.
    """
    wordform = "ôma"
    cell = WordformCell(wordform)

    assert cell.contains_wordform(wordform)

    # Trying to fill a cell returns the same cell back:
    assert cell == cell.fill_one({})


def sample_pane():
    return Pane(
        [
            HeaderRow(("Der/Dim",)),
            ContentRow([EmptyCell(), ColumnLabel(["Sg"]), ColumnLabel(["Obv"])]),
            ContentRow(
                [RowLabel("1Sg"), MissingForm(), InflectionTemplate("${lemma}+")]
            ),
        ]
    )


@pytest.mark.parametrize(
    "component",
    [
        EmptyCell(),
        MissingForm(),
        InflectionTemplate("${lemma}+N+A+Sg"),
        WordformCell("ôma"),
        ColumnLabel(("Sg",)),
        RowLabel(("1Sg",)),
        HeaderRow(("Imp",)),
        ContentRow([EmptyCell(), ColumnLabel(["Sg"]), ColumnLabel(["Pl"])]),
        ContentRow([RowLabel("1Sg"), MissingForm(), InflectionTemplate("${lemma}+Pl")]),
        sample_pane(),
    ],
)
def test_str_produces_parsable_result(component):
    """
    Parsing the stringified component should result in an equal component.
    """
    stringified = str(component)
    parsed = type(component).parse(stringified)
    assert component == parsed
    assert stringified == str(parsed)


def test_produces_fst_analysis_string(na_layout: ParadigmLayout):
    """
    It should produce a valid FST analysis string.
    """

    lemma = "minôs"
    expected_lines = {
        # Basic
        f"{lemma}+N+A+Sg",
        f"{lemma}+N+A+Pl",
        f"{lemma}+N+A+Obv",
        f"{lemma}+N+A+Loc",
        f"{lemma}+N+A+Distr",
        # Diminutive
        f"{lemma}+N+A+Der/Dim+N+A+Sg",
        # Possession
        f"{lemma}+N+A+Px1Sg+Sg",
        f"{lemma}+N+A+Px1Sg+Pl",
        f"{lemma}+N+A+Px1Sg+Obv",
        f"{lemma}+N+A+Px2Sg+Sg",
        f"{lemma}+N+A+Px2Sg+Pl",
        f"{lemma}+N+A+Px2Sg+Obv",
        f"{lemma}+N+A+Px3Sg+Obv",
        f"{lemma}+N+A+Px1Pl+Sg",
        f"{lemma}+N+A+Px1Pl+Pl",
        f"{lemma}+N+A+Px1Pl+Obv",
        f"{lemma}+N+A+Px12Pl+Sg",
        f"{lemma}+N+A+Px12Pl+Pl",
        f"{lemma}+N+A+Px12Pl+Obv",
        f"{lemma}+N+A+Px2Pl+Sg",
        f"{lemma}+N+A+Px2Pl+Pl",
        f"{lemma}+N+A+Px2Pl+Obv",
        f"{lemma}+N+A+Px3Pl+Obv",
        f"{lemma}+N+A+Px4Sg/Pl+Obv",
    }
    raw_analyses = na_layout.generate_fst_analysis_string(lemma)
    generated_analyses = raw_analyses.splitlines(keepends=False)
    assert len(expected_lines) == len(generated_analyses)
    assert expected_lines == set(generated_analyses)


@pytest.fixture
def na_layout_path(shared_datadir: Path) -> Path:
    """
    Return the path to the NA layout in the test fixture dir.
    NOTE: this is **NOT** the NA paradigm used in production!
    """
    p = shared_datadir / "paradigm-layouts" / "dynamic" / "NA.tsv"
    assert p.exists()
    return p


@pytest.fixture
def na_layout(na_layout_path: Path) -> ParadigmLayout:
    """
    Returns the parsed NA layout.
    """
    with na_layout_path.open(encoding="UTF-8") as layout_file:
        return ParadigmLayout.load(layout_file)


@pytest.fixture
def pronoun_paradigm_path(shared_datadir: Path) -> Path:
    """
    Return the path to the NA layout in the test fixture dir.
    NOTE: this is **NOT** the NA paradigm used in production!
    """
    p = shared_datadir / "paradigm-layouts" / "static" / "demonstrative-pronouns.tsv"
    assert p.exists()
    return p
