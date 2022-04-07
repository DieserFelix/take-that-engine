from fastapi import WebSocket
from app.lib.Game import Game

from app.lib.Player import Player


class Room:
    def __init__(self, uuid: str, owner: str):
        self.owner: str = owner
        self.uuid: str = uuid
        self.game: Game = Game()

    async def update(self):
        for _, player in self.game.players.items():
            await player.send(dict(event="GAME_STATE", content=self.game.state(player)))

    async def join(self, uuid: str, name: str, connection: WebSocket):
        try:
            player: Player = Player(uuid, name, uuid == self.owner, connection)
            self.game.add_player(player)
            await self.update()
        except Exception as e:
            print(e)
            await player.send(dict(event="NO_SUCH_ROOM"))

    async def leave(self, uuid: str):
        self.game.remove_player(uuid)
        await self.update()

    async def kick(self, uuid: str, issuer: str = None):
        player = self.game.remove_player(uuid, issuer)
        if player:
            await player.send(dict(event="NO_SUCH_ROOM"))
        await self.update()

    async def start(self, uuid: str):
        self.game.start(uuid)
        await self.update()

    async def reset(self, uuid: str):
        self.game.reset(uuid)
        await self.update()

    async def turn(self, uuid: str, source: int = None, target: int = None):
        if source and target:
            self.game.twist(uuid, source, target)
        elif source:
            self.game.extend(uuid, source)
        else:
            self.game.take(uuid)
        await self.update()