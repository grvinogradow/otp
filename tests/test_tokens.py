
from datetime import datetime, timezone

from modules.tokens import Tokens, Token
from modules.users import User


def test_generate_token():
    tokens = Tokens(users=None, database=None)

    token = tokens.generate()

    assert isinstance(token, str)
    assert len(token) == 12


def test_valid_token():
    tokens = Tokens(users=None, database=None)

    token = Token(
        user=User("steve", "Steve"),
        token="ABC123",
        active=True,
        made_at=int(datetime.now(timezone.utc).timestamp())
    )

    assert tokens.validate(token) is True


def test_inactive_token():
    tokens = Tokens(users=None, database=None)

    token = Token(
        user=User("steve", "Steve"),
        token="ABC123",
        active=False,
        made_at=int(datetime.now(timezone.utc).timestamp())
    )

    assert tokens.validate(token) is False


def test_expired_token():
    tokens = Tokens(users=None, database=None)

    token = Token(
        user=User("steve", "Steve"),
        token="ABC123",
        active=True,
        made_at=int(datetime.now(timezone.utc).timestamp()) - 172800
    )

    assert tokens.validate(token) is False
