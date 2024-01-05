#### Автор [kiber-king](https://github.com/kiber-king)

# Foodgram
http://foodleb.ddns.net
Foodgram - это онлайн-платформа, которая позволяет пользователям выкладывать рецепты с фотографиями, составлять список покупок на основе выбранных рецептов и добавлять их в избранное.

## Технологии

- Docker
- Git
- Python
- PostgreSQL
- Gunicorn
- Nginx

## Установка

1. Установите Docker на свой компьютер, если его еще нет.
2. Склонируйте репозиторий с помощью Git:


git clone https://github.com/kiber-king/foodgram-project-react.git


3. Перейдите в папку проекта:


cd foodgram


4. Создайте файл .env и заполните его следующими переменными окружения:


DB_NAME=foodgram
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=db
DB_PORT=5432
SECRET_KEY=your_secret_key


5. Запустите Docker Compose:


docker-compose up -d --build


6. Примените миграции:


docker compose exec -T backend python manage.py migrate


7. Создайте суперпользователя:


docker-compose exec -T python manage.py createsuperuser


8. Соберите статические файлы:


docker-compose exec -T python manage.py collectstatic --no-input


9. Загрузите :


docker-compose exec -t python manage.py 


10. Откройте приложение в браузере по адресу http://localhost.

## Использование

1. Зарегистрируйтесь на сайте или войдите под своей учетной записью.
2. Добавьте рецепты, указав название, описание, ингредиенты и приложив фотографию.
3. Просматривайте рецепты других пользователей и добавляйте их в избранное.
4. Создавайте список покупок на основе выбранных рецептов.
5. Планируйте свои приемы пищи, выбирая нужные рецепты и добавляя их в список покупок.

## Вклад

Если вы хотите внести свой вклад в развитие проекта, вы можете создать новую ветку с вашими изменениями и отправить Pull Request. Будем рады рассмотреть ваши предложения и улучшения.
