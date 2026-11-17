
import uvicorn

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware

from modules.tokens import Tokens
from modules.users import Users


class Web:
    def __init__(
        self,
        tokens: Tokens, users: Users, secret: str,
        ssl: bool = True, debug: bool = False
    ):
        self.tokens = tokens
        self.users = users

        self.ssl = ssl
        self.debug = debug

        self.app = FastAPI()
        self.app.add_middleware(
            SessionMiddleware,
            secret_key=secret,
            session_cookie="session",
            max_age=86400,
            https_only=self.ssl,
            same_site="lax"
        )

        self.register_routes()

    def register_routes(self) -> None:

        @self.app.get("/", response_class=JSONResponse)
        async def index(request: Request):
            uid = request.session.get("uid")
            if uid is None:
                raise HTTPException(status_code=403)

            user = await self.users.get(uid)
            if not user:
                raise HTTPException(status_code=403)

            return JSONResponse({
                "authorized": True,
                "profile": vars(user)
            })

        @self.app.get("/login")
        async def auth(request: Request, token: str | None = None):
            t = await self.tokens.get(token)
            if not t or not self.tokens.validate(t) or not t.user:
                raise HTTPException(status_code=403)

            if not await self.tokens.consume(t):
                raise HTTPException(status_code=403)

            request.session["uid"] = t.user.id

            return RedirectResponse("/", status_code=303)

        @self.app.get("/logout")
        async def logout(request: Request):
            request.session.clear()
            return RedirectResponse("/", status_code=303)

    async def start(self, **kwargs) -> None:
        config = uvicorn.Config(
            self.app,  **kwargs
        )
        server = uvicorn.Server(config)
        await server.serve()
