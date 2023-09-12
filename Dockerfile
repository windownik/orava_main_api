FROM python:3.11


ENV TZ=Europe/Moscow
RUN apt-get update && apt-get install -yy tzdata
RUN cp /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip3 install aiohttp
RUN pip3 install uvicorn fastapi
RUN pip3 install fastapi-asyncpg
RUN pip3 install python-multipart
RUN pip3 install firebase-admin
RUN pip3 install pillow
RUN pip3 install websockets
RUN pip3 install python-socketio
RUN pip3 install moviepy
RUN pip3 uninstall -y pydantic
RUN pip3 install pydantic==1.10.11


WORKDIR /main/
COPY . /main/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10020"]
