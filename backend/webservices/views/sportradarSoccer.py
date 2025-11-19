from django.http import HttpResponse
from django.conf.urls import include, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from db_table.models import Players
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.contrib.auth import get_user_model, login
from django.db.models import Q
import json
from django.http import JsonResponse
from rest_framework.response import Response
#import urllib.request
from django.views.decorators.cache import cache_page
from django.core.cache import cache
import random
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ParseError
import hashlib
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from webservices.views.BitfairLib import *
from webservices.views.LibGoalServeAPI import *
from webservices.views.bitfairapi import *
from webservices.views.constants import *

from datetime import datetime
from django.views import View
from django.views import generic
from webservices.serializers import *
from db_table.models import *
import re
import redis
from datetime import datetime, timedelta
from BetfairUpdater.SoccerCalculation import *
# from soccer.testData import *
from django.utils.text import slugify 
import random 
import string 
from django.db.models import Q

#Probability And AI
@csrf_exempt
def sportradarMapping(request):
    request_data = JSONParser().parse(request)
    if 'sportsradar_competitor_id' in request_data:
        compitator_id =request_data['sportsradar_competitor_id']
        league = SportsradarMapping.objects.all().filter(sportsradar_competitor_id=compitator_id)
        leagueserializer = SportsradarMappingSerializer(league, many=True)
        data = {"status": 200, "message": "success", "data": leagueserializer.data}
    else:
        league = SportsradarMapping.objects.all()
        leagueserializer = SportsradarMappingSerializer(league, many=True)
        data = {"status": 200, "message": "success", "data": leagueserializer.data}
    return JsonResponse(data)

@csrf_exempt
def sportradarSoccerEloRating(request):
    request_data = JSONParser().parse(request)
    if 'sportsradar_competitor_id' in request_data:
        compitator_id =request_data['sportsradar_competitor_id']
        league = SportsradarSoccerEloRating.objects.all().filter(sportsradar_competitor_id=compitator_id)
        leagueserializer = SportsradarSoccerEloRatingSerializer(league, many=True)
        data = {"status": 200, "message": "success", "data": leagueserializer.data}
    else:
        league = SportsradarSoccerEloRating.objects.all()
        leagueserializer = SportsradarSoccerEloRatingSerializer(league, many=True)
        data = {"status": 200, "message": "success", "data": leagueserializer.data}
    return JsonResponse(data)

@csrf_exempt
def SaveSoccerEloRating(request):
    request_data = JSONParser().parse(request)
    compitator_id = request_data['sportsradar_competitor_id']
    print(compitator_id)
    cnt =  SportsradarSoccerEloRating.objects.filter(sportsradar_competitor_id=compitator_id).count()
    print(cnt)
    if cnt == 0:
        ins = SportsradarSoccerEloRating.objects.create(
            sportsradar_competitor_id=request_data['sportsradar_competitor_id'],
            sportsradar_competitor_short_name = request_data['sportsradar_competitor_short_name'],
            clubelo_team_name = request_data['clubelo_team_name'],
            betfair_team_name = request_data['betfair_team_name'],
            elo_rating= request_data['elo_rating'],
           
        )
    else:
        data = SportsradarSoccerEloRating.objects.get(sportsradar_competitor_id__contains=str(compitator_id))
        data.sportsradar_competitor_short_name = request_data['sportsradar_competitor_short_name']
        data.clubelo_team_name = request_data['clubelo_team_name']
        data.betfair_team_name = request_data['betfair_team_name']
        data.elo_rating= request_data['elo_rating']
        data.save()
        
    data1 = {'status':200, 'message': 'success'}
    return JsonResponse(data1) 

@csrf_exempt
def SportsRaderLiveScore(request):
    final_res = []
    res=redis_instance.get('DailySummery')
    if res:
        final_res=json.loads(res)
    # print(final_res)
    data ={"status": 200, "message": "success", "data":final_res}
    return JsonResponse(data)
@csrf_exempt
def SofaScoreLiveScore(request):
    final_res = []
    res=redis_instance.get('DailySummerySofaScore')
    if res:
        final_res=json.loads(res)
    # print(final_res)
    data ={"status": 200, "message": "success", "data":final_res}
    return JsonResponse(data)
