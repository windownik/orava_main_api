from fastapi import Depends
from lib import sql_connect as conn


async def check_message(msg: dict, db: Depends, user_id: int) -> bool | str:
    if 'msg_type' not in msg.keys():
        return False
    if msg['msg_type'] == 'echo':
        return 'echo'

    if 'access_token' not in msg.keys():
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