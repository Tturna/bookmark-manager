FROM debian:bookworm

WORKDIR /app

SHELL ["/bin/bash", "-c"]

RUN apt update && apt upgrade -y && apt install -y python3.11 python3.11-venv
RUN python3.11 -m venv .venv

COPY ./requirements.txt .
COPY ./bookmarkmanager/ .

RUN source .venv/bin/activate && pip install -r requirements.txt

RUN cd bookmarkmanager

CMD source .venv/bin/activate && gunicorn -b '0.0.0.0:5001' bookmarkmanager.wsgi
