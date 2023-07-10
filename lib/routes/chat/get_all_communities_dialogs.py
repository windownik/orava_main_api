import os

import starlette.status as _status
from fastapi import Depends
from starlette.responses import Response, JSONResponse

from lib import sql_connect as conn
from lib.db_objects import Dialog
from lib.response_examples import *
from lib.sql_connect import data_b, app

ip_server = os.environ.get("IP_SERVER")
ip_port = os.environ.get("PORT_SERVER")

ip_port = 80 if ip_port is None else ip_port
ip_server = "127.0.0.1" if ip_server is None else ip_server


@app.get(path='/get_all', tags=['Chat'], responses=dialog_created_res)
async def get_all_communities_chats_dialogs(access_token: str, db=Depends(data_b.connection)):
    """Create new user in server.
    access_token: This is access auth token. You can get it when create account or login\n
    """

    owner_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not owner_id:
        return Response(content="bad access token",
                        status_code=_status.HTTP_401_UNAUTHORIZED)
    dialogs_data = await conn.get_users_dialogs(user_id=owner_id[0][0], db=db)
    list_dialogs = []
    for dialog_data in dialogs_data:
        dialog = Dialog.parse_obj(dialog_data)
        list_dialogs.append(await dialog.to_json(db, user_id=owner_id[0][0]))

    return JSONResponse(status_code=_status.HTTP_200_OK,
                        content={"ok": True,
                                 "dialogs": list_dialogs,
                                 "communities": [],
                                 "chats": []
                                 })
