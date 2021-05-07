from API.search.affix import (
    do_source_language_affix_search,
    do_target_language_affix_search,
    query_would_return_too_many_results,
)
from API.search.core import SearchRun
from API.search.cvd_search import do_cvd_search
from API.search.lookup import fetch_results
from API.search.query import CvdSearchType
from API.search.util import first_non_none_value


def search(*, query: str, include_affixes=True, include_auto_definitions=False):
    """
    Perform an actual search, using the provided options.

    This class encapsulates the logic of which search methods to try, and in
    which order, to build up results in a SearchRun.
    """
    search_run = SearchRun(
        query=query, include_auto_definitions=include_auto_definitions
    )

    cvd_search_type = first_non_none_value(
        search_run.query.cvd, default=CvdSearchType.DEFAULT
    )

    if cvd_search_type == CvdSearchType.EXCLUSIVE:
        do_cvd_search(search_run)
        return search_run

    fetch_results(search_run)

    if include_affixes and not query_would_return_too_many_results(
        search_run.internal_query
    ):
        do_source_language_affix_search(search_run)
        do_target_language_affix_search(search_run)

    if cvd_search_type != CvdSearchType.OFF:
        do_cvd_search(search_run)

    return search_run
