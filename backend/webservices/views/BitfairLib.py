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
import logging
import logging.handlers as handlers
import pandas as pd
import xlwt
dmt_app_log = 'logs/debug.log'
logger = logging.getLogger('betfair.py')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# 5 MB size
logHandler = handlers.RotatingFileHandler(dmt_app_log, maxBytes=5000000, backupCount=10)
logHandler.setLevel(logging.INFO)
# Here we set our logHandler's formatter
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

def str_to_date(str_date):
    match = re.search("\d{2}/\d{2}/\d{4}", str_date)
    obj_date = datetime.datetime.strptime(match.group(), "%d/%m/%Y").date()
    return obj_date

def getEventType(filter):
    
    endpoint = "https://api.betfair.com/exchange/betting/rest/v1.0/"
    header = { 'X-Application' :BeatfairApplicationKey, 'X-Authentication':BeatfairAuthenticationKey,'content-type' : 'application/json' }
    json_req='{"filter":{ }}'
    url = endpoint + "listEventTypes/"
    response = requests.post(url, data=json_req, headers=header)
    res =json.dumps(json.loads(response.text), indent=3)
    # print(res)
    # print(json.dumps(json.loads(response.text), indent=3))
    # data = {
    #     'status':0,
    #     'message': 'Username / password mismatch.'
    # }
    # redis_instance.set('eventType', res)
    # for resp in json.loads(res):
    #     # print (resp['eventType'])
    #     # print (resp['eventType']['id'])
    #     resp = EventType.objects.create(
    #                                     eventtype_id=resp['eventType']['id'],
    #                                     eventtype_name=resp['eventType']['name'],
    #                                     market_count=resp['marketCount']
    #                                 )
    return (json.dumps(json.loads(response.text), indent=3))

def getEventType2(from_date,to_date):
    url = "https://api.betfair.com/exchange/betting/json-rpc/v1"
    header = {'X-Application': BeatfairApplicationKey, 'X-Authentication': BeatfairAuthenticationKey,'content-type': 'application/json'}
    jsonrpc_req = '{"jsonrpc": "2.0", "method":"SportsAPING/v1.0/listEvents", "params": {"filter": {"eventTypeIds": ["1"],"marketStartTime": {"from": "2020-03-13","to": "2022-12-10"}}}, "id": 1}'
    response = requests.post(url, data=jsonrpc_req, headers=header)
    res = json.dumps(json.loads(response.text), indent=3)
    print(res)

    # redis_instance.set('eventType', res)
    # json_res = json.loads(res)
    # for resp in json_res["result"]:
    #     # print(resp['eventType'])
    #     # print(resp['eventType']['id'])
    #     resp = EventType2.objects.create(
    #         eventtype2_id=resp['eventType']['id'],
    #         eventtype2_name=resp['eventType']['name'],
    #         market_count2=resp['marketCount']
    #     )
    return (json.dumps(json.loads(response.text), indent=3))

def getEvents(from_date,to_date):
    Competitions = FootballCompetitions.objects.all().filter(is_active=True)
    for comp in Competitions:

        url = "https://api.betfair.com/exchange/betting/json-rpc/v1"
        header = {'X-Application': BeatfairApplicationKey, 'X-Authentication': BeatfairAuthenticationKey,'content-type': 'application/json'}
        jsonrpc_req = '{"jsonrpc": "2.0","method": "SportsAPING/v1.0/listEvents","params": {"filter": {"eventTypeIds": [1], "CompetitionId":[55] } }}'
        response = requests.post(url, data=jsonrpc_req, headers=header)
        res = json.dumps(json.loads(response.text), indent=3)
        print(jsonrpc_req)

        # redis_instance.set('event', res)
        json_res = json.loads(res)
        if 'result' in json_res:
            for resp in json_res["result"]:
                # print(resp['event'])
                # print(resp['event']['id'])
                cnt =  Events.objects.filter(events_id=resp['event']['id']).count()
                if cnt == 0:
                    print('Create',resp['event']['id'],'--',comp.competition_id)
                    # print(resp['event']['id'])
                    resp = Events.objects.create(
                        events_id=resp['event']['id'],
                        competition_id=comp.competition_id,
                        events_name=resp['event']['name'],
                        events_countrycode=resp['event']['countryCode'] if 'countryCode' in resp['event'] else '' ,
                        events_timezone=resp['event']['timezone'],
                        events_opendate=resp['event']['openDate'],
                        market_counts=resp['marketCount']
                    )
                # else:
                #     print('Edit',resp['event']['id'],'--',comp.competition_id)
                #     # print(resp['event']['id'])
                #     data = Events.objects.get(events_id=resp['event']['id'])
                #     data.events_name=resp['event']['name']
                #     data.competition_id=comp.competition_id
                #     data.events_countrycode=resp['event']['countryCode'] if 'countryCode' in resp['event'] else ''
                #     data.events_timezone=resp['event']['timezone']
                #     data.events_opendate=resp['event']['openDate']
                #     data.market_counts=resp['marketCount']
                #     data.save()
    return (json.dumps(status=2,indent=3))

def getMarketInformation(filter):
    import datetime
    url = "https://api.betfair.com/exchange/betting/json-rpc/v1"
    header = {
        "X-Application": BeatfairApplicationKey,
        "X-Authentication": BeatfairAuthenticationKey,
        "content-type": "application/json",
    }
    today = datetime.date(2022,1,1)
    print(today)
    queryObj = {
        'events_opendate__gte':today
    }
    event = Events.objects.all().filter(**queryObj)
    for evnt in event:
        print(evnt.events_id)
        jsonrpc_req = '{"jsonrpc": "2.0","method": "SportsAPING/v1.0/listMarketCatalogue","params": {"filter": { "eventIds": ['+ str(evnt.events_id) +'] }, "maxResults":"200","marketProjection": ["COMPETITION","EVENT","EVENT_TYPE","RUNNER_DESCRIPTION","RUNNER_METADATA","MARKET_START_TIME"]}, "id": 1 }'
        response = requests.post(url, data=jsonrpc_req, headers=header)
        res = json.dumps(json.loads(response.text), indent=3)
        # print(res)

        # redis_instance.set("market_info", res)
        json_res = json.loads(res)
        if "result" in json_res:
            for resp in json_res["result"]:
                print(resp)
                # print("------------")
                cnt =  MarketInformation.objects.filter(market_id=resp["marketId"]).count()
                if cnt == 0:
                    resp = MarketInformation.objects.create(
                        market_id=resp["marketId"],
                        market_name=resp["marketName"],
                        market_starttime=resp["marketStartTime"],
                        total_matched=resp["totalMatched"],
                        runners=json.dumps(resp["runners"]),
                        eventtype_id=resp["eventType"]["id"],
                        eventtype_name=resp["eventType"]["name"],
                        competition_id=resp["competition"]["id"] if 'competition' in resp and 'id' in resp["competition"] else '' ,
                        competition_name=resp["competition"]["name"] if 'competition' in resp and 'name' in resp["competition"] else '',
                        event_id=resp["event"]["id"],
                        event_name=resp["event"]["name"],
                        event_countrycode=resp["event"]["countryCode"] if 'countryCode' in resp["event"]  else '',
                        event_timezone=resp["event"]["timezone"],
                        event_opendate=resp["event"]["openDate"],
                    )
                    # if 'competition' in resp:
                    #     resp = MarketInformation.objects.create(
                    #         market_id=resp["marketId"],
                    #         market_name=resp["marketName"],
                    #         market_starttime=resp["marketStartTime"],
                    #         total_matched=resp["totalMatched"],
                    #         runners=json.dumps(resp["runners"]),
                    #         eventtype_id=resp["eventType"]["id"],
                    #         eventtype_name=resp["eventType"]["name"],
                    #         competition_id=resp["competition"]["id"] if 'competition' in resp and 'id' in resp["competition"] else '' ,
                    #         competition_name=resp["competition"]["name"] if 'competition' in resp and 'name' in resp["competition"] else '',
                    #         event_id=resp["event"]["id"],
                    #         event_name=resp["event"]["name"],
                    #         event_countrycode=resp["event"]["countryCode"] if 'countryCode' in resp["event"]  else '',
                    #         event_timezone=resp["event"]["timezone"],
                    #         event_opendate=resp["event"]["openDate"],
                    #     )
                    # else:
                    #     resp = MarketInformation.objects.create(
                    #         market_id=resp["marketId"],
                    #         market_name=resp["marketName"],
                    #         market_starttime=resp["marketStartTime"],
                    #         total_matched=resp["totalMatched"],
                    #         runners=json.dumps(resp["runners"]),
                    #         eventtype_id=resp["eventType"]["id"],
                    #         eventtype_name=resp["eventType"]["name"],
                    #         event_id=resp["event"]["id"],
                    #         event_name=resp["event"]["name"],
                    #         event_countrycode=resp["event"]["countryCode"] if 'countryCode' in resp["event"]  else '',
                    #         event_timezone=resp["event"]["timezone"],
                    #         event_opendate=resp["event"]["openDate"]
                    #     )
                else:
                    data = MarketInformation.objects.get(market_id=resp["marketId"])
                    data.market_name=resp["marketName"]
                    data.market_starttime=resp["marketStartTime"]
                    data.total_matched=resp["totalMatched"]
                    data.runners=json.dumps(resp["runners"])
                    data.eventtype_id=resp["eventType"]["id"]
                    data.eventtype_name=resp["eventType"]["name"]
                    data.competition_id=resp["competition"]["id"] if 'competition' in resp and 'id' in resp["competition"] else '' 
                    data.competition_name=resp["competition"]["name"] if 'competition' in resp and 'name' in resp["competition"] else ''
                    data.event_id=resp["event"]["id"]
                    data.event_name=resp["event"]["name"]
                    data.event_countrycode=resp["event"]["countryCode"] if 'countryCode' in resp["event"]  else ''
                    data.event_timezone=resp["event"]["timezone"]
                    data.event_opendate=resp["event"]["openDate"]
                    data.save()
                    # if 'competition' in resp:
                    #     data = MarketInformation.objects.get(market_id=resp["marketId"])
                    #     data.market_name=resp["marketName"]
                    #     data.market_starttime=resp["marketStartTime"]
                    #     data.total_matched=resp["totalMatched"]
                    #     data.runners=json.dumps(resp["runners"])
                    #     data.eventtype_id=resp["eventType"]["id"]
                    #     data.eventtype_name=resp["eventType"]["name"]
                    #     data.competition_id=resp["competition"]["id"] if 'competition' in resp and 'id' in resp["competition"] else '' 
                    #     data.competition_name=resp["competition"]["name"] if 'competition' in resp and 'name' in resp["competition"] else ''
                    #     data.event_id=resp["event"]["id"]
                    #     data.event_name=resp["event"]["name"]
                    #     data.event_countrycode=resp["event"]["countryCode"] if 'countryCode' in resp["event"]  else ''
                    #     data.event_timezone=resp["event"]["timezone"]
                    #     data.event_opendate=resp["event"]["openDate"]
                    #     data.save()
                    # else:
                    #     data = MarketInformation.objects.get(market_id=resp["marketId"])
                    #     data.market_name=resp["marketName"]
                    #     data.market_name=resp["marketName"]
                    #     data.market_starttime=resp["marketStartTime"]
                    #     data.total_matched=resp["totalMatched"]
                    #     data.runners=json.dumps(resp["runners"])
                    #     data.eventtype_id=resp["eventType"]["id"]
                    #     data.eventtype_name=resp["eventType"]["name"]
                    #     data.event_id=resp["event"]["id"]
                    #     data.event_name=resp["event"]["name"]
                    #     data.event_countrycode=resp["event"]["countryCode"] if 'countryCode' in resp["event"]  else ''
                    #     data.event_timezone=resp["event"]["timezone"]
                    #     data.event_opendate=resp["event"]["openDate"]
                    #     data.save()
        else:
            print(res)
    return json.dumps(json.loads(response.text), indent=3)

def getHorseRacing(filter):
    url = "https://api.betfair.com/exchange/betting/json-rpc/v1"
    header = {'X-Application': BeatfairApplicationKey, 'X-Authentication': BeatfairAuthenticationKey,'content-type': 'application/json'}
    jsonrpc_req = '{"jsonrpc": "2.0","method": "SportsAPING/v1.0/listMarketCatalogue", "params": {"filter": { "eventTypeIds": [ 7 ], "marketTypeCodes": ["WIN","PLACE"], "marketStartTime": {"from": "2021-05-04T00:00:00Z","to": "2021-05-04T23:59:00Z" } }, "maxResults": "200","marketProjection": ["MARKET_START_TIME", "RUNNER_METADATA", "RUNNER_DESCRIPTION", "EVENT_TYPE", "EVENT", "COMPETITION"]}, "id": 1 }'
    response = requests.post(url, data=jsonrpc_req, headers=header)
    res = json.dumps(json.loads(response.text), indent=3)
    # print(res)

def getFootballCompetitions(filter):
    url = "https://api.betfair.com/exchange/betting/json-rpc/v1"
    header = {'X-Application': BeatfairApplicationKey, 'X-Authentication': BeatfairAuthenticationKey,'content-type': 'application/json'}
    jsonrpc_req = '{"params": { "filter": {"eventTypeIds": [1] }},  "jsonrpc": "2.0",  "method": "SportsAPING/v1.0/listCompetitions"}'
    response = requests.post(url, data=jsonrpc_req, headers=header)
    res = json.dumps(json.loads(response.text), indent=3)
    # print(res)

    # redis_instance.set('competition', res)
    json_res = json.loads(res)
    for resp in json_res["result"]:
        # print(resp['competition'])
        # print(resp['competition']['id'])
        cnt =  FootballCompetitions.objects.filter(competition_id=resp['competition']['id']).count()
        if cnt == 0:
            resp =  FootballCompetitions.objects.create(
                competition_id=resp['competition']['id'],
                competition_name=resp['competition']['name'],
                market_count=resp['marketCount'],
                competition_region=resp['competitionRegion']
            )
    return (json.dumps(json.loads(response.text), indent=3))

