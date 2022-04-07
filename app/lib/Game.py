from random import Random
from typing import Dict, List
from app.lib.Deck import Deck
from app.lib.Player import Player

HAND_SIZE = {
    2: 9,
    3: 9,
    4: 8
}


class Game:
    def __init__(self):
        self.players: Dict[str, Player] = {}
        self.ingame: bool = False
        self.ended: bool = False
        self.deck: Deck = Deck()
        self.row: List[int] = []
        self.active_player = -1

    def add_player(self, player: Player):
        if player.uuid in self.players.keys():
            self.players[player.uuid].connection = player.connection
        else:
            if not self.ingame:
                if len(self.players.keys()) == 4:
                    raise Exception()
                self.players[player.uuid] = player

                uuids = list(self.players.keys())
                for i in range(0, len(uuids)):
                    uuid = uuids[i]
                    self.players[uuid].place = i

    def remove_player(self, uuid: str, issuer: str = None):
        if uuid in self.players.keys():
            if issuer:
                if issuer not in self.players.keys(
                ) or not self.players[issuer].is_owner or self.players[uuid].is_owner:
                    return

                player = self.players[uuid]
                del self.players[uuid]
                uuids = list(self.players.keys())
                for i in range(0, len(uuids)):
                    uuid = uuids[i]
                    self.players[uuid].place = i

                if len(uuids) == 1:
                    self.ended = True

                return player
            else:
                self.players[uuid].connection = None

    def start(self, uuid: str):
        if not self.ingame:
            if uuid in self.players.keys():
                if self.players[uuid].is_owner:
                    if len(self.players.keys()) >= 2:
                        self.prepare()
                        self.ingame = True

    def reset(self, uuid: str):
        if uuid in self.players.keys():
            if self.players[uuid].is_owner:
                self.deck.reset()
                for _, player in self.players.items():
                    player.reset()
                self.ingame = False
                self.ended = False

    def prepare(self):
        for _, player in self.players.items():
            for _ in range(0, HAND_SIZE[len(self.players.keys())]):
                player.hand.append(self.deck.pop())

        self.active_player = Random().randint(0, len(self.players.keys()) - 1)

    def twist(self, uuid: str, source: int, target: int):
        if self.ingame and not self.ended:
            uuids = list(self.players.keys())
            player = self.players[uuids[self.active_player]]
            if player.uuid == uuid:
                if source in player.hand and target in self.row:
                    if f"{source}" == f"{target}"[::-1]:
                        player.hand.remove(source)
                        player.bonus_stack.append(source)
                        self.row.remove(target)
                        player.bonus_stack.append(target)
                        if len(self.deck) > 0:
                            player.hand.append(self.deck.pop())
                        elif len(self.row) == 0:
                            self.ended = True

                        self.active_player = (self.active_player + 1) % len(self.players.keys())

    def extend(self, uuid: str, source: int):
        if self.ingame and not self.ended:
            uuids = list(self.players.keys())
            player = self.players[uuids[self.active_player]]
            if player.uuid == uuid:
                if source in player.hand:
                    if len(self.row
                          ) == 0 or (source >= self.row[-1] - 10 and source <= self.row[-1] + 10):
                        self.row.append(source)
                        player.hand.remove(source)
                        if len(self.deck) > 0:
                            player.hand.append(self.deck.pop())
                        else:
                            cardsOnHands = sum(
                                len(player.hand) for _, player in self.players.items()
                            )
                            if cardsOnHands == 0:
                                self.ended = True

                        self.active_player = (self.active_player + 1) % len(self.players.keys())

    def take(self, uuid: str):
        if self.ingame and not self.ended:
            uuids = list(self.players.keys())
            player = self.players[uuids[self.active_player]]
            if player.uuid == uuid:
                player.malus_stack += self.row
                self.row = []
                if len(self.deck) == 0:
                    self.ended = True

    def state(self, recipient: Player):
        return dict(
            ingame=self.ingame,
            ended=self.ended,
            deck_size=len(self.deck),
            row=self.row,
            players={
                player.place:
                player.to_dict(recipient.uuid, player.place == self.active_player, self.ended)
                for _, player in self.players.items()
            }
        )
