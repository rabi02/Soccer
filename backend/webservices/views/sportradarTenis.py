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
def sportradarAPI(request):
    # data =sportradarCompetitionInfo("69160")
    # data = sportradarCompetitorSummeryAPI("sr:competitor:131018")
    # data = sportradarDailySummaries('2022-06-19')
    data = sportradarCompetitorProfileAPI("sr:competitor:837920")
    # return data
    return JsonResponse(data, safe=False)

def sportradarCompetitionInfo(competition_id):
    pdata =[]
    import requests
    url = "https://api.sportradar.com/tennis/production/v3/en/competitions/sr:competition:"+competition_id+"/info.json?api_key="+SPORTRADER_KEY
    print(url)
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    res =json.dumps(json.loads(response.text))
    json_res = json.loads(res)
    data = {'status':200, 'message': 'success', "data": json_res}
    return JsonResponse(data)

def sportradarSeasonsAPI():
    pdata =[]
    import requests
    url = "https://api.sportradar.com/tennis/production/v3/en/seasons.json?api_key="+SPORTRADER_KEY
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    res =json.dumps(json.loads(response.text))
    json_res = json.loads(res)
    data = {'status':200, 'message': 'success', "data": json_res}
    return JsonResponse(data)
def sportradarDailySummaries(date):
    json_res ={}
    import requests
    url = "https://api.sportradar.com/tennis/production/v3/en/schedules/"+date+"/summaries.json?offset=0&api_key="+SPORTRADER_KEY
    payload={}
    headers = {}
    print(url)
    response = requests.request("GET", url, headers=headers, data=payload)
    # print(response.text)
    res =json.dumps(json.loads(response.text))
    if res:
        json_res = json.loads(res)
    return(json_res)
    # data = {'status':200, 'message': 'success', "data": json_res}
    # return JsonResponse(data)
def sportradarCompetitionsAPI():
    json_res ={}
    import requests
    url = "https://api.sportradar.com/tennis/production/v3/en/competitions.json?api_key="+SPORTRADER_KEY
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    res =json.dumps(json.loads(response.text))
    if res:
        json_res = json.loads(response.text)
    
    return json_res

def sportradarComplexesAPI():
    json_res={}
    url = "https://api.sportradar.com/tennis/production/v3/en/complexes.json?api_key="+SPORTRADER_KEY
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    res =json.dumps(json.loads(response.text))
    if res:
        json_res = json.loads(response.text)
    
    return(json_res)

def sportradarSummariesAPI(date):
    pdata =[]
    import requests
    url = "https://api.sportradar.com/tennis/production/v3/en/schedules/"+date+"/summaries.json?offset=0&api_key="+SPORTRADER_KEY
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    res =json.dumps(json.loads(response.text))
    json_res = json.loads(response.text)
    data = {'status':200, 'message': 'success', "data": json_res}
    return JsonResponse(data, safe=False)

def sportradarDoublesCompetitionsPlayedAPI(competiter_id):
    import requests
    url = "https://api.sportradar.com/tennis/production/v3/en/competitors/"+str(competiter_id)+"/doubles_competitions_played.json?api_key="+SPORTRADER_KEY
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    res =json.dumps(json.loads(response.text))
    json_res = json.loads(response.text)
    data = {'status':200, 'message': 'success', "data": json_res}
    return JsonResponse(data, safe=False)

def sportradarDoublesCompetitionsRankingAPI():
    import requests
    url = "https://api.sportradar.com/tennis/production/v3/en/double_competitors_rankings.json?api_key="+SPORTRADER_KEY
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    res =json.dumps(json.loads(response.text))
    json_res = json.loads(response.text)
    data = {'status':200, 'message': 'success', "data": json_res}
    return JsonResponse(data, safe=False)

def sportradarDoublesCompetitionsRaceRankingAPI():
    import requests
    url = "https://api.sportradar.com/tennis/production/v3/en/double_competitors_race_rankings.json?api_key="+SPORTRADER_KEY
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    res =json.dumps(json.loads(response.text))
    json_res = json.loads(response.text)
    data = {'status':200, 'message': 'success', "data": json_res}
    return JsonResponse(data, safe=False)

def sportradarDoublesCompetitionsRaceRankingAPI():

    import requests
    url = "https://api.sportradar.com/tennis/production/v3/en/double_competitors_race_rankings.json?api_key="+SPORTRADER_KEY
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    res =json.dumps(json.loads(response.text))
    json_res = json.loads(response.text)
    data = {'status':200, 'message': 'success', "data": json_res}
    return JsonResponse(data, safe=False)

