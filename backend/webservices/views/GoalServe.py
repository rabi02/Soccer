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
# from webservices.views.CommonFunction import *
from webservices.views.bitfairapi import *
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
from soccer.scrap import *
from django.db.models import Q

#Probability And AI

@csrf_exempt
def GoalServeAPI(request):
    pdata =[]
    StoreMatch()
    team_data = StoreTeamDetail()
    # StoreSeason()
    # GetLeague()
    # pdata= StorePlayerStatistics()
    # getMatchTest()
    # StoreLiveScoreRedis()
    # StorePredictionSaveBackdata()
    data = {'status':200, 'message': 'success', "data": pdata}
    return JsonResponse(data)

@csrf_exempt
def MatchByLeagueGoalserve(request):
    from django.utils.timezone import datetime #important if using timezones
    today = datetime.today()
    request_data = JSONParser().parse(request)
    league_ids=LeagueIdGolaServe() 
    response = {}
    queryObj = {}
    result =[]
    message=''

    if 'week' in request_data:
        queryObj = {}
        one_week_ago = datetime.today() + timedelta(days=7)
        queryObj['formated_date__gte'] = today.strftime('%Y-%m-%d')
        queryObj['formated_date__lte'] = one_week_ago.strftime('%Y-%m-%d')
        queryObj['league_id__in'] =  league_ids
    if 'popular' in request_data:
        queryObj = {}
        match_id =GetPopularMatch()
        # print(match_id)
        queryObj['match_id__in'] = match_id
    if 'country_id' in request_data:
        queryObj['country_id'] = request_data['country_id']
    
    if 'league_id' in  request_data:
        queryObj = {}
        queryObj['league_id'] = request_data['league_id']
        queryObj['formated_date__contains']= datetime.today().strftime('%Y-%m-%d')
    else:
        queryObj['league_id__in'] =  league_ids
        queryObj['formated_date__contains']= datetime.today().strftime('%Y-%m-%d')

    # result = MatchFixtureUpdateSerializer(fixtures, many=True).data
    print(queryObj)
    fixtures = MatchGoalserve.objects.all().filter(**queryObj)[:15]
    if fixtures:
        result = MatchByTeamGoalserveSerializer(fixtures, many=True).data
    else:
        message = 'Oops! There seems to be no match for today'
        
    data = {"status":200,"message":message,"data":result}

    return JsonResponse(data)

@csrf_exempt
def GetTodayOdds(request):
    league_ids=LeagueIdGolaServe()
    queryObj['league_id__in'] =  league_ids
    queryObj['formated_date']= datetime.today().strftime('%Y-%m-%d')
    fixtures = MatchGoalserve.objects.all().filter(**queryObj)[:10]
    finalres =[]
    for res in fixtures:
        match_name = res.match_name
        prediction=GetPosionDetailFormTeamId(res.localteam_name,res.visitorteam_name)
        pred =json.loads(prediction)
        print("+++++++++++++++++")
        print(pred)
        print("----+++++++++++++----")
        # qr = pred[0]['Predictions']
        qr = ''
        qr0 =0
        qr1=0
        if qr.count("-"):
            qualityQR = qr.split('-')
            qr0 =qualityQR[0]
            qr1 =qualityQR[1]

        # Get Team Standing Value
        # LteamStanding = GetTeamStatisticsAndStandingByTeamId(item['season_id'],item['localteam_id'])
        # VteamStanding = GetTeamStatisticsAndStandingByTeamId(item['season_id'],item['visitorteam_id'])
        # LPreprocess = preprocessdata(LteamStanding)
        # VPreprocess = preprocessdata(VteamStanding)
        # HomeTeamLP = 2
        # AwayTeamLP =5
        predictionOdds = []     # predictionOdds=GetPredictionByMatch(LPreprocess['HTFormPts'],VPreprocess['ATFormPts'],HomeTeamLP,AwayTeamLP,qr0,qr1)

        

        
    data = {"status":200,"message":"success","data":finalres}
    return JsonResponse(data)

@csrf_exempt
def GetSquadByTeam(request):
    requestdata = JSONParser().parse(request)
    team =TeamPlayerSquadGoalserve.objects.filter(team_id=requestdata["team_id"]).all()
    res =[]
    if team:
        res = TeamPlayerSquadGoalserveSerializer(
            TeamPlayerSquadGoalserve.objects.filter(team_id=requestdata["team_id"]).all()
            , many=True).data
    
 
    data = {"status": 200, "message": "success", "data":res}
    return JsonResponse(data)

@csrf_exempt
def GetPlayerInTeam(request):
    requestdata = JSONParser().parse(request)
    team =TeamPlayerTransferINGoalserve.objects.filter(team_id=requestdata["team_id"]).all()
    res =[]
    if team:
        res = TeamPlayerTransferINGoalserveSerializer(
            TeamPlayerTransferINGoalserve.objects.filter(team_id=requestdata["team_id"]).all()
            , many=True).data
 
    data = {"status": 200, "message": "success", "data":res}
    return JsonResponse(data)

