from fastapi import WebSocket, Depends
from lib import sql_connect as conn
from lib.db_objects import Message


class SocketResp:
    message: Message
    response_200: dict[str, int | bool | str]
    response_400: dict[str, int | bool | str]

    def __init__(self):
        self.response_401 = {"ok": False,
                             'status_code': 401,
                             'desc': 'bad access'}

    def with_message(self, message: Message):
        self.message = message
        self.response_400 = {"ok": False,
                             'status_code': 400,
                             'desc': 'not check message',
                             "msg_chat_id": message.msg_chat_id,
                             "to_id": message.to_id,
                             "chat_id": message.chat_id, }

    def not_check(self):
        self.response_400 = {"ok": False,
                             'status_code': 400,
                             'desc': 'not check message'}

    def resp_200(self, new_message: Message):
        self.message = new_message
        self.response_200 = {"ok": True,
                             'status_code': 200,
                             'desc': 'save and send to user',
                             "msg_chat_id": new_message.msg_chat_id,
                             "to_id": new_message.to_id,
                             "chat_id": new_message.chat_id,
                             "new_msg_id": new_message.chat_id,
                             }


async def check_message(msg: dict, db: Depends, user_id: int, websocket: WebSocket) -> bool | str:
    socket_resp = SocketResp()
    status = True
    if 'msg_type' not in msg.keys():
        return False
    if msg['msg_type'] == 'echo':
        await websocket.send_json(msg)
        return True

    if 'access_token' not in msg.keys():
        status = False
    if 'msg_chat_id' not in msg.keys():
        status = False
    if 'text' not in msg.keys():
        status = False
    if 'from_id' not in msg.keys():
        status = False
    if 'to_id' not in msg.keys():
        status = False
    if 'reply_id' not in msg.keys():
        status = False
    if 'chat_id' not in msg.keys():
        status = False
    if 'file_id' not in msg.keys():
        status = False
    if 'file_type' not in msg.keys():
        status = False

    if not status:
        await websocket.send_json(socket_resp.not_check())
    message = Message.parse_obj(msg)

    owner_id = await conn.get_token(db=db, token_type='access', token=msg["access_token"])
    if not owner_id:
        return 'bad access'

    if owner_id[0][0] != msg['from_id'] or owner_id[0][0] != user_id:
        socket_resp.with_message(message)
        await websocket.send_json(socket_resp.response_400)
        return False

    if message.msg_type == 'dialog':
        msg_id = await conn.save_dialog_msg(db=db, msg=msg)
        message.update_msg_id(msg_id[0][0])
        socket_resp.resp_200(message)
        await websocket.send_json(socket_resp.response_200)

        return False

    return False

