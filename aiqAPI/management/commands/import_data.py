import csv
from django.core.management.base import BaseCommand
from ...models import PowerPlantModel, StateModel

class Command(BaseCommand):
    help = 'Import power plant data from CSV'

    def handle(self, *args, **options):
        with open('/Users/mukulkadyan/Desktop/aiq/powerplants.csv', 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                PowerPlantModel.objects.create(
                    plant_name=row['PNAME'],
                    plant_state=row['PSTATABB'],
                    latitude=row['LAT'],
                    longitude=row['LON'],
                    annual_net_generation=row['GENNTAN']
                )
        self.stdout.write(self.style.SUCCESS('Power plant data imported successfully'))

        with open('/Users/mukulkadyan/Desktop/aiq/states.csv', 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                StateModel.objects.create(
                    state_name=row['PSTATABB'],
                    state_annual_net_generation=row['TOTALGENNTAN']
                )
        self.stdout.write(self.style.SUCCESS('States data imported successfully'))