def getPlaceOrders(filter):
    url = "https://api.betfair.com/exchange/betting/json-rpc/v1"
    header = {'X-Application': BeatfairApplicationKey, 'X-Authentication': BeatfairAuthenticationKey,'content-type': 'application/json'}
    queryObj={
        'event_id__in' : [2022802,259241,605621,268416]
    }
    market = MarketInformation.objects.all().filter(**queryObj)
    for mkt in market:
        runners = mkt.runners
        # print(runners)
        rtn = json.loads(runners)
        # print(rtn)
        for rn in rtn:
            print(rn['selectionId'])
            param ={
            "marketId":str(mkt.market_id),
                "instructions": [
                    {
                        "handicap": "0",
                        "orderType": "LIMIT",
                    }
                ]
            }
            jsonrpc_req ='{"jsonrpc": "2.0","method": "SportsAPING/v1.0/placeOrders","params":'+str(param)+', "id": 1}'
            response = requests.post(url, data=jsonrpc_req, headers=header)
            res = json.dumps(json.loads(response.text), indent=3)
            print(res)

    # redis_instance.set('competition', res)
    # json_res = json.loads(res)
    # for resp in json_res["result"]:
    #     print(resp['competition'])
    #     print(resp['competition']['id'])
    #     resp = PlaceOrders.objects.create(
    #         status=resp['competition']['id'],
    #         market_id =resp['competition']['name'],
    #         instruction_status=resp['marketCount'],
    #         instruction_selectionid =resp['competitionRegion'],
    #         instruction_handicap =resp['competitionRegion'],
    #         instruction_limitordersize =resp['competitionRegion'],
    #         instruction_limitorderprice=resp['competitionRegion'],
    #         instruction_limitorder_persistenceType =resp['competitionRegion'],
    #         instruction_ordertype =resp['competitionRegion'],
    #         instruction_side=resp['competitionRegion'],
    #         betid=resp['competitionRegion'],
    #         placedDate=resp['competitionRegion'],
    #         averagepriceMatched=resp['competitionRegion'],
    #         sizeMatched=resp['competitionRegion'],
    #         orderstatus =resp['competitionRegion'],
    #     )
    # return (json.dumps(json.loads(response.text), indent=3))
    return rtn
def getPlaceOrdersspbet(market_id,selectionId):
    url = "https://api.betfair.com/exchange/betting/json-rpc/v1"
    header = {'X-Application': BeatfairApplicationKey, 'X-Authentication': BeatfairAuthenticationKey,'content-type': 'application/json'}
    jsonrpc_req ='{"jsonrpc": "2.0","method": "SportsAPING/v1.0/placeOrders","params": {"marketId": "'+market_id+'", "instructions": [{ "selectionId": "'+selectionId+'", "handicap": "0","side": "BACK","orderType": "MARKET_ON_CLOSE", "marketOnCloseOrder": { "liability": "2"} } ] }, "id": 1 }'
    print(jsonrpc_req)
    response = requests.post(url, data=jsonrpc_req, headers=header)
    res = json.dumps(json.loads(response.text), indent=3)
    print("-----------")
    print(res)

def getListcurrentOrders(market_id):
    url = "https://api.betfair.com/exchange/betting/json-rpc/v1"
    header = {'X-Application': BeatfairApplicationKey, 'X-Authentication': BeatfairAuthenticationKey,'content-type': 'application/json'}
    jsonrpc_req ='{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listCurrentOrders","params":{"marketIds":["'+market_id+'"],"orderProjection":"ALL","dateRange":{}}, "id":1}'
    response = requests.post(url, data=jsonrpc_req, headers=header)
    res = json.dumps(json.loads(response.text), indent=3)
    print(res)

def  getListmarketbook(market_id):
    url = "https://api.betfair.com/exchange/betting/json-rpc/v1"
    header = {'X-Application': BeatfairApplicationKey, 'X-Authentication': BeatfairAuthenticationKey,'content-type': 'application/json'}
    jsonrpc_req ='{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketBook", "params":{"marketIds":['+str(market_id)+'],"priceProjection":{"priceData": ["EX_BEST_OFFERS", "EX_TRADED"],"virtualise": "true"}}, "id": 1}'
    response = requests.post(url, data=jsonrpc_req, headers=header)
    res = json.dumps(json.loads(response.text), indent=3)
    # print(res)
    json_res = json.loads(res)
    # print(json_res)

    for resp in json_res["result"]:
        # print(resp)
        # print("------------")
        cnt =  Listmarketbook.objects.filter(market_id=resp["marketId"]).count()
        if cnt == 0 :
            print('Create')
            print(resp["marketId"])
            crt = Listmarketbook.objects.create(
                market_id=resp["marketId"],
                is_marketdatadelayed=resp["isMarketDataDelayed"],
                status=resp["status"],
                betdelay=resp["betDelay"],
                runners=json.dumps(resp["runners"]),
                bspreconciled=resp["bspReconciled"],
                complete=resp["complete"],
                inplay=resp["inplay"] ,
                numberofwinners=resp["numberOfWinners"],
                numberofrunners=resp["numberOfRunners"],
                numberofactiverunners=resp["numberOfActiveRunners"],
                #lastmatchtime=resp["lastMatchTime"] if 'lastMatchTime' in resp else '0000-00-00',
                totalmatched=resp["totalMatched"],
                totalavailable=resp["totalAvailable"],
                crossmatching=resp["crossMatching"],
                runnersvoidable = resp["runnersVoidable"],
                version = resp["version"]
            )
        else:
            print('Update')
            print(resp["marketId"])
            data = Listmarketbook.objects.get(market_id=resp["marketId"])
            data.is_marketdatadelayed=resp["isMarketDataDelayed"]
            data.status=resp["status"]
            data.betdelay=resp["betDelay"]
            data.runners=json.dumps(resp["runners"])
            data.bspreconciled=resp["bspReconciled"]
            data.complete=resp["complete"]
            data.inplay=resp["inplay"] 
            data.numberofwinners=resp["numberOfWinners"]
            data.numberofrunners=resp["numberOfRunners"]
            data.numberofactiverunners=resp["numberOfActiveRunners"]
            # data.lastmatchtime=resp["lastMatchTime"]
            data.totalmatched=resp["totalMatched"]
            data.totalavailable=resp["totalAvailable"]
            data.crossmatching=resp["crossMatching"]
            data.runnersvoidable = resp["runnersVoidable"]
            data.version = resp["version"]

    
    # print(res)
    return json_res

def  getMarketPrices(filter):
    url = "https://api.betfair.com/exchange/betting/json-rpc/v1"
    header = {'X-Application': BeatfairApplicationKey, 'X-Authentication': BeatfairAuthenticationKey,'content-type': 'application/json'}
    jsonrpc_req ='{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketBook","params": {"marketIds": ["1.207341523"], "priceProjection": {"priceData": ["EX_BEST_OFFERS", "EX_TRADED"],"virtualise": "true"} }, "id": 1}'
    response = requests.post(url, data=jsonrpc_req, headers=header)
    res = json.dumps(json.loads(response.text), indent=3)
    print(res)

def RemoveDuplicate(request=''):
    from datetime import datetime
    rows = predictionOddsSportsradar.objects.all()
    for row in rows:
        try:
            predictionOddsSportsradar.objects.get(home_team_name =row.away_team_name)
        except:
            print(row.match_id)
            row.delete()

def getTennisComoitation(filter):
    url = "https://api.betfair.com/exchange/betting/json-rpc/v1"
    header = {'X-Application': BeatfairApplicationKey, 'X-Authentication': BeatfairAuthenticationKey,'content-type': 'application/json'}
    jsonrpc_req = '{"params": { "filter": {"eventTypeIds": [2] }},  "jsonrpc": "2.0",  "method": "SportsAPING/v1.0/listCompetitions"}'
    response = requests.post(url, data=jsonrpc_req, headers=header)
    res = json.dumps(json.loads(response.text), indent=3)
    # print(res)
    # redis_instance.set('competition', res)
    # json_res = json.loads(res)
    
    return (json.dumps(json.loads(response.text), indent=3))


# Get Data from Sports Monker

def get_countries(request, id=None):
    endpoint = "https://soccer.sportmonks.com/api/v2.0/countries"

    if id:
        url = endpoint + "/" + str(id) + "?api_token=" + football_token
        response = requests.get(url)
        res = json.dumps(json.loads(response.text), indent=3)
    else:
        url = endpoint + "?api_token=" + football_token
        response = requests.get(url)
        res = json.dumps(json.loads(response.text), indent=3)

    return res

def get_leagues(request, id=None, country_id=None):
    endpoint = "https://soccer.sportmonks.com/api/v2.0/leagues"

    if id:
        url = endpoint + "/" + str(id) + "?api_token=" + football_token
        response = requests.get(url)
        league_res = json.dumps(json.loads(response.text), indent=3)
        res = leagues_save(league_res)
    elif country_id:
        url = (
            "https://soccer.sportmonks.com/api/v2.0/countries/"
            + str(country_id)
            + "/leagues?api_token="
            + football_token
        )
        response = requests.get(url)
        res = json.dumps(json.loads(response.text), indent=3)
    else:
        url = endpoint + "?api_token=" + football_token
        response = requests.get(url)
        res = json.dumps(json.loads(response.text), indent=3)
        # redis_instance.set("leagues", res)
        json_res = json.loads(res)
        for resp in json_res["data"]:
            cnt = Leagues.objects.filter(league_id=resp["id"]).count()
            if cnt == 0:
                Leagues.objects.create(
                    league_id=resp["id"],
                    active=resp["active"],
                    type=resp["type"],
                    legacy_id=resp["legacy_id"],
                    country_id=resp["country_id"],
                    logo_path=resp["logo_path"],
                    name=resp["name"],
                    is_cup=resp["is_cup"],
                    season_id=resp["current_season_id"],
                    round_id=resp["current_round_id"],
                    stage_id=resp["current_stage_id"],
                    live_standings=resp["live_standings"],
                    predictions=resp["coverage"]["predictions"],
                    topscorer_goals=resp["coverage"]["topscorer_goals"],
                    topscorer_assists=resp["coverage"]["topscorer_assists"],
                    topscorer_cards=resp["coverage"]["topscorer_cards"],
                )
            else:
                data = Leagues.objects.get(league_id=resp["id"])
                data.league_id = resp["id"]
                data.active = resp["active"]
                data.type = resp["type"]
                data.legacy_id = resp["legacy_id"]
                data.country_id = resp["country_id"]
                data.logo_path = resp["logo_path"]
                data.name = resp["name"]
                data.is_cup = resp["is_cup"]
                data.season_id = resp["current_season_id"]
                data.round_id = resp["current_round_id"]
                data.stage_id = resp["current_stage_id"]
                data.live_standings = resp["live_standings"]
                data.predictions = resp["coverage"]["predictions"]
                data.topscorer_goals = resp["coverage"]["topscorer_goals"]
                data.topscorer_assists = resp["coverage"]["topscorer_assists"]
                data.topscorer_cards = resp["coverage"]["topscorer_cards"]
                data.save()
    return res

def search_by_league(request, league_name=None):
    endpoint = "https://soccer.sportmonks.com/api/v2.0/leagues/search"
    url = endpoint + "/" + league_name + "?api_token=" + football_token
    response = requests.get(url)
    res = json.dumps(json.loads(response.text), indent=3)
    return res
def SaveTeamBySeason(season_id):
    from db_table.models import Teams
    endpoint = "https://soccer.sportmonks.com/api/v2.0/teams/season"
    url = endpoint + "/" + str(season_id) + "?api_token=" + football_token
    print(url)
    response = requests.get(url)
    res = json.dumps(json.loads(response.text), indent=3)
    json_res = json.loads(res)
    resp=json_res["data"]
    if "data" in json_res:
        for resp in json_res["data"]:
            cnt = Teams.objects.filter(team_id=resp["id"],season_id=season_id).count()
            print(cnt)
            if cnt == 0:
                # print(resp)
                tid = str(resp["id"])+str(season_id)
                tid = int(tid)
                Teams.objects.create(
                    id =tid,
                    team_id=resp["id"],
                    legacy_id=resp["legacy_id"],
                    name=resp["name"],
                    short_code=resp["short_code"],
                    twitter=resp["twitter"],
                    country_id=resp["country_id"],
                    national_team=resp["national_team"],
                    founded=resp["founded"],
                    logo_path=resp["logo_path"],
                    venue_id=resp["venue_id"],
                    season_id=season_id,
                    is_placeholder=resp["is_placeholder"],
                    current_season_id =resp["current_season_id"],
                )
                
    
    return res

