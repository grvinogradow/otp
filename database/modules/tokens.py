
from database.database import Database, SQLite


class TokensDatabase:
    def __init__(self, database: Database):
        self.database : SQLite = database.instance
        self.table = 'tokens'

        self.keys = {
            "user": str, "active": bool
        }

    async def setup(self):
        await self.database.setup( self.table, **self.keys )

    async def add(
        self, token: str, user: str
    ):
        await self.database.insert(
            self.table, token, user = user, active = True
        )

    async def get(self, token: str, param: str = None) -> dict:
        return await self.database.get( self.table, token, param )

    async def delete(self, token: str):
        await self.database.delete( self.table, token )

    async def update(self, token: str, parameter: str, value):
        await self.database.update(
            self.table, token,
            parameter = parameter, value = value
        )

    async def get_all(self) -> list:
        return await self.database.get_all( table = self.table )
