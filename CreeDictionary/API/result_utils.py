import typing
from functools import cmp_to_key, partial
from typing import List, Callable, Any, cast

from utils import Language, get_modified_distance

from utils.fst_analysis_parser import LABELS, partition_analysis
from utils.types import FSTTag, Label, ConcatAnalysis

if typing.TYPE_CHECKING:
    from API.search import SearchResult


def replace_user_friendly_tags(fst_tags: List[FSTTag]) -> List[Label]:
    """ replace fst-tags to cute ones"""
    return LABELS.english.get_full_relabelling(fst_tags)


def safe_partition_analysis(analysis: ConcatAnalysis):
    try:
        (linguistic_breakdown_head, _, linguistic_breakdown_tail,) = partition_analysis(
            analysis
        )
    except ValueError:
        linguistic_breakdown_head = []
        linguistic_breakdown_tail = []
    return linguistic_breakdown_head, linguistic_breakdown_tail


def sort_search_result(
    res_a: "SearchResult", res_b: "SearchResult", user_query: str
) -> float:
    """
    determine how we sort search results.

    :return:   0: does not matter;
              >0: res_a should appear after res_b;
              <0: res_a should appear before res_b.
    """

    if res_a.matched_by is Language.CREE and res_b.matched_by is Language.CREE:
        # both from cree
        a_dis = get_modified_distance(user_query, res_a.matched_cree)
        b_dis = get_modified_distance(user_query, res_b.matched_cree)
        difference = a_dis - b_dis
        if difference:
            return difference

        # Both results are EXACTLY the same form!
        # Further disambiguate by checking if one is the lemma.
        if res_a.is_lemma and res_b.is_lemma:
            return 0
        elif res_a.is_lemma:
            return -1
        elif res_b.is_lemma:
            return 1
        else:
            # Somehow, both forms exactly match the user query and neither
            # is a lemma?
            return 0

    # todo: better English sort
    elif res_a.matched_by is Language.CREE:
        # a from cree, b from English
        return -1
    elif res_b.matched_by is Language.CREE:
        # a from English, b from Cree
        return 1
    else:
        from .models import Wordform

        # both from English
        a_in_rankings = res_a.matched_cree in Wordform.MORPHEME_RANKINGS
        b_in_rankings = res_b.matched_cree in Wordform.MORPHEME_RANKINGS

        if a_in_rankings and not b_in_rankings:
            return -1
        elif not a_in_rankings and b_in_rankings:
            return 1
        elif not a_in_rankings and not b_in_rankings:
            return 0
        else:  # both in rankings
            return (
                Wordform.MORPHEME_RANKINGS[res_a.matched_cree]
                - Wordform.MORPHEME_RANKINGS[res_b.matched_cree]
            )


def sort_by_user_query(user_query: str) -> Callable[[Any], Any]:
    """
    Returns a key function that sorts search results ranked by their distance
    to the user query.
    """
    # mypy doesn't really know how to handle partial(), so we tell it the
    # correct type with cast()
    # See: https://github.com/python/mypy/issues/1484
    return cmp_to_key(
        cast(
            Callable[[Any, Any], Any],
            partial(sort_search_result, user_query=user_query),
        )
    )