def get_player(request, id=None, country_id=None, name=None):
    endpoint = "https://soccer.sportmonks.com/api/v2.0/players"
    if id:
        url = endpoint + "/" + str(id) + "?api_token=" + football_token
        response = requests.get(url)
        res = json.dumps(json.loads(response.text), indent=3)
        # redis_instance.set(" player", res)
        # json_res = json.loads(res)
        # # for resp in json_res["data"]:
        # resp=json_res['data']
        # try:
        #     Players.objects.get(common_name=resp["common_name"],display_name=resp["display_name"],
        #         fullname=resp["fullname"])
        # except Players.DoesNotExist:
        #     Players.objects.create(
        #         player_id=resp["player_id"],
        #         team_id=resp["team_id"],
        #         country_id=resp["country_id"],
        #         position_id=resp["position_id"],
        #         common_name=resp["common_name"],
        #         display_name=resp["display_name"],
        #         fullname=resp["fullname"],
        #         firstname=resp["firstname"],
        #         lastname=resp["lastname"],
        #         nationality=resp["nationality"],
        #         birthdate=parse_date(resp["birthdate"]),
        #         birthcountry=resp["birthcountry"],
        #         birthplace=resp["birthplace"],
        #         height=resp["height"],
        #         weight=resp["weight"],
        #         image_path=resp["image_path"],
        #     )
    elif country_id:
        url = (
            "https://soccer.sportmonks.com/api/v2.0/countries"
            + "/"
            + str(country_id)
            + "/players?api_token="
            + football_token
        )
        response = requests.get(url)
        res = json.dumps(json.loads(response.text), indent=3)
        # redis_instance.set(" player", res)
        json_res = json.loads(res)
        for resp in json_res["data"]:
            cnt = Players.objects.filter(player_id=resp["player_id"]).count()
            if cnt == 0 :
                data= Players.objects.create(
                    player_id=resp["player_id"],
                    team_id=resp["team_id"],
                    country_id=resp["country_id"],
                    position_id=resp["position_id"],
                    common_name=resp["common_name"],
                    display_name=resp["display_name"],
                    fullname=resp["fullname"],
                    firstname=resp["firstname"],
                    lastname=resp["lastname"],
                    nationality=resp["nationality"],
                    # birthdate=str_to_date(resp["birthdate"]),
                    birthcountry=resp["birthcountry"],
                    birthplace=resp["birthplace"],
                    height=resp["height"],
                    weight=resp["weight"],
                    image_path=resp["image_path"],
                )
                try:
                    data.birthdate=str_to_date(resp["birthdate"])
                    data.save()
                except TypeError:
                    data.birthdate = None
                    data.save()
                data = Players.objects.latest('id')
                parent_player_id = data.id
                # print(parent_player_id)
                if parent_player_id >0:
                    get_player_stats(request, resp["player_id"],parent_player_id)
            # else:
            #     plr = Players.objects.filter(player_id=resp["player_id"]).first()
            #     print(plr)
            #     get_player_stats(request, resp["player_id"],plr[0]['parent_player_id'])

    elif name:
        url = "https://soccer.sportmonks.com/api/v2.0/players/search/" + name + "?api_token=" + football_token
        response = requests.get(url)
        res = json.dumps(json.loads(response.text), indent=3)
    else:
        return {}
    return res

def get_teams(request, id=None, country_id=None):
    endpoint = "https://soccer.sportmonks.com/api/v2.0/teams"
    if id:
        url = endpoint + "/" + str(id) + "?api_token=" + football_token
        response = requests.get(url)
        res = json.dumps(json.loads(response.text), indent=3)
        # redis_instance.set("teams", res)
        json_res = json.loads(res)
        # for resp in json_res["data"]:
        if "data" in json_res:
            resp=json_res["data"]
            cnt = Teams.objects.filter(Q(team_id=resp["id"]),Q(collection_datasource="")).count()
            print(url)
            print(cnt)
            print("--------")
            if cnt == 0:
                Teams.objects.create(
                    team_id=resp["id"],
                    legacy_id=resp["legacy_id"],
                    name=resp["name"],
                    short_code=resp["short_code"],
                    twitter=resp["twitter"],
                    country_id=resp["country_id"],
                    national_team=resp["national_team"],
                    founded=resp["founded"],
                    logo_path=resp["logo_path"],
                    venue_id=resp["venue_id"],
                    season_id=resp["current_season_id"],
                    is_placeholder=resp["is_placeholder"],
                )
    elif country_id:
        url = (
            "https://soccer.sportmonks.com/api/v2.0/countries"
            + "/"
            + str(country_id)
            + "/teams?api_token="
            + football_token
        )
        response = requests.get(url)
        res = json.dumps(json.loads(response.text), indent=3)
        # redis_instance.set("teams", res)
        json_res = json.loads(res)
        # resp = json_res["data"]
        for resp in json_res["data"]:
            cnt = Teams.objects.filter(team_id=resp["id"]).count()
            if cnt == 0:
                Teams.objects.create(
                    team_id=resp["id"],
                    legacy_id=resp["legacy_id"],
                    name=resp["name"],
                    short_code=resp["short_code"],
                    twitter=resp["twitter"],
                    country_id=resp["country_id"],
                    national_team=resp["national_team"],
                    founded=resp["founded"],
                    logo_path=resp["logo_path"],
                    venue_id=resp["venue_id"],
                    season_id=resp["current_season_id"],
                    is_placeholder=resp["is_placeholder"],
                )
            else:
                data = Teams.objects.get(team_id=resp["id"])
                data.team_id = resp["id"]
                data.legacy_id = resp["legacy_id"]
                data.name = resp["name"]
                data.short_code = resp["short_code"]
                data.twitter = resp["twitter"]
                data.country_id = resp["country_id"]
                data.national_team = resp["national_team"]
                data.founded = resp["founded"]
                data.logo_path = resp["logo_path"]
                data.venue_id = resp["venue_id"]
                data.season_id = resp["current_season_id"]
                data.is_placeholder = resp["is_placeholder"]
                data.save()

    else:
        return {}

    return res

def get_teamssquads(request, id=None):
    endpoint =  "https://soccer.sportmonks.com/api/v2.0/teams"
    url = endpoint+ "/" + str(id) + "?include=" +squad.player+ "?api_token=" + football_token
    # print(url)
    response = requests.get(url)
    res = json.dumps(json.loads(response.text), indent=3)
    return res

def get_teambyseason(request, id=None):
    endpoint = "https://soccer.sportmonks.com/api/v2.0/teams/season"

    if id:
        url = endpoint + "/" + str(id) + "?api_token=" + football_token
        response = requests.get(url)
        res = json.dumps(json.loads(response.text), indent=3)
        return res

def search_by_team(request, team_name=None):
    endpoint = "https://soccer.sportmonks.com/api/v2.0/teams/search"
    url = endpoint + "/" + team_name + "?api_token=" + football_token
    response = requests.get(url)
    res = json.dumps(json.loads(response.text), indent=3)
    return res

def get_currentleaguesbyteamid(request, team_id=None):
    endpoint = "https://soccer.sportmonks.com/api/v2.0/teams"
    url =(
            endpoint+"/"
            + str(team_id)
            + "/current?api_token="
            + football_token
        )
    # print(url)
    response = requests.get(url)
    res = json.dumps(json.loads(response.text), indent=3)
    return res

def get_allleaguesbyteamid(request, team_id=None):
    endpoint = "https://soccer.sportmonks.com/api/v2.0/teams"
    url =(
            endpoint+"/"
            + str(team_id)
            + "/history?api_token="
            + football_token
        )
    # print(url)
    response = requests.get(url)
    res = json.dumps(json.loads(response.text), indent=3)
    return res

def get_oddsList(request, fixture_id=None, bookmarker_id=None):
    endpoint = f"https://soccer.sportmonks.com/api/v2.0/odds/fixture"
    url = (
            endpoint + "/"
            + str(fixture_id)
            +"/bookmaker"
            +"/"
            +str(bookmarker_id)
            + "?api_token="
            + football_token
    )
    # print(url)
    response = requests.get(url)
    res = json.dumps(json.loads(response.text), indent=3)
    return res

def  get_oddsbyfixtureidList(request, fixture_id=None):
    endpoint = "https://soccer.sportmonks.com/api/v2.0/odds/fixture"
    url = (
            endpoint + "/"
            + str(fixture_id)
            + "?api_token="
            + football_token
    )
    response = requests.get(url)
    odds_res = json.dumps(json.loads(response.text), indent=3)
    res = odds_save(odds_res)
    return res

def get_oddsmarketList(request, fixture_id=None, market_id=None):
    endpoint = f"https://soccer.sportmonks.com/api/v2.0/odds/fixture"
    url = (
            endpoint + "/"
            + str(fixture_id)
            +"/market"
            +"/"
            +str(market_id)
            + "?api_token="
            + football_token
    )
    # print(url)
    response = requests.get(url)
    res = json.dumps(json.loads(response.text), indent=3)
    return res

def get_inplayoddsbyfixtureidList(request, fixture_id=None):
    endpoint = "https://soccer.sportmonks.com/api/v2.0/odds/inplay/fixture"
    url = (
            endpoint + "/"
            + str(fixture_id)
            + "?api_token="
            + football_token
    )

    # print(url)
    response = requests.get(url)
    res = json.dumps(json.loads(response.text), indent=3)
    return res

def get_standingseasonlist(request, season_id=None):
    endpoint = "https://soccer.sportmonks.com/api/v2.0/standings/season"
    url = (
            endpoint + "/"
            + str(season_id)
            + "?api_token="
            + football_token
    )

    response = requests.get(url)
    season_res = json.dumps(json.loads(response.text), indent=3)
    res = season_save(season_res)
    # redis_instance.set("season", res)
    # json_res = json.loads(res)
    # for resp in json_res["data"]:
    #     try:
    #         Season.objects.get(name=resp["name"])
    #     except Season.DoesNotExist:
    #         for nresp in resp["standings"]["data"]:
    #             Season.objects.create(
    #                 seasonid=resp["id"],
    #                 name=resp["name"],
    #                 league_id=resp["league_id"],
    #                 season_id=resp["season_id"],
    #                 round_id=resp["round_id"],
    #                 round_name=resp["round_name"],
    #                 type=resp["type"],
    #                 stage_id=resp["stage_id"],
    #                 stage_name=resp["stage_name"],
    #                 resource=resp["resource"],
    #                 # position=nresp["position"],
    #                 team_id=nresp["team_id"],
    #                 team_name=nresp["team_name"],
    #                 group_id=nresp["group_id"],
    #                 group_name=nresp["group_name"],
    #                 overall=nresp["overall"],
    #                 home=nresp["home"],
    #                 away=nresp["away"],
    #                 total=nresp["total"],
    #                 result=nresp["result"],
    #                 points=nresp["points"],
    #                 recent_form=nresp["recent_form"],
    #                 status=nresp["status"],
    #             )
    # # print("data saved success")
    return res

def get_standingliveseasonlist(request, season_id=None):
    endpoint = "https://soccer.sportmonks.com/api/v2.0/standings/season/live"
    url = (
            endpoint + "/"
            + str(season_id)
            + "?api_token="
            + football_token
    )

    # print(url)
    response = requests.get(url)
    res = json.dumps(json.loads(response.text), indent=3)
    return res

def get_standingbyseasonroundid(request, season_id=None, round_id=None):
    endpoint = "https://soccer.sportmonks.com/api/v2.0/standings/season"
    url = (
            endpoint + "/"
            + str(season_id)
            +"/round"
            +"/"
            +str(round_id)
            + "?api_token="
            + football_token
    )
    # print(url)
    response = requests.get(url)
    res = json.dumps(json.loads(response.text), indent=3)
    return res

def get_standingbyseasondate(request, start_date=None,season_id=None):
    endpoint = "https://soccer.sportmonks.com/api/v2.0/standings/season"
    url = (
            endpoint + "/"
            + str(season_id)
            + "/date"
            + "/"
            + str(start_date)
            + "?api_token="
            + football_token
    )
    # print(url)
    response = requests.get(url)
    res = json.dumps(json.loads(response.text), indent=3)
    return res

def get_correctionsbyseasonid(request, season_id=None):
    endpoint = "https://soccer.sportmonks.com/api/v2.0/corrections/season"
    url = (
            endpoint + "/"
            + str(season_id)
            + "?api_token="
            + football_token
    )

    # print(url)
    response = requests.get(url)
    res = json.dumps(json.loads(response.text), indent=3)
    return res

def getfixtureFromSportsmonk(today,week,league_ids):
    result =[]
    endpoint = "https://soccer.sportmonks.com/api/v2.0/fixtures/between/"+str(today)+"/"+str(week)
    # endpoint = "https://soccer.sportmonks.com/api/v2.0/fixtures/updates"
    url = endpoint + "?api_token=" + football_token
    print(url)
    response = requests.get(url)
    res = json.dumps(json.loads(response.text), indent=3)
    json_res = json.loads(res)
    if 'data' in json_res:
        return json_res["data"]
    else:
        return result

    # if 'meta' in json_res:
    #     pagination =  json_res["meta"]["pagination"]
    #     currentpage = int(pagination["current_page"])
    #     total_page = (pagination["total_pages"])
    #     for currentpage in range(total_page):
    #         endpoint = "https://soccer.sportmonks.com/api/v2.0/fixtures/between/"+str(today)+"/"+str(week)
    #         url1 = endpoint + "?api_token=" + football_token+"&page="+str(currentpage)
    #         response1 = requests.get(url1)
    #         res1 = json.dumps(json.loads(response1.text), indent=3)
    #         json_res1 = json.loads(res1)
    #         for resp in json_res1["data"]:
    #             if resp['league_id'] in league_ids:
    #                 result.append(resp)
    #     return result
    # else:
    #     return result

