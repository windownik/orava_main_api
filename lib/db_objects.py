import datetime
import time

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


class Message(BaseModel):
    msg_chat_id: int = 0
    msg_id: int = 0
    msg_type: int = 0
    text: str = '0'

    from_id: int = 0
    to_id: int = 0
    reply_id: int = 0

    chat_id: int = 0
    file_id: int = 0
    status: str = '0'
    read_date: int = 0
    deleted_date: int = 0
    create_date: int = 0

    def to_dialog(self):
        return {
            "msg_chat_id": self.msg_chat_id,
            "msg_type": self.msg_type,
            "text": self.text,
            "from_id": self.from_id,
            "to_id": self.to_id,
            "replay_id": self.reply_id,
            "chat_id": self.chat_id,
            "file_id": self.file_id,
            "status": self.status,
            "read_date": self.read_date,
            "deleted_date": self.deleted_date,
            "create_date": self.create_date,
        }

    def update_msg_id(self, msg_id: int):
        self.msg_id = msg_id


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

        messages_data = await conn.get_users_unread_messages(msg_chat_id=self.msg_chat_id, user_id=user_id, db=db)

        unread_msg = []
        for one in messages_data:
            msg = Message.parse_obj(one)
            unread_msg.append(msg.to_dialog())

        user_to = User.parse_obj(user_data[0])
        resp = self.dict()
        resp['user_to'] = user_to.dict()
        resp['unread_msg'] = unread_msg
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


class ReceiveMessage(BaseModel):
    access_token: str = 0

    msg_chat_id: int = 0
    msg_type: str = '0'
    text: str = '0'
    from_id: int = 0
    to_id: int = 0
    reply_id: int = 0

    chat_id: int = 0
    file_id: int = 0
    status: str = '0'
    file_type: str = '0'
    create_date: int = int(time.mktime(datetime.datetime.now().timetuple()))

    def print_msg(self):
        return self.dict()
