from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect


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

    async def broadcast_dialog(self, data: dict,):
        connect = self.connections[data["to_id"]]
        await connect.send_json(data)


manager = ConnectionManager()
