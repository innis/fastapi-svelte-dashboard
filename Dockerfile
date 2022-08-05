# above python 3.10.5
FROM python:alpine3.16

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

RUN apk add --no-cache build-base 
# inotify-tools
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN apk del build-base

COPY . /code

RUN echo `TZ='Asia/Seoul' date '+%Y-%m-%d_%H:%M:%S_%Z'` > /code/docker.buildtm

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--no-server-header"]