def sportradarCompetitorProfileAPI(competiter_id):
    json_res ={}
    import requests
    url = "https://api.sportradar.com/tennis/production/v3/en/competitors/"+str(competiter_id)+"/profile.json?api_key="+SPORTRADER_KEY
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    # print(response.text)
    res =json.dumps(json.loads(response.text))
    if res:
        json_res = json.loads(response.text)

    # data = {'status':200, 'message': 'success', "data": json_res}
    # return JsonResponse(data, safe=False)
    return json_res

def sportradarCompetitorSummeryAPI(competiter_id):
    json_res ={}
    import requests
    url = "https://api.sportradar.com/tennis/production/v3/en/competitors/"+str(competiter_id)+"/summaries.json?api_key="+SPORTRADER_KEY
    # print(url)
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    # print(response.text)
    res =json.dumps(json.loads(response.text))
    if res:
        json_res = json.loads(response.text)
    # data = {'status':200, 'message': 'success', "data": json_res}
    # return JsonResponse(data, safe=False)
    return json_res

def sportradarCompetitorvsCompetitorAPI(competiter_id1,competiter_id2):
    
    import requests
    url = "https://api.sportradar.com/tennis/production/v3/en/competitors/"+str(competiter_id1)+"/versus/"+str(competiter_id2)+"/summaries.json?api_key="+SPORTRADER_KEY
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    res =json.dumps(json.loads(response.text))
    json_res = json.loads(response.text)
    data = {'status':200, 'message': 'success', "data": json_res}
    return JsonResponse(data, safe=False)

def sportradarLiveTennisAPI():
    
    import requests
    url = "https://api.sportradar.com/tennis/production/v3/en/schedules/live/timelines.json?api_key="+SPORTRADER_KEY
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    res =json.dumps(json.loads(response.text))
    json_res = json.loads(response.text)
    data = {'status':200, 'message': 'success', "data": json_res}
    return JsonResponse(data, safe=False)

def sportradarLiveTimelineDeltaAPI():
    import requests
    url = "https://api.sportradar.com/tennis/production/v3/en/schedules/live/timelines_delta.json?api_key="+SPORTRADER_KEY
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    res =json.dumps(json.loads(response.text))
    json_res = json.loads(response.text)
    data = {'status':200, 'message': 'success', "data": json_res}
    return JsonResponse(data, safe=False)

def sportradarRaceRankingAPI():
    import requests
    url = "https://api.sportradar.com/tennis/production/v3/en/race_rankings.json?api_key="+SPORTRADER_KEY
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    res =json.dumps(json.loads(response.text))
    json_res = json.loads(response.text)
    data = {'status':200, 'message': 'success', "data": json_res}
    return JsonResponse(data, safe=False)

def sportradarRankingAPI():
    import requests
    json_res = {}
    url = "https://api.sportradar.com/tennis/production/v3/en/rankings.json?api_key="+SPORTRADER_KEY
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    res =json.dumps(json.loads(response.text))
    if res:
        json_res = json.loads(response.text)
    # data = {'status':200, 'message': 'success', "data": json_res}
    # return JsonResponse(data, safe=False)
    return json_res

def sportradarSeasonsCompitatorAPI(season_id):
    import requests
    json_res ={}
    url = "https://api.sportradar.com/tennis/production/v3/en/seasons/"+str(season_id)+"/competitors.json?offset=0&api_key="+SPORTRADER_KEY
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    # print(response.text)
    res =json.dumps(json.loads(response.text))
    if res:
        json_res = json.loads(response.text)
        # data = {'status':200, 'message': 'success', "data": json_res}
    return json_res

def sportradarSeasonsInfoAPI(season_id):
    import requests
    url = "https://api.sportradar.com/tennis/production/v3/en/seasons/sr:season:"+str(season_id)+"/info.json?api_key="+SPORTRADER_KEY
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    res =json.dumps(json.loads(response.text))
    json_res = json.loads(response.text)
    data = {'status':200, 'message': 'success', "data": json_res}
    return JsonResponse(data, safe=False)

def sportradarSeasonsLinkAPI(season_id):
    import requests
    url = "https://api.sportradar.com/tennis/production/v3/en/seasons/sr:season:"+str(season_id)+"/stages_groups_cup_rounds.json?api_key="+SPORTRADER_KEY
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    res =json.dumps(json.loads(response.text))
    json_res = json.loads(response.text)
    data = {'status':200, 'message': 'success', "data": json_res}
    return JsonResponse(data, safe=False)

