import datetime
import json
import os

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

from core import models


def testjson(request):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "./test.json"), 'r') as json_file:
        demoJson = json.load(json_file)

    return JsonResponse(demoJson)


def convert_toJson(request):
    returnDict = {}

    return JsonResponse(returnDict, encoder=DjangoJSONEncoder)
