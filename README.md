# Проект "Foodgram"

## Стек технологий
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=008080)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=56C0C0&color=008080)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/products/docker-hub)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=56C0C0&color=008080)](https://github.com/features/actions)

## Общее описание
Foodgram — это платформа для обмена кулинарными рецептами. Пользователи могут публиковать свои блюда, просматривать рецепты других, а если какой-то вариант понравился — добавить его в «Избранное». Также доступна подписка на авторов, чтобы не пропустить их новые публикации. Для удобства реализована фильтрация рецептов по тегам, что позволяет быстро находить подходящие варианты для завтрака, обеда или ужина. Если пользователь решит приготовить блюдо, он может добавить его в «Список покупок» и затем скачать готовый перечень необходимых ингредиентов с указанными объемами.



## Как развернуть проект локально

1. Клонируйте репозиторий [foodgram](https://github.com/GoarikMkrtchyan/foodgram) с помощью следующей команды:

```bash
git clone git@github.com:GoarikMkrtchyan/foodgram.git
```

3. В локальной директории проекта клонированного репозитория запустите `docker compose` с помощью команды:

```bash
docker compose up -d
```

4. Соберите статические данные и примените миграции с помощью команд:

```bash
docker compose exec backend python manage.py collectstatic
```
```bash
docker compose exec backend python manage.py makemigrations
```
```bash
docker compose exec backend python manage.py migrate
```

5. Загрузите в базу данных начальный набор ингредиентов:
```bash
docker compose exec backend python manage.py add_ingredients
```

6. Приложение будет доступно в браузере по адресу [http://localhost](http://localhost).

---

Проект "Foodgram" доступен по ссылке: [gogoshkafoodgram.zapto.org](gogoshkafoodgram.zapto.org)

Автор проекта: [Гоарик Мкртчян](https://github.com/GoarikMkrtchyan)