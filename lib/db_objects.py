import datetime

from fastapi import Depends
from pydantic import BaseModel

from lib.sql_connect import create_user


class Address:
    city: str = '0'
    street: str = '0'
    house: str = '0'
    latitudes: float = 0  # Широта
    longitudes: float = 0  # Долгота

    def __init__(self, data: dict):
        self.city = data['city']
        self.street = data['street']
        self.house = data['house']
        self.latitudes = data['latitudes']
        self.longitudes = data['longitudes']

    def get_address_json(self) -> dict:
        return {
            'city': self.city,
            'street': self.street,
            'house': self.house,
            'latitudes': self.latitudes,
            'longitudes': self.longitudes,
        }


class Work:
    work_type: str = 'clean',
    object_name: str = '0',
    object_size: int = 0,

    def __init__(self, data: dict):
        self.work_type = data['city']
        self.object_name = data['object_name']
        self.object_size = data['house']

    def get_address_json(self) -> dict:
        return {
            'work_type': self.work_type,
            'object_name': self.object_name,
            'object_size': self.object_size,
        }


class User:
    user_id: int = 0
    name: str = '0'
    phone: int = 0
    email: str = '0'
    image_link: str = '0'
    auth_type: str = '0'
    auth_id: int = 0
    description: str = '0'
    lang: str = '0'
    range: int = 1
    address: Address = None
    status: str = '0'
    score: int = 5
    total_score: int = 0
    score_count: int = 0
    last_active: datetime.datetime = None
    create_date: datetime.datetime = None

    def __init__(self, data: dict = None):
        if data is not None:
            self.user_id = data['user_id']
            self.phone = data['phone']
            self.email = data['email']
            self.image_link = data['image_link']
            self.name = data['name']
            self.auth_type = data['auth_type']
            self.auth_id = data['auth_id']
            self.description = data['description']
            self.lang = data['lang']
            self.address = Address(data)
            self.status = data['status']
            self.range = data['range']
            self.score = data['score']
            self.score_count = data['score_count']
            self.total_score = data['total_score']
            self.last_active = data['last_active'] if data['last_active'] is not None else None
            self.create_date = data['create_date'] if data['create_date'] is not None else None

    def get_user_json(self) -> dict:
        return {
            'user_id': self.user_id,
            'phone': self.phone,
            'email': self.email,
            'image_link': self.image_link,
            'name': self.name,
            'auth_type': self.auth_type,
            'auth_id': self.auth_id,
            'description': self.description,
            'lang': self.lang,
            'status': self.status,
            'score': self.score,
            'score_count': self.score_count,
            'total_score': self.total_score,
            'address': self.address.get_address_json(),
            'last_active': str(self.last_active),
            'create_date': str(self.create_date)
        }

    async def create_user(self, db: Depends):
        self.user_id = (await create_user(db=db, phone=self.phone, email=self.email, name=self.name,
                                          auth_type=self.auth_type, auth_id=self.auth_id, description=self.description,
                                          lang=self.lang, city=self.address.city, street=self.address.street,
                                          house=self.address.house, status=self.status, image_link=self.image_link,
                                          latitudes=self.address.latitudes, longitudes=self.address.longitudes))[0][0]


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


class UsersWork(BaseModel):
    work_id: int
    work_type: str
    object_id: int
    object_name_ru: str
    object_name_en: str
    object_name_he: str
    object_size: int


class OrderAddress:
    city: str
    street: str
    house: str
    latitudes: float  # Широта
    longitudes: float  # Долгота

    def from_db(self, data: dict):
        self.city = data['city']
        self.street = data['street']
        self.house = data['house']
        self.latitudes = data['latitudes']
        self.longitudes = data['longitudes']

    def dict(self) -> dict:
        return {
            'city': self.city,
            'street': self.street,
            'house': self.house,
            'latitudes': self.latitudes,
            'longitudes': self.longitudes,
        }


class Review:
    order_id: int
    worker_id: int
    review_text: str
    score: int
    review_status: str
    review_date: datetime.datetime

    def from_db(self, data: dict):
        self.order_id = data['order_id']
        self.worker_id = data['worker_id']
        self.review_text = data['review_text']
        self.score = data['score']
        self.review_status = data['review_status']
        self.review_date = data['review_date']

    def dict(self):
        return {
            'order_id': self.order_id,
            'worker_id': self.worker_id,
            'review_text': self.review_text,
            'score': self.score,
            'review_status': self.review_status,
            'review_date': str(self.review_date)
        }


class OrderComment:
    comment_id: int
    order_id: int
    user_id: int
    title: str
    text: str
    description: str
    create_date: datetime.datetime

    def from_db(self, data: dict):
        self.comment_id = data['id']
        self.order_id = data['msg_id']
        self.user_id = data['from_id']
        self.title = data['title']
        self.text = data['text']
        self.description = data['description']
        self.create_date = data['create_date']

    def dict(self):
        return {
            'comment_id': self.comment_id,
            'order_id': self.order_id,
            'user_id': self.user_id,
            'title': self.title,
            'text': self.review_status,
            'description': self.description,
            'create_date': str(self.review_date)
        }


class Order:
    order_id: int
    creator_id: int
    worker_id: int
    worker: User = None
    customer: User = None
    address: OrderAddress
    object_type_id: int
    object_name_ru: str
    object_name_en: str
    object_name_he: str
    object_size: int
    comment: str
    status: str
    review: Review
    start_work: datetime.datetime
    status_date: datetime.datetime
    create_date: datetime.datetime

    def from_db(self, data: dict, customer_data: dict = None, worker_data: dict = None, ):
        order_address = OrderAddress()
        order_address.from_db(data)

        review = Review()
        review.from_db(data)

        if customer_data is not None:
            customer = User(customer_data)
            self.customer = customer

        if worker_data is not None:
            worker = User(worker_data)
            self.worker = worker

        self.order_id = data['order_id']
        self.creator_id = data['creator_id']
        self.worker_id = data['worker_id']
        self.address = order_address
        self.object_type_id = data['object_type_id']
        self.object_name_ru = data['object_type_name_ru']
        self.object_name_en = data['object_type_name_en']
        self.object_name_he = data['object_type_name_he']
        self.object_size = data['object_size']
        self.comment = data['comment']
        self.status = data['status']
        self.review = review
        self.start_work = data['start_work']
        self.status_date = data['status_date']
        self.create_date = data['create_date']

    def dict(self):
        resp = {
            'order_id': self.order_id,
            'creator_id': self.creator_id,
            'worker_id': self.worker_id,
            'address': self.address.dict(),
            'object_type_id': self.object_type_id,
            'object_name_ru': self.object_name_ru,
            'object_name_en': self.object_name_en,
            'object_name_he': self.object_name_he,
            'object_size': self.object_size,
            'comment': self.comment,
            'status': self.status,
            'review': self.review.dict(),
            'start_work': str(self.start_work),
            'status_date': str(self.status_date),
            'create_date': str(self.create_date),
        }
        if self.customer is not None:
            resp['customer'] = self.customer.get_user_json()

        if self.worker is not None:
            resp['worker'] = self.worker.get_user_json()

        return resp

