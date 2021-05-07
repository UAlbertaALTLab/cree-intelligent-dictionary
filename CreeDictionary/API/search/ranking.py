from __future__ import annotations

from functools import cmp_to_key, partial
from typing import Callable, Any, cast

from utils import get_modified_distance
from . import core
from .query import CvdSearchType
from .types import Result
from ..models import wordform_cache


def sort_search_result(
    res_a: Result,
    res_b: Result,
    search_run: core.SearchRun,
) -> float:
    """
    determine how we sort search results.

    :return:   0: does not matter;
              >0: res_a should appear after res_b;
              <0: res_a should appear before res_b.
    """

    if res_a.did_match_source_language and res_b.did_match_source_language:
        # both from source
        a_dis = get_modified_distance(search_run.internal_query, res_a.wordform.text)
        b_dis = get_modified_distance(search_run.internal_query, res_b.wordform.text)
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
    elif res_a.did_match_source_language:
        # a from source, b from target
        return -1
    elif res_b.did_match_target_language:
        # a from target, b from source
        return 1
    else:
        # both from English
        if (
            search_run.query.cvd == CvdSearchType.EXCLUSIVE
            and res_a.cosine_vector_distance is not None
            and res_b.cosine_vector_distance is not None
        ):
            return res_a.cosine_vector_distance - res_b.cosine_vector_distance

        a_in_rankings = res_a.wordform.text in wordform_cache.MORPHEME_RANKINGS
        b_in_rankings = res_b.wordform.text in wordform_cache.MORPHEME_RANKINGS

        if a_in_rankings and not b_in_rankings:
            return -1
        elif not a_in_rankings and b_in_rankings:
            return 1
        elif not a_in_rankings and not b_in_rankings:
            return 0
        else:  # both in rankings
            return (
                wordform_cache.MORPHEME_RANKINGS[res_a.wordform.text]
                - wordform_cache.MORPHEME_RANKINGS[res_b.wordform.text]
            )


def sort_by_user_query(search_run: core.SearchRun) -> Callable[[Any], Any]:
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
            partial(sort_search_result, search_run=search_run),
        )
    )
