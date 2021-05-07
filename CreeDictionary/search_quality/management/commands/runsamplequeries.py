from argparse import ArgumentParser, BooleanOptionalAction

from django.core.management import BaseCommand

from ... import DEFAULT_SAMPLE_FILE, RESULTS_DIR
from ...run_sample import gen_run_sample


class Command(BaseCommand):
    help = """Run all the queries in a sample file and save the result

    The resulting json.gz file can later be analyzed for quality of the search
    results, and results run at different times and with different search
    algorithms can be compared.
    """

    def add_arguments(self, parser: ArgumentParser):
        group = parser.add_argument_group("runsamplequeries option")

        group.add_argument("--csv-file", default=DEFAULT_SAMPLE_FILE)
        group.add_argument("--max", type=int, help="Only run this many queries")
        group.add_argument(
            "--shuffle",
            action=BooleanOptionalAction,
            help="Shuffle sample before running, useful with --max",
        )
        group.add_argument(
            "--append-to-query",
            help="Append string to every query, useful with fancy queries",
        )

        naming = group.add_mutually_exclusive_group()
        default_results_file = RESULTS_DIR / "query-results.json.gz"
        naming.add_argument(
            "--result-file-path",
            "--query-results-file",  # legacy name
            help=f"Full path to write results to, default={default_results_file}",
            default=default_results_file,
        )
        naming.add_argument(
            "-n", "--result-file-name", help="Base name to use for results file"
        )

    def handle(self, *args, **options):
        if options["result_file_name"]:
            options["result_file_path"] = RESULTS_DIR / (
                options["result_file_name"] + ".json.gz"
            )

        kwargs = {}
        if options["max"]:
            kwargs["max"] = options["max"]
        if options["shuffle"]:
            kwargs["shuffle"] = True
        if options["append_to_query"]:
            kwargs["append_to_query"] = options["append_to_query"]

        for status in gen_run_sample(
            options["csv_file"], out_file=options["result_file_path"], **kwargs
        ):
            self.stdout.write(status)
