import uuid
from decimal import Decimal
from datetime import datetime
from django.db import models
from django.conf import settings
from rest_framework.exceptions import ValidationError

from api.exceptions import DispenserAlreadyOpenOrClosedException


class BeerTapDispenser(models.Model):
    class BeerTapDispenserStatus(models.TextChoices):
        OPEN = 'open', 'open'
        CLOSED = 'closed', 'closed'

    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4
    )
    flow_volume = models.DecimalField(
        max_digits=5,
        decimal_places=4
    )
    status = models.CharField(
        max_length=8,
        choices=BeerTapDispenserStatus.choices,
        default=BeerTapDispenserStatus.CLOSED,
        editable=False
    )

    class Meta:
        verbose_name = 'Beer Tap Dispenser'
        verbose_name_plural = 'Beer Tap Dispensers'

    def execute_operation(self, status, timestamp):
        """
            Execute the function open or closed of this class and send as parameter the timestamp to each function
            :param status: this attribute contains the status, open or closed
            :param timestamp: this attribute contains when the BeerTapDispenser was opened or closed
            :return: returns nothing
        """
        getattr(self, status)(timestamp=timestamp)

    def set_status(self, status):
        """
            It changes the status of a BeerTapDispenser
            :param status: this attribute contains the status, open or closed
            :return: returns nothing
        """
        self.status = status
        self.save(update_fields=['status'])

    def get_open_choice(self):
        return self.__class__.BeerTapDispenserStatus.OPEN

    def get_closed_choice(self):
        return self.__class__.BeerTapDispenserStatus.CLOSED

    def open(self, timestamp: str):
        """
            Opens a BeerTapDispenser
            :param timestamp: this attribute contains when the BeerTapDispenser was opened
            :return: returns nothing
        """
        if self.status == self.get_open_choice() and self.usages.filter(closed_at__isnull=True).exists():
            raise DispenserAlreadyOpenOrClosedException()

        self.set_status(status=self.get_open_choice())
        self.usages.create(
            opened_at=timestamp,
            flow_volume=self.flow_volume
        )

    def closed(self, timestamp: str):
        """
            Closes a BeerTapDispenser
            :param timestamp: this attribute contains when the BeerTapDispenser was closed
            :return: returns nothing
        """
        last_dispenser_history = self.usages.all().last()
        if self.status == self.get_closed_choice():
            raise DispenserAlreadyOpenOrClosedException()
        elif timestamp > last_dispenser_history.opened_at:
            self.set_status(status=self.get_closed_choice())
            last_dispenser_history.closed_at = timestamp
            last_dispenser_history.save(update_fields=['closed_at'])
        else:
            raise ValidationError({'error': 'updated_at value must be greater than opened_at'})

    def total_spent(self):
        """
            Calculates the total spent, sum all the usages
            :return: returns the total spent
        """
        return round(sum(h.total_spent() for h in self.usages.all()), 3)


class BeerTapDispenserHistory(models.Model):
    dispenser = models.ForeignKey(
        'api.BeerTapDispenser',
        related_name='usages',
        on_delete=models.CASCADE
    )
    opened_at = models.DateTimeField()
    closed_at = models.DateTimeField(
        blank=True,
        null=True
    )
    flow_volume = models.DecimalField(
        max_digits=5,
        decimal_places=4
    )

    class Meta:
        verbose_name = 'Beer Tap Dispenser History'
        verbose_name_plural = 'Beer Tap Dispensers History'
        ordering = ['id']

    def total_spent(self):
        """
            Calculates the total spent of this usage
            :return: returns the total spent
        """
        seconds = self.get_time_difference_in_seconds()
        return round(Decimal(settings.PRICE_BY_LITER) * (self.flow_volume * seconds), 3)

    def get_time_difference_in_seconds(self):
        """
            Calculates the total time between closed_at and opened_at
            :return: returns the difference in seconds
        """
        if self.closed_at:
            # difference between closed and opened at if both are not null
            seconds = (self.closed_at - self.opened_at).seconds
        else:
            now = datetime.now()
            # difference between time now because opened_at is None and  opened_at
            seconds = (now - self.opened_at).seconds
        return seconds

