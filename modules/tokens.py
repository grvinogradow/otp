
import secrets, string
from datetime import datetime, timezone, timedelta

from database.modules.tokens import TokensDatabase
from modules.users import Users, User

class Token:
    def __init__(
        self, user: User, token: str, active: bool, made_at: int
    ):
        self.user = user
        self.token = token
        self.active = active
        self.made_at = made_at

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

    async def validate(self, token: Token) -> bool:
        return token.active and \
            (datetime.now(timezone.utc).timestamp() - token.made_at <= self.expire_time)

    async def deactivate(self, token: Token) -> None:
        await self.database.update(token.token, "active", False)

    def generate(self, s: int = 12) -> str:
        token = ''.join(
            secrets.choice(string.ascii_letters + string.digits) for _ in range(s)
        )
        return token.upper() if self.upper else token

if __name__ == "__main__":
    tokens = Tokens()
    print(tokens.generate())
