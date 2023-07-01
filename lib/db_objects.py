import datetime

from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    name: str
    middle_name: str
    surname: str
    phone: int
    email: str
    image_link: str
    description: str
    lang: str
    status: str
    push: str
    last_active: int
    create_date: int


class Message:
    line_id: int = 0
    msg_id: int = 0
    msg_type: str = '0'
    title: str = '0'
    text: str = '0'
    description: str = '0'
    lang: str = '0'
    from_user: User = None
    to_user: User = None
    status: str = '0'
    user_type: str = '0'
    read_date: datetime.datetime = None
    deleted_date: datetime.datetime = None
    create_date: datetime.datetime = None

    def __init__(self, data: dict = None, user_from: dict = None, user_to: dict = None):
        if data is not None:
            self.line_id = data['id']
            self.msg_id = data['msg_id']
            self.msg_type = data['msg_type']
            self.title = data['title']
            self.text = data['text']
            self.description = data['description']
            self.lang = data['lang']
            self.from_user = User(user_from) if user_from is not None else data['from_id']
            self.to_user = User(user_to) if user_to is not None else data['to_id']
            self.status = data['status']
            self.user_type = data['user_type']
            self.read_date: datetime.datetime = data['read_date'] if data['read_date'] is not None else None
            self.deleted_date: datetime.datetime = data['deleted_date'] if data['deleted_date'] is not None else None
            self.create_date: datetime.datetime = data['create_date'] if data['create_date'] is not None else None

    def get_msg_json(self) -> dict:
        return {
            'id': self.line_id,
            'msg_id': self.msg_id,
            'msg_type': self.msg_type,
            'title': self.title,
            'text': self.text,
            'description': self.description,
            'lang': self.lang,
            'from_user': self.from_user.get_user_json() if type(self.from_user) == User else self.from_user,
            'to_user': self.to_user.get_user_json() if type(self.to_user) == User else self.to_user,
            'status': self.status,
            'user_type': self.user_type,
            'read_date': str(self.read_date),
            'deleted_date': str(self.deleted_date),
            'create_date': str(self.create_date)
        }
