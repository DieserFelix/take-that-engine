from typing import Any, List
from fastapi import WebSocket


class Player:
    def __init__(self, uuid: str, name: str, is_owner: bool, connection: WebSocket):
        self.uuid = uuid
        self.name = name
        self.place = -1
        self.is_owner = is_owner
        self.connection = connection
        self.hand: List[int] = []
        self.bonus_stack: List[int] = []
        self.malus_stack: List[int] = []

    def reset(self):
        self.hand = []
        self.bonus_stack = []
        self.malus_stack = []

    def to_dict(self, recipient: str, active: bool, evaluate: bool):
        bonus = len(self.bonus_stack)
        malus = sum(5 if f"{card}"[0] == f"{card}"[1] else 1 for card in self.malus_stack)
        return dict(
            uuid=self.uuid,
            self=self.uuid == recipient,
            name=self.name,
            is_owner=self.is_owner,
            active=active,
            connected=self.connection is not None,
            hand=self.hand if self.uuid == recipient else [-1] * len(self.hand),
            bonus_stack=self.bonus_stack,
            malus_stack=self.malus_stack if self.uuid == recipient else [-1] *
            len(self.malus_stack),
            bonus=bonus if evaluate else None,
            malus=malus if evaluate else None,
            points=bonus - malus
        )

    async def send(self, message: Any = None, messages: List[Any] = None):
        if self.connection is not None:
            if message is not None:
                await self.connection.send_json(message)
            elif messages is not None:
                for msg in messages:
                    await self.connection.send_json(msg)