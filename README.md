# Store Server

The project for study Django.

#### Stack:

- [Python](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)

## Local Developing

Для тех, у кого Windows

##### переход в папку store-server:
$ cd c:\course\store-server\

##### создание виртуального окружения:
$ c:\course\store-server>python -m venv venv
##### активация окружения:
$ c:\course\store-server>venv\Scripts\activate.bat
##### установка зависимостей:
$ (venv) c:\course\store-server>pip install requests
##### команда установки LTS-версии джанги:
$ pip install django==4.2.7 
##### разворачивание папки с проектом
$ django-admin startproject store

##### команда обновления pip для удобства
$ python -m pip install --upgrade pip

##### подключение PostgreSQL (нужна установленная программа)
cd C:\Program Files\PostgreSQL\{version}\bin, где PostgreSQL, установлен

и потом

psql -U postgres

CREATE DATABASE store_db;
CREATE ROLE store_username with password 'store_password';
ALTER ROLE "store_username" WITH LOGIN;
GRANT ALL PRIVILEGES ON DATABASE "store_db" to store_username;
ALTER USER store_username CREATEDB;

##### Чтобы в локальном проекте работало кэширование, нужно установить Redis и запустить его из консоли командой ниже
https://youtu.be/DLKzd3bvgt8?si=ziyZpM_9TSNZlYyv
$ redis-server

##### Для запуска Celery на Windows, для остановки - Ctrl+C 
$ celery -A store worker -l INFO -P solo

