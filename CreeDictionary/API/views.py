from typing import List

from API.schema import SerializedSearchResult
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from .models import Wordform


def click_in_text(request) -> HttpResponse:
    """
    click-in-text api
    see SerializedSearchResult in schema.py for API specifications
    """

    q = request.GET.get("q")
    if q is None:
        return HttpResponseBadRequest("query param q missing")
    elif q == "":
        return HttpResponseBadRequest("query param q is an empty string")

    results: List[SerializedSearchResult] = []
    for result in Wordform.simple_search(q, include_auto_definitions=False):
        results.append(result.serialize(include_auto_definitions=False))

    response = {"results": results}

    json_response = JsonResponse(response)
    json_response["Access-Control-Allow-Origin"] = "*"
    return json_response
