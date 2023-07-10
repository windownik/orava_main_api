import os

import starlette.status as _status
from fastapi import Depends
from starlette.responses import Response, JSONResponse

from lib import sql_connect as conn
from lib.db_objects import User
from lib.response_examples import *
from lib.sql_connect import data_b, app

ip_server = os.environ.get("IP_SERVER")
ip_port = os.environ.get("PORT_SERVER")

ip_port = 80 if ip_port is None else ip_port
ip_server = "127.0.0.1" if ip_server is None else ip_server


@app.post(path='/chat', tags=['Chat'], responses=create_user_res)
async def new_user(access_token: str, chat_type: str = 'dialog', name: str = '0', community_id: int = 0, image_link: str = '0',
                   image_link_little: str = '0', db=Depends(data_b.connection)):
    """Create new user in server.
    name: you can add name only for chat type\n
    midl_name:  users midl name\n
    surname: users midl surname\n
    phone: example 375294322114\n
    image_link: get from facebook API\n
    chat_type: status can be: dialog, chat"""

    owner_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not owner_id:
        return Response(content="bad access token",
                        status_code=_status.HTTP_401_UNAUTHORIZED)

    if chat_type != 'dialog' and chat_type != 'chat':
        return JSONResponse(status_code=_status.HTTP_400_BAD_REQUEST,
                            content={"ok": False,
                                     'description': 'Bad status', })

    data = await conn.create_user(db=db, user=user)
    user = User.parse_obj(data[0])

    return JSONResponse(content={"ok": True,
                                 'chat': user.dict(
                                     exclude={"push"}
                                 )},
                        status_code=_status.HTTP_200_OK,

                        headers={'content-type': 'application/json; charset=utf-8'})


@app.get(path='/user', tags=['User'], responses=get_me_res)
async def get_user_information(access_token: str, db=Depends(data_b.connection), user_id: int = 0):
    """Here you can check your username and password. Get users information.\n
    access_token: This is access auth token. You can get it when create account, login"""
    owner_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not owner_id:
        return Response(content="bad access token",
                        status_code=_status.HTTP_401_UNAUTHORIZED)
    if user_id != 0:
        user_data = await conn.read_data(db=db, name='*', table='all_users',
                                         id_name='user_id', id_data=user_id)
    else:
        user_data = await conn.read_data(db=db, name='*', table='all_users',
                                         id_name='user_id', id_data=owner_id[0][0])
    if not user_data:
        return Response(content="no user in database",
                        status_code=_status.HTTP_400_BAD_REQUEST)

    user = User.parse_obj(user_data[0])
    return JSONResponse(content={"ok": True,
                                 'user': user.dict(
                                     exclude={"push"}
                                 ),
                                 },
                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'})

