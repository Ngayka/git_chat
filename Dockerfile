FROM python:3.13-slim
LABEL maintainer="ngayka@gmail.com"

WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY . .

RUN mkdir -p /vol/web/media

RUN adduser \
    --disabled-password \
    --no-create-home \
    django-user

RUN chown -R django-user:django-user /vol/
RUN chmod -R 755 /vol/web/
RUN ln -snf /usr/share/zoneinfo/Europe/Kyiv /etc/localtime && \
    echo "Europe/Kyiv" > /etc/timezone

USER django-user