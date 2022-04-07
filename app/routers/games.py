from typing import Dict, List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.lib.Room import Room
from app.lib.decode_token import decode_token
from jose import jwt
from app.lib.environment import SECRET_KEY

rooms: Dict[str, Room] = {}

games = APIRouter(prefix="/api/games", tags=["games"])


@games.websocket("/{room}")
async def engine(socket: WebSocket, room: str):
    await socket.accept()
    if room not in rooms.keys():
        print("no such room")
        await socket.send_json(dict(event="NO_SUCH_ROOM"))
        await socket.close()
    else:
        room: Room = rooms[room]
        uuid = ""
        try:
            while True:
                msg = await socket.receive_json()
                if isinstance(msg, dict):
                    if not "event" in msg.keys():
                        continue
                    elif not "data" in msg.keys():
                        continue
                    if isinstance(msg["data"], dict):
                        if not "client" in msg["data"].keys():
                            continue
                    else:
                        continue
                else:
                    continue
                uuid = jwt.decode(msg["data"]["client"], SECRET_KEY,
                                  algorithms=["HS256"]).get("sub")
                if msg["event"] == "join":
                    if "name" in msg["data"].keys():
                        name = msg["data"]["name"]
                        await room.join(uuid, name, socket)
                elif msg["event"] == "kick":
                    if "uuid" in msg["data"].keys():
                        player = msg["data"]["uuid"]
                        await room.kick(player, issuer=uuid)
                elif msg["event"] == "start":
                    await room.start(uuid)
                elif msg["event"] == "reset":
                    await room.reset(uuid)
                elif msg["event"] == "extend":
                    if "source" in msg["data"].keys():
                        source = msg["data"]["source"]
                        await room.turn(uuid, source)
                elif msg["event"] == "twist":
                    if "source" in msg["data"].keys() and "target" in msg["data"].keys():
                        source = msg["data"]["source"]
                        target = msg["data"]["target"]
                        await room.turn(uuid, source, target)
                elif msg["event"] == "take":
                    await room.turn(uuid)
                elif msg["event"] == "reset":
                    await room.reset(uuid)
        except WebSocketDisconnect:
            if uuid:
                print("client lost connection")
                await room.leave(uuid)