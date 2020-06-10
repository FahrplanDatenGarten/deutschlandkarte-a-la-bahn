# -*- coding: utf-8 -*-

import datetime
import statistics

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from pyhafas import HafasClient
from pyhafas.profile import DBProfile

from core.models import (Agency, Source, Stop, StopID, StopIDKind,
                         StopLocation, StopName)

from ... import STOPS
from ...models import Connection


class Command(BaseCommand):
    help = 'Imports the distances between the listed stops'

    def handle(self, *args, **options):
        client = HafasClient(DBProfile())

        for start in STOPS:
            for end in STOPS:
                if start == end:
                    continue
                journeys = client.journeys(start, end, date=datetime.datetime.now())

                stops = [
                    Stop.objects.get(stopid__name=start),
                    Stop.objects.get(stopid__name=end)
                ]
                cons = Connection.objects.filter(
                    stop=stops[0]).filter(
                    stop=stops[1])

                if len(cons):
                    con = cons[0]
                else:
                    con = Connection()
                    con.save()
                    con.stop.add(*stops)

                con.duration = datetime.timedelta(seconds=statistics.mean(
                    [j.duration.total_seconds() for j in journeys]))
                con.save()
