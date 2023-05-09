# yamdb_final
[![Django-app workflow](https://github.com/PaulSssar/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/PaulSssar/yamdb_final/actions/workflows/yamdb_workflow.yml)
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 
Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.
Технологии
Python
Django
Django Rest Framework
PostgreSQL
Docker
Docker-Compose
Nginx
Gunicorn
Запуск проекта
Запустите docker-compose:
docker-compose up -d --build
docker-compose up
Создайте новые файлы миграций:
docker-compose exec web python manage.py makemigrations users
docker-compose exec web python manage.py makemigrations reviews
Выполните миграции:
docker-compose exec web python manage.py migrate
Создайте суперпользователя:
docker-compose exec web python manage.py createsuperuser
Соберите статику:
docker-compose exec web python manage.py collectstatic --no-input
Зайдите на http://localhost/admin/ и создайте запись