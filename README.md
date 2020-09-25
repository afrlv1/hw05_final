# hw05_final
Сайт с системой публикации блогов пользователей с возможностью создания постов с загрузкой фотографией.
Добавлена возможность комментировать, подписываться на интересных авторов.
Это будет сайт, на котором можно создать свою страницу. Если на нее зайти, то можно посмотреть все записи автора.
Пользователи смогут заходить на чужие страницы, подписываться на авторов и комментировать их записи.
Автор может выбрать имя и уникальный адрес для своей страницы.
Есть возможность модерировать записи и блокировать пользователей, если начнут присылать спам.
Записи можно группировать в сообщества.

#### Стек технологий
Python 3 Django 2.2, PostgreSQL

#### Технические требования
1) Все необходимые пакеты перечислены в ```requirements.txt```

#### Запуск приложения
1) Установите зависимости из ```requirements.txt```:
    - ```pip install -r requirements.txt```
2) После того как все зависимости установятся и  завершат свою инициализацию, примените все необходимые миграции:
    - ```python manage.py makemigrations```
    - ```python manage.py migrate```
3) Для доступа к панели администратора создайте администратора:
    - ```python manage.py createsuperuser```
4) Запустите приложение:
    - ```python manage.py runserver```
#### ВНИМАНИЕ
Должен быть файл .env. в котором указываются пароли, ссылки на БД, логины.
