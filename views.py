import datetime
import json
import os

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import JsonResponse

from core.models import (Agency, Source, Stop, StopID, StopIDKind,
                         StopLocation, StopName)

from . import STOPS


def convert_toJson(request):
    returnDict = {}

    for stop_id in STOPS:
        stop = Stop.objects.get(stopid__name=stop_id)
        returnDict[stop_id] = {
            'stationID': stop_id,
            'stationName': stop.stopname_set.first().name,
            'duration': {c.stop.get(
                ~Q(id=stop.pk)).stopid_set.first().name: c.duration.total_seconds() for c in stop.connection_set.all()},
            'lat': stop.stoplocation_set.first().latitude if stop.stoplocation_set.count() else 0,
            'lon': stop.stoplocation_set.first().longitude if stop.stoplocation_set.count() else 0,
        }

    return JsonResponse(returnDict, encoder=DjangoJSONEncoder)
