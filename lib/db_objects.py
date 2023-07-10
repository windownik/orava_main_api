import datetime

from fastapi import Depends
from pydantic import BaseModel

from lib import sql_connect as conn


class User(BaseModel):
    user_id: int
    name: str
    middle_name: str
    surname: str
    phone: int
    email: str
    image_link: str
    image_link_little: str
    description: str
    lang: str
    status: str
    push: str
    last_active: int
    create_date: int


class File(BaseModel):
    file_id: int = 0
    file_type: str = '0'


class Chat(BaseModel):
    chat_id: int = 0
    owner_user: User = None
    name: str = '0'
    img_url: str = '0'
    little_img_url: str = '0'
    status: str = '0'
    open_profile: bool = True
    send_media: bool = True
    send_voice: bool = True
    deleted_date: datetime.datetime = None
    create_date: datetime.datetime = None


class Dialog(BaseModel):
    msg_chat_id: int = 0
    owner_id: int = 0
    to_id: int = 0
    owner_status: str = '0'
    to_status: str = '0'
    create_date: int

    async def to_json(self, db: Depends, user_id: int):

        if user_id == self.owner_id:
            user_data = await conn.read_data(table='all_users', id_name='user_id', id_data=self.to_id, db=db)

        else:
            user_data = await conn.read_data(table='all_users', id_name='user_id', id_data=self.owner_id, db=db)
            self.to_status = self.owner_status

        user_to = User.parse_obj(user_data[0])
        resp = self.dict()
        resp['user_to'] = user_to.dict()
        resp.pop('owner_id')
        resp.pop('to_id')
        resp.pop('owner_status')
        return resp


class Community(BaseModel):
    community_id: int = 0
    owner_user: User = None
    name: str = '0'
    main_chat: Chat = None
    join_code: str = '0'
    img_url: str = '0'
    little_img_url: str = '0'
    status: str = '0'
    open_profile: bool = True
    send_media: bool = True
    send_voice: bool = True
    deleted_date: datetime.datetime = None
    create_date: datetime.datetime = None


class Message(BaseModel):
    msg_id: int = 0
    text: str = '0'
    replay_id: int = 0
    from_user: User = None
    to_user: User = None
    chat: Chat = None
    file: File = None
    status: str = '0'
    read_date: datetime.datetime = None
    deleted_date: datetime.datetime = None
    create_date: datetime.datetime = None
