from API.models import Wordform
from API.search.types import Result


def test_result_adding_cvd():
    def make_wf(text: str = "foo"):
        ret = Wordform(text=text, is_lemma=True)
        ret.lemma = ret
        return ret

    r = Result(make_wf(), query_wordform_edit_distance=1)
    assert r.cosine_vector_distance is None

    # if the existing Result has no CVD value, populate it from the new one
    r2 = Result(make_wf(), cosine_vector_distance=0.5)
    r.add_features_from(r2)
    assert r.cosine_vector_distance == 0.5

    # replace with better CVD
    r3 = Result(make_wf(), cosine_vector_distance=0.25)
    r.add_features_from(r3)
    assert r.cosine_vector_distance == 0.25

    # ignore worse CVD
    r4 = Result(make_wf(), cosine_vector_distance=0.3)
    r.add_features_from(r4)
    assert r.cosine_vector_distance == 0.25
