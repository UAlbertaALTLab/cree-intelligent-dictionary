import time
import unicodedata
from typing import List, Optional, Set, Dict
from urllib.parse import unquote

from cree_sro_syllabics import syllabics2sro
from django.db import models, connection, transaction

# todo: override save() to automatically increase id (so that people can add words on django admin)
# see: https://docs.djangoproject.com/en/2.2/topics/db/models/#overriding-predefined-model-methods
from django.db.models import QuerySet, Max
from django.forms import model_to_dict

from constants import LexicalCategory, LC
from fuzzy_search import CreeFuzzySearcher
from shared import descriptive_analyzer
from utils import hfstol_analysis_parser


class Inflection(models.Model):
    _cree_fuzzy_searcher = None

    @classmethod
    def init_fuzzy_searcher(cls):
        if cls._cree_fuzzy_searcher is None:
            cls._cree_fuzzy_searcher = CreeFuzzySearcher(cls.objects.all())

    @classmethod
    def fuzzy_search(cls, query: str, distance: int) -> QuerySet:
        if cls._cree_fuzzy_searcher is None:
            return Inflection.objects.none()
        return cls._cree_fuzzy_searcher.search(query, distance)

    # override pk to allow use of bulk_create
    # auto-increment is also implemented in the overridden save below
    id = models.PositiveIntegerField(primary_key=True)

    text = models.CharField(max_length=40)

    RECOGNIZABLE_LC = [(lc.value,) * 2 for lc in LexicalCategory] + [("", "")]
    lc = models.CharField(max_length=4, choices=RECOGNIZABLE_LC)
    RECOGNIZABLE_POS = ((p,) * 2 for p in ("IPV", "PRON", "N", "IPC", "V", ""))
    pos = models.CharField(max_length=4, choices=RECOGNIZABLE_POS)

    analysis = models.CharField(
        max_length=50,
        default="",
        help_text="fst analysis or the best possible if the source is not analyzable",
    )
    is_lemma = models.BooleanField(
        default=False, help_text="Lemma or non-lemma inflection"
    )
    as_is = models.BooleanField(
        default=False,
        help_text="Fst can not determine the lemma. Paradigm table will not be shown to the user for this entry",
    )

    default_spelling = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="alt_spellings"
    )

    lemma = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="inflections"
    )

    class Meta:
        # analysis is for faster user query (in function fetch_lemmas_by_user_query below)
        # text is for faster fuzzy search initialization when the app restarts on the server side (order_by text)
        indexes = [models.Index(fields=["analysis"]), models.Index(fields=["text"])]

    def __str__(self):
        return self.text

    def is_non_default_spelling(self) -> bool:
        return self.default_spelling != self

    def get_presentational_pos(self):
        """

        :return: a pos that is shown to users. like Noun, Verb, etc
        """
        if self.as_is:  # then self.analysis is just created from lc and pos
            if self.lc != "":

                lc = LC(self.lc)

                if lc.is_noun():
                    return "Noun"
                elif lc.is_verb():
                    return "Verb"
                elif lc is LC.IPC:
                    return "Ipc"
                elif lc is LC.Pron:
                    return "Pronoun"
                else:
                    raise NotImplementedError

            else:
                if self.pos == "N":
                    return "Noun"
                elif self.pos == "V":
                    return "Verb"
                elif self.pos == "IPC":
                    return "Ipc"
                elif self.pos == "PRON":
                    return "Pronoun"
                elif self.pos == "IPV":
                    return "Ipv"
                else:
                    raise ValueError(f"can not representational pos for {self}")
        else:
            return hfstol_analysis_parser.extract_category(self.analysis)

    def is_category(self, lc: LexicalCategory) -> Optional[bool]:
        """
        :return: None if self.as_is is true. Meaning the analysis is simply the lc and the pos from the xml

        :raise ValueError: the lexical category of the lemma can not be recognized
        """
        if self.as_is:  # meaning the analysis is simply the lc and the pos from the xml
            return None
        category = hfstol_analysis_parser.extract_category(self.analysis)
        if category is None:
            raise ValueError(
                "The lexical category of the inflection %s can not be recognized. (A malformed analysis field?)"
                % self
            )
        return category is lc

    @transaction.atomic
    def save(self, *args, **kwargs):
        """
        ensures id is auto-incrementing. infer foreign key 'lemma' to be self if self.is_lemma is set to True.
         Default foreign key "default spelling" to self.
        """
        max_id = Inflection.objects.aggregate(Max("id"))
        if max_id["id__max"] is None:
            self.id = 0
        else:
            self.id = max_id["id__max"] + 1

        # infer foreign keys default spelling and lemma if they are not set.
        # this helps with adding entries in django admin as the ui for
        # foreign keys default spelling and lemma takes forever to
        # load.
        # Also helps with tests as it's now easier to create entries
        if self.default_spelling_id is None:
            self.default_spelling_id = self.id

        if self.is_lemma:
            self.lemma_id = self.id

        super(Inflection, self).save(*args, **kwargs)

    @classmethod
    def fetch_lemmas_by_user_query(cls, user_query: str) -> QuerySet:
        """

        :param user_query: can be English or Cree (syllabics or not)
        :return: can be empty
        """
        # todo: test after searching strategy is fixed

        # URL Decode
        user_query = unquote(user_query)
        # Normalize to UTF8 NFC
        user_query = unicodedata.normalize("NFC", user_query)
        user_query = (
            user_query.replace("ā", "â")
            .replace("ē", "ê")
            .replace("ī", "î")
            .replace("ō", "ô")
        )
        user_query = syllabics2sro(user_query)

        user_query = user_query.lower()

        # build up result_lemmas in 3 ways
        # 1. spell relax in descriptive fst
        # 2. fuzzy search
        #
        # 3. definition containment of the query word
        result_lemmas = Inflection.objects.none()

        # utilize the spell relax in descriptive_analyzer
        fst_analyses: Set[str] = descriptive_analyzer.feed_in_bulk_fast([user_query])[
            user_query
        ]
        lemma_ids = Inflection.objects.filter(analysis__in=fst_analyses).values(
            "lemma__id"
        )

        result_lemmas |= Inflection.objects.filter(id__in=lemma_ids)
        if len(user_query) > 1:
            # fuzzy search does not make sense for a single letter, it will just give every single letter word
            lemma_ids = Inflection.fuzzy_search(user_query, 0).values("lemma__id")
            result_lemmas |= Inflection.objects.filter(id__in=lemma_ids)

        # todo: remind user "are you searching in cree/english?"
        if " " not in user_query:  # a whole word

            lemma_ids = EnglishKeyword.objects.filter(text__iexact=user_query).values(
                "lemma__id"
            )
            result_lemmas |= Inflection.objects.filter(id__in=lemma_ids)

        return result_lemmas


class Definition(models.Model):
    # override pk to allow use of bulk_create
    id = models.PositiveIntegerField(primary_key=True)

    text = models.CharField(max_length=200)
    # space separated acronyms
    sources = models.CharField(max_length=5)

    lemma = models.ForeignKey(Inflection, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class EnglishKeyword(models.Model):
    # override pk to allow use of bulk_create
    id = models.PositiveIntegerField(primary_key=True)

    text = models.CharField(max_length=20)

    lemma = models.ForeignKey(
        Inflection, on_delete=models.CASCADE, related_name="English"
    )

    class Meta:
        indexes = [models.Index(fields=["text"])]
