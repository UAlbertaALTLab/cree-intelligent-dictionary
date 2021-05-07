import json
import random
from argparse import ArgumentParser, BooleanOptionalAction
from contextlib import contextmanager

import sys
from django.core.management import BaseCommand
from django.db.models import prefetch_related_objects
from tqdm import tqdm

from API.search import search
from ... import DEFAULT_SAMPLE_FILE
from ...sample import load_sample_definition


class Command(BaseCommand):
    help = """Run search queries from survey, dumping JSON of features"""

    def add_arguments(self, parser: ArgumentParser):
        group = parser.add_argument_group("featuredump-specific options")
        group.add_argument("--csv-file", default=DEFAULT_SAMPLE_FILE)
        group.add_argument(
            "--prefix-queries-with",
            default="",
            help="String to include in every; see the fancy queries help page for suggestions",
        )
        group.add_argument("--max", type=int, help="Only run this many queries")
        group.add_argument(
            "--output-file", help="File to write features to, in JSON format"
        )
        group.add_argument(
            "--shuffle",
            action=BooleanOptionalAction,
            help="Shuffle sample before running, useful with --max",
        )

    def handle(self, *args, **options):
        samples = load_sample_definition(options["csv_file"])
        if options["shuffle"]:
            random.shuffle(samples)
        if options["max"] is not None:
            samples = samples[: options["max"]]

        with output_file(options["output_file"]) as out:
            # Only display progress bar if output is redirected
            if not out.isatty():
                samples = tqdm(samples)

            for entry in samples:
                query = entry["Query"]

                results = search(
                    query=f"verbose:1 {options['prefix_queries_with']} {query}"
                ).sorted_results()
                prefetch_related_objects(
                    [r.wordform for r in results], "definitions__citations"
                )
                for i, r in enumerate(results):
                    ret = r.features()
                    ret["query"] = query
                    ret["wordform_text"] = r.wordform.text
                    ret["lemma_wordform_text"] = r.wordform.lemma.text
                    ret["definitions"] = [
                        [d.text, ", ".join(c.abbrv for c in d.citations.all())]
                        for d in r.wordform.definitions.all()
                        if d.auto_translation_source_id is None
                    ]
                    ret["webapp_sort_rank"] = i + 1
                    print(json.dumps(ret, ensure_ascii=False), file=out)


@contextmanager
def output_file(filename):
    """Context manager that yields an open file, defaulting to sys.stdout"""
    ret = sys.stdout
    should_close = False
    if filename:
        ret = open(filename, "w")
        should_close = True
    try:
        yield ret
    finally:
        if should_close:
            ret.close()
