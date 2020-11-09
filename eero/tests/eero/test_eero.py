import eero
from eero.cookie_store import CookieStore


def test_eero():
    session = CookieStore("session.cookierandom")
    e = eero.Eero(session)
    assert e is not None
    assert e._cookie_dict is not None
    assert e.needs_login()
