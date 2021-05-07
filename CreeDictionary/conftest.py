import pytest
from django.conf import settings

# See “`conftest.py`: sharing fixtures across multiple files”
# https://docs.pytest.org/en/stable/fixture.html#conftest-py-sharing-fixtures-across-multiple-files
from django.core.management import call_command


@pytest.fixture(scope="session")
def django_db_setup(request, django_db_blocker):
    """
    Normally pytest-django creates a new, empty in-memory database and runs
    all your migrations for you.

    You can override that behaviour by creating your own `django_db_setup`
    fixture: https://pytest-django.readthedocs.io/en/latest/database.html#django-db-setup

    We do so to reuse the same database file every time because:
      - there’s currently no mutation functionality in the app for which
        we need a clean database to test against
      - with the ~1400 entries in the test DB, it takes ~30 seconds to
        generate all the wordforms, which would be too long to wait every
        time you wanted to run a single unit test.

    Also see the docs at
    https://pytest-django.readthedocs.io/en/latest/database.html#examples

    If you want different behaviour for some tests, you can create your own
    django_db_setup fixture in a test file or per-directory conftest.py.

    And to get back the django default behaviour, simply do

        from pytest_django.fixtures import django_db_setup
        django_db_setup # reference so import doesn’t appear unused

    in a test or conftest.
    """

    # If this environment variable is set, a conditional in settings.py
    # should have pointed the database at CreeDictionary/test_db.sqlite3
    assert settings.USE_TEST_DB

    # We’d like the output from the DB setup to go directly to stdout regardless
    # of any capture settings. This is a workaround for “ScopeMismatch: You
    # tried to access the 'function' scoped fixture 'capsys' with a 'session'
    # scoped request object”:
    # https://github.com/pytest-dev/pytest/issues/2704#issuecomment-603387680
    capmanager = request.config.pluginmanager.getplugin("capturemanager")
    with capmanager.global_and_fixture_disabled():

        with django_db_blocker.unblock():
            print("\nSyncing test database")
            call_command("ensuretestdb", verbosity=0)