def get_match_fixture(request, fixture_id=None):
    if fixture_id:
        endpoint = "https://soccer.sportmonks.com/api/v2.0/fixtures/{fixture_id}".format(fixture_id=fixture_id)
        url = endpoint + "?api_token=" + football_token
        response = requests.get(url)
        # print(url)
        res = json.dumps(json.loads(response.text), indent=3)
        # redis_instance.set("fixture", res)
        json_res = json.loads(res)
        resp = json_res["data"]
        print(resp["id"])
        cnt = Fixture.objects.filter(fixture_id=resp["id"]).count()
        if cnt == 0:
            Fixture.objects.create(
                fixture_id=resp["id"],
                league_id=resp["league_id"],
                season_id=resp["season_id"],
                stage_id=resp["stage_id"],
                round_id=resp["round_id"],
                group_id=resp["group_id"],
                aggregate_id=resp["aggregate_id"],
                venue_id=resp["venue_id"],
                referee_id=resp["referee_id"],
                localteam_id=resp["localteam_id"],
                visitorteam_id=resp["visitorteam_id"],
                winnerteam_id=resp["winner_team_id"],
                weather_report=json.dumps(resp["weather_report"]),
                commentaries=resp["commentaries"],
                attendance=resp["attendance"],
                pitch=resp["pitch"],
                details=resp["details"],
                neutral_venue=resp["neutral_venue"],
                winning_odds_calculated=resp["winning_odds_calculated"],
                formations=json.dumps(resp["formations"]),
                scores=json.dumps(resp["scores"]),
                time=json.dumps(resp["time"]),
                coaches=json.dumps(resp["coaches"]),
                standings=json.dumps(resp["standings"]),
                assistants=json.dumps(resp["assistants"]),
                leg=resp["leg"],
                colors=json.dumps(resp["colors"]),
                deleted=resp["deleted"],
                is_placeholder=resp["is_placeholder"],
                # time_date=resp["time"]["starting_at"]["date"]
            )
    else:
        endpoint = "https://soccer.sportmonks.com/api/v2.0/fixtures/updates"
        url = endpoint + "?api_token=" + football_token
        response = requests.get(url)
        res = json.dumps(json.loads(response.text), indent=3)
        # redis_instance.set("fixtureupdate", res)
        json_res = json.loads(res)
        for resp in json_res["data"]:
            cnt = MatchFixtureUpdate.objects.filter(matchid=resp["id"]).count()
            print(resp["id"])
            if cnt == 0:
                MatchFixtureUpdate.objects.create(
                    matchid=resp["id"],
                    league_id=resp["league_id"],
                    season_id=resp["season_id"],
                    stage_id=resp["stage_id"],
                    round_id=resp["round_id"],
                    group_id=resp["group_id"],
                    aggregate_id=resp["aggregate_id"],
                    venue_id=resp["venue_id"],
                    referee_id=resp["referee_id"],
                    localteam_id=resp["localteam_id"],
                    visitorteam_id=resp["visitorteam_id"],
                    winnerteam_id=resp["winner_team_id"],
                    weather_report=json.dumps(resp["weather_report"]),
                    commentaries=resp["commentaries"],
                    attendance=resp["attendance"],
                    pitch=resp["pitch"],
                    details=resp["details"],
                    neutral_venue=resp["neutral_venue"],
                    winning_odds_calculated=resp["winning_odds_calculated"],
                    formations=json.dumps(resp["formations"]),
                    scores=json.dumps(resp["scores"]),
                    time=json.dumps(resp["time"]),
                    coaches=json.dumps(resp["coaches"]),
                    standings=json.dumps(resp["standings"]),
                    assistants=json.dumps(resp["assistants"]),
                    leg=resp["leg"],
                    colors=json.dumps(resp["colors"]),
                    deleted=resp["deleted"],
                    is_placeholder=resp["is_placeholder"],
                    time_date=resp["time"]["starting_at"]["date"]
                )
            # else:
            #     data = MatchFixtureUpdate.objects.get(matchid=resp["id"])
            #     data.matchid = resp["id"]
            #     data.league_id = resp["league_id"]
            #     data.season_id = resp["season_id"]
            #     data.stage_id = resp["stage_id"]
            #     data.round_id = resp["round_id"]
            #     data.group_id = resp["group_id"]
            #     data.aggregate_id = resp["aggregate_id"]
            #     data.venue_id = resp["venue_id"]
            #     data.referee_id = resp["referee_id"]
            #     data.localteam_id = resp["localteam_id"]
            #     data.visitorteam_id = resp["visitorteam_id"]
            #     data.winnerteam_id = resp["winner_team_id"]
            #     data.weather_report = json.dumps(resp["weather_report"])
            #     data.commentaries = resp["commentaries"]
            #     data.attendance = resp["attendance"]
            #     data.pitch = resp["pitch"]
            #     data.details = resp["details"]
            #     data.neutral_venue = resp["neutral_venue"]
            #     data.winning_odds_calculated = resp["winning_odds_calculated"]
            #     data.formations = json.dumps(resp["formations"])
            #     data.scores = json.dumps(resp["scores"])
            #     data.time = json.dumps(resp["time"])
            #     data.coaches = json.dumps(resp["coaches"])
            #     data.standings = json.dumps(resp["standings"])
            #     data.assistants = json.dumps(resp["assistants"])
            #     data.leg = resp["leg"]
            #     data.colors = json.dumps(resp["colors"])
            #     data.deleted = resp["deleted"]
            #     data.is_placeholder = resp["is_placeholder"]
            #     data.time_date = resp["time"]["starting_at"]["date"]
            #     data.save()
    return res

def fixture_by_date(request, start_date=None, end_date=None, team_id=None):
    if start_date and not end_date and not team_id:
        endpoint = "https://soccer.sportmonks.com/api/v2.0/fixtures/date/{date}".format(date=start_date)
    elif start_date and end_date and not team_id:
        endpoint = "https://soccer.sportmonks.com/api/v2.0/fixtures/between/{s_date}/{e_date}".format(
            s_date=start_date, e_date=end_date
        )
    elif start_date and end_date and team_id:
        endpoint = "https://soccer.sportmonks.com/api/v2.0/fixtures/between/{s_date}/{e_date}/{team_id}".format(
            s_date=start_date, e_date=end_date, team_id=team_id
        )
    else:
        return {}
    url = endpoint + "?api_token=" + football_token
    response = requests.get(url)
    res = json.dumps(json.loads(response.text), indent=3)
    json_res = json.loads(res)
    for resp in json_res["data"]:
        cnt = MatchFixtureUpdate.objects.filter(matchid=resp["id"]).count()
        print(resp["id"])
        print(resp["league_id"])
        print("rabi")
        if cnt == 0:
            MatchFixtureUpdate.objects.create(
                matchid=resp["id"],
                league_id=resp["league_id"],
                season_id=resp["season_id"],
                stage_id=resp["stage_id"],
                round_id=resp["round_id"],
                group_id=resp["group_id"],
                aggregate_id=resp["aggregate_id"],
                venue_id=resp["venue_id"],
                referee_id=resp["referee_id"],
                localteam_id=resp["localteam_id"],
                visitorteam_id=resp["visitorteam_id"],
                winnerteam_id=resp["winner_team_id"],
                weather_report=json.dumps(resp["weather_report"]),
                commentaries=resp["commentaries"],
                attendance=resp["attendance"],
                pitch=resp["pitch"],
                details=resp["details"],
                neutral_venue=resp["neutral_venue"],
                winning_odds_calculated=resp["winning_odds_calculated"],
                formations=json.dumps(resp["formations"]),
                scores=json.dumps(resp["scores"]),
                time=json.dumps(resp["time"]),
                coaches=json.dumps(resp["coaches"]),
                standings=json.dumps(resp["standings"]),
                assistants=json.dumps(resp["assistants"]),
                leg=resp["leg"],
                colors=json.dumps(resp["colors"]),
                deleted=resp["deleted"],
                is_placeholder=resp["is_placeholder"],
                time_date=resp["time"]["starting_at"]["date"]
            )
    return res

def fixture_by_dateSeries(request, start_date=None, end_date=None):
    league_ids=[564,384,82,304,1114,8,38,32,42,1560,1351,1969,1560,1351,1092,1949,1968,1929,1971,1805,1950,1972,1969]
    endpoint = "https://soccer.sportmonks.com/api/v2.0/fixtures/between/{s_date}/{e_date}".format(
    s_date=start_date, e_date=end_date
    )
    url = endpoint + "?api_token=" + football_token
    print(url)
    response = requests.get(url)
    res = json.dumps(json.loads(response.text), indent=3)
    json_res = json.loads(res)
    pagination =  json_res["meta"]["pagination"]
    currentpage = int(pagination["current_page"])
    total_page = (pagination["total_pages"])

    for currentpage in range(total_page):
        endpoint = "https://soccer.sportmonks.com/api/v2.0/fixtures/between/{s_date}/{e_date}".format(
        s_date=start_date, e_date=end_date
        )
        url = endpoint + "?api_token=" + football_token+"&page="+str(currentpage)
        response = requests.get(url)
        res = json.dumps(json.loads(response.text), indent=3)
        json_res = json.loads(res)
        for resp in json_res["data"]:
            if resp["league_id"] in league_ids:
                cnt = MatchFixtureUpdate.objects.filter(matchid=resp["id"]).count()
                # print(resp["id"])
                # print(resp["league_id"])
                # print("rabi")
                if cnt == 0:
                    MatchFixtureUpdate.objects.create(
                        matchid=resp["id"],
                        league_id=resp["league_id"],
                        season_id=resp["season_id"],
                        stage_id=resp["stage_id"],
                        round_id=resp["round_id"],
                        group_id=resp["group_id"],
                        aggregate_id=resp["aggregate_id"],
                        venue_id=resp["venue_id"],
                        referee_id=resp["referee_id"],
                        localteam_id=resp["localteam_id"],
                        visitorteam_id=resp["visitorteam_id"],
                        winnerteam_id=resp["winner_team_id"],
                        weather_report=json.dumps(resp["weather_report"]),
                        commentaries=resp["commentaries"],
                        attendance=resp["attendance"],
                        pitch=resp["pitch"],
                        details=resp["details"],
                        neutral_venue=resp["neutral_venue"],
                        winning_odds_calculated=resp["winning_odds_calculated"],
                        formations=json.dumps(resp["formations"]),
                        scores=json.dumps(resp["scores"]),
                        time=json.dumps(resp["time"]),
                        coaches=json.dumps(resp["coaches"]),
                        standings=json.dumps(resp["standings"]),
                        assistants=json.dumps(resp["assistants"]),
                        leg=resp["leg"],
                        colors=json.dumps(resp["colors"]),
                        deleted=resp["deleted"],
                        is_placeholder=resp["is_placeholder"],
                        time_date=resp["time"]["starting_at"]["date"]
                    )
                get_teams(request='', id=resp["localteam_id"])
                get_teams(request='', id=resp["visitorteam_id"])
                get_seasonlist(request='', season_id=resp["season_id"])
                get_team_stats(request='', team_id=resp["localteam_id"])
                get_team_stats(request='', team_id=resp["visitorteam_id"])

    return res

def fixture_by_idlist(request, id_list=None):
    endpoint = "https://soccer.sportmonks.com/api/v2.0/fixtures/multi/{id_list}".format(id_list=id_list)
    url = endpoint + "?api_token=" + football_token
    response = requests.get(url)
    res = json.dumps(json.loads(response.text), indent=3)
    return res

def get_fixture(request, fixture_id_lineup=None, fixture_id_event=None):
    if fixture_id_lineup:
        endpoint = (
            "https://soccer.sportmonks.com/api/v2.0/fixtures/{fixture_id}?include=lineup.player,bench.player".format(
                fixture_id=fixture_id_lineup
            )
        )
    elif fixture_id_event:
        endpoint = "https://soccer.sportmonks.com/api/v2.0/fixtures/{fixture_id}?include=events.player".format(
            fixture_id=fixture_id_event
        )
    else:
        return {}
    url = endpoint + "&" + "api_token=" + football_token
    response = requests.get(url)
    res = json.dumps(json.loads(response.text), indent=3)

    return res

def get_fixturesupdate(request):
    request_data = JSONParser().parse(request)
    response = {}

    # query OBJ
    queryObj = {
        'id__gte': 0
    }
    if request_data['country_id']:
        queryObj['country_id'] = request_data['country_id']

    if request_data['league_id']:
        queryObj['league_id'] = request_data['league_id']
    if request_data['matchid']:
        queryObj['matchid'] = request_data['matchid']

    if request_data['id']:
        queryObj['id'] = request_data['id']

    endpoint = "https://soccer.sportmonks.com/api/v2.0/fixtures/updates"
    url = endpoint + "?api_token=" + football_token
    # print(queryObj)
    # response = requests.get(url)
    # res = json.dumps(json.loads(response.text), indent=3)
    # result = json.loads(res)
    final_res = []
    fixtures = MatchFixtureUpdate.objects.all().filter(**queryObj)
    result = MatchFixtureUpdateSerializer(fixtures, many=True).data
    for index, item in enumerate(result):
        # print(item)
        # print(item["winnerteam_id"])
        # print(item["visitorteam_id"])

        if (index <= 10):
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
            final_res.append(item)
    return final_res

def get_fixturebyid(request):
    
    requestdata = JSONParser().parse(request)
    query = Q()
    if requestdata['country_id']!='':
        query = query | Q(name__startswith=letter)


    query = query | Q(name__startswith=letter)
    final_res = []
    fixtures = MatchFixtureUpdate.objects.all().filter(id=requestdata['id'])
    result = MatchFixtureUpdateSerializer(fixtures, many=True).data

    for index, item in enumerate(result):
        # print(item)
        # print(item["winnerteam_id"])
        # print(item["visitorteam_id"])

        if (index <= 10):
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
            final_res.append(item)
    return final_res

def GetPlayerByteamId(team_id=0):
    leagues=[]
    league = Players.objects.all().filter(team_id=team_id)
    leagues = AllPlayerSerializer(league, many=True).data
    return leagues

def GetTimeSessionByteamId(team_id=0):
    # print(team_id)
    teams = []
    sessions = []
    maincat = {}
    team = Teams.objects.all().filter(team_id=team_id).order_by('-id')[:1]
    try:
        if team:
            teams = TeamDetailSerializer(team, many=True).data
            session = Season.objects.all().filter(team_id=team_id)
            sessions = SeasonSerializer(session, many=True).data
            maincat['teams'] = teams
            maincat['session'] = sessions
        else:
            get_teams(request='', id=team_id)
            get_team_stats(request='', team_id=team_id)
    except:
        maincat = []
    return maincat

def GetTeamByteamId(team_id=0):
    teams = []
    sessions = []
    maincat = {}
    team = Teams.objects.all().filter(~Q(collection_datasource="www.worldfootball.net"),team_id=team_id).order_by('-id')[:1]
    if team:
        teams = TeamDetailSerializer(team, many=True).data
    return teams

def GetTeamStatisticsDetailByteamId(team_id=0):
    team =[]
    team = TeamStatsDetails.objects.all().filter(team_id=team_id)[:5]
    if team:
        teams = TeamStatsDetailsSerializer(team, many=True).data
        return teams
    else:
        return team

