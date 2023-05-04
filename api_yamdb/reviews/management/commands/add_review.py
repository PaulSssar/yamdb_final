import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Review, Title

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(f'{settings.BASE_DIR}/static/data/review.csv', newline='',
                  encoding='utf-8'
                  ) as file:
            reader = csv.reader(file)
            count = 0
            for row in reader:
                if count > 0:
                    Review.objects.get_or_create(
                        id=row[0],
                        text=row[2],
                        author=User.objects.get(id=row[3]),
                        score=row[4],
                        pub_date=row[5],
                        title=Title.objects.get(id=row[1])
                    )
                count += 1
            self.stdout.write(self.style.SUCCESS('Данные загружены в БД'))
