import re
from typing import Optional, Tuple
from constants import InflectionCategory

from os.path import dirname
from pathlib import Path
from typing import Iterable, Dict, Optional, Set, Pattern
from constants import InflectionCategory
import re

inflection_category_to_pattern = dict()  # type: Dict[InflectionCategory, Pattern[str]]

with open(Path(dirname(__file__)) / ".." / "res" / "lemma-tags.tsv") as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        if line:
            cells = line.split("\t")
            category = InflectionCategory(cells[0].upper())

            # IPC and Pron are special cases
            if (
                category is not InflectionCategory.IPC
                and category is not InflectionCategory.Pron
            ):
                inflection_category_to_pattern[category] = re.compile(
                    "[^+]+" + re.escape(cells[1].split("{{ lemma }}")[-1])
                )


# layout_class = re.match("(nad?|nid?|vai|vii|vt[ai]|ipc)", layout_name).groups()[0]


analysis_pattern = re.compile(
    r"(?P<category>\+N\+A(\+D)?|\+N\+I(\+D)?|\+V\+AI|\+V\+T[AI]|\+V\+II|(\+Num)?\+Ipc|\+Pron).*?$"
)


def extract_lemma(analysis: str) -> Optional[str]:
    res = re.search(analysis_pattern, analysis)
    if res is not None:

        group = res.group("category")
        if group:
            end = res.span("category")[0]
            # print(res.groups())
            cursor = end - 1

            while cursor > 0 and analysis[cursor] != "+":
                cursor -= 1
            if analysis[cursor] == "+":
                cursor += 1
            # print(cursor, end)
            return analysis[cursor:end]
        else:
            return None
    else:
        return None


def extract_lemma_and_category(
    analysis: str
) -> Optional[Tuple[str, InflectionCategory]]:
    """
    faster than calling `extract_lemma` and `extract_category` separately
    """
    res = re.search(analysis_pattern, analysis)
    if res is not None:

        group = res.group("category")
        if group:
            end = res.span("category")[0]
            # print(res.groups())
            cursor = end - 1

            while cursor > 0 and analysis[cursor] != "+":
                cursor -= 1
            if analysis[cursor] == "+":
                cursor += 1

            lemma = analysis[cursor:end]

            if group.startswith("+Num"):  # special case
                group = group[4:]
            inflection_category = InflectionCategory(group.replace("+", "").upper())

            return lemma, inflection_category

        else:
            return None
    else:
        return None


def extract_category(analysis: str) -> Optional[InflectionCategory]:
    """

    :param analysis: in the form of 'a+VAI+b+c'
    """
    res = re.search(analysis_pattern, analysis)
    if res is not None:
        group = res.group("category")

        if group:
            if group.startswith("+Num"):  # special case
                group = group[4:]
            return InflectionCategory(group.replace("+", "").upper())
        else:
            return None
    else:
        return None


def identify_lemma_analysis(analyses: Iterable[str]) -> Set[str]:
    """
    An example:

    for cree wâpi-maskwa, hfstol gives the below analyses:

    ['wâpi-maskwa+N+A+Obv', 'wâpi-maskwa+N+A+Sg']

    both inflections look the same as the lemma, but which is the preference for a lemma?
    this function returns the preferred lemma analyses according to res/lemma-tags.tsv
    """
    possible_analyses = set()

    for analysis in analyses:
        cat = extract_category(analysis)

        if cat is InflectionCategory.Pron:
            if "+Pron" in analysis:
                possible_analyses.add(analysis)
        elif cat is InflectionCategory.IPC:

            if "+Ipc" in analysis and not analysis.endswith("+Num+Ipc"):
                possible_analyses.add(analysis)
        else:
            pattern = inflection_category_to_pattern[cat]
            if re.fullmatch(pattern, analysis):

                possible_analyses.add(analysis)

    return possible_analyses
