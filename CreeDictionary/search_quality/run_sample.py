import gzip
import json
import random
from typing import Optional

import time
from os import PathLike

from API.search import search_with_affixes
from . import SampleSearchResultsJson, DEFAULT_SAMPLE_FILE
from .analyze_results import count_results
from .sample import load_sample_definition


def gen_run_sample(
    sample_file: PathLike = DEFAULT_SAMPLE_FILE,
    *,
    out_file: PathLike,
    max: Optional[int] = None,
    shuffle=False,
    append_to_query=None,
):
    "Run the sample, yielding status messages"

    combined_results: SampleSearchResultsJson = {}

    samples = load_sample_definition(sample_file)
    if shuffle:
        random.shuffle(samples)
    if max is not None:
        samples = samples[:max]

    for entry in samples:
        query = entry["Query"]

        # If we were being rigorous about timing, we’d run all the queries
        # multiple times in randomized orders to spread out the effects of
        # warmup and caching
        start_time = time.time()
        results = search_with_affixes(
            query + (" " + append_to_query if append_to_query else "")
        )
        time_taken = time.time() - start_time

        combined_results[query] = {
            "time_taken_seconds": time_taken,
            "results": results,
        }

        count = count_results(results)
        yield f"{count:,} results for ‘{query}’ in {time_taken:0.3}s"

    # "wt" because although gzip is a binary file format, json.dump is going to
    # want to write a string inside it
    with gzip.open(out_file, "wt") as out:
        json.dump(combined_results, out, ensure_ascii=False, indent=2)
    print(f"Output written to {out_file}")