def GetLeagueByLeagueId(league_id=0):
    leagues = []
    league = Leagues.objects.all().filter(league_id=league_id)[:1]
    if league:
        leagues = AllLeagueSerializer(league, many=True).data
    return leagues

def GetSeasonNameAndTeamStatDetails(team_id=0):
    from db_table.models import AllSeason
    from db_table.models import TeamStatsDetails
    teamdata = []
    print(team_id)
    teamS = TeamStatsDetails.objects.all().filter(team_id=team_id)
    
    teamdata = TeamSeasonStatsDetailsSerializer(teamS, many=True).data
    # for rec in teamdata:
    #     print(rec['season'])
    #     print(rec['goals_for'])
    return teamdata

def get_player_stats(request, player_id=None,parent_player_id = None):
    endpoint = "https://soccer.sportmonks.com/api/v2.0/players/{player_id}?".format(
        player_id=player_id
    )
    url = endpoint + "&api_token=" + football_token + "&" + "include=stats"
    response = requests.get(url)
    res = json.dumps(json.loads(response.text), indent=3)
    # redis_instance.set("allPlayerstatistics", res)
    json_res = json.loads(res)
    # for resp in json_res["data"]:
    resp=json_res["data"]
    for nresp in resp["stats"]["data"]:
        cnt = PlayerStatistics.objects.filter(player_id=nresp["player_id"],team_id=nresp["team_id"],league_id=nresp["league_id"],season_id=nresp["season_id"]).count()
        if cnt == 0:
            PlayerStatistics.objects.create(
                parent_player_id=parent_player_id,
                player_id=nresp["player_id"],
                team_id=nresp["team_id"],
                league_id=nresp["league_id"],
                season_id=nresp["season_id"],
                captain=nresp["captain"],
                minutes=nresp["minutes"],
                appearences=nresp["appearences"],
                lineups=nresp["lineups"],
                substitute_in=nresp["substitute_in"],
                substitute_out=nresp["substitute_out"],
                substitutes_on_bench=nresp["substitutes_on_bench"],
                goals=nresp["goals"],
                owngoals=nresp["owngoals"],
                assists=nresp["assists"],
                saves=nresp["saves"],
                inside_box_saves=nresp["inside_box_saves"],
                dispossesed=nresp["dispossesed"],
                interceptions=nresp["interceptions"],
                yellowcards=nresp["yellowcards"],
                yellowred=nresp["yellowred"],
                redcards=nresp["redcards"],
                type=nresp["type"],
                tackles=nresp["tackles"],
                blocks=nresp["blocks"],
                hit_post=nresp["hit_post"],
                cleansheets=nresp["cleansheets"],
                rating=nresp["rating"],
                fouls=json.dumps(nresp["fouls"]),
                crosses=json.dumps(nresp["crosses"]),
                dribbles=json.dumps(nresp["dribbles"]),
                duels=json.dumps(nresp["duels"]),
                passes=json.dumps(nresp["passes"]),
                penalties=json.dumps(nresp["penalties"]),
            )
        # else:
        #     data = PlayerStatistics.objects.get(player_id=nresp["player_id"],team_id=nresp["team_id"],league_id=nresp["league_id"],season_id=nresp["season_id"])
        #     data.parent_player_id=parent_player_id,
        #     data.player_id=nresp["player_id"]
        #     data.team_id=nresp["team_id"]
        #     data.league_id=nresp["league_id"]
        #     data.season_id=nresp["season_id"]
        #     data.captain=nresp["captain"]
        #     data.minutes=nresp["minutes"]
        #     data.appearences=nresp["appearences"]
        #     data.lineups=nresp["lineups"]
        #     data.substitute_in=nresp["substitute_in"]
        #     data.substitute_out=nresp["substitute_out"]
        #     data.substitutes_on_bench=nresp["substitutes_on_bench"]
        #     data.goals=nresp["goals"]
        #     data.owngoals=nresp["owngoals"]
        #     data.assists=nresp["assists"]
        #     data.saves=nresp["saves"]
        #     data.inside_box_saves=nresp["inside_box_saves"]
        #     data.dispossesed=nresp["dispossesed"]
        #     data.interceptions=nresp["interceptions"]
        #     data.yellowcards=nresp["yellowcards"]
        #     data.yellowred=nresp["yellowred"]
        #     data.redcards=nresp["redcards"]
        #     data.type=nresp["type"]
        #     data.tackles=nresp["tackles"]
        #     data.blocks=nresp["blocks"]
        #     data.hit_post=nresp["hit_post"]
        #     data.cleansheets=nresp["cleansheets"]
        #     data.rating=nresp["rating"]
        #     data.fouls=nresp["fouls"]
        #     data.crosses=nresp["crosses"]
        #     data.dribbles=nresp["dribbles"]
        #     data.duels=nresp["duels"]
        #     data.passes=nresp["passes"]
        #     data.penalties=nresp["penalties"]
        #     data.save()
    return resp

def get_season_stats(request, season_id=None):
    endpoint = "https://soccer.sportmonks.com/api/v2.0/seasons/{season_id}?include=stats".format(season_id=season_id)
    url = endpoint + "&api_token=" + football_token
    response = requests.get(url)
    res = json.dumps(json.loads(response.text), indent=3)

    return res


    # print(res)
    # print("------------------------------")
    # redis_instance.set(" seasonstatistics", res)
    json_res = json.loads(res)
    # for resp in json_res["data"]:
    resp = json_res["data"]
    try:
        SeasonStatistics.objects.get(name=resp["name"])
    except SeasonStatistics.DoesNotExist:
        # for nresp in resp["stats"]["data"]:
            SeasonStatistics.objects.create(
                season_id=resp["id"],
                name=resp["name"],
                league_id=resp["league_id"],
                is_current_season=resp["is_current_season"],
                current_round_id=resp["current_round_id"],
                current_stage_id=resp["current_stage_id"],
                stats_id=resp["stats"]["data"]["id"],
                stats_season_id=resp["stats"]["data"]["season_id"],
                stats_league_id=resp["stats"]["data"]["league_id"],
                number_of_clubs=resp["stats"]["data"]["number_of_clubs"],
                number_of_matches=resp["stats"]["data"]["number_of_matches"],
                number_of_matches_played=resp["stats"]["data"]["number_of_matches_played"],
                number_of_goals=resp["stats"]["data"]["number_of_goals"],
                matches_both_teams_scored=resp["stats"]["data"]["matches_both_teams_scored"],
                number_of_yellowcards=resp["stats"]["data"]["number_of_yellowcards"],
                number_of_yellowredcards=resp["stats"]["data"]["number_of_yellowredcards"],
                number_of_redcards=resp["stats"]["data"]["number_of_redcards"],
                avg_goals_per_match=resp["stats"]["data"]["avg_goals_per_match"],
                avg_yellowcards_per_match=resp["stats"]["data"]["avg_yellowcards_per_match"],
                avg_yellowredcards_per_match=resp["stats"]["data"]["avg_yellowredcards_per_match"],
                avg_redcards_per_match=resp["stats"]["data"]["avg_redcards_per_match"],
                team_with_most_goals_id=resp["stats"]["data"]["team_with_most_goals_id"],
                team_with_most_goals_number=resp["stats"]["data"]["team_with_most_goals_number"],
                team_with_most_conceded_goals_id=resp["stats"]["data"]["team_with_most_conceded_goals_id"],
                team_with_most_conceded_goals_number=resp["stats"]["data"]["team_with_most_conceded_goals_number"],
                team_with_most_goals_per_match_id=resp["stats"]["data"]["team_with_most_goals_per_match_id"],
                team_with_most_goals_per_match_number=resp["stats"]["data"]["team_with_most_goals_per_match_number"],
                season_topscorer_id=resp["stats"]["data"]["season_topscorer_id"],
                season_topscorer_number=resp["stats"]["data"]["season_topscorer_number"],
                season_assist_topscorer_id=resp["stats"]["data"]["season_assist_topscorer_id"],
                season_assist_topscorer_number=resp["stats"]["data"]["season_assist_topscorer_number"],
                team_most_cleansheets_id=resp["stats"]["data"]["team_most_cleansheets_id"],
                team_most_cleansheets_number=resp["stats"]["data"]["team_most_cleansheets_number"],
                goals_scored_minutes=json.dumps(resp["stats"]["data"]["goals_scored_minutes"]),
                goalkeeper_most_cleansheets_id=resp["stats"]["data"]["goalkeeper_most_cleansheets_id"],
                goalkeeper_most_cleansheets_number=resp["stats"]["data"]["goalkeeper_most_cleansheets_number"],
                goal_scored_every_minutes=resp["stats"]["data"]["goal_scored_every_minutes"],
                btts=resp["stats"]["data"]["btts"],
                goal_line=json.dumps(resp["stats"]["data"]["goal_line"]),
                avg_corners_per_match=resp["stats"]["data"]["avg_corners_per_match"],
                team_most_corners_count=resp["stats"]["data"]["team_most_corners_count"],
                team_most_corners_id=resp["stats"]["data"]["team_most_corners_id"],
                goals_conceded=json.dumps(resp["stats"]["data"]["goals_conceded"]),
                goals_scored=json.dumps(resp["stats"]["data"]["goals_scored"]),
                win_percentage=json.dumps(resp["stats"]["data"]["win_percentage"]),
                defeat_percentage=json.dumps(resp["stats"]["data"]["defeat_percentage"]),
                draw_percentage=resp["stats"]["data"]["draw_percentage"],
                avg_homegoals_per_match=resp["stats"]["data"]["avg_homegoals_per_match"],
                avg_awaygoals_per_match=resp["stats"]["data"]["avg_awaygoals_per_match"],
                avg_player_rating=resp["stats"]["data"]["avg_player_rating"],
                # updated_at=str_to_date(resp["stats"]["data"]["updated_at"]),
            )
    return res

def get_seasonlist(request, season_id=None):
    endpoint = "https://soccer.sportmonks.com/api/v2.0/seasons"
    if season_id:
        url = endpoint + "/"+ str(season_id) + "?api_token="+ football_token
        response = requests.get(url)
        res = json.dumps(json.loads(response.text), indent=3)

    else:
        url = endpoint + "?api_token=" + football_token+"&page=100"
        print(url)
        response = requests.get(url)
        res = json.dumps(json.loads(response.text), indent=3)
        # redis_instance.set("allseason", res)
        json_res = json.loads(res)
        pagination =  json_res["meta"]["pagination"]
        currentpage = int(pagination["current_page"])
        total_page = (pagination["total_pages"])

        for currentpage in range(total_page):
            url = endpoint + "?api_token=" + football_token+"&page="+str(currentpage)
            response = requests.get(url)
            res = json.dumps(json.loads(response.text), indent=3)
            # redis_instance.set("allseason", res)
            json_res = json.loads(res)
            for resp in json_res["data"]:
                cnt = AllSeason.objects.filter(name=resp["name"],league_id=resp["league_id"],collection_datasource='www.sportmonks.com').count()
                print(cnt)
                print(resp)
                if cnt == 0:
                    AllSeason.objects.create(
                        season_id=resp["id"],
                        name=resp["name"],
                        league_id=resp["league_id"],
                        is_current_season=resp["is_current_season"],
                        current_round_id=resp["current_round_id"],
                        current_stage_id=resp["current_stage_id"],
                        collection_datasource='www.sportmonks.com'
                    )
    return re

def countries_save(res):
    # redis_instance.set("country", res)
    json_res = json.loads(res)
    for resp in json_res["data"]:
        try:
            continent = resp["extra"]["continent"]
        except TypeError:
            continent = None
        try:
            sub_region = resp["extra"]["sub_region"]
        except TypeError:
            sub_region = None
        try:
            world_region = resp["extra"]["world_region"]
        except TypeError:
            world_region = None
        try:
            fifa = resp["extra"]["fifa"]
        except TypeError:
            fifa = None
        try:
            iso = resp["extra"]["iso"]
        except TypeError:
            iso = None
        try:
            iso2 = resp["extra"]["iso2"]
        except TypeError:
            iso2 = None
        try:
            longitude = resp["extra"]["longitude"]
        except TypeError:
            longitude = None
        try:
            latitude = resp["extra"]["latitude"]
        except TypeError:
            latitude = None
        try:
            flag = json.dumps(resp["extra"]["flag"])
        except TypeError:
            flag = None
        cnt =  Countries.objects.filter(country_id=resp["id"]).count()
        if cnt == 0:
            Countries.objects.create(
                country_id=resp["id"],
                name=resp["name"],
                image_path=resp["image_path"],
                continent=continent,
                sub_region=sub_region,
                world_region=world_region,
                fifa=fifa,
                iso=iso,
                iso2=iso2,
                longitude=longitude,
                latitude=latitude,
                flag=flag,
            )
        else:
            data = Countries.objects.get(country_id=resp["id"])
            data.country_id = resp["id"]
            data.name = resp["name"]
            data.image_path = resp["image_path"]
            data.continent = continent
            data.sub_region = sub_region
            data.world_region = world_region
            data.fifa = fifa
            data.iso = iso
            data.iso2 = iso2
            data.longitude = longitude
            data.latitude = latitude
            data.flag = flag
            data.save()
    return res

