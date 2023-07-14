from fastapi import Depends
from lib import sql_connect as conn
from lib.db_objects import Chat


async def check_dialog_in_db(from_id: int, to_id: int, db: Depends) -> Chat:
    """
    Проверяем есть ли чат в базе данных. Если да то возвращаем объект Chat если нет,
    то создаем объект в бд и возвращаем Chat
    """
    from_chats = await conn.get_users_dialog(db=db, user_id=from_id)
    to_chats = await conn.get_users_dialog(db=db, user_id=to_id)

    chat_id = 0

    for chat in from_chats:
        for to_chat in to_chats:
            if chat[0] == to_chat[0]:
                chat_id = chat[0]

    if chat_id == 0:
        chat_data = await conn.create_chat(db=db, owner_id=from_id)
        await conn.save_user_to_chat(db=db, chat_id=chat_data[0][0], user_id=to_id)
        await conn.save_user_to_chat(db=db, chat_id=chat_data[0][0], user_id=from_id)
    else:
        chat_data = await conn.read_data(db=db, table='all_chats', id_name='chat_id', id_data=chat_id)

    return Chat.parse_obj(chat_data[0])
