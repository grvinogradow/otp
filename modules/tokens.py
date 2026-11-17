
import secrets, string
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass

from database.modules.tokens import TokensDatabase
from modules.users import Users, User


@dataclass
class Token:
    user: User
    token: str
    active: bool
    made_at: int

class Tokens:
    def __init__(
        self, users: Users, database: TokensDatabase,
        upper: bool = False, expire_time: int = 86400
    ):
        self.database = database
        self.users = users
        self.upper = upper
        self.expire_time = expire_time

    async def add(self, user: User) -> Token:
        t = Token(
            user = user, token = self.generate(12),
            active = True, made_at = int(datetime.now(timezone.utc).timestamp())
        )
        await self.database.add(t.token, t.user.id)
        return t

    async def delete(self, token: Token) -> None:
        await self.database.delete(token.token)

    async def get(self, token: str) -> Token | None:
        t = await self.database.get(token, "id")

        return Token(
            user = await self.users.get(t.get('user')),
            token = t.get('id'),
            active = bool(int(t.get('active'))),
            made_at = int(t.get('made_at'))
        ) if t else None

    async def get_all(self) -> list[Token]:
        return [
            Token(
                token = t.get('id'),
                user = await self.users.get(t.get('user')),
                active = bool(int(t.get('active'))),
                made_at = int(t.get('made_at'))
            )
            for t in await self.database.get_all()
        ]

    def validate(self, token: Token) -> bool:
        if not isinstance(token, Token):
            return False
        return token.active and \
            (datetime.now(timezone.utc).timestamp() - token.made_at <= self.expire_time)

    async def consume(self, token: Token) -> bool:
        if not self.validate(token):
            return False

        token.active = False
        return await self.database.consume(token.token)

    def generate(self, s: int = 12) -> str:
        token = ''.join(
            secrets.choice(string.ascii_letters + string.digits) for _ in range(s)
        )
        return token.upper() if self.upper else token
