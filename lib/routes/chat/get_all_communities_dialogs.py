import os

import starlette.status as _status
from fastapi import Depends
from starlette.responses import Response, JSONResponse

from lib import sql_connect as conn
from lib.db_objects import Chat, User, Community
from lib.response_examples import *
from lib.sql_connect import data_b, app

ip_server = os.environ.get("IP_SERVER")
ip_port = os.environ.get("PORT_SERVER")

ip_port = 80 if ip_port is None else ip_port
ip_server = "127.0.0.1" if ip_server is None else ip_server


@app.get(path='/get_all', tags=['Chat'], responses=get_all_res)
async def get_all_communities_chats(access_token: str, db=Depends(data_b.connection)):
    """Get all user's information about chats and communities.
    access_token: This is access auth token. You can get it when create account or login\n
    """

    owner_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not owner_id:
        return JSONResponse(content={"ok": False, "description": "bad access token"},
                            status_code=_status.HTTP_401_UNAUTHORIZED)
    user_data = await conn.read_data(db=db, name='*', table='all_users', id_name='user_id', id_data=owner_id[0][0])
    user = User.parse_obj(user_data[0])

    # Очищаем пуш метки
    await conn.clear_users_chat_push(db=db, user_id=owner_id[0][0])

    chats_data = await conn.get_users_chats(user_id=owner_id[0][0], db=db)
    list_chats = []

    for chat_data in chats_data:
        chat = Chat.parse_obj(chat_data)

        list_chats.append(await chat.to_json(db, reqwest_user=user))

    community_list = []
    comm_data = await conn.get_users_community(user_id=owner_id[0][0], db=db)
    for _comm in comm_data:
        comm = Community.parse_obj(_comm)
        for one in list_chats:
            if one['chat_id'] == comm.main_chat_id:
                comm.total_users_count = one['all_users_count']
        community_list.append(comm.dict())

    return JSONResponse(status_code=_status.HTTP_200_OK,
                        content={"ok": True,
                                 'user': user.dict(),
                                 "chats": list_chats,
                                 "community_list": community_list,
                                 },
                        headers={'content-type': 'application/json; charset=utf-8'})
