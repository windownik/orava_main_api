from fastapi import Depends
from lib import sql_connect as conn

a = {
    "access_token": "1",
    "msg_type": "msg_type",
    "msg_chat_id": 1,
    "text": "text of msg",
    "from_id": 1,
    "to_id": 4,
    "reply_id": 123,
    "chat_id": 4,
    "file_id": 0,
    "file_type": "0"
}


async def check_message(msg: dict, db: Depends, user_id: int) -> bool | str:
    print(msg.keys())
    if 'access_token' not in msg.keys():
        return False
    if 'msg_type' not in msg.keys():
        return False
    if 'msg_chat_id' not in msg.keys():
        return False
    if 'text' not in msg.keys():
        return False
    if 'from_id' not in msg.keys():
        return False
    if 'to_id' not in msg.keys():
        return False
    if 'reply_id' not in msg.keys():
        return False
    if 'chat_id' not in msg.keys():
        return False
    if 'file_id' not in msg.keys():
        return False
    if 'file_type' not in msg.keys():
        return False

    owner_id = await conn.get_token(db=db, token_type='access', token=msg["access_token"])
    if not owner_id:
        return 'bad access'
    print(owner_id[0][0], msg['from_id'], user_id)
    if owner_id[0][0] != msg['from_id'] or owner_id[0][0] != user_id:
        return False

    return True


async def save_msg_in_dialog(msg: dict, db: Depends) -> int:
    msg_id = await conn.save_dialog_msg(db=db, msg=msg)
    return msg_id[0][0]
#
# a = ['access_token', 'msg_chat_id', 'msg_type', 'text', 'from_id', 'to_id', 'reply_id', 'chat_id', 'file_id', 'file_type']
#
# if 'access_token' not in a:
#     print(1)
# if 'msg_type' not in a:
#     print(2)
# if 'msg_chat_id' not in a:
#     print(3)
# if 'text' not in a:
#     print(4)
# if 'from_id' not in a:
#     print(5)
# if 'to_id' not in a:
#     print(6)
# if 'reply_id' not in a:
#     print(7)
# if 'chat_id' not in a:
#     print(8)
# if 'file_id' not in a:
#     print(9)
# if 'file_type' not in a:
#     print(10)