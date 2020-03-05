from http import HTTPStatus

from API.models import Wordform
from constants import ORTHOGRAPHY_NAME, ParadigmSize
from CreeDictionary.forms import WordSearchForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

# "pragma: no cover" works with coverage.
# It excludes the clause or line (could be a function/class/if else block) from coverage
# it should be used on every view function
# rationale: we don't unit test the views functions, rather, we test them in integration tests with cypress.


def lemma_details(request, lemma_text: str = None):  # pragma: no cover
    """
    lemma detail page. Fall back to search page if no lemma is found or multiple lemmas are found

    :param request: accepts query params `pos` `full_lc` `analysis` `id` to further specify query_string
    :param lemma_text: the exact form of the lemma (no spell relaxation)
    """
    extra_constraints = {
        k: v for k, v in request.GET.items() if k in {"pos", "lc", "analysis", "id"}
    }
    lemma = Wordform.objects.filter(text=lemma_text, is_lemma=True, **extra_constraints)
    if lemma.count() == 1:
        lemma = lemma.get()
        context = {
            "lemma_id": lemma.id,
            "lemma": lemma,
            "paradigm_size": ParadigmSize.BASIC.display_form,
            "paradigm_tables": lemma.paradigm if lemma else None,
        }
        return HttpResponse(render(request, "CreeDictionary/index.html", context))
    else:
        return redirect("cree-dictionary-index-with-query", query_string=lemma_text)


def index(request, query_string=None):  # pragma: no cover
    """
    homepage with optional initial search results to display

    :param request:
    :param query_string: optional initial search results to display
    :return:
    """

    context = {
        "word_search_form": WordSearchForm(),
        # when we have initial query word to search and display
        "query_string": query_string,
        "search_results": [
            search_result.serialize() for search_result in Wordform.search(query_string)
        ]
        if query_string
        else [],
    }
    return HttpResponse(render(request, "CreeDictionary/index.html", context))


def search_results(request, query_string: str):  # pragma: no cover
    """
    returns rendered boxes of search results according to user query
    """
    results = Wordform.search(query_string)
    return render(
        request,
        "CreeDictionary/word-entries.html",
        {"search_results": [r.serialize() for r in results]},
    )


def lemma_details_internal(request, lemma_id: int):  # pragma: no cover
    """
    render paradigm table for a lemma
    """
    lemma = Wordform.objects.get(id=lemma_id)
    return render(
        request,
        "CreeDictionary/paradigm.html",
        {
            "lemma": lemma,
            "paradigm_size": ParadigmSize.BASIC.display_form,
            "paradigm_tables": lemma.paradigm,
        },
    )


def about(request):  # pragma: no cover
    """
    About page.
    """
    return render(request, "CreeDictionary/about.html")


class ChangeOrthography(View):
    """
    Sets the orth= cookie, which affects the default rendered orthography.

        > POST /change-orthography HTTP/1.1
        > Cookie: orth=Latn
        >
        > orth=Cans

        < HTTP/1.1 204 No Content
        < Set-Cookie: orth=Cans

    Supports only POST requests for now.
    """

    AVAILABLE_ORTHOGRAPHIES = tuple(ORTHOGRAPHY_NAME.keys())

    def post(self, request):
        orth = request.POST.get("orth")

        # Tried to set to an unsupported orthography
        if orth not in self.AVAILABLE_ORTHOGRAPHIES:
            return HttpResponse(status=HTTPStatus.BAD_REQUEST)

        response = HttpResponse(status=HTTPStatus.NO_CONTENT)
        response.set_cookie("orth", orth)
        return response
