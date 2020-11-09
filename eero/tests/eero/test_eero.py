import eero
from eero.cookie_store import CookieStore


def test_eero():
    session = CookieStore("session.cookierandom")
    e = eero.Eero(session)
    assert e is not None
    assert e._cookie_dict is not None
    assert e.needs_login()


def test_id_from_url():
    session = CookieStore("session.cookierandom")
    e = eero.Eero(session)
    result = e.id_from_url("/123")
    assert result == "123"
    result = e.id_from_url("123")
    assert result == "123"
