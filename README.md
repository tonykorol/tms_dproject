# AutoHUB
____

## Технологии
<div style="display: flex, flex">
    <div style="display: flex; align-items: center; gap: 10px">
        <img src="https://skillicons.dev/icons?i=py"/>
        <a href="https://www.python.org/">Python</a>
    </div><div style="display: flex; align-items: center; gap: 10px">
        <img src="https://skillicons.dev/icons?i=fastapi"/>
        <a href="https://fastapi.tiangolo.com/ru/">FastAPI</a>
    </div><div style="display: flex; align-items: center; gap: 10px">
        <img src="https://skillicons.dev/icons?i=postgres"/>
        <a href="https://www.postgresql.org/">PostgreSQL</a>
    </div><div style="display: flex; align-items: center; gap: 10px">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcReCBn5MIDpd6zlRmxeMr_tVRdWr4-3W28EoA&s" width="50" style="border-radius: 10px"/>
        <a href="https://www.sqlalchemy.org/">SQLAlchemy</a>
    </div><div style="display: flex; align-items: center; gap: 10px">
        <img src="https://docs.celeryq.dev/en/stable/_static/celery_512.png" width="50"/>
        <a href="https://docs.celeryq.dev/en/stable/">Celery</a>
    </div><div style="display: flex; align-items: center; gap: 10px">
        <img src="https://skillicons.dev/icons?i=redis"/>
        <a href="https://redis.io/">Redis</a>
    </div>
</div>

____

## Описание
Данный проект предназначен для сбора объявлений о продаже автомобилей с интернет-площадок.
Он состоит из парсера объявлений и API, для взаимодействия с объявлениями.

Парсер реализован с помощью библиотеки [requests](https://pypi.org/project/requests/).

__API состоит из двух модулей:__
* *users*
Реализован на основе библиотеки [FastAPI_users](https://fastapi-users.github.io/fastapi-users/latest/).
Предоставляет возможности регистрации пользователй и аутентификации с помощью jwt-токена и cookies.


* *publications*
Предоставляет возможность просмотра всех доступных объявлений, просмотра объявления по отдельности,
добавление объявлений в избранное, для дальнейшего мониторинга изменения цен. Реализован скрипт для отправки
уведомлений пользователю в Telegram при изменении цены на модель, которую он добавил в избранное.

____

## База данных
В проекте используется база данных [PostgreSQL](https://www.postgresql.org/).

![](/images/db_structure.png)

____

## Запуск

Для запуска необходимо:
1. Определить переменные окружения

    *Для базы данных:*
    ```
    POSTGRES_DB=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    ```
    *Для приложения:*
    ```
    DB_HOST=db
    DB_PORT=5432
    DB_NAME=postgres
    DB_USER=postgres
    DB_PASS=postgres
    
    REDIS_HOST=redis
    REDIS_PORT=6379
    
    SECRET=secret_key # Для хеширования паролей
    TG_BOT_TOKEN=tg_bot_token # Для отправки уведомлений в телеграм
    ```

2. Установить зависимости:
   ```bash
   pip install poetry
   poetry install
   ```

3. Запустить миграции базы данных
    ```bash
   alembic upgrade head
   ```

4. Запустить сервер:
    ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8088
   ```
   
5. Запустить celery и celery-beat:
    ```bash
    celery -A worker.worker worker -l INFO
    celery -A worker.worker beat -l INFO
    ```
   
После запуска приложения начнется парсинг объявлений с сайтов.
Планировщик Celery запускает парсинг каждый час.
____

## API
![](/images/api_handlers.png)

#### Описание маршрутов
* */api/v1*
  * */auth*
    * **POST** */jwt/login* - аутентификация пользователя
    * **POST** */jwt/logout* - "выход" пользователя
    * **POST** */register* - регистрация нового пользователя
    * **GET** */me* - регистрация нового пользователя
  * */adverts*
    * **GET** */* - получить все публикации
    * **GET** */favorites* - получить все избранные публикации
    * **GET** */favorites/token* - получить токен для телеграм-бота
    * **GET** */{pub_id}* - получить одну публикацию по id
    * **GET** */{pub_id}/price* - получить все цены публикации по id
    * **GET** */{pub_id}/price* - получить все цены публикации по id
    * **POST** */{pub_id}/favorite* - добавить публикацию в избранное
    * **DELETE** */{pub_id}/favorite* - удалить публикацию из избранного

