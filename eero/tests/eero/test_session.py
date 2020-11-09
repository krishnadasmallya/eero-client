from eero.session import Session


def test_session():
    ss = Session()
    assert ss.cookie is None
    assert ss is not None
