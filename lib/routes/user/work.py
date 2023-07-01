import json
import os

import starlette.status as _status
from fastapi import Depends
from starlette.responses import JSONResponse

from lib import sql_connect as conn
from lib.db_objects import UsersWork
from lib.response_examples import *
from lib.sql_connect import data_b, app

ip_server = os.environ.get("IP_SERVER")
ip_port = os.environ.get("PORT_SERVER")

ip_port = 80 if ip_port is None else ip_port
ip_server = "127.0.0.1" if ip_server is None else ip_server


@data_b.on_init
async def initialization(connect):
    # you can run your db initialization code here
    await connect.execute("SELECT 1")


@app.post(path='/user_profession', tags=['Work'], responses=update_user_profession_res)
async def update_user_profession(work_list: str, access_token: str, db=Depends(data_b.connection)):
    """
    Update user's profession information.\n
    work_list: example [{"work_type": "clean", "object_id": 1, "object_size": 1}]\n
    work_type: can be "clean" \n
    object_id: is integer number from object_list\n
    object_size: can be: 1, 2, 3 \n
    """

    user_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not user_id:
        return JSONResponse(content="bad access token",
                            status_code=_status.HTTP_401_UNAUTHORIZED)
    user_id = user_id[0][0]
    try:
        data = json.loads(work_list)
        for i in data:
            b = [i['work_type'], i["object_id"], i["object_size"]]
            await conn.delete_where(db=db, table='work', id_name='user_id', data=user_id)
        for i in data:
            await conn.save_users_work(db=db, user_id=user_id, work_type=i['work_type'], object_id=i["object_id"],
                                       object_size=i["object_size"])
    except Exception as _ex:
        print(_ex)
        return JSONResponse(content={"ok": False,
                                     'desc': 'bad work_list. Please put inside list of items in string '
                                             'with map from example'},
                            status_code=_status.HTTP_400_BAD_REQUEST)
    return JSONResponse(content={"ok": True,
                                 'description': 'users work list updated'},
                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'}
                        )


@app.get(path='/user_profession', tags=['Work'], responses=get_user_profession_list_res)
async def get_user_profession_list(access_token: str, user_id: int = 0, db=Depends(data_b.connection)):
    """
    Get user's profession information.\n
    user_id: is integer number from object_list\n
    """
    if user_id == 0:
        owner_id = await conn.get_token(db=db, token_type='access', token=access_token)
        if not owner_id:
            return JSONResponse(content="bad access token or haven't of access rights",
                                status_code=_status.HTTP_401_UNAUTHORIZED)
        user_id = owner_id[0][0]

    else:
        owner_id = await conn.get_token_admin(db=db, token_type='access', token=access_token)
        if not owner_id:
            return JSONResponse(content="bad access token",
                                status_code=_status.HTTP_401_UNAUTHORIZED)

    work_data = await conn.read_users_work(db=db, user_id=user_id)
    users_work_list = []
    for work in work_data:
        user_work = UsersWork.parse_obj(work)
        users_work_list.append(user_work.dict())

    return JSONResponse(content={"ok": True,
                                 'users_work_list': users_work_list
                                 },
                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'}
                        )


@app.get(path='/object_list', tags=['Work'], responses=get_object_list_res)
async def get_profession_list(db=Depends(data_b.connection)):
    """
    Get all objects types list for all users
    """
    all_object = await conn.read_all(table='object_type', db=db, order='id')
    object_list = []
    for i in all_object:
        object_list.append(
            {
                'id': i[0],
                'name_ru': i[1],
                'name_en': i[2],
                'name_heb': i[3],
            }
        )

    return JSONResponse(content={"ok": True,
                                 'object_types': object_list},
                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'}
                        )
