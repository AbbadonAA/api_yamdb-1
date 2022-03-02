import csv

from django.conf import settings
from django.core.management import BaseCommand

from titcatgen.models import (Category, Genre,
                            Title,)
from users.models import User

TABLES_DICT = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
}


class Command(BaseCommand):
    help = 'Load data from csv files'

    def handle(self, *args, **kwargs):
        for model, base in TABLES_DICT.items():
            with open(
                f'{settings.BASE_DIR}/static/data/{base}',
                'r', encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                model.objects.bulk_create(model(**data) for data in reader)

        self.stdout.write(self.style.SUCCESS('Successfully load data'))