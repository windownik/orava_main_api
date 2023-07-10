import os

from fastapi import Depends
from fastapi.responses import HTMLResponse

from lib import sql_connect as conn
from lib.sql_connect import data_b, app

ip_server = os.environ.get("IP_SERVER")
ip_port = os.environ.get("PORT_SERVER")

ip_port = 80 if ip_port is None else ip_port
ip_server = "127.0.0.1" if ip_server is None else ip_server


@data_b.on_init
async def initialization(connect):
    # you can run your db initialization code here
    await connect.execute("SELECT 1")


@app.get(path='/create_db', tags=['System'], )
async def init_database(db=Depends(data_b.connection)):
    """Here you can first initialise database"""

    await conn.create_users_chats_table(db)
    await conn.create_all_users_table(db)
    await conn.create_community_table(db)
    await conn.create_all_chats_table(db)
    await conn.create_sms_code_table(db)
    # await conn.create_sending_table(db)
    await conn.create_dialog_table(db)
    await conn.create_token_table(db)
    await conn.create_files_table(db)
    await conn.create_chats_table(db)

    return {"ok": True}


def generate_html_response():
    html_content = """
    <html>
        <head>
            <title>Start page</title>
        </head>
        <body>
            <h2>Documentation for ORAVA app API</h2>
            <p><a href="/docs">Documentation standart</a></p>
            <p><a href="/redoc">Documentation from reDoc</a></p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.get('/', response_class=HTMLResponse, tags=['System'])
async def main_page():
    """main page"""
    return generate_html_response()
