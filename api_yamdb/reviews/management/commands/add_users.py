import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(f'{settings.BASE_DIR}/static/data/users.csv', newline='',
                  encoding='utf-8'
                  ) as file:
            reader = csv.reader(file)
            count = 0
            for row in reader:
                if count > 0:
                    User.objects.get_or_create(
                        id=row[0],
                        username=row[1],
                        email=row[2],
                        role=row[3],
                        bio=row[4],
                        first_name=row[5],
                        last_name=row[6],
                    )
                count += 1
            self.stdout.write(self.style.SUCCESS('Данные загружены в БД'))
