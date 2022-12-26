import uuid
from datetime import datetime, timedelta
from decimal import Decimal

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from api.factory import BeerTapDispenserFactory
from api.models import BeerTapDispenser, BeerTapDispenserHistory


class BeerTapDispenserViewSetTest(APITestCase):
    def setUp(self) -> None:
        self.create_url = reverse('api:beertapdispenser-list')
        self.status_url = 'api:beertapdispenser-status'
        self.spending_url = 'api:beertapdispenser-spending'
        self.flow_volume_data = {'flow_volume': 0.0653}
        self.open_data = {
            'status': 'open',
            'updated_at': '2022-01-01T02:00:00'
        }
        self.closed_data = {
            'status': 'closed',
            'updated_at': '2022-01-01T02:00:50'
        }

    def send_status_request(self, data: dict, pk: str):
        status_url = reverse(self.status_url, kwargs={'pk': pk})
        return self.client.put(status_url, data=data, format='json')

    def open_tap_dispenser(self, btd: BeerTapDispenserFactory):
        return self.send_status_request(data=self.open_data, pk=btd.pk)

    def close_tap_dispenser(self, btd: BeerTapDispenserFactory):
        return self.send_status_request(data=self.closed_data, pk=btd.pk)

    def test_create_beer_tap_dispenser_success(self):
        response = self.client.post(self.create_url, data=self.flow_volume_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        btd = BeerTapDispenser.objects.all().first()
        self.assertEqual(str(btd.id), response.data.get('id'))
        self.assertEqual(btd.flow_volume, response.data.get('flow_volume'))
        self.assertEqual(btd.status, btd.BeerTapDispenserStatus.CLOSED)

    def test_create_beer_tap_dispenser_fail_wrong_number(self):
        data = {'flow_volume': 123.123}
        response = self.client.post(self.create_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('flow_volume')[0], 'Ensure that there are no more than 5 digits in total.')

    def test_create_beer_tap_dispenser_fail_empty_data(self):
        data = {}
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data.get('flow_volume')[0]), 'This field is required.')

    def test_status_open_success(self):
        btd = BeerTapDispenserFactory()
        response = self.open_tap_dispenser(btd=btd)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.open_data)

    def test_status_open_fail(self):
        btd = BeerTapDispenserFactory()
        response = self.open_tap_dispenser(btd=btd)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.open_data)

        # open request again
        response = self.open_tap_dispenser(btd=btd)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data.get('detail'), 'Dispenser is already opened/closed')

    def test_status_closed_success(self):
        btd = BeerTapDispenserFactory()
        response = self.open_tap_dispenser(btd=btd)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.open_data)

        response = self.close_tap_dispenser(btd=btd)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.closed_data)

    def test_status_closed_fail(self):
        btd = BeerTapDispenserFactory()

        response = self.open_tap_dispenser(btd=btd)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.open_data)

        response = self.close_tap_dispenser(btd=btd)
        self.assertEqual(response.data, self.closed_data)

        response = self.close_tap_dispenser(btd=btd)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data.get('detail'), 'Dispenser is already opened/closed')

    def test_status_closed_fail_closed_at_lte_updated_at(self):
        btd = BeerTapDispenserFactory()

        response = self.open_tap_dispenser(btd=btd)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.open_data)

        closed_data = {
            'status': 'closed',
            'updated_at': '2022-01-01T01:00:50'
        }

        response = self.send_status_request(data=closed_data, pk=btd.pk)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('error'), 'updated_at value must be greater than opened_at')

    def test_spending_success(self):
        btd = BeerTapDispenserFactory()
        url = reverse(self.spending_url, kwargs={'pk': btd.pk})
        response = self.client.get(url, data=self.open_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('usages')), btd.usages.count())
        self.assertEqual(response.data.get('amount'), btd.total_spent())

    def test_spending_fail(self):
        url = reverse(self.spending_url, kwargs={'pk': str(uuid.uuid4())})
        response = self.client.get(url, data=self.open_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get('detail'), 'Not found.')

    def test_spending_success_usage_open(self):
        # create dispenser
        btd = BeerTapDispenser.objects.create(flow_volume=0.0654)

        now = datetime.now()
        first_now = now - timedelta(hours=1)

        # records similar to api example -> https://shorturl.at/afyBM
        usages = [
            BeerTapDispenserHistory(
                dispenser=btd,
                opened_at=first_now,
                closed_at=first_now + timedelta(seconds=50),
                flow_volume=btd.flow_volume
            ),
            BeerTapDispenserHistory(
                dispenser=btd,
                opened_at=first_now + timedelta(minutes=8),
                closed_at=first_now + timedelta(minutes=8, seconds=22),
                flow_volume=btd.flow_volume),
            BeerTapDispenserHistory(
                dispenser=btd,
                opened_at=now,
                closed_at=None,
                flow_volume=btd.flow_volume
            ),
        ]

        # creating bulk usages
        btd.usages.bulk_create(usages)

        self.assertEqual(btd.usages.count(), len(usages))
        self.assertEqual(btd.usages.count(), len(usages))

        url = reverse(self.spending_url, kwargs={'pk': btd.pk})
        response = self.client.get(url, data=self.open_data, format='json')

        self.assertEqual(len(response.data.get('usages')), btd.usages.count())
        self.assertEqual(response.data.get('amount'), Decimal('57.683'))

        # check if any element contains closed_at = None
        any_value_contains = any(u.get('closed_at') is None for u in response.data.get('usages'))
        self.assertTrue(any_value_contains)