def leagues_save(res):
    # redis_instance.set("leagues", res)
    json_res = json.loads(res)
    resp = json_res["data"]
    cnt = Leagues.objects.filter(league_id=resp["id"]).count()
    if cnt == 0:
        Leagues.objects.create(
            league_id=resp["id"],
            active=resp["active"],
            type=resp["type"],
            legacy_id=resp["legacy_id"],
            country_id=resp["country_id"],
            logo_path=resp["logo_path"],
            name=resp["name"],
            is_cup=resp["is_cup"],
            season_id=resp["current_season_id"],
            round_id=resp["current_round_id"],
            stage_id=resp["current_stage_id"],
            live_standings=resp["live_standings"],
            predictions=resp["coverage"]["predictions"],
            topscorer_goals=resp["coverage"]["topscorer_goals"],
            topscorer_assists=resp["coverage"]["topscorer_assists"],
            topscorer_cards=resp["coverage"]["topscorer_cards"],
        )
    else:
        data = Leagues.objects.filter(league_id=resp["id"]).first()
        data.league_id = resp["id"]
        data.active = resp["active"]
        data.type = resp["type"]
        data.legacy_id = resp["legacy_id"]
        data.country_id = resp["country_id"]
        data.logo_path = resp["logo_path"]
        data.name = resp["name"]
        data.is_cup = resp["is_cup"]
        data.season_id = resp["current_season_id"]
        data.round_id = resp["current_round_id"]
        data.stage_id = resp["current_stage_id"]
        data.live_standings = resp["live_standings"]
        data.predictions = resp["coverage"]["predictions"]
        data.topscorer_goals = resp["coverage"]["topscorer_goals"]
        data.topscorer_assists = resp["coverage"]["topscorer_assists"]
        data.topscorer_cards = resp["coverage"]["topscorer_cards"]
        data.save()

    return res

def player_save(res):
    # redis_instance.set(" player", res)
    json_res = json.loads(res)
    # for resp in json_res["data"]:
    resp = json_res["data"]
    cnt = Players.objects.filter(player_id=resp["player_id"]).count()
    if cnt == 0:
        data=Players.objects.create(
            player_id=resp["player_id"],
            team_id=resp["team_id"],
            country_id=resp["country_id"],
            position_id=resp["position_id"],
            common_name=resp["common_name"],
            display_name=resp["display_name"],
            fullname=resp["fullname"],
            firstname=resp["firstname"],
            lastname=resp["lastname"],
            nationality=resp["nationality"],
            birthdate=str_to_date(resp["birthdate"]),
            birthcountry=resp["birthcountry"],
            birthplace=resp["birthplace"],
            height=resp["height"],
            weight=resp["weight"],
            image_path=resp["image_path"],
        )
        try:
            data.birthdate = str_to_date(resp["birthdate"])
            data.save()
        except TypeError:
            data.birthdate = None
            data.save()
    else:
        data = Players.objects.get(player_id=resp["player_id"])
        data.player_id = resp["player_id"]
        data.team_id = resp["team_id"]
        data.country_id = resp["country_id"]
        data.position_id = resp["position_id"]
        data.common_name = resp["common_name"]
        data.display_name = resp["display_name"]
        data.fullname = resp["fullname"]
        data.firstname = resp["firstname"]
        data.lastname = resp["lastname"]
        data.nationality = resp["nationality"]
        data.birthdate = str_to_date(resp["birthdate"])
        data.birthcountry = resp["birthcountry"]
        data.birthplace = resp["birthplace"]
        data.height = resp["height"]
        data.weight = resp["weight"]
        data.image_path = resp["image_path"]
        data.save()
    return res

def team_save(res):
    # redis_instance.set("teams", res)
    json_res = json.loads(res)
    resp = json_res["data"]
    cnt = Teams.objects.filter(team_id=resp["id"]).count()
    if cnt == 0:
        Teams.objects.create(
            team_id=resp["id"],
            legacy_id=resp["legacy_id"],
            name=resp["name"],
            short_code=resp["short_code"],
            twitter=resp["twitter"],
            country_id=resp["country_id"],
            national_team=resp["national_team"],
            founded=resp["founded"],
            logo_path=resp["logo_path"],
            venue_id=resp["venue_id"],
            season_id=resp["current_season_id"],
            is_placeholder=resp["is_placeholder"],
        )
    else:
        data = Teams.objects.get(team_id=resp["id"])
        data.team_id = resp["id"]
        data.legacy_id = resp["legacy_id"]
        data.name = resp["name"]
        data.short_code = resp["short_code"]
        data.twitter = resp["twitter"]
        data.country_id = resp["country_id"]
        data.national_team = resp["national_team"]
        data.founded = resp["founded"]
        data.logo_path = resp["logo_path"]
        data.venue_id = resp["venue_id"]
        data.season_id = resp["current_season_id"]
        data.is_placeholder = resp["is_placeholder"]
        data.save()
    return res

def odds_save(res):
    # redis_instance.set("odds", res)
    json_res = json.loads(res)
    for resp in json_res["data"]:
        cnt = Odds.objects.filter(odds_id=resp["id"]).count()
        if cnt == 0:
            Odds.objects.create(
                odds_id = resp["id"],
                name = resp["name"],
                suspended = resp["suspended"]
            )
            data = Odds.objects.get(odds_id=resp["id"])
            parent_id = data.id
            for nresp in resp["bookmaker"]["data"]:
                Bookmaker.objects.create(
                parent_oddsid=parent_id ,
                bookmaker_id = nresp["id"],
                bookmaker_name = nresp["name"]
            )
                for nnresp in nresp["odds"]["data"]:
                    Oddsdata.objects.create(
                    parent_oddsid=parent_id ,
                    label=nnresp["label"],
                    value=nnresp["value"],
                    probability=nnresp["probability"],
                    dp3=nnresp["dp3"],
                    american=nnresp["american"],
                    factional=nnresp["factional"],
                    winning=nnresp["winning"],
                    handicap=nnresp["handicap"],
                    total=nnresp["total"],
                    bookmaker_event_id=nnresp["bookmaker_event_id"],
                    date=nnresp["last_update"]["date"],
                    timezone_type=nnresp["last_update"]["timezone_type"],
                    timezone=nnresp["last_update"]["timezone"],
                    )

    return res

def season_save(res):
    # redis_instance.set("season", res)
    json_res = json.loads(res)
    # print(json_res)
    for resp in json_res["data"]:
        for chrrsp in resp["standings"]["data"]:
            if 'standings' in chrrsp:
                 for nnresp in chrrsp["standings"]["data"]:
                    # print(nnresp)
                    cnt = Season.objects.filter(standing_session_id=resp["id"]).count()
                    if cnt == 0:
                        Season.objects.create(
                            standing_session_id=resp["id"],
                            name=resp["name"],
                            league_id=resp["league_id"],
                            season_id=resp["season_id"],
                            round_id=resp["round_id"],
                            round_name=resp["round_name"],
                            type=resp["type"],
                            stage_id=resp["stage_id"],
                            stage_name=resp["stage_name"],
                            resource=resp["resource"],
                            position=nnresp["position"],
                            team_id=nnresp["team_id"],
                            team_name=nnresp["team_name"],
                            group_id=nnresp["group_id"],
                            group_name=nnresp["group_name"],
                            overall=json.dumps(nnresp["overall"]),
                            home=json.dumps(nnresp["home"]),
                            away=json.dumps(nnresp["away"]),

                            overall_games_played = nnresp["overall"]['games_played'],
                            overall_won = nnresp["overall"]['won'],
                            overall_draw = nnresp["overall"]['draw'],
                            overall_lost = nnresp["overall"]['lost'],
                            overall_goals_scored = nnresp["overall"]['goals_scored'],
                            overall_goals_against = nnresp["overall"]['goals_against'],
                            overall_points = nnresp["overall"]['points'],

                            home_games_played = nnresp["home"]['games_played'],
                            home_won = nnresp["home"]['won'],
                            home_draw = nnresp["home"]['draw'],
                            home_lost = nnresp["home"]['lost'],
                            home_goals_scored = nnresp["home"]['goals_scored'],
                            home_goals_against = nnresp["home"]['goals_against'],
                            home_points = nnresp["home"]['points'],

                            away_games_played = nnresp["away"]['games_played'],
                            away_won = nnresp["away"]['won'],
                            away_draw = nnresp["away"]['draw'],
                            away_lost = nnresp["away"]['lost'],
                            away_goals_scored = nnresp["away"]['games_played'],
                            away_goals_against = nnresp["away"]['games_played'],
                            away_points = nnresp["away"]['games_played'],

                            total=json.dumps(nnresp["total"]),

                            total_goals_difference = nnresp["total"]["goal_difference"],
                            total_points = nnresp["total"]["total_points"],

                            result=nnresp["result"],
                            points=nnresp["points"],
                            recent_form=nnresp["recent_form"],
                            status=nnresp["status"],
                        )
            else:
                cnt = Season.objects.filter(standing_session_id=resp["id"]).count()
                if cnt == 0:

                    Season.objects.create(
                        standing_session_id=resp["id"] if 'id' in resp  else '',
                        name=resp["name"] if 'name' in resp  else '',
                        league_id=resp["league_id"] if 'league_id' in resp  else '',
                        season_id=resp["season_id"] if 'season_id' in resp  else '',
                        round_id=resp["round_id"] if 'round_id' in resp  else '',
                        round_name=resp["round_name"] if 'round_name' in resp  else '',
                        type=resp["type"] if 'type' in resp  else '',
                        stage_id=resp["stage_id"] if 'stage_id' in resp  else '',
                        stage_name=resp["stage_name"] if 'stage_name' in resp  else '',
                        resource=resp["resource"] if 'resource' in resp  else '',
                        position=chrrsp["position"] if 'position' in chrrsp  else '',
                        team_id=chrrsp["team_id"],
                        team_name=chrrsp["team_name"],
                        group_id=chrrsp["group_id"],
                        group_name=chrrsp["group_name"],
                        overall=json.dumps(chrrsp["overall"]),
                        home=json.dumps(chrrsp["home"]),
                        away=json.dumps(chrrsp["away"]),
                        total=json.dumps(chrrsp["total"]),
                        result=chrrsp["result"],
                        points=chrrsp["points"],
                        recent_form=chrrsp["recent_form"],
                        status=chrrsp["status"],
                    )

    return res

def fixtureupdate_save(res):
    # redis_instance.set("fixtureupdate", res)
    json_res = json.loads(res)
    for resp in json_res["data"]:
        get_leagues(request='', id=resp["league_id"])
        get_teams(request='', id=resp["localteam_id"])
        get_teams(request='', id=resp["visitorteam_id"])
        get_team_stats(request='', team_id=resp["localteam_id"])
        get_team_stats(request='', team_id=resp["visitorteam_id"])
        get_standingseasonlist(request='', season_id=resp["season_id"])
        cnt =  MatchFixtureUpdate.objects.filter(matchid=resp["id"]).count()
        if cnt == 0:
            MatchFixtureUpdate.objects.create(
                matchid=resp["id"],
                league_id=resp["league_id"],
                season_id=resp["season_id"],
                stage_id=resp["stage_id"],
                round_id=resp["round_id"],
                group_id=resp["group_id"],
                aggregate_id=resp["aggregate_id"],
                venue_id=resp["venue_id"],
                referee_id=resp["referee_id"],
                localteam_id=resp["localteam_id"],
                visitorteam_id=resp["visitorteam_id"],
                winnerteam_id=resp["winner_team_id"],
                weather_report=json.dumps(resp["weather_report"]),
                commentaries=resp["commentaries"],
                attendance=resp["attendance"],
                pitch=resp["pitch"],
                details=resp["details"],
                neutral_venue=resp["neutral_venue"],
                winning_odds_calculated=resp["winning_odds_calculated"],
                formations=json.dumps(resp["formations"]),
                scores=json.dumps(resp["scores"]),
                time=json.dumps(resp["time"]),
                coaches=json.dumps(resp["coaches"]),
                standings=json.dumps(resp["standings"]),
                assistants=json.dumps(resp["assistants"]),
                leg=resp["leg"],
                colors=json.dumps(resp["colors"]),
                deleted=resp["deleted"],
                is_placeholder=resp["is_placeholder"],
                time_date=resp["time"]["starting_at"]["date"]
            )
        else:
            data = MatchFixtureUpdate.objects.filter(matchid=resp["id"]).first()
            data.matchid = resp["id"]
            data.league_id = resp["league_id"]
            data.season_id = resp["season_id"]
            data.stage_id = resp["stage_id"]
            data.round_id = resp["round_id"]
            data.group_id = resp["group_id"]
            data.aggregate_id = resp["aggregate_id"]
            data.venue_id = resp["venue_id"]
            data.referee_id = resp["referee_id"]
            data.localteam_id = resp["localteam_id"]
            data.visitorteam_id = resp["visitorteam_id"]
            data.winnerteam_id = resp["winner_team_id"]
            data.weather_report = json.dumps(resp["weather_report"])
            data.commentaries = resp["commentaries"]
            data.attendance = resp["attendance"]
            data.pitch = resp["pitch"]
            data.details = resp["details"]
            data.neutral_venue = resp["neutral_venue"]
            data.winning_odds_calculated = resp["winning_odds_calculated"]
            data.formations = json.dumps(resp["formations"])
            data.scores = json.dumps(resp["scores"])
            data.time = json.dumps(resp["time"])
            data.coaches = json.dumps(resp["coaches"])
            data.standings = json.dumps(resp["standings"])
            data.assistants = json.dumps(resp["assistants"])
            data.leg = resp["leg"]
            data.colors = json.dumps(resp["colors"])
            data.deleted = resp["deleted"]
            data.is_placeholder = resp["is_placeholder"]
            data.time_date = resp["time"]["starting_at"]["date"]
            data.save()
    return res