def sportradarSeasonsProbabilityAPI(season_id):
    import requests

    url = "https://api.sportradar.com/tennis/production/v3/en/seasons/sr:season::"+str(season_id)+"/probabilities.json?api_key="+SPORTRADER_KEY
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    res =json.dumps(json.loads(response.text))
    json_res = json.loads(response.text)
    data = {'status':200, 'message': 'success', "data": json_res}
    return JsonResponse(data, safe=False)

def sportradarSeasonsStandingAPI(season_id):
    import requests
    url = "https://api.sportradar.com/tennis/production/v3/en/seasons/sr:season:"+str(season_id)+"/standings.json?round=1&api_key="+SPORTRADER_KEY
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    res =json.dumps(json.loads(response.text))
    json_res = json.loads(response.text)
    data = {'status':200, 'message': 'success', "data": json_res}
    return JsonResponse(data, safe=False)

def sportradarSeasonsSummariesAPI(season_id):
    import requests
    url = "https://api.sportradar.com/tennis/production/v3/en/seasons/sr:season:"+str(season_id)+"/summaries.json?offset=0&api_key="+SPORTRADER_KEY
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    res =json.dumps(json.loads(response.text))
    json_res = json.loads(response.text)
    data = {'status':200, 'message': 'success', "data": json_res}
    return JsonResponse(data, safe=False)

def sportradarSeasonsAPI():
    import requests
    json_res ={}
    url = "https://api.sportradar.com/tennis/production/v3/en/seasons.json?api_key="+SPORTRADER_KEY
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    res =json.dumps(json.loads(response.text))
    if res:
        json_res = json.loads(response.text)
    
    return json_res

def sportradarSportsEventSummeryAPI(event_id):
    import requests
    url = "https://api.sportradar.com/tennis/production/v3/en/sport_events/sr:sport_event:"+str(event_id)+"/summary.json?api_key="+SPORTRADER_KEY
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    res =json.dumps(json.loads(response.text))
    json_res = json.loads(response.text)
    data = {'status':200, 'message': 'success', "data": json_res}
    return JsonResponse(data, safe=False)

def sportradarSportsEventTimelineAPI(event_id):
    import requests
    url = "https://api.sportradar.com/tennis/production/v3/en/sport_events/sr:sport_event:"+str(event_id)+"/timeline.json?api_key="+SPORTRADER_KEY
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    res =json.dumps(json.loads(response.text))
    json_res = json.loads(response.text)
    data = {'status':200, 'message': 'success', "data": json_res}
    return JsonResponse(data, safe=False)
    
def sportradarSportsEventRemovedAPI(event_id):
    import requests
    url = "https://api.sportradar.com/tennis/production/v3/en/sport_events/removed.json?offset=0&api_key="+SPORTRADER_KEY
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    res =json.dumps(json.loads(response.text))
    json_res = json.loads(response.text)
    data = {'status':200, 'message': 'success', "data": json_res}
    return JsonResponse(data, safe=False)

def sportradarSportsEventUpdatedAPI(event_id):
    import requests
    url = "https://api.sportradar.com/tennis/production/v3/en/sport_events/updated.json?offset=0&api_key="+SPORTRADER_KEY
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    res =json.dumps(json.loads(response.text))
    json_res = json.loads(response.text)
    data = {'status':200, 'message': 'success', "data": json_res}
    return JsonResponse(data, safe=False)   

