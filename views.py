import datetime
import json
import os

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import JsonResponse

from core.models import (Agency, Source, Stop, StopID, StopIDKind,
                         StopLocation, StopName)
from .models import Connection

from . import STOPS


def convert_toJson(request):
    returnDict = {
        'connections': {}
    }

    for stop_id in STOPS:
        stop = Stop.objects.get(stopid__name=stop_id)
        returnDict['connections'][stop_id] = {
            'stationID': stop_id,
            'stationName': stop.stopname_set.first().name,
            'duration': {c.stop.get(
                ~Q(id=stop.pk)).stopid_set.first().name: c.duration.total_seconds() for c in stop.connection_set.all()},
            'lat': stop.stoplocation_set.first().latitude if stop.stoplocation_set.count() else 0,
            'lon': stop.stoplocation_set.first().longitude if stop.stoplocation_set.count() else 0,
        }

    returnDict['lines'] = {'nodes': [], 'links': []}
    for _, value in returnDict['connections'].items():
        returnDict['lines']['nodes'].append(
            {'id': value['stationName'], 'group': 1})
        for stop_id, duration in value['duration'].items():
            returnDict['lines']['links'].append(
                {
                    'source': [
                        value['lat'],
                        value['lon']],
                    'target': [
                        returnDict['connections'][stop_id]['lat'],
                        returnDict['connections'][stop_id]['lon']],
                    'duration': duration})

    return JsonResponse(returnDict, encoder=DjangoJSONEncoder)


def d3_tree(request):
    returnDict = {
        'stations': [],
        'connections': []
    }

    for stop_id in STOPS:
        stop = Stop.objects.get(stopid__name=stop_id)
        loc = [
            stop.stoplocation_set.first().longitude if stop.stoplocation_set.count() else 0,
            stop.stoplocation_set.first().latitude if stop.stoplocation_set.count() else 0,
        ]

        returnDict['stations'].append({
            'name': stop.stopname_set.first().name,
            'location': loc}
        )

        for next_stop_id in STOPS:
            if next_stop_id == stop_id:
                continue

            next_stop = Stop.objects.get(stopid__name=next_stop_id)
            next_loc = [
                next_stop.stoplocation_set.first().longitude if next_stop.stoplocation_set.count() else 0,
                next_stop.stoplocation_set.first().latitude if next_stop.stoplocation_set.count() else 0,
            ]

            duration = Connection.objects.filter(
                stop=stop).filter(
                stop=next_stop).first().duration.total_seconds() if Connection.objects.filter(
                stop=stop).filter(
                stop=next_stop).count() else 0

            returnDict['connections'].append({
                'link': [
                    loc,
                    next_loc
                ],
                'duration': duration
            })

    return JsonResponse(returnDict, encoder=DjangoJSONEncoder)