def get_team_stats(request, team_id=None):
    if team_id!='':
        endpoint = "https://soccer.sportmonks.com/api/v2.0/teams/{team_id}?include=stats".format(team_id=team_id)
        url = endpoint + "&api_token=" + football_token + "&" + "include=stats"
        print(url)
        response = requests.get(url)
        res = json.dumps(json.loads(response.text), indent=3)
        # redis_instance.set("allteamstatistics", res)
        json_res = json.loads(res)
        if 'data' in json_res:
            resp=json_res["data"]
            # print(resp);
            cnt = TeamStatistics.objects.filter(team_id=resp["id"]).count()
            teamStatisticsId = 0
            # print(cnt) 
            if cnt == 0:
                ts = TeamStatistics.objects.create(
                    team_id=resp["id"],
                    legacy_id = resp["legacy_id"],
                    name = resp["name"],
                    short_code = resp["short_code"],
                    twitter = resp["twitter"],
                    country_id = resp["country_id"],
                    national_team = resp["national_team"],
                    founded = resp["founded"],
                    logo_path = resp["logo_path"],
                    venue_id = resp["venue_id"],
                    current_season_id = resp["current_season_id"],
                    is_placeholder = resp["is_placeholder"],
                )
                teamStatisticsId = ts.id
                # print(ts.id)
            elif cnt <=1:
               # print(resp["id"])
                data = TeamStatistics.objects.get(team_id=resp["id"])
                data.team_id = resp["id"]
                data.legacy_id = resp["legacy_id"]
                data.name = resp["name"]
                data.short_code = resp["short_code"]
                data.twitter = resp["twitter"]
                data.country_id = resp["country_id"]
                data.national_team = resp["national_team"]
                data.founded = resp["founded"]
                data.logo_path = resp["logo_path"]
                data.venue_id = resp["venue_id"]
                data.current_season_id = resp["current_season_id"]
                data.is_placeholder = resp["is_placeholder"]
                data.save()
                # print(data.id)
                teamStatisticsId = data.id

            for nresp in resp["stats"]["data"]:
                cnt = TeamStatsDetails.objects.filter(team_id=resp["id"],season_id = nresp["season_id"],stage_id = nresp["stage_id"]).count()
            
                if cnt == 0:
                    TeamStatsDetails.objects.create(
                        teamstatistics_id = teamStatisticsId,
                        team_id = nresp["team_id"],
                        season_id = nresp["season_id"],
                        stage_id = nresp["stage_id"],
                        win = json.dumps(nresp["win"]),
                        draw = json.dumps(nresp["draw"]),
                        lost = json.dumps(nresp["lost"]),
                        goals_for = json.dumps(nresp["goals_for"]),
                        goals_against = json.dumps(nresp["goals_against"]),
                        clean_sheet = json.dumps(nresp["clean_sheet"]),
                        failed_to_score = json.dumps(nresp["failed_to_score"]),
                        scoring_minutes = json.dumps(nresp["scoring_minutes"]),
                        goals_conceded_minutes = json.dumps(nresp["goals_conceded_minutes"]),
                        avg_goals_per_game_scored = json.dumps(nresp["avg_goals_per_game_scored"]),
                        avg_goals_per_game_conceded = json.dumps(nresp["avg_goals_per_game_conceded"]),
                        avg_first_goal_scored =  json.dumps(nresp["avg_first_goal_scored"]),
                        avg_first_goal_conceded = json.dumps(nresp["avg_first_goal_conceded"]),
                        attacks = nresp["attacks"],
                        dangerous_attacks = nresp["dangerous_attacks"],
                        avg_ball_possession_percentage = nresp["avg_ball_possession_percentage"],
                        fouls = nresp["fouls"],
                        avg_fouls_per_game = nresp["avg_fouls_per_game"],
                        offsides = nresp["offsides"],
                        redcards = nresp["redcards"],
                        yellowcards = nresp["yellowcards"],
                        shots_blocked = nresp["shots_blocked"],
                        shots_off_target = nresp["shots_off_target"],
                        avg_shots_off_target_per_game = nresp["avg_shots_off_target_per_game"],
                        shots_on_target = nresp["shots_on_target"],
                        avg_shots_on_target_per_game = nresp["avg_shots_on_target_per_game"],
                        avg_corners = nresp["avg_corners"],
                        total_corners = nresp["total_corners"],
                        btts  = nresp["btts"],
                        goal_line_over =json.dumps(nresp["goal_line"]['over']) if nresp["goal_line"]!= None else '',
                        goal_line_under = json.dumps(nresp["goal_line"]['under']) if nresp["goal_line"]!= None else '',
                        avg_player_rating = nresp["avg_player_rating"],
                        avg_player_rating_per_match = nresp["avg_player_rating_per_match"],
                        tackles = nresp["tackles"],
                    )
    return 1  

def getTwoTeam(team1,team2):
    # endpoint = "https://soccer.sportmonks.com/api/v2.0/fixtures/multi/"
    # url = endpoint+str(team1)+','+str(team2) + "?api_token=" + football_token
    # print()
    # response = requests.get(url)
    # res = json.dumps(json.loads(response.text), indent=3)
    # json_res = json.loads(res)
    # # for resp in json_res["data"]:
    # resp=json_res["data"]
    # return resp
    team=[team1,team2]
    fixtures = MatchFixtureUpdate.objects.all().filter(matchid__in=team)
    result = MatchFixtureUpdateSerializer(fixtures, many=True).data
    res =json.dumps(json.loads(result.text))
    return res

def head2head(localTeamId:int,visitorTeamId:int):
    # params = json.dumps(params)
    # url =BASEURL+"api/ai/GetTeamDetailFromMatch"
    # r = requests.post(url,data=params)
    files =[]
    lwin = 0
    lloss = 0
    draw = 0
    vwin = 0
    vloss = 0
    total_match =0
    localteamwin =0
    visitorteamwin =0
    tot_draw =0
    print(localTeamId)
    print(visitorTeamId)
    fixtures = TeamHeadtoHeadGoalserve.objects.filter (\

            Q(\
                team1_id=localTeamId, \
                team2_id=visitorTeamId \
            ) | \
            Q(
                team1_id=visitorTeamId, \
                team2_id=localTeamId \
            )\

    ).all()
    
    for h2h in fixtures:
        # print(h2h.overall['total']['total_games'])
        total_match = h2h.overall['total']['total_games']
        lwin = h2h.h2h_probabilities['team1_won']
        vwin = h2h.h2h_probabilities['team2_won']
        draw = h2h.h2h_probabilities['draws']
        localteamwin = h2h.overall['total']['team1_won']
        visitorteamwin =h2h.overall['total']['team2_won']
        tot_draw = h2h.overall['total']['draws']
    
    data = {
        "result": {
            "localteam_id": localTeamId,
            "visitorteam_id": visitorTeamId,
            "totalmatches": total_match,
            "localteamwin": localteamwin,
            "localteamloss": total_match - (localteamwin+tot_draw),
            "draw": tot_draw,
            "visitorteamwin": visitorteamwin,
            "visitorteamloss": total_match - (visitorteamwin+tot_draw)
            },
        "probability": {
            "localteamwin": lwin,
            "localteamloss": 100-lwin,
            "draw": draw,
            "visitorteamwin": vwin,
            "visitorteamloss": 100-vwin
            }
        }
    # data = json.dumps(data)
    return data

def head2headPrediction(localTeamId:int,visitorTeamId:int):
    # params = json.dumps(params)
    # url =BASEURL+"api/ai/GetTeamDetailFromMatch"
    # r = requests.post(url,data=params)
    files =[]
    teamFormPoints_team1 =0
    teamFormPoints_team2=0
    teamShotOnTarget_team1=0
    teamShotOnTarget_team2=0
    teamStandings_team1=0
    teamStandings_team2=0
    # print(localTeamId)
    # print(visitorTeamId)
    fixtures = TeamHeadtoHeadGoalserve.objects.filter (\

            Q(\
                team1_id=localTeamId, \
                team2_id=visitorTeamId \
            ) | \
            Q(
                team1_id=visitorTeamId, \
                team2_id=localTeamId \
            )\

    ).all()
    
    for h2h in fixtures:
        teamFormPoints_team1  = h2h.teamFormPoints['team1']
        teamFormPoints_team2= h2h.teamFormPoints['team2']
        teamShotOnTarget_team1= h2h.teamShotOnTarget['team1']
        teamShotOnTarget_team2= h2h.teamShotOnTarget['team2']
        teamStandings_team1= h2h.teamStandings['hteamLP']
        teamStandings_team2= h2h.teamStandings['ateamLP']
       
    
    data = {
        "result": {
            "teamFormPoints_team1": teamFormPoints_team1,
            "teamFormPoints_team2": teamFormPoints_team2,
            "teamShotOnTarget_team1": teamShotOnTarget_team1,
            "teamShotOnTarget_team2": teamShotOnTarget_team2,
            "teamStandings_team1":teamStandings_team1,
            "teamStandings_team2": teamStandings_team2,
            }
        }
    # data = json.dumps(data)
    return data


def TeamDetailFromMatch(localteam_id,visitorteam_id):
    data =[]
    # fixtures = TeamHeadtoHeadGoalserveGoalserveSerializer(
    #     TeamHeadtoHeadGoalserve.objects.filter (\

    #         Q(\
    #             team1_id=localteam_id, \
    #             team2_id=visitorteam_id \
    #         ) | \
    #         Q(
    #             team1_id=visitorteam_id, \
    #             team2_id=localteam_id \
    #         )\

    #     ).values('last5_matches'), many=True
    # ).data
    fixtures = TeamHeadtoHeadGoalserve.objects.filter (\

            Q(\
                team1_id=localteam_id, \
                team2_id=visitorteam_id \
            ) | \
            Q(
                team1_id=visitorteam_id, \
                team2_id=localteam_id \
            )\

        ).all()
    # fixtures = TeamHeadtoHeadGoalserve.objects.filter(team1_id=localteam_id,team2_id=visitorteam_id).all()
    # data1= TeamHeadtoHeadGoalserveGoalserveSerializer(fixtures,many=true).data
    for fixt in fixtures:
        print(fixt)
        print("---------")
        data = fixt.overall
        print(data)
        return (fixt)
    return (data) 
def Head2HeadSportsmonk(team1,team2):
    endpoint = "https://soccer.sportmonks.com/api/v2.0/head2head/"
    url = endpoint+str(team1)+'/'+str(team2) + "?api_token=" + football_token
    
    print(url)
    response = requests.get(url)
    res = json.dumps(json.loads(response.text), indent=3)
    json_res = json.loads(res)
    # for resp in json_res["data"]:
    resp=json_res["data"]
    return resp

def GetVenueById(venue_id):
    resp=[]
    endpoint = "https://soccer.sportmonks.com/api/v2.0/venues/"
    url = endpoint+str(venue_id) + "?api_token=" + football_token
    # print(url)
    response = requests.get(url)
    res = json.dumps(json.loads(response.text), indent=3)
    json_res = json.loads(res)
    # for resp in json_res["data"]:
    if 'data' in json_res:
        resp=json_res["data"]
    return resp

def GetPosionDetailFormTeamId(localteam,visiterteam):
    endpoint = AIURL+''
    res = '[]'
    print(localteam+'VS'+visiterteam)
    json_req={ "HomeTeam": [localteam],"AwayTeam": [visiterteam]}
    url = AIURL + "prediction/"
    response = requests.post(url, json=json_req)
    # print(response.text)
    if response.text!= 'Internal Server Error':
        res =json.dumps(json.loads(response.text))
   
    # print(res)
    # print("===============")
    return res

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

def GetTeamStatisticsBySportsMonk(team_id):
    endpoint = "https://soccer.sportmonks.com/api/v2.0/teams/"+str(team_id)
    url = endpoint + "?api_token=" + football_token + "&" + "include=stats"
    print(url)
    resp=[]
    response = requests.get(url)
    res = json.dumps(json.loads(response.text), indent=3)
    # redis_instance.set("allteamstatistics", res)
    json_res = json.loads(res)
    if 'data' in json_res:
        resp=json_res["data"]
    return resp
def GetTeamStandingBySeasonId(season_id,team_id):

    season = Season.objects.all().filter(team_id=team_id,season_id = season_id).values('position')
    if season:
        # result = SeasonSerializer(season, many=True).data
        return season[0]['position']
    else:
        endpoint = "https://soccer.sportmonks.com/api/v2.0/standings/season/"+str(season_id)
        url = endpoint + "?api_token=" + football_token
        # print(url)
        resp=[]
        response = requests.get(url)
        res = json.dumps(json.loads(response.text), indent=3)
        # redis_instance.set("allteamstatistics", res)
        json_res = json.loads(res)
        if 'data' in json_res:
            resp =  json_res["data"]
            # print(resp)
            # print("-------------------------------")
            # resp=json_res["data"]['standings']['data']
            for rec in resp:
                for ans in rec['standings']['data']:
                    if 'position' in ans:
                        # print("-----------------------")
                        # print(ans)
                        # print("--------------------********************----------")
                        Season.objects.create(
                            
                            name=rec["name"],
                            league_id=rec["league_id"],
                            season_id=rec["season_id"],
                            round_id=rec["round_id"],
                            round_name=rec["round_name"],
                            type= rec["type"] if 'type' in rec  else 0,
                            stage_id=rec["stage_id"],
                            stage_name=rec["stage_name"],
                            resource=rec["resource"],
                            position=ans["position"] if 'position' in ans  else 0,
                            team_id=ans["team_id"],
                            team_name=ans["team_name"],
                            group_id=ans["group_id"],
                            group_name=ans["group_name"],
                            overall=json.dumps(ans["overall"]),
                            home=json.dumps(ans["home"]),
                            away=json.dumps(ans["away"]),

                            total_goals_difference = ans["total"]["goal_difference"],
                            total_points = ans["total"]["points"],

                            overall_games_played = ans["overall"]['games_played'],
                            overall_won = ans["overall"]['won'],
                            overall_draw = ans["overall"]['draw'],
                            overall_lost = ans["overall"]['lost'],
                            overall_goals_scored = ans["overall"]['goals_scored'],
                            overall_goals_against = ans["overall"]['goals_against'],
                            overall_points = ans["overall"]['points'] if 'points' in ans["overall"]  else 0,

                            home_games_played = ans["home"]['games_played'],
                            home_won = ans["home"]['won'],
                            home_draw = ans["home"]['draw'],
                            home_lost = ans["home"]['lost'],
                            home_goals_scored = ans["home"]['goals_scored'],
                            home_goals_against = ans["home"]['goals_against'],
                            home_points = ans["home"]['points'] if 'points' in ans["home"]  else 0,

                            away_games_played = ans["away"]['games_played'],
                            away_won = ans["away"]['won'],
                            away_draw = ans["away"]['draw'],
                            away_lost = ans["away"]['lost'],
                            away_goals_scored = ans["away"]['games_played'],
                            away_goals_against = ans["away"]['games_played'],
                            away_points = ans["away"]['points'] if 'points' in ans["away"]  else 0,

                            total=json.dumps(ans["total"]),
                            result=ans["result"],
                            points=ans["points"],
                            recent_form=ans["recent_form"],
                            status=ans["status"]
                        )
                for ans1 in rec['standings']['data']:
                    
                    if 'team_id' in ans:
                        if team_id == ans['team_id']:
                            return ans['position']
                
    return 0

