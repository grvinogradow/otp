
from dataclasses import dataclass


@dataclass
class User:
    id: str
    name: str

class Users:
    def __init__(self, debug: bool):
        self.debug = debug
        self.users = []

        if self.debug:
            self.users = [
                User("steve", "Steve"),
                User("alex", "Alex")
            ]

    async def get(self, id: str) -> User | None:
        return next((i for i in self.users if i.id == id), None)
