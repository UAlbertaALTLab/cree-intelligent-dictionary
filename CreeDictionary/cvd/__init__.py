import logging
import re
from functools import cache
from os import fspath

from gensim.models import KeyedVectors

from CreeDictionary import settings
from utils import shared_res_dir

logger = logging.getLogger(__name__)

shared_vector_model_dir = shared_res_dir / "vector_models"


def _load_vectors(path):
    return KeyedVectors.load(fspath(path), mmap="r")


@cache
def google_news_vectors():
    return _load_vectors(shared_vector_model_dir / "news_vectors.kv")


class DefinitionVectorsNotFoundException(Exception):
    pass


def definition_vectors_path():
    filename = "definitions.kv"
    if settings.USE_TEST_DB:
        filename = "test_db_definitions.kv"
    return shared_vector_model_dir / filename


@cache
def definition_vectors():
    try:
        return _load_vectors(definition_vectors_path())

    except FileNotFoundError:
        raise DefinitionVectorsNotFoundException


# Implementation from https://stackoverflow.com/a/48027864/14558 which cites
# https://www.peterbe.com/plog/fastest-way-to-uniquify-a-list-in-python-3.6
# which cites a tweet of Raymond Hettinger
def uniq(l: list) -> list:
    """Return unique elements from l"""
    return list(dict.fromkeys(l))


def vector_for_keys(keyed_vectors, keys: list[str]):
    """Return the sum of vectors in keyed_vectors for the given keys"""
    if not keys:
        raise ValueError("keys cannot be empty")

    return keyed_vectors[keys].sum(axis=0)


RE_PUNCTUATION = re.compile(r'[!,.\[\]\(\)\{\};:"/\?]+')


def extract_keyed_words(query: str, keys, already_warned=None):
    """Split query into a list of words that occur in keys

    already_warned is an optional set, used to reduce debug log verbosity
    """
    ret = []

    query = query.lower()
    query = RE_PUNCTUATION.sub(" ", query)
    # ‘ice-cream’ is coded in the news vectors as ‘ice_cream’
    query = query.replace("-", "_")
    query = query.strip()

    for word in query.split():
        if word in keys:
            ret.append(word)
        elif word.endswith("'s") and word[:-2] in keys:
            ret.append(word[:-2])
        elif "_" in word:
            # if ‘ice_cream’ not found, try ‘ice’ and ‘cream’
            for piece in word.split("_"):
                if piece in keys:
                    ret.append(piece)
                else:
                    _warn(piece, f"not found: {word!r} piece {piece!r}", already_warned)
        else:
            _warn(word, f"not found: {word!r}", already_warned)

    return uniq(ret)


def _warn(word, msg, already_warned):
    if (
        logger.isEnabledFor(logging.DEBUG)
        and already_warned is not None
        and word not in already_warned
    ):
        already_warned.add(word)
        logger.debug(msg)
