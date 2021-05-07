from pathlib import Path

import pytest
from more_itertools import first, ilen

from CreeDictionary.paradigm.manager import ParadigmManager


def test_generates_personal_pronoun_paradigm(paradigm_manager) -> None:
    paradigm = paradigm_manager.static_paradigm_for("personal-pronouns")
    assert paradigm is not None

    # I don't know how many panes there will be, but the first should DEFINITELY have
    # the singular personal pronouns that folks learn in basic nêhiyawêwin class.
    assert ilen(paradigm.panes) >= 1
    pane = first(paradigm.panes)
    assert pane.contains_wordform("niya")
    assert pane.contains_wordform("kiya")
    assert pane.contains_wordform("wiya")

    # The rest of the paradigm should contain the remaining pronouns
    assert paradigm.contains_wordform("niyanân")
    assert paradigm.contains_wordform("kiyânaw")
    assert paradigm.contains_wordform("kiyawâw")
    assert paradigm.contains_wordform("wiyawâw")


@pytest.fixture
def paradigm_manager(shared_datadir: Path) -> ParadigmManager:
    from shared import expensive

    layout_dir = shared_datadir / "paradigm-layouts"
    assert layout_dir.is_dir()
    assert (layout_dir / "static").is_dir()
    assert (layout_dir / "dynamic").is_dir()
    return ParadigmManager(layout_dir, expensive.strict_generator)
