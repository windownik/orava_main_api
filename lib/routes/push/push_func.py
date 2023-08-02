
import firebase_admin
from firebase_admin import messaging
from firebase_admin import credentials

cred = credentials.Certificate("orava-app.json")
firebase_admin.initialize_app(cred)


def send_push(msg_id: int, fcm_token: str, title: str, body: str, data: str, push_type: str):
    message = messaging.Message(
        data={'msg_id': f"{msg_id}",
              'title': title,
              'body': body,
              'data': data,
              'push_type': push_type},
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=fcm_token
    )
    response = messaging.send(message)
