from fastapi import Depends
from lib import sql_connect as conn
from lib.db_objects import Dialog


async def check_dialog_in_db(from_id: int, to_id: int, db: Depends) -> Dialog | None:
    """
    Проверяем есть ли чат в базе данных. Если да то возвращаем объект Dialog
    """
    dialog_data = await conn.get_dialog(db=db, from_id=from_id, to_id=to_id)
    if not dialog_data:
        dialog_data = await conn.get_dialog(db=db, from_id=to_id, to_id=from_id)
    if not dialog_data:
        return None

    return Dialog.parse_obj(dialog_data[0])