@csrf_exempt
def CompetitorAI(request):
    requestdata = JSONParser().parse(request)
    competitor_id1 = requestdata['competitor_id1']
    competitor_id2 = requestdata['competitor_id2']
    competitor_id1Info=sportradarCompetitorProfileAPI(competitor_id1)
    competitor_id2Info=sportradarCompetitorProfileAPI(competitor_id2)
    summery1= sportradarCompetitorSummeryAPI(competitor_id1)
    summery2= sportradarCompetitorSummeryAPI(competitor_id2)
    surface1= GetSurfaceByCompitatorId(competitor_id1)
    surface2= GetSurfaceByCompitatorId(competitor_id2)
    AcesDfault1=getAcesDfault(summery1['summaries'])
    AcesDfault2=getAcesDfault(summery2['summaries'])
    rank = getRannkPointByCompitaterId(competitor_id1,competitor_id2)
    print(rank)
    competitor_name1 =''
    competitor_name2 =''
    elo_rating1 ='0.0'
    elo_rating2 ='0.0'
    if 'competitor' in competitor_id1Info:
        competitor_name1 = competitor_id1Info['competitor']['name'].strip()
        competitor_name1= competitor_name1.replace(",", "")
        words = competitor_name1.split(' ')
        reverse_competitor_name1 = ' '.join(reversed(words))

        cn1 = TennisEloRating.objects.filter(Q(player_name=competitor_name1)|Q(player_name=reverse_competitor_name1)).all()
        for cn in cn1:
            # print(season.season_id)
            elo_rating1 = cn.elo_rating

    if 'competitor' in competitor_id2Info:
        competitor_name2 = competitor_id2Info['competitor']['name'].strip()
        competitor_name2= competitor_name2.replace(",", "")
        words = competitor_name2.split(' ')
        reverse_competitor_name2 = ' '.join(reversed(words))
        cn2 = TennisEloRating.objects.filter(Q(player_name=competitor_name2)|Q(player_name=reverse_competitor_name2)).all()
        for cn in cn2:
            # print(season.season_id)
            elo_rating2 = cn.elo_rating

    srftot = getSurfaceTypeIntigerFormat(surface1)
    srftot2 = getSurfaceTypeIntigerFormat(surface2)
    SA = len(surface1) + len(surface2)
    # print(SA)
    st = srftot+srftot2
    # print(st)
    surface_type = st
    ace1 =0
    ace2 = 0
    df1=0
    df2=0
    AcI=1
    
    for ac1 in AcesDfault1['aces']:
        if AcI<=5:
            ace1 = ac1+ace1
        AcI=AcI+1
    ace1 =ace1/5
    AcI=1
    for ac2 in AcesDfault2['aces']:
        if AcI<=5:
            ace2 = ac2+ace2
        AcI=AcI+1
    ace2 =ace2/5
    AcI=1
    for dff1 in AcesDfault1['double_faults']:
        if AcI<=5:
            df1 = dff1+df1
        AcI=AcI+1
    df1 =df1/5
        
    AcI=1
    for dff2 in AcesDfault2['double_faults']:
        if AcI<=5:
            df2 = df2+dff2
        AcI=AcI+1
    df2 = df2/5

    cnt =  TennisDataInputAI.objects.filter(player_one_id=competitor_id1,player_two_id=competitor_id2).count()
    if cnt ==0:
        ins = TennisDataInputAI.objects.create(
                player_one_id=competitor_id1,
                player_two_id=competitor_id2,
                player_one_name=competitor_name1,
                player_two_name=competitor_name2,
                player_one_elo_rating=elo_rating1,
                player_two_elo_rating=elo_rating2,
                surface_encoded = surface_type,
                player_one_ace = ace1,
                player_two_ace = ace2,
                player_one_df = df1,
                player_two_df = df2,
                player_one_rank = rank['rank1'] if 'rank1' in rank else '0',
                player_two_rank = rank['rank2'] if 'rank2' in rank else '0',
                player_one_rank_points = rank['point1'] if 'point1' in rank else '0',
                player_two_rank_points = rank['point2'] if 'point2' in rank else '0'
            )
    arr =   {   'player_one_id':competitor_id1,
                'player_two_id':competitor_id2,
                'player_one_name':competitor_name1,
                'player_two_name':competitor_name2,
                'player_one_elo_rating':elo_rating1,
                'player_two_elo_rating':elo_rating2,
                'surface_encoded' : surface_type,
                'player_one_ace' : ace1,
                'player_two_ace' : ace2,
                'player_one_df' : df1,
                'player_two_df' : df2,
                'player_one_rank' : rank['rank1'] if 'rank1' in rank else '0',
                'player_two_rank' : rank['rank2'] if 'rank2' in rank else '0',
                'player_one_rank_points' : rank['point1'] if 'point1' in rank else '0',
                'player_two_rank_points' : rank['point2'] if 'point2' in rank else '0'
            }
    data = {'status':200, 'message': 'success','data':arr}
    return JsonResponse(data, safe=False)  
 
def getAcesDfault(data):
    rec={}
    aces =[]
    double_faults =[]
    for res in data:
       
        if 'statistics' in res:
            if 'totals' in res['statistics']:
                if 'competitors' in res['statistics']['totals']:
                    for stat in res['statistics']['totals']['competitors']:
                        if 'statistics' in stat:
                            # print(stat['statistics'])
                            # print("*****************************************************************")
                            if 'aces' in stat['statistics']:
                                acs = stat['statistics']['aces']
                                # print(acs)
                                aces.append(acs)
                            if 'double_faults' in stat['statistics']:
                                double_faults.append(stat['statistics']['double_faults'])
    rec['aces'] = aces
    rec['double_faults'] = double_faults
    return rec

