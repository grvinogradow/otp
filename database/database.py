
import aiosqlite


class DatabaseError(Exception):
    pass


class SQLite:
    def __init__(self, name: str = 'database.db'):
        self.name = name
        self.conn: aiosqlite.Connection = None
        self.KEYS = { int: "INTEGER", str: "TEXT" }

    async def connect(self):
        self.conn = await aiosqlite.connect(self.name)
        await self.conn.execute("PRAGMA foreign_keys = ON;")
        await self.conn.commit()

    async def setup( self, table: str, **keys ) -> None:
        try:
            keys = ", ".join([
                f"{key} {self.KEYS.get(ktype, 'TEXT')}" for key, ktype in keys.items()
            ])

            await self.conn.execute(f'''
                CREATE TABLE IF NOT EXISTS { table } (
                    id TEXT PRIMARY KEY,  { keys },
                    made_at INTEGER DEFAULT (strftime('%s', 'now'))
                )
            ''')
            await self.conn.commit()
        except Exception as e:
            raise DatabaseError(e)

    async def insert( self, table: str, recordid: str, **fields ) -> None:
        try:
            keys = ", ".join( fields.keys() )
            values = fields.values()

            await self.conn.execute(
                f"""INSERT INTO { table } (
                    id, { keys }
                ) VALUES (?{ ", ?" * len(fields) })""",
                (recordid, *values)
            )

            await self.conn.commit()
        except Exception as e:
            raise DatabaseError(e)

    async def get(
        self, table: str, id: str, param: str = None
    ) -> dict | None:
        try:
            async with self.conn.execute(
                f"SELECT * FROM { table } WHERE { param if param else 'id' } = ?",
                (id,)
            ) as cursor:
                row = await cursor.fetchone()
                if not row:
                    return None
                columns = [column[0] for column in cursor.description]
                return dict(zip(columns, row))
        except Exception as e:
            raise DatabaseError(e)

    async def delete( self, table: str, id: str ) -> None:
        try:
            await self.conn.execute(f"DELETE FROM { table } WHERE id = ?", (id,))
            await self.conn.commit()
        except Exception as e:
            raise DatabaseError(e)

    async def update(
        self, table: str, id: str, parameter: str, value
    ) -> None:
        try:
            await self.conn.execute(
                f"UPDATE { table } SET { parameter } = ? WHERE id = ?",
                (value, id)
            )
            await self.conn.commit()
        except Exception as e:
            raise DatabaseError(e)

    async def get_all(
        self, table: str, param: str = None, value: str = None
    ) -> list:
        try:
            if param is not None and value is not None:
                req = f"SELECT * FROM {table} WHERE {param} = ?"
                params = (value,)
            else:
                req = f"SELECT * FROM {table}"
                params = ()

            async with self.conn.execute(req, params) as cursor:
                rows = await cursor.fetchall()
                columns = [column[0] for column in cursor.description]
                return [dict(zip(columns, row)) for row in rows]

        except Exception as e:
            raise DatabaseError(e) from e


class Database:
    def __init__(self, instance: SQLite, *modules):
        self.instance = instance
        self.modules = modules

        for module in self.modules:
            i = module(self)
            setattr(self, module.__name__, i)

    async def initialize(self):
        await self.instance.connect()
        for module in self.modules:
            await getattr(self, module.__name__).setup()