def preprocessdata(data):
    # print("**************************")
    # print(data)
    # print("-------------------")
    
    if "teamdetail" in data[0]:
        data = data[0]["teamdetail"]
    
    formpts = 0
    avg_shots_on_target = 0
    total_shots_on_target = 0
    standings = 0
    res ={}
    
    for i in data:
        # print("**************")
        # print('i["standing"][0]["position"]')
        # print(i)
        # print("///////////////////")
        win_total =0
        draw_total =0
        lost_total =0
        if 'shots_on_target' in i and i["shots_on_target"]!=None:
            total_shots_on_target = total_shots_on_target + int(i["shots_on_target"])
        formpts += int(i['tot_win']) * 3 + int(i['tot_draw']) * 1 + int(i['tot_lost']) * 0
        standings = int(i["position"])
       

    # print(formpts)       
    avg_shots_on_target = round(total_shots_on_target/5)
    # print(formpts,avg_shots_on_target)
    res['formpts'] =formpts
    res['avg_shots_on_target'] =avg_shots_on_target
    res['standings'] =standings
    return res

def GetPredictionByMatch(HTFormPts,ATFormPts,HomeTeamLP,AwayTeamLP,HST,AST,HTEloRatings,ATEloRatings):
    json_req={ 
        "HTFormPts": HTFormPts,
        "ATFormPts": ATFormPts,
        "HomeTeamLP" :HomeTeamLP,
        "AwayTeamLP" :AwayTeamLP,
        "HST" :HST,
        "AST" :AST,
        "HTEloRatings" :HTEloRatings,
        "ATEloRatings" :ATEloRatings
        }
    # print(json_req)
    url = AIMODELURL + "prediction/"
    response = requests.post(url, json=json_req)
    res =json.dumps(json.loads(response.text))
    # print(response)
    # print(res)
    return res
def GetTeamStatisticsAndStandingByTeamId(season_id,team_id):

    result =[]
    fixture = []
    endpoint = " https://soccer.sportmonks.com/api/v2.0/fixtures/between/2021-01-04/2021-12-31/"+str(team_id)
    url = endpoint + "?api_token=" + football_token 
    response = requests.get(url)
    res = json.dumps(json.loads(response.text), indent=3)
    json_res = json.loads(res)
    i =0
    tot_win =0
    tot_draw = 0
    tot_lost =0
    position =0
    shots_on_target =0
    if 'data' in json_res:
        for resp in json_res['data']:
            if i<5:
                print(str(resp['winner_team_id'])+'-'+str(team_id))
                if str(resp['winner_team_id']) == str(team_id):
                    tot_win +=1
                if resp['winner_team_id'] == None:
                    tot_draw +=1
                if resp['winner_team_id'] != None and str(resp['winner_team_id']) != str(team_id):
                    tot_lost += 1
            i = i+1
    
    # Get Position
    season = Season.objects.all().filter(team_id=team_id,season_id = season_id).values('position')
    if season:
        # result = SeasonSerializer(season, many=True).data
        position = int(season[0]['position'])
    else:
        endpoint = "https://soccer.sportmonks.com/api/v2.0/standings/season/"+str(season_id)
        url = endpoint + "?api_token=" + football_token
        # print(url)
        resp=[]
        response = requests.get(url)
        res = json.dumps(json.loads(response.text), indent=3)
        # redis_instance.set("allteamstatistics", res)
        json_res = json.loads(res)
        if 'data' in json_res:
            resp =  json_res["data"]
            # print(resp)
            # print("-------------------------------")
            # resp=json_res["data"]['standings']['data']
            for rec in resp:
                for ans1 in rec['standings']['data']:
                    if 'team_id' in ans1:
                        if team_id == ans1['team_id']:
                            position = int(ans1['position']) 
                
    team_detail = TeamStatsDetails.objects.all().filter(team_id=team_id).values('shots_on_target')
    if team_detail:
        # result = SeasonSerializer(season, many=True).data
        for td in team_detail:
            if td['shots_on_target']:
                shots_on_target = td['shots_on_target']
                break
    else:
        endpoint = " https://soccer.sportmonks.com/api/v2.0/teams/"+str(team_id)
        url = endpoint + "?api_token=" + football_token +'&include=stats'
        # print(url)
        resp=[]
        response = requests.get(url)
        res = json.dumps(json.loads(response.text), indent=3)
        # redis_instance.set("allteamstatistics", res)
        json_res = json.loads(res)
        if 'data' in json_res:
            resp =  json_res["data"]
            # print(resp)
            # print("-------------------------------")
            # resp=json_res["data"]['standings']['data']
            for rec in resp['stats']['data']:
                for ans1 in rec:
                    if 'shots_on_target' in ans1:
                        if ans['shots_on_target']>0:
                            shots_on_target = int(ans['shots_on_target'])
                            break

    result.append({'tot_win':tot_win,'tot_draw':tot_draw,'tot_lost':tot_lost,'shots_on_target':shots_on_target,'position':position})
    
    print(tot_win)
    print(tot_draw)
    print(tot_lost)
    print(shots_on_target)
    print(position)
    
    return result
def GetTeamStatisticsByTeamIdSeasonIdFromSportsmonk(team_id,season_id):
    endpoint = "https://soccer.sportmonks.com/api/v2.0/teams/"+str(team_id)
    url = endpoint + "?api_token=" + football_token + "&" + "include=stats&season="+str(season_id)
    # print(url)
    response = requests.get(url)
    res = json.dumps(json.loads(response.text), indent=3)
    json_res = json.loads(res)
    if 'data' in json_res:
        return json_res["data"]
    else:
        return json_res

def SaveLeaguetoLeagueOtherSource():
    lg=Leagues.objects.filter(collection_datasource='www.soccerstats.com').delete()
    # league = Leagues.objects.all().filter(collection_datasource='www.worldfootball.net')
    # lg=LeaguesOtherSource.objects.filter(collection_datasource='www.worldfootball.net').delete()
    # for resp in league:
       
    #     cnt = LeaguesOtherSource.objects.filter(league_id=resp.league_id).count()
    #     if cnt == 0:
            
    #         LeaguesOtherSource.objects.create(
    #             league_id=resp.id,
    #             active=resp.active,
    #             type=resp.type,
    #             legacy_id=resp.legacy_id,
    #             country_id=resp.country_id,
    #             logo_path=resp.logo_path,
    #             name=resp.name,
    #             is_cup=resp.is_cup,
    #             season_id=resp.season_id,
    #             round_id=resp.round_id,
    #             stage_id=resp.stage_id,
    #             live_standings=resp.live_standings,
    #             predictions=resp.predictions,
    #             topscorer_goals=resp.topscorer_goals,
    #             topscorer_assists=resp.topscorer_assists,
    #             topscorer_cards=resp.topscorer_cards,
    #             collection_datasource='www.worldfootball.net'
    #         )
    return 1





def eloratings(hometeam,awayteam,date):
    team_mapping = {
        "Manchester City": "Man City",
        "Manchester Utd": "Man United",
        "Atl. Madrid": "Atletico",
        "Real Sociedad": "Sociedad",
        "Ath Bilbao": "Bilbao",
        "Celta Vigo": "Celta",
        "Granada CF": "Granada",
        "Cadiz CF": "Cadiz",
        "AC Milan": "Milan",
        "AS Roma": "Roma",
        "Bayern Munich": "Bayern",
        "Bayer Leverkusen": "Leverkusen",
        "FC Koln": "Koeln",
        "Eintracht Frankfurt": "Frankfurt",
        "B. Monchengladbach": "Gladbach",
        "Arminia Bielefeld": "Bielefeld",
        "Hertha Berlin": "Hertha",
        "Greuther Furth": "Fuerth",
        "St Etienne": "Saint-Etienne",
        "Malmo FF": "Malmoe",
        "Varberg": "Varbergs",
        "Mjallby": "Mjaellby",
        "Norrkoping": "Norrkoeping",
        "Hacken": "Haecken",
        "Goteborg": "Goeteborg",
        "Sirius": "IK Sirius",
        "AZ Alkmaar": "Alkmaar",
        "G.A. Eagles": "Go Ahead Eagles",
        "FC Porto": "Porto",
        "Vitoria Guimaraes": "Guimaraes",
        "Bodo/Glimt": "Bodoe Glimt",
        "Sarpsborg 08": "Sarpsborg",
        "Odd": "Odd Grenland",
        "Basaksehir": "Bueyueksehir",
        "Karagumruk": "Fatih Karaguemruek",
        "Adana Demirspor": "Adana Demirspor",
        "Kayserispor": "Kayseri",
        "Gaziantep": "Gaziantep FK",
        "Goztepe": "Goeztepe",
        "Yeni Malatyaspor": "Malatyaspor",
        "Zurich": "Zuerich",
        "Young Boys": "Young Boys",
        "St. Gallen": "StGallen",
        "Wolfsberger AC": "Wolfsberg",
        "Austria Vienna": "Austria Wien",
        "Rapid Vienna": "Rapid Wien",
        "Austria Klagenfurt": "Klagenfurt",
        "WSG Tirol": "Wattens",
        "Tirol": "Wattens",
        "Rheindorf Altach": "Altach",
        "FC Copenhagen": "FC Kobenhavn",
        "AaB": "Aalborg",
        "AGF": "Aarhus",
        "OB": "Odense",
        "AEK Athens": "AEK",
        "AEK Athens FC": "AEK",
        "PAS Giannina": "Giannina",
        "Panaitolikos": "Panetolikos",
        "Volos NFC": "NFC Volos",
        "Volos": "NFC Volos",
        "Apollon Smirnis": "Apollon Athens",
        "Randers FC": "Randers",
        "Sonderjyske": "SonderjyskE",
        "Olympiacos Piraeus": "Olympiakos",
        "OFI Crete": "OFI",
        "A. Klagenfurt": "Klagenfurt",
        "CFR Cluj": "CFR Cluj",
        "Universitatea Craiova": "Craiova",
        "FC Arges": "Arges Pitesti",
        "Boto?ani": "Botosani",
        "Rapid": "Rapid Bucuresti",
        "U Craiova 1948": "Craiova 1948",
        "UTA Arad": "UTA Arad",
        "Chindia Targoviste": "Chindia Targoviste",
        "Dinamo Bucuresti": "Dinamo Bucuresti",
        "Academica Clinceni": "Clinceni",
        "Gaz Metan Medias": "Gaz Metan",
        "Gornik Zabrze": "Gornik",
        "Jagiellonia Bialystok": "Jagiellonia",
        "Lech Poznan": "Lech",
        "Lechia Gdansk": "Lechia",
        "Legia Warsaw": "Legia",
        "Piast Gliwice": "Piast Gliwice",
        "Pogon Szczecin": "Pogon",
        "Radomiak Radom": "Radomiak",
        "Rakow Czestochowa": "Rakow",
        "Slask Wroclaw": "Slask",
        "Stal Mielec": "Stal Mielec",
        "Warta Poznan": "Warta",
        "Widzew Lodz": "Wisla",
        "Wisla Plock": "Plock",
        "Zaglebie Lubin": "Lubin",
        "Shamrock Rovers": "Shamrock",
        "Sligo Rovers": "Sligo",
        "Bohemians": "Bohemians Dublin",
        "KuPS": "Kuopio",
        "HJK": "HJK Helsinki",
        "Honka": "Honka Espoo",
        "Ross County": "Ross County",
        "St. Johnstone": "St Johnstone",
        "St. Mirren": "St Mirren",
        "Club Brugge": "Brugge",
        "Union Saint-Gilloise": "St Gillis",
        "Sporting Charleroi": "Charleroi",
        "Sint-Truiden": "St Truiden",
        "Cercle Brugge": "Cercle Brugge",
        "OH Leuven": "Leuven",
        "KV Oostende": "Oostende",
        "Standard Liege": "Standard",
        "AS Eupen": "Eupen",
        "Beerschot": "Beerschot AC",
        "Dundee Utd": "Dundee United"

    }
    url = 'http://api.clubelo.com/'+str(date)
    df =pd.read_csv(url)
    hteam = ''
    ateam = ''
    if hometeam in team_mapping and awayteam in team_mapping:
            hteam = team_mapping[hometeam]
            ateam = team_mapping[awayteam]
    elif hometeam in team_mapping and awayteam not in team_mapping:
            hteam = team_mapping[hometeam]
            ateam = awayteam
    elif hometeam not in team_mapping and awayteam in team_mapping:
            hteam = hometeam
            ateam = team_mapping[awayteam]
    else:
            hteam = hometeam
            ateam = awayteam
    filter_df = df[df.Club == hteam]
    ht_elo = filter_df.Elo.values[0]
    filter_df = df[df.Club == ateam]
    at_elo = filter_df.Elo.values[0]
    return {'HomeTeamElo': ht_elo,'AwayTeamElo': at_elo}

def LeagueIdGolaServe():
    author = LeagueGoalserve.objects.filter(is_active=True)
    ids    = author.values_list('league_id', flat=True)
    return(list(ids))

def GatAllActiveLeagueByGoalServe():
    league = LeagueGoalserve.objects.filter(is_active=True)
    league_detail = LeagueGoalserveSerializer(league, many=True).data
    return (league_detail)

def GatLeagueByCountryGoalServe(country):
    league = LeagueGoalserve.objects.filter(is_active=True,country=country)
    league_detail = LeagueGoalserveSerializer(league, many=True).data
    return (league_detail)