def getRannkPointByCompitaterId(competitor_id1,competitor_id2):
    data=sportradarRankingAPI()
    
    rank1 =0
    point1 =0
    point2=0
    rank2 =0
    response ={}
    if 'rankings' in data:
        res = data['rankings']
        for rec in res:
            if 'competitor_rankings' in rec:
                for dt in rec['competitor_rankings']:
                    if str(competitor_id1) in dt['competitor']['id']:
                        rank1 = dt['rank']
                        point1 = dt['points']
                    if str(competitor_id2) in dt['competitor']['id']:
                        rank2 = dt['rank']
                        point2 = dt['points']
        # print(rank1,rank2)
        response['rank1'] =rank1
        response['rank2'] =rank2
        response['point1'] =point1
        response['point2'] =point2
    return response

def GetSurfaceByCompitatorId(competitor_id):
    data = sportradarCompetitorProfileAPI(competitor_id)
    surfaceArray=[]
    if 'periods' in data:
        for rec in data['periods']:
            if 'surfaces' in rec:
                for sur in rec['surfaces']:
                    if 'type' in sur:
                        surfaceArray.append({'year':rec['year'],'surfaces':sur['type']})
    return surfaceArray

def getSurfaceTypeIntigerFormat(surface):
    surfacearr=[]
    srftot =0
    surfacearr = {
        'red_clay':1,
        'red_clay_indoor':1,
        'red_clay_outdoor':1,
        'carpet_indoor':0,
        'carpet_outdoor':0,
        'grass':2,
        'green_clay':2,
        'synthetic_grass':2,
        'hardcourt_indoor':3,
        'hardcourt_outdoor':3,
        'unknown':4
    }
    i =1
    for srf in surface:
        if i<=5:
            srftot = srftot + surfacearr[srf['surfaces']]
        i = i+1
    
    # print(srftot)
    # return srftot/5
    return 2

def elo_ratingTennis():
    import requests
    from bs4 import BeautifulSoup

def datetimemod(ans):
    ans = ans.split(' ')[-1].split('/')
    y = ans[-1]
    m = ans[1]
    d = ans[0]
    dt = y+'-'+m+'-'+d
    return dt

def elo_rating():
    r = requests.get('https://tenniseloranking.blogspot.com/')
    soup = BeautifulSoup(r.content, 'html5lib')
    list_value = soup.find('div', attrs = {'id':'ArchiveList'}).find('ul', attrs = {'class':'hierarchy'}).find('ul', attrs = {'class':'hierarchy'}).find('ul', attrs = {'class':'posts'}).findAll('li')
    output_value = []
    for i in list_value:
        if ("Men's ELO Rankings" in i.find('a').text) or ("Women's ELO Rankings" in i.find('a').text):
            data = {
                "Tournament": i.find('a').text,
                "date": datetimemod(i.find('a').text),
                "link": i.find('a')['href']
            }
            output_value.append(data)
        else:
            continue
    if len(output_value) != 0 :
        elo_data = []
        for row in output_value:
            req = requests.get(row['link'])
            soup = BeautifulSoup(req.content, 'html5lib')
            table = soup.find('table', attrs = {'class':'tg'}).find('tbody').find_all('tr')
            elo_output = []
            for row1 in table:
                td_data = row1.find_all('td')
                rank = int(td_data[0].text)
                name = td_data[1].text
                elo = int(td_data[2].text)
                data = {
                    "rank": rank,
                    "name": name,
                    "elo_rating": elo
                }
                elo_output.append(data)
            data1 = {
                "Tournament": row['Tournament'],
                'date': row['date'],
                'data': elo_output
            }
            elo_data.append(data1)
        return elo_data
    else:
        return [{"result": None}]
    
def SaveCompetitorAI():
    # requestdata = JSONParser().parse(request)
   
    summery= sportradarCompetitionsAPI()
    for rec in summery['competitions']:
        
        cnt =  CompetitionsTennisSportrader.objects.filter(competitions_id=rec['id']).count()
        if cnt ==0:
            ins = CompetitionsTennisSportrader.objects.create(
                competitions_id=rec['id'],
                competitions_name = rec['name'] if 'name' in rec else '',
                competitions_type = rec['type'] if 'type' in rec else '',
                gender = rec['gender'] if 'gender' in rec else '',
                category_name = rec['category']['name'] if 'name' in rec['category'] else '',
                category_id = rec['category']['id'] if 'id' in rec['category'] else '',
            )
    
    data = {'status':200, 'message': 'success'}
    return JsonResponse(data, safe=False)  
 
