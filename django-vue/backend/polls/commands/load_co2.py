import csv
from datetime import date
from itertools import islice
from django.conf import settings
from django.core.management.base import BaseCommand
from polls.models import CO2


class Command(BaseCommand):
    help = 'Laod data CO2 file'

    def handle(self, *args, **kwarngs):
        print('------',
        datafile,
        '\n----')
        datafile = settings.BASE_DIR / 'backend' / 'data' /'co2_mm_mlo.csv'
        print(datafile)

        with open(datafile, 'r') as csvfile:
            reader = csv.DictReader(islice(csvfile, 51, None))
            
            for row in reader:
                dt = date(
                    year  = int(row["year"]),
                    month = int(row['month']),
                    day   = 1
                )
                print('load_co2', row)
                CO2.objects.get_or_create(date=dt, average=row['average'])


