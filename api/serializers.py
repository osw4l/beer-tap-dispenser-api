from rest_framework import serializers
from .models import BeerTapDispenser, BeerTapDispenserHistory


class BeerTapDispenserSerializer(serializers.ModelSerializer):
    """
    Model serializer for BeerTapDispenser
    """
    class Meta:
        model = BeerTapDispenser
        fields = (
            'id',
            'flow_volume',
        )


class DispenserStatusSerializer(serializers.Serializer):
    """
       Serializer for validate the status and updated_at before to use the data on the api
    """
    status = serializers.ChoiceField(
        choices=BeerTapDispenser.BeerTapDispenserStatus.choices
    )
    updated_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    def update(self, instance, validated_data):  # pragma: no cover
        pass

    def create(self, validated_data):  # pragma: no cover
        pass


class BeerTapDispenserHistorySerializer(serializers.ModelSerializer):
    """
       Serializer for show the usages
    """
    class Meta:
        model = BeerTapDispenserHistory
        fields = (
            'opened_at',
            'closed_at',
            'flow_volume',
            'total_spent'
        )


class SpendingDispenserSerializer(serializers.ModelSerializer):
    """
       Serializer for show the usages and the amount
    """
    amount = serializers.ReadOnlyField(source='total_spent')
    usages = BeerTapDispenserHistorySerializer(many=True)

    class Meta:
        model = BeerTapDispenser
        fields = (
            'amount',
            'usages'
        )
