from __future__ import annotations

import dataclasses
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import NewType, Iterable, Tuple, Optional

from typing_extensions import Protocol

from API.models import Wordform, wordform_cache
from API.schema import SerializedLinguisticTag
from CreeDictionary.relabelling import LABELS
from utils.types import FSTTag

Preverb = Wordform
Lemma = NewType("Lemma", Wordform)
MatchedEnglish = NewType("MatchedEnglish", str)
InternalForm = NewType("InternalForm", str)


class LinguisticTag(Protocol):
    """
    A linguistic feature/tag pair.
    """

    @property
    def value(self) -> FSTTag:
        ...

    # TODO: linguistic feature

    @property
    def in_plain_english(self) -> str:
        ...

    def serialize(self) -> SerializedLinguisticTag:
        return SerializedLinguisticTag(
            value=self.value,
            in_plain_english=self.in_plain_english,
        )


class SimpleLinguisticTag(LinguisticTag):
    """
    A linguistic feature/tag pair.
    """

    def __init__(self, value: FSTTag):
        self._value = value

    @property
    def value(self) -> FSTTag:
        return self._value

    @property
    def in_plain_english(self) -> str:
        return LABELS.english.get(self.value) or "???"


class CompoundLinguisticTag(LinguisticTag):
    def __init__(self, tags: Iterable[FSTTag]) -> None:
        self._fst_tags = tuple(tags)

    @property
    def value(self):
        return "".join(self._fst_tags)

    @property
    def in_plain_english(self):
        return LABELS.english.get_longest(self._fst_tags)


def linguistic_tag_from_fst_tags(tags: Tuple[FSTTag, ...]) -> LinguisticTag:
    """
    Returns the appropriate LinguisticTag, no matter how many tags you chuck at it!
    """
    assert len(tags) > 0
    if len(tags) == 1:
        return SimpleLinguisticTag(tags[0])
    else:
        return CompoundLinguisticTag(tags)


class Language(Enum):
    SOURCE = "Source"
    TARGET = "Target"


@dataclass
class Result:
    """
    A target-language wordform and the features that link it to a query.

    Features of a wordform allow better inferences about how good a result is.

    Some examples of these features could include:
      - Is this Result a match between a source-language query and wordform
        text, or between a target-language query term and a word in the
        definition text?
      - What is the edit distance between the query term and the wordform?
      - What is the best cosine vector distance between a definition of the
        result wordform and the query terms?

    The best search results will presumably have better scores on more features
    of greater importance.

    Search methods may generate candidate results that are ultimately not sent
    to users, so any user-friendly tagging/relabelling is instead done in
    PresentationResult class.
    """

    def __post_init__(self):
        if all(
            getattr(self, field.name) in (None, [])
            for field in dataclasses.fields(Result)
            if field.init and field.name != "wordform"
        ):
            raise Exception("No features were provided for why this is a result.")

        self.is_lemma = self.wordform.is_lemma
        self.lemma_wordform = self.wordform.lemma
        self.wordform_length = len(self.wordform.text)

        if self.did_match_source_language and self.query_wordform_edit_distance is None:
            raise Exception("must include edit distance on source language matches")

        self.morpheme_ranking = wordform_cache.MORPHEME_RANKINGS.get(
            self.wordform.text, None
        ) or wordform_cache.MORPHEME_RANKINGS.get(self.lemma_wordform.text, None)

    def add_features_from(self, other: Result):
        """Add the features from `other` into this object

        Good results can match for many different reasons. This method merges
        features from a different result object for the same wordform into the
        current object.
        """
        assert self.wordform.key == other.wordform.key

        for field_name, other_value in other.features().items():
            if other_value is not None:
                self_value = getattr(self, field_name)
                # combine lists, applying uniq
                if isinstance(self_value, list):
                    self_value[:] = list(set(self_value + other_value))
                elif (
                    field_name == "cosine_vector_distance"
                    and self.cosine_vector_distance is not None
                    # We already checked that other.cosine_vector_distance is
                    # not None, but mypy can’t infer that.
                    and other.cosine_vector_distance is not None
                ):
                    self.cosine_vector_distance = min(
                        self.cosine_vector_distance, other.cosine_vector_distance
                    )
                else:
                    setattr(self, field_name, other_value)

    wordform: Wordform
    lemma_wordform: Lemma = field(init=False)
    is_lemma: bool = field(init=False)
    wordform_length: int = field(init=False)

    #: What, if any, was the matching string?
    source_language_match: Optional[str] = None
    query_wordform_edit_distance: Optional[float] = None

    source_language_affix_match: Optional[bool] = None
    target_language_affix_match: Optional[bool] = None

    target_language_keyword_match: list[str] = field(default_factory=list)
    pronoun_as_is_match: Optional[bool] = None

    analyzable_inflection_match: Optional[bool] = None

    is_preverb_match: Optional[bool] = None

    is_cw_as_is_wordform: Optional[bool] = None

    #: Was anything in the query a target-language match for this result?
    did_match_target_language: Optional[bool] = None

    morpheme_ranking: Optional[float] = None

    cosine_vector_distance: Optional[float] = None

    def features(self):
        ret = {}
        for field in dataclasses.fields(Result):
            if field.name not in ["wordform", "lemma_wordform"]:
                value = getattr(self, field.name)
                if value is not None:
                    ret[field.name] = value
        return ret

    def features_json(self):
        return json.dumps(
            self.features(),
            ensure_ascii=False,
            indent=2,
        )

    #: Was anything in the query a source-language match for this result?
    @property
    def did_match_source_language(self) -> bool:
        return bool(
            self.source_language_match or self.source_language_affix_match is not None
        )

    def __str__(self):
        return f"Result<wordform={self.wordform}>"
