from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

from lib.db_objects import Message


class ConnectionManager:
    def __init__(self):
        self.connections: dict = {int: WebSocket}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.connections[user_id] = websocket

    async def disconnect(self, user_id: int):
        self.connections.pop(user_id)

    async def broadcast(self, data: dict):
        for connect in self.connections:
            await connect.send_json(data)

    async def broadcast_dialog(self, body: dict, users_in_chat: tuple):
        user_id_list = self.connections.keys()
        print(len(users_in_chat), self.connections.keys())
        for user in users_in_chat:
            if user[0] in user_id_list:
                connect = self.connections[user['user_id']]
                await connect.send_json(body)


manager = ConnectionManager()
