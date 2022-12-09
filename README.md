# Курс 6. Курсовая

**Краткое описание задачи**

Данная курсовая работа представляет собой backend-часть для сайта объявлений. 

Backend-часть предполагает реализацию следующего функционала:

- Авторизация и аутентификация пользователей.
- Распределение ролей между пользователями (пользователь и админ).
- Восстановление пароля через электронную почту (не обязательно).
- **CRUD** для объявлений на сайте (админ может удалять или редактировать все объявления, а пользователи только свои).
- Под каждым объявлением пользователи могут оставлять отзывы.
- В заголовке сайта можно осуществлять поиск объявлений по названию.

### Краткое техническое задание и рекомендации по порядку выполнения:

<details><summary><strong>Этап I. Настройка Django-проекта.</strong></summary>

На данном этапе нам предстоит подготовить наш Django-проект к работе.  
Данный этап состоит из трех подзадач:

1. Подключение базы данных **Postgres**.
2. Подключение **CORS headers**.
3. Подключение **Swagger**.
</details>

<details><summary><strong>Этап II. Создание модели юзера. Настройка авторизации и аутентификации.</strong></summary>

<details><summary>Создание модели пользователя.</summary>

 Необходимые поля:

  * first_name — имя пользователя (строка).
  * last_name — фамилия пользователя (строка).
  * phone — телефон для связи (строка).
  * email — электронная почта пользователя (email) **(используется в качестве логина).**
  * role — роль пользователя, доступные значения: user, admin.
  * image - аватарка пользователя
 
</details>

<details><summary>Настройка авторизации и аутентификации.</summary>

На данном этапе мы будем настраивать авторизацию пользователя с помощью библиотеки **simple_jwt**. Подробнее об этом
можно узнать в рекомендациях

</details>

<details><summary>Сброс и восстановление пароля через почту* (необязательно).</summary>

Основная сложность при настройке сброса и восстановления пароля через почту — подключение самого почтового ящика,
через который будет происходить отправка таких сообщений. Как правило, при такой настройке требуется разрешить доступ
неавторизованным приложениям к используемому почтовому ящику — эти настройки обычно находятся в разделе «Безопасность»
на сайтах почтовых сервисов.
В целом логика сброса пароля с использованием Djoser достаточно проста.

1. Юзер отправляет POST-запрос на адрес `/users/reset_password/` с содержанием: 
    
    ```json
    {
        "email": "example@mail.com"
    } 
    ```
    
2. Сервер высылает на почту ссылку вида:
    
    ```html
    "/<url>/{uid}/{token}" # предварительно это настраивается в settings
    ```
    
3. Далее идет работа фронта — из данной ссылки парсится uid и токен, который впоследствии передается в JSON вместе
с новым паролем на адрес `users/reset_password_confirm` — по умолчанию он выглядит именно так.
А содержание POST-запроса, отправляемого на бэкэнд, выглядит следующим образом:
    
    ```json
    {
        "uid": "uid",
        "token": "token",
        "new_password": "P4$$W0RD"
    }
    ```

</details>

</details>

<details><summary><strong>Этап III. Описание моделей объявлений и отзывов.</strong></summary>

Модель **объявления** должна содержать следующие поля:

- title — название товара.
- price — цена товара (целое число).
- description — описание товара.
- author — пользователь, который создал объявление.
- created_at — время и дата создания объявления.

*Все записи при выдаче должны быть отсортированы по дате создания 
(чем новее, тем выше).*

Модель **отзыва** должна содержать следующие поля:

- text — текст отзыва.
- author — пользователь, который оставил отзыв.
- ad — объявление, под которым оставлен отзыв.
- created_at - время и дата создания отзыва

</details>

<details><summary><strong>Этап IV. Создание views и эндпоинтов.</strong></summary>

Для получения документации по требуемым эндпоинтам выполните команду `python3 manage.py runserver` в cклонированном
репозитории, откройте браузер и перейдите по адресу:
[http://localhost:8000/api/redoc-tasks/](http://localhost:8000/api/redoc-tasks/)

Задание со звездочкой* (не обязательно)

Также наша работа предусматривает реализацию поиска товаров на главной странице по названию. Для выполнения данного
задания рекомендуем использовать библиотеку `django-filter`. С документацией можно ознакомиться здесь:
[https://django-filter.readthedocs.io/en/stable/guide/install.html](https://django-filter.readthedocs.io/en/stable/guide/install.html).
В рекомендациях есть краткая инструкция по использованию фильтров.

Также обратите внимание на эндпоинты, которые требуют реализации пагинации. Эндпоинт `/ads/` требует не более 4 объектов
на странице (ограничение фронта).

</details>

<details><summary><strong>Этап V. Определение permissions к views.</strong></summary>

**Анонимный пользователь может**:

- получать список объявлений.

**Пользователь может:**

- получать список объявлений,
- получать одно объявление,
- создавать объявление
- редактировать и удалять свое объявление,
- получать список комментариев,
- создавать комментарии,
- редактировать/удалять свои комментарии.

**Администратор может:**

- дополнительно к правам пользователя, редактировать или удалять
объявления и комментарии любых других пользователей.

</details>

---
## Запуск проекта через docker-compose

**Для проверки функционала восстановления пароля пользователя по e-mail, необходимо в файле _.env_ указать параметры
подключения к smtp-серверу.**

Перейти в папку `backend_compose`:
```python
cd backend_compose
```
Выполнить команду:
```python
docker-compouse up --build -d
```
Дождаться, когда статус контейнера `backend_compose-frontend-1` станет _Exited_.  
Фронтенд-часть проекта будет доступна по адресу `localhost:3000` и будет ваимодействовать с бэкенд-сервером.  
Можно переходить к тестированию.  

---
## Запуск проекта через django manage.py

### Установка зависимостей

```python
pip install poetry
poetry install
```
### Создание и запуск образа с PostgreSQL

```python
docker run --name cw_6 -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:12.4-alpine
```

### Миграция таблиц в базу данных

```python
python manage.py migrate
```

### Загрузка фикстур в базу данных

```python
python manage.py loaddata users.json
python manage.py loaddata ads.json
python manage.py loaddata comments.json
```
