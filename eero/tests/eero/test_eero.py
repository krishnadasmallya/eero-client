import pytest
import eero


def test_Eero():
    session = eero.Eero(None)
    assert session is not None