@csrf_exempt
def GetPlayerOutTeam(request):
    requestdata = JSONParser().parse(request)
    team =TeamPlayerTransferOUTGoalserve.objects.filter(team_id=requestdata["team_id"]).all()
    res =[]
    if team:
        res = TeamPlayerTransferOutGoalserveSerializer(
            TeamPlayerTransferOUTGoalserve.objects.filter(team_id=requestdata["team_id"]).all()
            , many=True).data
    
    data = {"status": 200, "message": "success", "data":res}
    return JsonResponse(data)

@csrf_exempt
def OvaralTeamPlayerGoalServer(request):
    request_data = JSONParser().parse(request)
    response = {}
    result = []
    team_ids =[]
    fixer = MatchGoalserve.objects.filter(\
        (Q(localteam_id=request_data['team_id']) | Q(visitorteam_id=request_data['team_id']))).all()
    

    for item in fixer:
        if item.localteam_id !=request_data['team_id']:
            team_ids.append(item.localteam_id)

        if item.visitorteam_id !=request_data['team_id']:
            team_ids.append(item.visitorteam_id)

    if team_ids:
        result = TeamStatisticsGoalserveSerializer(
            TeamStatisticsGoalserve.objects.filter(team_id__in=team_ids).all()
            , many=True).data
    data ={"status": 200, "message": "success", "data":result}
    
    return JsonResponse(data)

@csrf_exempt
def LocalteamVisitorTeamStatistics(request):
    request_data = JSONParser().parse(request)
    fixtures = MatchGoalserve.objects.all().filter(league_id=request_data['league_id']).all()
    # fixtures = MatchGoalserve.objects.all().filter(\
    #     Q(league_id=request_data['league_id']),\
    #     ( \
    #         Q(\
    #             localteam_id=request_data['localteam_id'], \
    #             visitorteam_id=request_data['visitorteam_id'] \
    #         ) | \
    #         Q(
    #             visitorteam_id=request_data['visitorteam_id'], \
    #             localteam_id=request_data['localteam_id'] \
    #         )\
    #     )\

    # ).all()
    result= MatchByTeamGoalserveSerializer(fixtures , many=True).data
    data = {"status":200,"message":"success","data":result}
    return JsonResponse(data)
@csrf_exempt
def GetPrediction(request,match_id):
    request_data = JSONParser().parse(request)
    headtohead=[]
    final_res = []
    localteam ={}
    visiterteam ={}
    leagueByTeamId =[]
    teamDetail =[]
    league_id = 0
    final_h2h ={}
    dataSet={}
    success_message = ''
    error_message = ''
    subscrition = UserSubscriptionPayment.objects.all().filter(user_id=request_data['user_id'])
    if subscrition:
        success_message = 'success'
    else:
        error_message = 'User not subscribe any plan '
    fixtures = MatchGoalserve.objects.all().filter(match_id=match_id)
    if fixtures:
        result = MatchByTeamGoalserveSerializer(fixtures, many=True).data
        dataSet['match'] =result[0]
        dataSet['localteam'] = result[0]['localteam'][0]
        dataSet['visiterteam'] = result[0]['visitorteam'][0]
        # print(result[0]['localteam'])
        league_id =result[0]['league_id']   
        localteam_id =result[0]['localteam_id']
        visitorteam_id =result[0]['visitorteam_id']
        
        localteam_name =result[0]['localteam_name']
        visitorteam_name =result[0]['visitorteam_name']

        finalh2h = TeamStatisticsGoalserve.objects.all().filter(league_ids__contains=league_id)
        dataSet['teamDetail'] = TeamStatisticsGoalserveSerializer(finalh2h, many=True).data
        hea2head =head2head(int(localteam_id),int(visitorteam_id))
        dataSet['headtohead']=hea2head['result']
        dataSet['probability']=hea2head
        prediction = predictionH2HOddsGoalserve.objects.all().filter(match_id=match_id)
        prediction_detail =predictionH2HOddsGoalserveSerializer(prediction,many=True).data
        if prediction_detail:
            dataSet['prediction_detail'] =prediction_detail[0]
        else:
            dataSet['prediction_detail'] =[]
    data = {"status": 200, "error_message":error_message,'success_message':success_message, "data": dataSet}
    return JsonResponse(data)

@csrf_exempt
def UpcomingMatch(request):
    request_data = JSONParser().parse(request)
    success_message = None
    error_message = None
    subscrition = UserSubscriptionPayment.objects.all().filter(user_id=request_data['user_id'])
    if subscrition:
        success_message = 'success'
    else:
        error_message = 'User not subscribe any plan '
    queryObj = {}
    queryObj['match_id__in'] =  [4359068,4200012,4351090,4358682,4351091,4358642]
    fixtures = MatchGoalserve.objects.all().filter(**queryObj)
    result = MatchByTeamGoalserveSerializer(fixtures, many=True).data
    data = {"status":200,"error_message":error_message,'success_message':success_message,"data":result}
    return JsonResponse(data)