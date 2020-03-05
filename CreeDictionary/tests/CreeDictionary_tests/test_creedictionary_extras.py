#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pytest
from CreeDictionary.templatetags.creedictionary_extras import orth
from django.http import HttpRequest
from django.template import Context, RequestContext, Template
from pytest_django.asserts import assertInHTML


def test_orth_requires_two_arguments():
    """
    orth() original only took one argument, but now it must take two.
    """
    with pytest.raises(TypeError):
        orth("wâpamêw")


def test_produces_correct_markup():
    context = Context({"wordform": "wâpamêw"})
    template = Template("{% load creedictionary_extras %}" "{{ wordform|orth:'Latn' }}")

    rendered = template.render(context)
    assert 'lang="cr"' in rendered
    assert 'data-orth-Latn="wâpamêw"' in rendered
    assert 'data-orth-Latn-x-macron="wāpamēw"' in rendered
    assert 'data-orth-Cans="ᐚᐸᒣᐤ"' in rendered
    assertInHTML(
        """
        <span lang="cr" data-orth
              data-orth-Latn="wâpamêw"
              data-orth-latn-x-macron="wāpamēw"
              data-orth-Cans="ᐚᐸᒣᐤ">wâpamêw</span>
        """,
        rendered,
    )


def test_naughty_html():
    """
    Does it escape bad HTML?
    """

    context = Context({"wordform": '<img alt="tâpwêw">'})
    template = Template("{% load creedictionary_extras %}" "{{ wordform|orth:'Latn' }}")

    rendered = template.render(context)
    assertInHTML(
        """
        <span lang="cr" data-orth
              data-orth-Latn="&lt;img alt=&quot;tâpwêw&quot;&gt;"
              data-orth-latn-x-macron="&lt;img alt=&quot;tāpwēw&quot;&gt;"
              data-orth-Cans="&lt;img alt=&quot;ᑖᐻᐤ&quot;&gt;">&lt;img alt=&quot;tâpwêw&quot;&gt;</span>
        """,
        rendered,
    )


@pytest.mark.parametrize(
    "orth,inner_text",
    [("Latn", "wâpamêw"), ("Latn-x-macron", "wāpamēw"), ("Cans", "ᐚᐸᒣᐤ"),],
)
def test_provide_orthograpy(orth, inner_text):
    context = Context({"wordform": "wâpamêw"})
    template = Template(
        "{% load creedictionary_extras %}" "{{ wordform|orth:" + repr(orth) + " }}"
    )

    rendered = template.render(context)
    assertInHTML(
        f"""
        <span lang="cr" data-orth
              data-orth-Latn="wâpamêw"
              data-orth-latn-x-macron="wāpamēw"
              data-orth-Cans="ᐚᐸᒣᐤ">{inner_text}</span>
        """,
        rendered,
    )


@pytest.mark.parametrize(
    "orth,inner_text",
    [
        ("Latn", "wâpamêw"),
        ("Latn-x-macron", "wāpamēw"),
        ("Cans", "ᐚᐸᒣᐤ"),
        (None, "wâpamêw"),  # use Latn if the cookie is not set in the request
    ],
)
def test_orth_template_tag(orth, inner_text):
    """
    Test that the {% orth %} tag uses the orthography in the request's cookie.
    """
    request = HttpRequest()
    if orth is not None:
        request.COOKIES["orth"] = orth

    context = RequestContext(request, {"wordform": "wâpamêw"})
    template = Template("{% load creedictionary_extras %}" "{% orth wordform %}")
    rendered = template.render(context)

    assertInHTML(
        f"""
        <span lang="cr" data-orth
              data-orth-Latn="wâpamêw"
              data-orth-latn-x-macron="wāpamēw"
              data-orth-Cans="ᐚᐸᒣᐤ">{inner_text}</span>
        """,
        rendered,
    )


@pytest.mark.parametrize(
    "orth,name",
    [("Latn", "SRO"), ("Latn-x-macron", "SRO"), ("Cans", "Syllabics"), (None, "SRO")],
)
def test_current_orthography_name_tag(orth, name):
    """
    Test that the {% current_orthography_name %} tag uses the orthography in the request's cookie.
    """
    request = HttpRequest()
    if orth is not None:
        request.COOKIES["orth"] = orth

    context = RequestContext(request)
    template = Template(
        "{% load creedictionary_extras %}" "{% current_orthography_name %}"
    )
    rendered_html = template.render(context)
    assert name in rendered_html
