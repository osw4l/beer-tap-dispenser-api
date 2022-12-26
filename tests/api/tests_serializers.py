from datetime import timedelta
from decimal import Decimal
from django.test import TestCase
from django.forms.models import model_to_dict
from rest_framework.exceptions import ErrorDetail

from api.factory import BeerTapDispenserHistoryFactory, BeerTapDispenserFactory
from api.models import BeerTapDispenser
from api.serializers import (
    BeerTapDispenserSerializer,
    DispenserStatusSerializer,
    SpendingDispenserSerializer,
    BeerTapDispenserHistorySerializer
)


class BeerTapDispenserSerializerTests(TestCase):
    def setUp(self) -> None:
        self.serializer_class = BeerTapDispenserSerializer

    def test_serializer_class_success_data(self):
        data = {'flow_volume': Decimal('0.0653')}
        serializer = self.serializer_class(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(data, serializer.data)

    def test_serializer_class_fail_data(self):
        data = {}
        serializer = self.serializer_class(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(str(serializer.errors.get('flow_volume')[0]), 'This field is required.')
        self.assertIsInstance(serializer.errors.get('flow_volume')[0], ErrorDetail)

    def test_serializer_class_wrong_number_data(self):
        data = {'flow_volume': 123.123}
        serializer = self.serializer_class(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors.get('flow_volume')[0], 'Ensure that there are no more than 5 digits in '
                                                                  'total.')
        self.assertIsInstance(serializer.errors.get('flow_volume')[0], ErrorDetail)

    def test_serializer_class_save_data(self):
        data = {'flow_volume': Decimal('0.0653')}
        serializer = self.serializer_class(data=data)
        self.assertTrue(serializer.is_valid())

        serializer_instance = serializer.save()
        tap_dispenser = BeerTapDispenser.objects.all().first()

        self.assertEqual(serializer_instance, tap_dispenser)
        self.assertEqual(serializer_instance.id, tap_dispenser.id)
        self.assertEqual(serializer_instance.flow_volume, tap_dispenser.flow_volume)


class DispenserStatusSerializerTest(TestCase):
    def setUp(self) -> None:
        self.serializer_class = DispenserStatusSerializer

    def test_serializer_class_success_data(self):
        data = {
            'status': BeerTapDispenser.BeerTapDispenserStatus.OPEN,
            'updated_at': '2022-11-17T19:00:50'
        }
        serializer = self.serializer_class(data=data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(data, serializer.data)

    def test_serializer_class_wrong_date(self):
        data = {
            'status': BeerTapDispenser.BeerTapDispenserStatus.OPEN,
            'updated_at': 'XX22-11-17T19:00:50'
        }
        serializer = self.serializer_class(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIsNotNone(serializer.errors.get('updated_at'))
        self.assertEqual(len(serializer.errors.get('updated_at')), 1)
        msg = 'Datetime has wrong format. Use one of these formats instead: Y' \
              'YYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].'
        self.assertEqual(serializer.errors.get('updated_at')[0], msg)

    def test_serializer_class_wrong_status(self):
        data = {
            'status':  'wrong',
            'updated_at': '2022-11-17T19:00:50'
        }
        serializer = self.serializer_class(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIsNotNone(serializer.errors.get('status'))
        self.assertEqual(len(serializer.errors.get('status')), 1)
        self.assertEqual(serializer.errors.get('status')[0], '"wrong" is not a valid choice.')

    def test_serializer_class_wrong_status_and_date(self):
        data = {
            'status':  'wrong',
            'updated_at': 'XX2020-11-17T19:00:50'
        }
        serializer = self.serializer_class(data=data)

        self.assertFalse(serializer.is_valid())

        self.assertIsNotNone(serializer.errors.get('updated_at'))
        self.assertEqual(len(serializer.errors.get('updated_at')), 1)
        msg = 'Datetime has wrong format. Use one of these formats instead: Y' \
              'YYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].'
        self.assertEqual(serializer.errors.get('updated_at')[0], msg)

        self.assertIsNotNone(serializer.errors.get('status'))
        self.assertEqual(len(serializer.errors.get('status')), 1)
        self.assertEqual(serializer.errors.get('status')[0], '"wrong" is not a valid choice.')


class BeerTapDispenserHistorySerializerTest(TestCase):
    def setUp(self) -> None:
        self.serializer_class = BeerTapDispenserHistorySerializer
        self.dispenser = BeerTapDispenserFactory()

    def test_serializer_data_success(self):
        instance = BeerTapDispenserHistoryFactory(dispenser=self.dispenser)
        data = model_to_dict(instance)
        serializer = self.serializer_class(data=data)

        self.assertEqual(self.dispenser.usages.all().count(), 1)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(instance.flow_volume, serializer.validated_data.get('flow_volume'))
        self.assertEqual(instance.opened_at, serializer.validated_data.get('opened_at'))
        self.assertEqual(instance.closed_at, serializer.validated_data.get('closed_at'))

        close_time = serializer.validated_data.get('opened_at') + timedelta(seconds=10)
        self.assertEqual(close_time, serializer.validated_data.get('closed_at'))

        self.assertEqual(instance.dispenser, self.dispenser)
        self.assertEqual(self.dispenser.total_spent(), instance.total_spent())


class SpendingDispenserSerializerTest(TestCase):
    def setUp(self) -> None:
        self.serializer_class = SpendingDispenserSerializer
        self.dispenser = BeerTapDispenserFactory()
        self.usages = [BeerTapDispenserHistoryFactory(dispenser=self.dispenser)]

    def test_serializer_success(self):
        serializer = self.serializer_class(self.dispenser)
        parsed_usages = serializer.data.get('usages')

        self.assertEqual(len(parsed_usages), 1)
        usages = BeerTapDispenserHistorySerializer(self.usages, many=True)
        self.assertEqual(serializer.data.get('usages'), usages.data)

        self.assertEqual(serializer.data.get('amount'), self.dispenser.total_spent())

        total_usages_serializer = sum(usage.get('total_spent') for usage in serializer.data.get('usages'))
        self.assertEqual(total_usages_serializer, self.dispenser.total_spent())

