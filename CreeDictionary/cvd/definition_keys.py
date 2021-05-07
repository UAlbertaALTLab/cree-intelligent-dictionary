"""
We build definition vectors so that we can find relevant definitions, and then
later display the associated wordforms. Unfortunately we don’t currently have
any stable ID fields that we can use to refer to the wordform that the
definition came from. If we used the auto-generated wordform id pk, that would
become invalid whenever the dictionary was updated.

To deal with that, this file has functions to turn definitions into string keys that:
 1. Are unique per definition, so we can save multiple definitions per wordform
    into a KeyedVector
 2. Also refer unambiguously to a single wordform.
"""


import json
from typing import TypedDict, cast

from API.models import Definition, Wordform

CvdKey = str


class WordformQuery(TypedDict):
    text: str
    inflectional_category: str
    analysis: str
    stem: str


def definition_to_cvd_key(d: Definition) -> CvdKey:
    """Return a string that can be used for keying the given definition"""
    return cast(
        CvdKey,
        json.dumps(
            [
                # Unfortunately, with our current setup, we need to specify all four
                # of these for the result to be unique.
                d.wordform.text,
                d.wordform.inflectional_category,
                d.wordform.analysis,
                d.wordform.stem,
                # This is just a disambiguator so we can have multiple definitions
                # for the same word in a vector file without conflict.
                d.id,
            ],
            ensure_ascii=False,
        ),
    )


def cvd_key_to_wordform_query(s: CvdKey) -> WordformQuery:
    """Return kwargs for Wordform.objects.filter() to retrieve wordform

    While unambiguous, likely too slow for general use.
    """
    text, inflectional_category, analysis, stem, _ = json.loads(s)
    return {
        "text": text,
        "inflectional_category": inflectional_category,
        "analysis": analysis,
        "stem": stem,
    }


def wordform_query_matches(query: WordformQuery, wordform: Wordform):
    return (
        wordform.text == query["text"]
        and wordform.inflectional_category == query["inflectional_category"]
        and wordform.analysis == query["analysis"]
        and wordform.stem == query["stem"]
    )