def SaveComplexesTennis():
    
    summery= sportradarComplexesAPI()
    for rec in summery['complexes']:
        competitions_id= rec['id']
        competitions_name = rec['name']
        if 'venues' in rec:
            for vns in rec['venues']:
                cnt =  ComplexesTennisSportrader.objects.filter(venues_id=vns['id']).count()
                if cnt ==0:
                    ins = ComplexesTennisSportrader.objects.create(
                        
                        complexes_name = competitions_name,
                        complexes_id= competitions_id,
                        venues_id= vns['id'],
                        venues_name  = vns['name'] if 'name' in vns else '',
                        city_name = vns['city_name'] if 'city_name' in vns else '',
                        country_name =  vns['country_name'] if 'country_name' in vns else '',
                        country_code = vns['country_code'] if 'country_code' in vns else '',
            )
    
    data = {'status':200, 'message': 'success'}
    return JsonResponse(data, safe=False)  

def SaveEloRating(playerArr,elo_result,ptype):
    print(playerArr['id'])
    elo_rating='0.00'
    if ptype == 1:
        elo_rating = elo_result['player_id1']

    if ptype == 2:
        elo_rating = elo_result['player_id2']

    cnt =  TennisEloRating.objects.filter(player_id=playerArr['id']).count()
    if cnt ==0:
        ins = TennisEloRating.objects.create(
            player_id=playerArr['id'],
            abbreviation = playerArr['abbreviation'],
            country = playerArr['country'] if 'country' in playerArr else '',
            country_code = playerArr['country_code'] if 'country_code' in playerArr else '',
            player_name= playerArr['name'],
            elo_rating= elo_rating
        )
    else:
        data = TennisEloRating.objects.filter(player_id=playerArr['id']).update(
            player_id=playerArr['id'],
            abbreviation = playerArr['abbreviation'],
            country = playerArr['country'] if 'country' in playerArr else '',
            country_code = playerArr['country_code'] if 'country_code' in playerArr else '',
            player_name= playerArr['name'],
            elo_rating= elo_rating
        )
    data = {'status':200, 'message': 'success'}
    return 1  

def SaveSeasonTennis():
    
    summery= sportradarSeasonsAPI()
    for rec in summery['seasons']:

        cnt =  SeasonsTennisSportrader.objects.filter(season_id=rec['id']).count()
        if cnt ==0:
            ins = SeasonsTennisSportrader.objects.create(
                name = rec['name'] if 'name' in rec else '',
                season_id= rec['id'] if 'id' in rec else '',
                competition_id= rec['competition_id'] if 'competition_id' in rec else '',
                start_date  = rec['start_date'] if 'start_date' in rec else '',
                end_date = rec['end_date'] if 'end_date' in rec else '',
                year =  rec['year'] if 'year' in rec else ''
            )
    
    data = {'status':200, 'message': 'success'}
    return JsonResponse(data, safe=False)  

def SaveSeasonWiseCompitatorTennis(season_id):
    
    summery= sportradarSeasonsCompitatorAPI(season_id)
    for rec in summery['season_competitors']:

        cnt =  TennisSeasonCompitator.objects.filter(season_id=season_id,compitator_id=rec['id']).count()
        if cnt ==0:
            ins = TennisSeasonCompitator.objects.create(
                competitions_name = rec['name'] if 'name' in rec else '',
                season_id= season_id,
                compitator_id= rec['id'] if 'id' in rec else '',
                short_name  = rec['short_name'] if 'short_name' in rec else '',
                abbreviation = rec['abbreviation'] if 'abbreviation' in rec else ''
            )
    
    data = {'status':200, 'message': 'success'}
    return JsonResponse(data, safe=False)

def GetSasonSaveCompitator():
    data ={}
    seasoncompitator = SeasonsTennisSportrader.objects.all()
    for season in seasoncompitator:
        # print(season.season_id)
        data=SaveSeasonWiseCompitatorTennis(season.season_id)
    return data

@csrf_exempt
def GetLiveSummeryTennis(request):
    requestdata = JSONParser().parse(request)
    date = requestdata['date']
    json_res = sportradarDailySummaries(date)
    # import requests

    # url = "https://api.sportradar.com/tennis/production/v3/en/schedules/live/summaries.json?api_key="+SPORTRADER_KEY
    # payload={}
    # headers = {}
    # response = requests.request("GET", url, headers=headers, data=payload)
    # res =json.dumps(json.loads(response.text))
    # json_res = json.loads(response.text)
    data = {'status':200, 'message': 'success', "data": json_res}
    return JsonResponse(data, safe=False)

