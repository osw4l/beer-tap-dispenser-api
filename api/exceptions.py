from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_409_CONFLICT


class DispenserAlreadyOpenOrClosedException(APIException):
    status_code = HTTP_409_CONFLICT
    default_detail = 'Dispenser is already opened/closed'
    default_code = 'dispenser_conflict'

