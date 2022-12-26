import factory
from datetime import datetime, timedelta
from decimal import Decimal
from .models import BeerTapDispenser, BeerTapDispenserHistory


class BeerTapDispenserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BeerTapDispenser
        django_get_or_create = ('flow_volume',)

    flow_volume = Decimal('0.0653')


class BeerTapDispenserHistoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BeerTapDispenserHistory
        django_get_or_create = ('dispenser', 'flow_volume', 'opened_at', 'closed_at')

    dispenser = factory.SubFactory(BeerTapDispenserFactory)
    flow_volume = Decimal('0.0653')
    opened_at = datetime.now()
    closed_at = opened_at + timedelta(seconds=10)