@csrf_exempt
def GetLiveSummeryTennis(request):
    requestdata = JSONParser().parse(request)
    date = requestdata['date']
    json_res = sportradarDailySummaries(date)
    # import requests

    # url = "https://api.sportradar.com/tennis/production/v3/en/schedules/live/summaries.json?api_key="+SPORTRADER_KEY
    # payload={}
    # headers = {}
    # response = requests.request("GET", url, headers=headers, data=payload)
    # res =json.dumps(json.loads(response.text))
    # json_res = json.loads(response.text)
    data = {'status':200, 'message': 'success', "data": json_res}
    return JsonResponse(data, safe=False)

@csrf_exempt
def GetHistroyData(request,start_date):
    from datetime import datetime
    import datetime
    response = []
    player=[]
    matchByPlayer =[]
    from django.utils.timezone import datetime #important if using timezones
    today = datetime.today()
    stop_date = today.strftime('%Y-%m-%d')
    import datetime
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(stop_date, "%Y-%m-%d")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

    for date in date_generated:
        str_date = date.strftime("%Y-%m-%d")
        json_res = sportradarDailySummaries(str_date)
        if 'summaries' in json_res:
            # print('summaries exist')
            for dt in json_res['summaries']:
                if 'sport_event' in dt:
                    category_name=''
                    season_name=''
                    competition_name =''
                    sport_event =dt['sport_event']
                    if 'sport_event_context' in sport_event:

                        sport_event_context =sport_event['sport_event_context']
                        if 'category' in sport_event_context:
                            category_name=sport_event_context['category']['name']

                        if 'season' in sport_event_context:
                            season_name=sport_event_context['season']['name']
                        if 'competition' in sport_event_context:
                            competition_name=sport_event_context['competition']['name']
                        
                        # if 'ATP' in sport_event_context['category']['name'] or 'WTA' in sport_event_context['category']['name'] or 'ATP' in sport_event_context['season']['name'] or 'WTA' in sport_event_context['season']['name'] or 'ATP' in sport_event_context['competition']['name'] or 'WTA' in sport_event_context['competition']['name']:
                        response.append(dt)
                        # if 'competitors' in  sport_event:
                            # if any(plr['id'] != sport_event['competitors'][0]['id'] for plr in player):
                        matchByPlayer.append(sport_event['competitors'])
                        player.append({
                                    'abbreviation':sport_event['competitors'][0]['abbreviation'],
                                    #'country':sport_event['competitors'][0]['country'],
                                    #'country_code':sport_event['competitors'][0]['country_code'],
                                    'id':sport_event['competitors'][0]['id'],
                                    'name':sport_event['competitors'][0]['name'],
                                    'qualifier':sport_event['competitors'][0]['qualifier'],
                                })
                        # if any(plr['id'] != sport_event['competitors'][1]['id'] for plr in player):
                        player.append({
                                'abbreviation':sport_event['competitors'][1]['abbreviation'],
                                #'country':sport_event['competitors'][1]['country'],
                                #'country_code':sport_event['competitors'][1]['country_code'],
                                'id':sport_event['competitors'][1]['id'],
                                'name':sport_event['competitors'][1]['name'],
                                'qualifier':sport_event['competitors'][1]['qualifier'],
                            })
                
    redis_instance.set('tennis_match', json.dumps(response))  
    redis_instance.set('tennis_player', json.dumps(player))   
    redis_instance.set('tennis_match_player', json.dumps(matchByPlayer))                       
    data = {'status':200, 'message': 'success', "data": response,'player':player,'matchByPlayer':matchByPlayer}
    return JsonResponse(data, safe=False)

@csrf_exempt
def EloratingCalculation(request):
    import math
    from datetime import datetime
    import datetime              
    tennis_match=json.loads(redis_instance.get('tennis_match')) 
    tennis_player= json.loads(redis_instance.get('tennis_player'))  
    tennis_match_player = json.loads(redis_instance.get('tennis_match_player')) 
    # print(tennis_match_player)
    # res =json.dumps(json.loads(response.text))
    # json_res = json.loads(res)
   
    for plr in tennis_match_player:
        # print(plr)
        ratingA = 1600
        ratingB = 1600
        player_id1 =''
        player_id2 =''
        playerarr1 = plr[0]
        playerarr2 = plr[1]
        player_id1 = plr[0]['id']
        player_id2 = plr[1]['id']
        for mtch in tennis_match:
            if 'sport_event' in mtch:
                match = mtch['sport_event']
                if 'competitors' in match:
                    if match['competitors'][0]['id'] == player_id1 or match['competitors'][1]['id'] == player_id1:

                        if 'sport_event_status' in mtch:

                            if 'winner_id' in mtch['sport_event_status']:
                                if mtch['sport_event_status']['winner_id'] != player_id1:
                                   ratingA = ratingA+0 
                                elif mtch['sport_event_status']['winner_id'] == player_id1:
                                    ratingA = ratingA+1
                                else:
                                    ratingA = ratingA+.5

                    if match['competitors'][0]['id'] == player_id2 or match['competitors'][1]['id'] == player_id2:

                        if 'sport_event_status' in mtch:

                            if 'winner_id' in mtch['sport_event_status']:
                                if mtch['sport_event_status']['winner_id'] != player_id2:
                                   ratingB = ratingB+0 
                                elif mtch['sport_event_status']['winner_id'] == player_id2:
                                    ratingB = ratingB+1
                                else:
                                    ratingB = ratingB+.5
        elo_result=EloRating(ratingA, ratingB, 20, 1)
        SaveEloRating(playerarr1,elo_result,1)
        SaveEloRating(playerarr2,elo_result,2)

    
   

    data = {'status':200, 'message': 'success', "data": json.loads(tennis_match_player),'player':json.loads(tennis_player)}
    return JsonResponse(data, safe=False)

