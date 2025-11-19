from django.utils.dateparse import parse_date
import datetime
from django.http import JsonResponse
# from webservices.models import *
from django.http import Http404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.parsers import JSONParser
from rest_framework import generics
from django.db import connection
from itertools import chain
import json, base64 , ast
import time
import requests
import random
from django.db.models import Avg
import os
import socket
import urllib.request
from django.contrib.auth import get_user_model
from io import BytesIO
import json
# from datetime import datetime, timedelta
from mimetypes import MimeTypes
import urllib
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
import re
from django.apps import apps
from django.views import View
import requests
import json
from db_table.models import *
from webservices.views.constants import *
from webservices.views.bitfairapi import *
from webservices.views.BitfairLib import *
import redis
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from webservices.serializers import *

import datetime
import re
from django.db.models import Q

def str_to_date(str_date):
    match = re.search("\d{2}/\d{2}/\d{4}", str_date)
    obj_date = datetime.datetime.strptime(match.group(), "%d/%m/%Y").date()
    return obj_date

def testRapid():
    #get Fixture 50 fixture upcomming
    # import requests

    # url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

    # querystring = {"next":"50"}

    # headers = {
    # 'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
    # 'x-rapidapi-key': "ece33c90acmshe7a66df0ed99d01p1c7462jsnb1d8cfacb8fc"
    # }

    # response = requests.request("GET", url, headers=headers, params=querystring)

    # print(response.text)
    

    #Get League
    import requests

    url = "https://api-football-v1.p.rapidapi.com/v3/leagues"
    headers = {
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
    'x-rapidapi-key': "ece33c90acmshe7a66df0ed99d01p1c7462jsnb1d8cfacb8fc"
    }
    response = requests.request("GET", url, headers=headers)
    print(response.text)

    #Fixture by League
    # import requests

    # url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

    # querystring = {"league":"39","season":"2021"}

    # headers = {
    # 'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
    # 'x-rapidapi-key': "ece33c90acmshe7a66df0ed99d01p1c7462jsnb1d8cfacb8fc"
    # }

    # response = requests.request("GET", url, headers=headers, params=querystring)

    # print(response.text)
    res =json.dumps(json.loads(response.text))
    return res
def getFxtureByLeagueRAPIDAPI(league_id,season):
    import requests
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"league":league_id,"season":season}
    headers = {
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
        'x-rapidapi-key': "ece33c90acmshe7a66df0ed99d01p1c7462jsnb1d8cfacb8fc"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    # print(response.text)
    res =json.dumps(json.loads(response.text))
    return res
def getTeamByLeague(league_id):
    import requests
    url = "https://api-football-v1.p.rapidapi.com/v2/teams/league/"+str(league_id)
    headers = {
        'x-rapidapi-host':RAPIDAPI_HOST,
        'x-rapidapi-key': RAPIDAPI_KEY
    }
    response = requests.request("GET", url, headers=headers)
    res =json.dumps(json.loads(response.text))
    return res

def TeamStatisticsByLeagueandSeason(team_id,season_id,league_id):
    import requests
    url = "https://api-football-v1.p.rapidapi.com/v3/teams/statistics"
    querystring = {"league":league_id,"season":season_id,"team":team_id}
    headers = {
        'x-rapidapi-host':RAPIDAPI_HOST,
        'x-rapidapi-key': RAPIDAPI_KEY
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    res =json.dumps(json.loads(response.text))
    return res
def GetFixtureByFixtureId(fixture_id):
    import requests
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"id":str(fixture_id)}
    headers = {
        'x-rapidapi-host':RAPIDAPI_HOST,
        'x-rapidapi-key': RAPIDAPI_KEY
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    res =json.dumps(json.loads(response.text))
    return res