import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category, Title


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(f'{settings.BASE_DIR}/static/data/titles.csv', newline='',
                  encoding='utf-8'
                  ) as file:
            reader = csv.reader(file)
            count = 0
            for row in reader:
                if count > 0:
                    Title.objects.get_or_create(
                        id=row[0],
                        name=row[1],
                        year=row[2],
                        category=Category.objects.get(id=row[3]),
                    )
                count += 1
            self.stdout.write(self.style.SUCCESS('Данные загружены в БД'))
