import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Genre, Title


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(f'{settings.BASE_DIR}/static/data/genre_title.csv',
                  newline='', encoding='utf-8'
                  ) as file:
            reader = csv.reader(file)
            count = 0
            for row in reader:
                if count > 0:
                    genre = Genre.objects.get(id=row[2])
                    title = Title.objects.get(id=row[1])
                    genre.title_set.add(title)
                count += 1
            self.stdout.write(self.style.SUCCESS('Данные загружены в БД'))
