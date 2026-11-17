
import os, asyncio, argparse

from web import Web
from modules.tokens import Tokens
from modules.users import Users

from database.database import Database, SQLite
from database.modules.tokens import TokensDatabase

from dotenv import load_dotenv


class Main:
    def __init__(self, secret: str, debug: bool = False):
        self.debug = debug

        self.database = Database(
            SQLite(),
            TokensDatabase
        )

        # Modules
        self.users = Users( debug = self.debug )
        self.tokens = Tokens(
            users = self.users, database = self.database.TokensDatabase,
            upper = True
        )
        self.web = Web(
            users = self.users, tokens = self.tokens, secret = secret,
            ssl = False,  debug = self.debug
        )

    async def start( self, host: str, port: int ) -> None:
        # Database Init
        await self.database.initialize()
        await self.database.TokensDatabase.setup()

        # Debug Mode
        if self.debug:
            print("Debug mode activated!")

            for i in self.users.users:
                t = await self.tokens.add(i)
                print(f"Token for user {i.id} has been created: {t.token}")

            host = '127.0.0.1'

        # Backend Start
        await self.web.start(host = host, port = port)


if __name__ == "__main__":
    load_dotenv('.env')
    if not os.path.exists('.env'):
        raise ValueError(".env is not found")

    parser = argparse.ArgumentParser()

    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--debug", action="store_true")

    args = parser.parse_args()

    main = Main(
        secret=os.getenv('SECRET'),
        debug=args.debug
    )
    asyncio.run(main.start(args.host, args.port))