def Probability(rating1, rating2):
    import math
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400))

def EloRating(Ra, Rb, K, d):
    import math

    # To calculate the Winning
    # Probability of Player B
    Pb = Probability(Ra, Rb)

    # To calculate the Winning
    # Probability of Player A
    Pa = Probability(Rb, Ra)

    # Case -1 When Player A wins
    # Updating the Elo Ratings
    if (d == 1) :
        Ra = Ra + K * (1 - Pa)
        Rb = Rb + K * (0 - Pb)
    

    # Case -2 When Player B wins
    # Updating the Elo Ratings
    else :
        Ra = Ra + K * (0 - Pa)
        Rb = Rb + K * (1 - Pb)
    
    data ={'player_id1': round(Ra, 6),'player_id2':round(Rb, 6)}
    print(Ra,Rb)
    print('-------------')
    print(data)
    print("++++++++++++++++++++++++++++++++++")
    # print("Updated Ratings:-")
    # print("Ra =", round(Ra, 6)," Rb =", round(Rb, 6))
    return (data)

@csrf_exempt
def EloratingView(request):
    eloQuery =TennisEloRating.objects.all()
    data = EloRatingSerializer(eloQuery, many=True).data
    # import json
    # f = open('media/match_player.json')
    # data = json.load(f)
    # f.close()
    # import math
    # from datetime import datetime
    # import datetime              
    # tennis_match=data['data'] 
    # tennis_player= data['player']   
    # tennis_match_player =data['matchByPlayer'] 
    # # print(tennis_match_player)
    # # res =json.dumps(json.loads(response.text))
    # # json_res = json.loads(res)
   
    # for plr in tennis_match_player:
    #     ratingA = 1600
    #     ratingB = 1600
    #     player_id1 =''
    #     player_id2 =''
    #     # print(plr)
    #     playerarr1 = plr[0]
    #     playerarr2 = plr[1]
    #     player_id1 = plr[0]['id']
    #     player_id2 = plr[1]['id']
    #     for mtch in tennis_match:
    #         if 'sport_event' in mtch:
    #             match = mtch['sport_event']
    #             if 'competitors' in match:
    #                 if match['competitors'][0]['id'] == player_id1 or match['competitors'][1]['id'] == player_id1:

    #                     if 'sport_event_status' in mtch:

    #                         if 'winner_id' in mtch['sport_event_status']:
    #                             if mtch['sport_event_status']['winner_id'] != player_id1:
    #                                ratingA = ratingA+0 
    #                             elif mtch['sport_event_status']['winner_id'] == player_id1:
    #                                 ratingA = ratingA+1
    #                             else:
    #                                 ratingA = ratingA+.5

    #                 if match['competitors'][0]['id'] == player_id2 or match['competitors'][1]['id'] == player_id2:

    #                     if 'sport_event_status' in mtch:

    #                         if 'winner_id' in mtch['sport_event_status']:
    #                             if mtch['sport_event_status']['winner_id'] != player_id2:
    #                                ratingB = ratingB+0 
    #                             elif mtch['sport_event_status']['winner_id'] == player_id2:
    #                                 ratingB = ratingB+1
    #                             else:
    #                                 ratingB = ratingB+.5
    #     elo_result=EloRating(ratingA, ratingB, 20, 1)
    #     SaveEloRating(playerarr1,elo_result,1)
    #     SaveEloRating(playerarr2,elo_result,2)
    result = {"status": 200, "message": "success", "data":data}
    return JsonResponse(result)
