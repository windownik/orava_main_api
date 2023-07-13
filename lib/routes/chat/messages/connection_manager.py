from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

from lib.db_objects import Message


class ConnectionManager:
    def __init__(self):
        self.connections: dict = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.connections[user_id] = websocket

    async def disconnect(self, user_id: int):
        self.connections.pop(user_id)

    async def broadcast(self, data: dict):
        for connect in self.connections:
            await connect.send_json(data)

    async def broadcast_dialog(self, message: Message,):
        user_id_list = self.connections.keys()
        if message.to_id in user_id_list:
            connect = self.connections[message.to_id]
            await connect.send_json(message.to_dialog())


manager = ConnectionManager()
