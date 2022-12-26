import time
from django.conf import settings
from datetime import datetime
from decimal import Decimal
from django.db.utils import IntegrityError
from django.test import TestCase

from api.exceptions import DispenserAlreadyOpenOrClosedException
from api.factory import BeerTapDispenserFactory
from api.models import BeerTapDispenser, BeerTapDispenserHistory


class BeerTapDispenserTest(TestCase):
    def setUp(self) -> None:
        self.dispenser = BeerTapDispenserFactory()

    def test_create_beer_tap_dispenser_success(self):
        """
            This test creates a new BeerTapDispenserFactory with a default value
        """
        flow_volume = Decimal(1.2345)
        dispenser = BeerTapDispenserFactory.build(flow_volume=flow_volume)
        self.assertEqual(flow_volume, dispenser.flow_volume)

    def test_create_beer_tap_dispenser_fail(self):
        """
            This test try to create a new BeerTapDispenser
            we expect that fails, because
            the flow_volume attribute is required
            to create a new BeerTapDispenser instance
        """
        try:
            BeerTapDispenser.objects.create()
            self.fail()
        except Exception as e:
            self.assertIsInstance(e, IntegrityError)

    def operation_tab_dispenser(self, **kwargs):
        """
            **kwargs contains this structure
            kwargs = {
                'usages_before': 1, # usages counter before start operations
                'usages_after': 1,  # usages counter after start operations
                'operation': 'closed', # operation is closed or open method that receive a timestamp as parameter
                'attribute': 'closed_at' # attribute is closed or open method that receive a timestamp as parameter
            }
            this function contains dynamic attributes because we need to reuse code
        """
        usages = self.dispenser.usages.all()
        # counting usages before start tests
        self.assertEqual(usages.count(), kwargs.get('usages_before'))

        time.sleep(1)

        now = datetime.now()
        # this line call the open or closed method BeerTapDispenser
        getattr(self.dispenser, kwargs.get('operation'))(timestamp=now)
        # counting usages after start tests
        self.assertEqual(usages.count(), kwargs.get('usages_after'))

        last_usage = self.dispenser.usages.all().last()
        # timestamp_attr: represents opened_at or closed_at
        timestamp_attr = getattr(last_usage, kwargs.get('attribute'))
        # this line is comparing the timestamp of the opened_at or closed_at attribute is the same than now
        self.assertEqual(timestamp_attr, now)

    def test_open_tab_dispenser_success(self):
        # the dispenser must start closed
        self.assertEqual(self.dispenser.status, BeerTapDispenser.BeerTapDispenserStatus.CLOSED)
        open_data = dict(usages_before=0, usages_after=1, operation='open', attribute='opened_at')
        self.operation_tab_dispenser(**open_data)

    def test_open_tab_dispenser_fail(self):
        # the dispenser must start closed
        self.assertEqual(self.dispenser.status, BeerTapDispenser.BeerTapDispenserStatus.CLOSED)
        open_data = dict(usages_before=0, usages_after=1, operation='open', attribute='opened_at')
        self.operation_tab_dispenser(**open_data)

        try:
            open_data = dict(usages_before=1, usages_after=1, operation='open', attribute='opened_at')
            self.operation_tab_dispenser(**open_data)
            self.fail()
        except DispenserAlreadyOpenOrClosedException:
            self.assertTrue(True)

    def test_close_tab_dispenser_success(self):
        # the dispenser must start closed
        self.assertEqual(self.dispenser.status, BeerTapDispenser.BeerTapDispenserStatus.CLOSED)

        open_data = dict(usages_before=0, usages_after=1, operation='open', attribute='opened_at')
        self.operation_tab_dispenser(**open_data)
        # the dispenser must be open at this point
        self.assertEqual(self.dispenser.status, BeerTapDispenser.BeerTapDispenserStatus.OPEN)

        close_data = dict(usages_before=1, usages_after=1, operation='closed', attribute='closed_at')
        self.operation_tab_dispenser(**close_data)
        # the dispenser must be closed after finish
        self.assertEqual(self.dispenser.status, BeerTapDispenser.BeerTapDispenserStatus.CLOSED)

    def test_close_tab_dispenser_fail(self):
        # the dispenser must start closed
        self.assertEqual(self.dispenser.status, BeerTapDispenser.BeerTapDispenserStatus.CLOSED)

        open_data = dict(usages_before=0, usages_after=1, operation='open', attribute='opened_at')
        self.operation_tab_dispenser(**open_data)
        # the dispenser must be open at this point
        self.assertEqual(self.dispenser.status, BeerTapDispenser.BeerTapDispenserStatus.OPEN)

        close_data = dict(usages_before=1, usages_after=1, operation='closed', attribute='closed_at')
        self.operation_tab_dispenser(**close_data)
        # the dispenser must be closed after finish
        self.assertEqual(self.dispenser.status, BeerTapDispenser.BeerTapDispenserStatus.CLOSED)

        try:
            # it must fail because is already closed
            close_data = dict(usages_before=1, usages_after=1, operation='closed', attribute='closed_at')
            self.operation_tab_dispenser(**close_data)
            self.fail()
        except DispenserAlreadyOpenOrClosedException:
            self.assertTrue(True)

    def test_calculate_total_spent(self):
        # the dispenser must start closed
        self.assertEqual(self.dispenser.status, BeerTapDispenser.BeerTapDispenserStatus.CLOSED)

        open_data = dict(usages_before=0, usages_after=1, operation='open', attribute='opened_at')
        self.operation_tab_dispenser(**open_data)

        close_data = dict(usages_before=1, usages_after=1, operation='closed', attribute='closed_at')
        self.operation_tab_dispenser(**close_data)

        # the dispenser must be closed after finish
        self.assertEqual(self.dispenser.status, BeerTapDispenser.BeerTapDispenserStatus.CLOSED)

        total_spent_dispenser = sum(d.total_spent() for d in self.dispenser.usages.all())

        self.assertIsNot(total_spent_dispenser, 0)
        self.assertGreaterEqual(total_spent_dispenser, Decimal('0.7999'))

        total_spent_last = self.dispenser.usages.first().total_spent()
        self.assertEqual(total_spent_last, total_spent_dispenser)


