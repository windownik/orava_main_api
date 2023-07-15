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
    owner_id: int = 0
    owner_user: User = None
    second_user: User = None
    community_id: int = 0
    name: str = '0'
    img_url: str = '0'
    little_img_url: str = '0'
    chat_type: str = 'dialog'
    status: str = '0'
    open_profile: bool = True
    send_media: bool = True
    send_voice: bool = True
    deleted_date: int = None
    create_date: int = None

    async def to_json(self, db: Depends, dialog_user_data: tuple = None):
        if dialog_user_data is not None:
            self.second_user = User.parse_obj(dialog_user_data[0])

        user_data = await conn.read_data(table='all_users', id_name='user_id', id_data=self.owner_id, db=db)
        self.owner_user = User.parse_obj(user_data[0])

        resp = self.dict()
        unread_message = []
        unread_count = 0
        if self.status == 'delete':
            pass
        else:
            msg_data = await conn.get_users_unread_messages(db=db, chat_id=self.chat_id)
            unread_count = (await conn.get_users_unread_messages_count(db=db, chat_id=self.chat_id))[0][0]
            for one in msg_data:
                msg = Message.parse_obj(one)
                unread_message.append(msg.dict())

        resp.pop('owner_id')
        resp['unread_message'] = unread_message
        resp['unread_count'] = unread_count
        return resp


class Message(BaseModel):
    """
    msg_type: Может принимать значения 'new_message', 'system',
    """
    msg_id: int = 0
    client_msg_id: int = 0
    msg_type: str = 'new_message'
    text: str = '0'

    from_id: int = 0
    reply_id: int = 0
    chat_id: int = 0
    file_id: int = 0

    status: str = '0'
    read_date: int = 0
    deleted_date: int = 0
    create_date: int = 0

    def to_dialog(self):
        return {
            "status_code": 200,
            "msg_id": self.msg_id,
            "client_msg_id": self.client_msg_id,
            "msg_type": self.msg_type,
            "text": self.text,
            "from_id": self.from_id,
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
    msg_client_id: int = 0
    msg_type: str = '0'
    body: Message = None

