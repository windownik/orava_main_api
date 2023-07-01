import os

import starlette.status as _status
from fastapi import Depends
from starlette.responses import JSONResponse

from lib import sql_connect as conn
from lib.db_objects import User
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


@app.put(path='/user_status', tags=['Admin users'], responses=update_user_status_res)
async def update_user_information(user_id: int, status: str, access_token: str, db=Depends(data_b.connection)):
    """Admin Update user's status.

    user_id: users number from our service\n
    status: can be: worker, customer, admin, ban\n
    access_token: This is access auth token. You can get it when create account, login or \n"""

    if status != 'customer' and status != 'worker' and status != 'admin' and status != 'ban':
        return JSONResponse(status_code=_status.HTTP_400_BAD_REQUEST,
                            content={"ok": False,
                                     'description': 'Bad users status', })

    admin_id = await conn.get_token_admin(db=db, token_type='access', token=access_token)
    owner_id = await conn.get_token(db=db, token_type='access', token=access_token)

    if admin_id:
        pass
    elif owner_id:
        if owner_id[0][0] == user_id:
            pass
        else:
            return JSONResponse(content={"ok": False,
                                         'description': "bad access token or not enough rights"},
                                status_code=_status.HTTP_401_UNAUTHORIZED)
    else:
        return JSONResponse(content={"ok": False,
                                     'description': "bad access token or not enough rights"},
                            status_code=_status.HTTP_401_UNAUTHORIZED)

    user_data = await conn.read_data(db=db, name='status', table='all_users', id_name='user_id',
                                     id_data=user_id)
    if user_data is None:
        return JSONResponse(content={"ok": False,
                                     'description': "I haven't user with this user_id."},
                            status_code=_status.HTTP_400_BAD_REQUEST)

    await conn.update_data(db=db, table='all_users', name='status', id_name='user_id', id_data=user_id, data=status)

    return JSONResponse(content={"ok": True,
                                 'desc': 'users status updated'},
                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'})


@app.get(path='/admin_get_user', tags=['Admin users'], responses=update_user_status_res)
async def admin_get_users_with_search(access_token: str, user_type: str = 'all', search: str = '0', offset: int = 0,
                                      limit: int = 5, db=Depends(data_b.connection)):
    """Admin get users with search and offset.\n
    user_type: can be: all, worker, customer, admin, all_new\n
    search: substring for searching in email, name and phone\n
    access_token: This is access auth token. You can get it when create account, login or \n"""

    admin_id = await conn.get_token_admin(db=db, token_type='access', token=access_token)

    if not admin_id:
        return JSONResponse(content={"ok": False,
                                     'description': "bad access token or not enough rights"},
                            status_code=_status.HTTP_401_UNAUTHORIZED)

    if user_type not in ('all', 'worker', 'customer', 'admin', 'all_new'):
        return JSONResponse(content={"ok": False,
                                     'description': "bad user_type"},
                            status_code=_status.HTTP_400_BAD_REQUEST)

    search = search.lower()
    users_list = []
    users_count = 0
    if search == "0":
        users_count = (await conn.count_all(db=db, user_type=user_type))[0][0]
        users_data = await conn.admin_read_users(db=db, offset=offset, limit=limit, user_type=user_type)
        for one in users_data:
            user = User(one)
            users_list.append(user.get_user_json())
    else:
        users_data = await conn.admin_read_users(db=db, offset=offset, limit=limit, user_type=user_type, skip_limit=True)
        for one in users_data:
            if search not in (one['email']).lower() and search not in (one['name']).lower() \
                    and search not in str(one['phone']):
                continue
            users_count += 1
            if offset > 0:
                offset -= 1
                continue

            if limit <= 0:
                pass
            else:
                user = User(one)
                users_list.append(user.get_user_json())

            limit -= 1

    return JSONResponse(content={"ok": True,
                                 "total_users_count": users_count,
                                 'users': users_list,
                                 },
                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'})
