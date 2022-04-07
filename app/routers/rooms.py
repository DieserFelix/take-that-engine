from uuid import uuid4
from fastapi import APIRouter, Depends
from app.lib import decode_token
from app.lib.Room import Room
from app.routers.games import rooms as r

rooms = APIRouter(prefix="/api/rooms", tags=["rooms"])


@rooms.post("/", response_model=str)
def create_room(client: str = Depends(decode_token)):
    room = str(uuid4())
    r[room] = Room(room, client)
    return room
