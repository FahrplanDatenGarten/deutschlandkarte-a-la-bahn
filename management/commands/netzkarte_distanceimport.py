# -*- coding: utf-8 -*-

import datetime
import statistics

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from pyhafas import HafasClient
from pyhafas.profile import DBProfile

from core.models import (Agency, Source, Stop, StopID, StopIDKind,
                         StopLocation, StopName)

from ...models import Connection


class Command(BaseCommand):
    help = 'Imports the distances between the listed stops'
    stops = [
        8011160,
        8000080,
        8010085,
        8000085,
        8000086,
        8000098,
        8000105,
        8002549,
        8000152,
        8000191,
        8000207,
        8010205,
        8000261,
        8000284,
        8000096,
        8000128,
    ]

    def handle(self, *args, **options):
        client = HafasClient(DBProfile())

        for start in self.stops:
            for end in self.stops:
                if start == end:
                    continue

                journeys = client.journeys(start, end)

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
