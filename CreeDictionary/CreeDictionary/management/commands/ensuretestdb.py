from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from API.models import Definition, Wordform
from cvd import definition_vectors_path
from utils import shared_res_dir


class Command(BaseCommand):
    help = """Ensure that the test db exists and is properly set up.

    If it does not exist, it will be created. If it needs to be migrated, it
    will be migrated. If assorted other things need to be in there, they will be
    added if missing.
    """

    def handle(self, *args, **options):
        assert settings.USE_TEST_DB

        call_command("migrate", verbosity=0)

        import_test_dictionary()
        add_some_auto_translations()
        call_command("ensurecypressadminuser")

        if not definition_vectors_path().exists():
            call_command("builddefinitionvectors")


def import_test_dictionary():
    if Wordform.objects.count() == 0:
        print("No wordforms found, generating")
        call_command(
            "xmlimport",
            "import",
            shared_res_dir / "test_dictionaries" / "crkeng.xml",
        )


def add_some_auto_translations():
    if not Definition.objects.filter(auto_translation_source__isnull=False).exists():
        call_command("translatewordforms", wordforms=["acâhkosa"])
