from fastapi import WebSocket, Depends
from lib import sql_connect as conn
from lib.db_objects import ReceiveMessage
from lib.routes.chat.messages.connection_manager import ConnectionManager


class SocketResp:
    receive_msg: ReceiveMessage = None
    response_200: dict[str, int | bool | str]
    response_401: dict[str, int | bool | str]
    response_400_rights: dict[str, int | bool | str]
    response_201_confirm_receive: dict[str, int | bool | str]

    def __init__(self):
        self.response_400_not_check = {"ok": False,
                                       'status_code': 400,
                                       "msg_type": "system",
                                       'desc': 'not check message'}

    def update_message(self, receive_msg: ReceiveMessage):
        self.receive_msg = receive_msg

        self.response_401 = {"ok": False,
                             'status_code': 401,
                             'msg_client_id': receive_msg.msg_client_id,
                             "msg_type": "system",
                             'desc': 'bad access'}

        self.response_401 = {"ok": False,
                             'status_code': 400,
                             'msg_client_id': receive_msg.msg_client_id,
                             "msg_type": "system",
                             'desc': 'not enough rights'}

        self.response_201_confirm_receive = {"ok": True,
                                             'status_code': 201,
                                             'msg_client_id': receive_msg.msg_client_id,
                                             'msg_server_id': receive_msg.body.msg_id,
                                             "msg_type": "delivery",
                                             'desc': 'success receive'}

        self.response_200 = {"ok": True,
                             'status_code': 200,
                             "msg_type": "send_message",
                             'desc': 'save and send to user',
                             "body": self.receive_msg.body.dict()
                             }


example_message = {
    'access_token': 'fnriverino',
    'msg_client_id': 12,
    'msg_type': 'chat_message',
    'body': {
        'msg_id': 2132,
        'text': 'Text of this message',
        'from_id': 32,
        'reply_id': 342,
        'chat_id': 65,
        'file_id': 0,
        'status': 'not_read',
        'read_date': 0,
        'deleted_date': 0,
        'create_date': 124321412,
    }
}


def check_msg(msg: dict):
    for key in example_message.keys():
        if key not in msg.keys():
            return False

    for key in example_message['body'].keys():
        if key not in msg['body'].keys():
            return False
    return True


async def msg_manager(msg: dict, db: Depends, user_id: int, websocket: WebSocket,
                      manager: ConnectionManager):
    # Проверяем структуру сообщения
    socket_resp = SocketResp()
    if not check_msg(msg):
        await websocket.send_json(socket_resp.response_400_not_check)
        return True

    receive_msg = ReceiveMessage.parse_obj(msg)
    socket_resp.update_message(receive_msg)

    # Проверяем права доступа на сообщение
    owner_id = await conn.get_token(db=db, token_type='access', token=receive_msg.access_token)

    if not owner_id:
        await websocket.send_json(socket_resp.response_401)
        return True

    msg_id = await conn.save_msg(db=db, msg=msg['body'])

    msg['body']['msg_id'] = msg_id[0][0]

    receive_msg = ReceiveMessage.parse_obj(msg)
    socket_resp.update_message(receive_msg)

    # отправляем подтверждение о доставке и сохранении
    await websocket.send_json(socket_resp.response_201_confirm_receive)

    user_in_chat = await conn.check_user_in_chat(db=db, user_id=user_id, chat_id=receive_msg.body.chat_id)
    if not user_in_chat:
        await websocket.send_json(socket_resp.response_400_rights)
        return True

    all_users = await conn.read_data(table='users_chat', id_name='chat_id',
                                     id_data=receive_msg.body.chat_id, db=db)

    push_users = await manager.broadcast_dialog(users_in_chat=all_users, body=socket_resp.response_200, msg=receive_msg)
    for user in push_users:
        await conn.update_users_chat_push(db=db, chat_id=receive_msg.body.chat_id, user_id=user['user_id'])
        await conn.save_push_to_sending(db=db, msg_id=f"{receive_msg.body.msg_id}", push_type='text',
                                        title=f'Новое сообщение',
                                        short_text='У вас новое сообщение в чате: ', user_id=user['user_id'])
    #     if user[0] == user_id:
    #         continue
    #
    #     # Обрабатываем случай когда пользователь онлайн
    #     if user[0] in manager.connections.keys():
    #         connect = manager.connections[user[0]]
    #         await connect.send_json(socket_resp.response_200)
    #
    #     # Обрабатываем случай когда пользователь офлайн. Просто записываем в таблицу рассылки пушей
    #     else:
    #         if user['push_sent']:
    #             continue
    #         else:

