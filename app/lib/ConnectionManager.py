from typing import Any, Dict, List

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Dict[str, WebSocket]] = {}
        self.rooms: List[str] = []

    def open_room(self, room: str):
        self.active_connections[room] = {}

    async def connect(self, room: str, client: str, websocket: WebSocket):
        if room in self.active_connections.keys():
            self.active_connections[room][client] = websocket

    def disconnect(self, room: str, client: str, websocket: WebSocket):
        self.active_connections[room][client] = None

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, room, message: Any):
        for _, connection in self.active_connections[room].items():
            if connection is not None:
                await connection.send_json(message)