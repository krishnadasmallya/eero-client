import eero
from eero.cookie_store import CookieStore
import responses


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


@responses.activate
def test_eero_login():
    session = CookieStore("session")
    e = eero.Eero(session)
    r = {"data": {"user_token": "test token"}, "meta": {"code": 200}}
    responses.add(
        responses.POST, "https://api-user.e2ro.com/2.2/login", json=r
    )
    assert "test token" == e.login("blah")


@responses.activate
def test_eero_login_verify():
    session = CookieStore("session")
    e = eero.Eero(session)
    r = {"data": {"user_token": "test token"}, "meta": {"code": 200}}
    responses.add(
        responses.POST, "https://api-user.e2ro.com/2.2/login/verify", json=r
    )
    e.login_verify("code", "token")
