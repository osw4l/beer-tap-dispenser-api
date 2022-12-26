from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import BeerTapDispenser
from .serializers import BeerTapDispenserSerializer, DispenserStatusSerializer, SpendingDispenserSerializer


class BeerTapDispenserViewSet(mixins.CreateModelMixin,
                              viewsets.GenericViewSet):
    """
    API endpoint for creating beer tap dispensers
    This endpoint allows just the create operation.
    Args (POST method):
        'flow_volume' -> float: 0.0653 (this is the volume comes out (litres per second))
    Returns:
        [json]: id, flow_volume
    You can see the full json request/response example going to 'http://localhost:4500'
    in swagger documentation.
    """
    serializer_class = BeerTapDispenserSerializer
    queryset = BeerTapDispenser.objects.all()

    @action(
        detail=True,
        methods=['PUT'],
        serializer_class=DispenserStatusSerializer
    )
    def status(self, request, pk=None):
        """
        API endpoint action for update the status of a beer tap dispenser.
        You can see the full json request/response example going to 'http://0.0.0.0:5050/'
        in swagger documentation.
        args (PUT method):
        'status' -> str: 'open' (status must be open or closed)
        'updated_at' -> str: '2022-11-17T20:21:31.082Z' (update_at must be timestamp)
        Returns:
        [json]: status, updated_at
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            timestamp = serializer.validated_data.get('updated_at')
            status = serializer.validated_data.get('status')
            self.get_object().execute_operation(timestamp=timestamp, status=status)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=['GET'],
        serializer_class=SpendingDispenserSerializer
    )
    def spending(self, request, pk=None):
        """
        API endpoint action for getting all of spending data related to a beer tap dispenser.
        You can see the full json request/response example going to 'http://0.0.0.0:5050/'
        in swagger documentation.
        args (GET method):
        'id' -> uuid: 'd2a72ba4-7301-476e-bbb7-47de9b5cbf1e' (this is the uuid for filtering)
        Returns:
        [json]: amount, usages
        """
        beer_tap_dispenser = self.get_object()
        serializer = self.serializer_class(beer_tap_dispenser)
        return Response(serializer.data)