class BeerTapDispenserHistoryTest(TestCase):
    def setUp(self) -> None:
        self.dispenser = BeerTapDispenserFactory()

    def test_history_count(self):
        self.dispenser.open(timestamp=datetime.now())
        items = BeerTapDispenserHistory.objects.all().count()
        self.assertEqual(items, 1)

    def test_total_spent_still_open(self):
        self.dispenser.open(timestamp=datetime.now())
        items = BeerTapDispenserHistory.objects.all()

        self.assertEqual(items.count(), 1)
        self.assertEqual(items.first().closed_at, None)

        total_spent_dispenser = sum(d.total_spent() for d in self.dispenser.usages.all())
        total_spent_usage = items.first().total_spent()

        self.assertEqual(total_spent_dispenser, total_spent_usage)

    def test_flow_volume_are_equals(self):
        self.dispenser.open(timestamp=datetime.now())
        items = BeerTapDispenserHistory.objects.all()
        usage = items.first()
        self.assertEqual(usage.flow_volume, self.dispenser.flow_volume)

    def test_get_time_difference_in_seconds_open(self):
        self.dispenser.open(timestamp=datetime.now())
        items = BeerTapDispenserHistory.objects.all()
        usage = items.first()

        time.sleep(3)
        self.assertEqual(usage.get_time_difference_in_seconds(), 3)
        self.assertEqual(items.first().closed_at, None)

    def test_total_spent_closed(self):
        self.dispenser.open(timestamp=datetime.now())
        items = BeerTapDispenserHistory.objects.all()
        self.assertEqual(items.count(), 1)

        seconds = 3
        time.sleep(seconds)

        now = datetime.now()
        self.dispenser.closed(timestamp=now)
        self.assertIsNot(items.first().closed_at, now)

        total_spent_dispenser = sum(d.total_spent() for d in self.dispenser.usages.all())
        total_spent_usage = items.first().total_spent()

        spent = round(Decimal(settings.PRICE_BY_LITER) * (items.first().flow_volume * seconds), 3)
        self.assertGreaterEqual(spent, total_spent_usage)
        self.assertEqual(total_spent_dispenser, total_spent_usage)


