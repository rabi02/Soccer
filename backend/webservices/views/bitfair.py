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
from webservices.views.BetfairOrder import *
from webservices.views.LibGoalServeAPI import *
# from webservices.views.CommonFunction import *
from webservices.views.bitfairapi import *
from datetime import datetime
from django.views import View
from django.views import generic
from webservices.serializers import *
from db_table.models import *

from BetfairApi.BetfairExchangeAPI import *
import re
from datetime import datetime, timedelta
from BetfairUpdater.SoccerCalculation import *
# from soccer.testData import *
from django.utils.text import slugify 
import random 
import string 
from soccer.scrap import *
import redis


@csrf_exempt
def EventListBitfair(request):
    from django.conf import settings
    response = getTennisComoitation(request)
    # response = getTennisComoitation(request)
    data = {'status':200, 'message': 'success', "data": eval(response)}
    # to_csv = save_to_csv(eval(response), file_path=r"C:\Users\suman_m\Desktop\Csv\EventType.csv")
        # 'data' :json.dumps(json.loads(response.text), indent=3)

    return JsonResponse(data)

@csrf_exempt
def EventListBitfair2(request):
    from django.conf import settings
    # delete =RemoveDuplicate()
    response = getEvents("2020-03-13","2022-12-10")
    data = {'status': 200, 'message': 'success', "data": eval(response)}
    res = eval(response)

    # to_csv = save_to_csv(res["result"], file_path=r"C:\Users\suman_m\Desktop\Csv\EventType2.csv")
    return JsonResponse(res)

@csrf_exempt
def Events(request):
    from django.conf import settings
    # HistoricPredictionDataDataCSV()
    # request_data = JSONParser().parse(request)
    # response = getEvents('2020-01-01','2022-10-18')
    # ListEventBetfair()
    # delete =RemoveDuplicate()
    # ListMarketTypes(31998611)
    # data2=GetDailySummery()
    # data=PreparePredictionAndOtherData()
    # data1=StoreCompetitions()
    # data1=storeintoradis()
    # data =StorePredictionDataSportsradarToBetfairExchangeEvent()
    data = {'status': 200, 'message': 'success', "data": 'data'}
    # res = eval(response)
    # to_csv = save_to_csv(res["result"], file_path=r"C:\Users\suman_m\Desktop\Csv\Events.csv")
    return JsonResponse(data)

@csrf_exempt
def MarketInformation(request):
    from django.conf import settings
    from db_table.models import Events
    import time
    # ListEventBetfair()
    # delete =RemoveDuplicate()
    queryObj={}
    queryObj['competition_id__in'] =  [55,59,81,117,10932509]
    event = Events.objects.all().filter(competition_id=10932509)
    for evnt in event:
        # print(evnt.competition_id,evnt.events_id)
        
        MarketCatlogDetail(evnt.competition_id,evnt.events_id)
        time.sleep(5)
    # response = getMarketInformation(request)
    
    # to_csv = save_to_csv(res["result"], file_path=r"C:\Users\suman_m\Desktop\Csv\MarketInformation.csv")
    # delete =RemoveDuplicate()
    dt1=MarketCatlogDetail(10932509,32031895)
    data = {"status": 200, "message": "success", "data": ''}
    return JsonResponse(data)

@csrf_exempt
def HorseRacing(request):
    from django.conf import settings

    getHorseRacing(request)
    data = {
        'status': 0,
        'message': 'Username / password mismatch.',
        # 'data' :json.dumps(json.loads(response.text), indent=3)
    }

    return JsonResponse(data)

@csrf_exempt
def FootballCompetitions(request):
    from django.conf import settings

    response = getFootballCompetitions(request)
    data = {'status': 200, 'message': 'success', "data": eval(response)}
    # res = eval(response)
    # to_csv = save_to_csv(res["result"], file_path=r"C:\Users\admin\Desktop\betfair\me\FootballCompetitions.csv")

    return JsonResponse(data)

@csrf_exempt
def PlaceOrders(request):
    request_data = JSONParser().parse(request)
    from django.conf import settings

    # rtn = getPlaceOrders(request)
    market_id =request_data['market_id']
    selection_id = request_data['selection_id']
    handicap =request_data['handicap']
    price = request_data['price']
    size = request_data['size']
    user_id =request_data['uId']
    bookmaker_price =request_data['bookmaker_price']
    bookmaker_size=request_data['bookmaker_size']
    BetfairApplicationKey =request_data['AppName']
    BetfairPassword =request_data['BPassword']
    BetfairUserName =request_data['BUserName']
    
    rtn = place_order(market_id,selection_id,handicap,price,size,user_id,BetfairApplicationKey,BetfairPassword,BetfairUserName,bookmaker_price,bookmaker_size)
    data = {
        'status':0,
        'message': 'Place Order',
        'data':rtn
        # 'data' :json.dumps(json.loads(response.text), indent=3)
    }

    return JsonResponse(data)
@csrf_exempt
def AutobetPlaceOrders(request):
    request_data = JSONParser().parse(request)
    from django.conf import settings

    # rtn = getPlaceOrders(request)
    AutobetArr =request_data['AutobetArr']
    
    handicap =request_data['handicap']
    user_id =request_data['uId']
    BetfairApplicationKey =request_data['AppName']
    BetfairPassword =request_data['BPassword']
    BetfairUserName =request_data['BUserName']
    rtn = AutobetPlaceOrder(AutobetArr,user_id,BetfairApplicationKey,BetfairPassword,BetfairUserName)
    data = {
        'status':0,
        'message': 'Place Order',
        'data':rtn
        # 'data' :json.dumps(json.loads(response.text), indent=3)
    }

    return JsonResponse(data)
@csrf_exempt
def PlaceOrdersspbet(request):
    from django.conf import settings
    market_id='1.210557250'
    selection_id='67143'
    BetfairUsername='harding.darren4@gmail.com'
    BetfairPassword='Galaxy2007()!'
    BeatfairApplicationKey= '87bDCv3LEKLoIsP7'
    # getPlaceOrdersspbet(market_id,selection_id)
    # getListcurrentOrders(market_id)
    # dt = clearOrder(BetfairUsername,BetfairPassword,BeatfairApplicationKey)
    # dt=monthwiseReport()
    data = {
        'status': 0,
        'message': 'Username / password mismatch.',
        'data' :'dt'
    }

    return JsonResponse(data)

@csrf_exempt
def ListcurrentOrders(request):
    from django.conf import settings

    getListcurrentOrders(request)
    data = {
        'status': 0,
        'message': 'Username / password mismatch.',
        # 'data' :json.dumps(json.loads(response.text), indent=3)
    }

    return JsonResponse(data)
@csrf_exempt
def Listmarketbook(request):
    from django.conf import settings
    from db_table.models import MarketInformation
    MInformation = MarketInformation.objects.all()
    for minfo in MInformation:
    	getListmarketbook(minfo.market_id)
    data = {'status': 200, 'message': 'success', "data": ''}

    return JsonResponse(data)

@csrf_exempt
def MarketPrices(request):
    from django.conf import settings

    getMarketPrices(request)
    data = {
        'status': 0,
        'message': 'Username / password mismatch.',
        # 'data' :json.dumps(json.loads(response.text), indent=3)
    }

    return JsonResponse(data)

@csrf_exempt
def TennisComoitation(request):
    from django.conf import settings
    response = getTennisComoitation(request)
    # response = getTennisComoitation(request)
    data = {'status':200, 'message': 'success', "data": eval(response)}
    # to_csv = save_to_csv(eval(response), file_path=r"C:\Users\suman_m\Desktop\Csv\EventType.csv")
        # 'data' :json.dumps(json.loads(response.text), indent=3)
    return JsonResponse(data)

@csrf_exempt
def TennisEvent(request):
    from django.conf import settings
    request_data = JSONParser().parse(request)
    response = getTenisEvents(request_data['competition_ids'])
    # response = getTennisComoitation(request)
    data = {'status':200, 'message': 'success', "data": response}
    # to_csv = save_to_csv(eval(response), file_path=r"C:\Users\suman_m\Desktop\Csv\EventType.csv")
        # 'data' :json.dumps(json.loads(response.text), indent=3)
    return JsonResponse(data)

@csrf_exempt
def TennisMarket(request):
    from django.conf import settings
    request_data = JSONParser().parse(request)
    competition_id = request_data['competition_id']
    event_id = request_data['event_id']
    response =  MarketCatlogDetailTennis(competition_id,event_id)
    # response = getTennisComoitation(request)
    data = {'status':200, 'message': 'success', "data": response}
    # to_csv = save_to_csv(eval(response), file_path=r"C:\Users\suman_m\Desktop\Csv\EventType.csv")
        # 'data' :json.dumps(json.loads(response.text), indent=3)
    return JsonResponse(data)



@csrf_exempt
def getCountry(request):
    import requests
    url = "https://soccer.sportmonks.com/api/v2.0/countries?api_token=vAmUZViG0finz069tZMM0Uiy3hRN5YyRPmqY5KJqLaXEgpiYANMleR2kj2lM"
    response = requests.request("GET", url, headers={'Accept': 'application/json'})
    print(response)
    data = {
        'status': 0,
        'message': 'Username / password mismatch.',
        'data' :json.dumps(json.loads(response.text), indent=3)
    }
    return JsonResponse(data)

@csrf_exempt
def CountryList(request, id=None):
  
    # if id:
    #     country = Countries.objects.all().filter(id=id)
    #     countryerializer = CountrySerializer(country, many=True)
    #     data = {"status": 200, "message": "success", "data": countryerializer.data}
    # else:
    #     country = Countries.objects.all().filter(continent='Europe')
    #     countryerializer = CountrySerializer(country, many=True)
    #     data = {"status": 200, "message": "success", "data": countryerializer.data}
    

    #API from Goal Serve and get 5 Country
    country=[
        {'id':'England','name':'England'},
        {'id':'Spain','name':'Spain'},
        {'id':'Italy','name':'Italy'},
        {'id':'Germany','name':'Germany'},
        {'id':'France','name':'France'},
    ]
    data = {"status": 200, "message": "success", "data": country}
        # response = get_countries(request)
        # countries_save(response)
        # data = {"status": 200, "message": "success", "data": data_save}
        # data = {"status": 200, "message": "success", "data": json.loads(response)}
    return JsonResponse(data)
@csrf_exempt
def GetSaveLeague(request, id=None):
  
    if id:
        league = Leagues.objects.all().filter(id=id)
        leagueserializer = AllLeagueSerializer(league, many=True)
        data = {"status": 200, "message": "success", "data": leagueserializer.data}
    else:
        league = Leagues.objects.all()
        leagueserializer = AllLeagueSerializer(league, many=True)
        data = {"status": 200, "message": "success", "data": leagueserializer.data}
    return JsonResponse(data)

@csrf_exempt
def Leagues(request, id=None):
    if id:
        response = get_leagues(request, id=id)
    else:
        response = get_leagues(request)
    data = {"status": 200, "message": "success", "data": json.loads(response)}
    return JsonResponse(data)

@csrf_exempt
def LeaguesByCountry(request, country_id=None):
    # response = get_leagues(request, country_id=country_id)
    # data = {"status": 200, "message": "success", "data": json.loads(response)}
    league=GatLeagueByCountryGoalServe(country_id)
    data = {"status": 200, "message": "success", "data":league}
    return JsonResponse(data)

@csrf_exempt
def SearchLeagues(request, league_name):
    response = search_by_league(request, league_name=league_name)
    data = {"status": 200, "message": "success", "data": json.loads(response)}
    return JsonResponse(data)

@csrf_exempt
def Player(request, id=None, country_id=None, name=None):
    if id:
        response = get_player(request, id=id)
        # player_save(response)
    elif country_id:
        response = get_player(request, country_id=country_id)
    elif name:
        response = get_player(request, name=name)
    else:
        response = {}

    data = {"status": 200, "message": "success", "data": json.loads(response)}
    return JsonResponse(data)

@csrf_exempt
def Team(request, id=None, country_id=None):
    if id:
        response = get_teams(request, id=id)
        team_save(response)
    elif country_id:
        response = get_teams(request, country_id=country_id)
    else:
        response = {}

    data = {"status": 200, "message": "success", "data": json.loads(response)}
    return JsonResponse(data)

@csrf_exempt
def Teamssquads(request, id=None,squadplayer=None):
    response = get_teamssquads(request, id=id,squadplayer=squadplayer)
    data = {"status": 200, "message": "success", "data": json.loads(response)}
    return JsonResponse(data)

@csrf_exempt
def Teambyseason(request, id=None):
    response = get_teambyseason(request, id=id)
    data = {"status": 200, "message": "success", "data": json.loads(response)}
    return JsonResponse(data)

@csrf_exempt
def Searchteambyname(request, team_name):
    response = search_by_team(request, team_name=team_name)
    data = {"status": 200, "message": "success", "data": json.loads(response)}
    return JsonResponse(data)

@csrf_exempt
def Currentleaguesbyteamid(request, team_id=None):
    response = get_currentleaguesbyteamid(request, team_id=team_id)
    data = {"status": 200, "message": "success", "data": json.loads(response)}
    return JsonResponse(data)

@csrf_exempt
def Allleaguesbyteamid(request, team_id=None):
    response = get_allleaguesbyteamid(request, team_id=team_id)
    data = {"status": 200, "message": "success", "data": json.loads(response)}
    return JsonResponse(data)

@csrf_exempt
def OddsList(request, fixture_id=None, bookmarker_id=None):
    print(id)
    response = get_oddsList(request,fixture_id,bookmarker_id)
    data = {"status": 200, "message": "success", "data": json.loads(response)}
    return JsonResponse(data)

@csrf_exempt
def OddsMarketList(request, fixture_id=None, market_id=None):
    print(id)
    response = get_oddsmarketList(request,fixture_id,market_id)
    data = {"status": 200, "message": "success", "data": json.loads(response)}
    return JsonResponse(data)

@csrf_exempt
def OddsbyfixtureidList(request, fixture_id=None):
    response = get_oddsbyfixtureidList(request, fixture_id=fixture_id)
    odds_save(response)
    data = {"status": 200, "message": "success", "data": json.loads(response)}
    return JsonResponse(data)
@csrf_exempt
def OddsbyfixtureidList(request):
    teams = Odds.objects.all().filter(is_popular=True).order_by('-id')[:10]
    oddserializer = OddsSerializer(teams, many=True)
    data = {"status": 200, "message": "success", "data": oddserializer.data}
    return JsonResponse(data)

@csrf_exempt
def InplayOddsbyfixtureidList(request, fixture_id=None):
    response = get_inplayoddsbyfixtureidList(request, fixture_id=fixture_id)
    data = {"status": 200, "message": "success", "data": json.loads(response)}
    return JsonResponse(data)
@csrf_exempt
def StandingseasonList(request, season_id=None):
    response = get_standingseasonlist(request, season_id=season_id)
    season_save(response)
    data = {"status": 200, "message": "success", "data": json.loads(response)}
    return JsonResponse(data)

@csrf_exempt
def StandingliveseasonList(request, season_id=None):
    response = get_standingliveseasonlist(request, season_id=season_id)
    data = {"status": 200, "message": "success", "data": json.loads(response)}
    return JsonResponse(data)

@csrf_exempt
def Standingbyseasonroundid(request, season_id=None, round_id=None):
    print(id)
    response = get_standingbyseasonroundid(request,season_id,round_id)
    data = {"status": 200, "message": "success", "data": json.loads(response)}
    return JsonResponse(data)

@csrf_exempt
def Standingbyseasondate(request, season_id=None, start_date=None):
    print(id)
    response = get_standingbyseasondate(request,season_id=season_id,start_date=start_date)
    data = {"status": 200, "message": "success", "data": json.loads(response)}
    return JsonResponse(data)

@csrf_exempt
def Correctionsbyseasonid(request, season_id=None):
    response = get_correctionsbyseasonid(request, season_id=season_id)
    data = {"status": 200, "message": "success", "data": json.loads(response)}
    return JsonResponse(data)

@csrf_exempt
def MatchFixtures(request, fixture_id=None):
    if fixture_id:
        response = get_match_fixture(request, fixture_id=fixture_id)
    else:
        response = get_match_fixture(request)
    data = {"status": 200, "message": "success", "data": json.loads(response)}
    return JsonResponse(data)

@csrf_exempt
def FixtureByDate(request, start_date=None, end_date=None, team_id=None):
    response = fixture_by_dateSeries(request, start_date=start_date, end_date=end_date)
    data = {"status": 200, "message": "success", "data": json.loads(response)}
    return JsonResponse(data)

@csrf_exempt
def FixtureByIdList(request, id_list=None):
    response = fixture_by_idlist(request, id_list=id_list)
    data = {"status": 200, "message": "success", "data": json.loads(response)}
    return JsonResponse(data)

@csrf_exempt
def Fixtures(request, fixture_id_lineup=None, fixture_id_event=None):
    response = get_fixture(request, fixture_id_lineup=fixture_id_lineup, fixture_id_event=fixture_id_event)
    data = {"status": 200, "message": "success", "data": json.loads(response)}
    return JsonResponse(data)

@csrf_exempt
def MatchByLeague(request):
    from django.utils.timezone import datetime #important if using timezones
    today = datetime.today()
    request_data = JSONParser().parse(request)
    league_ids=[564,384,304,1114,38,32,1422]
    
    # print(request_data)
    # response = get_fixturesupdate(request)
    response = {}
    # query OBJ
    queryObj = {
        'time_date__gte': datetime.today(),
        'deleted':False

    }

    if 'week' in request_data:
        one_week_ago = datetime.today() - timedelta(days=7)
        queryObj['time_date__gte'] = today.strftime('%Y-%m-%d')
        queryObj['time_date__lte'] = one_week_ago.strftime('%Y-%m-%d')
    if 'popular' in request_data:
       queryObj['is_popular'] = True
    if 'country_id' in request_data:
        queryObj['country_id'] = request_data['country_id']
    if 'league_id' in  request_data:
        queryObj['league_id'] = request_data['league_id']
    else:
        queryObj['league_id__in'] =  league_ids

    if 'matchid' in request_data:
        queryObj['matchid'] = request_data['matchid']
    if 'id' in request_data:
        queryObj['id'] = request_data['id']
    
    # endpoint = "https://soccer.sportmonks.com/api/v2.0/fixtures/updates"
    # url = endpoint + "?api_token=" + football_token
    # print(queryObj)
    # response = requests.get(url)
    # res = json.dumps(json.loads(response.text), indent=3)
    # result = json.loads(res)

    final_res = []
    fixtures = MatchFixtureUpdate.objects.all().filter(**queryObj).order_by('-id')[:15]
    result = MatchFixtureUpdateSerializer(fixtures, many=True).data

    for index, item in enumerate(result):
        # print(index)
        # print("-----------------")
        # print(item["localteam_id"])
        # print("*********************")
        # print(item["visitorteam_id"])
        # print("============================")

        # try:
        req_data = {}
        # print(item["season_id"])
        # get_seasonlist(request, id=item["season_id"])
        league_res = GetLeagueByLeagueId(item["league_id"])
        item['league_response'] = league_res
        # local_team_id_res = GetTeamStatisticsByTeamIdSeasonIdFromSportsmonk(item["localteam_id"],item["season_id"])
        local_team_id_res = GetTimeSessionByteamId(item["localteam_id"])
        item['local_team_id_response'] =local_team_id_res
        # visitorteam_id_res = GetTeamStatisticsByTeamIdSeasonIdFromSportsmonk(item["visitorteam_id"],item["season_id"])
        visitorteam_id_res = GetTimeSessionByteamId(item["visitorteam_id"])
        item['visitorteam_id_response'] =visitorteam_id_res
        if item["winnerteam_id"] == item["localteam_id"]:
            item['winner_team'] =local_team_id_res
            # req_data.update({"winner_team": local_team_id_response})
        elif item["winnerteam_id"] == item["visitorteam_id"]:
            item['winner_team'] =visitorteam_id_res
            # req_data.update({"winner_team": visitorteam_id_response})
        else:
            item['winner_team'] = None
        final_res.append(item)
# print("------------------------")  
# print(item) 
# print("****************************")
            
    # print(final_res)
    # response = get_fixturesupdate(request)
    # result=[]
    # if 'country_id' in request.GET:
    #     for resp in response:
    #         for nresp in resp["league_response"]:
    #             if nresp["country_id"] == int(request.GET["country_id"]):
    #                 result.append(resp)
    #     data = {"status": 200, "message": "success", "data": result}
    #     return JsonResponse(data)
    # if 'league_id' in request.GET:
    #     for resp in response:
    #         if resp["league_id"] == int(request.GET["league_id"]):
    #             result.append(resp)
    #     data = {"status": 200, "message": "success", "data": result}
    #     return JsonResponse(data)

    # if 'match_id' in request.GET:
    #     for resp in response:
    #         if resp["matchid"] == int(request.GET["match_id"]):
    #             result.append(resp)
    #     data = {"status": 200, "message": "success", "data": result}
    #     return JsonResponse(data)
    
    data = {"status": 200, "message": "success", "data":final_res}

    return JsonResponse(data)

@csrf_exempt
def MatchByLeagueById(request):
    response = get_fixturebyid(request)
    data = {"status": 200, "message": "success", "data": response}
    return JsonResponse(data)

@csrf_exempt
def GetTeamById(request):
    requestdata = JSONParser().parse(request)
    team =TeamStatisticsGoalserve.objects.filter(team_id=requestdata["team_id"]).all()[:1]
    if team:
        res = TeamStatisticsGoalserveSerializer(
            TeamStatisticsGoalserve.objects.filter(team_id=requestdata["team_id"]).all()[:1]
            , many=True).data
    else:
        storeTeamAndStatistics(requestdata["team_id"])
        res = TeamStatisticsGoalserveSerializer(
            TeamStatisticsGoalserve.objects.filter(team_id=requestdata["team_id"]).all()[:1]
            , many=True).data
 
    data = {"status": 200, "message": "success", "data":res}
    return JsonResponse(data)

@csrf_exempt
def GetPlayerByTeamId(request):
    requestdata = JSONParser().parse(request)
    res=GetPlayerByteamId(requestdata["team_id"])
    data = {"status": 200, "message": "success", "data":res}
    return JsonResponse(data)

class getallplayer(APIView):
    def post(self, request):
        request_data = JSONParser().parse(request)
        response = {}
        queryObj = {}
        print(request_data)
        if 'team_id' in  request_data and request_data['team_id'] !='':
            queryObj['team_id'] = request_data['team_id']

        if 'league_id' in request_data and request_data['league_id'] !='':
            queryObj['league_id'] = request_data['league_id']
            
        if len(queryObj)>0:
            print(queryObj)

            players = PlayerGoalserve.objects.all().filter(**queryObj)
        else:
            league_ids= LeagueIdGolaServe()
            players = PlayerGoalserve.objects.all().filter(league_id__in=league_ids).order_by('-id')
        serializer = PlayerGoalserveSerializer(players, many=True)
        # print(serializer.data)

        return Response({"status": 200, "message": "success", "data": serializer.data}, status=200)

class Footballodds(APIView):
    def get(self, request):
        odds = Odds.objects.all()
        serializer = OddsSerializer(odds, many=True)
        return Response({"status": 200, "message": "success", "data": serializer.data}, status=200)


# @csrf_exempt
# def PlayerSatistics(request, player_id=None):
#     response = get_player_stats(request, player_id=player_id)
#     data = {"status": 200, "message": "success", "data": json.loads(response)}
#     return JsonResponse(data)


@csrf_exempt
def SeasonSatistics(request, season_id=None):
    response = get_season_stats(request, season_id=season_id)
    data = {"status": 200, "message": "success", "data": json.loads(response)}
    return JsonResponse(data)

class Playerstats(APIView):
    def get(self, request):
        player = PlayerStatistics.objects.all().order_by('-id')
        serializer = PlayerStatisticsSerializer(player, many=True)
        return Response({"status": 200, "message": "success", "data": serializer.data}, status=200)

class PlayerstatsByPlayerId(APIView):
    def post(self, request):
        instance ={}
       
        requestdata = JSONParser().parse(request)
        players = PlayerGoalserve.objects.all().filter(player_id=requestdata['player_id'])
        serializer =PlayerGoalserveSerializer(players, many=True)
        playerstatistics = PlayerStatisticsGoalserve.objects.all().filter(player_id=requestdata['player_id'])
        pserializer = PlayerStatisticsGoalserveSerializer(playerstatistics, many=True).data
        # print(pserializer[0]['statistics'])
        instance['player'] = serializer.data
        instance['playerstatistics'] = pserializer
        if len(pserializer[0]['statistics']) >5 :
            statistics = json.loads(pserializer[0]['statistics'])
            pserializer[0]['statistics'] = statistics['club']

        if len(pserializer[0]['statistic_club']) >5:
            statistic_club = json.loads(pserializer[0]['statistic_club'])
            pserializer[0]['statistic_club'] = statistic_club['club']

        if len(pserializer[0]['statistic_popular_intl_club']) >5:
            statistic_popular_intl_club = json.loads(pserializer[0]['statistic_popular_intl_club'])
            pserializer[0]['statistic_popular_intl_club'] = statistic_popular_intl_club['club']

        if len(pserializer[0]['statistic_international_club']) >5:
            print(pserializer[0]['statistic_international_club'])
            statistic_international_club = json.loads(pserializer[0]['statistic_international_club'])
            pserializer[0]['statistic_international_club'] = statistic_international_club['club']

        if len(pserializer[0]['overall_clubs'])>5:
            overall_clubs = json.loads(pserializer[0]['overall_clubs'])
            # pserializer[0]['overall_clubs'] = overall_clubs['club']
            

        if len(pserializer[0]['trophies']) >5:
            trophies = json.loads(pserializer[0]['trophies'])
            pserializer[0]['trophies'] = trophies['trophy']

        if len(pserializer[0]['transfers'])>5:
            transfers = json.loads(pserializer[0]['transfers'])
            pserializer[0]['transfers'] = transfers['transfer']
        return Response({"status": 200, "message": "success", "data": instance}, status=200)

class GetLeagueDetail(APIView):
    def get(self,request):
        # from db_table.models import Leagues
        # league_ids=[564,384,82,304,1114,38,32,8]
        # league = Leagues.objects.all().filter(league_id__in =  league_ids)
        # serializer = LeaguesPlayerSerializer(league,many=True)
        
        #League From Goal Serve
        league=GatAllActiveLeagueByGoalServe()
        
        return Response({"status": 200, "message": "success", "data":league}, status=200)

@csrf_exempt
def AllPlayerSatistics(request, player_id=None):
    response = get_player_stats(request, player_id=player_id)
    data = {"status": 200, "message": "success", "data": json.loads(response)}
    return JsonResponse(data)

class Competitions(APIView):
    def get(self, request):
        season = Season.objects.all()
        if 'league_id' in request.GET:
            season=season.filter(league_id=request.GET["league_id"])
        if 'season_id' in request.GET:
            season = season.filter(season_id=request.GET["season_id"])
        jsondata = []
        serializer = SeasonSerializer(season, many=True)
        for resp in serializer.data:
            home=eval(resp['home'])
            away=eval(resp['away'])
            total=eval(resp['total'])
            jsondata.append({"no":resp['id'], "name":resp['team_name'],"game_played":home["games_played"],"home_won":home['won'],"home_draw":home['draw'],"home_lost":home['lost'],
                             "away_won":away['won'],"away_draw":away['draw'],"away_lost":away['lost'],"goal_difference":total['goal_difference'],"goal_points":total['points']})
        return Response({"status": 200, "message": "success", "data": jsondata}, status=200)

class HistoricData(APIView):
    def get(self, request):
        from datetime import datetime, timedelta
        queryObj = {
            'time_date__lt': datetime.today()
        }
        match = MatchFixtureUpdate.objects.all()
        if 'league_id' in request.GET:
            match=match.filter(league_id=request.GET["league_id"])
        if 'season_id' in request.GET:
            match=match.filter(season_id=request.GET["season_id"])
        jsondata =[]
        serializer = HistoricDataSerializer(match, many=True)
        # for resp in serializer.data:
        #     dt =''
        #     dc=''
        #     if 'date_time' in resp['time']:
        #         st1 = resp['time'].find("date_time")
        #         dt = resp['time'][st1+13:st1+23]
        #     if 'ht_score' in resp['scores']:
        #         sc1 = resp['scores'].find("ft_score")
        #         dc = resp['scores'][sc1+12:sc1+15]
        #         if dc == 'one':
        #             dc =''
        #     jsondata.append({"league":resp['league']['name'],"season":resp['season'],'date':dt,'score':dc})

        return Response({"status": 200, "message": "success", "data": serializer.data}, status=200)

class ThisweekMatchSchedule(APIView):
    def get(self, request):
        one_week_ago = datetime.today() + timedelta(days=7)
        match = MatchFixtureUpdate.objects.filter(time_date__gte=datetime.today(),time_date__lte=one_week_ago)
        jsondata = []
        serializer =  ThisweekMatchScheduleSerializer(match, many=True)
        for resp in serializer.data:
            dt =''
            dc =''
            if 'date_time' in resp['time']:
                st1 = resp['time'].find("date_time")
                dt = resp['time'][st1+13:st1+23]
            if 'ht_score' in resp['scores']:
                sc1 = resp['scores'].find("ft_score")
                dc = resp['scores'][sc1 + 12:sc1 + 15]
                if dc == 'one':
                    dc = ''
            jsondata.append({"league": resp['league']['name'], "season": resp['season'], 'date': dt, 'score':dc})

        return Response({"status": 200, "message": "success", "data": jsondata}, status=200)

class MatchSchedule(APIView):
    def get(self, request):
        match = MatchFixtureUpdate.objects.all()
        if 'league_id' in request.GET:
            match=match.filter(league_id=request.GET["league_id"])
        if 'season_id' in request.GET:
            match=match.filter(season_id=request.GET["season_id"])
        jsondata =[]
        serializer = MatchScheduleSerializer(match, many=True)
        for resp in serializer.data:
            dt =''
            dc=''
            tm=''
            st=''
            if 'status' in resp['time']:
                st1 = resp['time'].find("status")
                st = resp['time'][st1+10:st1+12]
            if 'date_time' in resp['time']:
                st1 = resp['time'].find("date_time")
                dt = resp['time'][st1+13:st1+23]
            if 'date_time' in resp['time']:
                sm1 = resp['time'].find("date_time")
                tm = resp['time'][sm1+24:sm1+32]
            if 'ht_score' in resp['scores']:
                sc1 = resp['scores'].find("ft_score")
                dc = resp['scores'][sc1+12:sc1+15]
                if dc == 'one':
                    dc =''
            jsondata.append({"no": resp['id'],'date':dt,'score':dc,'time':tm,'status':st})

        return Response({"status": 200, "message": "success", "data": jsondata}, status=200)

@csrf_exempt
def JsonStringToJsonObject(request):
    requestdata = JSONParser().parse(request)
    jsonString = requestdata['jsonstring']

    print(json.load(str(jsonString)))
    return JsonResponse({"status": 200, "message": "success", "data": json.load(str(jsonString))}, status=200)


@csrf_exempt
def AllFixerByLeagueId(request, league_id=None):
    # match = Fixture.objects.all().filter(league_id=league_id)
    # jsondata =[]
    # serializer = FixerSerializer(match, many=True)
    # # print(serializer.data)
    # final_res =[]
    # for index, item in enumerate(serializer.data):
    #     name = item['localteam']['name']+' Vs '+item['visitorteam']['name']
    #     final_res.append({'fixture_id':item['fixture_id'],'name':name})
    queryObj = {}
    queryObj['league_id'] = league_id
    fixtures = MatchGoalserve.objects.all().filter(**queryObj)
    result = MatchGoalserveSerializer(fixtures, many=True).data
    data = {"status": 200, "message": "success", "data":result}
    return JsonResponse(data)

class FootballFixture(APIView):
    def get(self, request):
        fixture = Fixture.objects.all()
        serializer = FixtureSerializer(fixture, many=True)
        return Response({"status": 200, "message": "success", "data": serializer.data}, status=200)

class FootballTeamdetailsByTeamId(APIView):
    def post(self, request):
        instance ={}
        requestdata = JSONParser().parse(request)
        # print(requestdata['team_id'])
        teams = Teams.objects.all().filter(team_id=requestdata['team_id'])
        teamserializer = TeamDetailSerializer(teams, many=True)
        playerinateam = Players.objects.all().filter(team_id=requestdata['team_id'])
        playerdetails = PlayersSerializer(playerinateam, many=True)
        seasons = Season.objects.all().filter(team_id=requestdata['team_id'])
        seasonsserializer = SeasonSerializer(seasons, many=True)

        instance['team'] = teamserializer.data
        instance['playerdetails'] = playerdetails.data
        instance['seasondetails'] = seasonsserializer.data

        return Response({"status": 200, "message": "success", "data": instance}, status=200)


@csrf_exempt
def SeasonList(request, season_id=None):
    if season_id:
        response = get_seasonlist(request, season_id=season_id)
    else:
        response = get_seasonlist(request)
    data = {"status": 200, "message": "success", "data": ''}
    return JsonResponse(data)

@csrf_exempt
#GoalServe API
def SeasonByLeagueId(request, league_id=None):

    season = SeasonGoalserve.objects.all().filter(league_id=league_id,is_standing='0')
    seasonData = SeasonGoalserveSerializer(season, many=True).data
    data = {"status": 200, "message": "success", "data": seasonData}
    return JsonResponse(data)

@csrf_exempt
def GetSessionByLeagueID(request):
    requestdata = JSONParser().parse(request)
    data =[]
    if 'league_id' in requestdata:
        season=Season.objects.all().filter(league_id=requestdata["league_id"])
        serializer = SeasonSerializer(season, many=True)
        data =serializer.data 
    return Response({"status": 200, "message": "success", "data":data}, status=200)

@csrf_exempt
def GetTeam(request):
    result=[]
    from db_table.models import Teams
    league_ids= [1204,1399,1269,1229,1221,1041]
    requestdata = JSONParser().parse(request)
    
    if 'league_id' in requestdata:
        # print(season_search)
        team = TeamStatisticsGoalserve.objects.all().filter(league_ids__contains=requestdata["league_id"])
    else:
        team = TeamStatisticsGoalserve.objects.all().filter(league_ids__contains=1204)
    
    if team:
        result = TeamStatisticsGoalserveSerializer(team, many=True).data
    data ={"status": 200, "message": "success", "data":result}
    return JsonResponse(data)

@csrf_exempt
def GetSeasonByTeamID(request,team_id=None):
    from db_table.models import Season
    GetTeamwiseProbability(team_id)
    season = Season.objects.all().filter(team_id=team_id).order_by('name')
    serializer = SeasonSerializer(season, many=True)
    data ={"status": 200, "message": "success", "data":serializer.data}
    return JsonResponse(data)

@csrf_exempt
def allseasoon(request):
    from db_table.models import AllSeason
    season = AllSeason.objects.all().filter(is_active=True,collection_datasource="www.worldfootball.net")
    serializer = AllSeasonSerializer(season, many=True)
    data ={"status": 200, "message": "success", "data":serializer.data}
    return JsonResponse(data)

@csrf_exempt
def GetLeagues(request, id=None):
    from db_table.models import Leagues
    if id:
        league = Leagues.objects.all().filter(league_id=id).order_by('name')
    else:
        league = Leagues.objects.all().filter(active=True,collection_datasource="www.worldfootball.net")
    serializer = AllLeagueSerializer(league, many=True)
    data ={"status": 200, "message": "success", "data":serializer.data}
    return JsonResponse(data)

@csrf_exempt
def GetLeaguesCountryId(request, country_id=None):
    league = Leagues.objects.all().filter(country_id=country_id).order_by('name')
    serializer = AllLeagueSerializer(league, many=True)
    data ={"status": 200, "message": "success", "data":serializer.data}
    return JsonResponse(data)

@csrf_exempt
def GetSeasonByLeagueID(request,league_id=None):
    from db_table.models import Season
    season = Season.objects.all().filter(league_id=league_id).order_by('name')
    serializer = SeasonSerializer(season, many=True)
    data ={"status": 200, "message": "success", "data":serializer.data}
    return JsonResponse(data)

@csrf_exempt
def AllFixture(request):
    from db_table.models import SeasonMatchPlan
    request_data = JSONParser().parse(request)
    from django.utils.timezone import datetime #important if using timezones
    today = datetime.today()
    
    # print(request_data)
    # response = get_fixturesupdate(request)
    response = {}
    # query OBJ
    queryObj = {}
    
    if 'league_id' in  request_data:
        queryObj['league_id'] = request_data['league_id']
    if 'season_id' in request_data:
        queryObj['season_id'] = request_data['season_id']
    if 'odds_id' in request_data:
        queryObj['odds_id'] = request_data['odds_id']
    if len(queryObj) == 0:
        match = SeasonMatchPlan.objects.all().filter(**queryObj)[:100]
    else:
        match = SeasonMatchPlan.objects.all()[:100]
    final_res =[]
    result = SeasonMatchPlanSerializer(match, many=True).data
    # for index, item in enumerate(result):
    #     ft_scores =''
    #     try:
    #         scores = json.loads(item['scores'])
    #         ft_scores=scores['ft_score']
    #     except:
    #        ft_scores =''

    #     matchdate =''

    #     try:
    #         time = json.loads(item['time'])
    #         matchdate=time['date']
    #     except:
    #        matchdate ='0000-00-00'  
    #     final_res.append({'league_name':item['leage_name'],'season_name':item['season_name'],'match_name':item['match_name'],'home_name':item['localteam_name'],'score':ft_scores,'date':matchdate})

    #     # print(item["winnerteam_id"])
    #     # print(item["visitorteam_id"])
    data = {"status": 200, "message": "success", "data":result}
    return JsonResponse(data)
@csrf_exempt
def Histroydata(request):
    from db_table.models import HistoricData
    request_data = JSONParser().parse(request)
    from django.utils.timezone import datetime #important if using timezones
    today = datetime.today()
    
    # print(request_data)
    # response = get_fixturesupdate(request)
    response = {}
    # query OBJ
    queryObj = {}
    start=0
    end=100
    if 'league' in  request_data:
        queryObj['league'] = request_data['league']
    if 'start' in request_data:
        start = int(request_data['start'])
    if 'end' in request_data:
        end = int(request_data['end'])
    if len(queryObj) == 0:
        match = HistoricData.objects.all().filter(**queryObj)[start:end]
    else:
        match = HistoricData.objects.all()[start:end]
    final_res =[]
    result = HistoricDataSerializer(match, many=True).data
    data = {"status": 200, "message": "success", "data":result}
    return JsonResponse(data)

@csrf_exempt
def GetTeamStatistics(request):
    request_data = JSONParser().parse(request)
    ts = GetTeamStatisticsDetailByteamId(request_data['team_id'])
    data = {"status": 200, "message": "success", "data":ts}
    return JsonResponse(data)

@csrf_exempt
def livescore(request):
    final_res = []
    # request_data = JSONParser().parse(request)
    # league_ids=[1204,1399,1269,1229,1221]  
    # from django.utils.timezone import datetime #important if using timezones
    # today = datetime.today()
    # queryObj = {}
    # queryObj['league_id__in'] =  league_ids
    # queryObj['formated_date']= datetime.today().strftime('%Y-%m-%d')
    # fixtures = MatchGoalserve.objects.all().filter(**queryObj)[:15]
    # result = MatchByTeamGoalserveSerializer(fixtures, many=True).data

    # queryObj['is_active'] = True
    # queryObj['time__contains'] = datetime.today().strftime('%Y-%m-%d')
    # fixer = Fixture.objects.all().filter(**queryObj)
    # result = FixerSerializer(fixer, many=True).data
    
    
    # countryname=["England","Spain", "Italy", "Germany","France"]
    # league_ids=LeagueIdGolaServe()
    # data = GetLiveScore()
    # if data:
    #     for dt in data:
    #         match_name = dt['@name']
    #         # country =dt['@name'].split(":")
    #         # if dt['@gid'] in league_ids:
    #         if 'matches' in dt:
    #             if 'match' in dt['matches'] and type(dt['matches']['match']) is list:
    #                 for match in dt['matches']['match']:
    #                     match_id =  match['@id']
    #                     # print(match['localteam'])
    #                     teamdata1 = GetTeamImageLeagueDetail(match['localteam']['@id'])
    #                     if teamdata1:
    #                         match['localteam']['@image'] =teamdata1['image']
    #                     teamdata2 = GetTeamImageLeagueDetail(match['visitorteam']['@id'])
    #                     if teamdata2:
    #                         match['visitorteam']['@image'] =teamdata2['image']
    #                     match['@match_name'] =match_name
    #                     final_res.append(match)

    #             if 'match' in dt['matches'] and type(dt['matches']['match']) is dict:
    #                 matchD = dt['matches']['match']
    #                 matchD['@match_name'] =match_name
    #                 match_id =  matchD['@id']
    #                 teamdata1 = GetTeamImageLeagueDetail(matchD['localteam']['@id'])
    #                 if teamdata1:
    #                     matchD['localteam']['@image'] =teamdata1['image']
    #                 teamdata2 = GetTeamImageLeagueDetail(matchD['visitorteam']['@id'])
    #                 if teamdata2:
    #                     matchD['visitorteam']['@image'] =teamdata2['image']
    #                 final_res.append(matchD)
    res=redis_instance.get('DailySummery')
    if res:
        final_res=json.loads(res)
    print(final_res)
    data ={"status": 200, "message": "success", "data":final_res}
    return JsonResponse(data)

@csrf_exempt
def StoreLeagueOtherDataSource(request):
    request_data = JSONParser().parse(request)
    from db_table.models import Leagues
    print(request_data)
    Leagues.objects.create(
        league_id=request_data["league_id"],
        logo_path=request_data["logo_path"],
        name=request_data["name"],
        league_dname=request_data["league_dname"],
        slug_name=request_data["slug_name"],
        collection_datasource=request_data["collection_datasource"]
    )
    data ={"status": 200, "message": "success", "data":''}
    return JsonResponse(data)

@csrf_exempt
def StoreTeamOtherDataSource(request):
    # request_data = JSONParser().parse(request)
    from db_table.models import Teams
    myresult = storeTeam()
    for result in myresult:
        request_data = {'team_id':result[0],'name':result[1],'team_name_odd':result[2],'logo_path':result[3],'league_id':result[4],'collection_datasource':'www.worldfootball.net'}
        # print(PARAMS)
        # print(request_data)
        cnt = Teams.objects.filter(team_id=request_data["team_id"],collection_datasource=request_data["collection_datasource"]).count()
        if cnt == 0:
            Teams.objects.create(
                team_id=request_data["team_id"],
                logo_path=request_data["logo_path"],
                name=request_data["name"],
                team_name_odd=request_data["team_name_odd"],
                league_id=request_data["league_id"],
                collection_datasource=request_data["collection_datasource"]
            )
    data ={"status": 200, "message": "success", "data":''}
    return JsonResponse(data)
@csrf_exempt
def StoreSeasonOtherDataSource(request):
    request_data = JSONParser().parse(request)
    from db_table.models import AllSeason
    print(request_data)
    cnt = AllSeason.objects.filter(season_id=request_data["season_id"],collection_datasource=request_data["collection_datasource"]).count()
    if cnt == 0:
        AllSeason.objects.create(
            id=request_data["season_id"],
            season_id=request_data["season_id"],
            name=request_data["season_title"],
            collection_datasource=request_data["collection_datasource"]
        )
    data ={"status": 200, "message": "success", "data":''}
    return JsonResponse(data)
@csrf_exempt
def StoreSeasonMatchPlanOtherDataSource(request):
    request_data = JSONParser().parse(request)
    from db_table.models import SeasonMatchPlan
    print(request_data)
    cnt = SeasonMatchPlan.objects.filter(match_id=request_data["match_id"],collection_datasource=request_data["collection_datasource"]).count()
    if cnt == 0:
        SeasonMatchPlan.objects.create(
            match_id =request_data["match_id"],
            season_id =request_data["season_id"],
            league_id =request_data["league_id"],
            date=request_data["date"],
            time =request_data["time"],
            home_team_id =request_data["home_team_id"],
            away_team_id =request_data["away_team_id"],
            total_home_score =request_data["total_home_score"],
            half_home_score =request_data["half_home_score"],
            total_away_score =request_data["total_away_score"],
            half_away_score=request_data["half_away_score"],
            status =request_data["status"],
            Home_TGPR =request_data["Home_TGPR"],
            Away_TGPR=request_data["Away_TGPR"],
            D_Home_RS_8=request_data["D_Home_RS_8"],
            D_Home_ranking_8 =request_data["D_Home_ranking_8"],
            D_Home_RS_6 =request_data["D_Home_RS_6"],
            D_Home_ranking_6=request_data["D_Home_ranking_6"],
            home_team_score =request_data["home_team_score"],
            home_team_strength=request_data["home_team_strength"],
            away_team_score =request_data["away_team_score"],
            away_team_strength =request_data["away_team_strength"],
            D_Away_RS_8 =request_data["D_Away_RS_8"],
            D_Away_ranking_8=request_data["D_Away_ranking_8"],
            D_Away_RS_6=request_data["D_Away_RS_6"],
            D_Away_ranking_6=request_data["D_Away_ranking_6"],
            HPPG=request_data["HPPG"],
            HGDPG =request_data["HGDPG"],
            APPG=request_data["APPG"],
            AGDPG =request_data["AGDPG"],
            WN =request_data["WN"],
            c_WN =request_data["c_WN"],
            DSL_refer_id =request_data["DSL_refer_id"],
            DCL_refer_id=request_data["DCL_refer_id"],
            CL_mo_refer_id =request_data["CL_mo_refer_id"],
            collection_datasource=request_data["collection_datasource"]
        )
    data ={"status": 200, "message": "success", "data":''}
    return JsonResponse(data)

@csrf_exempt
def StoreMatchTeamPlayerInfoOtherDataSource(request):
    request_data = JSONParser().parse(request)
    from db_table.models import MatchTeamPlayerInfo
    print(request_data)
    cnt = MatchTeamPlayerInfo.objects.filter(id=request_data["id"],collection_datasource=request_data["collection_datasource"]).count()
    if cnt == 0:
        MatchTeamPlayerInfo.objects.create(
            id=request_data["id"],
            match_id=request_data["match_id"],
            team_id=request_data["team_id"],
            player_id=request_data["player_id"],
            goals=request_data["goals"],
            assists=request_data["assists"],
            collection_datasource=request_data["collection_datasource"]
        )
    data ={"status": 200, "message": "success", "data":''}
    return JsonResponse(data)

@csrf_exempt
def StorePlayerCareerOtherDataSource(request):
    request_data = JSONParser().parse(request)
    from db_table.models import PlayerCareer
    print(request_data)
    cnt = PlayerCareer.objects.filter(id=request_data["id"],collection_datasource=request_data["collection_datasource"]).count()
    if cnt == 0:
        PlayerCareer.objects.create(
            id=request_data["id"],
            player_id=request_data["player_id"],
            flag=request_data["flag"],
            team_id=request_data["team_id"],
            matches=request_data["matches"],
            goals=request_data["goals"],
            started=request_data["started"],
            s_in=request_data["s_in"],
            s_out=request_data["s_out"],
            yellow=request_data["yellow"],
            s_yellow=request_data["s_yellow"],
            red=request_data["red"],
            collection_datasource=request_data["collection_datasource"]
        )
    data ={"status": 200, "message": "success", "data":''}
    return JsonResponse(data)

@csrf_exempt
def StorePlayerListOtherDataSource(request):
    from db_table.models import PlayerList
    data = storePlayerList()
    print(data)
    for result in data:
        
        request_data = {
          'player_id' :result[0] if result[0]  else 0,
          'player_name' :result[1] if result[1]  else '',
          'birthday' :str(result[2]) if result[2]  else '',
          'nationality' :result[3] if result[3]  else '',
          'img_src' :result[4] if result[4]  else '',
          'height' :result[5] if result[5]  else '',
          'weight' :result[6] if result[6]  else '',
          'foot' :result[7] if result[7]  else '',
          'position' :result[8] if result[8]  else '',
          'now_team_id' :result[9] if result[9]  else 0,
          'now_pNumber' :result[10] if result[10]  else 0,
          'collection_datasource':'www.worldfootball.net'
        }
        print(request_data)
        cnt = PlayerList.objects.filter(player_id=request_data["player_id"],collection_datasource=request_data["collection_datasource"]).count()
        if cnt == 0:
            PlayerList.objects.create(
                player_id=request_data["player_id"],
                player_name=request_data["player_name"],
                birthday=request_data["birthday"],
                nationality=request_data["nationality"],
                img_src=request_data["img_src"],
                height=request_data["height"],
                weight=request_data["weight"],
                foot=request_data["foot"],
                position=request_data["position"],
                now_team_id=request_data["now_team_id"],
                now_pNumber=request_data["now_pNumber"],
                collection_datasource=request_data["collection_datasource"]
            )
        
    # from db_table.models import PlayerList
    # print(request_data)
    
    data ={"status": 200, "message": "success", "data":''}
    return JsonResponse(data)

@csrf_exempt
def StoreSeasonLeagueTeamInfoOtherDataSource(request):
    request_data = JSONParser().parse(request)
    from db_table.models import SeasonLeagueTeamInfo
    print(request_data)
    cnt = SeasonLeagueTeamInfo.objects.filter(info_id=request_data["info_id"],collection_datasource=request_data["collection_datasource"]).count()
    if cnt == 0:
        SeasonLeagueTeamInfo.objects.create(
            info_id = request_data["info_id"],
            season_id = request_data["season_id"],
            league_id = request_data["league_id"],
            team_id = request_data["team_id"],
            t_mp = request_data["t_mp"],
            t_w = request_data["t_w"],
            t_d = request_data["t_d"],
            t_l = request_data["t_l"],
            t_f = request_data["t_f"],
            t_a = request_data["t_a"],
            h_mp = request_data["h_mp"],
            h_w = request_data["h_w"],
            h_d = request_data["h_d"],
            h_l = request_data["h_l"],
            h_f = request_data["h_f"],
            h_a = request_data["h_a"],
            a_mp = request_data["a_mp"],
            a_w = request_data["a_w"],
            a_d = request_data["a_d"],
            a_l = request_data["a_l"],
            a_f = request_data["a_f"],
            D = request_data["D"],
            P = request_data["P"],
            PPG = request_data["PPG"],
            HPPG = request_data["HPPG"],
            H_percent = request_data["H_percent"],
            HG = request_data["HG"],
            HDGPG = request_data["HDGPG"],
            HRS = request_data["HRS"],
            APPG = request_data["APPG"],
            A_percent = request_data["A_percent"],
            AG = request_data["AG"],
            ADGPG = request_data["ADGPG"],
            ARS = request_data["ARS"],
            S_H_ranking = request_data["S_H_ranking"],
            S_A_ranking = request_data["S_A_ranking"],
            collection_datasource=request_data["collection_datasource"]
        )
    data ={"status": 200, "message": "success", "data":''}
    return JsonResponse(data)

def GetTeamwiseProbability(team_id):
    team = Teams.objects.all().filter(team_id=team_id,collection_datasource="www.worldfootball.net").first()
    result = SeasonLeagueTeamInfo.objects.filter(team_id = team_id).values('team_id').order_by('team_id').annotate(total_match=Sum('t_mp')).annotate(total_win=Sum('t_w')).annotate(total_loss=Sum('t_l')).annotate(total_drow=Sum('t_d'))
    pd = result[0]['total_drow'] *100 /result[0]['total_match']
    pl = result[0]['total_loss'] *100/result[0]['total_match']
    pw = result[0]['total_win'] *100/result[0]['total_match']
    res ={}
    res['total_draw'] = result[0]['total_drow']
    res['total_match'] = result[0]['total_match']
    res['total_loss'] = result[0]['total_loss']
    res['total_win'] = result[0]['total_win']
    res['Pwin'] = "{:.2f}".format(pw)           #Win Probability
    res['Plost'] = "{:.2f}".format(pl)          #Lost Probability
    res['Pdraw'] = "{:.2f}".format(pd)          #Draw Probability
    res['team_name']= team.name
    # print(pd)
    # print(pl)
    # print(pw)
    return res

@csrf_exempt
def OvaralTeamPlayer(request):
    request_data = JSONParser().parse(request)
    response = {}
    final_res = []
    fixer = MatchFixtureUpdate.objects.filter(\
        (Q(localteam_id=request_data['team_id']) | Q(visitorteam_id=request_data['team_id']))).all()
    result = OvaralTeamTeamDetailSerializer(fixer, many=True).data

    data ={"status": 200, "message": "success", "data":result}
    for index, item in enumerate(result):
        # print(item['localteam_id'])
        rec =[]
        if item['localteam_id'] != request_data['team_id']:
            item['team_name'] = item['localteam_name']
            teamstatistic = TeamStatsDetails.objects.filter(team_id=item['localteam_id']).all()
            ptotal = 0
            wtotal =0
            dtotal = 0
            ltotal = 0
            GFtotal =0
            GLtotal =0
            if teamstatistic:
                rec = TeamStatsDetailsSerializer(teamstatistic, many=True).data
                
                for index, dt in enumerate(rec):

                    w_json_object = json.loads(dt['win'])
                    if 'total' in w_json_object:
                        ptotal = ptotal+ int(w_json_object["total"])
                    d_json_object = json.loads(dt['draw'])
                    if 'total' in d_json_object:
                        ptotal = ptotal+ int(d_json_object["total"])
                    l_json_object = json.loads(dt['lost'])
                    if 'total' in l_json_object:
                        ptotal = ptotal+ int(l_json_object["total"])
                    
                    GF_json_object = json.loads(dt['goals_for'])
                    GA_json_object = json.loads(dt['goals_against'])
                    GFtotal = GFtotal + int(GF_json_object["total"])
                    GLtotal = GLtotal + int(GA_json_object["total"])
                    wtotal =  wtotal + int(w_json_object["total"])
                    dtotal = dtotal+ int(d_json_object["total"])
                    ltotal = dtotal+ int(l_json_object["total"])
                    
            item['playertot'] = ptotal 
            item['GDTotal'] = GFtotal-GLtotal
            item['PointTotal'] = (wtotal *3) + dtotal
            item['playerwin'] = wtotal 
            item['playerdraw'] = dtotal 
            item['playerlost'] = ltotal 

        if item['visitorteam_id'] != request_data['team_id']:
            item['team_name'] = item['visitorteam_name']
            teamstatistic = TeamStatsDetails.objects.filter(team_id=item['visitorteam_id']).all()
            ptotal = 0
            wtotal =0
            dtotal = 0
            ltotal = 0
            GFtotal =0
            GLtotal =0
            if teamstatistic:
                rec = TeamStatsDetailsSerializer(teamstatistic, many=True).data
                
                for index, dt in enumerate(rec):

                    w_json_object = json.loads(dt['win'])
                    if 'total' in w_json_object:
                        ptotal = ptotal+ int(w_json_object["total"])
                    d_json_object = json.loads(dt['draw'])
                    if 'total' in d_json_object:
                        ptotal = ptotal+ int(d_json_object["total"])
                    l_json_object = json.loads(dt['lost'])
                    if 'total' in l_json_object:
                        ptotal = ptotal+ int(l_json_object["total"])
                    GF_json_object = json.loads(dt['goals_for'])
                    GA_json_object = json.loads(dt['goals_against'])
                    GFtotal = GFtotal + int(GF_json_object["total"])
                    GLtotal = GLtotal + int(GA_json_object["total"])
                    wtotal =  wtotal + int(w_json_object["total"])
                    dtotal = dtotal+ int(d_json_object["total"])
                    ltotal = dtotal+ int(l_json_object["total"])
                    
            item['playertot'] = ptotal 
            item['GDTotal'] = GFtotal-GLtotal
            item['PointTotal'] = (wtotal *3) + dtotal
            item['playerwin'] = wtotal 
            item['playerdraw'] = dtotal 
            item['playerlost'] = ltotal 
    
    return JsonResponse(data)

@csrf_exempt
def LoanInByTeam(request):
    request_data = JSONParser().parse(request)
    response = {}
    final_res = []
    
    team = Teams.objects.all().filter(team_id = request_data['team_id'])
    for item in team:
        # if item.collection_datasource != None:
            # if item.collection_datasource == 'www.worldfootball.net':
        team_name = item.name
        # print(team_name)
        # print(item.collection_datasource)
        teamid=Teams.objects.filter(\
                Q(collection_datasource='www.worldfootball.net'),\
                (
                    Q(name=team_name) \
                    | Q(team_name_odd=team_name)
                )
            )
        for ret in teamid:            
            print(ret.team_id)
            print("111111111")
            player_list = PlayerList.objects.all().filter(now_team_id = now_team_id)
            for indx, rec in enumerate(player_list):            
                print(rec)
                print("222222222222")
    data ={"status": 200, "message": "success", "data":''}
    return JsonResponse(data)

@csrf_exempt
def ScrapToolForVisiter(request):
    
    response = {}
    final_res = []
    scrap_list = ScrapTool.objects.all()
    result = ScrapToolSerializer(scrap_list, many=True).data
    data ={"status": 200, "message": "success", "data":result}
    return JsonResponse(data)

@csrf_exempt
def ScrapTooldownload(request,slug):
    # This action requires the 'csv' module
    import csv
    import numpy as np
    import csv
    import re
    header_array = []
    scrap_list = ScrapTool.objects.all().filter(slug=slug)
    listrow =[]
    result = json.loads(scrap_list[0].scrap_return_reult)
    # print(result)
    if scrap_list[0].scrap_type == 'HTML':
        
        # print(result)
        for res in enumerate(result):
            
            for rec in res:

                if isinstance(rec, int):
                     print('')
                else:
                    # print(len(rec))
                    # print(rec)
                    single_row =[]

                    for data in rec:
                        # print(data['field_name'])
                        if len(data) >0 :
                            
                            if data['field_name'] :

                                header_array.append(data['field_name'])
                                single_row.append(re.sub(r'\s', '', data['value']))
                        
                    if len(single_row) >0:
                        listrow.append(single_row)
        with open("static/export.csv", 'w') as csvfile: 
            csvwriter = csv.writer(csvfile) 
            csvwriter.writerow(header_array) 
            csvwriter.writerows(listrow)       
  
    from django.shortcuts import redirect
    response = redirect('http://44.195.135.131:8000/static/export.csv')
    return response

@csrf_exempt
def SaveScrapingData(request):
    print(request.POST)
    # request_data = JSONParser().parse(request)
    # data =ScrapTool(scrap_type=request.POST['scrap_type'],exemptColumn=request.POST['exemptColumn'],slug=unique_slug_generator(request.POST['scrapname']),scrapname=request.POST['scrapname'],scrap_url=request.POST['scrap_url'],scrap_element_class=request.POST['scrap_element_class'],scrap_element_type=request.POST['scrap_element_type'])
    # data.save()
    array =[2022,2021,2020,2019,2018,2017,2016,2015,2014]
    iid= 872
    for arr in array:

        AllSeason.objects.create(season_id=iid,name=arr,collection_datasource='www.soccerstats.com')
        iid = iid+1
    data ={"status": 200, "message": "success"}
    return JsonResponse(data)

def unique_slug_generator(scrapname,new_slug = None): 
    if new_slug is not None: 
        slug = new_slug 
    else: 
        slug = slugify(scrapname) 
    qs_exists = ScrapTool.objects.filter(slug = slug).exists() 
      
    if qs_exists: 
        new_slug = "{slug}-{randstr}".format( 
            slug = slug, randstr = random_string_generator(size = 4)) 
              
        return unique_slug_generator(scrapname, new_slug = new_slug) 
    return slug  
def random_string_generator(size = 10, chars = string.ascii_lowercase + string.digits): 
    return ''.join(random.choice(chars) for _ in range(size)) 
@csrf_exempt
def RunScrapingScriptOuterPage(request,slug):
    
    scrap_list = ScrapTool.objects.filter(slug=slug).first()
    scrap_url = scrap_list.scrap_url
    scrap_element_class = scrap_list.scrap_element_class
    scrap_type =scrap_list.scrap_type
    scrap_element_type = scrap_list.scrap_element_type
    arr=[]
    exemptColumn = scrap_list.exemptColumn
    if scrap_list.exemptColumn:
        arr=exemptColumn.split(',')
    # print(scrap_url)
    # print(scrap_element_class)
    # print("---------------")
    data = ScrapData(scrap_url,scrap_element_class,arr,scrap_type,scrap_element_type)
    if data:
        ScrapTool.objects.filter(slug=slug).update(scrap_return_reult=json.dumps(data))
        
    # ScrapTool.objects.create(
    #   scrapname=request.POST['scrapname'],
    #   scrap_url=request.POST['scrap_url'],
    #   scrap_element_class=request.POST['scrap_element_class']
    # )

    data ={"status": 200, "message": "success"}
    return JsonResponse(data)

@csrf_exempt
def ScrapFromSoccerstats(request):
    # from db_table.models import Leagues
    # # league_list = Leagues.objects.filter(collection_datasource="www.soccerstats.com").all()
    # # for row in league_list:
    # #     Leagues.objects.filter(id=row.id).update(league_id=row.id)
    # # SaveLeagueSoccerstats()
    # league_list = Leagues.objects.filter(collection_datasource="www.soccerstats.com",league_id__gt=1749).all()
    # i =0
    # for resp in league_list:
    #     print(resp.slug_name)
    #     scrap_url = 'https://www.soccerstats.com/homeaway.asp?league='+resp.slug_name
    #     scrap_element_class = 'h2h-team1'
    #     scrap_type ='html'
    #     scrap_element_type = 'id'
    #     arr=[]
    #     exemptColumn = 1
    #     myrec =[]
    #     # arr=exemptColumn.split(',')
    #     print(scrap_url)

    #     data = ScrapDatasoccerstats(scrap_url,scrap_element_class,arr,scrap_type,scrap_element_type)
    #     insertHomeAway(data,'home',resp.league_id)
    #     scrap_element_class = 'h2h-team2'
    #     data = ScrapDatasoccerstats(scrap_url,scrap_element_class,arr,scrap_type,scrap_element_type)
    #     insertHomeAway(data,'away',resp.league_id)


    # Update Team and Slug
    from db_table.models import HomeAwayTeamByLeague
    hatl_list = HomeAwayTeamByLeague.objects.filter(collection_datasource="www.soccerstats.com").all()
    for row in hatl_list:
        slug= unique_slug_generator(row.team_name)
        print(slug)
        HomeAwayTeamByLeague.objects.filter(id=row.id).update(team_id=row.id,team_slug = slug)
    data ={"status": 200, "message": "success"}
    return JsonResponse(data)

def insertHomeAway(data,team_type,league_id):
    if data:
        for rec in data:
            # print("/////////////////")
            # print(rec)
            league_name =''
            gp =''
            w=''
            d=''
            l=''
            gf=''
            ga=''
            gd=''
            pts =''
            
            team_name = rec[1][0]['text']['value']
            gp =  rec[2][0]['text']['value']
            w =  rec[3][0]['text']['value']
            d =  rec[4][0]['text']['value']
            l =  rec[5][0]['text']['value']
            gf =  rec[6][0]['text']['value']
            ga =  rec[7][0]['text']['value']
            gd =  rec[8][0]['text']['value']
            pts =  rec[9][0]['text']['value']
            league_id = league_id
            team_type = team_type
            HomeAwayTeamByLeague.objects.create(
                league_id=league_id,
                team_type=team_type,
                team_name=team_name,
                gp=gp,
                w=w,
                d=d,
                l=l,
                gf=gf,
                ga=ga,
                gd=gd,
                pts=pts,
                collection_datasource='www.soccerstats.com'
            )
    return 1
               
def SaveLeagueSoccerstats():
    from db_table.models import Leagues
    scrap_url = 'https://www.soccerstats.com/leagues.asp'
    scrap_element_class = 'sortable'
    scrap_type ='html'
    scrap_element_type = 'class'
    arr=[]
    
    myrec =[]
    data = ScrapData(scrap_url,scrap_element_class,arr,scrap_type,scrap_element_type)
    # print(data)
    for rec in data:
        # print(rec)
        insertArr=[]
        i =0
        league_image =''
        league_text=''
        league_href=''
        for res in rec:
            print(res)
            if i < 2:
                if i ==0:
                    league_image = res[0]['image']['value']
                    league_text = res[0]['text']['value']
                if i ==1:
                    league_href = res[0]['href']['value']
            i = i+1

                   
        if league_href !='':
            val=league_href.split('=')
            league_href1 = val[1]
            Leagues.objects.create(
                logo_path=league_image,
                name=league_text,
                league_dname=league_href1,
                slug_name=league_href1,
                collection_datasource='www.soccerstats.com'
            )

    return 0

@csrf_exempt
def saveScrapData(request):
    # for row in Teams.objects.all().filter(collection_datasource='www.soccerstats.com'):
    #     row.delete()
    from db_table.models import Leagues
    arrayTeam =[{'value':'Vllaznia S. (ALBANIA)','data':'8'},{'value':'Egnatia R. (ALBANIA)','data':'3'},{'value':'Dinamo Tirana (ALBANIA)','data':'6'},{'value':'Skenderbeu K. (ALBANIA)','data':'2'},{'value':'Teuta Durres (ALBANIA)','data':'9'},{'value':'Partizani T. (ALBANIA)','data':'10'},{'value':'Kastrioti Kruje (ALBANIA)','data':'5'},{'value':'Laci (ALBANIA)','data':'7'},{'value':'Kukesi (ALBANIA)','data':'4'},{'value':'Tirana (ALBANIA)','data':'1'},{'value':'Vora (ALBANIA2)','data':'4'},{'value':'Lushnja (ALBANIA2)','data':'6'},{'value':'Turbina Cerrik (ALBANIA2)','data':'14'},{'value':'Flamurtari (ALBANIA2)','data':'13'},{'value':'Luftetari G. (ALBANIA2)','data':'12'},{'value':'Pogradeci (ALBANIA2)','data':'12'},{'value':'Erzeni Shijak (ALBANIA2)','data':'2'},{'value':'Elbasani (ALBANIA2)','data':'9'},{'value':'Veleciku Koplik (ALBANIA2)','data':'8'},{'value':'Burreli (ALBANIA2)','data':'8'},{'value':'Apolonia Fier (ALBANIA2)','data':'1'},{'value':'Korabi Peshkopi (ALBANIA2)','data':'10'},{'value':'Bylis (ALBANIA2)','data':'16'},{'value':'Beselidhja L. (ALBANIA2)','data':'15'},{'value':'Partizani T. B (ALBANIA2)','data':'17'},{'value':'Shkumbini Peqin (ALBANIA2)','data':'3'},{'value':'Tomori Berat (ALBANIA2)','data':'9'},{'value':'Maliqi (ALBANIA2)','data':'5'},{'value':'Tërbuni Pukë (ALBANIA2)','data':'7'},{'value':'B. Sarande (ALBANIA2)','data':'11'},{'value':'Oriku (ALBANIA2)','data':'6'},{'value':'Besa Kavaje (ALBANIA2)','data':'13'},{'value':'USM Alger (ALGERIA)','data':'4'},{'value':'RC Relizane (ALGERIA)','data':'17'},{'value':'Paradou AC (ALGERIA)','data':'9'},{'value':'JS Kabylie (ALGERIA)','data':'12'},{'value':'CR Belouizdad (ALGERIA)','data':'14'},{'value':'NC Magra (ALGERIA)','data':'6'},{'value':'ASO Chlef (ALGERIA)','data':'10'},{'value':'Olympique Medea (ALGERIA)','data':'15'},{'value':'JS Saoura (ALGERIA)','data':'11'},{'value':'MC Oran (ALGERIA)','data':'2'},{'value':'US Biskra (ALGERIA)','data':'8'},{'value':'MC Alger (ALGERIA)','data':'16'},{'value':'Tlemcen (ALGERIA)','data':'5'},{'value':'Chelghoum (ALGERIA)','data':'18'},{'value':'Hussein Dey (ALGERIA)','data':'3'},{'value':'RC Arbaa (ALGERIA)','data':'7'},{'value':'CS Constantine (ALGERIA)','data':'1'},{'value':'ES Setif (ALGERIA)','data':'13'},{'value':'RC Kouba (ALGERIA2)','data':'19'},{'value':'MSP Batna (ALGERIA2)','data':'6'},{'value':'MO Constantine (ALGERIA2)','data':'26'},{'value':'Lakhdaria (ALGERIA2)','data':'7'},{'value':'Khenchela (ALGERIA2)','data':'6'},{'value':'Msila (ALGERIA2)','data':'21'},{'value':'USM Blida (ALGERIA2)','data':'17'},{'value':'CR Béni Thour (ALGERIA2)','data':'14'},{'value':'Amal Bou Saada (ALGERIA2)','data':'18'},{'value':'CA Batna (ALGERIA2)','data':'31'},{'value':'Aïn Defla (ALGERIA2)','data':'17'},{'value':'Teleghma (ALGERIA2)','data':'29'},{'value':'US Chaouia (ALGERIA2)','data':'27'},{'value':'Arzew (ALGERIA2)','data':'26'},{'value':'IRB El Kerma (ALGERIA2)','data':'30'},{'value':'Oued Rhiou (ALGERIA2)','data':'32'},{'value':'Bel Abbes (ALGERIA2)','data':'10'},{'value':'Tiaret (ALGERIA2)','data':'24'},{'value':'Ouled Djellal (ALGERIA2)','data':'4'},{'value':'Khemis Melina (ALGERIA2)','data':'16'},{'value':'JSM Skikda (ALGERIA2)','data':'28'},{'value':'Oued Sly (ALGERIA2)','data':'21'},{'value':'Mlila (ALGERIA2)','data':'8'},{'value':'WA Boufarik (ALGERIA2)','data':'9'},{'value':'CABB Areridj (ALGERIA2)','data':'2'},{'value':'Remchi (ALGERIA2)','data':'33'},{'value':'MO Bejaia (ALGERIA2)','data':'1'},{'value':'Ben Aknoun (ALGERIA2)','data':'20'},{'value':'Hamra Annaba (ALGERIA2)','data':'3'},{'value':'RB Ouargla (ALGERIA2)','data':'4'},{'value':'USMM Hadjout (ALGERIA2)','data':'11'},{'value':'GC Mascara (ALGERIA2)','data':'12'},{'value':'JS Bordj Ménaïe (ALGERIA2)','data':'25'},{'value':'Khroub (ALGERIA2)','data':'7'},{'value':'Annaba (ALGERIA2)','data':'30'},{'value':'Ain Ouessar (ALGERIA2)','data':'22'},{'value':'JSM Bejaia (ALGERIA2)','data':'32'},{'value':'ASM Oran (ALGERIA2)','data':'13'},{'value':'Temouchent (ALGERIA2)','data':'18'},{'value':'El Eulma (ALGERIA2)','data':'5'},{'value':'El Harrach (ALGERIA2)','data':'14'},{'value':'MC Saida (ALGERIA2)','data':'23'},{'value':'Tadjenanet (ALGERIA2)','data':'12'},{'value':'El Bayadh (ALGERIA2)','data':'15'},{'value':'ASO Chlef U21 (ALGERIA3)','data':'18'},{'value':'O. Medea U21 (ALGERIA3)','data':'15'},{'value':'Saoura U21 (ALGERIA3)','data':'13'},{'value':'Mlila U21 (ALGERIA3)','data':'19'},{'value':'Belouizdad U21 (ALGERIA3)','data':'12'},{'value':'RC Arbaa U21 (ALGERIA3)','data':'3'},{'value':'Magra U21 (ALGERIA3)','data':'8'},{'value':'Bel Abbes U21 (ALGERIA3)','data':'11'},{'value':'Chelghoum U21 (ALGERIA3)','data':'10'},{'value':'MC Oran U21 (ALGERIA3)','data':'2'},{'value':'Constantine U21 (ALGERIA3)','data':'1'},{'value':'Tlemcen U21 (ALGERIA3)','data':'7'},{'value':'RC Relizane U21 (ALGERIA3)','data':'14'},{'value':'USM Alger U21 (ALGERIA3)','data':'6'},{'value':'Hussein Dey U21 (ALGERIA3)','data':'5'},{'value':'ES Setif U21 (ALGERIA3)','data':'9'},{'value':'JS Kabylie U21 (ALGERIA3)','data':'16'},{'value':'Bordj B. A. U21 (ALGERIA3)','data':'8'},{'value':'Biskra U21 (ALGERIA3)','data':'4'},{'value':'Skikda U21 (ALGERIA3)','data':'10'},{'value':'MC Alger U21 (ALGERIA3)','data':'11'},{'value':'Paradou U21 (ALGERIA3)','data':'17'},{'value':'Platense (ARGENTINA)','data':'12'},{'value':'Sarmiento (ARGENTINA)','data':'3'},{'value':'Racing Club (ARGENTINA)','data':'14'},{'value':'Independiente (ARGENTINA)','data':'21'},{'value':'Banfield (ARGENTINA)','data':'24'},{'value':'River Plate (ARGENTINA)','data':'19'},{'value':'Godoy Cruz (ARGENTINA)','data':'25'},{'value':'Rosario Central (ARGENTINA)','data':'26'},{'value':'Argentinos Jrs (ARGENTINA)','data':'22'},{'value':'Newells (ARGENTINA)','data':'7'},{'value':'Boca Juniors (ARGENTINA)','data':'2'},{'value':'Aldosivi (ARGENTINA)','data':'5'},{'value':'Estudiantes (ARGENTINA)','data':'4'},{'value':'Velez Sarsfield (ARGENTINA)','data':'13'},{'value':'A. Tucuman (ARGENTINA)','data':'10'},{'value':'Central Cordoba (ARGENTINA)','data':'23'},{'value':'San Lorenzo (ARGENTINA)','data':'18'},{'value':'Union Santa Fe (ARGENTINA)','data':'1'},{'value':'Gimnasia (ARGENTINA)','data':'11'},{'value':'Patronato (ARGENTINA)','data':'6'},{'value':'Huracan (ARGENTINA)','data':'15'},{'value':'Arsenal Sarandi (ARGENTINA)','data':'17'},{'value':'Colon (ARGENTINA)','data':'20'},{'value':'Defensa y J. (ARGENTINA)','data':'16'},{'value':'Lanus (ARGENTINA)','data':'9'},{'value':'T. de Cordoba (ARGENTINA)','data':'8'},{'value':'I. Rivadavia (ARGENTINA2)','data':'10'},{'value':'Guillermo Brown (ARGENTINA2)','data':'22'},{'value':'Gimnasia Jujuy (ARGENTINA2)','data':'14'},{'value':'Brown de A. (ARGENTINA2)','data':'21'},{'value':'Almirante Brown (ARGENTINA2)','data':'15'},{'value':'D. de Belgrano (ARGENTINA2)','data':'5'},{'value':'Instituto (ARGENTINA2)','data':'6'},{'value':'Tristan Suarez (ARGENTINA2)','data':'32'},{'value':'Villa Dálmine (ARGENTINA2)','data':'9'},{'value':'A. Rafaela (ARGENTINA2)','data':'2'},{'value':'SM San Juan (ARGENTINA2)','data':'1'},{'value':'Temperley (ARGENTINA2)','data':'35'},{'value':'All Boys (ARGENTINA2)','data':'17'},{'value':'D. Santa Marina (ARGENTINA2)','data':'13'},{'value':'Barracas C. (ARGENTINA2)','data':'8'},{'value':'Tigre (ARGENTINA2)','data':'20'},{'value':'E. Rio Cuarto (ARGENTINA2)','data':'23'},{'value':'Deportivo Maipu (ARGENTINA2)','data':'24'},{'value':'San Telmo (ARGENTINA2)','data':'7'},{'value':'G. Mendoza (ARGENTINA2)','data':'11'},{'value':'Agropecuario (ARGENTINA2)','data':'12'},{'value':'D. Riestra (ARGENTINA2)','data':'29'},{'value':'CA Guemes (ARGENTINA2)','data':'27'},{'value':'Belgrano (ARGENTINA2)','data':'19'},{'value':'Almagro (ARGENTINA2)','data':'31'},{'value':'SM Tucuman (ARGENTINA2)','data':'25'},{'value':'Alvarado (ARGENTINA2)','data':'26'},{'value':'E. Caseros (ARGENTINA2)','data':'16'},{'value':'Nueva Chicago (ARGENTINA2)','data':'3'},{'value':'Atletico Mitre (ARGENTINA2)','data':'4'},{'value':'Chacarita J. (ARGENTINA2)','data':'33'},{'value':'Atlanta (ARGENTINA2)','data':'34'},{'value':'Deportivo Morón (ARGENTINA2)','data':'18'},{'value':'Ferro Carril (ARGENTINA2)','data':'28'},{'value':'Quilmes (ARGENTINA2)','data':'30'},{'value':'V. San Carlos (ARGENTINA4)','data':'8'},{'value':'Canuelas (ARGENTINA4)','data':'7'},{'value':'Deportivo Merlo (ARGENTINA4)','data':'1'},{'value':'Defensores U. (ARGENTINA4)','data':'10'},{'value':'Acassuso (ARGENTINA4)','data':'9'},{'value':'Sacachispas (ARGENTINA4)','data':'11'},{'value':'Flandria (ARGENTINA4)','data':'15'},{'value':'San Miguel (ARGENTINA4)','data':'5'},{'value':'Fenix (ARGENTINA4)','data':'12'},{'value':'JJ Urquiza (ARGENTINA4)','data':'3'},{'value':'Comunicaciones (ARGENTINA4)','data':'2'},{'value':'UAI Urquiza (ARGENTINA4)','data':'6'},{'value':'Colegiales (ARGENTINA4)','data':'4'},{'value':'T. Remedios (ARGENTINA4)','data':'17'},{'value':'Los Andes (ARGENTINA4)','data':'14'},{'value':'A. Quilmes (ARGENTINA4)','data':'13'},{'value':'D. Armenio (ARGENTINA4)','data':'16'},{'value':'Real Pilar (ARGENTINA6)','data':'5'},{'value':'D. Laferrere (ARGENTINA6)','data':'1'},{'value':'G. Lamadrid (ARGENTINA6)','data':'7'},{'value':'Dock Sud (ARGENTINA6)','data':'20'},{'value':'Argentino Merlo (ARGENTINA6)','data':'4'},{'value':'Claypole (ARGENTINA6)','data':'3'},{'value':'El Porvenir (ARGENTINA6)','data':'18'},{'value':'Atlas (ARGENTINA6)','data':'11'},{'value':'D. Espanol (ARGENTINA6)','data':'17'},{'value':'Midland (ARGENTINA6)','data':'13'},{'value':'Lujan (ARGENTINA6)','data':'15'},{'value':'Leandro N. Alem (ARGENTINA6)','data':'6'},{'value':'S. Italiano (ARGENTINA6)','data':'16'},{'value':'Berazategui (ARGENTINA6)','data':'8'},{'value':'SM Burzaco (ARGENTINA6)','data':'14'},{'value':'Ituzaingo (ARGENTINA6)','data':'2'},{'value':'Central Cordoba (ARGENTINA6)','data':'12'},{'value':'V. Arenas (ARGENTINA6)','data':'9'},{'value':'Excursionistas (ARGENTINA6)','data':'10'},{'value':'Liniers (ARGENTINA8)','data':'11'},{'value':'Yupanqui (ARGENTINA8)','data':'10'},{'value':'Lugano (ARGENTINA8)','data':'8'},{'value':'D. Cambaceres (ARGENTINA8)','data':'12'},{'value':'S. Barracas (ARGENTINA8)','data':'6'},{'value':'D. Paraguayo (ARGENTINA8)','data':'2'},{'value':'Juventud Unida  (ARGENTINA8)','data':'1'},{'value':'Centro Espanol (ARGENTINA8)','data':'7'},{'value':'A. Rosario (ARGENTINA8)','data':'9'},{'value':'Deportivo Muniz (ARGENTINA8)','data':'3'},{'value':'C. Ballester (ARGENTINA8)','data':'5'},{'value':'Puerto Nuevo (ARGENTINA8)','data':'4'},{'value':'Crucero del N. (ARGENTINA9)','data':'1'},{'value':'Pronunciamiento (ARGENTINA9)','data':'15'},{'value':'Sarmiento R. (ARGENTINA9)','data':'14'},{'value':'D. Belgrano VR (ARGENTINA9)','data':'13'},{'value':'Circulo D. (ARGENTINA9)','data':'12'},{'value':'D. Madryn (ARGENTINA9)','data':'11'},{'value':'Cipolletti (ARGENTINA9)','data':'10'},{'value':'Olimpo Bahia B. (ARGENTINA9)','data':'9'},{'value':'S. Desamparados (ARGENTINA9)','data':'8'},{'value':'Camioneros (ARGENTINA9)','data':'7'},{'value':'S. Belgrano (ARGENTINA9)','data':'16'},{'value':'S. Estudiantes (ARGENTINA9)','data':'4'},{'value':'Sol de Mayo (ARGENTINA9)','data':'5'},{'value':'JU Gualeguaychu (ARGENTINA9)','data':'2'},{'value':'Ferro (ARGENTINA9)','data':'6'},{'value':'Boca Unidos (ARGENTINA9)','data':'26'},{'value':'Ciudad Bolivar (ARGENTINA9)','data':'3'},{'value':'Gimnasia y E. (ARGENTINA9)','data':'31'},{'value':'Sansinena (ARGENTINA9)','data':'30'},{'value':'Juventud U. U. (ARGENTINA9)','data':'29'},{'value':'S. Las Parejas (ARGENTINA9)','data':'28'},{'value':'CS Penarol (ARGENTINA9)','data':'17'},{'value':'Chaco For Ever (ARGENTINA9)','data':'27'},{'value':'Central Norte (ARGENTINA9)','data':'25'},{'value':'Gimnasia y Tiro (ARGENTINA9)','data':'24'},{'value':'Union Sunchales (ARGENTINA9)','data':'23'},{'value':'Douglas Haig (ARGENTINA9)','data':'22'},{'value':'Racing Cordoba (ARGENTINA9)','data':'21'},{'value':'Villa Mitre (ARGENTINA9)','data':'20'},{'value':'Huracán Las H. (ARGENTINA9)','data':'19'},{'value':'I. Chivilcoy (ARGENTINA9)','data':'18'},{'value':'Van (ARMENIA)','data':'8'},{'value':'BKMA (ARMENIA)','data':'1'},{'value':'Urartu (ARMENIA)','data':'5'},{'value':'Junior Sevan (ARMENIA)','data':'7'},{'value':'Pyunik (ARMENIA)','data':'2'},{'value':'Noravank (ARMENIA)','data':'6'},{'value':'Alashkert (ARMENIA)','data':'3'},{'value':'Lori (ARMENIA)','data':'10'},{'value':'Noah (ARMENIA)','data':'10'},{'value':'Ararat-Armenia (ARMENIA)','data':'4'},{'value':'Ararat Yerevan (ARMENIA)','data':'9'},{'value':'Shirak B (ARMENIA2)','data':'1'},{'value':'L. Artsakh (ARMENIA2)','data':'2'},{'value':'Ararat B (ARMENIA2)','data':'11'},{'value':'Urartu B (ARMENIA2)','data':'4'},{'value':'A.-Armenia B (ARMENIA2)','data':'3'},{'value':'Gandzasar (ARMENIA2)','data':'6'},{'value':'BKMA B (ARMENIA2)','data':'8'},{'value':'Pyunik B (ARMENIA2)','data':'1'},{'value':'Alashkert B (ARMENIA2)','data':'5'},{'value':'Shirak (ARMENIA2)','data':'7'},{'value':'West Armenia (ARMENIA2)','data':'6'},{'value':'Melbourne V. (AUSTRALIA)','data':'6'},{'value':'Macarthur FC (AUSTRALIA)','data':'11'},{'value':'Western Sydney  (AUSTRALIA)','data':'3'},{'value':'Sydney FC (AUSTRALIA)','data':'4'},{'value':'Melbourne City (AUSTRALIA)','data':'1'},{'value':'Wellington (AUSTRALIA)','data':'12'},{'value':'Brisbane Roar (AUSTRALIA)','data':'2'},{'value':'Adelaide Utd (AUSTRALIA)','data':'8'},{'value':'Western United (AUSTRALIA)','data':'5'},{'value':'Perth Glory (AUSTRALIA)','data':'7'},{'value':'Central Coast (AUSTRALIA)','data':'10'},{'value':'Newcastle Jets (AUSTRALIA)','data':'9'},{'value':'C. Croatia (AUSTRALIA10)','data':'8'},{'value':'Cooma Tigers (AUSTRALIA10)','data':'7'},{'value':'Belconnen Utd (AUSTRALIA10)','data':'6'},{'value':'Tuggeranong Utd (AUSTRALIA10)','data':'5'},{'value':'C. Olympic (AUSTRALIA10)','data':'4'},{'value':'Monaro Panthers (AUSTRALIA10)','data':'3'},{'value':'Gungahlin (AUSTRALIA10)','data':'2'},{'value':'West Camberra (AUSTRALIA10)','data':'1'},{'value':'Mt Druitt Town (AUSTRALIA11)','data':'2'},{'value':'Marconi S. (AUSTRALIA11)','data':'3'},{'value':'Sydney FC B (AUSTRALIA11)','data':'4'},{'value':'Sydney Olympic (AUSTRALIA11)','data':'5'},{'value':'Sydney United (AUSTRALIA11)','data':'6'},{'value':'Northbridge B. (AUSTRALIA11)','data':'7'},{'value':'Blacktown City (AUSTRALIA11)','data':'9'},{'value':'Manly Utd (AUSTRALIA11)','data':'1'},{'value':'Wollongong W. (AUSTRALIA11)','data':'12'},{'value':'Sutherland S. (AUSTRALIA11)','data':'8'},{'value':'Rockdale City (AUSTRALIA11)','data':'11'},{'value':'APIA L. Tigers (AUSTRALIA11)','data':'10'},{'value':'Werribee City (AUSTRALIA13)','data':'12'},{'value':'Bulleen Lions (AUSTRALIA13)','data':'10'},{'value':'Goulburn Valley (AUSTRALIA13)','data':'9'},{'value':'Northcote City (AUSTRALIA13)','data':'8'},{'value':'North Geelong (AUSTRALIA13)','data':'7'},{'value':'Manningham Utd (AUSTRALIA13)','data':'6'},{'value':'Langwarrin (AUSTRALIA13)','data':'5'},{'value':'Pascoe Vale (AUSTRALIA13)','data':'1'},{'value':'Moreland City (AUSTRALIA13)','data':'2'},{'value':'Brunswick City (AUSTRALIA13)','data':'3'},{'value':'Moreland Zebras (AUSTRALIA13)','data':'4'},{'value':'Kingston City (AUSTRALIA13)','data':'11'},{'value':'Fulham Utd (AUSTRALIA15)','data':'7'},{'value':'Playford City (AUSTRALIA15)','data':'9'},{'value':'A. Hills Hawks (AUSTRALIA15)','data':'11'},{'value':'W. Strikers (AUSTRALIA15)','data':'12'},{'value':'West Torrens (AUSTRALIA15)','data':'2'},{'value':'White City W. (AUSTRALIA15)','data':'8'},{'value':'Adelaide Cobras (AUSTRALIA15)','data':'1'},{'value':'West Torrens B. (AUSTRALIA15)','data':'2'},{'value':'A. Victory (AUSTRALIA15)','data':'3'},{'value':'Eastern Utd (AUSTRALIA15)','data':'4'},{'value':'West Adelaide (AUSTRALIA15)','data':'5'},{'value':'Para Hills K. (AUSTRALIA15)','data':'6'},{'value':'Modbury Jets (AUSTRALIA15)','data':'10'},{'value':'Melbourne C. W (AUSTRALIA2)','data':'4'},{'value':'Brisbane Roar W (AUSTRALIA2)','data':'8'},{'value':'Perth Glory W (AUSTRALIA2)','data':'7'},{'value':'Canberra Utd W (AUSTRALIA2)','data':'3'},{'value':'Sydney W (AUSTRALIA2)','data':'5'},{'value':'Western S. W (AUSTRALIA2)','data':'2'},{'value':'Adelaide Utd W (AUSTRALIA2)','data':'10'},{'value':'Wellington Phoe (AUSTRALIA2)','data':'1'},{'value':'Newcastle J. W (AUSTRALIA2)','data':'6'},{'value':'Melbourne V. W (AUSTRALIA2)','data':'9'},{'value':'Dandenong City (AUSTRALIA3)','data':'4'},{'value':'South Melbourne (AUSTRALIA3)','data':'14'},{'value':'Heidelberg Utd (AUSTRALIA3)','data':'13'},{'value':'Green Gully (AUSTRALIA3)','data':'12'},{'value':'St. Albans (AUSTRALIA3)','data':'11'},{'value':'Altona Magic (AUSTRALIA3)','data':'10'},{'value':'Hume City (AUSTRALIA3)','data':'9'},{'value':'Oakleigh C. (AUSTRALIA3)','data':'8'},{'value':'Port Melbourne (AUSTRALIA3)','data':'1'},{'value':'Melbourne K. (AUSTRALIA3)','data':'2'},{'value':'Eastern Lions (AUSTRALIA3)','data':'5'},{'value':'Dandenong T. (AUSTRALIA3)','data':'3'},{'value':'Bentleigh G. (AUSTRALIA3)','data':'6'},{'value':'Avondale (AUSTRALIA3)','data':'7'},{'value':'B. Strikers (AUSTRALIA4)','data':'5'},{'value':'Q. Lions (AUSTRALIA4)','data':'3'},{'value':'Logan Lightning (AUSTRALIA4)','data':'2'},{'value':'Peninsula (AUSTRALIA4)','data':'1'},{'value':'Moreton Bay Utd (AUSTRALIA4)','data':'7'},{'value':'Redlands (AUSTRALIA4)','data':'8'},{'value':'SC Wanderers (AUSTRALIA4)','data':'9'},{'value':'Capalaba (AUSTRALIA4)','data':'10'},{'value':'Olympic (AUSTRALIA4)','data':'11'},{'value':'Eastern Suburbs (AUSTRALIA4)','data':'13'},{'value':'Gold Coast (AUSTRALIA4)','data':'12'},{'value':'Brisbane Roar B (AUSTRALIA4)','data':'14'},{'value':'Magpies C. (AUSTRALIA4)','data':'6'},{'value':'Gold C. Knights (AUSTRALIA4)','data':'4'},{'value':'Perth Glory B (AUSTRALIA5)','data':'8'},{'value':'Gwelup Croatia  (AUSTRALIA5)','data':'11'},{'value':'Cockburn City (AUSTRALIA5)','data':'1'},{'value':'Sorrento (AUSTRALIA5)','data':'2'},{'value':'Armadale (AUSTRALIA5)','data':'3'},{'value':'Inglewood Utd (AUSTRALIA5)','data':'4'},{'value':'Bayswater (AUSTRALIA5)','data':'5'},{'value':'Rockingham City (AUSTRALIA5)','data':'6'},{'value':'Perth SC (AUSTRALIA5)','data':'7'},{'value':'Balcatta (AUSTRALIA5)','data':'10'},{'value':'Floreat Athena (AUSTRALIA5)','data':'9'},{'value':'ECU Joondalup (AUSTRALIA5)','data':'12'},{'value':'Adelaide City (AUSTRALIA6)','data':'2'},{'value':'Blue Eagles (AUSTRALIA6)','data':'11'},{'value':'A. Raiders (AUSTRALIA6)','data':'12'},{'value':'Croydon Kings (AUSTRALIA6)','data':'3'},{'value':'Sturt Lions (AUSTRALIA6)','data':'4'},{'value':'NE MetroStars (AUSTRALIA6)','data':'10'},{'value':'Adelaide Comets (AUSTRALIA6)','data':'9'},{'value':'Campbelltown (AUSTRALIA6)','data':'1'},{'value':'Adelaide Utd (AUSTRALIA6)','data':'8'},{'value':'South Adelaide  (AUSTRALIA6)','data':'7'},{'value':'Cumberland Utd (AUSTRALIA6)','data':'5'},{'value':'A. Olympic (AUSTRALIA6)','data':'6'},{'value':'Lake Macquarie (AUSTRALIA7)','data':'3'},{'value':'Adamstown R. (AUSTRALIA7)','data':'6'},{'value':'Charlestown A. (AUSTRALIA7)','data':'7'},{'value':'Maitland (AUSTRALIA7)','data':'2'},{'value':'Broadmeadow (AUSTRALIA7)','data':'4'},{'value':'Newcastle O. (AUSTRALIA7)','data':'5'},{'value':'Weston Workers (AUSTRALIA7)','data':'9'},{'value':'Lambton Jaffas (AUSTRALIA7)','data':'10'},{'value':'Edgeworth E. (AUSTRALIA7)','data':'1'},{'value':'Valentine (AUSTRALIA7)','data':'8'},{'value':'St George W. (AUSTRALIA9)','data':'1'},{'value':'Acacia Ridge (AUSTRALIA9)','data':'12'},{'value':'The Lakes (AUSTRALIA9)','data':'11'},{'value':'Bayside Utd (AUSTRALIA9)','data':'10'},{'value':'Mt Gravatt (AUSTRALIA9)','data':'9'},{'value':'Brisbane K. (AUSTRALIA9)','data':'8'},{'value':'Albany Creek (AUSTRALIA9)','data':'7'},{'value':'U. Queensland (AUSTRALIA9)','data':'6'},{'value':'Western Spirit (AUSTRALIA9)','data':'5'},{'value':'Toowong (AUSTRALIA9)','data':'4'},{'value':'The Gap (AUSTRALIA9)','data':'3'},{'value':'Centenary S. (AUSTRALIA9)','data':'2'},{'value':'Sturm Graz (AUSTRIA)','data':'1'},{'value':'A. Klagenfurt (AUSTRIA)','data':'11'},{'value':'Salzburg (AUSTRIA)','data':'2'},{'value':'Wolfsberger AC (AUSTRIA)','data':'12'},{'value':'WSG Tirol (AUSTRIA)','data':'7'},{'value':'Ried (AUSTRIA)','data':'9'},{'value':'Hartberg (AUSTRIA)','data':'4'},{'value':'R. Altach (AUSTRIA)','data':'5'},{'value':'Austria Wien (AUSTRIA)','data':'10'},{'value':'LASK Linz (AUSTRIA)','data':'6'},{'value':'Admira Wacker (AUSTRIA)','data':'8'},{'value':'Rapid Wien (AUSTRIA)','data':'3'},{'value':'Floridsdorfer (AUSTRIA2)','data':'4'},{'value':'Kapfenberger (AUSTRIA2)','data':'9'},{'value':'BW Linz (AUSTRIA2)','data':'13'},{'value':'A. Lustenau (AUSTRIA2)','data':'15'},{'value':'FC Juniors (AUSTRIA2)','data':'5'},{'value':'SV Horn (AUSTRIA2)','data':'7'},{'value':'Lafnitz (AUSTRIA2)','data':'6'},{'value':'St. Polten (AUSTRIA2)','data':'11'},{'value':'Rapid Wien B (AUSTRIA2)','data':'12'},{'value':'Liefering (AUSTRIA2)','data':'10'},{'value':'Grazer AK (AUSTRIA2)','data':'16'},{'value':'Vorwarts Steyr (AUSTRIA2)','data':'8'},{'value':'Amstetten (AUSTRIA2)','data':'3'},{'value':'W. Innsbruck (AUSTRIA2)','data':'2'},{'value':'Austria Wien B (AUSTRIA2)','data':'1'},{'value':'Dornbirn (AUSTRIA2)','data':'14'},{'value':'Swar. Tirol B (AUSTRIA3)','data':'4'},{'value':'SV Innsbruck (AUSTRIA3)','data':'6'},{'value':'W. Innsbruck B (AUSTRIA3)','data':'9'},{'value':'Telfs (AUSTRIA3)','data':'11'},{'value':'Worgl (AUSTRIA3)','data':'8'},{'value':'Imst (AUSTRIA3)','data':'10'},{'value':'Hall (AUSTRIA3)','data':'2'},{'value':'Kufstein (AUSTRIA3)','data':'7'},{'value':'Reichenau (AUSTRIA3)','data':'3'},{'value':'Schwaz (AUSTRIA3)','data':'1'},{'value':'Fügen (AUSTRIA3)','data':'5'},{'value':'Kitzbuhel (AUSTRIA3)','data':'12'},{'value':'Wolfurt (AUSTRIA4)','data':'6'},{'value':'Lauterach (AUSTRIA4)','data':'11'},{'value':'Rotenberg (AUSTRIA4)','data':'1'},{'value':'Rothis (AUSTRIA4)','data':'3'},{'value':'Bregenz (AUSTRIA4)','data':'10'},{'value':'Dornbirner SV (AUSTRIA4)','data':'7'},{'value':'Hohenems (AUSTRIA4)','data':'9'},{'value':'RW Rankweil (AUSTRIA4)','data':'2'},{'value':'FC Egg (AUSTRIA4)','data':'8'},{'value':'Admira Dornbirn (AUSTRIA4)','data':'5'},{'value':'A. Lustenau B (AUSTRIA4)','data':'4'},{'value':'Seekirchen (AUSTRIA5)','data':'1'},{'value':'St. Johann (AUSTRIA5)','data':'5'},{'value':'Bischofshofen (AUSTRIA5)','data':'4'},{'value':'A. Salzburg (AUSTRIA5)','data':'7'},{'value':'Anif (AUSTRIA5)','data':'2'},{'value':'Salzburger AK (AUSTRIA5)','data':'8'},{'value':'Wals-Grunau (AUSTRIA5)','data':'10'},{'value':'P. Saalfelden (AUSTRIA5)','data':'6'},{'value':'Grodig (AUSTRIA5)','data':'9'},{'value':'Kuchl (AUSTRIA5)','data':'3'},{'value':'Deutschlandsber (AUSTRIA6)','data':'9'},{'value':'Wolfsberger B (AUSTRIA6)','data':'10'},{'value':'Spittal (AUSTRIA6)','data':'1'},{'value':'Vocklamarkt (AUSTRIA6)','data':'13'},{'value':'Gleisdorf (AUSTRIA6)','data':'6'},{'value':'St. Anna (AUSTRIA6)','data':'16'},{'value':'FC Wels (AUSTRIA6)','data':'14'},{'value':'Allerheiligen (AUSTRIA6)','data':'15'},{'value':'Ried B (AUSTRIA6)','data':'4'},{'value':'Sturm Graz B (AUSTRIA6)','data':'2'},{'value':'Bad Gleichenber (AUSTRIA6)','data':'7'},{'value':'Gurten (AUSTRIA6)','data':'12'},{'value':'WSC Hertha Wels (AUSTRIA6)','data':'11'},{'value':'Stadl Paura (AUSTRIA6)','data':'17'},{'value':'Ried B (AUSTRIA6)','data':'4'},{'value':'Kalsdorf (AUSTRIA6)','data':'8'},{'value':'Weiz (AUSTRIA6)','data':'5'},{'value':'Treibach (AUSTRIA6)','data':'3'},{'value':'Mannsdorf (AUSTRIA7)','data':'6'},{'value':'Bruck Leitha (AUSTRIA7)','data':'3'},{'value':'Wiener Neustadt (AUSTRIA7)','data':'14'},{'value':'Leobendorf (AUSTRIA7)','data':'4'},{'value':'Neusiedl (AUSTRIA7)','data':'10'},{'value':'Mauerwerk (AUSTRIA7)','data':'8'},{'value':'Drassburg (AUSTRIA7)','data':'9'},{'value':'Wiener Viktoria (AUSTRIA7)','data':'13'},{'value':'Admira B (AUSTRIA7)','data':'12'},{'value':'First Vienna (AUSTRIA7)','data':'2'},{'value':'Stripfing (AUSTRIA7)','data':'1'},{'value':'Traiskirchen (AUSTRIA7)','data':'7'},{'value':'Wiener SC (AUSTRIA7)','data':'5'},{'value':'Wiener Linien (AUSTRIA7)','data':'12'},{'value':'TWL Elektra (AUSTRIA7)','data':'11'},{'value':'Qarabag (AZERBAIJAN)','data':'6'},{'value':'Sabah (AZERBAIJAN)','data':'1'},{'value':'Sumqayit (AZERBAIJAN)','data':'4'},{'value':'Qabala (AZERBAIJAN)','data':'8'},{'value':'Zira (AZERBAIJAN)','data':'5'},{'value':'Keshla (AZERBAIJAN)','data':'3'},{'value':'Neftci (AZERBAIJAN)','data':'7'},{'value':'Sebail (AZERBAIJAN)','data':'2'},{'value':'Budaiya (BAHRAIN)','data':'8'},{'value':'Al-Hidd (BAHRAIN)','data':'9'},{'value':'Khalidiya (BAHRAIN)','data':'7'},{'value':'Manama (BAHRAIN)','data':'5'},{'value':'East Riffa (BAHRAIN)','data':'6'},{'value':'Al Hala (BAHRAIN)','data':'10'},{'value':'Malkiya (BAHRAIN)','data':'7'},{'value':'Al Ahli M. (BAHRAIN)','data':'3'},{'value':'Al Riffa (BAHRAIN)','data':'2'},{'value':'Muharraq (BAHRAIN)','data':'1'},{'value':'Al-Najma (BAHRAIN)','data':'4'},{'value':'Busaiteen (BAHRAIN)','data':'3'},{'value':'A. Chittagong (BANGLADESH)','data':'12'},{'value':'Muktijoddha (BANGLADESH)','data':'13'},{'value':'Brothers Union (BANGLADESH)','data':'6'},{'value':'Sheikh Jamal (BANGLADESH)','data':'11'},{'value':'Baridhara (BANGLADESH)','data':'2'},{'value':'Bashundhara K. (BANGLADESH)','data':'1'},{'value':'Abahani (BANGLADESH)','data':'3'},{'value':'B. Police (BANGLADESH)','data':'4'},{'value':'Sheikh Russel (BANGLADESH)','data':'5'},{'value':'Saif (BANGLADESH)','data':'7'},{'value':'Rahmatgonj MFS (BANGLADESH)','data':'8'},{'value':'Mohammedan (BANGLADESH)','data':'10'},{'value':'Arambagh (BANGLADESH)','data':'9'},{'value':'Vitebsk (BELARUS)','data':'14'},{'value':'Smorgon (BELARUS)','data':'3'},{'value':'T. Zhodino (BELARUS)','data':'16'},{'value':'S. Soligorsk (BELARUS)','data':'5'},{'value':'FC Minsk (BELARUS)','data':'6'},{'value':'Rukh Brest (BELARUS)','data':'7'},{'value':'Sputnik (BELARUS)','data':'9'},{'value':'Gomel (BELARUS)','data':'8'},{'value':'Neman Grodno (BELARUS)','data':'13'},{'value':'Isloch (BELARUS)','data':'1'},{'value':'Slutsk (BELARUS)','data':'12'},{'value':'Slavia Mozyr (BELARUS)','data':'2'},{'value':'BATE Borisov (BELARUS)','data':'11'},{'value':'Dinamo Brest (BELARUS)','data':'10'},{'value':'Dinamo Minsk (BELARUS)','data':'15'},{'value':'Energetik-BGU (BELARUS)','data':'4'},{'value':'S.Petrikov (BELARUS2)','data':'10'},{'value':'Belshina (BELARUS2)','data':'1'},{'value':'Krumkachy (BELARUS2)','data':'11'},{'value':'Arsenal D. (BELARUS2)','data':'9'},{'value':'Orsha (BELARUS2)','data':'8'},{'value':'Slonim (BELARUS2)','data':'7'},{'value':'Lida (BELARUS2)','data':'6'},{'value':'Dnepr Mogilev (BELARUS2)','data':'5'},{'value':'Baranovichi (BELARUS2)','data':'4'},{'value':'Naftan (BELARUS2)','data':'3'},{'value':'Volna Pinsk (BELARUS2)','data':'2'},{'value':'Lokomotiv Gomel (BELARUS2)','data':'12'},{'value':'Neman W (BELARUS4)','data':'1'},{'value':'Gomel W (BELARUS4)','data':'10'},{'value':'Dnepr Mogilev W (BELARUS4)','data':'9'},{'value':'Dinamo Brest W (BELARUS4)','data':'8'},{'value':'ABFF U19 W (BELARUS4)','data':'7'},{'value':'Minsk FK W (BELARUS4)','data':'6'},{'value':'Zorka-BDU W (BELARUS4)','data':'5'},{'value':'Bobruichanka W (BELARUS4)','data':'4'},{'value':'Vitebsk W (BELARUS4)','data':'2'},{'value':'Dinamo-BGU W (BELARUS4)','data':'3'},{'value':'Gent (BELGIUM)','data':'18'},{'value':'Kortrijk (BELGIUM)','data':'5'},{'value':'Anderlecht (BELGIUM)','data':'15'},{'value':'KV Mechelen (BELGIUM)','data':'11'},{'value':'KRC Genk (BELGIUM)','data':'2'},{'value':'Cercle Brugge (BELGIUM)','data':'8'},{'value':'Charleroi (BELGIUM)','data':'10'},{'value':'Seraing (BELGIUM)','data':'6'},{'value':'Zulte-Waregem (BELGIUM)','data':'4'},{'value':'Club Brugge (BELGIUM)','data':'13'},{'value':'Eupen (BELGIUM)','data':'14'},{'value':'Standard Liege (BELGIUM)','data':'1'},{'value':'Sint-Truiden (BELGIUM)','data':'17'},{'value':'Beerschot-Wil. (BELGIUM)','data':'7'},{'value':'Oostende (BELGIUM)','data':'9'},{'value':'St. Gilloise (BELGIUM)','data':'16'},{'value':'Antwerp (BELGIUM)','data':'12'},{'value':'OH Leuven (BELGIUM)','data':'3'},{'value':'RWDM (BELGIUM2)','data':'2'},{'value':'Mouscron (BELGIUM2)','data':'3'},{'value':'Beveren (BELGIUM2)','data':'7'},{'value':'Lommel SK (BELGIUM2)','data':'4'},{'value':'Club Brugge B (BELGIUM2)','data':'4'},{'value':'Westerlo (BELGIUM2)','data':'1'},{'value':'Lierse K. (BELGIUM2)','data':'5'},{'value':'Deinze (BELGIUM2)','data':'8'},{'value':'E. Virton (BELGIUM2)','data':'6'},{'value':'O. Charleroi (BELGIUM3)','data':'3'},{'value':'RFC Liege (BELGIUM3)','data':'11'},{'value':'Rupel Boom (BELGIUM3)','data':'2'},{'value':'Tienen (BELGIUM3)','data':'12'},{'value':'Francs Borains (BELGIUM3)','data':'7'},{'value':'URSL Vise (BELGIUM3)','data':'13'},{'value':'Heist (BELGIUM3)','data':'5'},{'value':'Dender (BELGIUM3)','data':'6'},{'value':'Dessel Sport (BELGIUM3)','data':'14'},{'value':'Knokke (BELGIUM3)','data':'15'},{'value':'La Louviere (BELGIUM3)','data':'8'},{'value':'Patro Eisden (BELGIUM3)','data':'4'},{'value':'Sint-Eloois (BELGIUM3)','data':'9'},{'value':'Thes Sport (BELGIUM3)','data':'1'},{'value':'Mandel Utd (BELGIUM3)','data':'10'},{'value':'KSV Roeselare (BELGIUM3)','data':'9'},{'value':'E. Aalst W (BELGIUM4)','data':'7'},{'value':'Gent W (BELGIUM4)','data':'3'},{'value':'OH Leuven W (BELGIUM4)','data':'4'},{'value':'Club Brugge W (BELGIUM4)','data':'5'},{'value':'St. Liege W (BELGIUM4)','data':'6'},{'value':'Zulte-Waregem W (BELGIUM4)','data':'8'},{'value':'WS Woluwe W (BELGIUM4)','data':'2'},{'value':'Charleroi W (BELGIUM4)','data':'1'},{'value':'Genk W (BELGIUM4)','data':'10'},{'value':'Anderlecht W (BELGIUM4)','data':'9'},{'value':'Anderlecht B W (BELGIUM5)','data':'13'},{'value':'Moldavo W (BELGIUM5)','data':'1'},{'value':'Mechelen W (BELGIUM5)','data':'2'},{'value':'Kontich W (BELGIUM5)','data':'3'},{'value':'Wuustwezel W (BELGIUM5)','data':'4'},{'value':'Genk B W (BELGIUM5)','data':'5'},{'value':'Tienen W (BELGIUM5)','data':'6'},{'value':'Chastre W (BELGIUM5)','data':'7'},{'value':'Famkes Merkem W (BELGIUM5)','data':'9'},{'value':'OH Leuven B W (BELGIUM5)','data':'12'},{'value':'Gent B W (BELGIUM5)','data':'8'},{'value':'R. Mons W (BELGIUM5)','data':'14'},{'value':'V. Zwevezele W (BELGIUM5)','data':'15'},{'value':'RFC Liege W (BELGIUM5)','data':'11'},{'value':'S. Liege B W (BELGIUM5)','data':'10'},{'value':'Aurora (BOLIVIA)','data':'3'},{'value':'Nacional Potosí (BOLIVIA)','data':'1'},{'value':'The Strongest (BOLIVIA)','data':'2'},{'value':'Blooming (BOLIVIA)','data':'14'},{'value':'Guabira (BOLIVIA)','data':'7'},{'value':'San Jose (BOLIVIA)','data':'12'},{'value':'A. Palmaflor (BOLIVIA)','data':'10'},{'value':'Santa Cruz (BOLIVIA)','data':'11'},{'value':'Oriente P. (BOLIVIA)','data':'13'},{'value':'Wilstermann (BOLIVIA)','data':'9'},{'value':'Royal Pari (BOLIVIA)','data':'4'},{'value':'Real Tomayapo (BOLIVIA)','data':'5'},{'value':'Always Ready (BOLIVIA)','data':'6'},{'value':'Bolivar (BOLIVIA)','data':'8'},{'value':'Real Potosí (BOLIVIA)','data':'16'},{'value':'I. Petrolero (BOLIVIA)','data':'15'},{'value':'Olimpik (BOSNIA)','data':'6'},{'value':'Sloboda Tuzla (BOSNIA)','data':'5'},{'value':'Leotar (BOSNIA)','data':'2'},{'value':'FK Sarajevo (BOSNIA)','data':'9'},{'value':'Siroki Brijeg (BOSNIA)','data':'7'},{'value':'Tusla City (BOSNIA)','data':'10'},{'value':'FK Krupa (BOSNIA)','data':'9'},{'value':'Zeljeznicar (BOSNIA)','data':'3'},{'value':'Zrinjski Mostar (BOSNIA)','data':'8'},{'value':'Rudar Prijedor (BOSNIA)','data':'6'},{'value':'Posusje (BOSNIA)','data':'12'},{'value':'Borac Banja L. (BOSNIA)','data':'4'},{'value':'Rad. Bijeljina (BOSNIA)','data':'1'},{'value':'Velez Mostar (BOSNIA)','data':'11'},{'value':'Orasje (BOSNIA2)','data':'9'},{'value':'TOSK Tesanj (BOSNIA2)','data':'16'},{'value':'Slaven Zivinice (BOSNIA2)','data':'1'},{'value':'Z. Gradacac (BOSNIA2)','data':'2'},{'value':'GOSK Gabela (BOSNIA2)','data':'6'},{'value':'Jedinstvo Bihac (BOSNIA2)','data':'11'},{'value':'Capljina (BOSNIA2)','data':'10'},{'value':'Rudar Kakanj (BOSNIA2)','data':'5'},{'value':'Vis Simm-Bau (BOSNIA2)','data':'3'},{'value':'B. Banovici (BOSNIA2)','data':'1'},{'value':'Gorazde (BOSNIA2)','data':'10'},{'value':'Travnik (BOSNIA2)','data':'8'},{'value':'Mladost D. (BOSNIA2)','data':'12'},{'value':'Igman Konjic (BOSNIA2)','data':'7'},{'value':'Tomislav (BOSNIA2)','data':'13'},{'value':'G. Srebrenik (BOSNIA2)','data':'14'},{'value':'B. Gracanica (BOSNIA2)','data':'4'},{'value':'Radnik Hadzici (BOSNIA2)','data':'15'},{'value':'Athletico PR (BRAZIL)','data':'15'},{'value':'Cuiaba (BRAZIL)','data':'5'},{'value':'Gremio (BRAZIL)','data':'14'},{'value':'Atletico GO (BRAZIL)','data':'18'},{'value':'Bahia (BRAZIL)','data':'3'},{'value':'Corinthians (BRAZIL)','data':'17'},{'value':'Juventude (BRAZIL)','data':'6'},{'value':'Ceara (BRAZIL)','data':'13'},{'value':'Flamengo (BRAZIL)','data':'11'},{'value':'Atletico MG (BRAZIL)','data':'9'},{'value':'Fortaleza (BRAZIL)','data':'10'},{'value':'Santos (BRAZIL)','data':'4'},{'value':'Internacional (BRAZIL)','data':'19'},{'value':'Sport Recife (BRAZIL)','data':'20'},{'value':'Chapecoense (BRAZIL)','data':'1'},{'value':'Fluminense (BRAZIL)','data':'8'},{'value':'Bragantino (BRAZIL)','data':'2'},{'value':'America MG (BRAZIL)','data':'16'},{'value':'Sao Paulo (BRAZIL)','data':'7'},{'value':'Palmeiras (BRAZIL)','data':'12'},{'value':'Operario PR (BRAZIL2)','data':'10'},{'value':'Avai (BRAZIL2)','data':'8'},{'value':'Botafogo (BRAZIL2)','data':'6'},{'value':'Coritiba (BRAZIL2)','data':'7'},{'value':'Confianca (BRAZIL2)','data':'13'},{'value':'Remo (BRAZIL2)','data':'12'},{'value':'CSA (BRAZIL2)','data':'16'},{'value':'Vila Nova (BRAZIL2)','data':'5'},{'value':'Cruzeiro (BRAZIL2)','data':'14'},{'value':'Nautico (BRAZIL2)','data':'15'},{'value':'CRB (BRAZIL2)','data':'11'},{'value':'Ponte Preta (BRAZIL2)','data':'18'},{'value':'Guarani (BRAZIL2)','data':'3'},{'value':'Brasil de P. (BRAZIL2)','data':'1'},{'value':'Vasco da Gama (BRAZIL2)','data':'9'},{'value':'Goias (BRAZIL2)','data':'20'},{'value':'Sampaio Correa (BRAZIL2)','data':'19'},{'value':'Londrina (BRAZIL2)','data':'2'},{'value':'Brusque (BRAZIL2)','data':'17'},{'value':'Vitoria (BRAZIL2)','data':'4'},{'value':'Jacuipense (BRAZIL3)','data':'2'},{'value':'Mirassol (BRAZIL3)','data':'20'},{'value':'Santa Cruz (BRAZIL3)','data':'14'},{'value':'Oeste (BRAZIL3)','data':'19'},{'value':'Manaus (BRAZIL3)','data':'13'},{'value':'EC Sao Jose (BRAZIL3)','data':'16'},{'value':'Botafogo PB (BRAZIL3)','data':'5'},{'value':'Figueirense (BRAZIL3)','data':'4'},{'value':'Ituano (BRAZIL3)','data':'12'},{'value':'Botafogo SP (BRAZIL3)','data':'15'},{'value':'Floresta (BRAZIL3)','data':'1'},{'value':'Criciuma (BRAZIL3)','data':'11'},{'value':'Ypiranga (BRAZIL3)','data':'17'},{'value':'Paysandu (BRAZIL3)','data':'8'},{'value':'Altos (BRAZIL3)','data':'9'},{'value':'Ferroviario (BRAZIL3)','data':'6'},{'value':'Volta Redonda (BRAZIL3)','data':'10'},{'value':'Novorizontino (BRAZIL3)','data':'3'},{'value':'Parana (BRAZIL3)','data':'18'},{'value':'Tombense (BRAZIL3)','data':'7'},{'value':'Santana (BRAZIL4)','data':'62'},{'value':'Peñarol (BRAZIL4)','data':'59'},{'value':'Moto Club (BRAZIL4)','data':'60'},{'value':'Real Ariquemes (BRAZIL4)','data':'66'},{'value':'Picos (BRAZIL4)','data':'65'},{'value':'GAS (BRAZIL4)','data':'63'},{'value':'G. Juventus (BRAZIL4)','data':'47'},{'value':'Aquidauanense (BRAZIL4)','data':'68'},{'value':'Caldense (BRAZIL4)','data':'58'},{'value':'Brasiliense (BRAZIL4)','data':'67'},{'value':'Tocantinópolis (BRAZIL4)','data':'64'},{'value':'Jaraguá EC (BRAZIL4)','data':'11'},{'value':'Sao Raimundo (BRAZIL4)','data':'26'},{'value':'A. Acreano (BRAZIL4)','data':'25'},{'value':'Galvez (BRAZIL4)','data':'24'},{'value':'Castanhal (BRAZIL4)','data':'23'},{'value':'Ypiranga AP (BRAZIL4)','data':'22'},{'value':'Fast Clube (BRAZIL4)','data':'21'},{'value':'Rio Branco VN (BRAZIL4)','data':'20'},{'value':'Patrocinense (BRAZIL4)','data':'19'},{'value':'Uberlândia (BRAZIL4)','data':'18'},{'value':'Aguia Negra (BRAZIL4)','data':'16'},{'value':'Boa (BRAZIL4)','data':'15'},{'value':'ABC (BRAZIL4)','data':'50'},{'value':'Gama (BRAZIL4)','data':'12'},{'value':'Portuguesa (BRAZIL4)','data':'29'},{'value':'Porto Velho (BRAZIL4)','data':'10'},{'value':'U. Rondonopolis (BRAZIL4)','data':'9'},{'value':'A. Alagoinas (BRAZIL4)','data':'8'},{'value':'ASA (BRAZIL4)','data':'7'},{'value':'Murici (BRAZIL4)','data':'6'},{'value':'Retro (BRAZIL4)','data':'5'},{'value':'Juazeirense (BRAZIL4)','data':'4'},{'value':'Itabaiana (BRAZIL4)','data':'3'},{'value':'Sergipe (BRAZIL4)','data':'2'},{'value':'Bahia de Feira (BRAZIL4)','data':'1'},{'value':'Sao Bento (BRAZIL4)','data':'32'},{'value':'Rio Branco ES (BRAZIL4)','data':'69'},{'value':'Aparecidense (BRAZIL4)','data':'13'},{'value':'Rio Branco PR (BRAZIL4)','data':'43'},{'value':'Campinense (BRAZIL4)','data':'56'},{'value':'Caucaia (BRAZIL4)','data':'55'},{'value':'Atletico CE (BRAZIL4)','data':'54'},{'value':'Sousa (BRAZIL4)','data':'53'},{'value':'Salgueiro (BRAZIL4)','data':'52'},{'value':'América RN (BRAZIL4)','data':'51'},{'value':'Central (BRAZIL4)','data':'61'},{'value':'Imperatriz (BRAZIL4)','data':'35'},{'value':'Treze (BRAZIL4)','data':'49'},{'value':'Ferroviária (BRAZIL4)','data':'17'},{'value':'Caxias (BRAZIL4)','data':'48'},{'value':'Joinville (BRAZIL4)','data':'46'},{'value':'Bangu (BRAZIL4)','data':'27'},{'value':'Esportivo (BRAZIL4)','data':'44'},{'value':'Santo André (BRAZIL4)','data':'28'},{'value':'Marcílio Dias (BRAZIL4)','data':'42'},{'value':'Aimoré (BRAZIL4)','data':'41'},{'value':'4 de Julho (BRAZIL4)','data':'40'},{'value':'Juventude (BRAZIL4)','data':'39'},{'value':'Paragominas (BRAZIL4)','data':'38'},{'value':'Guarany (BRAZIL4)','data':'37'},{'value':'Palmas (BRAZIL4)','data':'36'},{'value':'Madureira (BRAZIL4)','data':'34'},{'value':'Inter Limeira (BRAZIL4)','data':'33'},{'value':'Boavista (BRAZIL4)','data':'31'},{'value':'Cianorte (BRAZIL4)','data':'30'},{'value':'Goianésia (BRAZIL4)','data':'57'},{'value':'Cascavel (BRAZIL4)','data':'45'},{'value':'Nova Mutum (BRAZIL4)','data':'14'},{'value':'Internacional W (BRAZIL5)','data':'3'},{'value':'Kindermann-A. W (BRAZIL5)','data':'16'},{'value':'Botafogo W (BRAZIL5)','data':'7'},{'value':'Napoli CA W (BRAZIL5)','data':'6'},{'value':'Bahia W (BRAZIL5)','data':'8'},{'value':'Flamengo W (BRAZIL5)','data':'9'},{'value':'Sao Paulo W (BRAZIL5)','data':'1'},{'value':'Cruzeiro W (BRAZIL5)','data':'11'},{'value':'Minas ICESP W (BRAZIL5)','data':'10'},{'value':'Santos W (BRAZIL5)','data':'4'},{'value':'Corinthians W (BRAZIL5)','data':'5'},{'value':'Sao Jose W (BRAZIL5)','data':'15'},{'value':'Ferroviaria W (BRAZIL5)','data':'14'},{'value':'Palmeiras W (BRAZIL5)','data':'13'},{'value':'Real Brasília W (BRAZIL5)','data':'12'},{'value':'Gremio W (BRAZIL5)','data':'2'},{'value':'Corinthians U20 (BRAZIL6)','data':'3'},{'value':'Ceara U20 (BRAZIL6)','data':'16'},{'value':'Internacio. U20 (BRAZIL6)','data':'19'},{'value':'America MG U20 (BRAZIL6)','data':'15'},{'value':'Santos U20 (BRAZIL6)','data':'14'},{'value':'Vitoria U20 (BRAZIL6)','data':'13'},{'value':'Chapecoen. U20  (BRAZIL6)','data':'12'},{'value':'Sp. Recife U20 (BRAZIL6)','data':'11'},{'value':'Palmeiras U20 (BRAZIL6)','data':'10'},{'value':'Botafogo U20 (BRAZIL6)','data':'1'},{'value':'Atletico PR U20 (BRAZIL6)','data':'18'},{'value':'Atletico MG U20 (BRAZIL6)','data':'2'},{'value':'Flamengo RJ U20 (BRAZIL6)','data':'20'},{'value':'Goias U20 (BRAZIL6)','data':'9'},{'value':'Bahia U20 (BRAZIL6)','data':'8'},{'value':'Fluminense U20 (BRAZIL6)','data':'7'},{'value':'Vasco U20 (BRAZIL6)','data':'6'},{'value':'Cruzeiro U20 (BRAZIL6)','data':'5'},{'value':'Gremio U20 (BRAZIL6)','data':'4'},{'value':'Sao Paulo U20 (BRAZIL6)','data':'17'},{'value':'Lok. Plovdiv (BULGARIA)','data':'11'},{'value':'Lokomotiv Sofia (BULGARIA)','data':'4'},{'value':'Beroe (BULGARIA)','data':'3'},{'value':'Pirin Blag. (BULGARIA)','data':'6'},{'value':'Tsarsko Selo (BULGARIA)','data':'1'},{'value':'Cherno More (BULGARIA)','data':'2'},{'value':'Slavia Sofia (BULGARIA)','data':'8'},{'value':'Botev Plovdiv (BULGARIA)','data':'5'},{'value':'Ludogorets (BULGARIA)','data':'12'},{'value':'Botev Vratsa (BULGARIA)','data':'13'},{'value':'CSKA 1948 Sofia (BULGARIA)','data':'9'},{'value':'CSKA Sofia (BULGARIA)','data':'10'},{'value':'Levski Sofia (BULGARIA)','data':'7'},{'value':'Arda (BULGARIA)','data':'14'},{'value':'Marek (BULGARIA2)','data':'10'},{'value':'Kariana Erden (BULGARIA2)','data':'6'},{'value':'Etar (BULGARIA2)','data':'17'},{'value':'Sportist Svoge (BULGARIA2)','data':'3'},{'value':'CSKA 1948 S. B (BULGARIA2)','data':'20'},{'value':'Botev Plovdiv B (BULGARIA2)','data':'13'},{'value':'Yantra (BULGARIA2)','data':'1'},{'value':'Spartak Varna (BULGARIA2)','data':'6'},{'value':'Maritsa Plovdiv (BULGARIA2)','data':'4'},{'value':'Levski Lom (BULGARIA2)','data':'18'},{'value':'Lokomotiv Gorna (BULGARIA2)','data':'15'},{'value':'Neftohimik (BULGARIA2)','data':'5'},{'value':'Minyor Pernik (BULGARIA2)','data':'15'},{'value':'V. Bistritsa (BULGARIA2)','data':'17'},{'value':'Montana (BULGARIA2)','data':'19'},{'value':'Dobrudzha (BULGARIA2)','data':'12'},{'value':'Sozopol (BULGARIA2)','data':'11'},{'value':'Lovech (BULGARIA2)','data':'14'},{'value':'Septemvri S. (BULGARIA2)','data':'9'},{'value':'Septemvri Sofia (BULGARIA2)','data':'8'},{'value':'Strumska slava (BULGARIA2)','data':'7'},{'value':'Hebar (BULGARIA2)','data':'2'},{'value':'Ludogorets B (BULGARIA2)','data':'16'},{'value':'Bumamuru (BURUNDI)','data':'15'},{'value':'Olympic Star (BURUNDI)','data':'6'},{'value':'Royal Muramvia (BURUNDI)','data':'2'},{'value':'Kayanza (BURUNDI)','data':'3'},{'value':'Les Elephants (BURUNDI)','data':'4'},{'value':'Aigle Noir (BURUNDI)','data':'5'},{'value':'Muzinga (BURUNDI)','data':'1'},{'value':'Musongati (BURUNDI)','data':'7'},{'value':'Inter Star (BURUNDI)','data':'8'},{'value':'A. Olympic (BURUNDI)','data':'9'},{'value':'Dynamik (BURUNDI)','data':'10'},{'value':'Rukinzo (BURUNDI)','data':'12'},{'value':'Le Messager N. (BURUNDI)','data':'14'},{'value':'Bujumbura City (BURUNDI)','data':'16'},{'value':'Vital`O (BURUNDI)','data':'11'},{'value':'Flambeau du C. (BURUNDI)','data':'13'},{'value':'Stade Renard (CAMEROON)','data':'12'},{'value':'UMS de Loum (CAMEROON)','data':'6'},{'value':'Panthère (CAMEROON)','data':'5'},{'value':'Colombe (CAMEROON)','data':'18'},{'value':'Canon Yaoundé (CAMEROON)','data':'13'},{'value':'Tonnerre (CAMEROON)','data':'19'},{'value':'Young Sport (CAMEROON)','data':'17'},{'value':'APEJES Academy (CAMEROON)','data':'20'},{'value':'Cotonsport (CAMEROON)','data':'16'},{'value':'Dragon Yaoundé (CAMEROON)','data':'15'},{'value':'Fortuna Mfou (CAMEROON)','data':'3'},{'value':'New Star (CAMEROON)','data':'21'},{'value':'Fovu (CAMEROON)','data':'11'},{'value':'Avion Academy (CAMEROON)','data':'10'},{'value':'Bamboutos (CAMEROON)','data':'9'},{'value':'Union Douala (CAMEROON)','data':'8'},{'value':'Feutcheu (CAMEROON)','data':'7'},{'value':'PWD Bamenda (CAMEROON)','data':'2'},{'value':'Yafoot (CAMEROON)','data':'1'},{'value':'Eding Sport (CAMEROON)','data':'4'},{'value':'Les Astres (CAMEROON)','data':'14'},{'value':'Ngaoundéré (CAMEROON2)','data':'3'},{'value':'Matelots (CAMEROON2)','data':'2'},{'value':'FAP (CAMEROON2)','data':'4'},{'value':'R. Bafoussam (CAMEROON2)','data':'5'},{'value':'Dynamo Douala (CAMEROON2)','data':'6'},{'value':'Stade Bertoua (CAMEROON2)','data':'7'},{'value':'Fauve Azur E. (CAMEROON2)','data':'8'},{'value':'Leopard Douala (CAMEROON2)','data':'11'},{'value':'Unisport Bafang (CAMEROON2)','data':'12'},{'value':'Foncha ST (CAMEROON2)','data':'9'},{'value':'OFTA (CAMEROON2)','data':'10'},{'value':'Lion Blesse (CAMEROON2)','data':'13'},{'value':'Aigle Royal (CAMEROON2)','data':'14'},{'value':'Renaissance (CAMEROON2)','data':'1'},{'value':'York Utd (CANADA)','data':'8'},{'value':'Cavalry (CANADA)','data':'7'},{'value':'Forge (CANADA)','data':'5'},{'value':'Pacific (CANADA)','data':'3'},{'value':'HFX Wanderers (CANADA)','data':'4'},{'value':'Edmonton (CANADA)','data':'1'},{'value':'A. Ottawa (CANADA)','data':'2'},{'value':'Valour (CANADA)','data':'6'},{'value':'Everton (CHILE)','data':'2'},{'value':'Melipilla (CHILE)','data':'5'},{'value':'U. Catolica (CHILE)','data':'13'},{'value':'Curico Unido (CHILE)','data':'12'},{'value':'O`Higgins (CHILE)','data':'15'},{'value':'Union Espanola (CHILE)','data':'4'},{'value':'S. Wanderers (CHILE)','data':'17'},{'value':'Palestino (CHILE)','data':'14'},{'value':'Antofagasta (CHILE)','data':'1'},{'value':'Huachipato (CHILE)','data':'8'},{'value':'Colo-Colo (CHILE)','data':'10'},{'value':'Nublense (CHILE)','data':'6'},{'value':'Union La Calera (CHILE)','data':'3'},{'value':'Audax Italiano (CHILE)','data':'16'},{'value':'La Serena (CHILE)','data':'11'},{'value':'U. de Chile (CHILE)','data':'7'},{'value':'Cobresal (CHILE)','data':'9'},{'value':'U. Concepcion (CHILE2)','data':'15'},{'value':'S. Morning (CHILE2)','data':'16'},{'value':'Puerto Montt (CHILE2)','data':'1'},{'value':'Fernandez Vial (CHILE2)','data':'20'},{'value':'CD Santa Cruz (CHILE2)','data':'11'},{'value':'San Marcos (CHILE2)','data':'4'},{'value':'Coquimbo Unido (CHILE2)','data':'10'},{'value':'U. San Felipe (CHILE2)','data':'14'},{'value':'San Luis (CHILE2)','data':'8'},{'value':'Deportes Temuco (CHILE2)','data':'7'},{'value':'Cobreloa (CHILE2)','data':'5'},{'value':'D. Iquique (CHILE2)','data':'9'},{'value':'Magallanes (CHILE2)','data':'3'},{'value':'Copiapo (CHILE2)','data':'2'},{'value':'Rangers (CHILE2)','data':'13'},{'value':'Barnechea (CHILE2)','data':'6'},{'value':'I. Cauquenes (CHILE3)','data':'7'},{'value':'Concepcion (CHILE3)','data':'4'},{'value':'D. Colina (CHILE3)','data':'11'},{'value':'San Antonio U. (CHILE3)','data':'5'},{'value':'D. Limache (CHILE3)','data':'6'},{'value':'D. Valdivia (CHILE3)','data':'1'},{'value':'Recoleta (CHILE3)','data':'8'},{'value':'G. Velasquez (CHILE3)','data':'9'},{'value':'Iberia (CHILE3)','data':'3'},{'value':'Lautaro de Buin (CHILE3)','data':'12'},{'value':'Rodelindo (CHILE3)','data':'2'},{'value':'Colchagua (CHILE3)','data':'10'},{'value':'Guangzhou FC (CHINA)','data':'3'},{'value':'Chongqing Lifan (CHINA)','data':'1'},{'value':'Shandong Taisha (CHINA)','data':'2'},{'value':'Shenzhen (CHINA)','data':'8'},{'value':'S. Shenhua (CHINA)','data':'15'},{'value':'Wuhan FC (CHINA)','data':'14'},{'value':'Hebei (CHINA)','data':'13'},{'value':'Shanghai Port (CHINA)','data':'12'},{'value':'Tianjin T. (CHINA)','data':'11'},{'value':'Changchun Yatai (CHINA)','data':'10'},{'value':'Guangzhou City (CHINA)','data':'4'},{'value':'Dalian P. (CHINA)','data':'9'},{'value':'Beijing Guoan (CHINA)','data':'16'},{'value':'Henan SL (CHINA)','data':'7'},{'value':'Qingdao FC (CHINA)','data':'5'},{'value':'Cangzhou (CHINA)','data':'6'},{'value':'Beijing BG (CHINA2)','data':'12'},{'value':'Jiangxi L. (CHINA2)','data':'15'},{'value':'Chengdu (CHINA2)','data':'16'},{'value':'Sichuan Jiuniu (CHINA2)','data':'1'},{'value':'Shaanxi Changan (CHINA2)','data':'2'},{'value':'Wuhan Three T. (CHINA2)','data':'3'},{'value':'Meizhou Hakka (CHINA2)','data':'9'},{'value':'Kunshan (CHINA2)','data':'11'},{'value':'Beijing IT (CHINA2)','data':'4'},{'value':'Suzhou Dongwu (CHINA2)','data':'13'},{'value':'Heilongjiang L. (CHINA2)','data':'14'},{'value':'Nantong Zhiyun (CHINA2)','data':'8'},{'value':'Nanjing (CHINA2)','data':'7'},{'value':'Zhejiang (CHINA2)','data':'6'},{'value':'Zibo Cuju (CHINA2)','data':'5'},{'value':'Xinjiang T. (CHINA2)','data':'10'},{'value':'Shenyang Urban (CHINA2)','data':'17'},{'value':'Guizhou (CHINA2)','data':'18'},{'value':'Boyaca Chico (COLOMBIA)','data':'16'},{'value':'Deportivo Cali (COLOMBIA2)','data':'8'},{'value':'Santa Fe (COLOMBIA2)','data':'7'},{'value':'Atletico Huila (COLOMBIA2)','data':'16'},{'value':'D. Quindio (COLOMBIA2)','data':'5'},{'value':'Envigado (COLOMBIA2)','data':'9'},{'value':'Patriotas (COLOMBIA2)','data':'11'},{'value':'America de Cali (COLOMBIA2)','data':'3'},{'value':'Junior (COLOMBIA2)','data':'4'},{'value':'A. Petrolera (COLOMBIA2)','data':'17'},{'value':'Deportivo Pasto (COLOMBIA2)','data':'13'},{'value':'La Equidad (COLOMBIA2)','data':'18'},{'value':'A. Nacional (COLOMBIA2)','data':'10'},{'value':'D. Pereira (COLOMBIA2)','data':'20'},{'value':'Jaguares de C. (COLOMBIA2)','data':'6'},{'value':'Deportes Tolima (COLOMBIA2)','data':'19'},{'value':'Millonarios (COLOMBIA2)','data':'14'},{'value':'Once Caldas (COLOMBIA2)','data':'15'},{'value':'R. Aguilas (COLOMBIA2)','data':'2'},{'value':'I. Medelin (COLOMBIA2)','data':'1'},{'value':'A. Bucaramanga (COLOMBIA2)','data':'12'},{'value':'Sporting SJ (COSTARICA)','data':'3'},{'value':'San Carlos (COSTARICA)','data':'11'},{'value':'ADR Jicaral (COSTARICA)','data':'2'},{'value':'Saprissa (COSTARICA)','data':'5'},{'value':'AD Grecia (COSTARICA)','data':'7'},{'value':'Guadalupe (COSTARICA)','data':'10'},{'value':'Alajuelense (COSTARICA)','data':'12'},{'value':'Santos DG (COSTARICA)','data':'6'},{'value':'Herediano (COSTARICA)','data':'9'},{'value':'Guanacasteca (COSTARICA)','data':'4'},{'value':'Zeledon (COSTARICA)','data':'1'},{'value':'Cartagines (COSTARICA)','data':'8'},{'value':'Puntarenas FC (COSTARICA3)','data':'4'},{'value':'Santa Ana (COSTARICA3)','data':'6'},{'value':'Limon (COSTARICA3)','data':'2'},{'value':'M. Liberia (COSTARICA3)','data':'7'},{'value':'M. Puntarena (COSTARICA3)','data':'16'},{'value':'Carmelita (COSTARICA3)','data':'3'},{'value':'M. Garabito (COSTARICA3)','data':'13'},{'value':'B. Mexico (COSTARICA3)','data':'10'},{'value':'CS Uruguay (COSTARICA3)','data':'5'},{'value':'Aserri (COSTARICA3)','data':'1'},{'value':'Escazucena (COSTARICA3)','data':'8'},{'value':'Consultants (COSTARICA3)','data':'17'},{'value':'Escorpiones (COSTARICA3)','data':'15'},{'value':'M. Turrialba (COSTARICA3)','data':'11'},{'value':'Puerto Golfito (COSTARICA3)','data':'9'},{'value':'Cariari Pococí (COSTARICA3)','data':'12'},{'value':'Cofutpa (COSTARICA3)','data':'14'},{'value':'Santa Rosa (COSTARICA4)','data':'11'},{'value':'M. San Ramon (COSTARICA4)','data':'18'},{'value':'Rijeka (CROATIA)','data':'7'},{'value':'Osijek (CROATIA)','data':'3'},{'value':'Slaven Belupo (CROATIA)','data':'2'},{'value':'Hajduk Split (CROATIA)','data':'6'},{'value':'Istra (CROATIA)','data':'9'},{'value':'Dragovoljac (CROATIA)','data':'10'},{'value':'Gorica (CROATIA)','data':'8'},{'value':'Lok. Zagreb (CROATIA)','data':'5'},{'value':'Sibenik (CROATIA)','data':'4'},{'value':'Dinamo Zagreb (CROATIA)','data':'1'},{'value':'Osijek B (CROATIA2)','data':'2'},{'value':'Jarun (CROATIA2)','data':'6'},{'value':'Opatija (CROATIA2)','data':'12'},{'value':'Dinamo Zagreb B (CROATIA2)','data':'16'},{'value':'Bijelo Brdo (CROATIA2)','data':'15'},{'value':'Solin (CROATIA2)','data':'14'},{'value':'Dugopolje (CROATIA2)','data':'5'},{'value':'Cibalia (CROATIA2)','data':'11'},{'value':'Dubrava Zagreb (CROATIA2)','data':'7'},{'value':'Orijent (CROATIA2)','data':'9'},{'value':'Rudes (CROATIA2)','data':'8'},{'value':'Inter Zapresic (CROATIA2)','data':'3'},{'value':'Cr. Zmijavci (CROATIA2)','data':'4'},{'value':'Kustosija (CROATIA2)','data':'13'},{'value':'Sesvete (CROATIA2)','data':'1'},{'value':'Varazdin (CROATIA2)','data':'10'},{'value':'Hajduk Split B (CROATIA2)','data':'8'},{'value':'Virovitica (CROATIA3)','data':'9'},{'value':'Koprivnica (CROATIA3)','data':'1'},{'value':'G. Durdevac (CROATIA3)','data':'1'},{'value':'Tehnicar C. (CROATIA3)','data':'2'},{'value':'P. Ludbreg (CROATIA3)','data':'11'},{'value':'Rudar Mursko S. (CROATIA3)','data':'7'},{'value':'Podravac Virje (CROATIA3)','data':'4'},{'value':'Polet (CROATIA3)','data':'8'},{'value':'M. Cakovec (CROATIA3)','data':'12'},{'value':'V. Varazdin (CROATIA3)','data':'10'},{'value':'Mladost Zdralov (CROATIA3)','data':'3'},{'value':'Krizevci (CROATIA3)','data':'5'},{'value':'Papuk (CROATIA3)','data':'2'},{'value':'Bjelovar (CROATIA3)','data':'6'},{'value':'Zmaj Blato (CROATIA4)','data':'2'},{'value':'Zmaj Makarska (CROATIA4)','data':'12'},{'value':'N. Opuzen (CROATIA4)','data':'18'},{'value':'Jadran LP (CROATIA4)','data':'11'},{'value':'Zagora (CROATIA4)','data':'5'},{'value':'RNK Split (CROATIA4)','data':'1'},{'value':'HNK Zadar (CROATIA4)','data':'13'},{'value':'GOSK Dubrovnik (CROATIA4)','data':'7'},{'value':'Junak (CROATIA4)','data':'16'},{'value':'Hrvace (CROATIA4)','data':'3'},{'value':'H. Posedarje (CROATIA4)','data':'10'},{'value':'Vodice (CROATIA4)','data':'6'},{'value':'N. Metkovic (CROATIA4)','data':'4'},{'value':'Sloga Mravince (CROATIA4)','data':'8'},{'value':'Otok (CROATIA4)','data':'2'},{'value':'Urania Baska (CROATIA4)','data':'14'},{'value':'Kamen I. (CROATIA4)','data':'15'},{'value':'Uskok Klis (CROATIA4)','data':'17'},{'value':'P. Biograd (CROATIA4)','data':'9'},{'value':'G. Zupanja (CROATIA5)','data':'10'},{'value':'S. Pozega (CROATIA5)','data':'1'},{'value':'Vuteks-Sloga (CROATIA5)','data':'11'},{'value':'Valpovka (CROATIA5)','data':'12'},{'value':'NASK Nasice (CROATIA5)','data':'2'},{'value':'Sloga Nova G. (CROATIA5)','data':'8'},{'value':'Dakovo-Croatia (CROATIA5)','data':'11'},{'value':'S. Bukovlje (CROATIA5)','data':'3'},{'value':'Vuteks-Sloga (CROATIA5)','data':'16'},{'value':'Marsonia (CROATIA5)','data':'6'},{'value':'Kutjevo (CROATIA5)','data':'14'},{'value':'Darda (CROATIA5)','data':'7'},{'value':'Gornja (CROATIA5)','data':'17'},{'value':'Oriolik Oriovac (CROATIA5)','data':'4'},{'value':'S. Pleternica (CROATIA5)','data':'13'},{'value':'Vukovar (CROATIA5)','data':'5'},{'value':'Belisce (CROATIA5)','data':'9'},{'value':'Vihor Jelisavac (CROATIA5)','data':'4'},{'value':'Bedem Ivankovo (CROATIA5)','data':'12'},{'value':'Z. Jurjevac (CROATIA5)','data':'18'},{'value':'Cepin (CROATIA5)','data':'15'},{'value':'Cres (CROATIA6)','data':'1'},{'value':'Grobnican Cavle (CROATIA6)','data':'11'},{'value':'Pazinka (CROATIA6)','data':'6'},{'value':'Vinodol (CROATIA6)','data':'9'},{'value':'Buje (CROATIA6)','data':'8'},{'value':'Rudar Labin (CROATIA6)','data':'14'},{'value':'Krk (CROATIA6)','data':'13'},{'value':'Pomorac (CROATIA6)','data':'2'},{'value':'Uljanik Pula (CROATIA6)','data':'3'},{'value':'Nehaj (CROATIA6)','data':'9'},{'value':'Jadran Porec (CROATIA6)','data':'12'},{'value':'Novigrad (CROATIA6)','data':'7'},{'value':'N. Hreljin (CROATIA6)','data':'4'},{'value':'Vinodol (CROATIA6)','data':'10'},{'value':'Buje (CROATIA6)','data':'8'},{'value':'Crikvenica (CROATIA6)','data':'5'},{'value':'Crikvenica (CROATIA6)','data':'13'},{'value':'Naprijed Hrelji (CROATIA6)','data':'4'},{'value':'Rovinj (CROATIA6)','data':'12'},{'value':'Segesta (CROATIA7)','data':'3'},{'value':'NK Lukavec (CROATIA7)','data':'12'},{'value':'Dugo Selo (CROATIA7)','data':'5'},{'value':'Trnje (CROATIA7)','data':'15'},{'value':'Vrbovec (CROATIA7)','data':'14'},{'value':'Gaj Mace (CROATIA7)','data':'2'},{'value':'Kurilovec (CROATIA7)','data':'1'},{'value':'Spansko Zagreb (CROATIA7)','data':'8'},{'value':'M. Petrinja (CROATIA7)','data':'16'},{'value':'Zagorec (CROATIA7)','data':'11'},{'value':'Bistra (CROATIA7)','data':'17'},{'value':'Lucko (CROATIA7)','data':'10'},{'value':'Tresnjevka (CROATIA7)','data':'4'},{'value':'Ponikve (CROATIA7)','data':'8'},{'value':'T. Ravnice (CROATIA7)','data':'6'},{'value':'HASK (CROATIA7)','data':'9'},{'value':'Maksimir Zagreb (CROATIA7)','data':'18'},{'value':'Karlovac (CROATIA7)','data':'13'},{'value':'Vrapce Zagreb (CROATIA7)','data':'7'},{'value':'Omonia Nicosia (CYPRUS)','data':'3'},{'value':'Apollon (CYPRUS)','data':'11'},{'value':'Doxa Katokopia (CYPRUS)','data':'2'},{'value':'Olympiakos N. (CYPRUS)','data':'7'},{'value':'Aris (CYPRUS)','data':'8'},{'value':'PAEEK (CYPRUS)','data':'9'},{'value':'APOEL Nicosia (CYPRUS)','data':'6'},{'value':'Paphos (CYPRUS)','data':'5'},{'value':'AEL Limassol (CYPRUS)','data':'4'},{'value':'Anorthosis (CYPRUS)','data':'10'},{'value':'AEK Larnaca (CYPRUS)','data':'1'},{'value':'Achnas (CYPRUS)','data':'12'},{'value':'Enosis P. (CYPRUS2)','data':'13'},{'value':'O. Sotiras (CYPRUS2)','data':'15'},{'value':'Kouris Erimi (CYPRUS2)','data':'3'},{'value':'Ermis (CYPRUS2)','data':'14'},{'value':'Nea Salamis (CYPRUS2)','data':'12'},{'value':'Ahironas (CYPRUS2)','data':'7'},{'value':'O. Aradippou (CYPRUS2)','data':'3'},{'value':'D. Ypsonas (CYPRUS2)','data':'18'},{'value':'Olympiada Lympi (CYPRUS2)','data':'6'},{'value':'Xylotympou (CYPRUS2)','data':'1'},{'value':'A. Chloraka (CYPRUS2)','data':'2'},{'value':'Othellos (CYPRUS2)','data':'4'},{'value':'Ayia Napa (CYPRUS2)','data':'10'},{'value':'Alki Oroklini (CYPRUS2)','data':'5'},{'value':'Digenis (CYPRUS2)','data':'11'},{'value':'Anagennisi D. (CYPRUS2)','data':'11'},{'value':'Karmiotissa (CYPRUS2)','data':'8'},{'value':'T. Lakatamias (CYPRUS2)','data':'8'},{'value':'ASIL Lysi (CYPRUS2)','data':'16'},{'value':'Omonia 29is Mai (CYPRUS2)','data':'9'},{'value':'Omonia Psevda (CYPRUS2)','data':'4'},{'value':'Zakakiou (CYPRUS2)','data':'9'},{'value':'Teplice (CZECHREPUBLIC)','data':'12'},{'value':'Sparta Prague (CZECHREPUBLIC)','data':'7'},{'value':'Karvina (CZECHREPUBLIC)','data':'4'},{'value':'Mlada Boleslav (CZECHREPUBLIC)','data':'10'},{'value':'Bohemians (CZECHREPUBLIC)','data':'2'},{'value':'Banik Ostrava (CZECHREPUBLIC)','data':'6'},{'value':'Jablonec (CZECHREPUBLIC)','data':'5'},{'value':'Pardubice (CZECHREPUBLIC)','data':'3'},{'value':'Sigma Olomouc (CZECHREPUBLIC)','data':'8'},{'value':'Slovacko (CZECHREPUBLIC)','data':'14'},{'value':'C. Budejovice (CZECHREPUBLIC)','data':'11'},{'value':'Slavia Prague (CZECHREPUBLIC)','data':'16'},{'value':'Hradec Kralove (CZECHREPUBLIC)','data':'1'},{'value':'Slovan Liberec (CZECHREPUBLIC)','data':'13'},{'value':'Viktoria Plzen (CZECHREPUBLIC)','data':'9'},{'value':'Zlin (CZECHREPUBLIC)','data':'15'},{'value':'Lisen (CZECHREPUBLIC2)','data':'13'},{'value':'Prostejov (CZECHREPUBLIC2)','data':'15'},{'value':'Dukla Praha (CZECHREPUBLIC2)','data':'9'},{'value':'Slavoj Vydehrad (CZECHREPUBLIC2)','data':'3'},{'value':'Varnsdorf (CZECHREPUBLIC2)','data':'2'},{'value':'Vlasim (CZECHREPUBLIC2)','data':'12'},{'value':'Vikto Zizkov (CZECHREPUBLIC2)','data':'14'},{'value':'Trinec (CZECHREPUBLIC2)','data':'5'},{'value':'Chrudim (CZECHREPUBLIC2)','data':'7'},{'value':'Jihlava (CZECHREPUBLIC2)','data':'1'},{'value':'Zbrojovka Brno (CZECHREPUBLIC2)','data':'4'},{'value':'Taborsko (CZECHREPUBLIC2)','data':'3'},{'value':'Usti nad Labem (CZECHREPUBLIC2)','data':'6'},{'value':'Opava (CZECHREPUBLIC2)','data':'11'},{'value':'Pribram (CZECHREPUBLIC2)','data':'16'},{'value':'Vyskov (CZECHREPUBLIC2)','data':'10'},{'value':'Sparta Prague B (CZECHREPUBLIC2)','data':'8'},{'value':'Uhersky Brod (CZECHREPUBLIC3)','data':'12'},{'value':'Domazlice (CZECHREPUBLIC3)','data':'29'},{'value':'Pardubice B (CZECHREPUBLIC3)','data':'30'},{'value':'Prepere (CZECHREPUBLIC3)','data':'31'},{'value':'Viktoria Plzen  (CZECHREPUBLIC3)','data':'28'},{'value':'Sigma Olomouc B (CZECHREPUBLIC3)','data':'3'},{'value':'Brozany (CZECHREPUBLIC3)','data':'25'},{'value':'Han. Kromeriz (CZECHREPUBLIC3)','data':'15'},{'value':'Vrchovina (CZECHREPUBLIC3)','data':'6'},{'value':'Budejovice U19 (CZECHREPUBLIC3)','data':'16'},{'value':'Karvina U19 (CZECHREPUBLIC3)','data':'15'},{'value':'M. Boleslav U19 (CZECHREPUBLIC3)','data':'14'},{'value':'H. Kralove U19 (CZECHREPUBLIC3)','data':'13'},{'value':'Plzen U19 (CZECHREPUBLIC3)','data':'12'},{'value':'Hlucin (CZECHREPUBLIC3)','data':'9'},{'value':'Slavia Prague B (CZECHREPUBLIC3)','data':'20'},{'value':'Chlumec nad C. (CZECHREPUBLIC3)','data':'15'},{'value':'Bohemians (CZECHREPUBLIC3)','data':'14'},{'value':'Usti nad Orlici (CZECHREPUBLIC3)','data':'13'},{'value':'Zbuzany (CZECHREPUBLIC3)','data':'12'},{'value':'Zivanice (CZECHREPUBLIC3)','data':'11'},{'value':'Hradec Kralove  (CZECHREPUBLIC3)','data':'17'},{'value':'Rakovnik (CZECHREPUBLIC3)','data':'27'},{'value':'Admira Prague (CZECHREPUBLIC3)','data':'19'},{'value':'Fastav Zlin U19 (CZECHREPUBLIC3)','data':'11'},{'value':'Karlovy Vary (CZECHREPUBLIC3)','data':'21'},{'value':'Pribram B (CZECHREPUBLIC3)','data':'22'},{'value':'Zapy (CZECHREPUBLIC3)','data':'23'},{'value':'Dukla Prague B (CZECHREPUBLIC3)','data':'24'},{'value':'Slovacko U19 (CZECHREPUBLIC3)','data':'4'},{'value':'Frydek-Mistek (CZECHREPUBLIC3)','data':'17'},{'value':'Teplice B (CZECHREPUBLIC3)','data':'26'},{'value':'Mlada Boleslav  (CZECHREPUBLIC3)','data':'18'},{'value':'Dolni Benesov (CZECHREPUBLIC3)','data':'16'},{'value':'S. Liberec B (CZECHREPUBLIC3)','data':'10'},{'value':'Odra Petrkovice (CZECHREPUBLIC3)','data':'9'},{'value':'Jablonec B (CZECHREPUBLIC3)','data':'16'},{'value':'Otrokovice (CZECHREPUBLIC3)','data':'11'},{'value':'Unicov (CZECHREPUBLIC3)','data':'1'},{'value':'Velke Mezirici (CZECHREPUBLIC3)','data':'8'},{'value':'Banik Ostrava B (CZECHREPUBLIC3)','data':'4'},{'value':'Znojmo (CZECHREPUBLIC3)','data':'7'},{'value':'Zlin B (CZECHREPUBLIC3)','data':'5'},{'value':'Slovacko B (CZECHREPUBLIC3)','data':'18'},{'value':'Slovan Rosice (CZECHREPUBLIC3)','data':'14'},{'value':'Vratimov (CZECHREPUBLIC3)','data':'13'},{'value':'Blansko (CZECHREPUBLIC3)','data':'10'},{'value':'Jihlava B (CZECHREPUBLIC3)','data':'2'},{'value':'Brno U19 (CZECHREPUBLIC3)','data':'2'},{'value':'Slovan Velvary (CZECHREPUBLIC3)','data':'9'},{'value':'Ostrava U19 (CZECHREPUBLIC3)','data':'3'},{'value':'Hostoun (CZECHREPUBLIC3)','data':'8'},{'value':'Benesov (CZECHREPUBLIC3)','data':'7'},{'value':'Kraluv Dvur (CZECHREPUBLIC3)','data':'1'},{'value':'Povltava FA (CZECHREPUBLIC3)','data':'2'},{'value':'Loko Vltavin (CZECHREPUBLIC3)','data':'3'},{'value':'Pisek (CZECHREPUBLIC3)','data':'4'},{'value':'Banik Sokolov (CZECHREPUBLIC3)','data':'5'},{'value':'Motorlet Prague (CZECHREPUBLIC3)','data':'6'},{'value':'S. Olomouc U19 (CZECHREPUBLIC3)','data':'10'},{'value':'Opava U19 (CZECHREPUBLIC3)','data':'9'},{'value':'Pardubice U19 (CZECHREPUBLIC3)','data':'7'},{'value':'Sparta P. U19 (CZECHREPUBLIC3)','data':'8'},{'value':'Pribram U19 (CZECHREPUBLIC3)','data':'1'},{'value':'Meteor P. U19 (CZECHREPUBLIC3)','data':'5'},{'value':'Slavia P. U19 (CZECHREPUBLIC3)','data':'6'},{'value':'Liberec W (CZECHREPUBLIC4)','data':'5'},{'value':'Slavia Prague W (CZECHREPUBLIC4)','data':'4'},{'value':'Plzen W (CZECHREPUBLIC4)','data':'6'},{'value':'Sparta Prague W (CZECHREPUBLIC4)','data':'7'},{'value':'Dukla Prague W (CZECHREPUBLIC4)','data':'2'},{'value':'Pardubice W (CZECHREPUBLIC4)','data':'3'},{'value':'L. Brno W (CZECHREPUBLIC4)','data':'8'},{'value':'Slovacko W (CZECHREPUBLIC4)','data':'1'},{'value':'Silkeborg (DENMARK)','data':'11'},{'value':'Aalborg BK (DENMARK)','data':'8'},{'value':'Vejle BK (DENMARK)','data':'5'},{'value':'AGF Aarhus (DENMARK)','data':'9'},{'value':'FC Kobenhavn (DENMARK)','data':'7'},{'value':'Brondby IF (DENMARK)','data':'10'},{'value':'SonderjyskE (DENMARK)','data':'12'},{'value':'Odense BK (DENMARK)','data':'2'},{'value':'Viborg (DENMARK)','data':'4'},{'value':'FC Midtjylland (DENMARK)','data':'1'},{'value':'Randers FC (DENMARK)','data':'6'},{'value':'Nordsjaelland (DENMARK)','data':'3'},{'value':'Fredericia (DENMARK2)','data':'1'},{'value':'Kolding IF (DENMARK2)','data':'12'},{'value':'Jammerbugt (DENMARK2)','data':'8'},{'value':'Vendsyssel (DENMARK2)','data':'10'},{'value':'Fremad Amager (DENMARK2)','data':'4'},{'value':'Esbjerg (DENMARK2)','data':'9'},{'value':'AC Horsens (DENMARK2)','data':'5'},{'value':'Hvidovre (DENMARK2)','data':'7'},{'value':'HB Koge (DENMARK2)','data':'6'},{'value':'Hobro (DENMARK2)','data':'2'},{'value':'Helsingor (DENMARK2)','data':'3'},{'value':'Nykobing (DENMARK2)','data':'11'},{'value':'Lyngby (DENMARK2)','data':'12'},{'value':'Skive (DENMARK2)','data':'7'},{'value':'Oure (DENMARK3)','data':'3'},{'value':'BK Frem (DENMARK3)','data':'2'},{'value':'Aalborg BK W (DENMARK3)','data':'8'},{'value':'Nordsjaelland W (DENMARK3)','data':'7'},{'value':'FC Thisted W (DENMARK3)','data':'6'},{'value':'Naesby (DENMARK3)','data':'4'},{'value':'F. Hjorring W (DENMARK3)','data':'4'},{'value':'Aarhus Fremad (DENMARK3)','data':'9'},{'value':'AGF Aarhus W (DENMARK3)','data':'3'},{'value':'KoldingQ W (DENMARK3)','data':'2'},{'value':'Koge W (DENMARK3)','data':'5'},{'value':'VSK Arhus (DENMARK3)','data':'5'},{'value':'Dalum (DENMARK3)','data':'6'},{'value':'Thisted (DENMARK3)','data':'8'},{'value':'Holstebro (DENMARK3)','data':'10'},{'value':'Middelfart (DENMARK3)','data':'11'},{'value':'Holbaek (DENMARK3)','data':'13'},{'value':'B 93 (DENMARK3)','data':'14'},{'value':'Sydvest (DENMARK3)','data':'1'},{'value':'Brondby W (DENMARK3)','data':'1'},{'value':'Brabrand (DENMARK3)','data':'7'},{'value':'Roskilde (DENMARK4)','data':'14'},{'value':'Slagelse (DENMARK4)','data':'11'},{'value':'KFUM Roskilde (DENMARK4)','data':'12'},{'value':'Hellerup IK (DENMARK4)','data':'1'},{'value':'Naestved (DENMARK4)','data':'13'},{'value':'Vanlose (DENMARK4)','data':'10'},{'value':'Bronshoj (DENMARK4)','data':'9'},{'value':'Skovshoved (DENMARK4)','data':'8'},{'value':'AB Copenhagen (DENMARK4)','data':'6'},{'value':'Hillerod (DENMARK4)','data':'5'},{'value':'Avarta (DENMARK4)','data':'4'},{'value':'FA 2000 (DENMARK4)','data':'3'},{'value':'AB Tarnby (DENMARK4)','data':'2'},{'value':'Dauphins Noirs (DRCONGO)','data':'14'},{'value':'JSK (DRCONGO)','data':'13'},{'value':'Bazano (DRCONGO)','data':'10'},{'value':'Simba (DRCONGO)','data':'9'},{'value':'Blessing (DRCONGO)','data':'8'},{'value':'Mazembe (DRCONGO)','data':'7'},{'value':'Vita Club (DRCONGO)','data':'12'},{'value':'AC Rangers (DRCONGO)','data':'11'},{'value':'RCK (DRCONGO)','data':'6'},{'value':'Motema Pembe (DRCONGO)','data':'5'},{'value':'Saint Eloi L. (DRCONGO)','data':'4'},{'value':'Lubumbashi S. (DRCONGO)','data':'3'},{'value':'Maniema Union (DRCONGO)','data':'2'},{'value':'Renaissance (DRCONGO)','data':'1'},{'value':'Don Bosco (DRCONGO)','data':'15'},{'value':'Sanga Balende (DRCONGO)','data':'16'},{'value':'Macará (ECUADOR2)','data':'5'},{'value':'I. del Valle (ECUADOR2)','data':'9'},{'value':'Barcelona SC (ECUADOR2)','data':'13'},{'value':'Tecnico U. (ECUADOR2)','data':'16'},{'value':'Nueve Octubre (ECUADOR2)','data':'11'},{'value':'Manta (ECUADOR2)','data':'14'},{'value':'Guayaquil City (ECUADOR2)','data':'6'},{'value':'U. Catolica (ECUADOR2)','data':'4'},{'value':'Emelec (ECUADOR2)','data':'8'},{'value':'Delfin (ECUADOR2)','data':'15'},{'value':'Aucas (ECUADOR2)','data':'1'},{'value':'LDU Quito (ECUADOR2)','data':'12'},{'value':'Olmedo (ECUADOR2)','data':'3'},{'value':'Mushuc Runa (ECUADOR2)','data':'2'},{'value':'D. Cuenca (ECUADOR2)','data':'7'},{'value':'Orense (ECUADOR2)','data':'10'},{'value':'America de Q. (ECUADOR3)','data':'9'},{'value':'LDU Portoviejo (ECUADOR3)','data':'5'},{'value':'Gualaceo (ECUADOR3)','data':'4'},{'value':'Chacaritas (ECUADOR3)','data':'7'},{'value':'A. Porteno (ECUADOR3)','data':'1'},{'value':'Fuerza Amarilla (ECUADOR3)','data':'6'},{'value':'El Nacional (ECUADOR3)','data':'10'},{'value':'Santa Rita (ECUADOR3)','data':'4'},{'value':'Santo Domingo (ECUADOR3)','data':'2'},{'value':'Guayaquil (ECUADOR3)','data':'6'},{'value':'Cumbaya (ECUADOR3)','data':'3'},{'value':'I. Juniors (ECUADOR3)','data':'8'},{'value':'ENPPI (EGYPT)','data':'11'},{'value':'Ghazl El M. (EGYPT)','data':'17'},{'value':'Smouha (EGYPT)','data':'3'},{'value':'Coca-Cola (EGYPT)','data':'5'},{'value':'Misr L. Makassa (EGYPT)','data':'14'},{'value':'Al Ahly (EGYPT)','data':'16'},{'value':'Ismaily (EGYPT)','data':'15'},{'value':'Al Masry (EGYPT)','data':'18'},{'value':'Zamalek (EGYPT)','data':'12'},{'value':'Al Mokawloon (EGYPT)','data':'7'},{'value':'Al Ittihad (EGYPT)','data':'4'},{'value':'Pyramids FC (EGYPT)','data':'13'},{'value':'El Sharqia D. (EGYPT)','data':'8'},{'value':'Pharco (EGYPT)','data':'6'},{'value':'El Geish (EGYPT)','data':'2'},{'value':'El Gouna (EGYPT)','data':'9'},{'value':'Ceramica C. (EGYPT)','data':'10'},{'value':'National Bank (EGYPT)','data':'1'},{'value':'Sohag (EGYPT2)','data':'12'},{'value':'Beni Suef (EGYPT2)','data':'7'},{'value':'Telephonaat B. (EGYPT2)','data':'1'},{'value':'El Alameen (EGYPT2)','data':'10'},{'value':'Aluminium N. (EGYPT2)','data':'6'},{'value':'Fayoum (EGYPT2)','data':'4'},{'value':'El Minya (EGYPT2)','data':'14'},{'value':'Qena (EGYPT2)','data':'13'},{'value':'Asyut P. (EGYPT2)','data':'5'},{'value':'Kima Aswan (EGYPT2)','data':'8'},{'value':'Shoban Moslemen (EGYPT2)','data':'13'},{'value':'Asmant Asyut (EGYPT2)','data':'14'},{'value':'Markaz Shabab (EGYPT2)','data':'15'},{'value':'Tahta (EGYPT2)','data':'16'},{'value':'Aswan (EGYPT2)','data':'11'},{'value':'Dayrout (EGYPT2)','data':'16'},{'value':'El Badari (EGYPT2)','data':'2'},{'value':'Mallawi (EGYPT2)','data':'3'},{'value':'Tamya (EGYPT2)','data':'9'},{'value':'El Madina EM (EGYPT2)','data':'15'},{'value':'Bur Fouad (EGYPT3)','data':'1'},{'value':'Porto Suez (EGYPT3)','data':'6'},{'value':'Suez (EGYPT3)','data':'7'},{'value':'El Seka (EGYPT3)','data':'2'},{'value':'Tersana (EGYPT3)','data':'5'},{'value':'El Daklyeh (EGYPT3)','data':'11'},{'value':'Al Nasr (EGYPT3)','data':'16'},{'value':'Al Merreikh (EGYPT3)','data':'14'},{'value':'Belbeis (EGYPT3)','data':'13'},{'value':'Banha (EGYPT3)','data':'10'},{'value':'Petrojet (EGYPT3)','data':'12'},{'value':'Nojom El M. (EGYPT3)','data':'10'},{'value':'ZED (EGYPT3)','data':'8'},{'value':'O. El Qanah (EGYPT3)','data':'15'},{'value':'Gomhoreyat S. (EGYPT3)','data':'13'},{'value':'Sers Elyan (EGYPT3)','data':'14'},{'value':'El Entag El H. (EGYPT3)','data':'4'},{'value':'Wadi Degla (EGYPT3)','data':'9'},{'value':'Tanta (EGYPT3)','data':'16'},{'value':'Itesalat (EGYPT3)','data':'3'},{'value':'Dikernis (EGYPT4)','data':'7'},{'value':'Kafr El Sheikh (EGYPT4)','data':'6'},{'value':'Alaab Damanhour (EGYPT4)','data':'12'},{'value':'Biyala (EGYPT4)','data':'2'},{'value':'Alexandria SC (EGYPT4)','data':'4'},{'value':'Haras El Hodood (EGYPT4)','data':'16'},{'value':'Maleyet Kafr (EGYPT4)','data':'10'},{'value':'El Raja (EGYPT4)','data':'15'},{'value':'Al Jazeera (EGYPT4)','data':'13'},{'value':'Al Hamam (EGYPT4)','data':'14'},{'value':'Baladeyet (EGYPT4)','data':'2'},{'value':'Beni Ebeid (EGYPT4)','data':'16'},{'value':'Pioneers (EGYPT4)','data':'9'},{'value':'Sed Elmahla (EGYPT4)','data':'13'},{'value':'Olympic Club (EGYPT4)','data':'1'},{'value':'El Zarqa (EGYPT4)','data':'11'},{'value':'El Mansoura (EGYPT4)','data':'8'},{'value':'Egy Salloum (EGYPT4)','data':'5'},{'value':'El Magd (EGYPT4)','data':'3'},{'value':'Abu Qir Semad (EGYPT4)','data':'10'},{'value':'Arsenal (ENGLAND)','data':'2'},{'value':'Leicester City (ENGLAND)','data':'11'},{'value':'Norwich City (ENGLAND)','data':'15'},{'value':'West Ham Utd (ENGLAND)','data':'18'},{'value':'Liverpool (ENGLAND)','data':'16'},{'value':'Tottenham (ENGLAND)','data':'19'},{'value':'Crystal Palace (ENGLAND)','data':'8'},{'value':'Newcastle Utd (ENGLAND)','data':'17'},{'value':'Aston Villa (ENGLAND)','data':'14'},{'value':'Manchester City (ENGLAND)','data':'20'},{'value':'Burnley (ENGLAND)','data':'5'},{'value':'Manchester Utd (ENGLAND)','data':'3'},{'value':'Southampton (ENGLAND)','data':'10'},{'value':'Wolverhampton (ENGLAND)','data':'12'},{'value':'Everton (ENGLAND)','data':'9'},{'value':'Leeds Utd (ENGLAND)','data':'4'},{'value':'Chelsea (ENGLAND)','data':'7'},{'value':'Watford (ENGLAND)','data':'13'},{'value':'Brighton (ENGLAND)','data':'6'},{'value':'Brentford (ENGLAND)','data':'1'},{'value':'Rushden & D. (ENGLAND10)','data':'21'},{'value':'Peterborough S. (ENGLAND10)','data':'13'},{'value':'Nuneaton Town (ENGLAND10)','data':'11'},{'value':'Redditch Utd (ENGLAND10)','data':'15'},{'value':'Needham Market (ENGLAND10)','data':'8'},{'value':'Stratford Town (ENGLAND10)','data':'6'},{'value':'Biggleswade (ENGLAND10)','data':'12'},{'value':'St. Ives Town (ENGLAND10)','data':'19'},{'value':'Banbury Utd (ENGLAND10)','data':'1'},{'value':'Tamworth (ENGLAND10)','data':'18'},{'value':'Rushall (ENGLAND10)','data':'14'},{'value':'Leiston (ENGLAND10)','data':'4'},{'value':'Alvechurch (ENGLAND10)','data':'20'},{'value':'Hednesford (ENGLAND10)','data':'7'},{'value':'Royston (ENGLAND10)','data':'17'},{'value':'Barwell (ENGLAND10)','data':'10'},{'value':'Lowestoft (ENGLAND10)','data':'9'},{'value':'Hitchin Town (ENGLAND10)','data':'16'},{'value':'Stourbridge (ENGLAND10)','data':'2'},{'value':'Coalville Town (ENGLAND10)','data':'5'},{'value':'Bromsgrove (ENGLAND10)','data':'3'},{'value':'Taunton Town (ENGLAND11)','data':'22'},{'value':'Salisbury (ENGLAND11)','data':'18'},{'value':'Poole Town (ENGLAND11)','data':'8'},{'value':'Chesham Utd (ENGLAND11)','data':'2'},{'value':'Gosport Borough (ENGLAND11)','data':'7'},{'value':'Kings Langley (ENGLAND11)','data':'13'},{'value':'Weston-s.-Mare (ENGLAND11)','data':'14'},{'value':'Swindon Sup. (ENGLAND11)','data':'12'},{'value':'Hayes & Yeading (ENGLAND11)','data':'11'},{'value':'Beaconsfield (ENGLAND11)','data':'4'},{'value':'Yate Town (ENGLAND11)','data':'10'},{'value':'Dorchester (ENGLAND11)','data':'3'},{'value':'Hendon (ENGLAND11)','data':'20'},{'value':'Tiverton Town (ENGLAND11)','data':'1'},{'value':'Wimborne (ENGLAND11)','data':'21'},{'value':'Truro City (ENGLAND11)','data':'19'},{'value':'Harrow Borough (ENGLAND11)','data':'9'},{'value':'Walton Casuals (ENGLAND11)','data':'6'},{'value':'Hartley Wintney (ENGLAND11)','data':'16'},{'value':'Merthyr Town (ENGLAND11)','data':'15'},{'value':'Metropolitan P. (ENGLAND11)','data':'17'},{'value':'Farnborough (ENGLAND11)','data':'5'},{'value':'Maldon & T. (ENGLAND12)','data':'14'},{'value':'Coggeshall Town (ENGLAND12)','data':'20'},{'value':'Hashtag United (ENGLAND12)','data':'19'},{'value':'Stowmarket Town (ENGLAND12)','data':'15'},{'value':'AFC Sudbury (ENGLAND12)','data':'1'},{'value':'Barking (ENGLAND12)','data':'12'},{'value':'Witham Town (ENGLAND12)','data':'10'},{'value':'Soham Town (ENGLAND12)','data':'17'},{'value':'Histon (ENGLAND12)','data':'16'},{'value':'Heybridge S. (ENGLAND12)','data':'4'},{'value':'Felixstowe & W. (ENGLAND12)','data':'5'},{'value':'Grays Athletic (ENGLAND12)','data':'7'},{'value':'Basildon Utd (ENGLAND12)','data':'6'},{'value':'Bury Town (ENGLAND12)','data':'8'},{'value':'Aveley (ENGLAND12)','data':'2'},{'value':'Hullbridge S. (ENGLAND12)','data':'11'},{'value':'Great Wakering  (ENGLAND12)','data':'9'},{'value':'Dereham Town (ENGLAND12)','data':'3'},{'value':'Brentwood Town (ENGLAND12)','data':'18'},{'value':'Cambridge City (ENGLAND12)','data':'9'},{'value':'Tilbury (ENGLAND12)','data':'17'},{'value':'Canvey Island (ENGLAND12)','data':'16'},{'value':'Romford (ENGLAND12)','data':'13'},{'value':'Harlow Town (ENGLAND13)','data':'19'},{'value':'Basingstoke T. (ENGLAND13)','data':'16'},{'value':'Whyteleafe (ENGLAND13)','data':'15'},{'value':'Sutton CR (ENGLAND13)','data':'18'},{'value':'Thatcham Town (ENGLAND13)','data':'11'},{'value':'South Park (ENGLAND13)','data':'8'},{'value':'Northwood (ENGLAND13)','data':'12'},{'value':'FC Romania (ENGLAND13)','data':'20'},{'value':'Binfield (ENGLAND13)','data':'19'},{'value':'Ware (ENGLAND13)','data':'12'},{'value':'Westfield (S) (ENGLAND13)','data':'13'},{'value':'Bedfont Sports (ENGLAND13)','data':'1'},{'value':'Marlow (ENGLAND13)','data':'7'},{'value':'Bracknell Town (ENGLAND13)','data':'6'},{'value':'Chipstead (ENGLAND13)','data':'2'},{'value':'Chalfont St P. (ENGLAND13)','data':'3'},{'value':'Ashford Town M. (ENGLAND13)','data':'4'},{'value':'Chertsey Town (ENGLAND13)','data':'10'},{'value':'Uxbridge (ENGLAND13)','data':'17'},{'value':'Hertford Town (ENGLAND13)','data':'14'},{'value':'Hanwell Town (ENGLAND13)','data':'5'},{'value':'Waltham Abbey (ENGLAND13)','data':'15'},{'value':'Staines Town (ENGLAND13)','data':'9'},{'value':'Tooting & M. (ENGLAND13)','data':'14'},{'value':'Guernsey (ENGLAND13)','data':'20'},{'value':'Faversham Town (ENGLAND14)','data':'14'},{'value':'Hastings Utd (ENGLAND14)','data':'7'},{'value':'Cray Valley PM (ENGLAND14)','data':'5'},{'value':'Haywards Heath (ENGLAND14)','data':'9'},{'value':'East Grinstead (ENGLAND14)','data':'10'},{'value':'Herne Bay (ENGLAND14)','data':'8'},{'value':'Sittingbourne (ENGLAND14)','data':'15'},{'value':'Hythe Town (ENGLAND14)','data':'11'},{'value':'Three Bridges (ENGLAND14)','data':'17'},{'value':'Whitstable Town (ENGLAND14)','data':'19'},{'value':'VCD Athletic (ENGLAND14)','data':'4'},{'value':'Whitehawk (ENGLAND14)','data':'6'},{'value':'Sevenoaks Town (ENGLAND14)','data':'20'},{'value':'Burgess Hill (ENGLAND14)','data':'2'},{'value':'Lancing (ENGLAND14)','data':'16'},{'value':'Phoenix Sports (ENGLAND14)','data':'13'},{'value':'Chichester City (ENGLAND14)','data':'3'},{'value':'Ramsgate (ENGLAND14)','data':'18'},{'value':'Corinthian (ENGLAND14)','data':'12'},{'value':'Ashford Utd (ENGLAND14)','data':'1'},{'value':'Liverpool U23 (ENGLAND15)','data':'1'},{'value':'Brighton U23 (ENGLAND15)','data':'10'},{'value':'Tottenham U23 (ENGLAND15)','data':'11'},{'value':'Everton U23 (ENGLAND15)','data':'6'},{'value':'Derby C. U23 (ENGLAND15)','data':'9'},{'value':'Man City U23 (ENGLAND15)','data':'2'},{'value':'Blackburn U23 (ENGLAND15)','data':'5'},{'value':'Arsenal U23 (ENGLAND15)','data':'14'},{'value':'Crystal P. U23 (ENGLAND15)','data':'7'},{'value':'Leicester U23 (ENGLAND15)','data':'4'},{'value':'Man Utd U23 (ENGLAND15)','data':'3'},{'value':'Leeds U23 (ENGLAND15)','data':'8'},{'value':'West Ham U23 (ENGLAND15)','data':'13'},{'value':'Chelsea U23 (ENGLAND15)','data':'12'},{'value':'Reading U23 (ENGLAND16)','data':'4'},{'value':'Middlesb. U23 (ENGLAND16)','data':'12'},{'value':'Wolves U23 (ENGLAND16)','data':'11'},{'value':'Burnley U23 (ENGLAND16)','data':'10'},{'value':'Newcastle U23 (ENGLAND16)','data':'3'},{'value':'West Brom U23 (ENGLAND16)','data':'9'},{'value':'Stoke City U23 (ENGLAND16)','data':'5'},{'value':'Norwich U23 (ENGLAND16)','data':'2'},{'value':'Southampton U23 (ENGLAND16)','data':'1'},{'value':'Sunderland U23 (ENGLAND16)','data':'7'},{'value':'Fulham U23 (ENGLAND16)','data':'8'},{'value':'Birmingham U23 (ENGLAND16)','data':'6'},{'value':'Nottingham U23 (ENGLAND16)','data':'14'},{'value':'Aston Villa U23 (ENGLAND16)','data':'13'},{'value':'Birmingham W (ENGLAND17)','data':'8'},{'value':'Tottenham W (ENGLAND17)','data':'7'},{'value':'Chelsea W (ENGLAND17)','data':'10'},{'value':'West Ham W (ENGLAND17)','data':'12'},{'value':'Leicester W (ENGLAND17)','data':'4'},{'value':'Everton W (ENGLAND17)','data':'5'},{'value':'Reading W (ENGLAND17)','data':'2'},{'value':'Brighton W (ENGLAND17)','data':'11'},{'value':'Arsenal W (ENGLAND17)','data':'9'},{'value':'Man City W (ENGLAND17)','data':'6'},{'value':'Aston Villa W (ENGLAND17)','data':'3'},{'value':'Man Utd W (ENGLAND17)','data':'1'},{'value':'Durham W (ENGLAND18)','data':'1'},{'value':'Sunderland W (ENGLAND18)','data':'6'},{'value':'Watford W (ENGLAND18)','data':'2'},{'value':'Lewes W (ENGLAND18)','data':'9'},{'value':'Sheffield Utd W (ENGLAND18)','data':'4'},{'value':'London City L W (ENGLAND18)','data':'12'},{'value':'Liverpool W (ENGLAND18)','data':'11'},{'value':'London Bees W (ENGLAND18)','data':'4'},{'value':'Coventry Utd W (ENGLAND18)','data':'5'},{'value':'Crystal P. W (ENGLAND18)','data':'7'},{'value':'Charlton W (ENGLAND18)','data':'10'},{'value':'Bristol City W (ENGLAND18)','data':'8'},{'value':'Blackburn W (ENGLAND18)','data':'3'},{'value':'Millwall U23 (ENGLAND19)','data':'9'},{'value':'Wigan U23 (ENGLAND19)','data':'2'},{'value':'Peterbor. U23 (ENGLAND19)','data':'6'},{'value':'Bristol C. U23 (ENGLAND19)','data':'15'},{'value':'Sheffield W U23 (ENGLAND19)','data':'16'},{'value':'QP Rangers U23 (ENGLAND19)','data':'11'},{'value':'Charlton U23 (ENGLAND19)','data':'17'},{'value':'Cardiff U23 (ENGLAND19)','data':'1'},{'value':'Crewe U23 (ENGLAND19)','data':'10'},{'value':'Ipswich U23 (ENGLAND19)','data':'3'},{'value':'Coventry U23 (ENGLAND19)','data':'4'},{'value':'Barnsley U23 (ENGLAND19)','data':'8'},{'value':'Swansea U23 (ENGLAND19)','data':'5'},{'value':'Colchester U23 (ENGLAND19)','data':'7'},{'value':'Sheffield U U23 (ENGLAND19)','data':'14'},{'value':'Hull City U23 (ENGLAND19)','data':'12'},{'value':'Watford U23 (ENGLAND19)','data':'13'},{'value':'Millwall (ENGLAND2)','data':'16'},{'value':'Huddersfield (ENGLAND2)','data':'10'},{'value':'Reading (ENGLAND2)','data':'18'},{'value':'Derby County (ENGLAND2)','data':'9'},{'value':'Coventry City (ENGLAND2)','data':'23'},{'value':'Middlesbrough (ENGLAND2)','data':'22'},{'value':'Bournemouth (ENGLAND2)','data':'1'},{'value':'Stoke City (ENGLAND2)','data':'17'},{'value':'Nottm Forest (ENGLAND2)','data':'24'},{'value':'Bristol City (ENGLAND2)','data':'5'},{'value':'Luton Town (ENGLAND2)','data':'11'},{'value':'Barnsley (ENGLAND2)','data':'8'},{'value':'Blackburn (ENGLAND2)','data':'3'},{'value':'Cardiff City (ENGLAND2)','data':'7'},{'value':'Hull City (ENGLAND2)','data':'14'},{'value':'Swansea City (ENGLAND2)','data':'4'},{'value':'QP Rangers (ENGLAND2)','data':'15'},{'value':'Peterborough (ENGLAND2)','data':'12'},{'value':'Birmingham City (ENGLAND2)','data':'20'},{'value':'Blackpool (ENGLAND2)','data':'6'},{'value':'Preston (ENGLAND2)','data':'13'},{'value':'Fulham (ENGLAND2)','data':'21'},{'value':'West Brom (ENGLAND2)','data':'2'},{'value':'Sheffield Utd (ENGLAND2)','data':'19'},{'value':'Burton Albion (ENGLAND3)','data':'18'},{'value':'Lincoln City (ENGLAND3)','data':'12'},{'value':'Plymouth (ENGLAND3)','data':'16'},{'value':'Portsmouth (ENGLAND3)','data':'10'},{'value':'AFC Wimbledon (ENGLAND3)','data':'8'},{'value':'Bolton (ENGLAND3)','data':'1'},{'value':'Oxford Utd (ENGLAND3)','data':'4'},{'value':'Wycombe (ENGLAND3)','data':'21'},{'value':'Rotherham (ENGLAND3)','data':'15'},{'value':'Morecambe (ENGLAND3)','data':'14'},{'value':'Cheltenham (ENGLAND3)','data':'6'},{'value':'Sheffield Wed (ENGLAND3)','data':'24'},{'value':'Accrington (ENGLAND3)','data':'22'},{'value':'Crewe Alexandra (ENGLAND3)','data':'5'},{'value':'Charlton (ENGLAND3)','data':'23'},{'value':'Cambridge Utd (ENGLAND3)','data':'3'},{'value':'Doncaster (ENGLAND3)','data':'7'},{'value':'Ipswich Town (ENGLAND3)','data':'13'},{'value':'Fleetwood (ENGLAND3)','data':'9'},{'value':'Gillingham (ENGLAND3)','data':'11'},{'value':'Milton Keynes (ENGLAND3)','data':'2'},{'value':'Shrewsbury (ENGLAND3)','data':'17'},{'value':'Sunderland (ENGLAND3)','data':'19'},{'value':'Wigan Athletic (ENGLAND3)','data':'20'},{'value':'Hartlepool (ENGLAND4)','data':'9'},{'value':'Sutton Utd (ENGLAND4)','data':'6'},{'value':'Walsall (ENGLAND4)','data':'24'},{'value':'Harrogate (ENGLAND4)','data':'7'},{'value':'Newport (ENGLAND4)','data':'16'},{'value':'Scunthorpe (ENGLAND4)','data':'19'},{'value':'Northampton (ENGLAND4)','data':'13'},{'value':'Exeter City (ENGLAND4)','data':'3'},{'value':'Swindon Town (ENGLAND4)','data':'20'},{'value':'Bristol Rovers (ENGLAND4)','data':'12'},{'value':'Barrow (ENGLAND4)','data':'22'},{'value':'Carlisle Utd (ENGLAND4)','data':'1'},{'value':'Mansfield (ENGLAND4)','data':'11'},{'value':'Tranmere (ENGLAND4)','data':'23'},{'value':'Oldham (ENGLAND4)','data':'15'},{'value':'Rochdale (ENGLAND4)','data':'8'},{'value':'Leyton Orient (ENGLAND4)','data':'18'},{'value':'Salford City (ENGLAND4)','data':'17'},{'value':'Port Vale (ENGLAND4)','data':'14'},{'value':'Crawley Town (ENGLAND4)','data':'10'},{'value':'Forest Green (ENGLAND4)','data':'5'},{'value':'Bradford (ENGLAND4)','data':'4'},{'value':'Colchester Utd (ENGLAND4)','data':'2'},{'value':'Stevenage (ENGLAND4)','data':'21'},{'value':'Southend Utd (ENGLAND5)','data':'10'},{'value':'Notts County (ENGLAND5)','data':'4'},{'value':'Altrincham (ENGLAND5)','data':'14'},{'value':'Halifax Town (ENGLAND5)','data':'7'},{'value':'Yeovil Town (ENGLAND5)','data':'20'},{'value':'Weymouth (ENGLAND5)','data':'17'},{'value':'Barnet (ENGLAND5)','data':'3'},{'value':'Eastleigh (ENGLAND5)','data':'23'},{'value':'Grimsby (ENGLAND5)','data':'22'},{'value':'Wrexham (ENGLAND5)','data':'19'},{'value':'Dover Athletic (ENGLAND5)','data':'5'},{'value':'Boreham Wood (ENGLAND5)','data':'18'},{'value':'Solihull Moors (ENGLAND5)','data':'6'},{'value':'Woking (ENGLAND5)','data':'16'},{'value':'Chesterfield (ENGLAND5)','data':'2'},{'value':'Wealdstone (ENGLAND5)','data':'15'},{'value':'Stockport (ENGLAND5)','data':'11'},{'value':'Torquay Utd (ENGLAND5)','data':'13'},{'value':'Macclesfield (ENGLAND5)','data':'11'},{'value':'Kings Lynn (ENGLAND5)','data':'9'},{'value':'Dagenham & R. (ENGLAND5)','data':'12'},{'value':'Aldershot Town (ENGLAND5)','data':'1'},{'value':'Bromley (ENGLAND5)','data':'21'},{'value':'Maidenhead Utd (ENGLAND5)','data':'8'},{'value':'Chorley (ENGLAND6)','data':'7'},{'value':'Telford Utd (ENGLAND6)','data':'10'},{'value':'York City (ENGLAND6)','data':'21'},{'value':'Curzon (ENGLAND6)','data':'6'},{'value':'Bradford PA (ENGLAND6)','data':'16'},{'value':'Farsley Celtic (ENGLAND6)','data':'14'},{'value':'Boston Utd (ENGLAND6)','data':'3'},{'value':'Leamington (ENGLAND6)','data':'17'},{'value':'Gateshead FC (ENGLAND6)','data':'18'},{'value':'Spennymoor (ENGLAND6)','data':'4'},{'value':'Southport (ENGLAND6)','data':'19'},{'value':'Alfreton Town (ENGLAND6)','data':'2'},{'value':'Chester (ENGLAND6)','data':'5'},{'value':'Darlington (ENGLAND6)','data':'9'},{'value':'Guiseley (ENGLAND6)','data':'11'},{'value':'Brackley Town (ENGLAND6)','data':'8'},{'value':'Hereford Utd (ENGLAND6)','data':'13'},{'value':'Kidderminster (ENGLAND6)','data':'22'},{'value':'Gloucester City (ENGLAND6)','data':'20'},{'value':'Kettering Town (ENGLAND6)','data':'15'},{'value':'Blyth Spartans (ENGLAND6)','data':'1'},{'value':'AFC Fylde (ENGLAND6)','data':'12'},{'value':'Concord Rangers (ENGLAND7)','data':'5'},{'value':'Chippenham (ENGLAND7)','data':'8'},{'value':'Hemel Hempstead (ENGLAND7)','data':'16'},{'value':'Havant & W. (ENGLAND7)','data':'13'},{'value':'Dartford (ENGLAND7)','data':'20'},{'value':'Hampton & R. (ENGLAND7)','data':'10'},{'value':'St Albans (ENGLAND7)','data':'19'},{'value':'Bath City (ENGLAND7)','data':'1'},{'value':'Oxford City (ENGLAND7)','data':'4'},{'value':'Chelmsford City (ENGLAND7)','data':'18'},{'value':'Maidstone Utd (ENGLAND7)','data':'15'},{'value':'Billericay Town (ENGLAND7)','data':'2'},{'value':'Hungerford (ENGLAND7)','data':'21'},{'value':'Dorking (ENGLAND7)','data':'6'},{'value':'Eastbourne Boro (ENGLAND7)','data':'9'},{'value':'Slough Town (ENGLAND7)','data':'17'},{'value':'Dulwich Hamlet (ENGLAND7)','data':'7'},{'value':'Ebbsfleet Utd (ENGLAND7)','data':'11'},{'value':'Braintree Town (ENGLAND7)','data':'3'},{'value':'Tonbridge (ENGLAND7)','data':'12'},{'value':'Welling Utd (ENGLAND7)','data':'14'},{'value':'Merstham (ENGLAND8)','data':'22'},{'value':'Kingstonian (ENGLAND8)','data':'11'},{'value':'Bishop`s St. (ENGLAND8)','data':'18'},{'value':'Bognor Regis (ENGLAND8)','data':'17'},{'value':'Brightlingsea (ENGLAND8)','data':'21'},{'value':'Margate (ENGLAND8)','data':'16'},{'value':'Potters Bar (ENGLAND8)','data':'13'},{'value':'East Thurrock (ENGLAND8)','data':'4'},{'value':'Corinthian-C. (ENGLAND8)','data':'14'},{'value':'Horsham (ENGLAND8)','data':'9'},{'value':'Cray Wanderers (ENGLAND8)','data':'5'},{'value':'Bowers & Pitsea (ENGLAND8)','data':'19'},{'value':'Enfield Town (ENGLAND8)','data':'2'},{'value':'Lewes (ENGLAND8)','data':'6'},{'value':'Hornchurch (ENGLAND8)','data':'10'},{'value':'Cheshunt (ENGLAND8)','data':'3'},{'value':'Leatherhead (ENGLAND8)','data':'20'},{'value':'Folkestone (ENGLAND8)','data':'7'},{'value':'Worthing (ENGLAND8)','data':'8'},{'value':'Wingate & F. (ENGLAND8)','data':'15'},{'value':'Haringey (ENGLAND8)','data':'12'},{'value':'Carshalton (ENGLAND8)','data':'1'},{'value':'Radcliffe (ENGLAND9)','data':'15'},{'value':'Stafford (ENGLAND9)','data':'21'},{'value':'Grantham (ENGLAND9)','data':'16'},{'value':'Morpeth Town (ENGLAND9)','data':'22'},{'value':'Hyde Utd (ENGLAND9)','data':'9'},{'value':'FC United (ENGLAND9)','data':'20'},{'value':'Buxton (ENGLAND9)','data':'5'},{'value':'Matlock (ENGLAND9)','data':'2'},{'value':'Scarborough (ENGLAND9)','data':'4'},{'value':'Lancaster City (ENGLAND9)','data':'11'},{'value':'Mickleover (ENGLAND9)','data':'18'},{'value':'Stalybridge (ENGLAND9)','data':'14'},{'value':'Nantwich (ENGLAND9)','data':'13'},{'value':'Gainsborough (ENGLAND9)','data':'7'},{'value':'Bamber Bridge (ENGLAND9)','data':'6'},{'value':'Ashton Utd (ENGLAND9)','data':'1'},{'value':'Whitby Town (ENGLAND9)','data':'12'},{'value':'Warrington (ENGLAND9)','data':'19'},{'value':'Basford Utd (ENGLAND9)','data':'3'},{'value':'Witton Albion (ENGLAND9)','data':'8'},{'value':'Atherton C. (ENGLAND9)','data':'10'},{'value':'South Shields (ENGLAND9)','data':'17'},{'value':'Levadia (ESTONIA)','data':'1'},{'value':'Paide (ESTONIA)','data':'5'},{'value':'Legion (ESTONIA)','data':'8'},{'value':'Flora (ESTONIA)','data':'10'},{'value':'Narva Trans (ESTONIA)','data':'6'},{'value':'Tammeka (ESTONIA)','data':'7'},{'value':'Tulevik (ESTONIA)','data':'4'},{'value':'Nomme Kalju (ESTONIA)','data':'9'},{'value':'Vaprus (ESTONIA)','data':'2'},{'value':'Kuressaare (ESTONIA)','data':'3'},{'value':'Flora B (ESTONIA2)','data':'6'},{'value':'Elva (ESTONIA2)','data':'8'},{'value':'Levadia B (ESTONIA2)','data':'4'},{'value':'Tammeka B (ESTONIA2)','data':'10'},{'value':'Parnu (ESTONIA2)','data':'7'},{'value':'Tallinna Kalev (ESTONIA2)','data':'1'},{'value':'Paide B (ESTONIA2)','data':'3'},{'value':'Tartu Welco (ESTONIA2)','data':'5'},{'value':'Nomme Utd (ESTONIA2)','data':'2'},{'value':'Maardu (ESTONIA2)','data':'9'},{'value':'B68 Toftir (FAROEISLANDS)','data':'9'},{'value':'Klaksvik (FAROEISLANDS)','data':'10'},{'value':'TB Tvoroyri (FAROEISLANDS)','data':'8'},{'value':'Vikingur (FAROEISLANDS)','data':'7'},{'value':'NSI Runavik (FAROEISLANDS)','data':'6'},{'value':'B36 Torshavn (FAROEISLANDS)','data':'4'},{'value':'07 Vestur (FAROEISLANDS)','data':'3'},{'value':'IF Fuglafjordur (FAROEISLANDS)','data':'2'},{'value':'Streymur (FAROEISLANDS)','data':'1'},{'value':'HB Torshavn (FAROEISLANDS)','data':'5'},{'value':'B71 Sandur (FAROEISLANDS2)','data':'3'},{'value':'Skala (FAROEISLANDS2)','data':'8'},{'value':'HB B (FAROEISLANDS2)','data':'9'},{'value':'Streymur B (FAROEISLANDS2)','data':'10'},{'value':'AB Argir (FAROEISLANDS2)','data':'7'},{'value':'B36 Torshavn B (FAROEISLANDS2)','data':'6'},{'value':'NSI Runavik B (FAROEISLANDS2)','data':'1'},{'value':'Klaksvik B (FAROEISLANDS2)','data':'4'},{'value':'Vikingur B (FAROEISLANDS2)','data':'2'},{'value':'Suduroy (FAROEISLANDS2)','data':'5'},{'value':'Netherlands (FIFAQUAL)','data':'4'},{'value':'Malta (FIFAQUAL)','data':'7'},{'value':'Cyprus (FIFAQUAL)','data':'5'},{'value':'North Macedonia (FIFAQUAL)','data':'40'},{'value':'Turkey (FIFAQUAL)','data':'3'},{'value':'Italy (FIFAQUAL)','data':'45'},{'value':'Wales (FIFAQUAL)','data':'20'},{'value':'Switzerland (FIFAQUAL)','data':'26'},{'value':'Denmark (FIFAQUAL)','data':'28'},{'value':'Finland (FIFAQUAL)','data':'15'},{'value':'Belgium (FIFAQUAL)','data':'19'},{'value':'Russia (FIFAQUAL)','data':'8'},{'value':'England (FIFAQUAL)','data':'31'},{'value':'Scotland (FIFAQUAL)','data':'49'},{'value':'Austria (FIFAQUAL)','data':'50'},{'value':'Germany (FIFAQUAL)','data':'35'},{'value':'Ukraine (FIFAQUAL)','data':'18'},{'value':'Czech Republic (FIFAQUAL)','data':'2'},{'value':'Poland (FIFAQUAL)','data':'34'},{'value':'Slovakia (FIFAQUAL)','data':'6'},{'value':'Spain (FIFAQUAL)','data':'41'},{'value':'Sweden (FIFAQUAL)','data':'43'},{'value':'Hungary (FIFAQUAL)','data':'33'},{'value':'Portugal (FIFAQUAL)','data':'11'},{'value':'France (FIFAQUAL)','data':'17'},{'value':'Croatia (FIFAQUAL)','data':'10'},{'value':'Greece (FIFAQUAL)','data':'42'},{'value':'Bulgaria (FIFAQUAL)','data':'25'},{'value':'Israel (FIFAQUAL)','data':'27'},{'value':'Andorra (FIFAQUAL)','data':'29'},{'value':'Albania (FIFAQUAL)','data':'30'},{'value':'San Marino (FIFAQUAL)','data':'32'},{'value':'Iceland (FIFAQUAL)','data':'36'},{'value':'Liechtenstein (FIFAQUAL)','data':'37'},{'value':'Montenegro (FIFAQUAL)','data':'24'},{'value':'Romania (FIFAQUAL)','data':'39'},{'value':'Luxembourg (FIFAQUAL)','data':'52'},{'value':'Georgia (FIFAQUAL)','data':'44'},{'value':'North. Ireland (FIFAQUAL)','data':'46'},{'value':'Moldova (FIFAQUAL)','data':'47'},{'value':'Faroe Islands (FIFAQUAL)','data':'48'},{'value':'Belarus (FIFAQUAL)','data':'51'},{'value':'Kazakhstan (FIFAQUAL)','data':'53'},{'value':'Estonia (FIFAQUAL)','data':'1'},{'value':'Kosovo (FIFAQUAL)','data':'55'},{'value':'Armenia (FIFAQUAL)','data':'38'},{'value':'Norway (FIFAQUAL)','data':'22'},{'value':'Gibraltar (FIFAQUAL)','data':'21'},{'value':'Bosnia-H. (FIFAQUAL)','data':'16'},{'value':'Ireland (FIFAQUAL)','data':'14'},{'value':'Latvia (FIFAQUAL)','data':'23'},{'value':'Lithuania (FIFAQUAL)','data':'54'},{'value':'Slovenia (FIFAQUAL)','data':'9'},{'value':'Azerbaijan (FIFAQUAL)','data':'12'},{'value':'Serbia (FIFAQUAL)','data':'13'},{'value':'Colombia (FIFAQUALSA)','data':'7'},{'value':'Peru (FIFAQUALSA)','data':'2'},{'value':'Ecuador (FIFAQUALSA)','data':'6'},{'value':'Venezuela (FIFAQUALSA)','data':'8'},{'value':'Brazil (FIFAQUALSA)','data':'9'},{'value':'Bolivia (FIFAQUALSA)','data':'10'},{'value':'Paraguay (FIFAQUALSA)','data':'1'},{'value':'Chile (FIFAQUALSA)','data':'4'},{'value':'Argentina (FIFAQUALSA)','data':'5'},{'value':'Uruguay (FIFAQUALSA)','data':'3'},{'value':'Ilves (FINLAND)','data':'12'},{'value':'SJK (FINLAND)','data':'7'},{'value':'Oulu (FINLAND)','data':'11'},{'value':'KTP (FINLAND)','data':'8'},{'value':'Haka (FINLAND)','data':'10'},{'value':'KuPS (FINLAND)','data':'4'},{'value':'HJK Helsinki (FINLAND)','data':'1'},{'value':'Mariehamn (FINLAND)','data':'5'},{'value':'Honka (FINLAND)','data':'2'},{'value':'HIFK (FINLAND)','data':'9'},{'value':'Lahti (FINLAND)','data':'6'},{'value':'Inter Turku (FINLAND)','data':'3'},{'value':'Mikkelin (FINLAND2)','data':'8'},{'value':'MuSa (FINLAND2)','data':'12'},{'value':'TPS (FINLAND2)','data':'11'},{'value':'Gnistan (FINLAND2)','data':'9'},{'value':'Jaro (FINLAND2)','data':'7'},{'value':'VPS (FINLAND2)','data':'5'},{'value':'Rovaniemi (FINLAND2)','data':'4'},{'value':'Klubi-04 (FINLAND2)','data':'3'},{'value':'JIPPO (FINLAND2)','data':'2'},{'value':'KPV Kokkola (FINLAND2)','data':'1'},{'value':'PK-35 (FINLAND2)','data':'6'},{'value':'Ekenas IF (FINLAND2)','data':'10'},{'value':'Kiffen (FINLAND3)','data':'2'},{'value':'KaPa (FINLAND3)','data':'11'},{'value':'PEPO (FINLAND3)','data':'10'},{'value':'NJS (FINLAND3)','data':'9'},{'value':'MiPK (FINLAND3)','data':'8'},{'value':'PeKa (FINLAND3)','data':'6'},{'value':'Reipas (FINLAND3)','data':'7'},{'value':'KuFu-98 (FINLAND3)','data':'3'},{'value':'MYPA (FINLAND3)','data':'1'},{'value':'Atlantis (FINLAND3)','data':'12'},{'value':'JaPS (FINLAND3)','data':'4'},{'value':'PKKU (FINLAND3)','data':'5'},{'value':'GrIFK (FINLAND4)','data':'9'},{'value':'EPS (FINLAND4)','data':'1'},{'value':'Ilves-Kissat (FINLAND4)','data':'2'},{'value':'Honka Akatemia (FINLAND4)','data':'3'},{'value':'HJS Akatemia (FINLAND4)','data':'4'},{'value':'Ilves B (FINLAND4)','data':'5'},{'value':'Jazz Pori (FINLAND4)','data':'6'},{'value':'KaaPo (FINLAND4)','data':'8'},{'value':'SalPa (FINLAND4)','data':'10'},{'value':'TPV (FINLAND4)','data':'11'},{'value':'PIF Pargas (FINLAND4)','data':'12'},{'value':'VJS (FINLAND4)','data':'7'},{'value':'PS Kemi (FINLAND5)','data':'2'},{'value':'Kemi City (FINLAND5)','data':'12'},{'value':'JS Hercules (FINLAND5)','data':'1'},{'value':'GBK (FINLAND5)','data':'8'},{'value':'OTP (FINLAND5)','data':'4'},{'value':'Rovaniemi B (FINLAND5)','data':'3'},{'value':'JJK (FINLAND5)','data':'11'},{'value':'JBK (FINLAND5)','data':'5'},{'value':'Vaajakoski (FINLAND5)','data':'7'},{'value':'VIFK (FINLAND5)','data':'10'},{'value':'SJK Akatemia (FINLAND5)','data':'6'},{'value':'Narpes Kraft (FINLAND5)','data':'9'},{'value':'OLS Oulu (FINLAND5)','data':'2'},{'value':'JyPK W (FINLAND6)','data':'4'},{'value':'PK35 Helsinki W (FINLAND6)','data':'5'},{'value':'TiPS W (FINLAND6)','data':'6'},{'value':'KuPS W (FINLAND6)','data':'7'},{'value':'Ilves W (FINLAND6)','data':'10'},{'value':'Honka W (FINLAND6)','data':'9'},{'value':'HPS W (FINLAND6)','data':'8'},{'value':'HJK W (FINLAND6)','data':'3'},{'value':'Aland Utd W (FINLAND6)','data':'2'},{'value':'PK35 Vantaa W (FINLAND6)','data':'1'},{'value':'Clermont (FRANCE)','data':'14'},{'value':'Angers (FRANCE)','data':'20'},{'value':'Marseille (FRANCE)','data':'8'},{'value':'Saint-Etienne (FRANCE)','data':'17'},{'value':'Metz (FRANCE)','data':'3'},{'value':'Montpellier (FRANCE)','data':'7'},{'value':'Lyon (FRANCE)','data':'1'},{'value':'Lens (FRANCE)','data':'12'},{'value':'Nice (FRANCE)','data':'15'},{'value':'Paris SG (FRANCE)','data':'10'},{'value':'Nantes (FRANCE)','data':'6'},{'value':'Rennes (FRANCE)','data':'11'},{'value':'Brest (FRANCE)','data':'2'},{'value':'Bordeaux (FRANCE)','data':'13'},{'value':'Troyes (FRANCE)','data':'9'},{'value':'Lille (FRANCE)','data':'4'},{'value':'Reims (FRANCE)','data':'16'},{'value':'Lorient (FRANCE)','data':'18'},{'value':'Strasbourg (FRANCE)','data':'19'},{'value':'Monaco (FRANCE)','data':'5'},{'value':'Anglet Genets (FRANCE10)','data':'14'},{'value':'Poitiers (FRANCE10)','data':'11'},{'value':'Tartas-St Y. (FRANCE10)','data':'8'},{'value':'Neuville (FRANCE10)','data':'7'},{'value':'Niort B (FRANCE10)','data':'13'},{'value':'Bordeaux  B (FRANCE10)','data':'5'},{'value':'Lege-Cap-Ferret (FRANCE10)','data':'2'},{'value':'Bressuire (FRANCE10)','data':'3'},{'value':'Chatellerault (FRANCE10)','data':'6'},{'value':'Av. Bayonnais (FRANCE10)','data':'1'},{'value':'Stade Bordelais (FRANCE10)','data':'12'},{'value':'Cognac (FRANCE10)','data':'13'},{'value':'Libourne (FRANCE10)','data':'10'},{'value':'Cognac (FRANCE10)','data':'9'},{'value':'Chauvigny (FRANCE10)','data':'4'},{'value':'CA Neuville (FRANCE10)','data':'7'},{'value':'Vimy (FRANCE11)','data':'12'},{'value':'Amiens SC B (FRANCE11)','data':'10'},{'value':'IC Croix (FRANCE11)','data':'3'},{'value':'Marcq-en-B. (FRANCE11)','data':'11'},{'value':'Feignies-A. (FRANCE11)','data':'6'},{'value':'US Chantilly (FRANCE11)','data':'13'},{'value':'Valenciennes B (FRANCE11)','data':'2'},{'value':'Boulogne B (FRANCE11)','data':'7'},{'value':'Wasquehal (FRANCE11)','data':'14'},{'value':'Saint-Omer (FRANCE11)','data':'5'},{'value':'Lille B (FRANCE11)','data':'1'},{'value':'Amiens AC (FRANCE11)','data':'4'},{'value':'Maubeuge (FRANCE11)','data':'9'},{'value':'Le Touquet (FRANCE11)','data':'8'},{'value':'Alberes Argelès (FRANCE12)','data':'6'},{'value':'Rodez B (FRANCE12)','data':'10'},{'value':'Fabregues (FRANCE12)','data':'8'},{'value':'Alberes Argeles (FRANCE12)','data':'7'},{'value':'Blagnac (FRANCE12)','data':'5'},{'value':'Balma (FRANCE12)','data':'7'},{'value':'Aigues-Mortes (FRANCE12)','data':'13'},{'value':'Castanet (FRANCE12)','data':'3'},{'value':'Stade Beaucaire (FRANCE12)','data':'12'},{'value':'Agde (FRANCE12)','data':'1'},{'value':'Muret (FRANCE12)','data':'14'},{'value':'Ales (FRANCE12)','data':'9'},{'value':'Nimes B (FRANCE12)','data':'4'},{'value':'Toulouse B (FRANCE12)','data':'2'},{'value':'Narbonne (FRANCE12)','data':'11'},{'value':'Saran Municipal (FRANCE13)','data':'6'},{'value':'USM Saran (FRANCE13)','data':'1'},{'value':'Chateauneuf (FRANCE13)','data':'13'},{'value':'Chateauroux B (FRANCE13)','data':'8'},{'value':'Montlouis (FRANCE13)','data':'4'},{'value':'Orleans B (FRANCE13)','data':'14'},{'value':'Chartres B (FRANCE13)','data':'9'},{'value':'Montargis (FRANCE13)','data':'2'},{'value':'Avoine OCC (FRANCE13)','data':'10'},{'value':'Vierzon (FRANCE13)','data':'1'},{'value':'O. Tourangeau (FRANCE13)','data':'3'},{'value':'St-Jean-le-B. (FRANCE13)','data':'5'},{'value':'Tours (FRANCE13)','data':'5'},{'value':'Deols (FRANCE13)','data':'7'},{'value':'Amilly (FRANCE13)','data':'11'},{'value':'Bourges Foot 18 (FRANCE13)','data':'12'},{'value':'Dijon W (FRANCE14)','data':'3'},{'value':'Saint-Étienne W (FRANCE14)','data':'7'},{'value':'Paris FC W (FRANCE14)','data':'9'},{'value':'Lyon W (FRANCE14)','data':'1'},{'value':'Guingamp W (FRANCE14)','data':'10'},{'value':'Paris SG W (FRANCE14)','data':'11'},{'value':'Issy W (FRANCE14)','data':'6'},{'value':'Reims W (FRANCE14)','data':'2'},{'value':'Soyaux W (FRANCE14)','data':'5'},{'value':'Montpellier W (FRANCE14)','data':'4'},{'value':'Fleury W (FRANCE14)','data':'12'},{'value':'Le Havre W (FRANCE14)','data':'2'},{'value':'Bordeaux W (FRANCE14)','data':'8'},{'value':'Quevilly Rouen (FRANCE2)','data':'8'},{'value':'SC Bastia (FRANCE2)','data':'1'},{'value':'Grenoble (FRANCE2)','data':'9'},{'value':'Nimes (FRANCE2)','data':'2'},{'value':'Nancy (FRANCE2)','data':'14'},{'value':'Amiens (FRANCE2)','data':'3'},{'value':'Sochaux (FRANCE2)','data':'20'},{'value':'USL Dunkerque (FRANCE2)','data':'7'},{'value':'Auxerre (FRANCE2)','data':'4'},{'value':'Le Havre (FRANCE2)','data':'11'},{'value':'Toulouse (FRANCE2)','data':'15'},{'value':'Paris FC (FRANCE2)','data':'10'},{'value':'Ajaccio (FRANCE2)','data':'16'},{'value':'Pau FC (FRANCE2)','data':'13'},{'value':'Caen (FRANCE2)','data':'5'},{'value':'Guingamp (FRANCE2)','data':'12'},{'value':'Dijon (FRANCE2)','data':'19'},{'value':'Niort (FRANCE2)','data':'18'},{'value':'Rodez Aveyron (FRANCE2)','data':'6'},{'value':'Valenciennes (FRANCE2)','data':'17'},{'value':'Chambly (FRANCE3)','data':'16'},{'value':'Concarneau (FRANCE3)','data':'17'},{'value':'Stade Briochin (FRANCE3)','data':'14'},{'value':'Bourg-en-Bresse (FRANCE3)','data':'1'},{'value':'Sete (FRANCE3)','data':'3'},{'value':'Bastia-Borgo (FRANCE3)','data':'4'},{'value':'Villefranche (FRANCE3)','data':'2'},{'value':'Cholet (FRANCE3)','data':'10'},{'value':'Sedan (FRANCE3)','data':'11'},{'value':'Red Star (FRANCE3)','data':'18'},{'value':'Le Mans (FRANCE3)','data':'13'},{'value':'Chateauroux (FRANCE3)','data':'9'},{'value':'Boulogne (FRANCE3)','data':'15'},{'value':'Orleans (FRANCE3)','data':'6'},{'value':'Laval (FRANCE3)','data':'5'},{'value':'Avranches (FRANCE3)','data':'8'},{'value':'Annecy (FRANCE3)','data':'12'},{'value':'Creteil (FRANCE3)','data':'7'},{'value':'Blois (FRANCE4)','data':'1'},{'value':'Poissy (FRANCE4)','data':'7'},{'value':'Caen B (FRANCE4)','data':'14'},{'value':'Guingamp B (FRANCE4)','data':'11'},{'value':'Versailles (FRANCE4)','data':'2'},{'value':'Granville (FRANCE4)','data':'4'},{'value':'Rouen (FRANCE4)','data':'12'},{'value':'St-Pryve St-H. (FRANCE4)','data':'9'},{'value':'Romorantin (FRANCE4)','data':'8'},{'value':'Chartres (FRANCE4)','data':'3'},{'value':'Stade Plabennec (FRANCE4)','data':'13'},{'value':'Vannes (FRANCE4)','data':'6'},{'value':'Vitré (FRANCE4)','data':'16'},{'value':'Saint-Malo (FRANCE4)','data':'10'},{'value':'Chateaubriant (FRANCE4)','data':'5'},{'value':'Lorient B (FRANCE4)','data':'15'},{'value':'Fleury-Merogis (FRANCE5)','data':'14'},{'value':'Beauvais (FRANCE5)','data':'12'},{'value':'Metz B (FRANCE5)','data':'6'},{'value':'Reims B (FRANCE5)','data':'3'},{'value':'St Maur Lusit. (FRANCE5)','data':'10'},{'value':'Epinal (FRANCE5)','data':'2'},{'value':'St Quentin (FRANCE5)','data':'9'},{'value':'Ste Genevieve (FRANCE5)','data':'11'},{'value':'Auxerre B (FRANCE5)','data':'1'},{'value':'Belfort (FRANCE5)','data':'4'},{'value':'Entente SSG (FRANCE5)','data':'8'},{'value':'Paris 13 A. (FRANCE5)','data':'15'},{'value':'Schiltigheim (FRANCE5)','data':'16'},{'value':'Lens B (FRANCE5)','data':'13'},{'value':'Bobigny (FRANCE5)','data':'5'},{'value':'Haguenau (FRANCE5)','data':'7'},{'value':'Grasse (FRANCE6)','data':'11'},{'value':'G. O. A. L. (FRANCE6)','data':'5'},{'value':'Monaco B (FRANCE6)','data':'2'},{'value':'Marseille B (FRANCE6)','data':'13'},{'value':'Martigues (FRANCE6)','data':'10'},{'value':'Aubagne (FRANCE6)','data':'3'},{'value':'Hyeres (FRANCE6)','data':'8'},{'value':'Louhans-Cuis. (FRANCE6)','data':'7'},{'value':'Frejus St-Raph. (FRANCE6)','data':'4'},{'value':'GFA Rumilly (FRANCE6)','data':'14'},{'value':'Toulon (FRANCE6)','data':'6'},{'value':'SC Lyon (FRANCE6)','data':'12'},{'value':'Lyon B (FRANCE6)','data':'1'},{'value':'Jura Sud Foot (FRANCE6)','data':'15'},{'value':'Saint-Priest (FRANCE6)','data':'16'},{'value':'Marignane (FRANCE6)','data':'9'},{'value':'Les Herbiers (FRANCE7)','data':'12'},{'value':'Chamalieres (FRANCE7)','data':'11'},{'value':'Angers B (FRANCE7)','data':'2'},{'value':'Stade Montois (FRANCE7)','data':'10'},{'value':'Colomiers (FRANCE7)','data':'5'},{'value':'Nantes B (FRANCE7)','data':'7'},{'value':'Trelissac (FRANCE7)','data':'3'},{'value':'Bourges Foot 18 (FRANCE7)','data':'8'},{'value':'Angouleme (FRANCE7)','data':'16'},{'value':'Bourges 18 (FRANCE7)','data':'16'},{'value':'Montpellier B (FRANCE7)','data':'13'},{'value':'Le Puy (FRANCE7)','data':'6'},{'value':'Andrezieux (FRANCE7)','data':'1'},{'value':'Canet R. (FRANCE7)','data':'9'},{'value':'Beziers (FRANCE7)','data':'15'},{'value':'Moulins-Yzeure (FRANCE7)','data':'4'},{'value':'Bergerac (FRANCE7)','data':'14'},{'value':'Bourges Foot (FRANCE7)','data':'6'},{'value':'Les Mureaux (FRANCE8)','data':'4'},{'value':'Blanc Mesnil (FRANCE8)','data':'6'},{'value':'Aubervilliers (FRANCE8)','data':'2'},{'value':'Drancy JA (FRANCE8)','data':'9'},{'value':'Creteil L. B (FRANCE8)','data':'12'},{'value':'Ivry US (FRANCE8)','data':'11'},{'value':'Les Ulis (FRANCE8)','data':'1'},{'value':'Paris SG B (FRANCE8)','data':'8'},{'value':'Mantes (FRANCE8)','data':'5'},{'value':'Racing CFF (FRANCE8)','data':'10'},{'value':'Paris FC B (FRANCE8)','data':'3'},{'value':'Meaux Academy (FRANCE8)','data':'14'},{'value':'Bretigny FCS (FRANCE8)','data':'13'},{'value':'Linas-Montlhery (FRANCE8)','data':'7'},{'value':'Dinamo Tbilisi (GEORGIA)','data':'1'},{'value':'Shukura (GEORGIA)','data':'6'},{'value':'Samtredia (GEORGIA)','data':'8'},{'value':'L. Tbilisi (GEORGIA)','data':'10'},{'value':'Dila Gori (GEORGIA)','data':'5'},{'value':'Torpedo Kutaisi (GEORGIA)','data':'3'},{'value':'Saburtalo (GEORGIA)','data':'9'},{'value':'Telavi (GEORGIA)','data':'7'},{'value':'Samgurali (GEORGIA)','data':'2'},{'value':'Dinamo Batumi (GEORGIA)','data':'4'},{'value':'Gareji Sagarejo (GEORGIA2)','data':'2'},{'value':'Shevardeni (GEORGIA2)','data':'4'},{'value':'Merani Tbilisi (GEORGIA2)','data':'1'},{'value':'Rustavi (GEORGIA2)','data':'7'},{'value':'Zugdidi (GEORGIA2)','data':'3'},{'value':'Sioni Bolsini (GEORGIA2)','data':'8'},{'value':'Merani Martvili (GEORGIA2)','data':'10'},{'value':'WIT Georgia (GEORGIA2)','data':'6'},{'value':'Chikhura (GEORGIA2)','data':'5'},{'value':'Gagra (GEORGIA2)','data':'9'},{'value':'Guria (GEORGIA3)','data':'9'},{'value':'Varketili (GEORGIA3)','data':'14'},{'value':'Gori (GEORGIA3)','data':'13'},{'value':'Tbilisi City (GEORGIA3)','data':'11'},{'value':'Bakhmaro (GEORGIA3)','data':'8'},{'value':'Merani Tbilisi  (GEORGIA3)','data':'10'},{'value':'M. Chiatura (GEORGIA3)','data':'12'},{'value':'Saburtalo B (GEORGIA3)','data':'1'},{'value':'Kolkheti Khobi (GEORGIA3)','data':'2'},{'value':'Kolkheti Poti (GEORGIA3)','data':'3'},{'value':'Didube 2014 (GEORGIA3)','data':'4'},{'value':'Meshakhte (GEORGIA3)','data':'6'},{'value':'Spaeri (GEORGIA3)','data':'7'},{'value':'Aragvi Dusheti (GEORGIA3)','data':'5'},{'value':'FSV Mainz (GERMANY)','data':'15'},{'value':'Bochum (GERMANY)','data':'4'},{'value':'RB Leipzig (GERMANY)','data':'16'},{'value':'Union Berlin (GERMANY)','data':'5'},{'value':'Monchengladbach (GERMANY)','data':'1'},{'value':'FC Koln (GERMANY)','data':'17'},{'value':'Hoffenheim (GERMANY)','data':'10'},{'value':'Wolfsburg (GERMANY)','data':'3'},{'value':'Hertha Berlin (GERMANY)','data':'18'},{'value':'FC Augsburg (GERMANY)','data':'9'},{'value':'Stuttgart (GERMANY)','data':'7'},{'value':'Dortmund (GERMANY)','data':'13'},{'value':'Leverkusen (GERMANY)','data':'6'},{'value':'Bayern Munich (GERMANY)','data':'2'},{'value':'Greuther Furth (GERMANY)','data':'8'},{'value':'Freiburg (GERMANY)','data':'12'},{'value':'E. Frankfurt (GERMANY)','data':'14'},{'value':'Bielefeld (GERMANY)','data':'11'},{'value':'Bramfelder SV (GERMANY10)','data':'15'},{'value':'Sasel (GERMANY10)','data':'16'},{'value':'Hamm Utd (GERMANY10)','data':'17'},{'value':'Curslack-N. (GERMANY10)','data':'18'},{'value':'Hamburger SV C (GERMANY10)','data':'10'},{'value':'Rugenbergen (GERMANY10)','data':'19'},{'value':'W. Concordia (GERMANY10)','data':'3'},{'value':'Victoria H. B (GERMANY10)','data':'1'},{'value':'Lohbrugge (GERMANY10)','data':'12'},{'value':'Osdorf (GERMANY10)','data':'14'},{'value':'HEBC (GERMANY10)','data':'2'},{'value':'Meiendorfer SV (GERMANY10)','data':'4'},{'value':'Barmbek-U. (GERMANY10)','data':'5'},{'value':'Paloma (GERMANY10)','data':'6'},{'value':'Buchholz (GERMANY10)','data':'7'},{'value':'Süderelbe (GERMANY10)','data':'8'},{'value':'Niendorfer TSV (GERMANY10)','data':'9'},{'value':'Dassendorf (GERMANY10)','data':'11'},{'value':'Union Tornesch (GERMANY10)','data':'13'},{'value':'G. Ratingen (GERMANY11)','data':'20'},{'value':'Meerbusch (GERMANY11)','data':'14'},{'value':'TuRU Dusseldorf (GERMANY11)','data':'12'},{'value':'Niederwenigern (GERMANY11)','data':'9'},{'value':'Bocholt (GERMANY11)','data':'2'},{'value':'Union Nettetal (GERMANY11)','data':'15'},{'value':'SC Velbert (GERMANY11)','data':'11'},{'value':'SF Baumberg (GERMANY11)','data':'1'},{'value':'Jahn Dinslaken (GERMANY11)','data':'7'},{'value':'Sterkrade-Nord (GERMANY11)','data':'4'},{'value':'SW Essen (GERMANY11)','data':'6'},{'value':'Dusseldorf-West (GERMANY11)','data':'17'},{'value':'Kleve (GERMANY11)','data':'13'},{'value':'FSV Duisburg (GERMANY11)','data':'21'},{'value':'Kray (GERMANY11)','data':'8'},{'value':'Cronenberger SC (GERMANY11)','data':'3'},{'value':'TVD Velbert (GERMANY11)','data':'16'},{'value':'Cronenberger (GERMANY11)','data':'6'},{'value':'Monheim (GERMANY11)','data':'22'},{'value':'Hilden (GERMANY11)','data':'19'},{'value':'Teutonia St T. (GERMANY11)','data':'10'},{'value':'FC Mgladbach (GERMANY11)','data':'23'},{'value':'Schonnebeck (GERMANY11)','data':'5'},{'value':'SSVg Velbert (GERMANY11)','data':'18'},{'value':'Hammer SpVg (GERMANY12)','data':'12'},{'value':'Gütersloh (GERMANY12)','data':'13'},{'value':'Finnentrop / Ba (GERMANY12)','data':'14'},{'value':'Westfalia Herne (GERMANY12)','data':'15'},{'value':'Victoria Clarho (GERMANY12)','data':'16'},{'value':'Meinerzhagen (GERMANY12)','data':'11'},{'value':'Sportfreunde Si (GERMANY12)','data':'18'},{'value':'TuS Haltern (GERMANY12)','data':'19'},{'value':'Holzwickeder SC (GERMANY12)','data':'20'},{'value':'Preußen Münster (GERMANY12)','data':'2'},{'value':'Erndtebrück (GERMANY12)','data':'17'},{'value':'Eintracht Rhein (GERMANY12)','data':'6'},{'value':'Paderborn 07 II (GERMANY12)','data':'10'},{'value':'Schermbeck (GERMANY12)','data':'21'},{'value':'Westfalia Rhyne (GERMANY12)','data':'3'},{'value':'Vreden (GERMANY12)','data':'5'},{'value':'Kaan-Marienborn (GERMANY12)','data':'1'},{'value':'Ennepetal (GERMANY12)','data':'7'},{'value':'ASC Dortmund (GERMANY12)','data':'8'},{'value':'Sprockhövel (GERMANY12)','data':'9'},{'value':'Wattenscheid 09 (GERMANY12)','data':'4'},{'value':'Stern (GERMANY13)','data':'9'},{'value':'Pampow (GERMANY13)','data':'17'},{'value':'CFC Hertha (GERMANY13)','data':'8'},{'value':'Torgelower G. (GERMANY13)','data':'5'},{'value':'Hansa Rostock B (GERMANY13)','data':'7'},{'value':'Lok Stendal (GERMANY13)','data':'11'},{'value':'Neustrelitz (GERMANY13)','data':'6'},{'value':'H. Zehlendorf (GERMANY13)','data':'18'},{'value':'RSV Eintracht (GERMANY13)','data':'16'},{'value':'Mahlsdorf (GERMANY13)','data':'15'},{'value':'Rostocker FC (GERMANY13)','data':'13'},{'value':'Ludwigsfelder (GERMANY13)','data':'10'},{'value':'M. Schwerin (GERMANY13)','data':'12'},{'value':'Greifswald (GERMANY13)','data':'19'},{'value':'Blau W. Berlin (GERMANY13)','data':'4'},{'value':'Staaken (GERMANY13)','data':'3'},{'value':'Victoria Seelow (GERMANY13)','data':'2'},{'value':'MSV Neuruppin (GERMANY13)','data':'1'},{'value':'Brandenburger (GERMANY13)','data':'14'},{'value':'VfL Halle (GERMANY14)','data':'16'},{'value':'Bischofswerdaer (GERMANY14)','data':'2'},{'value':'Krieschow (GERMANY14)','data':'5'},{'value':'BW Zorbau (GERMANY14)','data':'8'},{'value':'An der Fahner (GERMANY14)','data':'4'},{'value':'FC Merseburg (GERMANY14)','data':'12'},{'value':'Grimma (GERMANY14)','data':'18'},{'value':'CZ Jena B (GERMANY14)','data':'7'},{'value':'VFC Plauen (GERMANY14)','data':'13'},{'value':'Martinroda (GERMANY14)','data':'6'},{'value':'FC Oberlausitz (GERMANY14)','data':'11'},{'value':'RW Erfurt (GERMANY14)','data':'17'},{'value':'E. Rudolstadt (GERMANY14)','data':'10'},{'value':'Nordhausen (GERMANY14)','data':'19'},{'value':'Sandersdorf (GERMANY14)','data':'14'},{'value':'Inter Leipzig (GERMANY14)','data':'9'},{'value':'Budissa Bautzen (GERMANY14)','data':'3'},{'value':'E. Wernigerode (GERMANY14)','data':'1'},{'value':'Arnstadt (GERMANY14)','data':'15'},{'value':'Viktoria G. (GERMANY15)','data':'5'},{'value':'Bad Vilbel (GERMANY15)','data':'12'},{'value':'Neuhof (GERMANY15)','data':'17'},{'value':'Fulda-Lehnerz (GERMANY15)','data':'3'},{'value':'RW Hadamar (GERMANY15)','data':'6'},{'value':'RW Walldorf (GERMANY15)','data':'20'},{'value':'Hunfelder SV (GERMANY15)','data':'14'},{'value':'Stadtallendorf (GERMANY15)','data':'22'},{'value':'B. Flieden (GERMANY15)','data':'4'},{'value':'Erlensee (GERMANY15)','data':'13'},{'value':'Bayern Alzenau (GERMANY15)','data':'9'},{'value':'Eddersheim (GERMANY15)','data':'2'},{'value':'Waldgirmes (GERMANY15)','data':'7'},{'value':'Zeilsheim (GERMANY15)','data':'1'},{'value':'Dietkirchen (GERMANY15)','data':'11'},{'value':'SV Steinbach (GERMANY15)','data':'15'},{'value':'KSV Baunatal (GERMANY15)','data':'16'},{'value':'Hessen Dreieich (GERMANY15)','data':'21'},{'value':'Fernwald (GERMANY15)','data':'18'},{'value':'Hanau (GERMANY15)','data':'10'},{'value':'Friedberg (GERMANY15)','data':'8'},{'value':'Ginsheim (GERMANY15)','data':'19'},{'value':'Fernwald (GERMANY15)','data':'18'},{'value':'Komet Arsten (GERMANY16)','data':'1'},{'value':'Habenhauser (GERMANY16)','data':'10'},{'value':'Hemelingen (GERMANY16)','data':'11'},{'value':'Blumenthaler (GERMANY16)','data':'4'},{'value':'Hastedt (GERMANY16)','data':'16'},{'value':'Schwachhausen (GERMANY16)','data':'9'},{'value':'SFL Bremerhaven (GERMANY16)','data':'17'},{'value':'Geestemunde (GERMANY16)','data':'18'},{'value':'Union Bremen (GERMANY16)','data':'13'},{'value':'Leher TS (GERMANY16)','data':'6'},{'value':'Brinkumer (GERMANY16)','data':'2'},{'value':'Aumund-Vegesack (GERMANY16)','data':'7'},{'value':'Werder Bremen C (GERMANY16)','data':'14'},{'value':'OSC Bremerhaven (GERMANY16)','data':'12'},{'value':'BTS Neustadt (GERMANY16)','data':'5'},{'value':'Bremer SV (GERMANY16)','data':'3'},{'value':'Vatan Sport (GERMANY16)','data':'8'},{'value':'Borgfeld (GERMANY16)','data':'15'},{'value':'Eichede (GERMANY18)','data':'2'},{'value':'D. Lubeck (GERMANY18)','data':'11'},{'value':'Frisia Risum-L. (GERMANY18)','data':'16'},{'value':'Flensburg (GERMANY18)','data':'4'},{'value':'Eckernforder (GERMANY18)','data':'17'},{'value':'Pansdorf (GERMANY18)','data':'1'},{'value':'Inter Turkspor (GERMANY18)','data':'6'},{'value':'P. Reinfel (GERMANY18)','data':'14'},{'value':'Husumer SV (GERMANY18)','data':'3'},{'value':'Todesfelde (GERMANY18)','data':'8'},{'value':'Lubeck B (GERMANY18)','data':'13'},{'value':'U. Neumünster (GERMANY18)','data':'7'},{'value':'Oldenburger (GERMANY18)','data':'15'},{'value':'Eutiner SV (GERMANY18)','data':'12'},{'value':'Bordesholm (GERMANY18)','data':'5'},{'value':'SC Weiche B (GERMANY18)','data':'3'},{'value':'Kronshagen (GERMANY18)','data':'9'},{'value':'Altenholz (GERMANY18)','data':'10'},{'value':'G.-Paffendorf (GERMANY19)','data':'12'},{'value':'Fortuna Köln B (GERMANY19)','data':'13'},{'value':'Eilendorf (GERMANY19)','data':'14'},{'value':'Bergisch G. (GERMANY19)','data':'6'},{'value':'VfL Vichttal (GERMANY19)','data':'11'},{'value':'Frechen (GERMANY19)','data':'17'},{'value':'Hennef (GERMANY19)','data':'5'},{'value':'Siegburger (GERMANY19)','data':'16'},{'value':'Freialdenhoven (GERMANY19)','data':'18'},{'value':'Breinig (GERMANY19)','data':'10'},{'value':'Pesch (GERMANY19)','data':'9'},{'value':'Deutz (GERMANY19)','data':'15'},{'value':'Alfter (GERMANY19)','data':'7'},{'value':'Friesdorf (GERMANY19)','data':'4'},{'value':'Hürth (GERMANY19)','data':'3'},{'value':'FC Viktoria (GERMANY19)','data':'2'},{'value':'Düren Merzenich (GERMANY19)','data':'1'},{'value':'Wesseling-Urfel (GERMANY19)','data':'8'},{'value':'Hansa Rostock (GERMANY2)','data':'9'},{'value':'FC Ingolstadt (GERMANY2)','data':'8'},{'value':'Karlsruher SC (GERMANY2)','data':'10'},{'value':'Schalke 04 (GERMANY2)','data':'1'},{'value':'Werder Bremen (GERMANY2)','data':'11'},{'value':'Hamburger SV (GERMANY2)','data':'2'},{'value':'Dusseldorf (GERMANY2)','data':'18'},{'value':'Regensburg (GERMANY2)','data':'4'},{'value':'Dynamo Dresden (GERMANY2)','data':'7'},{'value':'Hannover 96 (GERMANY2)','data':'12'},{'value':'Sankt Pauli (GERMANY2)','data':'13'},{'value':'Sandhausen (GERMANY2)','data':'17'},{'value':'Darmstadt (GERMANY2)','data':'3'},{'value':'Erzgebirge Aue (GERMANY2)','data':'16'},{'value':'Heidenheim (GERMANY2)','data':'5'},{'value':'Holstein Kiel (GERMANY2)','data':'14'},{'value':'Paderborn (GERMANY2)','data':'6'},{'value':'FC Nurnberg (GERMANY2)','data':'15'},{'value':'Kaiserslaut. B (GERMANY20)','data':'12'},{'value':'Mechtersheim (GERMANY20)','data':'1'},{'value':'Speyer (GERMANY20)','data':'2'},{'value':'Engers (GERMANY20)','data':'3'},{'value':'Koblenz (GERMANY20)','data':'4'},{'value':'Eintracht Trier (GERMANY20)','data':'5'},{'value':'Eisbachtal (GERMANY20)','data':'6'},{'value':'Elversberg B (GERMANY20)','data':'7'},{'value':'Jagersburg (GERMANY20)','data':'8'},{'value':'Waldalgesheim (GERMANY20)','data':'9'},{'value':'Diefflen (GERMANY20)','data':'20'},{'value':'Hassia Bingen (GERMANY20)','data':'11'},{'value':'Dudenhofen (GERMANY20)','data':'24'},{'value':'Wormatia Worms (GERMANY20)','data':'13'},{'value':'Hertha Wiesbach (GERMANY20)','data':'14'},{'value':'Eppelborn (GERMANY20)','data':'15'},{'value':'Pfeddersheim (GERMANY20)','data':'16'},{'value':'Emmelshausen (GERMANY20)','data':'17'},{'value':'Karbach (GERMANY20)','data':'18'},{'value':'A. Ludwigshafen (GERMANY20)','data':'19'},{'value':'Mülheim-Karlich (GERMANY20)','data':'21'},{'value':'Salmrohr (GERMANY20)','data':'22'},{'value':'Rochling (GERMANY20)','data':'23'},{'value':'Gonsenheim (GERMANY20)','data':'10'},{'value':'DJK Bamberg (GERMANY21)','data':'2'},{'value':'ATSV Erlangen (GERMANY21)','data':'12'},{'value':'Wurzburger FV (GERMANY21)','data':'4'},{'value':'Karlburg (GERMANY21)','data':'6'},{'value':'Ansbach (GERMANY21)','data':'7'},{'value':'Gebenbach (GERMANY21)','data':'8'},{'value':'Bayern Hof (GERMANY21)','data':'9'},{'value':'SC Feucht (GERMANY21)','data':'1'},{'value':'Cham (GERMANY21)','data':'11'},{'value':'Ammerthal (GERMANY21)','data':'3'},{'value':'Abtswind (GERMANY21)','data':'13'},{'value':'Vatan Spor (GERMANY21)','data':'14'},{'value':'Grossbardorf (GERMANY21)','data':'15'},{'value':'Vilzing (GERMANY21)','data':'16'},{'value':'Sand (GERMANY21)','data':'17'},{'value':'E. Bamberg (GERMANY21)','data':'18'},{'value':'Neumarkt (GERMANY21)','data':'10'},{'value':'Seligenporten (GERMANY21)','data':'5'},{'value':'Ismaning (GERMANY22)','data':'2'},{'value':'Pullach (GERMANY22)','data':'1'},{'value':'Landsberg (GERMANY22)','data':'3'},{'value':'J. Regensburg B (GERMANY22)','data':'4'},{'value':'Dachau (GERMANY22)','data':'5'},{'value':'Donaustauf (GERMANY22)','data':'6'},{'value':'Hankofen-H. (GERMANY22)','data':'7'},{'value':'Schwabmunchen (GERMANY22)','data':'8'},{'value':'Gundelfingen (GERMANY22)','data':'9'},{'value':'Ingolstadt B (GERMANY22)','data':'10'},{'value':'Hallbergmoos-G. (GERMANY22)','data':'11'},{'value':'1880 Wasserburg (GERMANY22)','data':'19'},{'value':'Garching (GERMANY22)','data':'13'},{'value':'Kirchanschoring (GERMANY22)','data':'14'},{'value':'1860 München B (GERMANY22)','data':'15'},{'value':'Schwaben A. (GERMANY22)','data':'16'},{'value':'Kottern (GERMANY22)','data':'17'},{'value':'Deisenhofen (GERMANY22)','data':'18'},{'value':'Turkspor Augsbu (GERMANY22)','data':'12'},{'value':'Leverkusen W (GERMANY23)','data':'12'},{'value':'E. Frankfurt W (GERMANY23)','data':'7'},{'value':'Werder Bremen W (GERMANY23)','data':'6'},{'value':'Duisburg W (GERMANY23)','data':'11'},{'value':'Meppen W (GERMANY23)','data':'12'},{'value':'Freiburg W (GERMANY23)','data':'10'},{'value':'Köln W (GERMANY23)','data':'4'},{'value':'Sand W (GERMANY23)','data':'8'},{'value':'Carl Zeiss Jena (GERMANY23)','data':'11'},{'value':'T. Potsdam W (GERMANY23)','data':'2'},{'value':'Bayern Munich W (GERMANY23)','data':'5'},{'value':'SGS Essen W (GERMANY23)','data':'3'},{'value':'Wolfsburg W (GERMANY23)','data':'1'},{'value':'Hoffenheim W (GERMANY23)','data':'9'},{'value':'1860 Munchen (GERMANY3)','data':'13'},{'value':'Saarbrücken (GERMANY3)','data':'6'},{'value':'Mannheim (GERMANY3)','data':'3'},{'value':'Viktoria Berlin (GERMANY3)','data':'15'},{'value':'Meppen (GERMANY3)','data':'10'},{'value':'MSV Duisburg (GERMANY3)','data':'2'},{'value':'Turkgucu M. (GERMANY3)','data':'18'},{'value':'Hallescher (GERMANY3)','data':'9'},{'value':'Wurzburger K. (GERMANY3)','data':'14'},{'value':'Viktoria Koln (GERMANY3)','data':'16'},{'value':'Dortmund B (GERMANY3)','data':'12'},{'value':'Verl (GERMANY3)','data':'17'},{'value':'Wehen Wiesbaden (GERMANY3)','data':'20'},{'value':'Zwickau (GERMANY3)','data':'11'},{'value':'Kaiserslautern (GERMANY3)','data':'7'},{'value':'Magdeburg (GERMANY3)','data':'4'},{'value':'Braunschweig (GERMANY3)','data':'8'},{'value':'Freiburg B (GERMANY3)','data':'19'},{'value':'Osnabruck (GERMANY3)','data':'1'},{'value':'Havelse (GERMANY3)','data':'5'},{'value':'St. Pauli B (GERMANY4)','data':'8'},{'value':'Heider SV (GERMANY4)','data':'18'},{'value':'Oldenburg (GERMANY4)','data':'1'},{'value':'HSC Hannover (GERMANY4)','data':'6'},{'value':'Drochtersen/A. (GERMANY4)','data':'14'},{'value':'Teutonia O. (GERMANY4)','data':'17'},{'value':'BSV Rehden (GERMANY4)','data':'5'},{'value':'Holstein Kiel B (GERMANY4)','data':'15'},{'value':'Hildesheim (GERMANY4)','data':'20'},{'value':'Wolfsburg B (GERMANY4)','data':'22'},{'value':'Werder Bremen B (GERMANY4)','data':'2'},{'value':'Oberneuland (GERMANY4)','data':'12'},{'value':'Phonix Lubeck (GERMANY4)','data':'4'},{'value':'Altona (GERMANY4)','data':'16'},{'value':'Hamburger SV B (GERMANY4)','data':'13'},{'value':'VfB Lubeck (GERMANY4)','data':'7'},{'value':'Jeddeloh (GERMANY4)','data':'9'},{'value':'Norderstedt (GERMANY4)','data':'3'},{'value':'Weiche F. (GERMANY4)','data':'21'},{'value':'Delmenhorst (GERMANY4)','data':'11'},{'value':'Hannover 96 B (GERMANY4)','data':'10'},{'value':'LSK Hansa (GERMANY4)','data':'19'},{'value':'Fuerstenwalde (GERMANY5)','data':'11'},{'value':'Luckenwalde (GERMANY5)','data':'18'},{'value':'Eilenburg (GERMANY5)','data':'19'},{'value':'Lichtenberg (GERMANY5)','data':'16'},{'value':'Lok. Leipzig (GERMANY5)','data':'13'},{'value':'TB Berlin (GERMANY5)','data':'2'},{'value':'Rathenow (GERMANY5)','data':'10'},{'value':'Tasmania Berlin (GERMANY5)','data':'5'},{'value':'Hertha Berlin B (GERMANY5)','data':'4'},{'value':'Auerbach (GERMANY5)','data':'12'},{'value':'Altglienicke (GERMANY5)','data':'9'},{'value':'Halberstadt (GERMANY5)','data':'3'},{'value':'Berliner AK (GERMANY5)','data':'7'},{'value':'Energie Cottbus (GERMANY5)','data':'17'},{'value':'Carl Zeiss Jena (GERMANY5)','data':'8'},{'value':'Chemie Leipzig (GERMANY5)','data':'20'},{'value':'BFC Dynamo (GERMANY5)','data':'14'},{'value':'Chemnitzer FC (GERMANY5)','data':'1'},{'value':'Meuselwitz (GERMANY5)','data':'15'},{'value':'Babelsberg (GERMANY5)','data':'6'},{'value':'Dusseldorf B (GERMANY6)','data':'9'},{'value':'KFC Uerdingen (GERMANY6)','data':'18'},{'value':'Wegberg-Beeck (GERMANY6)','data':'12'},{'value':'Schalke 04 B (GERMANY6)','data':'19'},{'value':'Oberhausen (GERMANY6)','data':'17'},{'value':'FC Koln B (GERMANY6)','data':'20'},{'value':'M`gladbach B (GERMANY6)','data':'8'},{'value':'Bonner SC (GERMANY6)','data':'3'},{'value':'Lotte (GERMANY6)','data':'10'},{'value':'Wiedenbruck (GERMANY6)','data':'2'},{'value':'Homberg (GERMANY6)','data':'7'},{'value':'RW Essen (GERMANY6)','data':'4'},{'value':'Lippstadt (GERMANY6)','data':'1'},{'value':'Rot Weiss Ahlen (GERMANY6)','data':'16'},{'value':'Wuppertaler (GERMANY6)','data':'13'},{'value':'Fortuna Koln (GERMANY6)','data':'11'},{'value':'Alemannia A. (GERMANY6)','data':'6'},{'value':'Preuss. Munster (GERMANY6)','data':'5'},{'value':'Rodinghausen (GERMANY6)','data':'14'},{'value':'Straelen (GERMANY6)','data':'15'},{'value':'Schott Mainz (GERMANY7)','data':'3'},{'value':'Homburg (GERMANY7)','data':'14'},{'value':'Bahlinger (GERMANY7)','data':'16'},{'value':'Kickers Offenb. (GERMANY7)','data':'13'},{'value':'FSV Mainz B (GERMANY7)','data':'5'},{'value':'Hoffenheim B (GERMANY7)','data':'17'},{'value':'Balingen (GERMANY7)','data':'4'},{'value':'Walldord (GERMANY7)','data':'7'},{'value':'Ulm (GERMANY7)','data':'1'},{'value':'Pirmasens (GERMANY7)','data':'15'},{'value':'Hessen Kassel (GERMANY7)','data':'9'},{'value':'VfB Stuttgart B (GERMANY7)','data':'12'},{'value':'Steinbach (GERMANY7)','data':'10'},{'value':'Aalen (GERMANY7)','data':'6'},{'value':'Giessen (GERMANY7)','data':'8'},{'value':'Elversberg (GERMANY7)','data':'19'},{'value':'Grossaspach (GERMANY7)','data':'18'},{'value':'FSV Frankfurt (GERMANY7)','data':'2'},{'value':'RW Koblenz (GERMANY7)','data':'11'},{'value':'Augsburg B (GERMANY8)','data':'18'},{'value':'Nürnberg B (GERMANY8)','data':'6'},{'value':'Pipinsried (GERMANY8)','data':'17'},{'value':'Eltersdorf (GERMANY8)','data':'14'},{'value':'Eichstätt (GERMANY8)','data':'19'},{'value':'Buchbach (GERMANY8)','data':'4'},{'value':'1860 Rosenheim (GERMANY8)','data':'11'},{'value':'Greuther F. B (GERMANY8)','data':'1'},{'value':'Aschaffenburg (GERMANY8)','data':'3'},{'value':'Rain / Lech (GERMANY8)','data':'16'},{'value':'Schweinfurt (GERMANY8)','data':'15'},{'value':'Bayern Munich B (GERMANY8)','data':'9'},{'value':'Schalding (GERMANY8)','data':'5'},{'value':'W. Burghausen (GERMANY8)','data':'8'},{'value':'Memmingen (GERMANY8)','data':'13'},{'value':'Bayreuth (GERMANY8)','data':'2'},{'value':'Aubstadt (GERMANY8)','data':'12'},{'value':'Unterhaching (GERMANY8)','data':'7'},{'value':'Heimstetten (GERMANY8)','data':'10'},{'value':'Illertissen (GERMANY8)','data':'20'},{'value':'Freiburger FC (GERMANY9)','data':'9'},{'value':'Linx (GERMANY9)','data':'18'},{'value':'Goppinger SV (GERMANY9)','data':'1'},{'value':'S. Kickers (GERMANY9)','data':'7'},{'value':'Ravensburg (GERMANY9)','data':'2'},{'value':'Bruchsal (GERMANY9)','data':'17'},{'value':'Backnang (GERMANY9)','data':'16'},{'value':'Lorrach-B. (GERMANY9)','data':'15'},{'value':'Ilshofen (GERMANY9)','data':'5'},{'value':'Freiberg (GERMANY9)','data':'12'},{'value':'Bissingen (GERMANY9)','data':'19'},{'value':'Reutlingen (GERMANY9)','data':'14'},{'value':'Villingen (GERMANY9)','data':'20'},{'value':'Rielasingen-A. (GERMANY9)','data':'6'},{'value':'Walldorf B (GERMANY9)','data':'8'},{'value':'Nottingen (GERMANY9)','data':'13'},{'value':'Oberachern (GERMANY9)','data':'11'},{'value':'Dorfmerkingen (GERMANY9)','data':'3'},{'value':'Pforzheim (GERMANY9)','data':'4'},{'value':'Sandhausen B (GERMANY9)','data':'16'},{'value':'Neckarsulmer (GERMANY9)','data':'10'},{'value':'Aduana Stars (GHANA)','data':'16'},{'value':'Bechem Utd (GHANA)','data':'7'},{'value':'Ashanti (GHANA)','data':'4'},{'value':'Dreams (GHANA)','data':'5'},{'value':'Real Tamale (GHANA)','data':'9'},{'value':'Eleven Wonders (GHANA)','data':'3'},{'value':'Asante Kotoko (GHANA)','data':'6'},{'value':'Elmina Sharks (GHANA)','data':'18'},{'value':'Ebusua (GHANA)','data':'9'},{'value':'Great Olympics (GHANA)','data':'10'},{'value':'Inter Allies (GHANA)','data':'15'},{'value':'Karela (GHANA)','data':'15'},{'value':'Liberty P. (GHANA)','data':'13'},{'value':'Hearts of Oak (GHANA)','data':'1'},{'value':'King Faisal (GHANA)','data':'13'},{'value':'WAFA (GHANA)','data':'14'},{'value':'Berekum Chelsea (GHANA)','data':'12'},{'value':'Legon Cities (GHANA)','data':'2'},{'value':'Accra Lions (GHANA)','data':'17'},{'value':'Bibiani GS (GHANA)','data':'11'},{'value':'Medeama (GHANA)','data':'8'},{'value':'Europa Point (GIBRALTAR)','data':'8'},{'value':'Europa FC (GIBRALTAR)','data':'10'},{'value':'Manchester 62 (GIBRALTAR)','data':'5'},{'value':'Mons Calpe (GIBRALTAR)','data':'1'},{'value':'Glacis Utd (GIBRALTAR)','data':'11'},{'value':'Lincoln RI (GIBRALTAR)','data':'9'},{'value':'College 1975 (GIBRALTAR)','data':'6'},{'value':'Lynx (GIBRALTAR)','data':'4'},{'value':'St Josephs (GIBRALTAR)','data':'3'},{'value':'Lions FC (GIBRALTAR)','data':'2'},{'value':'Boca Gibraltar (GIBRALTAR)','data':'8'},{'value':'Magpies (GIBRALTAR)','data':'7'},{'value':'Apollon Smirnis (GREECE)','data':'3'},{'value':'Aris (GREECE)','data':'10'},{'value':'PAOK (GREECE)','data':'6'},{'value':'Ionikos (GREECE)','data':'9'},{'value':'Lamia (GREECE)','data':'13'},{'value':'Panathinaikos (GREECE)','data':'2'},{'value':'PAS Giannina (GREECE)','data':'1'},{'value':'AEK Athens (GREECE)','data':'12'},{'value':'Asteras T. (GREECE)','data':'5'},{'value':'OFI Crete (GREECE)','data':'11'},{'value':'Panaitolikos (GREECE)','data':'8'},{'value':'Atromitos (GREECE)','data':'7'},{'value':'Volos (GREECE)','data':'4'},{'value':'Olympiakos (GREECE)','data':'14'},{'value':'Kallithea (GREECE2)','data':'19'},{'value':'Kalamata (GREECE2)','data':'32'},{'value':'Niki Volos (GREECE2)','data':'10'},{'value':'Apollon Pontou  (GREECE2)','data':'13'},{'value':'Thesprotos (GREECE2)','data':'16'},{'value':'Panserraikos (GREECE2)','data':'5'},{'value':'Veria (GREECE2)','data':'11'},{'value':'Olympiakos P. B (GREECE2)','data':'3'},{'value':'O. Volos (GREECE2)','data':'6'},{'value':'Kavala (GREECE2)','data':'14'},{'value':'Egaleo (GREECE2)','data':'21'},{'value':'OF Ierapetra (GREECE2)','data':'33'},{'value':'Chania (GREECE2)','data':'22'},{'value':'A. Vlachioti (GREECE2)','data':'26'},{'value':'Episkopi (GREECE2)','data':'27'},{'value':'Rodos (GREECE2)','data':'1'},{'value':'Trikala (GREECE2)','data':'8'},{'value':'Panachaiki (GREECE2)','data':'7'},{'value':'Almopos (GREECE2)','data':'12'},{'value':'Pierikos (GREECE2)','data':'17'},{'value':'Irodotos (GREECE2)','data':'23'},{'value':'Panathinaikos B (GREECE2)','data':'30'},{'value':'AEK Athens B (GREECE2)','data':'31'},{'value':'Xanthi (GREECE2)','data':'18'},{'value':'Doxa Dramas (GREECE2)','data':'6'},{'value':'Diagoras (GREECE2)','data':'24'},{'value':'Levadiakos (GREECE2)','data':'25'},{'value':'PAOK B (GREECE2)','data':'4'},{'value':'Apollon Larissa (GREECE2)','data':'7'},{'value':'Iraklis 1908 (GREECE2)','data':'9'},{'value':'Ergotelis (GREECE2)','data':'2'},{'value':'Kifisia (GREECE2)','data':'29'},{'value':'Zakynthos (GREECE2)','data':'20'},{'value':'Karaiskakis (GREECE2)','data':'28'},{'value':'AEL Larissa (GREECE2)','data':'34'},{'value':'A. Karditsa (GREECE2)','data':'15'},{'value':'Triglia (GREECE3)','data':'14'},{'value':'Ialysos (GREECE3)','data':'3'},{'value':'A. Enosis (GREECE3)','data':'20'},{'value':'Santorini (GREECE3)','data':'5'},{'value':'Kozani (GREECE3)','data':'10'},{'value':'N. Concepcion (GUATEMALA)','data':'11'},{'value':'Achuapa (GUATEMALA)','data':'12'},{'value':'Xelaju (GUATEMALA)','data':'7'},{'value':'Guastatoya (GUATEMALA)','data':'6'},{'value':'Municipal (GUATEMALA)','data':'5'},{'value':'Coban Imperial (GUATEMALA)','data':'8'},{'value':'Antigua GFC (GUATEMALA)','data':'4'},{'value':'Solola (GUATEMALA)','data':'9'},{'value':'Iztapa (GUATEMALA)','data':'3'},{'value':'Santa Lucia (GUATEMALA)','data':'2'},{'value':'Malacateco (GUATEMALA)','data':'1'},{'value':'Comunicaciones (GUATEMALA)','data':'10'},{'value':'Juventud P. (GUATEMALA3)','data':'11'},{'value':'Deportivo Reu (GUATEMALA3)','data':'15'},{'value':'Zacapa Tellioz (GUATEMALA3)','data':'14'},{'value':'D. Sanarate (GUATEMALA3)','data':'12'},{'value':'Chimaltenango (GUATEMALA3)','data':'20'},{'value':'Agua Blanca (GUATEMALA3)','data':'19'},{'value':'Marquense (GUATEMALA3)','data':'18'},{'value':'San Pedro (GUATEMALA3)','data':'17'},{'value':'Plataneros (GUATEMALA3)','data':'16'},{'value':'Comunicacion. B (GUATEMALA3)','data':'1'},{'value':'Mictlan (GUATEMALA3)','data':'13'},{'value':'Xinabajul (GUATEMALA3)','data':'10'},{'value':'Aurora (GUATEMALA3)','data':'3'},{'value':'Amatitlan (GUATEMALA3)','data':'5'},{'value':'Quiche (GUATEMALA3)','data':'6'},{'value':'Suchitepequez (GUATEMALA3)','data':'7'},{'value':'Mixco (GUATEMALA3)','data':'4'},{'value':'Siquinala (GUATEMALA3)','data':'8'},{'value':'Puerto San Jose (GUATEMALA3)','data':'9'},{'value':'Sacachispas (GUATEMALA3)','data':'2'},{'value':'Ouanaminthe (HAITI)','data':'4'},{'value':'Mirebalais (HAITI)','data':'5'},{'value':'Real du Cap (HAITI)','data':'6'},{'value':'Baltimore (HAITI)','data':'8'},{'value':'RC Haitien (HAITI)','data':'1'},{'value':'Racing Gonaives (HAITI)','data':'9'},{'value':'T. Liancourt (HAITI)','data':'10'},{'value':'Juventus (HAITI)','data':'12'},{'value':'Cosmopolites (HAITI)','data':'13'},{'value':'Don Bosco (HAITI)','data':'14'},{'value':'Capoise (HAITI)','data':'15'},{'value':'Violette AC (HAITI)','data':'16'},{'value':'Tempete (HAITI)','data':'17'},{'value':'FICA (HAITI)','data':'18'},{'value':'America Cayes (HAITI)','data':'7'},{'value':'Rivartibonit. (HAITI)','data':'11'},{'value':'Cavaly (HAITI)','data':'3'},{'value':'Arcahaie (HAITI)','data':'2'},{'value':'UPNFM (HONDURAS)','data':'4'},{'value':'Real Espana (HONDURAS)','data':'1'},{'value':'Victoria (HONDURAS)','data':'2'},{'value':'Vida (HONDURAS)','data':'3'},{'value':'H. Progreso (HONDURAS)','data':'9'},{'value':'Platense (HONDURAS)','data':'8'},{'value':'Real Sociedad (HONDURAS)','data':'5'},{'value':'Olimpia (HONDURAS)','data':'6'},{'value':'Motagua (HONDURAS)','data':'7'},{'value':'Marathon (HONDURAS)','data':'10'},{'value':'LM Warriors (HONGKONG)','data':'8'},{'value':'Pegasus (HONGKONG)','data':'3'},{'value':'Resources C. (HONGKONG)','data':'5'},{'value':'Eastern (HONGKONG)','data':'2'},{'value':'Hong Kong FC (HONGKONG)','data':'4'},{'value':'Southern D. (HONGKONG)','data':'3'},{'value':'HK Rangers (HONGKONG)','data':'6'},{'value':'Happy Valley (HONGKONG)','data':'6'},{'value':'HK U23 (HONGKONG)','data':'7'},{'value':'Kitchee (HONGKONG)','data':'1'},{'value':'Mezokovesd (HUNGARY)','data':'2'},{'value':'MOL Fehervar (HUNGARY)','data':'10'},{'value':'Puskas Akad. (HUNGARY)','data':'12'},{'value':'Ujpest (HUNGARY)','data':'11'},{'value':'Kisvarda (HUNGARY)','data':'6'},{'value':'Gyirmot (HUNGARY)','data':'3'},{'value':'Zalaegerszegi (HUNGARY)','data':'9'},{'value':'Paks (HUNGARY)','data':'1'},{'value':'Ferencvaros (HUNGARY)','data':'5'},{'value':'MTK (HUNGARY)','data':'4'},{'value':'Debrecen (HUNGARY)','data':'8'},{'value':'Honved (HUNGARY)','data':'7'},{'value':'Szeged (HUNGARY2)','data':'8'},{'value':'Soroksar (HUNGARY2)','data':'16'},{'value':'Budaors (HUNGARY2)','data':'14'},{'value':'Ajka (HUNGARY2)','data':'18'},{'value':'Gyori ETO (HUNGARY2)','data':'9'},{'value':'Pecsi MFC (HUNGARY2)','data':'19'},{'value':'Dorogi (HUNGARY2)','data':'4'},{'value':'III. Keruleti (HUNGARY2)','data':'1'},{'value':'Budafoki (HUNGARY2)','data':'2'},{'value':'Diosgyor VTK (HUNGARY2)','data':'6'},{'value':'Kecskemeti TE (HUNGARY2)','data':'13'},{'value':'Szentlorinc (HUNGARY2)','data':'12'},{'value':'Vasas (HUNGARY2)','data':'17'},{'value':'Siofok (HUNGARY2)','data':'15'},{'value':'Bekescsaba (HUNGARY2)','data':'7'},{'value':'Szolnoki MAV (HUNGARY2)','data':'11'},{'value':'Tiszakecske (HUNGARY2)','data':'10'},{'value':'Haladas (HUNGARY2)','data':'20'},{'value':'Csakvari (HUNGARY2)','data':'5'},{'value':'Nyiregyhaza (HUNGARY2)','data':'3'},{'value':'Tiszafured (HUNGARY3)','data':'6'},{'value':'Putnok VSE (HUNGARY3)','data':'19'},{'value':'Hatvan (HUNGARY3)','data':'10'},{'value':'Kisvarda B (HUNGARY3)','data':'11'},{'value':'Fuzesgyarmati (HUNGARY3)','data':'2'},{'value':'Sajobabony (HUNGARY3)','data':'13'},{'value':'Gyongyos (HUNGARY3)','data':'14'},{'value':'Tiszaujvaros (HUNGARY3)','data':'9'},{'value':'Jaszberenyi (HUNGARY3)','data':'17'},{'value':'BKV Elore (HUNGARY3)','data':'13'},{'value':'Senyo Carnifex (HUNGARY3)','data':'12'},{'value':'Bekescsaba B (HUNGARY3)','data':'1'},{'value':'Hajduszoboszloi (HUNGARY3)','data':'7'},{'value':'Torokszen. (HUNGARY3)','data':'18'},{'value':'Hidasnemeti (HUNGARY3)','data':'20'},{'value':'Eger (HUNGARY3)','data':'3'},{'value':'Diosgyor B (HUNGARY3)','data':'16'},{'value':'Debreceni EAC (HUNGARY3)','data':'15'},{'value':'Ujpest B (HUNGARY3)','data':'10'},{'value':'Debrecen B (HUNGARY3)','data':'8'},{'value':'Kazincbarcika (HUNGARY3)','data':'5'},{'value':'Mezokovesd B (HUNGARY3)','data':'18'},{'value':'Tallya (HUNGARY3)','data':'4'},{'value':'Salgotarjan BTC (HUNGARY3)','data':'14'},{'value':'Ferencvaros B (HUNGARY4)','data':'1'},{'value':'Mako (HUNGARY4)','data':'3'},{'value':'Gerjeni (HUNGARY4)','data':'5'},{'value':'Ivancsa (HUNGARY4)','data':'2'},{'value':'Mohacs (HUNGARY4)','data':'17'},{'value':'MTK Budapest B (HUNGARY4)','data':'19'},{'value':'Mohacsi TE (HUNGARY4)','data':'15'},{'value':'Balassagyarmat  (HUNGARY4)','data':'20'},{'value':'Honved B (HUNGARY4)','data':'18'},{'value':'Dunaujvaros-P. (HUNGARY4)','data':'11'},{'value':'Kozarmisleny (HUNGARY4)','data':'16'},{'value':'Paksi B (HUNGARY4)','data':'6'},{'value':'Cegledi (HUNGARY4)','data':'13'},{'value':'Dabas (HUNGARY4)','data':'9'},{'value':'Taksony (HUNGARY4)','data':'7'},{'value':'Rakosment (HUNGARY4)','data':'10'},{'value':'Vac (HUNGARY4)','data':'17'},{'value':'ESMTK (HUNGARY4)','data':'7'},{'value':'Hodmezovasarh. (HUNGARY4)','data':'14'},{'value':'Szekszard (HUNGARY4)','data':'12'},{'value':'Monori SE (HUNGARY4)','data':'4'},{'value':'Dabas-Gyon (HUNGARY4)','data':'8'},{'value':'Majosi (HUNGARY4)','data':'10'},{'value':'Korosladany (HUNGARY4)','data':'9'},{'value':'Szegedi VSE (HUNGARY4)','data':'18'},{'value':'Menfocsanak (HUNGARY5)','data':'16'},{'value':'Sopron (HUNGARY5)','data':'18'},{'value':'Bicskei (HUNGARY5)','data':'6'},{'value':'Puskas Ak. B (HUNGARY5)','data':'2'},{'value':'MTE (HUNGARY5)','data':'20'},{'value':'Tatabanya (HUNGARY5)','data':'15'},{'value':'Komarom (HUNGARY5)','data':'4'},{'value':'Papai Perutz (HUNGARY5)','data':'17'},{'value':'Nagykanizsa (HUNGARY5)','data':'7'},{'value':'Nagyatad (HUNGARY5)','data':'11'},{'value':'MOL Fehervar B (HUNGARY5)','data':'1'},{'value':'Veszprem (HUNGARY5)','data':'3'},{'value':'Gardony (HUNGARY5)','data':'10'},{'value':'Erd (HUNGARY5)','data':'5'},{'value':'Balatonfuredi (HUNGARY5)','data':'13'},{'value':'Zalaegerszeg B (HUNGARY5)','data':'8'},{'value':'Lipot (HUNGARY5)','data':'19'},{'value':'Gyori B (HUNGARY5)','data':'16'},{'value':'Kelen (HUNGARY5)','data':'14'},{'value':'Gyirmot B (HUNGARY5)','data':'12'},{'value':'Andráshida (HUNGARY5)','data':'11'},{'value':'Szabadkikoto (HUNGARY5)','data':'20'},{'value':'Kaposvar (HUNGARY5)','data':'19'},{'value':'BVSC (HUNGARY5)','data':'9'},{'value':'Hafnarfjordur (ICELAND)','data':'8'},{'value':'Stjarnan (ICELAND)','data':'3'},{'value':'IA Akranes (ICELAND)','data':'2'},{'value':'KR Reykjavik (ICELAND)','data':'12'},{'value':'Valur (ICELAND)','data':'1'},{'value':'Breidablik (ICELAND)','data':'11'},{'value':'HK Kopavogur (ICELAND)','data':'9'},{'value':'Fylkir (ICELAND)','data':'7'},{'value':'Keflavik (ICELAND)','data':'6'},{'value':'Vikingur R. (ICELAND)','data':'5'},{'value':'Leiknir R. (ICELAND)','data':'4'},{'value':'KA Akureyri (ICELAND)','data':'10'},{'value':'IBV (ICELAND2)','data':'8'},{'value':'V. Olafsvik (ICELAND2)','data':'4'},{'value':'Grotta (ICELAND2)','data':'5'},{'value':'Fram (ICELAND2)','data':'3'},{'value':'Thor Akureyri (ICELAND2)','data':'6'},{'value':'Fjolnir (ICELAND2)','data':'2'},{'value':'Grindavík (ICELAND2)','data':'7'},{'value':'Kordrengir (ICELAND2)','data':'10'},{'value':'Vestri (ICELAND2)','data':'12'},{'value':'Throttur R. (ICELAND2)','data':'1'},{'value':'Afturelding (ICELAND2)','data':'9'},{'value':'Selfoss (ICELAND2)','data':'11'},{'value':'Kari (ICELAND3)','data':'5'},{'value':'Njardvík (ICELAND3)','data':'1'},{'value':'Magni (ICELAND3)','data':'12'},{'value':'KV Reykjavik (ICELAND3)','data':'11'},{'value':'Volsungur (ICELAND3)','data':'10'},{'value':'Fjardabyggd (ICELAND3)','data':'9'},{'value':'Leiknir F. (ICELAND3)','data':'8'},{'value':'KF Fjallab. (ICELAND3)','data':'6'},{'value':'Throttur Vogar (ICELAND3)','data':'2'},{'value':'Haukar (ICELAND3)','data':'3'},{'value':'Reynir (ICELAND3)','data':'4'},{'value':'IR Reykjavik (ICELAND3)','data':'7'},{'value':'Dalvik / Reynir (ICELAND4)','data':'1'},{'value':'Aegir (ICELAND4)','data':'4'},{'value':'Hottur / Huginn (ICELAND4)','data':'5'},{'value':'Sindri (ICELAND4)','data':'6'},{'value':'KFS (ICELAND4)','data':'7'},{'value':'Einherji (ICELAND4)','data':'8'},{'value':'Ellidi (ICELAND4)','data':'3'},{'value':'Augnablik (ICELAND4)','data':'9'},{'value':'Hafnarjordur (ICELAND4)','data':'10'},{'value':'KFG Gardabar (ICELAND4)','data':'11'},{'value':'Tindastoll (ICELAND4)','data':'12'},{'value':'Vidir (ICELAND4)','data':'2'},{'value':'Valur R. W (ICELAND5)','data':'9'},{'value':'Breidablik W (ICELAND5)','data':'3'},{'value':'Fylkir W (ICELAND5)','data':'4'},{'value':'Tindastoll W (ICELAND5)','data':'5'},{'value':'Throttur R. W (ICELAND5)','data':'6'},{'value':'Keflavík W (ICELAND5)','data':'7'},{'value':'Selfoss W (ICELAND5)','data':'8'},{'value':'IBV W (ICELAND5)','data':'1'},{'value':'Stjarnan W (ICELAND5)','data':'10'},{'value':'Thor Akureyri W (ICELAND5)','data':'2'},{'value':'Mumbai City (INDIA)','data':'7'},{'value':'Kerala Blasters (INDIA)','data':'2'},{'value':'Goa (INDIA)','data':'8'},{'value':'Bengaluru (INDIA)','data':'3'},{'value':'Odisha FC (INDIA)','data':'11'},{'value':'Hyderabad (INDIA)','data':'9'},{'value':'Jamshedpur (INDIA)','data':'6'},{'value':'Chennaiyin (INDIA)','data':'10'},{'value':'East Bengal (INDIA)','data':'5'},{'value':'NorthEast Utd (INDIA)','data':'4'},{'value':'ATK Mohun Bagan (INDIA)','data':'1'},{'value':'TRAU (INDIA2)','data':'8'},{'value':'Aizawl (INDIA2)','data':'4'},{'value':'Punjab (INDIA2)','data':'3'},{'value':'Mohammedan (INDIA2)','data':'2'},{'value':'Sudeva (INDIA2)','data':'1'},{'value':'Neroca (INDIA2)','data':'11'},{'value':'Churchill B. (INDIA2)','data':'10'},{'value':'Gokulam (INDIA2)','data':'5'},{'value':'Real Kashmir (INDIA2)','data':'7'},{'value':'Indian Arrows (INDIA2)','data':'9'},{'value':'Chennai City (INDIA2)','data':'6'},{'value':'PSM (INDONESIA)','data':'11'},{'value':'Borneo (INDONESIA)','data':'13'},{'value':'Persita (INDONESIA)','data':'18'},{'value':'Persipura (INDONESIA)','data':'17'},{'value':'Persik Kediri (INDONESIA)','data':'16'},{'value':'Bhayangkara S. (INDONESIA)','data':'9'},{'value':'Persebaya S. (INDONESIA)','data':'14'},{'value':'Arema (INDONESIA)','data':'12'},{'value':'Persiraja (INDONESIA)','data':'10'},{'value':'Madura Utd (INDONESIA)','data':'8'},{'value':'TIRA Persikabo (INDONESIA)','data':'7'},{'value':'Barito Putera (INDONESIA)','data':'6'},{'value':'Persib (INDONESIA)','data':'5'},{'value':'PSIS Semarang (INDONESIA)','data':'3'},{'value':'Persija (INDONESIA)','data':'2'},{'value':'PSS Sleman (INDONESIA)','data':'1'},{'value':'Persela L. (INDONESIA)','data':'4'},{'value':'Bali Utd (INDONESIA)','data':'15'},{'value':'Sepahan (IRAN)','data':'7'},{'value':'Aluminium Arak (IRAN)','data':'4'},{'value':'N. Mazandaran (IRAN)','data':'1'},{'value':'Tractor Sazi (IRAN)','data':'10'},{'value':'Naft Masjed S. (IRAN)','data':'6'},{'value':'Gol Gohar (IRAN)','data':'9'},{'value':'Zob Ahan (IRAN)','data':'12'},{'value':'Esteghlal (IRAN)','data':'13'},{'value':'Mes Rafsanjan (IRAN)','data':'8'},{'value':'Sanat Naft (IRAN)','data':'11'},{'value':'Shahr Khodrou (IRAN)','data':'3'},{'value':'Persepolis (IRAN)','data':'16'},{'value':'Foolad (IRAN)','data':'15'},{'value':'Paykan (IRAN)','data':'5'},{'value':'Havadar (IRAN)','data':'14'},{'value':'Fajr Sepasi (IRAN)','data':'2'},{'value':'Gol Reyhan (IRAN2)','data':'5'},{'value':'Pars Jam (IRAN2)','data':'2'},{'value':'Arman Gohar (IRAN2)','data':'4'},{'value':'Machine Sazi (IRAN2)','data':'11'},{'value':'E. Mollasani (IRAN2)','data':'15'},{'value':'Rayka Babol (IRAN2)','data':'16'},{'value':'K. Khorramabad (IRAN2)','data':'7'},{'value':'Saipa (IRAN2)','data':'5'},{'value':'S. Astara (IRAN2)','data':'8'},{'value':'Mes Shahr Babak (IRAN2)','data':'1'},{'value':'S. Hamedan (IRAN2)','data':'12'},{'value':'Vista Turbin (IRAN2)','data':'14'},{'value':'Baderan (IRAN2)','data':'9'},{'value':'E. Khuzestan (IRAN2)','data':'6'},{'value':'K. Khorramabad (IRAN2)','data':'15'},{'value':'Shahin Bushehr (IRAN2)','data':'17'},{'value':'Khooshe Talaee  (IRAN2)','data':'13'},{'value':'Qashqai (IRAN2)','data':'18'},{'value':'Malavan (IRAN2)','data':'3'},{'value':'Navad Urmia (IRAN2)','data':'8'},{'value':'Mes Kerman (IRAN2)','data':'10'},{'value':'Shams A. Qazvin (IRAN2)','data':'9'},{'value':'Chooka Talesh (IRAN2)','data':'16'},{'value':'Naft Al-Wasat (IRAQ)','data':'13'},{'value':'Al Sinaah (IRAQ)','data':'18'},{'value':'Al Najaf (IRAQ)','data':'19'},{'value':'Al Hudod (IRAQ)','data':'6'},{'value':'Al Diwaniya (IRAQ)','data':'20'},{'value':'Al Simawa (IRAQ)','data':'8'},{'value':'Al Zawraa (IRAQ)','data':'17'},{'value':'Al Quwa Al J. (IRAQ)','data':'9'},{'value':'Al Kahrabaa (IRAQ)','data':'12'},{'value':'Al Naft (IRAQ)','data':'1'},{'value':'A. Alkahrabaiya (IRAQ)','data':'12'},{'value':'Baghdad (IRAQ)','data':'11'},{'value':'Samaraa (IRAQ)','data':'14'},{'value':'Erbil (IRAQ)','data':'16'},{'value':'Al Talaba (IRAQ)','data':'8'},{'value':'Naft Al-Janoob (IRAQ)','data':'4'},{'value':'Zakho (IRAQ)','data':'5'},{'value':'Al Karkh (IRAQ)','data':'3'},{'value':'Al-Qasim (IRAQ)','data':'10'},{'value':'Naft Maysan (IRAQ)','data':'2'},{'value':'Newroz SC (IRAQ)','data':'6'},{'value':'Al Shorta (IRAQ)','data':'7'},{'value':'Al Minaa Basra (IRAQ)','data':'15'},{'value':'Finn Harps (IRELAND)','data':'3'},{'value':'Waterford (IRELAND)','data':'2'},{'value':'Drogheda Utd (IRELAND)','data':'1'},{'value':'Shamrock Rovers (IRELAND)','data':'5'},{'value':'St. Patricks (IRELAND)','data':'6'},{'value':'Longford Town (IRELAND)','data':'7'},{'value':'Bohemians (IRELAND)','data':'4'},{'value':'Sligo Rovers (IRELAND)','data':'9'},{'value':'Dundalk (IRELAND)','data':'10'},{'value':'Derry City (IRELAND)','data':'8'},{'value':'Treaty Utd (IRELAND2)','data':'2'},{'value':'Cork City (IRELAND2)','data':'5'},{'value':'Wexford (IRELAND2)','data':'9'},{'value':'Cobh Ramblers (IRELAND2)','data':'6'},{'value':'UC Dublin (IRELAND2)','data':'7'},{'value':'Athlone Town (IRELAND2)','data':'8'},{'value':'Bray Wanderers (IRELAND2)','data':'1'},{'value':'Cabinteely (IRELAND2)','data':'10'},{'value':'Galway Utd (IRELAND2)','data':'3'},{'value':'Shelbourne (IRELAND2)','data':'4'},{'value':'Cork City W (IRELAND3)','data':'2'},{'value':'Peamount Utd W (IRELAND3)','data':'8'},{'value':'Bohemians W (IRELAND3)','data':'3'},{'value':'Wexford Y. W (IRELAND3)','data':'7'},{'value':'Athlone W (IRELAND3)','data':'6'},{'value':'Galway W (IRELAND3)','data':'1'},{'value':'Shelbourne W (IRELAND3)','data':'5'},{'value':'Treaty Utd W (IRELAND3)','data':'4'},{'value':'DLR Waves W (IRELAND3)','data':'9'},{'value':'H. Beer Sheva (ISRAEL)','data':'12'},{'value':'M. Petah Tikva (ISRAEL)','data':'3'},{'value':'Bnei Sakhnin (ISRAEL)','data':'7'},{'value':'Hapoel Tel Aviv (ISRAEL)','data':'5'},{'value':'Maccabi Netanya (ISRAEL)','data':'2'},{'value':'Hapoel Haifa (ISRAEL)','data':'1'},{'value':'B. Jerusalem (ISRAEL)','data':'11'},{'value':'Hapoel Hadera (ISRAEL)','data':'9'},{'value':'H. Nof Hagalil (ISRAEL)','data':'13'},{'value':'M. Tel Aviv (ISRAEL)','data':'8'},{'value':'Ashdod (ISRAEL)','data':'6'},{'value':'H. Jerusalem (ISRAEL)','data':'14'},{'value':'Maccabi Haifa (ISRAEL)','data':'10'},{'value':'Ironi Kiryat (ISRAEL)','data':'4'},{'value':'H. Kfar Shalem (ISRAEL2)','data':'16'},{'value':'Hapoel Raanana (ISRAEL2)','data':'2'},{'value':'Ramat Hasharon (ISRAEL2)','data':'3'},{'value':'H. Umm al-Fahm (ISRAEL2)','data':'1'},{'value':'M. A. Nazareth (ISRAEL2)','data':'13'},{'value':'Nes Tziona (ISRAEL2)','data':'12'},{'value':'A. Sport Ashdod (ISRAEL2)','data':'4'},{'value':'M. Bnei Raina (ISRAEL2)','data':'8'},{'value':'H. Ramat Gan (ISRAEL2)','data':'7'},{'value':'H. Ironi Rishon (ISRAEL2)','data':'10'},{'value':'H. Petah Tikva (ISRAEL2)','data':'5'},{'value':'Hapoel Akko (ISRAEL2)','data':'15'},{'value':'Bnei Yehuda (ISRAEL2)','data':'6'},{'value':'Hapoel Iksal (ISRAEL2)','data':'3'},{'value':'Kafr Qasim (ISRAEL2)','data':'11'},{'value':'Hapoel Afula (ISRAEL2)','data':'14'},{'value':'H. Kfar Saba (ISRAEL2)','data':'16'},{'value':'Beitar Tel Aviv (ISRAEL2)','data':'9'},{'value':'Bologna (ITALY)','data':'9'},{'value':'Sampdoria (ITALY)','data':'19'},{'value':'Juventus (ITALY)','data':'12'},{'value':'Cagliari (ITALY)','data':'17'},{'value':'Lazio (ITALY)','data':'6'},{'value':'AS Roma (ITALY)','data':'15'},{'value':'Sassuolo (ITALY)','data':'2'},{'value':'Genoa (ITALY)','data':'4'},{'value':'Napoli (ITALY)','data':'13'},{'value':'Fiorentina (ITALY)','data':'16'},{'value':'Torino (ITALY)','data':'7'},{'value':'Hellas Verona (ITALY)','data':'1'},{'value':'Atalanta (ITALY)','data':'8'},{'value':'Inter Milan (ITALY)','data':'3'},{'value':'Spezia (ITALY)','data':'18'},{'value':'Udinese (ITALY)','data':'11'},{'value':'Empoli (ITALY)','data':'5'},{'value':'AC Milan (ITALY)','data':'20'},{'value':'Venezia (ITALY)','data':'14'},{'value':'Salernitana (ITALY)','data':'10'},{'value':'Sinalunghese (ITALY10)','data':'13'},{'value':'Foligno (ITALY10)','data':'3'},{'value':'Sangiovannese (ITALY10)','data':'15'},{'value':'Gavorrano (ITALY10)','data':'5'},{'value':'Pianese (ITALY10)','data':'7'},{'value':'San Donato (ITALY10)','data':'13'},{'value':'Cannara (ITALY10)','data':'10'},{'value':'ACN Siena (ITALY10)','data':'11'},{'value':'Scandicci (ITALY10)','data':'8'},{'value':'Flaminia (ITALY10)','data':'12'},{'value':'S. Trestina (ITALY10)','data':'2'},{'value':'Rieti (ITALY10)','data':'16'},{'value':'Montespaccato (ITALY10)','data':'4'},{'value':'Grassina (ITALY10)','data':'18'},{'value':'Lornano Badesse (ITALY10)','data':'18'},{'value':'Unipomezia (ITALY10)','data':'14'},{'value':'Pro Livorno (ITALY10)','data':'11'},{'value':'Tiferno Lerchi (ITALY10)','data':'17'},{'value':'Cascina (ITALY10)','data':'6'},{'value':'Arezzo (ITALY10)','data':'1'},{'value':'Poggibonsi (ITALY10)','data':'9'},{'value':'A. Terme Fiuggi (ITALY11)','data':'3'},{'value':'Trastevere (ITALY11)','data':'17'},{'value':'Vastese (ITALY11)','data':'2'},{'value':'Alto Casertano (ITALY11)','data':'5'},{'value':'Nereto (ITALY11)','data':'7'},{'value':'Pineto (ITALY11)','data':'9'},{'value':'Castelnuovo V. (ITALY11)','data':'10'},{'value':'Porto D` Ascoli (ITALY11)','data':'11'},{'value':'Castelfidardo (ITALY11)','data':'16'},{'value':'Sambenedettese (ITALY11)','data':'18'},{'value':'Chieti (ITALY11)','data':'8'},{'value':'Fano (ITALY11)','data':'1'},{'value':'Tolentino (ITALY11)','data':'14'},{'value':'P. Sant Elpidio (ITALY11)','data':'3'},{'value':'Recanatese (ITALY11)','data':'13'},{'value':'Vastogirardi (ITALY11)','data':'15'},{'value':'Giulianova (ITALY11)','data':'13'},{'value':'San Nicolo (ITALY11)','data':'4'},{'value':'O. Agnonese (ITALY11)','data':'9'},{'value':'Matese (ITALY11)','data':'12'},{'value':'Montegiorgio (ITALY11)','data':'6'},{'value':'Gladiator (ITALY12)','data':'7'},{'value':'Insieme Formia (ITALY12)','data':'14'},{'value':'Cassino (ITALY12)','data':'5'},{'value':'Vis Artena (ITALY12)','data':'17'},{'value':'Giugliano (ITALY12)','data':'16'},{'value':'Afragolese (ITALY12)','data':'18'},{'value':'Muravera (ITALY12)','data':'9'},{'value':'Real Monteroton (ITALY12)','data':'6'},{'value':'Nuova Florida (ITALY12)','data':'13'},{'value':'CynthiAlbalonga (ITALY12)','data':'12'},{'value':'Atletico Uri (ITALY12)','data':'10'},{'value':'Arzachena (ITALY12)','data':'1'},{'value':'Lanusei (ITALY12)','data':'2'},{'value':'Aprilia (ITALY12)','data':'8'},{'value':'Ostia Mare (ITALY12)','data':'11'},{'value':'Latte Dolce (ITALY12)','data':'4'},{'value':'Carbonia (ITALY12)','data':'3'},{'value':'Gladiator (ITALY12)','data':'6'},{'value':'Savoia (ITALY12)','data':'8'},{'value':'Muravera (ITALY12)','data':'9'},{'value':'Sassari Torres (ITALY12)','data':'15'},{'value':'Nardo (ITALY13)','data':'15'},{'value':'Bitonto (ITALY13)','data':'5'},{'value':'Bisceglie (ITALY13)','data':'3'},{'value':'Gravina (ITALY13)','data':'11'},{'value':'Francavilla (ITALY13)','data':'9'},{'value':'Puteolana (ITALY13)','data':'13'},{'value':'Molfetta Calcio (ITALY13)','data':'14'},{'value':'Sorrento (ITALY13)','data':'18'},{'value':'Brindisi (ITALY13)','data':'10'},{'value':'Brindisi (ITALY13)','data':'7'},{'value':'Mariglianese (ITALY13)','data':'17'},{'value':'Lavello (ITALY13)','data':'13'},{'value':'Citta di Fasano (ITALY13)','data':'2'},{'value':'Altamura (ITALY13)','data':'16'},{'value':'Casarano (ITALY13)','data':'12'},{'value':'A. Cerignola (ITALY13)','data':'1'},{'value':'Rotonda (ITALY13)','data':'6'},{'value':'Nocerina (ITALY13)','data':'4'},{'value':'San Giorgio (ITALY13)','data':'20'},{'value':'Nola (ITALY13)','data':'8'},{'value':'Virtus Matino (ITALY13)','data':'19'},{'value':'Casertana (ITALY13)','data':'7'},{'value':'Giarre (ITALY14)','data':'16'},{'value':'Castrovillari (ITALY14)','data':'10'},{'value':'Dattilo (ITALY14)','data':'6'},{'value':'Acireale (ITALY14)','data':'3'},{'value':'Rende (ITALY14)','data':'2'},{'value':'Lamezia Terme (ITALY14)','data':'7'},{'value':'Sancataldese (ITALY14)','data':'14'},{'value':'Roccella (ITALY14)','data':'15'},{'value':'Paterno (ITALY14)','data':'13'},{'value':'Troina (ITALY14)','data':'8'},{'value':'Licata (ITALY14)','data':'11'},{'value':'Cittanovese (ITALY14)','data':'3'},{'value':'Biancavilla (ITALY14)','data':'20'},{'value':'Cavese (ITALY14)','data':'1'},{'value':'FC Messina (ITALY14)','data':'12'},{'value':'San Luca (ITALY14)','data':'19'},{'value':'Gelbison (ITALY14)','data':'9'},{'value':'Portici (ITALY14)','data':'15'},{'value':'Santa Maria C. (ITALY14)','data':'18'},{'value':'Real Aversa (ITALY14)','data':'17'},{'value':'Marina Ragusa (ITALY14)','data':'13'},{'value':'Licata (ITALY14)','data':'14'},{'value':'Trapani (ITALY14)','data':'6'},{'value':'Cittanova Inter (ITALY14)','data':'4'},{'value':'CD S. Agata (ITALY14)','data':'5'},{'value':'Inter U19 (ITALY15)','data':'15'},{'value':'Juventus U19 (ITALY15)','data':'12'},{'value':'Verona U19 (ITALY15)','data':'9'},{'value':'Pescara U19 (ITALY15)','data':'8'},{'value':'Empoli U19 (ITALY15)','data':'10'},{'value':'Genoa U19 (ITALY15)','data':'7'},{'value':'Napoli U19 (ITALY15)','data':'6'},{'value':'Atalanta U19 (ITALY15)','data':'16'},{'value':'Torino U19 (ITALY15)','data':'13'},{'value':'Fiorentina U19 (ITALY15)','data':'11'},{'value':'Bologna U19 (ITALY15)','data':'5'},{'value':'Lecce U19 (ITALY15)','data':'18'},{'value':'Cagliari U19 (ITALY15)','data':'17'},{'value':'Milan U19 (ITALY15)','data':'4'},{'value':'Sassuolo U19 (ITALY15)','data':'3'},{'value':'Spal U19 (ITALY15)','data':'1'},{'value':'Sampdoria U19 (ITALY15)','data':'2'},{'value':'Roma U19 (ITALY15)','data':'14'},{'value':'Ascoli U19 (ITALY16)','data':'6'},{'value':'Pisa U19 (ITALY16)','data':'22'},{'value':'Crotone U19 (ITALY16)','data':'23'},{'value':'Cosenza U19 (ITALY16)','data':'26'},{'value':'Udinese U19 (ITALY16)','data':'25'},{'value':'Alessandria U19 (ITALY16)','data':'12'},{'value':'Salernitana U19 (ITALY16)','data':'5'},{'value':'Reggina U19 (ITALY16)','data':'4'},{'value':'Frosinone U19 (ITALY16)','data':'3'},{'value':'Cesena U19 (ITALY16)','data':'2'},{'value':'Benevento U19 (ITALY16)','data':'1'},{'value':'Brescia U19 (ITALY16)','data':'7'},{'value':'Como U19 (ITALY16)','data':'8'},{'value':'Vicenza V. U19 (ITALY16)','data':'9'},{'value':'Spezia U19 (ITALY16)','data':'24'},{'value':'Parma U19 (ITALY16)','data':'11'},{'value':'Pordenone U19 (ITALY16)','data':'13'},{'value':'Monza U19 (ITALY16)','data':'14'},{'value':'Reggiana U19 (ITALY16)','data':'15'},{'value':'Cittadella U19 (ITALY16)','data':'16'},{'value':'Venezia U19 (ITALY16)','data':'17'},{'value':'Cremonese U19 (ITALY16)','data':'18'},{'value':'Perugia U19 (ITALY16)','data':'19'},{'value':'Lazio U19 (ITALY16)','data':'20'},{'value':'Ternana U19 (ITALY16)','data':'21'},{'value':'V. Entella U19 (ITALY16)','data':'10'},{'value':'Juventus W (ITALY17)','data':'3'},{'value':'Verona W (ITALY17)','data':'10'},{'value':'Fiorentina W (ITALY17)','data':'12'},{'value':'Sassuolo W (ITALY17)','data':'11'},{'value':'AC Milan W (ITALY17)','data':'9'},{'value':'Sampdoria W (ITALY17)','data':'8'},{'value':'Lazio W (ITALY17)','data':'7'},{'value':'Inter Milan W (ITALY17)','data':'6'},{'value':'Pomigliano W (ITALY17)','data':'4'},{'value':'Roma W (ITALY17)','data':'2'},{'value':'Empoli W (ITALY17)','data':'1'},{'value':'Napoli W (ITALY17)','data':'5'},{'value':'Alessandria (ITALY2)','data':'14'},{'value':'Como (ITALY2)','data':'18'},{'value':'Ternana (ITALY2)','data':'9'},{'value':'Pisa (ITALY2)','data':'19'},{'value':'Perugia (ITALY2)','data':'4'},{'value':'Frosinone (ITALY2)','data':'1'},{'value':'Parma (ITALY2)','data':'2'},{'value':'Benevento (ITALY2)','data':'13'},{'value':'Monza (ITALY2)','data':'8'},{'value':'SPAL (ITALY2)','data':'20'},{'value':'Brescia (ITALY2)','data':'10'},{'value':'Crotone (ITALY2)','data':'17'},{'value':'Cosenza (ITALY2)','data':'12'},{'value':'Cittadella (ITALY2)','data':'5'},{'value':'Lecce (ITALY2)','data':'16'},{'value':'Pordenone (ITALY2)','data':'3'},{'value':'Chievo (ITALY2)','data':'12'},{'value':'Reggina (ITALY2)','data':'7'},{'value':'Vicenza (ITALY2)','data':'6'},{'value':'Cremonese (ITALY2)','data':'15'},{'value':'Ascoli (ITALY2)','data':'11'},{'value':'Virtus Verona (ITALY3)','data':'6'},{'value':'Legnago Salus (ITALY3)','data':'7'},{'value':'Giana Erminio (ITALY3)','data':'11'},{'value':'Sudtirol (ITALY3)','data':'5'},{'value':'AlbinoLeffe (ITALY3)','data':'18'},{'value':'Pro Sesto (ITALY3)','data':'12'},{'value':'Pergolettese (ITALY3)','data':'13'},{'value':'Juventus U23 (ITALY3)','data':'14'},{'value':'Triestina (ITALY3)','data':'9'},{'value':'Renate (ITALY3)','data':'3'},{'value':'Lecco (ITALY3)','data':'20'},{'value':'Livorno (ITALY3)','data':'4'},{'value':'Mantova (ITALY3)','data':'8'},{'value':'Padova (ITALY3)','data':'4'},{'value':'FeralpiSalo (ITALY3)','data':'1'},{'value':'Fiorenzuola (ITALY3)','data':'2'},{'value':'Seregno (ITALY3)','data':'10'},{'value':'Trento (ITALY3)','data':'16'},{'value':'Pro Patria (ITALY3)','data':'17'},{'value':'Piacenza (ITALY3)','data':'15'},{'value':'Pro Vercelli (ITALY3)','data':'19'},{'value':'Carrarese (ITALY4)','data':'16'},{'value':'Cesena (ITALY4)','data':'9'},{'value':'Olbia (ITALY4)','data':'7'},{'value':'Reggiana (ITALY4)','data':'19'},{'value':'Matelica (ITALY4)','data':'12'},{'value':'Virtus Entella (ITALY4)','data':'5'},{'value':'Imolese (ITALY4)','data':'13'},{'value':'Vis Pesaro (ITALY4)','data':'18'},{'value':'Carpi (ITALY4)','data':'3'},{'value':'Pescara (ITALY4)','data':'3'},{'value':'Gubbio (ITALY4)','data':'10'},{'value':'Modena (ITALY4)','data':'12'},{'value':'Fermana (ITALY4)','data':'1'},{'value':'Grosseto (ITALY4)','data':'11'},{'value':'Lucchese (ITALY4)','data':'14'},{'value':'Montevarchi (ITALY4)','data':'20'},{'value':'ACN Siena (ITALY4)','data':'17'},{'value':'Teramo (ITALY4)','data':'6'},{'value':'Pontedera (ITALY4)','data':'15'},{'value':'Viterbese (ITALY4)','data':'2'},{'value':'Pistoiese (ITALY4)','data':'8'},{'value':'Ancona 1905 (ITALY4)','data':'4'},{'value':'Juve Stabia (ITALY5)','data':'14'},{'value':'Campobasso (ITALY5)','data':'12'},{'value':'Turris (ITALY5)','data':'18'},{'value':'Avellino (ITALY5)','data':'11'},{'value':'Bari (ITALY5)','data':'20'},{'value':'V. Francavilla (ITALY5)','data':'10'},{'value':'Catanzaro (ITALY5)','data':'9'},{'value':'Potenza (ITALY5)','data':'19'},{'value':'Trapani (ITALY5)','data':'7'},{'value':'Palermo (ITALY5)','data':'15'},{'value':'Paganese (ITALY5)','data':'1'},{'value':'Catania (ITALY5)','data':'4'},{'value':'Vibonese (ITALY5)','data':'7'},{'value':'Monopoli (ITALY5)','data':'3'},{'value':'Foggia (ITALY5)','data':'6'},{'value':'Monterosi (ITALY5)','data':'5'},{'value':'Fidelis Andria (ITALY5)','data':'13'},{'value':'Latina (ITALY5)','data':'16'},{'value':'ACR Messina (ITALY5)','data':'2'},{'value':'Picerno (ITALY5)','data':'8'},{'value':'Taranto (ITALY5)','data':'17'},{'value':'Citta di Varese (ITALY6)','data':'12'},{'value':'Lavagnese (ITALY6)','data':'11'},{'value':'Vado (ITALY6)','data':'19'},{'value':'Chieri (ITALY6)','data':'5'},{'value':'Casale (ITALY6)','data':'3'},{'value':'Gozzano (ITALY6)','data':'9'},{'value':'Novara (ITALY6)','data':'13'},{'value':'Asti (ITALY6)','data':'14'},{'value':'RG Ticino (ITALY6)','data':'4'},{'value':'Ligorna (ITALY6)','data':'8'},{'value':'Sanremese (ITALY6)','data':'2'},{'value':'Bra (ITALY6)','data':'18'},{'value':'Pro Imperia (ITALY6)','data':'10'},{'value':'Saluzzo (ITALY6)','data':'17'},{'value':'Fossano (ITALY6)','data':'7'},{'value':'Borgosesia (ITALY6)','data':'6'},{'value':'Derthona (ITALY6)','data':'20'},{'value':'Caronnese (ITALY6)','data':'1'},{'value':'PDHAE (ITALY6)','data':'15'},{'value':'Sestri Levante (ITALY6)','data':'16'},{'value':'Nibionnoggiono (ITALY7)','data':'8'},{'value':'Adrense (ITALY7)','data':'9'},{'value':'Casatese (ITALY7)','data':'18'},{'value':'Ciserano (ITALY7)','data':'13'},{'value':'Sona (ITALY7)','data':'7'},{'value':'Calvina (ITALY7)','data':'20'},{'value':'Breno (ITALY7)','data':'16'},{'value':'Caravaggio (ITALY7)','data':'19'},{'value':'Villa Alme (ITALY7)','data':'11'},{'value':'Crema (ITALY7)','data':'8'},{'value':'Olginatese (ITALY7)','data':'2'},{'value':'Real Calepina (ITALY7)','data':'5'},{'value':'Vis N. Giussano (ITALY7)','data':'15'},{'value':'Scanzorosciate (ITALY7)','data':'14'},{'value':'Brusaporto (ITALY7)','data':'6'},{'value':'Sangiuliano CN (ITALY7)','data':'12'},{'value':'Pontisola (ITALY7)','data':'10'},{'value':'F. Caratese (ITALY7)','data':'1'},{'value':'Legnano (ITALY7)','data':'14'},{'value':'Arconatese (ITALY7)','data':'17'},{'value':'Castellanzese (ITALY7)','data':'4'},{'value':'Leon (ITALY7)','data':'3'},{'value':'Cartigliano (ITALY8)','data':'15'},{'value':'Dolomiti Bellun (ITALY8)','data':'5'},{'value':'Levico (ITALY8)','data':'6'},{'value':'Manzanese (ITALY8)','data':'2'},{'value':'Ambrosiana (ITALY8)','data':'9'},{'value':'Caldiero Terme (ITALY8)','data':'1'},{'value':'Arzignano (ITALY8)','data':'10'},{'value':'Spinea (ITALY8)','data':'18'},{'value':'Mestre (ITALY8)','data':'4'},{'value':'Adriese (ITALY8)','data':'8'},{'value':'Montebelluna (ITALY8)','data':'11'},{'value':'Chions (ITALY8)','data':'11'},{'value':'San Giorgio-S. (ITALY8)','data':'12'},{'value':'Luparense (ITALY8)','data':'20'},{'value':'Delta Porto T. (ITALY8)','data':'17'},{'value':'Union Feltre (ITALY8)','data':'18'},{'value':'Virtus Bolzano (ITALY8)','data':'17'},{'value':'Belluno (ITALY8)','data':'16'},{'value':'Este (ITALY8)','data':'14'},{'value':'Clodiense (ITALY8)','data':'7'},{'value':'Cjarlins Muzane (ITALY8)','data':'3'},{'value':'Campodarsego (ITALY8)','data':'13'},{'value':'Cattolica C. (ITALY8)','data':'16'},{'value':'San Martino Spe (ITALY8)','data':'12'},{'value':'Luparense (ITALY8)','data':'2'},{'value':'Cattolica (ITALY8)','data':'10'},{'value':'Sammaurese (ITALY9)','data':'10'},{'value':'Real Forte Q. (ITALY9)','data':'15'},{'value':'Ghivizzano BM (ITALY9)','data':'11'},{'value':'Mezzolara (ITALY9)','data':'13'},{'value':'Progresso (ITALY9)','data':'8'},{'value':'Sasso M. Zola (ITALY9)','data':'9'},{'value':'Prato (ITALY9)','data':'18'},{'value':'Ravenna (ITALY9)','data':'16'},{'value':'Correggese (ITALY9)','data':'10'},{'value':'Corticella (ITALY9)','data':'11'},{'value':'Tritium (ITALY9)','data':'2'},{'value':'Bagnolese (ITALY9)','data':'6'},{'value':'Lentigione (ITALY9)','data':'20'},{'value':'Seravezza (ITALY9)','data':'19'},{'value':'Forlì (ITALY9)','data':'4'},{'value':'B. San Donnino (ITALY9)','data':'14'},{'value':'Sasso Marconi (ITALY9)','data':'12'},{'value':'Correggese (ITALY9)','data':'7'},{'value':'Athletic Carpi (ITALY9)','data':'5'},{'value':'Alcione (ITALY9)','data':'3'},{'value':'Rimini (ITALY9)','data':'17'},{'value':'Fanfula (ITALY9)','data':'9'},{'value':'Aglianese (ITALY9)','data':'1'},{'value':'UWI (JAMAICA)','data':'8'},{'value':'Vere Utd (JAMAICA)','data':'3'},{'value':'Arnett Gardens (JAMAICA)','data':'2'},{'value':'Dunbeholden (JAMAICA)','data':'10'},{'value':'Tivoli Gardens (JAMAICA)','data':'1'},{'value':'Portmore Utd (JAMAICA)','data':'4'},{'value':'Molynes Utd (JAMAICA)','data':'5'},{'value':'Cavalier (JAMAICA)','data':'9'},{'value':'Mount Pleasant  (JAMAICA)','data':'6'},{'value':'Humble Lions (JAMAICA)','data':'12'},{'value':'Harbour View (JAMAICA)','data':'7'},{'value':'Waterhouse (JAMAICA)','data':'11'},{'value':'Sagan Tosu (JAPAN)','data':'14'},{'value':'C. Sapporo (JAPAN)','data':'3'},{'value':'Kashiwa Reysol (JAPAN)','data':'16'},{'value':'Nagoya G. (JAPAN)','data':'20'},{'value':'Vissel Kobe (JAPAN)','data':'17'},{'value':'Vegalta Sendai (JAPAN)','data':'8'},{'value':'Urawa RD (JAPAN)','data':'5'},{'value':'Cerezo Osaka (JAPAN)','data':'15'},{'value':'Shonan Bellmare (JAPAN)','data':'13'},{'value':'K. Frontale (JAPAN)','data':'1'},{'value':'Avispa Fukuoka (JAPAN)','data':'19'},{'value':'Tokushima V. (JAPAN)','data':'10'},{'value':'Oita Trinita (JAPAN)','data':'9'},{'value':'Shimizu S-Pulse (JAPAN)','data':'12'},{'value':'FC Tokyo (JAPAN)','data':'6'},{'value':'Yokohama M. (JAPAN)','data':'2'},{'value':'Gamba Osaka (JAPAN)','data':'18'},{'value':'Kashima Antlers (JAPAN)','data':'11'},{'value':'Yokohama FC (JAPAN)','data':'4'},{'value':'S. Hiroshima (JAPAN)','data':'7'},{'value':'G. Kitakyushu (JAPAN2)','data':'1'},{'value':'Albirex Niigata (JAPAN2)','data':'2'},{'value':'R. Yamaguchi (JAPAN2)','data':'21'},{'value':'Ehime FC (JAPAN2)','data':'18'},{'value':'Blaublitz Akita (JAPAN2)','data':'12'},{'value':'Kyoto Sanga (JAPAN2)','data':'6'},{'value':'Tochigi SC (JAPAN2)','data':'9'},{'value':'V-V. Nagasaki (JAPAN2)','data':'3'},{'value':'SC Sagamihara (JAPAN2)','data':'5'},{'value':'Tokyo Verdy (JAPAN2)','data':'17'},{'value':'Matsumoto Y. (JAPAN2)','data':'22'},{'value':'T. Gunma (JAPAN2)','data':'11'},{'value':'Mito Hollyhock (JAPAN2)','data':'7'},{'value':'JEF Utd Chiba (JAPAN2)','data':'13'},{'value':'FC Ryukyu (JAPAN2)','data':'19'},{'value':'Machida Zelvia (JAPAN2)','data':'15'},{'value':'Ventforet Kofu (JAPAN2)','data':'14'},{'value':'Jubilo Iwata (JAPAN2)','data':'20'},{'value':'M. Yamagata (JAPAN2)','data':'16'},{'value':'Fagiano Okayama (JAPAN2)','data':'10'},{'value':'Z. Kanazawa (JAPAN2)','data':'4'},{'value':'Omiya Ardija (JAPAN2)','data':'8'},{'value':'Gainare Tottori (JAPAN3)','data':'14'},{'value':'T. Miyazaki (JAPAN3)','data':'7'},{'value':'Gamba Osaka B (JAPAN3)','data':'18'},{'value':'Kamatamare S. (JAPAN3)','data':'11'},{'value':'Nagano Parceiro (JAPAN3)','data':'12'},{'value':'Kataller Toyama (JAPAN3)','data':'4'},{'value':'Fukushima Utd (JAPAN3)','data':'1'},{'value':'FC Gifu (JAPAN3)','data':'9'},{'value':'V. Hachinohe (JAPAN3)','data':'10'},{'value':'Cerezo Osaka B (JAPAN3)','data':'11'},{'value':'Kagoshima Utd (JAPAN3)','data':'13'},{'value':'R. Kumamoto (JAPAN3)','data':'6'},{'value':'YSCC (JAPAN3)','data':'3'},{'value':'Fujieda MYFC (JAPAN3)','data':'2'},{'value':'AC Numazu (JAPAN3)','data':'15'},{'value':'FC Imabari (JAPAN3)','data':'5'},{'value':'IG Morioka (JAPAN3)','data':'8'},{'value':'Cerezo Osaka W (JAPAN4)','data':'11'},{'value':'NGU Nagoya W (JAPAN4)','data':'8'},{'value':'Yokohama W (JAPAN4)','data':'7'},{'value':'Y. Sylphid W (JAPAN4)','data':'6'},{'value':'S. Sfida W (JAPAN4)','data':'5'},{'value':'Nittaidai W (JAPAN4)','data':'4'},{'value':'Speranza W (JAPAN4)','data':'10'},{'value':'Ehime W (JAPAN4)','data':'1'},{'value':'Kamogawa W (JAPAN4)','data':'3'},{'value':'Urawa RD W (JAPAN4)','data':'4'},{'value':'JEF United W (JAPAN4)','data':'3'},{'value':'INAC Kobe L. W (JAPAN4)','data':'2'},{'value':'Iga Kunoichi W (JAPAN4)','data':'9'},{'value':'Nojima Stella W (JAPAN4)','data':'10'},{'value':'A. Hiroshima W (JAPAN4)','data':'2'},{'value':'NTV Beleza W (JAPAN4)','data':'9'},{'value':'A. Niigata W (JAPAN4)','data':'8'},{'value':'Harima W (JAPAN4)','data':'12'},{'value':'V. Sendai W (JAPAN4)','data':'7'},{'value':'Kariya (JAPAN5)','data':'10'},{'value':'Sony Sendai (JAPAN5)','data':'4'},{'value':'Suzuka U. (JAPAN5)','data':'5'},{'value':'Matsue City (JAPAN5)','data':'17'},{'value':'Honda Lock (JAPAN5)','data':'6'},{'value':'Iwaki (JAPAN5)','data':'7'},{'value':'Honda (JAPAN5)','data':'3'},{'value':'Osaka (JAPAN5)','data':'9'},{'value':'Biwako Shiga (JAPAN5)','data':'11'},{'value':'Nara Club (JAPAN5)','data':'12'},{'value':'Tokyo Musashino (JAPAN5)','data':'13'},{'value':'Reinmeer Aomori (JAPAN5)','data':'14'},{'value':'TIAMO Hirakata (JAPAN5)','data':'16'},{'value':'Veertien Mie (JAPAN5)','data':'8'},{'value':'M. Okazaki (JAPAN5)','data':'15'},{'value':'Verspah Oita (JAPAN5)','data':'1'},{'value':'Kochi Utd (JAPAN5)','data':'2'},{'value':'Al Hussein (JORDAN)','data':'5'},{'value':'Al Ahli (JORDAN)','data':'11'},{'value':'Al Wihdat (JORDAN)','data':'12'},{'value':'Al Sareeh (JORDAN)','data':'9'},{'value':'Al Ramtha (JORDAN)','data':'8'},{'value':'Al Faysali (JORDAN)','data':'10'},{'value':'Aqaba (JORDAN)','data':'7'},{'value':'Sahab (JORDAN)','data':'9'},{'value':'Al Jazeera (JORDAN)','data':'2'},{'value':'Maan (JORDAN)','data':'4'},{'value':'Al Salt (JORDAN)','data':'1'},{'value':'Al Buqa`a (JORDAN)','data':'11'},{'value':'Al Jalil (JORDAN)','data':'6'},{'value':'Shabab Al Ordon (JORDAN)','data':'3'},{'value':'Akzhayik (KAZAKHSTAN)','data':'14'},{'value':'FC Astana (KAZAKHSTAN)','data':'6'},{'value':'Zhetysu (KAZAKHSTAN)','data':'2'},{'value':'Aktobe (KAZAKHSTAN)','data':'8'},{'value':'Kairat Almaty (KAZAKHSTAN)','data':'1'},{'value':'Atyrau (KAZAKHSTAN)','data':'3'},{'value':'S. Karagandy (KAZAKHSTAN)','data':'4'},{'value':'Arys (KAZAKHSTAN)','data':'5'},{'value':'Kaspiy Aktau (KAZAKHSTAN)','data':'7'},{'value':'Ordabasy (KAZAKHSTAN)','data':'9'},{'value':'Kyzylzhar (KAZAKHSTAN)','data':'10'},{'value':'Kaisar K. (KAZAKHSTAN)','data':'11'},{'value':'Taraz (KAZAKHSTAN)','data':'12'},{'value':'Tobol (KAZAKHSTAN)','data':'13'},{'value':'Taraz B (KAZAKHSTAN2)','data':'6'},{'value':'Kyzylzhar B (KAZAKHSTAN2)','data':'12'},{'value':'Baykonur (KAZAKHSTAN2)','data':'11'},{'value':'Kyran (KAZAKHSTAN2)','data':'1'},{'value':'A. Ontustik (KAZAKHSTAN2)','data':'2'},{'value':'Igilik (KAZAKHSTAN2)','data':'3'},{'value':'Bulat (KAZAKHSTAN2)','data':'10'},{'value':'Aksu (KAZAKHSTAN2)','data':'5'},{'value':'Maqtaaral (KAZAKHSTAN2)','data':'7'},{'value':'S. A. Kairat (KAZAKHSTAN2)','data':'9'},{'value':'Ekibastuz (KAZAKHSTAN2)','data':'8'},{'value':'Okzhetpes (KAZAKHSTAN2)','data':'4'},{'value':'Posta Rangers (KENYA)','data':'3'},{'value':'Ulinzi Stars (KENYA)','data':'17'},{'value':'Bidco Utd (KENYA)','data':'6'},{'value':'Gor Mahia (KENYA)','data':'1'},{'value':'Police (KENYA)','data':'16'},{'value':'Talanta (KENYA)','data':'9'},{'value':'Vihiga Bullets (KENYA)','data':'5'},{'value':'Leopards (KENYA)','data':'13'},{'value':'Vihiga United (KENYA)','data':'5'},{'value':'Mathare Utd (KENYA)','data':'8'},{'value':'Western Stima (KENYA)','data':'9'},{'value':'Tusker (KENYA)','data':'14'},{'value':'KCB (KENYA)','data':'2'},{'value':'Bandari (KENYA)','data':'7'},{'value':'Zoo Kericho (KENYA)','data':'18'},{'value':'Kariobangi S. (KENYA)','data':'4'},{'value':'Wazito (KENYA)','data':'10'},{'value':'Nairobi City S. (KENYA)','data':'12'},{'value':'Nzoia (KENYA)','data':'18'},{'value':'Sofapaka (KENYA)','data':'11'},{'value':'Homeboyz (KENYA)','data':'15'},{'value':'Gjilani (KOSOVO)','data':'8'},{'value':'Arberia (KOSOVO)','data':'2'},{'value':'Ballkani (KOSOVO)','data':'5'},{'value':'Dukagjini (KOSOVO)','data':'6'},{'value':'Trepca 89 (KOSOVO)','data':'1'},{'value':'Ulpiana (KOSOVO)','data':'10'},{'value':'Prishtina (KOSOVO)','data':'4'},{'value':'Drenica (KOSOVO)','data':'7'},{'value':'Besa Peje (KOSOVO)','data':'5'},{'value':'Feronikeli (KOSOVO)','data':'2'},{'value':'Llapi (KOSOVO)','data':'9'},{'value':'Drita (KOSOVO)','data':'1'},{'value':'Malisheva (KOSOVO)','data':'3'},{'value':'Al Qadsia (KUWAIT)','data':'10'},{'value':'Al Kuwait (KUWAIT)','data':'7'},{'value':'Al Shabab (KUWAIT)','data':'9'},{'value':'Khaitan (KUWAIT)','data':'1'},{'value':'Al Nasar (KUWAIT)','data':'5'},{'value':'Al Tadhamon (KUWAIT)','data':'4'},{'value':'Burgan (KUWAIT)','data':'8'},{'value':'Al Jahra (KUWAIT)','data':'7'},{'value':'Kazma (KUWAIT)','data':'1'},{'value':'Al Sahel (KUWAIT)','data':'2'},{'value':'Al Fahaheel (KUWAIT)','data':'2'},{'value':'Al Salmiyah (KUWAIT)','data':'6'},{'value':'Al Arabi SC (KUWAIT)','data':'3'},{'value':'Al Sulaibikhat (KUWAIT)','data':'2'},{'value':'Yarmouk (KUWAIT)','data':'8'},{'value':'Kauno Zalgiris (LITHUANIA)','data':'1'},{'value':'Riteriai (LITHUANIA)','data':'10'},{'value':'Panevezys (LITHUANIA)','data':'8'},{'value':'Suduva (LITHUANIA)','data':'7'},{'value':'Nevezis (LITHUANIA)','data':'6'},{'value':'Dainava (LITHUANIA)','data':'5'},{'value':'Hegelmann L. (LITHUANIA)','data':'4'},{'value':'Dziugas Telsiai (LITHUANIA)','data':'3'},{'value':'Banga (LITHUANIA)','data':'2'},{'value':'Zalgiris (LITHUANIA)','data':'9'},{'value':'Silas (LITHUANIA2)','data':'4'},{'value':'BFA Vilnius (LITHUANIA2)','data':'7'},{'value':'Neptuna K. (LITHUANIA2)','data':'12'},{'value':'Riteriai B (LITHUANIA2)','data':'10'},{'value':'Kauno Z. B (LITHUANIA2)','data':'9'},{'value':'Atmosfera (LITHUANIA2)','data':'8'},{'value':'FA Siauliai (LITHUANIA2)','data':'5'},{'value':'Panevezys B (LITHUANIA2)','data':'11'},{'value':'Minija (LITHUANIA2)','data':'3'},{'value':'Babrungas (LITHUANIA2)','data':'2'},{'value':'Jonava (LITHUANIA2)','data':'1'},{'value':'Banga B (LITHUANIA2)','data':'13'},{'value':'Zalgiris B (LITHUANIA2)','data':'14'},{'value':'Suduva B (LITHUANIA2)','data':'6'},{'value':'Fola Esch (LUXEMBOURG)','data':'6'},{'value':'Wiltz (LUXEMBOURG)','data':'15'},{'value':'Ettelbruck (LUXEMBOURG)','data':'3'},{'value':'Petange (LUXEMBOURG)','data':'11'},{'value':'UNA Strassen (LUXEMBOURG)','data':'12'},{'value':'Hesperang (LUXEMBOURG)','data':'2'},{'value':'Differdange (LUXEMBOURG)','data':'16'},{'value':'Jeunesse Esch (LUXEMBOURG)','data':'9'},{'value':'V. Rosport (LUXEMBOURG)','data':'4'},{'value':'Rodange (LUXEMBOURG)','data':'8'},{'value':'Mondorf (LUXEMBOURG)','data':'5'},{'value':'Hostert (LUXEMBOURG)','data':'7'},{'value':'Racing (LUXEMBOURG)','data':'1'},{'value':'Dudelange (LUXEMBOURG)','data':'14'},{'value':'Niedercorn (LUXEMBOURG)','data':'13'},{'value':'Hamm Benfica (LUXEMBOURG)','data':'10'},{'value':'Chitipa Utd (MALAWI)','data':'6'},{'value':'Ekwendeni H. (MALAWI)','data':'1'},{'value':'Kamuzu Barracks (MALAWI)','data':'2'},{'value':'Mighty Tigers (MALAWI)','data':'3'},{'value':'TN Stars (MALAWI)','data':'4'},{'value':'MAFCO (MALAWI)','data':'7'},{'value':'Red Lions (MALAWI)','data':'8'},{'value':'Big Bullets (MALAWI)','data':'9'},{'value':'Blue Eagles (MALAWI)','data':'10'},{'value':'CIVO Utd (MALAWI)','data':'11'},{'value':'Silver Strikers (MALAWI)','data':'12'},{'value':'Ntopwa (MALAWI)','data':'13'},{'value':'Moyale Barracks (MALAWI)','data':'14'},{'value':'Karonga Utd (MALAWI)','data':'5'},{'value':'BF Wanderers (MALAWI)','data':'16'},{'value':'Mzuni (MALAWI)','data':'15'},{'value':'Melaka Utd (MALAYSIA)','data':'9'},{'value':'UiTM (MALAYSIA)','data':'5'},{'value':'Terengganu (MALAYSIA)','data':'6'},{'value':'Petaling Jaya (MALAYSIA)','data':'12'},{'value':'Perak (MALAYSIA)','data':'11'},{'value':'Pulau Pinang (MALAYSIA)','data':'3'},{'value':'Pahang (MALAYSIA)','data':'8'},{'value':'Kedah (MALAYSIA)','data':'2'},{'value':'Sabah (MALAYSIA)','data':'10'},{'value':'Selangor (MALAYSIA)','data':'7'},{'value':'Johor Darul (MALAYSIA)','data':'1'},{'value':'Kuala Lumpur (MALAYSIA)','data':'4'},{'value':'Johor Darul B (MALAYSIA2)','data':'8'},{'value':'Kuching (MALAYSIA2)','data':'11'},{'value':'Sarawak Utd (MALAYSIA2)','data':'9'},{'value':'Negeri Sembilan (MALAYSIA2)','data':'7'},{'value':'Selangor B (MALAYSIA2)','data':'6'},{'value':'PDRM (MALAYSIA2)','data':'5'},{'value':'Kelantan (MALAYSIA2)','data':'1'},{'value':'Perak B (MALAYSIA2)','data':'2'},{'value':'Skuad Projek (MALAYSIA2)','data':'4'},{'value':'Terengganu B (MALAYSIA2)','data':'3'},{'value':'Kelantan United (MALAYSIA2)','data':'10'},{'value':'Balzan (MALTA)','data':'1'},{'value':'Birkirkara (MALTA)','data':'8'},{'value':'Valletta (MALTA)','data':'6'},{'value':'Sirens (MALTA)','data':'4'},{'value':'Hamrun Spartans (MALTA)','data':'5'},{'value':'Gzira Utd (MALTA)','data':'11'},{'value':'Floriana (MALTA)','data':'9'},{'value':'Sliema W. (MALTA)','data':'2'},{'value':'Hibernians (MALTA)','data':'12'},{'value':'Gudja Utd (MALTA)','data':'3'},{'value':'Mosta (MALTA)','data':'7'},{'value':'Santa Lucia (MALTA)','data':'10'},{'value':'Mgarr (MALTA2)','data':'21'},{'value':'Vittoriosa (MALTA2)','data':'11'},{'value':'Tarxien (MALTA2)','data':'4'},{'value':'Qrendi (MALTA2)','data':'20'},{'value':'Marsaxlokk (MALTA2)','data':'14'},{'value':'Naxxar Lions (MALTA2)','data':'7'},{'value':'Rabat Ajax (MALTA2)','data':'22'},{'value':'Marsa (MALTA2)','data':'18'},{'value':'Luqa (MALTA2)','data':'19'},{'value':'Melita (MALTA2)','data':'13'},{'value':'Zejtun C. (MALTA2)','data':'1'},{'value':'Lija Athletic (MALTA2)','data':'2'},{'value':'San Gwann (MALTA2)','data':'5'},{'value':'Senglea A. (MALTA2)','data':'3'},{'value':'Qormi (MALTA2)','data':'9'},{'value':'St. Andrews (MALTA2)','data':'17'},{'value':'Fgura Utd (MALTA2)','data':'10'},{'value':'Zebbug Rangers (MALTA2)','data':'15'},{'value':'Mqabba (MALTA2)','data':'8'},{'value':'Swieqi (MALTA2)','data':'9'},{'value':'St. George`s (MALTA2)','data':'6'},{'value':'Pembroke (MALTA2)','data':'12'},{'value':'Pieta Hotspurs (MALTA2)','data':'16'},{'value':'Bolton City (MAURITIUS)','data':'3'},{'value':'AS Vacoas P. (MAURITIUS)','data':'5'},{'value':'AS Port Louis (MAURITIUS)','data':'6'},{'value':'Cercle Joachim (MAURITIUS)','data':'7'},{'value':'Petite Riviere  (MAURITIUS)','data':'8'},{'value':'La Cure S. (MAURITIUS)','data':'9'},{'value':'Grande Riviere  (MAURITIUS)','data':'10'},{'value':'Entente Boulet  (MAURITIUS)','data':'2'},{'value':'Pamplemousses (MAURITIUS)','data':'1'},{'value':'Savanne (MAURITIUS)','data':'4'},{'value':'Atlas (MEXICO)','data':'12'},{'value':'CF America (MEXICO)','data':'2'},{'value':'Necaxa (MEXICO)','data':'3'},{'value':'Santos Laguna (MEXICO)','data':'4'},{'value':'Toluca (MEXICO)','data':'6'},{'value':'Club Leon (MEXICO)','data':'8'},{'value':'Guadalajara (MEXICO)','data':'9'},{'value':'Queretaro (MEXICO)','data':'1'},{'value':'Pumas UNAM (MEXICO)','data':'11'},{'value':'Juarez (MEXICO)','data':'5'},{'value':'Monterrey (MEXICO)','data':'13'},{'value':'Puebla (MEXICO)','data':'14'},{'value':'Tijuana (MEXICO)','data':'15'},{'value':'Tigres (MEXICO)','data':'16'},{'value':'Cruz Azul (MEXICO)','data':'17'},{'value':'Mazatlan (MEXICO)','data':'18'},{'value':'A. San Luis (MEXICO)','data':'10'},{'value':'Pachuca (MEXICO)','data':'7'},{'value':'Leones Negros (MEXICO5)','data':'9'},{'value':'Toluca W (MEXICO5)','data':'9'},{'value':'Tigres UANL W (MEXICO5)','data':'13'},{'value':'Juarez W (MEXICO5)','data':'17'},{'value':'Necaxa W (MEXICO5)','data':'4'},{'value':'Leon W (MEXICO5)','data':'6'},{'value':'Pumas UNAM W (MEXICO5)','data':'3'},{'value':'Colima (MEXICO5)','data':'13'},{'value':'Canoneros M. (MEXICO5)','data':'12'},{'value':'Queretaro W (MEXICO5)','data':'1'},{'value':'Tecos (MEXICO5)','data':'10'},{'value':'Pachuca W (MEXICO5)','data':'11'},{'value':'ACD Uruapan (MEXICO5)','data':'8'},{'value':'Zitacuaro (MEXICO5)','data':'7'},{'value':'Atl. San Luis B (MEXICO5)','data':'6'},{'value':'Santos Laguna W (MEXICO5)','data':'8'},{'value':'Durango (MEXICO5)','data':'5'},{'value':'M. Fresnillo (MEXICO5)','data':'4'},{'value':'Atl. Saltillo (MEXICO5)','data':'3'},{'value':'CAFESSA Jalisco (MEXICO5)','data':'2'},{'value':'Inter Playa d. (MEXICO5)','data':'1'},{'value':'Ciervos (MEXICO5)','data':'11'},{'value':'Cimarrones B (MEXICO5)','data':'19'},{'value':'UA Zacatecas (MEXICO5)','data':'25'},{'value':'Cuautla (MEXICO5)','data':'24'},{'value':'Reb. La Piedad (MEXICO5)','data':'23'},{'value':'C. Azul Hidaldo (MEXICO5)','data':'22'},{'value':'Tijuana W (MEXICO5)','data':'12'},{'value':'Mazorqueros (MEXICO5)','data':'20'},{'value':'Atl. San Luis W (MEXICO5)','data':'16'},{'value':'Pioneros Cancun (MEXICO5)','data':'18'},{'value':'Caf. Chiapas B (MEXICO5)','data':'17'},{'value':'Deportivo Dongu (MEXICO5)','data':'16'},{'value':'Monterrey W (MEXICO5)','data':'2'},{'value':'Irapuato (MEXICO5)','data':'21'},{'value':'Puebla W (MEXICO5)','data':'5'},{'value':'Azores Hidalgo (MEXICO5)','data':'15'},{'value':'Mazatlan W (MEXICO5)','data':'14'},{'value':'America W (MEXICO5)','data':'7'},{'value':'Cruz Azul W (MEXICO5)','data':'18'},{'value':'Guadalajara W (MEXICO5)','data':'15'},{'value':'Gavilanes FC (MEXICO5)','data':'14'},{'value':'Atlas W (MEXICO5)','data':'10'},{'value':'Floresti (MOLDOVA)','data':'1'},{'value':'Zimbru Chisinau (MOLDOVA)','data':'5'},{'value':'Petrocub (MOLDOVA)','data':'2'},{'value':'Milsami (MOLDOVA)','data':'7'},{'value':'Codru Lozova (MOLDOVA)','data':'6'},{'value':'S. Gheorghe (MOLDOVA)','data':'8'},{'value':'Dinamo-Auto (MOLDOVA)','data':'6'},{'value':'S. Tiraspol (MOLDOVA)','data':'3'},{'value':'Dacia-Buiucani (MOLDOVA)','data':'10'},{'value':'CSF Balti (MOLDOVA)','data':'4'},{'value':'S. Nisporeni (MOLDOVA)','data':'4'},{'value':'Rudar (MONTENEGRO)','data':'1'},{'value':'Decic (MONTENEGRO)','data':'7'},{'value':'Buducnost (MONTENEGRO)','data':'2'},{'value':'Mornar (MONTENEGRO)','data':'4'},{'value':'Jezero (MONTENEGRO)','data':'6'},{'value':'Zeta (MONTENEGRO)','data':'8'},{'value':'Iskra (MONTENEGRO)','data':'5'},{'value':'Sutjeska (MONTENEGRO)','data':'9'},{'value':'Petrovac (MONTENEGRO)','data':'3'},{'value':'Podgorica (MONTENEGRO)','data':'10'},{'value':'Khouribga (MOROCCO)','data':'5'},{'value':'C. Mohammedia (MOROCCO)','data':'7'},{'value':'Maghreb de Fes (MOROCCO)','data':'13'},{'value':'Hassania Agadir (MOROCCO)','data':'9'},{'value':'Difaa El Jadida (MOROCCO)','data':'4'},{'value':'Olympic Safi (MOROCCO)','data':'3'},{'value':'Mouloudia Oujda (MOROCCO)','data':'6'},{'value':'Ittihad Tanger (MOROCCO)','data':'12'},{'value':'Wydad (MOROCCO)','data':'11'},{'value':'Salmi (MOROCCO)','data':'16'},{'value':'Youssoufia B. (MOROCCO)','data':'1'},{'value':'FAR Rabat (MOROCCO)','data':'15'},{'value':'Rapide Oued Z. (MOROCCO)','data':'10'},{'value':'FUS Rabat (MOROCCO)','data':'8'},{'value':'Berkane (MOROCCO)','data':'14'},{'value':'Raja Casablanca (MOROCCO)','data':'2'},{'value':'I. Khemisset (MOROCCO2)','data':'12'},{'value':'El Massira (MOROCCO2)','data':'5'},{'value':'KAC Kenitra (MOROCCO2)','data':'15'},{'value':'Kawkab M. (MOROCCO2)','data':'14'},{'value':'RAC Casablanca (MOROCCO2)','data':'9'},{'value':'UTS Rabat (MOROCCO2)','data':'2'},{'value':'AS Salé (MOROCCO2)','data':'3'},{'value':'Chabab Atlas K. (MOROCCO2)','data':'15'},{'value':'Stade Marocain (MOROCCO2)','data':'7'},{'value':'USM Oujda (MOROCCO2)','data':'6'},{'value':'Dcheira (MOROCCO2)','data':'1'},{'value':'Wydad Fès (MOROCCO2)','data':'4'},{'value':'C. Benguerir (MOROCCO2)','data':'11'},{'value':'Widad Temara (MOROCCO2)','data':'4'},{'value':'R. Zemamra (MOROCCO2)','data':'13'},{'value':'TAS Casamblanca (MOROCCO2)','data':'16'},{'value':'R. Beni Mellal (MOROCCO2)','data':'10'},{'value':'Moghreb Tetouan (MOROCCO2)','data':'8'},{'value':'FC Groningen (NETHERLANDS)','data':'12'},{'value':'PSV Eindhoven (NETHERLANDS)','data':'6'},{'value':'RKC Waalwijk (NETHERLANDS)','data':'3'},{'value':'Vitesse Arnhem (NETHERLANDS)','data':'14'},{'value':'FC Utrecht (NETHERLANDS)','data':'15'},{'value':'Cambuur (NETHERLANDS)','data':'11'},{'value':'NEC Nijmegen (NETHERLANDS)','data':'10'},{'value':'Go Ahead Eagles (NETHERLANDS)','data':'1'},{'value':'AZ Alkmaar (NETHERLANDS)','data':'4'},{'value':'Heerenveen (NETHERLANDS)','data':'2'},{'value':'Ajax Amsterdam (NETHERLANDS)','data':'9'},{'value':'Fortuna Sittard (NETHERLANDS)','data':'7'},{'value':'FC Twente (NETHERLANDS)','data':'8'},{'value':'Feyenoord (NETHERLANDS)','data':'18'},{'value':'PEC Zwolle (NETHERLANDS)','data':'13'},{'value':'Willem II (NETHERLANDS)','data':'17'},{'value':'Sparta (NETHERLANDS)','data':'16'},{'value':'Heracles Almelo (NETHERLANDS)','data':'5'},{'value':'FC Dordrecht (NETHERLANDS2)','data':'3'},{'value':'Roda JC (NETHERLANDS2)','data':'12'},{'value':'Jong Ajax (NETHERLANDS2)','data':'14'},{'value':'FC Volendam (NETHERLANDS2)','data':'6'},{'value':'Almere City (NETHERLANDS2)','data':'18'},{'value':'Jong AZ (NETHERLANDS2)','data':'17'},{'value':'NAC Breda (NETHERLANDS2)','data':'16'},{'value':'Telstar (NETHERLANDS2)','data':'9'},{'value':'FC Emmen (NETHERLANDS2)','data':'10'},{'value':'De Graafschap (NETHERLANDS2)','data':'11'},{'value':'FC Den Bosch (NETHERLANDS2)','data':'1'},{'value':'TOP Oss (NETHERLANDS2)','data':'8'},{'value':'Excelsior (NETHERLANDS2)','data':'7'},{'value':'Jong PSV (NETHERLANDS2)','data':'4'},{'value':'FC Eindhoven (NETHERLANDS2)','data':'5'},{'value':'Jong Utrecht (NETHERLANDS2)','data':'19'},{'value':'ADO Den Haag (NETHERLANDS2)','data':'13'},{'value':'Helmond Sport (NETHERLANDS2)','data':'2'},{'value':'MVV Maastricht (NETHERLANDS2)','data':'20'},{'value':'VVV (NETHERLANDS2)','data':'15'},{'value':'Jong Sparta (NETHERLANDS3)','data':'17'},{'value':'Quick Boys (NETHERLANDS3)','data':'11'},{'value':'AFC (NETHERLANDS3)','data':'5'},{'value':'De Treffers (NETHERLANDS3)','data':'18'},{'value':'HHC (NETHERLANDS3)','data':'15'},{'value':'Volendam II (NETHERLANDS3)','data':'14'},{'value':'Koninklijke HFC (NETHERLANDS3)','data':'4'},{'value':'TEC (NETHERLANDS3)','data':'8'},{'value':'ASWH (NETHERLANDS3)','data':'7'},{'value':'Kozakken Boys (NETHERLANDS3)','data':'12'},{'value':'Rijnsburgse Boy (NETHERLANDS3)','data':'2'},{'value':'IJsselmeervogel (NETHERLANDS3)','data':'10'},{'value':'Noordwijk (NETHERLANDS3)','data':'3'},{'value':'Katwijk (NETHERLANDS3)','data':'6'},{'value':'Excelsior Ma. (NETHERLANDS3)','data':'9'},{'value':'GVVV (NETHERLANDS3)','data':'1'},{'value':'Scheveningen (NETHERLANDS3)','data':'16'},{'value':'Spakenburg (NETHERLANDS3)','data':'13'},{'value':'GOES (NETHERLANDS4)','data':'8'},{'value':'HSV Hoek (NETHERLANDS4)','data':'13'},{'value':'DVS 33 (NETHERLANDS4)','data':'12'},{'value':'Barendrecht (NETHERLANDS4)','data':'14'},{'value':'Ajax Amateurs (NETHERLANDS4)','data':'11'},{'value':'DOVO (NETHERLANDS4)','data':'10'},{'value':'VVOG (NETHERLANDS4)','data':'9'},{'value':'Sparta Nijkerk (NETHERLANDS4)','data':'17'},{'value':'Sportlust (NETHERLANDS4)','data':'15'},{'value':'ODIN (NETHERLANDS4)','data':'18'},{'value':'Staphorst (NETHERLANDS4)','data':'1'},{'value':'VVSB (NETHERLANDS4)','data':'2'},{'value':'Lisse (NETHERLANDS4)','data':'3'},{'value':'ACV (NETHERLANDS4)','data':'4'},{'value':'Excelsior 31 (NETHERLANDS4)','data':'5'},{'value':'Ter Leede (NETHERLANDS4)','data':'6'},{'value':'Harkemase Boys (NETHERLANDS4)','data':'7'},{'value':'SteDoCo (NETHERLANDS4)','data':'16'},{'value':'HV & CV Quick (NETHERLANDS5)','data':'9'},{'value':'GVV Unitas (NETHERLANDS5)','data':'18'},{'value':'USV Hercules (NETHERLANDS5)','data':'17'},{'value':'DEM (NETHERLANDS5)','data':'16'},{'value':'Groene Ster (NETHERLANDS5)','data':'15'},{'value':'EVV (NETHERLANDS5)','data':'14'},{'value':'HSC 21 (NETHERLANDS5)','data':'13'},{'value':'OSS 20 (NETHERLANDS5)','data':'12'},{'value':'Hoogland (NETHERLANDS5)','data':'1'},{'value':'Westlandia (NETHERLANDS5)','data':'10'},{'value':'UNA (NETHERLANDS5)','data':'8'},{'value':'Hollandia (NETHERLANDS5)','data':'7'},{'value':'Watergraafsmeer (NETHERLANDS5)','data':'6'},{'value':'Dongen (NETHERLANDS5)','data':'5'},{'value':'OFC Oostzaan (NETHERLANDS5)','data':'4'},{'value':'ADO 20 (NETHERLANDS5)','data':'3'},{'value':'Gemert (NETHERLANDS5)','data':'2'},{'value':'Blauw Geel 38 (NETHERLANDS5)','data':'11'},{'value':'PEC Zwolle W (NETHERLANDS6)','data':'2'},{'value':'PSV Eindhoven W (NETHERLANDS6)','data':'1'},{'value':'Alkmaar W (NETHERLANDS6)','data':'4'},{'value':'Excelsior W (NETHERLANDS6)','data':'5'},{'value':'ADO Den Haag W (NETHERLANDS6)','data':'7'},{'value':'Heerenveen W (NETHERLANDS6)','data':'9'},{'value':'Ajax W (NETHERLANDS6)','data':'6'},{'value':'FC Twente W (NETHERLANDS6)','data':'3'},{'value':'Feyenoord W (NETHERLANDS6)','data':'8'},{'value':'Wellington P. B (NEWZEALAND)','data':'3'},{'value':'Waitakere Utd (NEWZEALAND)','data':'2'},{'value':'Eastern Suburbs (NEWZEALAND)','data':'8'},{'value':'Team Wellington (NEWZEALAND)','data':'4'},{'value':'Hawke`s Bay (NEWZEALAND)','data':'5'},{'value':'Hamilton (NEWZEALAND)','data':'6'},{'value':'Auckland City (NEWZEALAND)','data':'7'},{'value':'Canterbury Utd (NEWZEALAND)','data':'1'},{'value':'Juventus M. (NICARAGUA)','data':'8'},{'value':'Jalapa (NICARAGUA)','data':'9'},{'value':'Real Esteli (NICARAGUA)','data':'5'},{'value':'D. Ocotal (NICARAGUA)','data':'10'},{'value':'Walter Ferreti (NICARAGUA)','data':'3'},{'value':'Real Madriz (NICARAGUA)','data':'4'},{'value':'Diriangen (NICARAGUA)','data':'1'},{'value':'UNAN Managua (NICARAGUA)','data':'2'},{'value':'Export Sebaco (NICARAGUA)','data':'6'},{'value':'Managua FC (NICARAGUA)','data':'7'},{'value':'Junior Managua (NICARAGUA2)','data':'1'},{'value':'Chinandega (NICARAGUA2)','data':'7'},{'value':'Managua FC U20 (NICARAGUA3)','data':'3'},{'value':'W. Ferretti U20 (NICARAGUA3)','data':'5'},{'value':'Real Madriz U20 (NICARAGUA3)','data':'6'},{'value':'Real Esteli U20 (NICARAGUA3)','data':'7'},{'value':'Export S. U20 (NICARAGUA3)','data':'8'},{'value':'Diriangen U20 (NICARAGUA3)','data':'1'},{'value':'UNAN M. U20 (NICARAGUA3)','data':'2'},{'value':'Juventus M. U20 (NICARAGUA3)','data':'4'},{'value':'M. Jalapa U20 (NICARAGUA3)','data':'9'},{'value':'D. Ocotal U20 (NICARAGUA3)','data':'10'},{'value':'Chinandega U20 (NICARAGUA4)','data':'7'},{'value':'CD Junior U20 (NICARAGUA4)','data':'1'},{'value':'Adamawa Utd (NIGERIA)','data':'1'},{'value':'Abia Warriors (NIGERIA)','data':'18'},{'value':'Lobi Stars (NIGERIA)','data':'10'},{'value':'MFM (NIGERIA)','data':'11'},{'value':'Warri Wolves (NIGERIA)','data':'12'},{'value':'Jigawa G. Stars (NIGERIA)','data':'7'},{'value':'Akwa Utd (NIGERIA)','data':'13'},{'value':'Akwa Starlets (NIGERIA)','data':'14'},{'value':'Katsina Utd (NIGERIA)','data':'15'},{'value':'Enugu Rangers (NIGERIA)','data':'20'},{'value':'Enyimba (NIGERIA)','data':'17'},{'value':'Kano Pillars (NIGERIA)','data':'2'},{'value':'Sunshine Stars (NIGERIA)','data':'8'},{'value':'Rivers Utd (NIGERIA)','data':'19'},{'value':'Jigawa Golden S (NIGERIA)','data':'7'},{'value':'Kwara Utd (NIGERIA)','data':'6'},{'value':'Plateau Utd (NIGERIA)','data':'5'},{'value':'Wikki Tourist (NIGERIA)','data':'4'},{'value':'Nasarawa Utd (NIGERIA)','data':'3'},{'value':'Heartland (NIGERIA)','data':'16'},{'value':'Ifeanyi Uba (NIGERIA)','data':'9'},{'value':'Crusaders (NORTHERNIRELAND)','data':'10'},{'value':'Coleraine (NORTHERNIRELAND)','data':'8'},{'value':'Ballymena Utd (NORTHERNIRELAND)','data':'12'},{'value':'Cliftonville (NORTHERNIRELAND)','data':'3'},{'value':'Glentoran (NORTHERNIRELAND)','data':'6'},{'value':'Larne (NORTHERNIRELAND)','data':'7'},{'value':'Dungannon (NORTHERNIRELAND)','data':'5'},{'value':'Linfield (NORTHERNIRELAND)','data':'9'},{'value':'Warrenpoint (NORTHERNIRELAND)','data':'11'},{'value':'Glenavon (NORTHERNIRELAND)','data':'2'},{'value':'Portadown (NORTHERNIRELAND)','data':'1'},{'value':'Carrick Rangers (NORTHERNIRELAND)','data':'4'},{'value':'Ards (NORTHERNIRELAND2)','data':'2'},{'value':'Queens U (NORTHERNIRELAND2)','data':'11'},{'value':'Knockbreda (NORTHERNIRELAND2)','data':'10'},{'value':'Annagh Utd (NORTHERNIRELAND2)','data':'1'},{'value':'Newry City (NORTHERNIRELAND2)','data':'9'},{'value':'Dergview (NORTHERNIRELAND2)','data':'5'},{'value':'H&W Welders (NORTHERNIRELAND2)','data':'12'},{'value':'Ballyclare (NORTHERNIRELAND2)','data':'3'},{'value':'Institute (NORTHERNIRELAND2)','data':'6'},{'value':'Ballinamallard  (NORTHERNIRELAND2)','data':'4'},{'value':'Dundela (NORTHERNIRELAND2)','data':'8'},{'value':'Loughgall (NORTHERNIRELAND2)','data':'7'},{'value':'Cliftonville W (NORTHERNIRELAND3)','data':'2'},{'value':'Derry City W (NORTHERNIRELAND3)','data':'1'},{'value':'Linfield W (NORTHERNIRELAND3)','data':'5'},{'value':'Sion Swifts W (NORTHERNIRELAND3)','data':'6'},{'value':'Crusaders W (NORTHERNIRELAND3)','data':'4'},{'value':'Glentoran W (NORTHERNIRELAND3)','data':'3'},{'value':'A. Pandev (NORTHMACEDONIA)','data':'11'},{'value':'Struga (NORTHMACEDONIA)','data':'12'},{'value':'Shkupi (NORTHMACEDONIA)','data':'6'},{'value':'Rabotnicki (NORTHMACEDONIA)','data':'1'},{'value':'Makedonija (NORTHMACEDONIA)','data':'7'},{'value':'FK Skopje (NORTHMACEDONIA)','data':'10'},{'value':'Pelister (NORTHMACEDONIA)','data':'8'},{'value':'Skendija (NORTHMACEDONIA)','data':'4'},{'value':'Bregalnica Stip (NORTHMACEDONIA)','data':'5'},{'value':'Borec (NORTHMACEDONIA)','data':'2'},{'value':'Tikves (NORTHMACEDONIA)','data':'3'},{'value':'Renova (NORTHMACEDONIA)','data':'9'},{'value':'Kadino Skopje (NORTHMACEDONIA2)','data':'1'},{'value':'Belasica (NORTHMACEDONIA2)','data':'20'},{'value':'Korab (NORTHMACEDONIA2)','data':'9'},{'value':'Teteks (NORTHMACEDONIA2)','data':'19'},{'value':'Velazerimi (NORTHMACEDONIA2)','data':'18'},{'value':'Drita (NORTHMACEDONIA2)','data':'15'},{'value':'Veleshta (NORTHMACEDONIA2)','data':'6'},{'value':'Vardar (NORTHMACEDONIA2)','data':'10'},{'value':'Pobeda (NORTHMACEDONIA2)','data':'17'},{'value':'Pehchevo (NORTHMACEDONIA2)','data':'18'},{'value':'Rosoman (NORTHMACEDONIA2)','data':'3'},{'value':'Sloga Vinica (NORTHMACEDONIA2)','data':'11'},{'value':'Sasa (NORTHMACEDONIA2)','data':'14'},{'value':'Vardari Forino (NORTHMACEDONIA2)','data':'16'},{'value':'Teteks (NORTHMACEDONIA2)','data':'5'},{'value':'Sileks (NORTHMACEDONIA2)','data':'2'},{'value':'Detonit Junior (NORTHMACEDONIA2)','data':'19'},{'value':'Tim Lokomotiva (NORTHMACEDONIA2)','data':'15'},{'value':'Voska Sport (NORTHMACEDONIA2)','data':'8'},{'value':'Besa Dobërdoll (NORTHMACEDONIA2)','data':'4'},{'value':'Osogovo (NORTHMACEDONIA2)','data':'13'},{'value':'Gostivar (NORTHMACEDONIA2)','data':'7'},{'value':'Ohrid (NORTHMACEDONIA2)','data':'3'},{'value':'K. Gevgelija (NORTHMACEDONIA2)','data':'16'},{'value':'Plackovica (NORTHMACEDONIA2)','data':'7'},{'value':'Bratstvo Zitose (NORTHMACEDONIA2)','data':'12'},{'value':'Valerenga (NORWAY)','data':'15'},{'value':'Rosenborg (NORWAY)','data':'11'},{'value':'Lillestrom (NORWAY)','data':'8'},{'value':'Molde (NORWAY)','data':'16'},{'value':'Viking (NORWAY)','data':'14'},{'value':'Sarpsborg 08 (NORWAY)','data':'13'},{'value':'Stromsgodset (NORWAY)','data':'12'},{'value':'Sandefjord (NORWAY)','data':'10'},{'value':'Mjondalen (NORWAY)','data':'9'},{'value':'Tromso (NORWAY)','data':'6'},{'value':'Haugesund (NORWAY)','data':'5'},{'value':'Brann (NORWAY)','data':'4'},{'value':'Bodo / Glimt (NORWAY)','data':'3'},{'value':'Odd (NORWAY)','data':'2'},{'value':'Stabaek (NORWAY)','data':'1'},{'value':'Kristiansund (NORWAY)','data':'7'},{'value':'Valerenga W (NORWAY11)','data':'7'},{'value':'Lyn W (NORWAY11)','data':'9'},{'value':'LSK Kvinner W (NORWAY11)','data':'10'},{'value':'Klepp W (NORWAY11)','data':'1'},{'value':'Arna-Bjornar W (NORWAY11)','data':'2'},{'value':'Sandviken W (NORWAY11)','data':'3'},{'value':'Rosenborg W (NORWAY11)','data':'5'},{'value':'Stabaek W (NORWAY11)','data':'6'},{'value':'Avaldsnes W (NORWAY11)','data':'8'},{'value':'Kolbotn W (NORWAY11)','data':'4'},{'value':'Medkila W (NORWAY12)','data':'8'},{'value':'O. Hosle W (NORWAY12)','data':'1'},{'value':'Grei W (NORWAY12)','data':'2'},{'value':'Roa W (NORWAY12)','data':'3'},{'value':'A. Grimstad W (NORWAY12)','data':'4'},{'value':'Honefoss W (NORWAY12)','data':'5'},{'value':'Fart W (NORWAY12)','data':'7'},{'value':'Floya W (NORWAY12)','data':'9'},{'value':'KIL / Hemne W (NORWAY12)','data':'10'},{'value':'Asane W (NORWAY12)','data':'6'},{'value':'Strommen (NORWAY2)','data':'13'},{'value':'Raufoss (NORWAY2)','data':'14'},{'value':'Sandnes Ulf (NORWAY2)','data':'15'},{'value':'Fredrikstad (NORWAY2)','data':'10'},{'value':'Sogndal (NORWAY2)','data':'11'},{'value':'Ullensaker / K. (NORWAY2)','data':'12'},{'value':'Ranheim (NORWAY2)','data':'7'},{'value':'Bryne (NORWAY2)','data':'2'},{'value':'HamKam (NORWAY2)','data':'3'},{'value':'Stjordals-Blink (NORWAY2)','data':'4'},{'value':'Aalesund (NORWAY2)','data':'1'},{'value':'KFUM Oslo (NORWAY2)','data':'6'},{'value':'Grorud (NORWAY2)','data':'8'},{'value':'Start (NORWAY2)','data':'16'},{'value':'Asane (NORWAY2)','data':'9'},{'value':'Jerv (NORWAY2)','data':'5'},{'value':'Eidsvold (NORWAY3)','data':'6'},{'value':'Floya (NORWAY3)','data':'11'},{'value':'Floro (NORWAY3)','data':'1'},{'value':'Asker (NORWAY3)','data':'5'},{'value':'Baerum (NORWAY3)','data':'10'},{'value':'Brattvag (NORWAY3)','data':'9'},{'value':'Alta (NORWAY3)','data':'7'},{'value':'Kongsvinger (NORWAY3)','data':'12'},{'value':'Tromsdalen (NORWAY3)','data':'4'},{'value':'Senja (NORWAY3)','data':'3'},{'value':'Kvik Halden (NORWAY3)','data':'2'},{'value':'Moss (NORWAY3)','data':'14'},{'value':'Valerenga B (NORWAY3)','data':'13'},{'value':'Hodd (NORWAY3)','data':'8'},{'value':'Levanger (NORWAY4)','data':'10'},{'value':'Fram (NORWAY4)','data':'14'},{'value':'Rosenborg B (NORWAY4)','data':'13'},{'value':'Sotra (NORWAY4)','data':'11'},{'value':'Skeid (NORWAY4)','data':'1'},{'value':'Odd B (NORWAY4)','data':'9'},{'value':'Oygarden (NORWAY4)','data':'8'},{'value':'Arendal (NORWAY4)','data':'7'},{'value':'Egersund (NORWAY4)','data':'6'},{'value':'Flekkeroy (NORWAY4)','data':'5'},{'value':'Notodden (NORWAY4)','data':'4'},{'value':'Vard (NORWAY4)','data':'3'},{'value':'Nardo (NORWAY4)','data':'2'},{'value':'Kjelsas (NORWAY4)','data':'12'},{'value':'Oman Club (OMAN)','data':'13'},{'value':'Muscat (OMAN)','data':'9'},{'value':'Al-Rustaq (OMAN)','data':'12'},{'value':'Bahla (OMAN)','data':'14'},{'value':'Al Suwaiq (OMAN)','data':'8'},{'value':'Sohar (OMAN)','data':'7'},{'value':'Dhofar (OMAN)','data':'10'},{'value':'Al-Ittihad (OMAN)','data':'11'},{'value':'Al-Nahda (OMAN)','data':'5'},{'value':'Nizwa (OMAN)','data':'1'},{'value':'Al Seeb (OMAN)','data':'4'},{'value':'Al-Musannah (OMAN)','data':'6'},{'value':'Al Nasr (OMAN)','data':'2'},{'value':'Saham (OMAN)','data':'3'},{'value':'Markaz Tulkarm (PALESTINE)','data':'2'},{'value':'Markez Balata (PALESTINE)','data':'4'},{'value':'T. Wadi Al-Nes (PALESTINE)','data':'5'},{'value':'J. Al Mukaber (PALESTINE)','data':'1'},{'value':'Islami Kalkelea (PALESTINE)','data':'5'},{'value':'S. Al Khaleel (PALESTINE)','data':'11'},{'value':'Al-Birah (PALESTINE)','data':'3'},{'value':'Ahli Al-Khalil (PALESTINE)','data':'10'},{'value':'Tubas (PALESTINE)','data':'7'},{'value':'Shabab Alsamu (PALESTINE)','data':'8'},{'value':'Hilal Al-Quds (PALESTINE)','data':'12'},{'value':'Thagafi Tulkarm (PALESTINE)','data':'6'},{'value':'S. Al Amari (PALESTINE)','data':'10'},{'value':'S. Al-Dhahiriya (PALESTINE)','data':'9'},{'value':'Herrera (PANAMA2)','data':'4'},{'value':'Plaza Amador (PANAMA2)','data':'2'},{'value':'Veraguas (PANAMA2)','data':'8'},{'value':'San Francisco (PANAMA2)','data':'6'},{'value':'San Miguelito (PANAMA2)','data':'9'},{'value':'A. Chiriqui (PANAMA2)','data':'5'},{'value':'Costa del Este (PANAMA2)','data':'11'},{'value':'Tauro (PANAMA2)','data':'1'},{'value':'Independiente (PANAMA2)','data':'3'},{'value':'Arabe Unido (PANAMA2)','data':'12'},{'value':'Universitario (PANAMA2)','data':'7'},{'value':'Alianza (PANAMA2)','data':'10'},{'value':'Olimpia (PARAGUAY2)','data':'1'},{'value':'Nacional (PARAGUAY2)','data':'8'},{'value':'Sol de America (PARAGUAY2)','data':'10'},{'value':'Guarani (PARAGUAY2)','data':'9'},{'value':'Libertad (PARAGUAY2)','data':'3'},{'value':'Guairena (PARAGUAY2)','data':'4'},{'value':'12 de Octubre (PARAGUAY2)','data':'7'},{'value':'Cerro Porteno (PARAGUAY2)','data':'6'},{'value':'Sport. Luqueno (PARAGUAY2)','data':'5'},{'value':'C. River Plate (PARAGUAY2)','data':'2'},{'value':'S. Ameliano (PARAGUAY3)','data':'11'},{'value':'General Diaz (PARAGUAY3)','data':'16'},{'value':'San Lorenzo (PARAGUAY3)','data':'6'},{'value':'Independiente (PARAGUAY3)','data':'18'},{'value':'D. Capiata (PARAGUAY3)','data':'17'},{'value':'Resistencia (PARAGUAY3)','data':'15'},{'value':'Rubio Nu (PARAGUAY3)','data':'14'},{'value':'2 de Mayo (PARAGUAY3)','data':'1'},{'value':'G. Caballero (PARAGUAY3)','data':'12'},{'value':'Sportivo Iteno (PARAGUAY3)','data':'10'},{'value':'Tacuary (PARAGUAY3)','data':'9'},{'value':'D. Santani (PARAGUAY3)','data':'8'},{'value':'S. Trinidense (PARAGUAY3)','data':'7'},{'value':'F. de la Mora (PARAGUAY3)','data':'5'},{'value':'Fulgencio Y. (PARAGUAY3)','data':'4'},{'value':'3 de Febrero (PARAGUAY3)','data':'3'},{'value':'G. de Trinidad (PARAGUAY3)','data':'2'},{'value':'Atyra (PARAGUAY3)','data':'13'},{'value':'Alianza A. (PERU2)','data':'18'},{'value':'A. Huanuco (PERU2)','data':'14'},{'value':'Cusco (PERU2)','data':'16'},{'value':'Cesar Vallejo (PERU2)','data':'15'},{'value':'Sport Boys (PERU2)','data':'9'},{'value':'FBC Melgar (PERU2)','data':'8'},{'value':'Universitario (PERU2)','data':'17'},{'value':'Cajamarca (PERU2)','data':'2'},{'value':'Cienciano (PERU2)','data':'10'},{'value':'U. San Martin (PERU2)','data':'3'},{'value':'Ayacucho (PERU2)','data':'12'},{'value':'AD Cantolao (PERU2)','data':'5'},{'value':'Binacional (PERU2)','data':'13'},{'value':'Sport Huancayo (PERU2)','data':'7'},{'value':'S. Cristal (PERU2)','data':'6'},{'value':'Alianza Lima (PERU2)','data':'11'},{'value':'Carlos Manucci (PERU2)','data':'4'},{'value':'D. Municipal (PERU2)','data':'1'},{'value':'Huaral (PERU4)','data':'2'},{'value':'Llacuabamba (PERU4)','data':'5'},{'value':'Juan Aurich (PERU4)','data':'12'},{'value':'Carlos Stein (PERU4)','data':'6'},{'value':'Atletico Grau (PERU4)','data':'7'},{'value':'Santa Rosa (PERU4)','data':'3'},{'value':'D. Coopsol (PERU4)','data':'10'},{'value':'Santos FC (PERU4)','data':'1'},{'value':'S. Chavelines (PERU4)','data':'8'},{'value':'Comerciantes U. (PERU4)','data':'9'},{'value':'M. El Pirata (PERU4)','data':'11'},{'value':'Union Comercio (PERU4)','data':'4'},{'value':'Pogon Szczecin (POLAND)','data':'15'},{'value':'Cracovia Krakow (POLAND)','data':'6'},{'value':'Jagiellonia (POLAND)','data':'7'},{'value':'Piast Gliwice (POLAND)','data':'11'},{'value':'Wisla Krakow (POLAND)','data':'17'},{'value':'Lech Poznan (POLAND)','data':'3'},{'value':'Radomiak Radom (POLAND)','data':'4'},{'value':'Slask Wroclaw (POLAND)','data':'13'},{'value':'Gornik Leczna (POLAND)','data':'5'},{'value':'Gornik Zabrze (POLAND)','data':'16'},{'value':'Lechia Gdansk (POLAND)','data':'8'},{'value':'Warta Poznan (POLAND)','data':'14'},{'value':'Stal Mielec (POLAND)','data':'2'},{'value':'Wisla Plock (POLAND)','data':'10'},{'value':'Legia Warsaw (POLAND)','data':'9'},{'value':'Rakow C. (POLAND)','data':'12'},{'value':'Nieciecza (POLAND)','data':'1'},{'value':'Zaglebie Lubin (POLAND)','data':'18'},{'value':'Miedz Legnica (POLAND2)','data':'2'},{'value':'Chrobry Glogow (POLAND2)','data':'18'},{'value':'Z. Sosnowiec (POLAND2)','data':'12'},{'value':'Sandecja Nowy (POLAND2)','data':'14'},{'value':'Stomil Olsztyn (POLAND2)','data':'17'},{'value':'Tychy (POLAND2)','data':'5'},{'value':'Resovia Rzeszow (POLAND2)','data':'8'},{'value':'Puszcza Niepolo (POLAND2)','data':'10'},{'value':'Jastrzebie (POLAND2)','data':'9'},{'value':'Korona Kielce (POLAND2)','data':'3'},{'value':'Odra Opole (POLAND2)','data':'1'},{'value':'Katowice (POLAND2)','data':'7'},{'value':'Widzew Lodz (POLAND2)','data':'13'},{'value':'LKS Lodz (POLAND2)','data':'6'},{'value':'Arka Gdynia (POLAND2)','data':'11'},{'value':'Polkowice (POLAND2)','data':'15'},{'value':'Podbeskidzie (POLAND2)','data':'16'},{'value':'SKRA Czestochow (POLAND2)','data':'4'},{'value':'Sokol Ostroda (POLAND3)','data':'9'},{'value':'Lech Poznan B (POLAND3)','data':'4'},{'value':'Slask Wroclaw B (POLAND3)','data':'15'},{'value':'Belchatow (POLAND3)','data':'12'},{'value':'Motor Lublin (POLAND3)','data':'6'},{'value':'Pogon Grodzisk  (POLAND3)','data':'10'},{'value':'Radunia Stezyca (POLAND3)','data':'3'},{'value':'Hutnik Krakow (POLAND3)','data':'16'},{'value':'Znicz Pruszkow (POLAND3)','data':'5'},{'value':'Garbarnia (POLAND3)','data':'14'},{'value':'Ruch Chorzów (POLAND3)','data':'1'},{'value':'Stargard Szczec (POLAND3)','data':'10'},{'value':'Wisla Pulawy (POLAND3)','data':'11'},{'value':'Kalisz (POLAND3)','data':'7'},{'value':'Bytovia Bytow (POLAND3)','data':'11'},{'value':'O. Grudziadz (POLAND3)','data':'12'},{'value':'Pogon Siedlce (POLAND3)','data':'2'},{'value':'Chojniczanka (POLAND3)','data':'18'},{'value':'Olimpia Elblag (POLAND3)','data':'8'},{'value':'Suwalki (POLAND3)','data':'17'},{'value':'Stal Rzeszow (POLAND3)','data':'13'},{'value':'Bron Radom (POLAND4)','data':'14'},{'value':'Polonia Warszaw (POLAND4)','data':'6'},{'value':'Olimpia Zambrów (POLAND4)','data':'7'},{'value':'Bydgoszcz W (POLAND4)','data':'10'},{'value':'Unia Skierniewi (POLAND4)','data':'8'},{'value':'Swit (POLAND4)','data':'9'},{'value':'Concordia Elbla (POLAND4)','data':'10'},{'value':'Blonianka Bloni (POLAND4)','data':'11'},{'value':'Ruch Wysokie Ma (POLAND4)','data':'15'},{'value':'Pelikan Lowicz (POLAND4)','data':'13'},{'value':'Wasilków (POLAND4)','data':'4'},{'value':'Huragan Morag (POLAND4)','data':'16'},{'value':'Rekord Bielsko- (POLAND4)','data':'3'},{'value':'Tarnovia Tarnów (POLAND4)','data':'9'},{'value':'Ursus Warszawa (POLAND4)','data':'12'},{'value':'Leczna W (POLAND4)','data':'7'},{'value':'Jagiellonia II (POLAND4)','data':'1'},{'value':'UKS Lodz W (POLAND4)','data':'5'},{'value':'O. Szczecin W (POLAND4)','data':'2'},{'value':'C. Sosnowiec W (POLAND4)','data':'12'},{'value':'GKS Katowice W (POLAND4)','data':'8'},{'value':'Medyk Konin W (POLAND4)','data':'1'},{'value':'ROW Rybnik W (POLAND4)','data':'7'},{'value':'Slask Wroclaw W (POLAND4)','data':'6'},{'value':'Rolnik B. W (POLAND4)','data':'9'},{'value':'Kutno (POLAND4)','data':'5'},{'value':'L. Gdansk W (POLAND4)','data':'11'},{'value':'Znicz Biala Pis (POLAND4)','data':'2'},{'value':'Lechia T. Mazow (POLAND4)','data':'21'},{'value':'Sokól Aleksandr (POLAND4)','data':'20'},{'value':'Wikielec (POLAND4)','data':'3'},{'value':'Legia Warszawa  (POLAND4)','data':'18'},{'value':'Rks Radomsko (POLAND4)','data':'17'},{'value':'UJ Krakow W (POLAND4)','data':'4'},{'value':'Famalicao (PORTUGAL)','data':'16'},{'value':'Benfica (PORTUGAL)','data':'6'},{'value':'Vizela (PORTUGAL)','data':'2'},{'value':'Guimaraes (PORTUGAL)','data':'9'},{'value':'FC Porto (PORTUGAL)','data':'13'},{'value':'Moreirense (PORTUGAL)','data':'5'},{'value':'Tondela (PORTUGAL)','data':'11'},{'value':'Portimonense (PORTUGAL)','data':'10'},{'value':'Pacos Ferreira (PORTUGAL)','data':'15'},{'value':'Santa Clara (PORTUGAL)','data':'12'},{'value':'Estoril (PORTUGAL)','data':'4'},{'value':'Sporting Braga (PORTUGAL)','data':'8'},{'value':'Gil Vicente (PORTUGAL)','data':'17'},{'value':'Sporting CP (PORTUGAL)','data':'1'},{'value':'Boavista (PORTUGAL)','data':'18'},{'value':'Maritimo (PORTUGAL)','data':'7'},{'value':'Belenenses (PORTUGAL)','data':'14'},{'value':'Arouca (PORTUGAL)','data':'3'},{'value':'Farense (PORTUGAL2)','data':'18'},{'value':'Estrela Amadora (PORTUGAL2)','data':'9'},{'value':'Trofense (PORTUGAL2)','data':'6'},{'value':'Nacional (PORTUGAL2)','data':'14'},{'value':'Rio Ave (PORTUGAL2)','data':'11'},{'value':'Leixoes (PORTUGAL2)','data':'17'},{'value':'Cova Piedade (PORTUGAL2)','data':'5'},{'value':'Mafra (PORTUGAL2)','data':'10'},{'value':'Academica (PORTUGAL2)','data':'12'},{'value':'Academico Viseu (PORTUGAL2)','data':'1'},{'value':'Feirense (PORTUGAL2)','data':'7'},{'value':'Varzim (PORTUGAL2)','data':'3'},{'value':'Chaves (PORTUGAL2)','data':'4'},{'value':'Covilha (PORTUGAL2)','data':'8'},{'value':'Casa Pia (PORTUGAL2)','data':'2'},{'value':'Penafiel (PORTUGAL2)','data':'16'},{'value':'FC Porto B (PORTUGAL2)','data':'5'},{'value':'Benfica B (PORTUGAL2)','data':'13'},{'value':'Oliveirense (PORTUGAL2)','data':'4'},{'value':'Vilafranquense (PORTUGAL2)','data':'15'},{'value':'Al Duhail (QATAR)','data':'8'},{'value':'Qatar SC (QATAR)','data':'3'},{'value':'Al Gharafa (QATAR)','data':'1'},{'value':'Al Sailiya (QATAR)','data':'12'},{'value':'Al Sadd (QATAR)','data':'11'},{'value':'Al Kharitiyath (QATAR)','data':'1'},{'value':'Al Rayyan (QATAR)','data':'6'},{'value':'Umm Salal (QATAR)','data':'5'},{'value':'Al Wakrah (QATAR)','data':'9'},{'value':'Al Ahli (QATAR)','data':'4'},{'value':'Al Khor (QATAR)','data':'7'},{'value':'Al Shamal (QATAR)','data':'2'},{'value':'Al Arabi (QATAR)','data':'10'},{'value':'Al Shahaniya (QATAR2)','data':'1'},{'value':'Al Mesaimeer (QATAR2)','data':'5'},{'value':'Lusail City (QATAR2)','data':'2'},{'value':'Al Markhiya (QATAR2)','data':'8'},{'value':'Al Bidda (QATAR2)','data':'6'},{'value':'Al Muaidar (QATAR2)','data':'4'},{'value':'Al Waab (QATAR2)','data':'7'},{'value':'Farul Constanta (ROMANIA)','data':'12'},{'value':'U Craiova 1948 (ROMANIA)','data':'6'},{'value':'Rapid Bucharest (ROMANIA)','data':'13'},{'value':'Mioveni (ROMANIA)','data':'8'},{'value':'Din. Bucharest (ROMANIA)','data':'15'},{'value':'Univ. Craiova (ROMANIA)','data':'9'},{'value':'FCSB (ROMANIA)','data':'2'},{'value':'C. Targoviste (ROMANIA)','data':'14'},{'value':'A. Clinceni (ROMANIA)','data':'4'},{'value':'CFR Cluj (ROMANIA)','data':'5'},{'value':'UTA Arad (ROMANIA)','data':'11'},{'value':'Viitorul (ROMANIA)','data':'6'},{'value':'Botosani (ROMANIA)','data':'1'},{'value':'Arges (ROMANIA)','data':'10'},{'value':'Sepsi OSK (ROMANIA)','data':'3'},{'value':'Gaz Metan (ROMANIA)','data':'7'},{'value':'Voluntari (ROMANIA)','data':'16'},{'value':'Metaloglobus (ROMANIA2)','data':'8'},{'value':'P. Iasi (ROMANIA2)','data':'10'},{'value':'Comuna Recea (ROMANIA2)','data':'3'},{'value':'Steaua B. (ROMANIA2)','data':'19'},{'value':'Petrolul (ROMANIA2)','data':'9'},{'value':'Concordia (ROMANIA2)','data':'11'},{'value':'Brasov Steagul  (ROMANIA2)','data':'15'},{'value':'Astra (ROMANIA2)','data':'7'},{'value':'Viitorul T. J. (ROMANIA2)','data':'16'},{'value':'Aerostar Bacau (ROMANIA2)','data':'15'},{'value':'D. Calarasi (ROMANIA2)','data':'2'},{'value':'U. Cluj (ROMANIA2)','data':'17'},{'value':'Unirea Dej (ROMANIA2)','data':'3'},{'value':'Unirea Slobozia (ROMANIA2)','data':'4'},{'value':'Pandurii Targu  (ROMANIA2)','data':'10'},{'value':'R. Timisoara (ROMANIA2)','data':'1'},{'value':'ASU Poli T. (ROMANIA2)','data':'18'},{'value':'CSM Resita (ROMANIA2)','data':'20'},{'value':'Braila (ROMANIA2)','data':'6'},{'value':'FC Buzau (ROMANIA2)','data':'14'},{'value':'Unirea C. (ROMANIA2)','data':'12'},{'value':'V. Selimbar (ROMANIA2)','data':'5'},{'value':'Hermannstadt (ROMANIA2)','data':'13'},{'value':'Slatina (ROMANIA2)','data':'1'},{'value':'Turnu Magurele (ROMANIA2)','data':'8'},{'value':'Csikszereda (ROMANIA2)','data':'20'},{'value':'Banat W (ROMANIA3)','data':'3'},{'value':'SSU Poli T. W (ROMANIA3)','data':'2'},{'value':'U. Galati W (ROMANIA3)','data':'7'},{'value':'Heniu Prundu W (ROMANIA3)','data':'6'},{'value':'Vasas W (ROMANIA3)','data':'10'},{'value':'Fairplay B. W (ROMANIA3)','data':'8'},{'value':'Carmen B. W (ROMANIA3)','data':'9'},{'value':'P. Security W (ROMANIA3)','data':'11'},{'value':'O. Cluj W (ROMANIA3)','data':'12'},{'value':'S. Constanta W (ROMANIA3)','data':'5'},{'value':'U. Alexandria W (ROMANIA3)','data':'1'},{'value':'Baia Mare W (ROMANIA3)','data':'4'},{'value':'Fortuna B. W (ROMANIA3)','data':'2'},{'value':'Targoviste W (ROMANIA3)','data':'5'},{'value':'Targu Mures W (ROMANIA3)','data':'9'},{'value':'FC Krasnodar (RUSSIA)','data':'10'},{'value':'Krylya Sovetov (RUSSIA)','data':'11'},{'value':'Khimki (RUSSIA)','data':'3'},{'value':'Arsenal Tula (RUSSIA)','data':'6'},{'value':'PFC Sochi (RUSSIA)','data':'16'},{'value':'Nizhny Novgorod (RUSSIA)','data':'15'},{'value':'Lokomotiv M. (RUSSIA)','data':'5'},{'value':'Rubin Kazan (RUSSIA)','data':'7'},{'value':'Zenit (RUSSIA)','data':'4'},{'value':'FC Tambov (RUSSIA)','data':'3'},{'value':'Ural (RUSSIA)','data':'9'},{'value':'Ufa (RUSSIA)','data':'14'},{'value':'Spartak Moscow (RUSSIA)','data':'8'},{'value':'Akhmat Grozny (RUSSIA)','data':'12'},{'value':'CSKA Moscow (RUSSIA)','data':'13'},{'value':'Rostov (RUSSIA)','data':'1'},{'value':'Dinamo Moscow (RUSSIA)','data':'2'},{'value':'Kamaz (RUSSIA2)','data':'5'},{'value':'Neftekhimik (RUSSIA2)','data':'13'},{'value':'Urozhay (RUSSIA2)','data':'7'},{'value':'Veles Moscow (RUSSIA2)','data':'15'},{'value':'O.-Dolgoprudny (RUSSIA2)','data':'14'},{'value':'Fakel Voronezh (RUSSIA2)','data':'11'},{'value':'Rotor Volgograd (RUSSIA2)','data':'17'},{'value':'Yenisey (RUSSIA2)','data':'16'},{'value':'Tom Tomsk (RUSSIA2)','data':'20'},{'value':'Tekstilshchik (RUSSIA2)','data':'18'},{'value':'Spartak M. B (RUSSIA2)','data':'9'},{'value':'Akron (RUSSIA2)','data':'1'},{'value':'Orenburg (RUSSIA2)','data':'3'},{'value':'V. Astrakhan (RUSSIA2)','data':'4'},{'value':'Krasnodar B (RUSSIA2)','data':'10'},{'value':'A. Vladikavkaz (RUSSIA2)','data':'6'},{'value':'SKA Khabarovsk (RUSSIA2)','data':'2'},{'value':'Torpedo Moscow (RUSSIA2)','data':'8'},{'value':'M. Lipetsk (RUSSIA2)','data':'19'},{'value':'Baltika (RUSSIA2)','data':'12'},{'value':'Biolog (RUSSIA3)','data':'4'},{'value':'Kuban Kholding (RUSSIA3)','data':'17'},{'value':'Krasnodar C (RUSSIA3)','data':'13'},{'value':'Inter Cherkessk (RUSSIA3)','data':'17'},{'value':'Essentuki (RUSSIA3)','data':'3'},{'value':'Chernomorets N. (RUSSIA3)','data':'1'},{'value':'Mashuk (RUSSIA3)','data':'6'},{'value':'Legion Dynamo (RUSSIA3)','data':'2'},{'value':'Rotor V. B (RUSSIA3)','data':'10'},{'value':'D. Stavropol (RUSSIA3)','data':'5'},{'value':'Alaniya B (RUSSIA3)','data':'14'},{'value':'D. Makhachkala (RUSSIA3)','data':'11'},{'value':'Chayka (RUSSIA3)','data':'16'},{'value':'Tuapse (RUSSIA3)','data':'15'},{'value':'Druzhba Maikop (RUSSIA3)','data':'12'},{'value':'Anzhi (RUSSIA3)','data':'9'},{'value':'SKA Rostov (RUSSIA3)','data':'7'},{'value':'Spartak Nalchik (RUSSIA3)','data':'8'},{'value':'Forte Taganrog (RUSSIA3)','data':'13'},{'value':'Chita (RUSSIA4)','data':'22'},{'value':'Zenit Irkutsk (RUSSIA4)','data':'8'},{'value':'Shinnik (RUSSIA4)','data':'8'},{'value':'Volna N. (RUSSIA4)','data':'2'},{'value':'Chertanovo (RUSSIA4)','data':'21'},{'value':'Tver (RUSSIA4)','data':'17'},{'value':'Murom (RUSSIA4)','data':'10'},{'value':'Zvezda St. P. (RUSSIA4)','data':'11'},{'value':'Luki-Energiya (RUSSIA4)','data':'3'},{'value':'T. Vladimir (RUSSIA4)','data':'19'},{'value':'Krasava (RUSSIA4)','data':'18'},{'value':'Znamya Truda (RUSSIA4)','data':'20'},{'value':'Leningradets (RUSSIA4)','data':'15'},{'value':'Baltika BFU (RUSSIA4)','data':'12'},{'value':'Dolgoprudny B (RUSSIA4)','data':'7'},{'value':'L. Kazanka (RUSSIA4)','data':'1'},{'value':'Kairat Moskva (RUSSIA4)','data':'16'},{'value':'Smolensk (RUSSIA4)','data':'13'},{'value':'Zenit B (RUSSIA4)','data':'4'},{'value':'Yenisey B (RUSSIA4)','data':'6'},{'value':'Dinamo St. P. (RUSSIA4)','data':'14'},{'value':'Khimik Dzerzhin (RUSSIA4)','data':'5'},{'value':'Dinamo Moscow B (RUSSIA4)','data':'9'},{'value':'P. Podolsk (RUSSIA5)','data':'2'},{'value':'Khabarovsk B (RUSSIA5)','data':'22'},{'value':'Zenit Penza (RUSSIA5)','data':'20'},{'value':'S. Ramenskoye (RUSSIA5)','data':'6'},{'value':'Ryazan (RUSSIA5)','data':'12'},{'value':'Avangard Kursk (RUSSIA5)','data':'17'},{'value':'Khimki B (RUSSIA5)','data':'4'},{'value':'Sakhalin (RUSSIA5)','data':'21'},{'value':'Arsenal Tula B (RUSSIA5)','data':'11'},{'value':'D. Vladivostok (RUSSIA5)','data':'10'},{'value':'Salyut Belgorod (RUSSIA5)','data':'19'},{'value':'Znamya Noginsk (RUSSIA5)','data':'15'},{'value':'M. Vidnoye (RUSSIA5)','data':'8'},{'value':'Khimik-Arsenal (RUSSIA5)','data':'3'},{'value':'Sokol Saratov (RUSSIA5)','data':'13'},{'value':'Kvant (RUSSIA5)','data':'5'},{'value':'Dinamo Bryansk (RUSSIA5)','data':'14'},{'value':'Kaluga (RUSSIA5)','data':'18'},{'value':'Kolomna (RUSSIA5)','data':'7'},{'value':'Saransk (RUSSIA5)','data':'3'},{'value':'Krasnyy-SGAFKST (RUSSIA5)','data':'9'},{'value':'Rodina Moscow (RUSSIA5)','data':'1'},{'value':'F. Voronezh B (RUSSIA5)','data':'9'},{'value':'Strogino (RUSSIA5)','data':'16'},{'value':'Krylya S. B (RUSSIA6)','data':'8'},{'value':'Irtysh Omsk (RUSSIA6)','data':'11'},{'value':'Zenit Izhevsk (RUSSIA6)','data':'12'},{'value':'Tyumen (RUSSIA6)','data':'15'},{'value':'L. Dimitrovgrad (RUSSIA6)','data':'13'},{'value':'Chelyabinsk (RUSSIA6)','data':'2'},{'value':'L. Tolyatti (RUSSIA6)','data':'1'},{'value':'Volga Ulyanovsk (RUSSIA6)','data':'7'},{'value':'Spartak Tuymazy (RUSSIA6)','data':'4'},{'value':'Dinamo Barnaul (RUSSIA6)','data':'9'},{'value':'Nosta (RUSSIA6)','data':'3'},{'value':'Novosibirsk (RUSSIA6)','data':'14'},{'value':'Orenburg B (RUSSIA6)','data':'5'},{'value':'Zvezda Perm (RUSSIA6)','data':'13'},{'value':'Amkar Perm (RUSSIA6)','data':'10'},{'value':'Torpedo Miass (RUSSIA6)','data':'6'},{'value':'Ural B (RUSSIA6)','data':'8'},{'value':'Ufa U19 (RUSSIA7)','data':'11'},{'value':'Strogino U19 (RUSSIA7)','data':'12'},{'value':'K. Sovetov U19 (RUSSIA7)','data':'15'},{'value':'Nizhny Novgorod (RUSSIA7)','data':'7'},{'value':'Rostov U19 (RUSSIA7)','data':'3'},{'value':'Rubin Kazan U19 (RUSSIA7)','data':'8'},{'value':'Krasnodar U19 (RUSSIA7)','data':'20'},{'value':'Zenit U19 (RUSSIA7)','data':'18'},{'value':'UOR U19 (RUSSIA7)','data':'10'},{'value':'Sochi U19 (RUSSIA7)','data':'4'},{'value':'Tambov U19 (RUSSIA7)','data':'15'},{'value':'Rotor V. U19 (RUSSIA7)','data':'14'},{'value':'Ural U19 (RUSSIA7)','data':'5'},{'value':'L. Moscow U19 (RUSSIA7)','data':'19'},{'value':'Rostov U19 (RUSSIA7)','data':'20'},{'value':'Khimki U19 (RUSSIA7)','data':'9'},{'value':'A. Grozny U19 (RUSSIA7)','data':'17'},{'value':'Arsenal T. U19 (RUSSIA7)','data':'2'},{'value':'Spartak M. U19 (RUSSIA7)','data':'6'},{'value':'CSKA Moscow U19 (RUSSIA7)','data':'14'},{'value':'A. Konoplev U19 (RUSSIA7)','data':'16'},{'value':'Chertanovo U19 (RUSSIA7)','data':'1'},{'value':'D. Moscow U19 (RUSSIA7)','data':'13'},{'value':'Yenisey W (RUSSIA8)','data':'1'},{'value':'Zvezda 2005 W (RUSSIA8)','data':'2'},{'value':'CSKA Moscow W (RUSSIA8)','data':'4'},{'value':'Lokomotiv M. W (RUSSIA8)','data':'5'},{'value':'Krasnodar W (RUSSIA8)','data':'6'},{'value':'Chertanovo W (RUSSIA8)','data':'7'},{'value':'Rubin Kazan W (RUSSIA8)','data':'8'},{'value':'Zenit W (RUSSIA8)','data':'9'},{'value':'Ryazan VDV W (RUSSIA8)','data':'10'},{'value':'Rostov W (RUSSIA8)','data':'3'},{'value':'Kiyovu Sports (RWANDA)','data':'10'},{'value':'Rayon Sports (RWANDA)','data':'16'},{'value':'Etincelles (RWANDA)','data':'8'},{'value':'Muhanga (RWANDA)','data':'7'},{'value':'Mukura (RWANDA)','data':'9'},{'value':'Sunrise (RWANDA)','data':'11'},{'value':'Gasogi Utd (RWANDA)','data':'12'},{'value':'Espoir (RWANDA)','data':'13'},{'value':'AS Kigali (RWANDA)','data':'1'},{'value':'Police Rwanda (RWANDA)','data':'2'},{'value':'Rutsiro (RWANDA)','data':'15'},{'value':'Bugesera (RWANDA)','data':'14'},{'value':'APR (RWANDA)','data':'3'},{'value':'Musanze (RWANDA)','data':'4'},{'value':'Marines (RWANDA)','data':'5'},{'value':'Gorilla (RWANDA)','data':'6'},{'value':'Al Ittifaq (SAUDIARABIA)','data':'13'},{'value':'Al Ittihad (SAUDIARABIA)','data':'2'},{'value':'Al Taawon (SAUDIARABIA)','data':'8'},{'value':'Abha (SAUDIARABIA)','data':'3'},{'value':'Al Hilal (SAUDIARABIA)','data':'15'},{'value':'Al Batin (SAUDIARABIA)','data':'14'},{'value':'Al Ahli Jeddah (SAUDIARABIA)','data':'11'},{'value':'Al Nassr (SAUDIARABIA)','data':'9'},{'value':'Al Fateh (SAUDIARABIA)','data':'6'},{'value':'Damak (SAUDIARABIA)','data':'10'},{'value':'Al Faisaly (SAUDIARABIA)','data':'12'},{'value':'Al Hazm (SAUDIARABIA)','data':'7'},{'value':'Al Shabab (SAUDIARABIA)','data':'4'},{'value':'Al Feiha (SAUDIARABIA)','data':'1'},{'value':'Al Raed (SAUDIARABIA)','data':'5'},{'value':'Al Taeee (SAUDIARABIA)','data':'16'},{'value':'Al Adalh (SAUDIARABIA2)','data':'1'},{'value':'Al Bukayriyah (SAUDIARABIA2)','data':'14'},{'value':'Al Jabalain (SAUDIARABIA2)','data':'12'},{'value':'Al Kholood (SAUDIARABIA2)','data':'8'},{'value':'Jeddah (SAUDIARABIA2)','data':'5'},{'value':'Al Sahel (SAUDIARABIA2)','data':'16'},{'value':'Al Orubah (SAUDIARABIA2)','data':'11'},{'value':'Al Akhdoud (SAUDIARABIA2)','data':'18'},{'value':'Al Najoom (SAUDIARABIA2)','data':'18'},{'value':'Najran (SAUDIARABIA2)','data':'3'},{'value':'Bisha (SAUDIARABIA2)','data':'9'},{'value':'Al Draih (SAUDIARABIA2)','data':'6'},{'value':'Al Wahda (SAUDIARABIA2)','data':'17'},{'value':'Al Quadisiya (SAUDIARABIA2)','data':'13'},{'value':'Al Jeel (SAUDIARABIA2)','data':'20'},{'value':'Al-Ain (SAUDIARABIA2)','data':'10'},{'value':'Ohod (SAUDIARABIA2)','data':'4'},{'value':'Arar (SAUDIARABIA2)','data':'8'},{'value':'Al Nahdha (SAUDIARABIA2)','data':'14'},{'value':'Al Khaleej (SAUDIARABIA2)','data':'19'},{'value':'Hajer (SAUDIARABIA2)','data':'7'},{'value':'Al Shoalah (SAUDIARABIA2)','data':'15'},{'value':'Al-Thuqbah (SAUDIARABIA2)','data':'3'},{'value':'Al-Kawkab (SAUDIARABIA2)','data':'2'},{'value':'St. Johnstone (SCOTLAND)','data':'6'},{'value':'Dundee FC (SCOTLAND)','data':'3'},{'value':'Motherwell (SCOTLAND)','data':'11'},{'value':'Hearts (SCOTLAND)','data':'7'},{'value':'Ross County (SCOTLAND)','data':'5'},{'value':'Hibernian (SCOTLAND)','data':'12'},{'value':'Aberdeen (SCOTLAND)','data':'9'},{'value':'Livingston (SCOTLAND)','data':'2'},{'value':'Celtic (SCOTLAND)','data':'8'},{'value':'Dundee Utd (SCOTLAND)','data':'10'},{'value':'St. Mirren (SCOTLAND)','data':'4'},{'value':'Rangers (SCOTLAND)','data':'1'},{'value':'Ayr Utd (SCOTLAND2)','data':'10'},{'value':'Queen of South (SCOTLAND2)','data':'6'},{'value':'Dunfermline (SCOTLAND2)','data':'4'},{'value':'Inverness (SCOTLAND2)','data':'2'},{'value':'Hamilton (SCOTLAND2)','data':'8'},{'value':'Raith Rovers (SCOTLAND2)','data':'7'},{'value':'Arbroath (SCOTLAND2)','data':'1'},{'value':'Kilmarnock (SCOTLAND2)','data':'9'},{'value':'Partick Thistle (SCOTLAND2)','data':'5'},{'value':'Greenock Morton (SCOTLAND2)','data':'3'},{'value':'Montrose (SCOTLAND3)','data':'2'},{'value':'Falkirk (SCOTLAND3)','data':'6'},{'value':'Queen`s Park (SCOTLAND3)','data':'8'},{'value':'Dumbarton (SCOTLAND3)','data':'4'},{'value':'East Fife (SCOTLAND3)','data':'7'},{'value':'Clyde (SCOTLAND3)','data':'3'},{'value':'Cove Rangers (SCOTLAND3)','data':'5'},{'value':'Alloa Athletic (SCOTLAND3)','data':'10'},{'value':'Airdrieonians (SCOTLAND3)','data':'1'},{'value':'Peterhead (SCOTLAND3)','data':'9'},{'value':'Elgin City (SCOTLAND4)','data':'3'},{'value':'Forfar Athletic (SCOTLAND4)','data':'2'},{'value':'Stirling Albion (SCOTLAND4)','data':'8'},{'value':'Annan Athletic (SCOTLAND4)','data':'1'},{'value':'Cowdenbeath (SCOTLAND4)','data':'6'},{'value':'Brechin City (SCOTLAND4)','data':'3'},{'value':'Stenhousemuir (SCOTLAND4)','data':'7'},{'value':'Albion Rovers (SCOTLAND4)','data':'9'},{'value':'Kelty Hearts (SCOTLAND4)','data':'5'},{'value':'Edinburgh City (SCOTLAND4)','data':'10'},{'value':'Stranraer (SCOTLAND4)','data':'4'},{'value':'Brora Rangers (SCOTLAND5)','data':'18'},{'value':'Nairn County (SCOTLAND5)','data':'25'},{'value':'Formartine Unit (SCOTLAND5)','data':'24'},{'value':'Inverurie Loco  (SCOTLAND5)','data':'23'},{'value':'Clachnacuddin (SCOTLAND5)','data':'22'},{'value':'Deveronvale (SCOTLAND5)','data':'21'},{'value':'Rothes (SCOTLAND5)','data':'19'},{'value':'Turriff United (SCOTLAND5)','data':'27'},{'value':'Fraserburgh (SCOTLAND5)','data':'26'},{'value':'Buckie Thistle (SCOTLAND5)','data':'20'},{'value':'Wick Academy (SCOTLAND5)','data':'31'},{'value':'Caledonian B. (SCOTLAND5)','data':'17'},{'value':'Spartans (SCOTLAND5)','data':'16'},{'value':'Strathspey This (SCOTLAND5)','data':'32'},{'value':'Keith (SCOTLAND5)','data':'30'},{'value':'Fort William (SCOTLAND5)','data':'29'},{'value':'Huntly (SCOTLAND5)','data':'28'},{'value':'Gretna 2008 (SCOTLAND5)','data':'15'},{'value':'Bonnyrigg Rose  (SCOTLAND5)','data':'14'},{'value':'Gala Fairydean  (SCOTLAND5)','data':'13'},{'value':'Civil Service (SCOTLAND5)','data':'12'},{'value':'Edinburgh U. (SCOTLAND5)','data':'4'},{'value':'Lossiemouth (SCOTLAND5)','data':'33'},{'value':'East Stirling. (SCOTLAND5)','data':'11'},{'value':'Stirling U. (SCOTLAND5)','data':'1'},{'value':'East Kilbride (SCOTLAND5)','data':'2'},{'value':'Berwick Rangers (SCOTLAND5)','data':'5'},{'value':'Vale of Leithen (SCOTLAND5)','data':'6'},{'value':'Bo`ness Utd (SCOTLAND5)','data':'7'},{'value':'Cumbernauld C. (SCOTLAND5)','data':'8'},{'value':'BSC Glasgow (SCOTLAND5)','data':'9'},{'value':'Dalbeattie Star (SCOTLAND5)','data':'10'},{'value':'Radnicki 1923 (SERBIA)','data':'12'},{'value':'Sp. Subotica (SERBIA)','data':'9'},{'value':'Red Star (SERBIA)','data':'3'},{'value':'Rad. Surdulica (SERBIA)','data':'13'},{'value':'Vozdovac (SERBIA)','data':'2'},{'value':'Proleter (SERBIA)','data':'7'},{'value':'Novi Pazar (SERBIA)','data':'6'},{'value':'Cukaricki (SERBIA)','data':'1'},{'value':'Metalac GM (SERBIA)','data':'14'},{'value':'Radnicki Nis (SERBIA)','data':'10'},{'value':'Napredak (SERBIA)','data':'15'},{'value':'Mladost Lucani (SERBIA)','data':'11'},{'value':'Backa Topola (SERBIA)','data':'5'},{'value':'Kolubara (SERBIA)','data':'16'},{'value':'Partizan (SERBIA)','data':'8'},{'value':'Vojvodina (SERBIA)','data':'4'},{'value':'Zarkovo (SERBIA2)','data':'7'},{'value':'Macva Sabac (SERBIA2)','data':'9'},{'value':'Z. Cajetina (SERBIA2)','data':'15'},{'value':'Rad Beograd (SERBIA2)','data':'1'},{'value':'Bud. Dovanovci (SERBIA2)','data':'10'},{'value':'Backa Palanka (SERBIA2)','data':'13'},{'value':'Indija (SERBIA2)','data':'5'},{'value':'Javor Ivanjica (SERBIA2)','data':'3'},{'value':'Graficar (SERBIA2)','data':'11'},{'value':'Mladost Novi S. (SERBIA2)','data':'12'},{'value':'Kabel Novi Sad (SERBIA2)','data':'6'},{'value':'Loznica (SERBIA2)','data':'4'},{'value':'Timok (SERBIA2)','data':'16'},{'value':'IMT N. Beograd (SERBIA2)','data':'14'},{'value':'Z. Pancevo (SERBIA2)','data':'8'},{'value':'S. Mitrovica (SERBIA2)','data':'2'},{'value':'Teleoptik (SERBIA3)','data':'7'},{'value':'Zvezdara (SERBIA3)','data':'14'},{'value':'Radnicki B. (SERBIA3)','data':'8'},{'value':'OFK Beograd (SERBIA3)','data':'9'},{'value':'Studentski Grad (SERBIA3)','data':'16'},{'value':'BSK Borca (SERBIA3)','data':'13'},{'value':'Usce Novi B. (SERBIA3)','data':'12'},{'value':'Brodarac (SERBIA3)','data':'3'},{'value':'Lestane (SERBIA3)','data':'10'},{'value':'TEK Sloga (SERBIA3)','data':'1'},{'value':'Prva Iskra (SERBIA3)','data':'5'},{'value':'Zemun (SERBIA3)','data':'11'},{'value':'Borac Lazarevac (SERBIA3)','data':'15'},{'value':'R. Obrenovac (SERBIA3)','data':'4'},{'value':'J. Surcin (SERBIA3)','data':'2'},{'value':'BASK (SERBIA3)','data':'6'},{'value':'Mesevo (SERBIA5)','data':'2'},{'value':'Timocanin (SERBIA5)','data':'15'},{'value':'R. Pirot (SERBIA5)','data':'6'},{'value':'R. Svilajnac (SERBIA5)','data':'4'},{'value':'Brzi Brod (SERBIA5)','data':'14'},{'value':'B. Popovac (SERBIA5)','data':'11'},{'value':'Rembas (SERBIA5)','data':'13'},{'value':'Hajduk Veljko (SERBIA5)','data':'12'},{'value':'P. Trgoviste (SERBIA5)','data':'3'},{'value':'Vlasina (SERBIA5)','data':'10'},{'value':'Sloga Leskovac (SERBIA5)','data':'8'},{'value':'Jagodina (SERBIA5)','data':'9'},{'value':'Trajal Krusevac (SERBIA5)','data':'1'},{'value':'Dinamo Vranje (SERBIA5)','data':'7'},{'value':'Dubocica (SERBIA5)','data':'5'},{'value':'J. Paracin (SERBIA5)','data':'16'},{'value':'Khalsa (SINGAPORE)','data':'8'},{'value':'Tampines Rovers (SINGAPORE)','data':'2'},{'value':'A. Niigata (S) (SINGAPORE)','data':'3'},{'value':'Hougang (SINGAPORE)','data':'4'},{'value':'Geylang (SINGAPORE)','data':'5'},{'value':'Tanjong Pagar (SINGAPORE)','data':'6'},{'value':'Young Lions (SINGAPORE)','data':'7'},{'value':'Lion City (SINGAPORE)','data':'1'},{'value':'L. Mikulas (SLOVAKIA)','data':'3'},{'value':'Zilina (SLOVAKIA)','data':'9'},{'value':'DAC Streda (SLOVAKIA)','data':'8'},{'value':'Spartak Trnava (SLOVAKIA)','data':'11'},{'value':'Trencin (SLOVAKIA)','data':'1'},{'value':'Nitra (SLOVAKIA)','data':'1'},{'value':'Senica (SLOVAKIA)','data':'6'},{'value':'Zlate Moravce (SLOVAKIA)','data':'2'},{'value':'Sered (SLOVAKIA)','data':'10'},{'value':'Ruzomberok (SLOVAKIA)','data':'5'},{'value':'S. Bratislava (SLOVAKIA)','data':'4'},{'value':'Pohronie (SLOVAKIA)','data':'12'},{'value':'Z. Michalovce (SLOVAKIA)','data':'7'},{'value':'Slavoj Trebisov (SLOVAKIA2)','data':'7'},{'value':'Puchov (SLOVAKIA2)','data':'14'},{'value':'Komarno (SLOVAKIA2)','data':'9'},{'value':'Podbrezova (SLOVAKIA2)','data':'4'},{'value':'FC Kosice (SLOVAKIA2)','data':'12'},{'value':'Petrzalka (SLOVAKIA2)','data':'8'},{'value':'Skalica (SLOVAKIA2)','data':'16'},{'value':'Námestovo (SLOVAKIA2)','data':'1'},{'value':'S. Bratislava B (SLOVAKIA2)','data':'11'},{'value':'Banska Bystrica (SLOVAKIA2)','data':'2'},{'value':'Samorin (SLOVAKIA2)','data':'6'},{'value':'Zilina B (SLOVAKIA2)','data':'13'},{'value':'Poprad (SLOVAKIA2)','data':'1'},{'value':'Futura Humenne (SLOVAKIA2)','data':'3'},{'value':'Dubnica (SLOVAKIA2)','data':'10'},{'value':'P. Bardejov (SLOVAKIA2)','data':'5'},{'value':'Rohozník (SLOVAKIA2)','data':'15'},{'value':'Gorica (SLOVENIA)','data':'9'},{'value':'Aluminij (SLOVENIA)','data':'3'},{'value':'Maribor (SLOVENIA)','data':'10'},{'value':'O. Ljubljana (SLOVENIA)','data':'8'},{'value':'Celje (SLOVENIA)','data':'9'},{'value':'Domzale (SLOVENIA)','data':'7'},{'value':'Tabor Sezana (SLOVENIA)','data':'6'},{'value':'Mura (SLOVENIA)','data':'5'},{'value':'Koper (SLOVENIA)','data':'4'},{'value':'Radomlje (SLOVENIA)','data':'2'},{'value':'Bravo (SLOVENIA)','data':'1'},{'value':'Stellenbosch (SOUTHAFRICA)','data':'4'},{'value':'Mamelodi S. (SOUTHAFRICA)','data':'1'},{'value':'Baroka (SOUTHAFRICA)','data':'9'},{'value':'Bloemfontein C. (SOUTHAFRICA)','data':'1'},{'value':'Cape Town City (SOUTHAFRICA)','data':'11'},{'value':'Chippa Utd (SOUTHAFRICA)','data':'6'},{'value':'AmaZulu (SOUTHAFRICA)','data':'2'},{'value':'Kaizer Chiefs (SOUTHAFRICA)','data':'16'},{'value':'SuperSport Utd (SOUTHAFRICA)','data':'12'},{'value':'Maritzburg Utd (SOUTHAFRICA)','data':'8'},{'value':'Moroka Swallows (SOUTHAFRICA)','data':'13'},{'value':'Tshakhuma (SOUTHAFRICA)','data':'10'},{'value':'TS Galaxy (SOUTHAFRICA)','data':'15'},{'value':'Royal AM (SOUTHAFRICA)','data':'14'},{'value':'Sekhukhune (SOUTHAFRICA)','data':'5'},{'value':'Orlando Pirates (SOUTHAFRICA)','data':'3'},{'value':'Golden Arrows (SOUTHAFRICA)','data':'7'},{'value':'Hungry Lions (SOUTHAFRICA2)','data':'3'},{'value':'Uthongathi (SOUTHAFRICA2)','data':'4'},{'value':'Cape Town Spurs (SOUTHAFRICA2)','data':'11'},{'value':'Polokwane (SOUTHAFRICA2)','data':'2'},{'value':'Cape Town AS (SOUTHAFRICA2)','data':'8'},{'value':'JDR Stars (SOUTHAFRICA2)','data':'5'},{'value':'Black Leopards (SOUTHAFRICA2)','data':'1'},{'value':'Venda FC (SOUTHAFRICA2)','data':'12'},{'value':'Bizana Pondo C. (SOUTHAFRICA2)','data':'15'},{'value':'TTM (SOUTHAFRICA2)','data':'7'},{'value':'Steenberg Utd (SOUTHAFRICA2)','data':'14'},{'value':'Jomo Cosmos (SOUTHAFRICA2)','data':'15'},{'value':'Richards Bay (SOUTHAFRICA2)','data':'16'},{'value':'Pretoria U. (SOUTHAFRICA2)','data':'6'},{'value':'Cape Umoya (SOUTHAFRICA2)','data':'10'},{'value':'TS Sporting (SOUTHAFRICA2)','data':'9'},{'value':'Free State S. (SOUTHAFRICA2)','data':'13'},{'value':'Pretoria C. (SOUTHAFRICA2)','data':'10'},{'value':'Platinum City (SOUTHAFRICA2)','data':'14'},{'value':'Pohang Steelers (SOUTHKOREA)','data':'5'},{'value':'Seongnam (SOUTHKOREA)','data':'11'},{'value':'Gangwon (SOUTHKOREA)','data':'10'},{'value':'Gwangju (SOUTHKOREA)','data':'8'},{'value':'Jeju Utd (SOUTHKOREA)','data':'12'},{'value':'Incheon Utd (SOUTHKOREA)','data':'6'},{'value':'Ulsan (SOUTHKOREA)','data':'9'},{'value':'Suwon City (SOUTHKOREA)','data':'4'},{'value':'Daegu (SOUTHKOREA)','data':'3'},{'value':'Seoul (SOUTHKOREA)','data':'2'},{'value':'Jeonbuk Motors (SOUTHKOREA)','data':'1'},{'value':'Suwon Bluewings (SOUTHKOREA)','data':'7'},{'value':'Jeonnam Dragons (SOUTHKOREA2)','data':'5'},{'value':'Gimcheon Sangmu (SOUTHKOREA2)','data':'4'},{'value':'Ansan Greeners (SOUTHKOREA2)','data':'3'},{'value':'Chungnam Asan (SOUTHKOREA2)','data':'6'},{'value':'Anyang (SOUTHKOREA2)','data':'2'},{'value':'Seoul E-Land (SOUTHKOREA2)','data':'10'},{'value':'Gyeongnam (SOUTHKOREA2)','data':'1'},{'value':'Bucheon FC (SOUTHKOREA2)','data':'7'},{'value':'Daejeon Citizen (SOUTHKOREA2)','data':'8'},{'value':'Busan IPark (SOUTHKOREA2)','data':'9'},{'value':'Gimpo (SOUTHKOREA3)','data':'15'},{'value':'Cheonan City (SOUTHKOREA3)','data':'14'},{'value':'Hwaseong (SOUTHKOREA3)','data':'8'},{'value':'Cheongju (SOUTHKOREA3)','data':'13'},{'value':'Busan Transport (SOUTHKOREA3)','data':'7'},{'value':'Gimhae (SOUTHKOREA3)','data':'1'},{'value':'Mokpo City (SOUTHKOREA3)','data':'2'},{'value':'Changwon (SOUTHKOREA3)','data':'3'},{'value':'Ulsan Citizen (SOUTHKOREA3)','data':'4'},{'value':'Gyeongju HNP (SOUTHKOREA3)','data':'5'},{'value':'Daejeon Korail (SOUTHKOREA3)','data':'10'},{'value':'Pyeongtaek C. (SOUTHKOREA3)','data':'6'},{'value':'Paju Citizen (SOUTHKOREA3)','data':'12'},{'value':'Yangju Citizen (SOUTHKOREA3)','data':'9'},{'value':'Gangneung City (SOUTHKOREA3)','data':'11'},{'value':'Seoul W (SOUTHKOREA4)','data':'2'},{'value':'Changnyeong W (SOUTHKOREA4)','data':'4'},{'value':'Suwon FMC W (SOUTHKOREA4)','data':'6'},{'value':'Boeun Sangmu W (SOUTHKOREA4)','data':'7'},{'value':'Gyeongju W (SOUTHKOREA4)','data':'3'},{'value':'Sejong W (SOUTHKOREA4)','data':'8'},{'value':'Incheon W (SOUTHKOREA4)','data':'1'},{'value':'Hwacheon W (SOUTHKOREA4)','data':'5'},{'value':'Osasuna (SPAIN)','data':'3'},{'value':'Celta Vigo (SPAIN)','data':'11'},{'value':'Granada (SPAIN)','data':'18'},{'value':'Cadiz (SPAIN)','data':'7'},{'value':'FC Barcelona (SPAIN)','data':'13'},{'value':'Elche (SPAIN)','data':'19'},{'value':'Real Madrid (SPAIN)','data':'10'},{'value':'Getafe (SPAIN)','data':'2'},{'value':'Alaves (SPAIN)','data':'9'},{'value':'Espanyol (SPAIN)','data':'4'},{'value':'Athletic Bilbao (SPAIN)','data':'20'},{'value':'Real Betis (SPAIN)','data':'6'},{'value':'Rayo Vallecano (SPAIN)','data':'16'},{'value':'Mallorca (SPAIN)','data':'5'},{'value':'Sevilla FC (SPAIN)','data':'15'},{'value':'Atletico Madrid (SPAIN)','data':'12'},{'value':'Levante (SPAIN)','data':'8'},{'value':'Valencia (SPAIN)','data':'1'},{'value':'Villarreal (SPAIN)','data':'17'},{'value':'Real Sociedad (SPAIN)','data':'14'},{'value':'Levante W (SPAIN10)','data':'5'},{'value':'FC Barcelona W (SPAIN10)','data':'1'},{'value':'Atletico M. W (SPAIN10)','data':'3'},{'value':'Real Sociedad W (SPAIN10)','data':'13'},{'value':'R. Vallecano W (SPAIN10)','data':'4'},{'value':'Valencia W (SPAIN10)','data':'14'},{'value':'Athletic Club W (SPAIN10)','data':'16'},{'value':'Real Betis W (SPAIN10)','data':'12'},{'value':'Sevilla W (SPAIN10)','data':'8'},{'value':'Granadilla T. W (SPAIN10)','data':'2'},{'value':'Real Madrid W (SPAIN10)','data':'6'},{'value':'Villarreal W (SPAIN10)','data':'10'},{'value':'Huelva W (SPAIN10)','data':'9'},{'value':'Madrid CFF W (SPAIN10)','data':'15'},{'value':'Alaves W (SPAIN10)','data':'11'},{'value':'Eibar W (SPAIN10)','data':'7'},{'value':'Castellon (SPAIN2)','data':'2'},{'value':'Real Oviedo (SPAIN2)','data':'13'},{'value':'Almeria (SPAIN2)','data':'22'},{'value':'Sabadell (SPAIN2)','data':'11'},{'value':'Girona (SPAIN2)','data':'7'},{'value':'Albacete (SPAIN2)','data':'8'},{'value':'UD Ibiza (SPAIN2)','data':'4'},{'value':'Sporting Gijon (SPAIN2)','data':'11'},{'value':'Cartagena (SPAIN2)','data':'21'},{'value':'Leganes (SPAIN2)','data':'6'},{'value':'Real Zaragoza (SPAIN2)','data':'3'},{'value':'Ponferradina (SPAIN2)','data':'9'},{'value':'Huesca (SPAIN2)','data':'1'},{'value':'Valladolid (SPAIN2)','data':'16'},{'value':'Amorebieta (SPAIN2)','data':'8'},{'value':'Eibar (SPAIN2)','data':'2'},{'value':'Las Palmas (SPAIN2)','data':'15'},{'value':'Burgos (SPAIN2)','data':'12'},{'value':'Lugo (SPAIN2)','data':'14'},{'value':'Mirandes (SPAIN2)','data':'20'},{'value':'Alcorcon (SPAIN2)','data':'10'},{'value':'Tenerife (SPAIN2)','data':'18'},{'value':'Real Sociedad B (SPAIN2)','data':'5'},{'value':'Malaga (SPAIN2)','data':'19'},{'value':'Logrones (SPAIN2)','data':'6'},{'value':'Fuenlabrada (SPAIN2)','data':'17'},{'value':'Viveiro (SPAIN3)','data':'16'},{'value':'Polvorin (SPAIN3)','data':'17'},{'value':'Leonesa (SPAIN3)','data':'2'},{'value':'Somozas (SPAIN3)','data':'7'},{'value':'Racing Ferrol (SPAIN3)','data':'15'},{'value':'Guijuelo (SPAIN3)','data':'3'},{'value':'Coruxo (SPAIN3)','data':'17'},{'value':'Ponteareas (SPAIN3)','data':'11'},{'value':'Zamora (SPAIN3)','data':'18'},{'value':'Alondras (SPAIN3)','data':'9'},{'value':'Arzúa (SPAIN3)','data':'8'},{'value':'Celta Vigo B (SPAIN3)','data':'4'},{'value':'Choco (SPAIN3)','data':'15'},{'value':'Noia (SPAIN3)','data':'14'},{'value':'Estradense (SPAIN3)','data':'12'},{'value':'Atletico Arnoia (SPAIN3)','data':'10'},{'value':'Unionistas (SPAIN3)','data':'13'},{'value':'Valladolid B (SPAIN3)','data':'5'},{'value':'Langreo (SPAIN3)','data':'8'},{'value':'Numancia (SPAIN3)','data':'11'},{'value':'M. de Luanco (SPAIN3)','data':'12'},{'value':'Pontevedra (SPAIN3)','data':'16'},{'value':'Ourense CF (SPAIN3)','data':'13'},{'value':'RC Villalbes (SPAIN3)','data':'6'},{'value':'Compostela (SPAIN3)','data':'14'},{'value':'Salamanca (SPAIN3)','data':'20'},{'value':'Deportivo (SPAIN3)','data':'19'},{'value':'Barco (SPAIN3)','data':'1'},{'value':'Silva (SPAIN3)','data':'2'},{'value':'Sofan (SPAIN3)','data':'3'},{'value':'Deportivo B (SPAIN3)','data':'5'},{'value':'Rapido Bouzas (SPAIN3)','data':'4'},{'value':'G. Industrial (SPAIN4)','data':'3'},{'value':'Llanes (SPAIN4)','data':'2'},{'value':'L`Entregu (SPAIN4)','data':'1'},{'value':'Mutilvera (SPAIN4)','data':'3'},{'value':'Izarra (SPAIN4)','data':'4'},{'value':'Roces (SPAIN4)','data':'8'},{'value':'Real Union (SPAIN4)','data':'11'},{'value':'Mosconia (SPAIN4)','data':'13'},{'value':'Osasuna B (SPAIN4)','data':'10'},{'value':'Colunga (SPAIN4)','data':'18'},{'value':'Praviano (SPAIN4)','data':'19'},{'value':'Ebro (SPAIN4)','data':'5'},{'value':'Tarazona (SPAIN4)','data':'9'},{'value':'SD Logrones (SPAIN4)','data':'6'},{'value':'San Martin (SPAIN4)','data':'20'},{'value':'Ejea (SPAIN4)','data':'8'},{'value':'Haro (SPAIN4)','data':'13'},{'value':'Arenas de Getxo (SPAIN4)','data':'19'},{'value':'Luarca (SPAIN4)','data':'16'},{'value':'Lenense (SPAIN4)','data':'17'},{'value':'Urraca (SPAIN4)','data':'15'},{'value':'Langreo B (SPAIN4)','data':'14'},{'value':'Sporting B (SPAIN4)','data':'6'},{'value':'Real Titanico (SPAIN4)','data':'11'},{'value':'Real Oviedo B (SPAIN4)','data':'7'},{'value':'SD Navarro (SPAIN4)','data':'9'},{'value':'Lealtad (SPAIN4)','data':'4'},{'value':'Covadonga (SPAIN4)','data':'5'},{'value':'Racing (SPAIN4)','data':'17'},{'value':'Calahorra (SPAIN4)','data':'14'},{'value':'Laredo (SPAIN4)','data':'2'},{'value':'Tudelano (SPAIN4)','data':'7'},{'value':'Tuilla (SPAIN4)','data':'12'},{'value':'Caudal (SPAIN4)','data':'10'},{'value':'Athletic Club B (SPAIN4)','data':'20'},{'value':'Cornella (SPAIN5)','data':'3'},{'value':'Albericia (SPAIN5)','data':'16'},{'value':'La Nucia (SPAIN5)','data':'19'},{'value':'Samano (SPAIN5)','data':'1'},{'value':'Cartes (SPAIN5)','data':'10'},{'value':'Torrelavega (SPAIN5)','data':'11'},{'value':'Naval (SPAIN5)','data':'12'},{'value':'Lleida Esportiu (SPAIN5)','data':'21'},{'value':'Textil Escudo (SPAIN5)','data':'13'},{'value':'Barreda (SPAIN5)','data':'14'},{'value':'Vimenor (SPAIN5)','data':'15'},{'value':'Escobedo (SPAIN5)','data':'8'},{'value':'Prat (SPAIN5)','data':'6'},{'value':'Torina (SPAIN5)','data':'7'},{'value':'Levante B (SPAIN5)','data':'7'},{'value':'Badalona (SPAIN5)','data':'17'},{'value':'Peña Deportiva (SPAIN5)','data':'9'},{'value':'Villarreal B (SPAIN5)','data':'10'},{'value':'Llagostera (SPAIN5)','data':'11'},{'value':'FC Andorra (SPAIN5)','data':'12'},{'value':'Alcoyano (SPAIN5)','data':'13'},{'value':'Hercules (SPAIN5)','data':'14'},{'value':'FC Barcelona B (SPAIN5)','data':'15'},{'value':'Espanyol B (SPAIN5)','data':'5'},{'value':'Siete Villas (SPAIN5)','data':'6'},{'value':'Selaya (SPAIN5)','data':'5'},{'value':'Gimnastic Tar. (SPAIN5)','data':'16'},{'value':'Noja (SPAIN5)','data':'3'},{'value':'Guarnizo (SPAIN5)','data':'4'},{'value':'Castro (SPAIN5)','data':'2'},{'value':'Colindres (SPAIN5)','data':'9'},{'value':'Deusto (SPAIN6)','data':'8'},{'value':'Basconia (SPAIN6)','data':'20'},{'value':'CD Vitoria (SPAIN6)','data':'18'},{'value':'Amurrio (SPAIN6)','data':'17'},{'value':'Beti Gazte (SPAIN6)','data':'16'},{'value':'Durango (SPAIN6)','data':'15'},{'value':'A. Ondarroa (SPAIN6)','data':'14'},{'value':'Urduliz (SPAIN6)','data':'13'},{'value':'San Ignacio (SPAIN6)','data':'11'},{'value':'Uritarra (SPAIN6)','data':'7'},{'value':'Lagun Onak (SPAIN6)','data':'6'},{'value':'Pasaia KE (SPAIN6)','data':'5'},{'value':'Tamaraceite (SPAIN6)','data':'7'},{'value':'Anaitasuna FT (SPAIN6)','data':'3'},{'value':'Beasain (SPAIN6)','data':'2'},{'value':'Tolosa (SPAIN6)','data':'1'},{'value':'Santutxu (SPAIN6)','data':'12'},{'value':'Linense (SPAIN6)','data':'10'},{'value':'Leioa (SPAIN6)','data':'9'},{'value':'Portugalete (SPAIN6)','data':'4'},{'value':'Barakaldo (SPAIN6)','data':'19'},{'value':'Real Murcia (SPAIN6)','data':'1'},{'value':'Granada B (SPAIN6)','data':'2'},{'value':'Sevilla B (SPAIN6)','data':'3'},{'value':'UCAM Murcia (SPAIN6)','data':'4'},{'value':'Las Palmas B (SPAIN6)','data':'6'},{'value':'Alaves B (SPAIN6)','data':'10'},{'value':'Marino (SPAIN6)','data':'9'},{'value':'El Ejido (SPAIN6)','data':'17'},{'value':'Linares Dep. (SPAIN6)','data':'11'},{'value':'Yeclano (SPAIN6)','data':'12'},{'value':'Sanluqueno (SPAIN6)','data':'13'},{'value':'Recreativo H. (SPAIN6)','data':'14'},{'value':'Algeciras (SPAIN6)','data':'15'},{'value':'Marbella (SPAIN6)','data':'16'},{'value':'Real Betis B (SPAIN6)','data':'18'},{'value':'Lorca Deportiva (SPAIN6)','data':'20'},{'value':'Cadiz B (SPAIN6)','data':'5'},{'value':'San Fernando (SPAIN6)','data':'8'},{'value':'Cordoba (SPAIN6)','data':'19'},{'value':'Sants (SPAIN7)','data':'13'},{'value':'R. Majadahonda (SPAIN7)','data':'2'},{'value':'Guineueta (SPAIN7)','data':'1'},{'value':'Grama (SPAIN7)','data':'2'},{'value':'Castelldefels (SPAIN7)','data':'4'},{'value':'Sant Andreu (SPAIN7)','data':'5'},{'value':'Manresa (SPAIN7)','data':'6'},{'value':'Peralada (SPAIN7)','data':'9'},{'value':'Real Madrid B (SPAIN7)','data':'4'},{'value':'Vilafranca (SPAIN7)','data':'12'},{'value':'Girona B (SPAIN7)','data':'8'},{'value':'Figueres (SPAIN7)','data':'14'},{'value':'Granollers (SPAIN7)','data':'15'},{'value':'San Cristobal (SPAIN7)','data':'16'},{'value':'Asco (SPAIN7)','data':'17'},{'value':'L`Hospitalet (SPAIN7)','data':'7'},{'value':'Olot (SPAIN7)','data':'3'},{'value':'Vilassar Mar (SPAIN7)','data':'11'},{'value':'Extremadura (SPAIN7)','data':'16'},{'value':'Pobla Mafumet (SPAIN7)','data':'10'},{'value':'San S. Reyes (SPAIN7)','data':'5'},{'value':'Villanovense (SPAIN7)','data':'20'},{'value':'Villarrubia (SPAIN7)','data':'19'},{'value':'Merida (SPAIN7)','data':'17'},{'value':'Don Benito (SPAIN7)','data':'15'},{'value':'Villarrobledo (SPAIN7)','data':'14'},{'value':'Atl. Baleares (SPAIN7)','data':'9'},{'value':'Navalcarnero (SPAIN7)','data':'6'},{'value':'Talavera CF (SPAIN7)','data':'18'},{'value':'Poblense (SPAIN7)','data':'8'},{'value':'Internacional (SPAIN7)','data':'10'},{'value':'Socuellamos (SPAIN7)','data':'11'},{'value':'Badajoz (SPAIN7)','data':'12'},{'value':'Melilla (SPAIN7)','data':'13'},{'value':'Beniganim (SPAIN8)','data':'14'},{'value':'Elche B (SPAIN8)','data':'1'},{'value':'Valencia B (SPAIN8)','data':'9'},{'value':'Santa Teresa W (SPAIN8)','data':'13'},{'value':'Orihuela (SPAIN8)','data':'4'},{'value':'Olimpic Xativa (SPAIN8)','data':'19'},{'value':'Villarreal C (SPAIN8)','data':'18'},{'value':'Callosa (SPAIN8)','data':'17'},{'value':'Saguntino (SPAIN8)','data':'16'},{'value':'Silla (SPAIN8)','data':'15'},{'value':'Espanyol W (SPAIN8)','data':'5'},{'value':'Recambios C. (SPAIN8)','data':'13'},{'value':'Roda (SPAIN8)','data':'11'},{'value':'Deportivo W (SPAIN8)','data':'4'},{'value':'Acero (SPAIN8)','data':'8'},{'value':'Torrent (SPAIN8)','data':'6'},{'value':'Villajoyosa (SPAIN8)','data':'5'},{'value':'Hercules B (SPAIN8)','data':'2'},{'value':'Logrono W (SPAIN8)','data':'1'},{'value':'Atzeneta (SPAIN8)','data':'7'},{'value':'Torrellano (SPAIN8)','data':'12'},{'value':'Jove Espanol (SPAIN8)','data':'3'},{'value':'Castellon B (SPAIN8)','data':'10'},{'value':'CDE Madrid (SPAIN9)','data':'12'},{'value':'Villaverde-B. (SPAIN9)','data':'2'},{'value':'Alcorcon B (SPAIN9)','data':'3'},{'value':'C. Moscardo (SPAIN9)','data':'5'},{'value':'Ursaria (SPAIN9)','data':'6'},{'value':'Carabanchel (SPAIN9)','data':'7'},{'value':'Trival Valderas (SPAIN9)','data':'8'},{'value':'P. Antamira (SPAIN9)','data':'21'},{'value':'Complutense (SPAIN9)','data':'10'},{'value':'Las Rozas (SPAIN9)','data':'11'},{'value':'Parla (SPAIN9)','data':'14'},{'value':'Pozuelo Alarcon (SPAIN9)','data':'15'},{'value':'Villaviciosa (SPAIN9)','data':'16'},{'value':'Galapagar (SPAIN9)','data':'17'},{'value':'Tres Cantos (SPAIN9)','data':'18'},{'value':'RSD Alcala (SPAIN9)','data':'19'},{'value':'Moratalaz (SPAIN9)','data':'20'},{'value':'Torrejon (SPAIN9)','data':'9'},{'value':'Atletico M. B (SPAIN9)','data':'13'},{'value':'Getafe B (SPAIN9)','data':'4'},{'value':'R. Vallecano B (SPAIN9)','data':'1'},{'value':'Malmo FF (SWEDEN)','data':'1'},{'value':'Djurgarden (SWEDEN)','data':'10'},{'value':'Elfsborg (SWEDEN)','data':'9'},{'value':'Varberg BoIS (SWEDEN)','data':'8'},{'value':'Mjallby (SWEDEN)','data':'7'},{'value':'Hacken (SWEDEN)','data':'6'},{'value':'Halmstad (SWEDEN)','data':'5'},{'value':'IFK Goteborg (SWEDEN)','data':'4'},{'value':'Hammarby (SWEDEN)','data':'2'},{'value':'Norrkoping (SWEDEN)','data':'11'},{'value':'Sirius (SWEDEN)','data':'12'},{'value':'AIK Stockholm (SWEDEN)','data':'13'},{'value':'Degerfors (SWEDEN)','data':'14'},{'value':'Kalmar (SWEDEN)','data':'15'},{'value':'Ostersunds (SWEDEN)','data':'16'},{'value':'Orebro (SWEDEN)','data':'3'},{'value':'Asarum (SWEDEN10)','data':'5'},{'value':'Prespa Birlik (SWEDEN10)','data':'11'},{'value':'Karlshamn (SWEDEN10)','data':'12'},{'value':'Kristianstad (SWEDEN10)','data':'13'},{'value':'Balkan (SWEDEN10)','data':'14'},{'value':'IFK Hassleholm (SWEDEN10)','data':'15'},{'value':'Eslov (SWEDEN10)','data':'9'},{'value':'Olympic (SWEDEN10)','data':'8'},{'value':'Rappe (SWEDEN10)','data':'10'},{'value':'Berga (SWEDEN10)','data':'6'},{'value':'Karlskrona (SWEDEN10)','data':'4'},{'value':'Rosengard (SWEDEN10)','data':'3'},{'value':'Hsssleholms IF (SWEDEN10)','data':'2'},{'value':'Nosaby (SWEDEN10)','data':'1'},{'value':'Solvesborg (SWEDEN10)','data':'7'},{'value':'Eskilstuna U. W (SWEDEN11)','data':'9'},{'value':'Vaxjo W (SWEDEN11)','data':'1'},{'value':'AIK W (SWEDEN11)','data':'2'},{'value':'Djurgarden W (SWEDEN11)','data':'3'},{'value':'Orebro W (SWEDEN11)','data':'4'},{'value':'Vittsjo W (SWEDEN11)','data':'5'},{'value':'Pitea W (SWEDEN11)','data':'6'},{'value':'Hacken W (SWEDEN11)','data':'8'},{'value':'Rosengard W (SWEDEN11)','data':'12'},{'value':'Kristianstads W (SWEDEN11)','data':'10'},{'value':'Linkoping W (SWEDEN11)','data':'11'},{'value':'Hammarby W (SWEDEN11)','data':'7'},{'value':'Alingsas W (SWEDEN12)','data':'12'},{'value':'Alvsjo W (SWEDEN12)','data':'2'},{'value':'Norrkoping W (SWEDEN12)','data':'3'},{'value':'Kalmar W (SWEDEN12)','data':'4'},{'value':'Uppsala W (SWEDEN12)','data':'5'},{'value':'Lidkoping W (SWEDEN12)','data':'6'},{'value':'Borgeby W (SWEDEN12)','data':'1'},{'value':'Umea W (SWEDEN12)','data':'13'},{'value':'Jitex W (SWEDEN12)','data':'7'},{'value':'Moron W (SWEDEN12)','data':'11'},{'value':'Brommapojk. W  (SWEDEN12)','data':'10'},{'value':'Mallbacken W (SWEDEN12)','data':'9'},{'value':'Sundsvall W (SWEDEN12)','data':'8'},{'value':'Bollstanas W (SWEDEN12)','data':'14'},{'value':'Norrby (SWEDEN2)','data':'12'},{'value':'Helsingborg (SWEDEN2)','data':'16'},{'value':'Falkenberg (SWEDEN2)','data':'1'},{'value':'GAIS (SWEDEN2)','data':'2'},{'value':'Landskrona (SWEDEN2)','data':'3'},{'value':'Varnamo (SWEDEN2)','data':'4'},{'value':'Akropolis (SWEDEN2)','data':'5'},{'value':'Brage (SWEDEN2)','data':'6'},{'value':'Orgryte (SWEDEN2)','data':'7'},{'value':'Oster (SWEDEN2)','data':'8'},{'value':'Jonkopings (SWEDEN2)','data':'9'},{'value':'Vasalund (SWEDEN2)','data':'10'},{'value':'Trelleborg (SWEDEN2)','data':'11'},{'value':'Vasteras (SWEDEN2)','data':'13'},{'value':'AFC Eskilstuna (SWEDEN2)','data':'14'},{'value':'GIF Sundsvall (SWEDEN2)','data':'15'},{'value':'Gefle (SWEDEN3)','data':'15'},{'value':'Sollentuna (SWEDEN3)','data':'4'},{'value':'Haninge (SWEDEN3)','data':'5'},{'value':'Sylvia (SWEDEN3)','data':'7'},{'value':'Dalkurd (SWEDEN3)','data':'9'},{'value':'Pitea (SWEDEN3)','data':'10'},{'value':'Hammarby Talang (SWEDEN3)','data':'12'},{'value':'Taby (SWEDEN3)','data':'14'},{'value':'Orebro S. (SWEDEN3)','data':'3'},{'value':'IFK Lulea (SWEDEN3)','data':'16'},{'value':'Umea (SWEDEN3)','data':'11'},{'value':'Frej (SWEDEN3)','data':'16'},{'value':'Sandviken (SWEDEN3)','data':'8'},{'value':'Karlstad (SWEDEN3)','data':'2'},{'value':'Brommapojkarna (SWEDEN3)','data':'1'},{'value':'Assyriska (SWEDEN3)','data':'13'},{'value':'Hudiksvall (SWEDEN3)','data':'6'},{'value':'Osterlen (SWEDEN4)','data':'4'},{'value':'Lund (SWEDEN4)','data':'3'},{'value':'Torns (SWEDEN4)','data':'2'},{'value':'Tvaaker (SWEDEN4)','data':'1'},{'value':'Skovde AIK (SWEDEN4)','data':'7'},{'value':'Lindome (SWEDEN4)','data':'6'},{'value':'Trollhattan (SWEDEN4)','data':'5'},{'value':'Utsikten (SWEDEN4)','data':'14'},{'value':'Atvidaberg (SWEDEN4)','data':'16'},{'value':'Oskarshamns (SWEDEN4)','data':'13'},{'value':'Vanersborgs (SWEDEN4)','data':'12'},{'value':'Linkoping City (SWEDEN4)','data':'11'},{'value':'Ljungskile (SWEDEN4)','data':'10'},{'value':'Assyriska (SWEDEN4)','data':'9'},{'value':'Qviding (SWEDEN4)','data':'8'},{'value':'IFK Malmo (SWEDEN4)','data':'15'},{'value':'Angered BK (SWEDEN5)','data':'3'},{'value':'Vanersborgs (SWEDEN5)','data':'15'},{'value':'Kumla (SWEDEN5)','data':'14'},{'value':'IF Karlstad B (SWEDEN5)','data':'13'},{'value':'Ahlafors (SWEDEN5)','data':'12'},{'value':'Nordvarmland (SWEDEN5)','data':'11'},{'value':'Forward (SWEDEN5)','data':'10'},{'value':'Yxhult (SWEDEN5)','data':'9'},{'value':'Stenungsund (SWEDEN5)','data':'8'},{'value':'Lidkoping (SWEDEN5)','data':'7'},{'value':'IFK Skovde (SWEDEN5)','data':'6'},{'value':'Oddevold (SWEDEN5)','data':'4'},{'value':'Tidaholm (SWEDEN5)','data':'2'},{'value':'Gauthiod (SWEDEN5)','data':'1'},{'value':'Grebbestad (SWEDEN5)','data':'5'},{'value':'IFK Osteraker (SWEDEN6)','data':'15'},{'value':'Stocksund (SWEDEN6)','data':'14'},{'value':'Gute (SWEDEN6)','data':'13'},{'value':'Jarfalla (SWEDEN6)','data':'11'},{'value':'Arlanda (SWEDEN6)','data':'9'},{'value':'Sandvikens (SWEDEN6)','data':'4'},{'value':'Kungsangen (SWEDEN6)','data':'8'},{'value':'Stockholm Inter (SWEDEN6)','data':'7'},{'value':'Karlberg (SWEDEN6)','data':'6'},{'value':'Enkoping (SWEDEN6)','data':'2'},{'value':'Enskede (SWEDEN6)','data':'5'},{'value':'Skiljebo (SWEDEN6)','data':'10'},{'value':'Lidingo (SWEDEN6)','data':'3'},{'value':'Kvarnsveden (SWEDEN6)','data':'12'},{'value':'Gamla Upsala (SWEDEN6)','data':'1'},{'value':'Friska Viljor (SWEDEN7)','data':'8'},{'value':'Froso (SWEDEN7)','data':'14'},{'value':'Tegs SK (SWEDEN7)','data':'15'},{'value':'IFK Ostersund (SWEDEN7)','data':'12'},{'value':'Bergnasets (SWEDEN7)','data':'11'},{'value':'Boden (SWEDEN7)','data':'9'},{'value':'Notvikens IK (SWEDEN7)','data':'7'},{'value':'Taftea (SWEDEN7)','data':'6'},{'value':'Skelleftea (SWEDEN7)','data':'5'},{'value':'Ytterhogdal (SWEDEN7)','data':'4'},{'value':'Sandviks (SWEDEN7)','data':'3'},{'value':'Stode (SWEDEN7)','data':'2'},{'value':'Gottne IF (SWEDEN7)','data':'10'},{'value':'Storfors (SWEDEN7)','data':'1'},{'value':'Umea FC A. (SWEDEN7)','data':'13'},{'value':'Eskilstuna City (SWEDEN8)','data':'4'},{'value':'Varmbols (SWEDEN8)','data':'11'},{'value':'Motala (SWEDEN8)','data':'10'},{'value':'Trosa Vagnharad (SWEDEN8)','data':'9'},{'value':'Tyreso (SWEDEN8)','data':'8'},{'value':'United Nordic (SWEDEN8)','data':'7'},{'value':'Syrianska (SWEDEN8)','data':'12'},{'value':'Nykoping (SWEDEN8)','data':'5'},{'value':'Mjolby (SWEDEN8)','data':'13'},{'value':'Smedby (SWEDEN8)','data':'3'},{'value':'Rynninge (SWEDEN8)','data':'2'},{'value':'IFK Eskilstuna (SWEDEN8)','data':'1'},{'value':'Karlslund (SWEDEN8)','data':'15'},{'value':'Huddinge (SWEDEN8)','data':'14'},{'value':'Arameiska-S. (SWEDEN8)','data':'6'},{'value':'Ullared (SWEDEN9)','data':'10'},{'value':'Angelholm (SWEDEN9)','data':'8'},{'value':'Tord (SWEDEN9)','data':'15'},{'value':'Onsala (SWEDEN9)','data':'14'},{'value':'Astrio (SWEDEN9)','data':'13'},{'value':'Vastra Frolunda (SWEDEN9)','data':'12'},{'value':'Savedalen (SWEDEN9)','data':'7'},{'value':'Eskilsminne (SWEDEN9)','data':'6'},{'value':'Vinberg (SWEDEN9)','data':'5'},{'value':'Torslanda (SWEDEN9)','data':'4'},{'value':'Varbergs GIF (SWEDEN9)','data':'3'},{'value':'Assyriska BK (SWEDEN9)','data':'2'},{'value':'Hoganas (SWEDEN9)','data':'1'},{'value':'Dalstorps (SWEDEN9)','data':'11'},{'value':'Husqvarna (SWEDEN9)','data':'9'},{'value':'St. Gallen (SWITZERLAND)','data':'4'},{'value':'Lugano (SWITZERLAND)','data':'5'},{'value':'Grasshopper (SWITZERLAND)','data':'7'},{'value':'Sion (SWITZERLAND)','data':'9'},{'value':'Servette (SWITZERLAND)','data':'10'},{'value':'Lausanne Sport (SWITZERLAND)','data':'3'},{'value':'FC Basel (SWITZERLAND)','data':'8'},{'value':'FC Zurich (SWITZERLAND)','data':'6'},{'value':'BSC Young Boys (SWITZERLAND)','data':'2'},{'value':'Luzern (SWITZERLAND)','data':'1'},{'value':'Vaduz (SWITZERLAND2)','data':'10'},{'value':'Schaffhausen (SWITZERLAND2)','data':'7'},{'value':'Yverdon (SWITZERLAND2)','data':'2'},{'value':'Winterthur (SWITZERLAND2)','data':'6'},{'value':'Kriens (SWITZERLAND2)','data':'8'},{'value':'Neuchatel Xamax (SWITZERLAND2)','data':'3'},{'value':'Thun (SWITZERLAND2)','data':'1'},{'value':'Aarau (SWITZERLAND2)','data':'4'},{'value':'Wil (SWITZERLAND2)','data':'9'},{'value':'Lausanne Ouchy (SWITZERLAND2)','data':'5'},{'value':'Stade Nyonnais (SWITZERLAND3)','data':'14'},{'value':'Chiasso (SWITZERLAND3)','data':'13'},{'value':'Biel-Bienne (SWITZERLAND3)','data':'2'},{'value':'BSC Y. Boys B (SWITZERLAND3)','data':'16'},{'value':'Breitenrain (SWITZERLAND3)','data':'9'},{'value':'YF Juventus (SWITZERLAND3)','data':'7'},{'value':'Zurich B (SWITZERLAND3)','data':'6'},{'value':'Koniz (SWITZERLAND3)','data':'6'},{'value':'Sion B (SWITZERLAND3)','data':'4'},{'value':'Bellinzona (SWITZERLAND3)','data':'15'},{'value':'Rapperswil (SWITZERLAND3)','data':'10'},{'value':'Etoile Carouge (SWITZERLAND3)','data':'8'},{'value':'Munsingen (SWITZERLAND3)','data':'15'},{'value':'Basel B (SWITZERLAND3)','data':'12'},{'value':'Cham (SWITZERLAND3)','data':'3'},{'value':'Black Stars (SWITZERLAND3)','data':'11'},{'value':'Bavois (SWITZERLAND3)','data':'1'},{'value':'Bruhl (SWITZERLAND3)','data':'5'},{'value':'Ruvu Shooting (TANZANIA)','data':'8'},{'value':'Namungo (TANZANIA)','data':'3'},{'value':'Coastal Union (TANZANIA)','data':'5'},{'value':'Geita Gold (TANZANIA)','data':'4'},{'value':'Mtibwa Sugar (TANZANIA)','data':'1'},{'value':'Young Africans (TANZANIA)','data':'16'},{'value':'Dodoma Jiji (TANZANIA)','data':'7'},{'value':'Gwambina (TANZANIA)','data':'10'},{'value':'Simba (TANZANIA)','data':'12'},{'value':'Ihefu (TANZANIA)','data':'5'},{'value':'Kagera Sugar (TANZANIA)','data':'15'},{'value':'T. Prisons (TANZANIA)','data':'10'},{'value':'Mbeya Kwanza (TANZANIA)','data':'2'},{'value':'KMC (TANZANIA)','data':'14'},{'value':'Mbeya City (TANZANIA)','data':'9'},{'value':'Biashara Utd (TANZANIA)','data':'11'},{'value':'Polisi Tanzania (TANZANIA)','data':'13'},{'value':'Mwadui (TANZANIA)','data':'8'},{'value':'Azam (TANZANIA)','data':'6'},{'value':'JKT Tanzania (TANZANIA)','data':'16'},{'value':'Muang Thong Utd (THAILAND)','data':'6'},{'value':'Khon Kaen Utd (THAILAND)','data':'7'},{'value':'Ratchaburi (THAILAND)','data':'8'},{'value':'Chonburi (THAILAND)','data':'13'},{'value':'Chiangmai Utd (THAILAND)','data':'3'},{'value':'Buriram Utd (THAILAND)','data':'9'},{'value':'Pathum Utd (THAILAND)','data':'14'},{'value':'Police Tero (THAILAND)','data':'16'},{'value':'Suphanburi (THAILAND)','data':'10'},{'value':'N. Ratchasima (THAILAND)','data':'2'},{'value':'Chiangrai Utd (THAILAND)','data':'11'},{'value':'Prachuap (THAILAND)','data':'5'},{'value':'Bangkok Utd (THAILAND)','data':'4'},{'value':'Port FC (THAILAND)','data':'15'},{'value':'N. Bua Pitchaya (THAILAND)','data':'1'},{'value':'Samut Prakan (THAILAND)','data':'12'},{'value':'Rayong (THAILAND2)','data':'10'},{'value':'Trat (THAILAND2)','data':'1'},{'value':'Udon Thani (THAILAND2)','data':'8'},{'value':'Sukhothai (THAILAND2)','data':'11'},{'value':'Chiangmai FC (THAILAND2)','data':'9'},{'value':'Muangkan United (THAILAND2)','data':'4'},{'value':'Phrae Utd (THAILAND2)','data':'13'},{'value':'Chainat (THAILAND2)','data':'5'},{'value':'Uthai Thani (THAILAND2)','data':'18'},{'value':'Kasetsart (THAILAND2)','data':'15'},{'value':'Customs Utd (THAILAND2)','data':'17'},{'value':'Khonkaen FC (THAILAND2)','data':'16'},{'value':'Lamphun Warrior (THAILAND2)','data':'3'},{'value':'Raj Pracha (THAILAND2)','data':'6'},{'value':'Samut Sakhon (THAILAND2)','data':'15'},{'value':'Sisaket (THAILAND2)','data':'9'},{'value':'Nakhon Pathom (THAILAND2)','data':'2'},{'value':'Ranong Utd (THAILAND2)','data':'7'},{'value':'Ayutthaya Utd (THAILAND2)','data':'12'},{'value':'Navy (THAILAND2)','data':'14'},{'value':'Lampang (THAILAND2)','data':'18'},{'value':'CA Bizertin (TUNISIA)','data':'6'},{'value':'Etoile du Sahel (TUNISIA)','data':'16'},{'value':'CS Sfaxien (TUNISIA)','data':'13'},{'value':'Métlaoui (TUNISIA)','data':'14'},{'value':'ES Tunis (TUNISIA)','data':'12'},{'value':'Slimane (TUNISIA)','data':'11'},{'value':'Hammam-Lif (TUNISIA)','data':'10'},{'value':'Hammam-Sousse (TUNISIA)','data':'9'},{'value':'Ben Guerdane (TUNISIA)','data':'15'},{'value':'Monastir (TUNISIA)','data':'7'},{'value':'Tataouine (TUNISIA)','data':'5'},{'value':'Rejiche (TUNISIA)','data':'4'},{'value':'Club Africain (TUNISIA)','data':'3'},{'value':'Olympique Béja (TUNISIA)','data':'2'},{'value':'Zarzis (TUNISIA)','data':'1'},{'value':'Chebba (TUNISIA)','data':'8'},{'value':'Sivasspor (TURKEY)','data':'17'},{'value':'Giresunspor (TURKEY)','data':'19'},{'value':'Goztepe (TURKEY)','data':'12'},{'value':'Trabzonspor (TURKEY)','data':'16'},{'value':'Besiktas (TURKEY)','data':'1'},{'value':'Antalyaspor (TURKEY)','data':'11'},{'value':'Rizespor (TURKEY)','data':'2'},{'value':'Hatayspor (TURKEY)','data':'7'},{'value':'Basaksehir (TURKEY)','data':'9'},{'value':'Fenerbahce (TURKEY)','data':'14'},{'value':'Alanyaspor (TURKEY)','data':'10'},{'value':'F. Karagumruk (TURKEY)','data':'3'},{'value':'Y. Malatyaspor (TURKEY)','data':'15'},{'value':'Galatasaray (TURKEY)','data':'20'},{'value':'Gaziantep (TURKEY)','data':'4'},{'value':'Adana Demirspor (TURKEY)','data':'13'},{'value':'Kasimpasa (TURKEY)','data':'8'},{'value':'Kayserispor (TURKEY)','data':'6'},{'value':'Altay (TURKEY)','data':'5'},{'value':'Konyaspor (TURKEY)','data':'18'},{'value':'Istanbulspor (TURKEY2)','data':'3'},{'value':'Tuzlaspor (TURKEY2)','data':'9'},{'value':'Bandirmaspor (TURKEY2)','data':'6'},{'value':'Adanaspor (TURKEY2)','data':'14'},{'value':'Eyupspor (TURKEY2)','data':'2'},{'value':'Samsunspor (TURKEY2)','data':'19'},{'value':'Kocaelispor (TURKEY2)','data':'17'},{'value':'Erzurum BB (TURKEY2)','data':'16'},{'value':'Balikesirspor (TURKEY2)','data':'7'},{'value':'Genclerbirligi (TURKEY2)','data':'1'},{'value':'Menemen B. (TURKEY2)','data':'15'},{'value':'Bursaspor (TURKEY2)','data':'13'},{'value':'Keciorengucu (TURKEY2)','data':'11'},{'value':'Boluspor (TURKEY2)','data':'8'},{'value':'Umraniyespor (TURKEY2)','data':'18'},{'value':'Altinordu (TURKEY2)','data':'12'},{'value':'Manisa BB (TURKEY2)','data':'4'},{'value':'Denizlispor (TURKEY2)','data':'5'},{'value':'Ankaragucu (TURKEY2)','data':'10'},{'value':'Pazarspor (TURKEY3)','data':'1'},{'value':'Kastamonuspor (TURKEY3)','data':'7'},{'value':'Kirsehir B. (TURKEY3)','data':'2'},{'value':'Kirklarelispor (TURKEY3)','data':'9'},{'value':'Eskisehirspor (TURKEY3)','data':'14'},{'value':'Karacabey (TURKEY3)','data':'13'},{'value':'Akhisarspor (TURKEY3)','data':'4'},{'value':'Z. Komurspor (TURKEY3)','data':'3'},{'value':'Pendikspor (TURKEY3)','data':'8'},{'value':'1922 Konyaspor  (TURKEY3)','data':'5'},{'value':'Tarsus Idman Y. (TURKEY3)','data':'6'},{'value':'24 Erzincanspor (TURKEY3)','data':'19'},{'value':'Sanliurfaspor (TURKEY3)','data':'15'},{'value':'A. Demirspor (TURKEY3)','data':'16'},{'value':'Utas Usakspor (TURKEY3)','data':'12'},{'value':'Isparta Davrazs (TURKEY3)','data':'18'},{'value':'Nazilli Belediy (TURKEY3)','data':'10'},{'value':'Amed SK (TURKEY3)','data':'11'},{'value':'Tire 1922 (TURKEY3)','data':'17'},{'value':'Somaspor (TURKEY4)','data':'15'},{'value':'Adiyaman 1954 (TURKEY4)','data':'4'},{'value':'Osmanlispor (TURKEY4)','data':'17'},{'value':'Van Buyuksehir (TURKEY4)','data':'3'},{'value':'Sakaryaspor (TURKEY4)','data':'6'},{'value':'Serik Belediyes (TURKEY4)','data':'8'},{'value':'Yeni Diyarbekir (TURKEY4)','data':'20'},{'value':'Corum (TURKEY4)','data':'19'},{'value':'Kahramanmar. (TURKEY4)','data':'7'},{'value':'Bayburt (TURKEY4)','data':'5'},{'value':'Etimesgut (TURKEY4)','data':'10'},{'value':'Bodrumspor (TURKEY4)','data':'13'},{'value':'Sivas Belediyes (TURKEY4)','data':'1'},{'value':'Hekimoglu T. (TURKEY4)','data':'9'},{'value':'Inegolspor (TURKEY4)','data':'18'},{'value':'Turgutluspor (TURKEY4)','data':'2'},{'value':'Ergene Velimese (TURKEY4)','data':'12'},{'value':'Afjet Afyonspor (TURKEY4)','data':'14'},{'value':'Nigde Anadolu (TURKEY4)','data':'16'},{'value':'Sariyer (TURKEY4)','data':'11'},{'value':'Elazigspor-2 (TURKEY4)','data':'22'},{'value':'Bursa Y. (TURKEY5)','data':'4'},{'value':'Erbaaspor (TURKEY5)','data':'11'},{'value':'Artvin Hopaspor (TURKEY5)','data':'2'},{'value':'Arnavutkoy B. (TURKEY5)','data':'18'},{'value':'Kutahyaspor (TURKEY5)','data':'17'},{'value':'Osmaniyespor (TURKEY5)','data':'16'},{'value':'Elazigspor (TURKEY5)','data':'9'},{'value':'Kelkit (TURKEY5)','data':'12'},{'value':'Sancaktepe (TURKEY5)','data':'15'},{'value':'Bergama B. (TURKEY5)','data':'10'},{'value':'Hendek (TURKEY5)','data':'7'},{'value':'Karaman (TURKEY5)','data':'6'},{'value':'Catalcaspor (TURKEY5)','data':'5'},{'value':'B. Petrolspor (TURKEY5)','data':'3'},{'value':'Kahta (TURKEY5)','data':'1'},{'value':'Fatsa B. (TURKEY5)','data':'8'},{'value':'Baskent G. (TURKEY5)','data':'14'},{'value':'Nevsehirspor (TURKEY5)','data':'13'},{'value':'Siirt Ozel (TURKEY6)','data':'19'},{'value':'Aksaray B. (TURKEY6)','data':'11'},{'value':'Düzcespor (TURKEY6)','data':'13'},{'value':'Yesilyurt B. (TURKEY6)','data':'14'},{'value':'Kizilcaboluk (TURKEY6)','data':'15'},{'value':'Darica G. (TURKEY6)','data':'17'},{'value':'Yomraspor (TURKEY6)','data':'18'},{'value':'Bayrampasa (TURKEY6)','data':'16'},{'value':'Kestel (TURKEY6)','data':'3'},{'value':'Hacettepe (TURKEY6)','data':'1'},{'value':'Orduspor (TURKEY6)','data':'10'},{'value':'Elaziz K. (TURKEY6)','data':'2'},{'value':'Igdir (TURKEY6)','data':'4'},{'value':'Beyoglu Yeni C. (TURKEY6)','data':'5'},{'value':'Altindag B. (TURKEY6)','data':'6'},{'value':'Sile Yildizspor (TURKEY6)','data':'7'},{'value':'Carsambaspor (TURKEY6)','data':'8'},{'value':'Kusadasispor (TURKEY6)','data':'9'},{'value':'Iskenderun (TURKEY6)','data':'12'},{'value':'Derince (TURKEY7)','data':'16'},{'value':'Erokspor (TURKEY7)','data':'17'},{'value':'Ofspor (TURKEY7)','data':'1'},{'value':'Kirikkale B. (TURKEY7)','data':'9'},{'value':'Edirnespor (TURKEY7)','data':'15'},{'value':'Agri 1970 (TURKEY7)','data':'14'},{'value':'Icelspor (TURKEY7)','data':'13'},{'value':'Karakopru B. (TURKEY7)','data':'12'},{'value':'Fethiyespor (TURKEY7)','data':'10'},{'value':'Ceyhanspor (TURKEY7)','data':'8'},{'value':'Tepecik (TURKEY7)','data':'6'},{'value':'Orduspor 1967 (TURKEY7)','data':'5'},{'value':'Modafenspor (TURKEY7)','data':'4'},{'value':'Cankaya FK (TURKEY7)','data':'2'},{'value':'K. Karabukspor (TURKEY7)','data':'11'},{'value':'Karsiyaka (TURKEY7)','data':'18'},{'value':'Gumushanespor (TURKEY7)','data':'7'},{'value':'Mardin BB (TURKEY7)','data':'3'},{'value':'Al Urooba (UAE)','data':'3'},{'value':'Emirates (UAE)','data':'1'},{'value':'Shabab Al Ahli  (UAE)','data':'2'},{'value':'Al Jazira (UAE)','data':'9'},{'value':'Al Nasr (UAE)','data':'6'},{'value':'Al Khaleej (UAE)','data':'7'},{'value':'Al Wahda (UAE)','data':'4'},{'value':'Al Dhafra (UAE)','data':'10'},{'value':'Ajman (UAE)','data':'5'},{'value':'Al Ain (UAE)','data':'8'},{'value':'Al Sharjah (UAE)','data':'13'},{'value':'Al Wasl (UAE)','data':'12'},{'value':'Bani Yas (UAE)','data':'11'},{'value':'Ittihad Kalba (UAE)','data':'14'},{'value':'Al Taawon (UAE2)','data':'15'},{'value':'Gulf Heroes (UAE2)','data':'12'},{'value':'Al Hamriyah (UAE2)','data':'2'},{'value':'Al Ramms (UAE2)','data':'1'},{'value':'Al Bataeh (UAE2)','data':'3'},{'value':'Al Jazira Al H. (UAE2)','data':'11'},{'value':'Masafi (UAE2)','data':'14'},{'value':'Dubai City (UAE2)','data':'13'},{'value':'Al Thaid (UAE2)','data':'8'},{'value':'Dibba Al Hisn (UAE2)','data':'9'},{'value':'Al Arabi (UAE2)','data':'7'},{'value':'Hatta (UAE2)','data':'5'},{'value':'D. Al Fujairah (UAE2)','data':'4'},{'value':'Al Fujairah (UAE2)','data':'6'},{'value':'Masfut (UAE2)','data':'10'},{'value':'Oleksandria (UKRAINE)','data':'12'},{'value':'Dynamo Kiev (UKRAINE)','data':'16'},{'value':'Shakhtar (UKRAINE)','data':'5'},{'value':'Vorskla Poltava (UKRAINE)','data':'13'},{'value':'Zorya Luhansk (UKRAINE)','data':'11'},{'value':'Kolos Kovalivka (UKRAINE)','data':'4'},{'value':'Desna (UKRAINE)','data':'9'},{'value':'FC Lviv (UKRAINE)','data':'1'},{'value':'Rukh Lviv (UKRAINE)','data':'8'},{'value':'Chornomorets (UKRAINE)','data':'10'},{'value':'Veres (UKRAINE)','data':'3'},{'value':'Metalist 1925 (UKRAINE)','data':'7'},{'value':'Dnipro-1 (UKRAINE)','data':'14'},{'value':'Inhulets (UKRAINE)','data':'6'},{'value':'Mariupol (UKRAINE)','data':'2'},{'value':'FC Minaj (UKRAINE)','data':'15'},{'value':'Obolon (UKRAINE2)','data':'10'},{'value':'Alians Lypova (UKRAINE2)','data':'15'},{'value':'Prykarpattia (UKRAINE2)','data':'8'},{'value':'VPK-Ahro (UKRAINE2)','data':'2'},{'value':'Hirnyk-Sport (UKRAINE2)','data':'3'},{'value':'Polessya (UKRAINE2)','data':'14'},{'value':'A. Kramatorsk (UKRAINE2)','data':'4'},{'value':'Kremin (UKRAINE2)','data':'1'},{'value':'Ahrobiznes V. (UKRAINE2)','data':'5'},{'value':'Nyva Ternopil (UKRAINE2)','data':'13'},{'value':'Kryvbas KR (UKRAINE2)','data':'11'},{'value':'M. Kharkiv (UKRAINE2)','data':'16'},{'value':'Olimpik Donetsk (UKRAINE2)','data':'12'},{'value':'Podillya K. (UKRAINE2)','data':'9'},{'value':'Uzhhorod (UKRAINE2)','data':'7'},{'value':'Volyn Lutsk (UKRAINE2)','data':'6'},{'value':'Bukovyna (UKRAINE3)','data':'12'},{'value':'Karpaty Lviv (UKRAINE3)','data':'15'},{'value':'Dnipro Cherkasy (UKRAINE3)','data':'7'},{'value':'Lyubomyr Stavys (UKRAINE3)','data':'5'},{'value':'Obolon B (UKRAINE3)','data':'1'},{'value':'Volyn Lutsk B (UKRAINE3)','data':'5'},{'value':'Nyva Vinnytsya (UKRAINE3)','data':'4'},{'value':'Karpaty Halych (UKRAINE3)','data':'6'},{'value':'Chayka (UKRAINE3)','data':'11'},{'value':'Rubikon (UKRAINE3)','data':'13'},{'value':'Dunayivtsi (UKRAINE3)','data':'3'},{'value':'Kalush (UKRAINE3)','data':'12'},{'value':'Dinaz Vyshhorod (UKRAINE3)','data':'14'},{'value':'Munkács (UKRAINE3)','data':'1'},{'value':'AFSK Kyiv (UKRAINE3)','data':'8'},{'value':'Livyi Bereh (UKRAINE3)','data':'9'},{'value':'Chernihiv (UKRAINE3)','data':'2'},{'value':'LNZ Cherkasy (UKRAINE3)','data':'10'},{'value':'Tavriya (UKRAINE4)','data':'8'},{'value':'Krystal (UKRAINE4)','data':'7'},{'value':'Mykolaiv (UKRAINE4)','data':'11'},{'value':'Nikopol (UKRAINE4)','data':'13'},{'value':'Met. Zaporizhya (UKRAINE4)','data':'16'},{'value':'Real Pharma (UKRAINE4)','data':'10'},{'value':'Peremoga (UKRAINE4)','data':'1'},{'value':'Balkany Zorya (UKRAINE4)','data':'14'},{'value':'Cherkashchyna (UKRAINE4)','data':'13'},{'value':'Nova Kakhovka (UKRAINE4)','data':'9'},{'value':'Yarud Mariupol (UKRAINE4)','data':'3'},{'value':'Sumy (UKRAINE4)','data':'6'},{'value':'Mykolaiv B (UKRAINE4)','data':'9'},{'value':'Skoruk Tomakivk (UKRAINE4)','data':'2'},{'value':'Viktoriya Mykol (UKRAINE4)','data':'4'},{'value':'SK Poltava (UKRAINE4)','data':'5'},{'value':'Vovchansk (UKRAINE4)','data':'15'},{'value':'Trostianets (UKRAINE4)','data':'12'},{'value':'Vorskla U21 (UKRAINE5)','data':'9'},{'value':'Shakhtar U21 (UKRAINE5)','data':'1'},{'value':'Kolos Kov. U21 (UKRAINE5)','data':'2'},{'value':'O. Donetsk U21 (UKRAINE5)','data':'3'},{'value':'Dynamo Kiev U21 (UKRAINE5)','data':'4'},{'value':'Desna U21 (UKRAINE5)','data':'5'},{'value':'Zorya U21 (UKRAINE5)','data':'6'},{'value':'Mariupol U21 (UKRAINE5)','data':'8'},{'value':'Rukh Vynn. U21 (UKRAINE5)','data':'10'},{'value':'Lviv U21 (UKRAINE5)','data':'11'},{'value':'Dnipro-1 U21 (UKRAINE5)','data':'12'},{'value':'Inhulets U21 (UKRAINE5)','data':'13'},{'value':'Minai U21 (UKRAINE5)','data':'14'},{'value':'Oleksandr. U21 (UKRAINE5)','data':'7'},{'value':'Cerrito (URUGUAY2)','data':'4'},{'value':'Villa Espanola (URUGUAY2)','data':'16'},{'value':'Nacional (URUGUAY2)','data':'6'},{'value':'Plaza Colonia (URUGUAY2)','data':'11'},{'value':'Penarol (URUGUAY2)','data':'12'},{'value':'River Plate (URUGUAY2)','data':'3'},{'value':'Liverpool M. (URUGUAY2)','data':'13'},{'value':'Progreso (URUGUAY2)','data':'15'},{'value':'Wanderers (URUGUAY2)','data':'10'},{'value':'Boston River (URUGUAY2)','data':'9'},{'value':'Montevideo City (URUGUAY2)','data':'2'},{'value':'Sud America (URUGUAY2)','data':'1'},{'value':'Rentistas (URUGUAY2)','data':'8'},{'value':'Fenix (URUGUAY2)','data':'7'},{'value':'D. Maldonado (URUGUAY2)','data':'14'},{'value':'Cerro Largo (URUGUAY2)','data':'5'},{'value':'Rampla Juniors (URUGUAY3)','data':'4'},{'value':'Racing CM (URUGUAY3)','data':'9'},{'value':'Central Espanol (URUGUAY3)','data':'2'},{'value':'Atenas (URUGUAY3)','data':'11'},{'value':'Juventud (URUGUAY3)','data':'5'},{'value':'Danubio (URUGUAY3)','data':'6'},{'value':'Rocha (URUGUAY3)','data':'8'},{'value':'Defensor S. (URUGUAY3)','data':'12'},{'value':'Villa Teresa (URUGUAY3)','data':'7'},{'value':'Cerro (URUGUAY3)','data':'10'},{'value':'U. Montevideo (URUGUAY3)','data':'3'},{'value':'Albion (URUGUAY3)','data':'1'},{'value':'Tacuarembo (URUGUAY5)','data':'10'},{'value':'DC United (USA)','data':'15'},{'value':'CF Montreal (USA)','data':'5'},{'value':'Seattle (USA)','data':'3'},{'value':'SJ Earthquakes (USA)','data':'2'},{'value':'Houston Dynamo (USA)','data':'1'},{'value':'Philadelphia (USA)','data':'24'},{'value':'LA Galaxy (USA)','data':'22'},{'value':'Toronto (USA)','data':'6'},{'value':'Inter Miami (USA)','data':'21'},{'value':'New England (USA)','data':'20'},{'value':'Chicago Fire (USA)','data':'19'},{'value':'Cincinnati (USA)','data':'18'},{'value':'Nashville SC (USA)','data':'17'},{'value':'Columbus Crew (USA)','data':'23'},{'value':'New York City (USA)','data':'16'},{'value':'New York RB (USA)','data':'11'},{'value':'Sporting KC (USA)','data':'12'},{'value':'Minnesota Utd (USA)','data':'4'},{'value':'Dallas (USA)','data':'13'},{'value':'Orlando City (USA)','data':'7'},{'value':'Colorado Rapids (USA)','data':'14'},{'value':'Real Salt Lake (USA)','data':'27'},{'value':'Portland (USA)','data':'26'},{'value':'Vancouver (USA)','data':'25'},{'value':'Austin (USA)','data':'10'},{'value':'Los Angeles FC (USA)','data':'9'},{'value':'Atlanta Utd (USA)','data':'8'},{'value':'Orange County (USA2)','data':'31'},{'value':'Memphis (USA2)','data':'30'},{'value':'Austin Bold (USA2)','data':'29'},{'value':'Tacoma Defiance (USA2)','data':'28'},{'value':'Charlotte (USA2)','data':'19'},{'value':'Phoenix Rising (USA2)','data':'9'},{'value':'Real Monarchs (USA2)','data':'27'},{'value':'Loudoun Utd (USA2)','data':'21'},{'value':'Colorado S. (USA2)','data':'17'},{'value':'San Antonio (USA2)','data':'16'},{'value':'New Mexico (USA2)','data':'15'},{'value':'Rio Grande (USA2)','data':'14'},{'value':'Miami FC (USA2)','data':'20'},{'value':'Sporting KC B (USA2)','data':'13'},{'value':'Las Vegas L. (USA2)','data':'22'},{'value':'Indy Eleven (USA2)','data':'12'},{'value':'San Diego Loyal (USA2)','data':'10'},{'value':'Tampa Bay (USA2)','data':'18'},{'value':'Pittsburgh (USA2)','data':'25'},{'value':'Oakland Roots (USA2)','data':'26'},{'value':'Louisville City (USA2)','data':'1'},{'value':'Atlanta Utd B (USA2)','data':'2'},{'value':'Birmingham L. (USA2)','data':'11'},{'value':'FC Tulsa (USA2)','data':'4'},{'value':'Hartford A. (USA2)','data':'8'},{'value':'El Paso (USA2)','data':'24'},{'value':'Charleston (USA2)','data':'23'},{'value':'LA Galaxy B (USA2)','data':'5'},{'value':'Sacramento R. (USA2)','data':'6'},{'value':'New York RB B (USA2)','data':'7'},{'value':'OKC Energy (USA2)','data':'3'},{'value':'Chattanooga RW (USA3)','data':'10'},{'value':'Toronto FC B (USA3)','data':'12'},{'value':'Forward Madison (USA3)','data':'11'},{'value':'Tormenta (USA3)','data':'3'},{'value':'North Carolina (USA3)','data':'9'},{'value':'New England B (USA3)','data':'2'},{'value':'Richmond K. (USA3)','data':'4'},{'value':'Greenville (USA3)','data':'5'},{'value':'Tucson (USA3)','data':'8'},{'value':'Fort Lauderdale (USA3)','data':'1'},{'value':'North Texas (USA3)','data':'7'},{'value':'Union Omaha (USA3)','data':'6'},{'value':'Michigan Stars (USA5)','data':'1'},{'value':'Chicago House (USA5)','data':'4'},{'value':'LA Force (USA5)','data':'8'},{'value':'Stumptown (USA5)','data':'6'},{'value':'San Diego 1904 (USA5)','data':'9'},{'value':'New Amsterdam (USA5)','data':'7'},{'value':'Detroit City (USA5)','data':'3'},{'value':'Maryland B. (USA5)','data':'10'},{'value':'California Utd  (USA5)','data':'2'},{'value':'Chattanooga (USA5)','data':'5'},{'value':'Surkhon (UZBEKISTAN)','data':'11'},{'value':'Qizilqum (UZBEKISTAN)','data':'13'},{'value':'Metallurg (UZBEKISTAN)','data':'12'},{'value':'AMGK (UZBEKISTAN)','data':'1'},{'value':'L. Tashkent (UZBEKISTAN)','data':'2'},{'value':'Navbahor (UZBEKISTAN)','data':'3'},{'value':'Andijan (UZBEKISTAN)','data':'14'},{'value':'Sogdiana (UZBEKISTAN)','data':'4'},{'value':'Turan (UZBEKISTAN)','data':'5'},{'value':'Kokand-1912 (UZBEKISTAN)','data':'6'},{'value':'Nasaf Qarshi (UZBEKISTAN)','data':'7'},{'value':'Pakhtakor (UZBEKISTAN)','data':'8'},{'value':'Bunyodkor (UZBEKISTAN)','data':'9'},{'value':'Mashal (UZBEKISTAN)','data':'10'},{'value':'UCV (VENEZUELA)','data':'14'},{'value':'H. Colmenares (VENEZUELA)','data':'8'},{'value':'Zulia (VENEZUELA)','data':'19'},{'value':'Yaracuyanos (VENEZUELA)','data':'6'},{'value':'A. Venezuela (VENEZUELA)','data':'17'},{'value':'LALA (VENEZUELA)','data':'21'},{'value':'Carabobo (VENEZUELA)','data':'4'},{'value':'Caracas (VENEZUELA)','data':'13'},{'value':'Lara (VENEZUELA)','data':'5'},{'value':'M. de Guayana (VENEZUELA)','data':'16'},{'value':'Zamora (VENEZUELA)','data':'11'},{'value':'Monagas (VENEZUELA)','data':'15'},{'value':'Trujillanos (VENEZUELA)','data':'10'},{'value':'E. Merida (VENEZUELA)','data':'9'},{'value':'Aragua (VENEZUELA)','data':'2'},{'value':'D. La Guaira (VENEZUELA)','data':'1'},{'value':'Puerto Cabello (VENEZUELA)','data':'20'},{'value':'Metropolitanos (VENEZUELA)','data':'18'},{'value':'D. Tachira (VENEZUELA)','data':'7'},{'value':'Gran Valencia (VENEZUELA)','data':'3'},{'value':'Portuguesa (VENEZUELA)','data':'12'},{'value':'Than Quang Ninh (VIETNAM)','data':'12'},{'value':'Hong Linh Ha T. (VIETNAM)','data':'11'},{'value':'Ho Chi Minh (VIETNAM)','data':'10'},{'value':'Da Nang (VIETNAM)','data':'9'},{'value':'Hai Phong (VIETNAM)','data':'8'},{'value':'The Cong (VIETNAM)','data':'7'},{'value':'Thanh Hoa (VIETNAM)','data':'6'},{'value':'Ha Noi (VIETNAM)','data':'2'},{'value':'Nam Dinh (VIETNAM)','data':'1'},{'value':'Sai Gon (VIETNAM)','data':'13'},{'value':'Binh Duong (VIETNAM)','data':'5'},{'value':'Binh Dinh (VIETNAM)','data':'4'},{'value':'Song Lam Nghe (VIETNAM)','data':'3'},{'value':'H. A. Gia Lai (VIETNAM)','data':'14'},{'value':'Pho Hien (VIETNAM2)','data':'11'},{'value':'Long An (VIETNAM2)','data':'12'},{'value':'Quang Nam (VIETNAM2)','data':'10'},{'value':'Binh Phuoc (VIETNAM2)','data':'9'},{'value':'Hue (VIETNAM2)','data':'8'},{'value':'S. Khanh Hoa (VIETNAM2)','data':'6'},{'value':'Phu Tho (VIETNAM2)','data':'5'},{'value':'Ba Ria Vung Tau (VIETNAM2)','data':'4'},{'value':'Can Tho (VIETNAM2)','data':'1'},{'value':'An Giang (VIETNAM2)','data':'3'},{'value':'Cong An Nhan (VIETNAM2)','data':'2'},{'value':'Dak Lak (VIETNAM2)','data':'7'},{'value':'Phu Dong (VIETNAM2)','data':'13'},{'value':'Bala Town (WALES)','data':'7'},{'value':'Caernarfon Town (WALES)','data':'9'},{'value':'Penybont (WALES)','data':'8'},{'value':'Flint (WALES)','data':'12'},{'value':'Newtown (WALES)','data':'1'},{'value':'Haverfordwest (WALES)','data':'10'},{'value':'Connah`s Quay (WALES)','data':'4'},{'value':'Cardiff MU (WALES)','data':'11'},{'value':'Cefn Druids (WALES)','data':'3'},{'value':'Aberystwyth (WALES)','data':'5'},{'value':'Barry Town (WALES)','data':'6'},{'value':'The New Saints (WALES)','data':'2'},{'value':'Chambishi (ZAMBIA)','data':'8'},{'value':'Kitwe Utd (ZAMBIA)','data':'1'},{'value':'Prison Leopards (ZAMBIA)','data':'9'},{'value':'Buildcon (ZAMBIA)','data':'12'},{'value':'Lusaka Dynamos (ZAMBIA)','data':'16'},{'value':'Forest Rangers (ZAMBIA)','data':'10'},{'value':'Nkana (ZAMBIA)','data':'17'},{'value':'Green Buffaloes (ZAMBIA)','data':'15'},{'value':'Red Arrows (ZAMBIA)','data':'4'},{'value':'Zanaco (ZAMBIA)','data':'6'},{'value':'Indeni (ZAMBIA)','data':'1'},{'value':'Konkola Blades (ZAMBIA)','data':'13'},{'value':'Kafue Celtic (ZAMBIA)','data':'7'},{'value':'Kansanshi Dynam (ZAMBIA)','data':'5'},{'value':'Power Dynamos (ZAMBIA)','data':'14'},{'value':'ZESCO Utd (ZAMBIA)','data':'3'},{'value':'NAPSA Stars (ZAMBIA)','data':'15'},{'value':'Nkwazi (ZAMBIA)','data':'18'},{'value':'Lumwana Radiant (ZAMBIA)','data':'13'},{'value':'Green Eagles (ZAMBIA)','data':'11'},{'value':'Kabwe Warriors (ZAMBIA)','data':'2'},{'value':'Y. Green Eagles (ZAMBIA)','data':'18'}]
    for rec in arrayTeam:
        # print("*******************")
        # print(rec)
        # print("--------------------")
        name = rec['value']
        print(name)
        if name.find(".") > 0:
            val=name.split('.')
            slug= unique_slug_generator(val[0])
            string = val[-1]
            league_name = string.replace("(", "")
            league_name = league_name.replace(")", "")
        elif name.find("-") > 0:
            val=name.split('-')
            slug= unique_slug_generator(val[0])
            string = val[-1]
            league_name = string
        else:
            val=name.split(' ')
            slug= unique_slug_generator(val[0])
            string = val[-1]
            league_name = string
        data_id = rec['data']
        league = league_name.lower()
        print(league)
        from db_table.models import Leagues
        leaguesData=Leagues.objects.all().filter(slug_name=league.strip(),collection_datasource="www.soccerstats.com").first()
        print(leaguesData)
        if leaguesData:
            print(leaguesData.league_id)
            league_id = leaguesData.league_id

            Teams.objects.create(
                    name=name,
                    short_code=slug,
                    team_name_odd=slug,
                    league_id=league_id,
                    slug=slug,
                    data_id=data_id,
                    collection_datasource='www.soccerstats.com'
                )
        else:
            Teams.objects.create(
                name=name,
                short_code=slug,
                team_name_odd=slug,
                slug=slug,
                data_id=data_id,
                collection_datasource='www.soccerstats.com'
            )
    data ={"status": 200, "message": "success"}
    return JsonResponse(data)

@csrf_exempt
def GetSeasonLeagueWiseData(request,season_id):
    queryObj = {}
    request_data =[]
    response = []
    queryObj['season_id'] = season_id
    # if 'season_id' in request_data:
    #     queryObj['season_id'] = request_data['season_id']
    # if 'team_id' in request_data:
    #    queryObj['team_id'] = request_data['team_id']
    # if 'league_id' in request_data:
    #    queryObj['league_id'] = request_data['league_id']

    fixer = MatchFixtureUpdate.objects.all().filter(**queryObj)
    result = SeasonWiseTeamDetailSerializer(fixer, many=True).data
    AllTotalMatchHome =0
    AllTotalGoalForHome =0
    AllTotalGoalAgainstHome =0
    AllTotalMatchAway =0
    AllTotalGoalForAway =0
    AllTotalGoalAgainstAway =0
    for rec in result:
        #print(rec['localteam_name'])
        array = []
        total_match_home = 0
        total_goal_for_home =0
        total_goal_against_home =0
        tot_match_away =0
        total_goal_for_away =0
        total_goal_against_away =0
        # print(rec['localteam_name']['win'])
        # print(rec['localteam_name']['draw'])
        # print(rec['localteam_name']['lost'])
        if 'total' in rec['localteam_name']['win']:
            total_match_home= int(rec['localteam_name']['win']['total'])+int(rec['localteam_name']['draw']['total'])+ int(rec['localteam_name']['lost']['total'])
        
        if 'total' in rec['visitorteam_name']['win']:
            tot_match_away= int(rec['visitorteam_name']['win']['total'])+int(rec['visitorteam_name']['draw']['total'])+int(rec['visitorteam_name']['lost']['total'])
        
        if 'total' in rec['localteam_name']['goal_for']:
            total_goal_for_home = int(rec['localteam_name']['goal_for']['total'])
        
        if 'total' in rec['localteam_name']['goals_against']:
            total_goal_against_home = int(rec['localteam_name']['goals_against']['total'])

        if 'total' in rec['visitorteam_name']['goal_for']:
            total_goal_for_away = int(rec['visitorteam_name']['goal_for']['total'])
        
        if 'total' in rec['visitorteam_name']['goals_against']:    
            total_goal_against_away = int(rec['visitorteam_name']['goals_against']['total'])
        
        AllTotalMatchHome = AllTotalMatchHome +total_match_home
        AllTotalGoalForHome = AllTotalGoalForHome + total_goal_for_home
        AllTotalGoalAgainstHome = AllTotalGoalAgainstHome + total_goal_against_home
        AllTotalMatchAway = AllTotalMatchAway + tot_match_away
        AllTotalGoalForAway = AllTotalGoalForAway + total_goal_for_away
        AllTotalGoalAgainstAway = AllTotalGoalAgainstAway + total_goal_against_away

        array.append(
            {
            "home_team_name":rec['localteam_name']['name'],
            "home_win":rec['localteam_name']['win'],
            "home_draw":rec['localteam_name']['draw'],
            "home_lost":rec['localteam_name']['lost'],
            "home_goal_for":rec['localteam_name']['goal_for'],
            "home_goals_against":rec['localteam_name']['goals_against'],
            "away_team_name":rec['visitorteam_name']['name'],
            "away_win":rec['visitorteam_name']['win'],
            "away_draw":rec['visitorteam_name']['draw'],
            "away_lost":rec['visitorteam_name']['lost'],
            "away_goal_for":rec['visitorteam_name']['goal_for'],
            "away_goals_against":rec['visitorteam_name']['goals_against'],
            'winner_team_name':rec['winnerteam_name'],
            'total_match_home':total_match_home,
            'tot_match_away':tot_match_away,
            'total_goal_for_home':total_goal_for_home,
            'total_goal_against_home':total_goal_against_home,
            'total_goal_for_away':total_goal_for_away,
            'total_goal_against_away':total_goal_against_away,
            }
        )
        response.append(array)
    data ={"status": 200, "message": "success" ,"data":response,'AllTotalMatchHome':AllTotalMatchHome,'AllTotalGoalForHome':AllTotalGoalForHome,'AllTotalGoalAgainstHome':AllTotalGoalAgainstHome,'AllTotalMatchAway':AllTotalMatchAway,'AllTotalGoalForAway':AllTotalGoalForAway,'AllTotalGoalAgainstAway':AllTotalGoalAgainstAway,'season_name':'2018-2019'}
    return JsonResponse(data)


#Probability And AI


@csrf_exempt
def MatchTeamInfoByLeague(request):
    request_data = JSONParser().parse(request)
    final_res = {}  
    for req in request_data['league_id']:
        fixtures = MatchFixtureUpdate.objects.all().filter(league_id=req)
        print(req)
        result = MatchFixtureUpdateSerializer(fixtures, many=True).data
        for index, item in enumerate(result):
            req_data = {}
            league_res = GetLeagueByLeagueId(item["league_id"])
            item['league_response'] = league_res
            local_team_id_res = GetTimeSessionByteamId(item["localteam_id"])
            item['local_team_id_response'] =local_team_id_res
            visitorteam_id_res = GetTimeSessionByteamId(item["visitorteam_id"])
            item['visitorteam_id_response'] =visitorteam_id_res
            if item["winnerteam_id"] == item["localteam_id"]:
                item['winner_team'] =local_team_id_res
                # req_data.update({"winner_team": local_team_id_response})
            elif item["winnerteam_id"] == item["visitorteam_id"]:
                item['winner_team'] =visitorteam_id_res
                # req_data.update({"winner_team": visitorteam_id_response})
            else:
                item['winner_team'] = None
        
        final_res[req]=result
        
    data = {"status": 200, "message": "All PlayerSatistics data saved success", "data": final_res}
    return JsonResponse(data)

@csrf_exempt
def GetTeamDetailFromMatch(request):
    request_data = JSONParser().parse(request)
    fixtures = MatchFixtureUpdateSerializer(
        MatchFixtureUpdate.objects.filter (\

            Q(\
                localteam_id=request_data['localteam_id'], \
                visitorteam_id=request_data['visitorteam_id'] \
            ) | \
            Q(
                localteam_id=request_data['visitorteam_id'], \
                visitorteam_id=request_data['localteam_id'] \
            )\

        ), many=True
    ).data
    print(fixtures)
    # fixtures=getTwoTeam(request_data['localteam_id'],request_data['visitorteam_id'])
    data = {"status": 200, "message": "success", "data": fixtures}
    return JsonResponse(data)

@csrf_exempt
def Head2HeadCalculation(request):
    result ={}
    request_data = JSONParser().parse(request)
    result['sanjaya']=head2head(request_data['localteam_id'],request_data['visitorteam_id'])
    result['sportsmonk']=Head2HeadSportsmonk(request_data['localteam_id'],request_data['visitorteam_id'])
    data = {"status": 200, "message": "success", "data": result}
    return JsonResponse(data)

@csrf_exempt
def GetTeamByLeagueName(request):
    teambyleague_result=[]
    # league_ids=[564,384,82,304,1114,8,38,32,42,1560,1351,1969,1560,1351,1092,1949,1968,1929,1971,1805,1950,1972,1506,1969]
    # fixtures = MatchFixtureUpdate.objects.all().filter(league_id__in=league_ids).order_by('-id')
    # for rec in fixtures:
    #     team=GetTeamByteamId(rec.localteam_id)
    #     team2=GetTeamByteamId(rec.visitorteam_id)
    #     teambyleague_result.append(team[0]['name'])
    #     teambyleague_result.append(team2[0]['name'])
    request_data = JSONParser().parse(request)

    team = TeamStatisticsGoalserve.objects.filter(league_ids__contains =request_data['league_id']).all()
    result = TeamStatisticsGoalserveSerializer(team, many=True).data
    data = {"status": 200, "message": "success", "data": result}
    return JsonResponse(data)

@csrf_exempt
def GetTeamByLeagueIds(request):
    teambyleague_result=[]
  
    request_data = JSONParser().parse(request)
    print(request_data)
    team = TeamStatisticsGoalserve.objects.filter(league_ids__contains =request_data['league_ids']).all()[:20]
    result = TeamStatisticsGoalserveSerializer(team, many=True).data
    data = {"status": 200, "message": "success", "data": result}
    return JsonResponse(data)
@csrf_exempt
def GetTeamStatisticsByTeam(request,team_id):
    result =[]
    # GetTeamStandingBySeasonId(718,3468)
    result = GetTeamStatisticsDetailByteamId(team_id)
    for rec in result:
        for res in rec['teamdetail']:
            res['standing'] = GetTeamStandingBySeasonId(res['season_id'],res['team_id'])
    data = {"status": 200, "message": "success", "data": result}
    return JsonResponse(data)

@csrf_exempt
def bannerlist(request):
    banner = Banner.objects.all().filter(is_active =True,is_deleted=False)
    Banner_detail = BannerSerializer(banner, many=True).data
    data = {"status": 200, "message": "success", "data": Banner_detail}
    return JsonResponse(data)

@csrf_exempt
def GetTeamByCompitationIdSportsradar(request):
    from db_table.models import SportsradarTeamData
    result =[]
    request_data = JSONParser().parse(request)
    # print(request_data)
    record=getdatasportsradarteam(request_data['competitor_id'],request_data['competition_id'])
    data = {"status": 200, "message": "success", "data": record}
    
    return JsonResponse(data)

@csrf_exempt
def GetMonthWiseReport(request):
    record=monthwiseReport()
    data = {"status": 200, "message": "success", "data": record}
    
    return JsonResponse(data)