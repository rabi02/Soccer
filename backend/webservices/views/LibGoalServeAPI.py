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
from webservices.views.teamstatsLIB import *
from webservices.views.playerstats_libGS import *

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
import xlwt

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

def StoreLeague():
    import requests
    from datetime import datetime, timedelta
    url = "https://www.goalserve.com/getfeed/c05d9fc7d36540dcdfaa08d9e34f661d/soccerfixtures/data/mapping?json=1"
    response = requests.request("GET", url)
    # print(response.text)
    res =json.dumps(json.loads(response.text))
    # print(res)
    json_res = json.loads(res)
    if 'fixtures' in json_res:
        fixtureData = json_res['fixtures']
        if 'mapping' in fixtureData:
            mapdata = fixtureData['mapping']
            for resp in mapdata:
                print(resp["@id"])
                cnt =  LeagueGoalserve.objects.filter(league_id=resp["@id"]).count()
                if cnt == 0:
                    start_date=resp["@date_start"].replace(".",'-')
                    date_end=resp["@date_end"].replace(".",'-')
                    import datetime
                    new_start_date= datetime.datetime.strptime(start_date, "%d-%m-%Y").strftime("%Y-%m-%d")
                    new_end_date= datetime.datetime.strptime(date_end, "%d-%m-%Y").strftime("%Y-%m-%d")
                   
                    LeagueGoalserve.objects.create(
                        league_id=resp["@id"],
                        country=resp["@country"],
                        name=resp["@name"],
                        season=resp["@season"],
                        date_start= new_start_date,
                        date_end= new_end_date,
                        iscup=resp["@iscup"],
                        live_lineups=resp["@live_lineups"],
                        live_stats=resp["@live_stats"],
                        path=resp["@path"],
                    )
    return res

def StoreSeason():
    import requests
    from datetime import datetime, timedelta
    url = "https://www.goalserve.com/getfeed/c05d9fc7d36540dcdfaa08d9e34f661d/soccerfixtures/data/seasons?json=1"
    response = requests.request("GET", url)
    # print(response.text)
    res =json.dumps(json.loads(response.text))
    # print(res)
    json_res = json.loads(res)
    if 'seasons' in json_res:
        fixtureData = json_res['seasons']
        if 'league' in fixtureData:
            mapdata = fixtureData['league']
            for resp in mapdata:
                
                league_id = resp["@id"]
                country=resp["@country"]
                league_name=resp["@name"]
                iscup=resp["@iscup"]
                if int(league_id) > 2647:
                    if 'results' in resp:
                        result = resp['results']
                        try:
                            if 'season' in result:
                                if '@name' in result['season']:
                                    season = result['season']['@name']
                                    SeasonGoalserve.objects.create(
                                        league_id=league_id,
                                        country=country,
                                        league_name=league_name,
                                        season=season,
                                        iscup=iscup,
                                        is_standing='0',
                                        standing=season
                                    )
                                else:
                                    for ses in result['season']:
                                        season= ses['@name']
                                        SeasonGoalserve.objects.create(
                                            league_id=league_id,
                                            country=country,
                                            league_name=league_name,
                                            season=season,
                                            iscup=iscup,
                                            is_standing='',
                                            standing=''
                                        )
                        except:
                            print(league_id)
                    if 'standings' in resp:
                        result = resp['standings']
                        try:
                            if 'season' in result:
                                print(league_id)
                                if '@name' in result['season']:
                                    season = result['season']['@name']
                                    SeasonGoalserve.objects.create(
                                        league_id=league_id,
                                        country=country,
                                        league_name=league_name,
                                        season=season,
                                        iscup=iscup,
                                        is_standing='0',
                                        standing=season
                                    )
                                else:
                                    for ses in result['season']:
                                         
                                        season = ses['@name']
                                        SeasonGoalserve.objects.create(
                                            league_id=league_id,
                                            country=country,
                                            league_name=league_name,
                                            season=season,
                                            iscup=iscup,
                                            is_standing='0',
                                            standing=season
                                        )
                        except:
                            print(league_id)
    return res

def StoreMatch():
    import requests
    from db_table.models import MatchGoalserve
    from datetime import datetime, timedelta
    for i in range(7,1,-1):
        url = "https://www.goalserve.com/getfeed/c05d9fc7d36540dcdfaa08d9e34f661d/soccernew/d"+str(i)+"?json=1"
        print(url)
        response = requests.request("GET", url)
        # print(response.text)
        res =json.dumps(json.loads(response.text))
        # print(res)
        json_res = json.loads(res)
        if 'scores' in json_res:
            scoresData = json_res['scores']
            if 'category' in scoresData:
                categorydata = scoresData['category']
                for league in categorydata:
                    match_name = league['@name']
                    gid = league['@gid']
                    league_id = league['@id']
                    file_group = league['@file_group']
                    iscup = league['@iscup']
                    # print("league_id="+league_id)
                    # print("gid="+gid)

                    if 'matches' in league:
                        matches = league['matches']
                        str_date = matches['@date']
                        formated_date = matches['@formatted_date']

                        if 'match' in league['matches']:
                            matcharr = league['matches']['match']
                            # print(matcharr)
                            # # print("league_id="+league_id)
                            # print("++++++++++++++++++++++++++++")
                            if '@status' in matcharr:
                                if formated_date:
                                    import datetime
                                    frmt_date=formated_date.replace(".",'-')
                                    frmt_date= datetime.datetime.strptime(frmt_date, "%d-%m-%Y").strftime("%Y-%m-%d")
                                      
                                status =matcharr['@status']
                                new_str_date = matcharr['@date']
                                new_formated_date = matcharr['@formatted_date']
                                formated_time = matcharr['@time']
                                venue = matcharr['@venue']
                                static_id = matcharr['@static_id']
                                fix_id = matcharr['@fix_id']
                                match_id = matcharr['@id']
                                events = matcharr['events']
                                localteam_name = matcharr['localteam']['@name']
                                localteam_goals = matcharr['localteam']['@goals']
                                localteam_id = matcharr['localteam']['@id']
                                visitorteam_name = matcharr['visitorteam']['@name']
                                visitorteam_goals = matcharr['visitorteam']['@goals']
                                visitorteam_id = matcharr['visitorteam']['@id']
                                ht_score = matcharr['ht']['@score']
                                if new_formated_date:
                                    new_frmt_date=new_formated_date.replace(".",'-')
                                    new_frmt_date= datetime.datetime.strptime(new_frmt_date, "%d-%m-%Y").strftime("%Y-%m-%d")
                                # print("match_id="+match_id)
                                cnt =  MatchGoalserve.objects.filter(match_id=match_id).count()
                                if cnt ==0:
                                    # print(match_id)
                                    ins = MatchGoalserve.objects.create(
                                        group_id= gid if gid!= '' else 0,
                                        league_id=league_id if league_id!= '' else 0,
                                        match_name=match_name,
                                        gid = gid if gid!= '' else 0,
                                        file_group=file_group,
                                        iscup=iscup,
                                        string_date = str_date if str_date!= '' else new_str_date,
                                        formated_date=frmt_date if frmt_date!= '' else new_frmt_date,
                                        formated_time=formated_time,
                                        time_status=status,
                                        venue=venue,
                                        static_id = static_id if static_id != '' else 0,
                                        fix_id= fix_id if fix_id != '' else 0,
                                        match_id = match_id if match_id != '' else 0,
                                        localteam_name=localteam_name,
                                        localteam_goals=localteam_goals,
                                        localteam_id = localteam_id if localteam_id != '' else 0,
                                        visitorteam_name=visitorteam_name,
                                        visitorteam_goals=visitorteam_goals,
                                        visitorteam_id = visitorteam_id if visitorteam_id != '' else 0,
                                        events=events,
                                        ht_score=ht_score,
                                    )
                                    TeamStatistics(localteam_id,match_id)
                                    TeamStatistics(visitorteam_id,match_id)
                                    predictionSave(match_id)


                            else:
                                for rec in matcharr:
                                    if rec:
                                        if formated_date:
                                            import datetime
                                            frmt_date=formated_date.replace(".",'-')
                                            frmt_date= datetime.datetime.strptime(frmt_date, "%d-%m-%Y").strftime("%Y-%m-%d")
                                      
                                        status =rec['@status']
                                        new_str_date = rec['@date']
                                        new_formated_date = rec['@formatted_date']
                                        formated_time = rec['@time']
                                        venue = rec['@venue']
                                        static_id = rec['@static_id']
                                        fix_id = rec['@fix_id']
                                        match_id = rec['@id']
                                        events = rec['events']
                                        localteam_name = rec['localteam']['@name']
                                        localteam_goals = rec['localteam']['@goals']
                                        localteam_id = rec['localteam']['@id']
                                        visitorteam_name = rec['visitorteam']['@name']
                                        visitorteam_goals = rec['visitorteam']['@goals']
                                        visitorteam_id = rec['visitorteam']['@id']
                                        ht_score = rec['ht']['@score']
                                        if new_formated_date:
                                            new_frmt_date=new_formated_date.replace(".",'-')
                                            new_frmt_date= datetime.datetime.strptime(new_frmt_date, "%d-%m-%Y").strftime("%Y-%m-%d")
                                        # print("match_id="+match_id)
                                        cnt =  MatchGoalserve.objects.filter(match_id=match_id).count()
                                        if cnt == 0:
                                            ins = MatchGoalserve.objects.create(
                                                group_id= gid if gid!= '' else 0,
                                                league_id=league_id if league_id!= '' else 0,
                                                match_name=match_name,
                                                gid = gid if gid!= '' else 0,
                                                file_group=file_group,
                                                iscup=iscup,
                                                string_date = str_date if str_date!= '' else new_str_date,
                                                formated_date=frmt_date if frmt_date!= '' else new_frmt_date,
                                                formated_time=formated_time,
                                                time_status=status,
                                                venue=venue,
                                                static_id = static_id if static_id != '' else 0,
                                                fix_id= fix_id if fix_id != '' else 0,
                                                match_id = match_id if match_id != '' else 0,
                                                localteam_name=localteam_name,
                                                localteam_goals=localteam_goals,
                                                localteam_id = localteam_id if localteam_id != '' else 0,
                                                visitorteam_name=visitorteam_name,
                                                visitorteam_goals=visitorteam_goals,
                                                visitorteam_id = visitorteam_id if visitorteam_id != '' else 0,
                                                events=events,
                                                ht_score=ht_score,
                                            )

                                        TeamStatistics(localteam_id,match_id)
                                        TeamStatistics(visitorteam_id,match_id)
                                        predictionSave(match_id)
        
    return res

def storeTeamAndStatisticsOLD(team_id):
    import requests
    from db_table.models import MatchGoalserve
    from datetime import datetime, timedelta
    url = "https://www.goalserve.com/getfeed/c05d9fc7d36540dcdfaa08d9e34f661d/soccerstats/team/"+str(team_id)+"?json=1"
    response = requests.request("GET", url)
    # print(response.text)
    try:
        res =json.dumps(json.loads(response.text))
        # print(res)
        json_res = json.loads(res)

        if 'teams' in json_res:
            teamsData = json_res['teams']
            if 'team' in teamsData:
                teamsdata = teamsData['team']
                cnt =  TeamStatisticsGoalserve.objects.filter(team_id=teamsdata['@id']).count()
                if cnt ==0:
                    
                    TeamStatisticsGoalserve.objects.create(
                        team_id = teamsdata['@id'],
                        is_national_team = teamsdata['@is_national_team'],
                        name = teamsdata['name'],
                        fullname = teamsdata['fullname'],
                        country = teamsdata['country'],
                        founded = teamsdata['founded'],
                        league_rank = teamsdata['leagues']['@league_rank'],
                        league_ids = json.dumps(teamsdata['leagues']['league_id']),
                        venue_name = teamsdata['venue_name'],
                        venue_id = teamsdata['venue_id'],
                        venue_city = teamsdata['venue_city']['#cdata-section'],
                        venue_capacity = teamsdata['venue_capacity'],
                        venue_image = teamsdata['venue_image'],
                        image = teamsdata['image'],
                        coach_id = teamsdata['coach']['@id'],
                        coach_name =  teamsdata['coach']['@name'],

                        rank_home = teamsdata['statistics']['rank']['@home'] if '@home' in teamsdata['statistics']['rank']  else '',
                        rank_total = teamsdata['statistics']['rank']['@total'] if '@total' in teamsdata['statistics']['rank']  else '',
                        rank_away = teamsdata['statistics']['rank']['@away'] if '@away' in teamsdata['statistics']['rank']  else '',

                        win_home = teamsdata['statistics']['win']['@home'] if '@home' in teamsdata['statistics']['win']  else '',
                        win_total = teamsdata['statistics']['win']['@total'] if '@total' in teamsdata['statistics']['win']  else '',
                        win_away = teamsdata['statistics']['win']['@away'] if '@away' in teamsdata['statistics']['win']  else '',

                        draw_home = teamsdata['statistics']['draw']['@home'] if '@home' in teamsdata['statistics']['draw']  else '',
                        draw_total = teamsdata['statistics']['draw']['@total'] if '@total' in teamsdata['statistics']['draw']  else '',
                        draw_away = teamsdata['statistics']['draw']['@away'] if '@away' in teamsdata['statistics']['draw']  else '',

                        lost_home = teamsdata['statistics']['lost']['@home'] if '@home' in teamsdata['statistics']['lost']  else '',
                        lost_total = teamsdata['statistics']['lost']['@total'] if '@total' in teamsdata['statistics']['lost']  else '',
                        lost_away = teamsdata['statistics']['lost']['@away'] if '@away' in teamsdata['statistics']['lost']  else '',

                        goals_for_home = teamsdata['statistics']['goals_for']['@home'] if '@home' in teamsdata['statistics']['goals_for']  else '',
                        goals_for_total = teamsdata['statistics']['goals_for']['@total'] if '@total' in teamsdata['statistics']['goals_for']  else '',
                        goals_for_away = teamsdata['statistics']['goals_for']['@away'] if '@away' in teamsdata['statistics']['goals_for']  else '',

                        goals_against_home = teamsdata['statistics']['goals_against']['@home'] if '@home' in teamsdata['statistics']['goals_against']  else '',
                        goals_against_total = teamsdata['statistics']['goals_against']['@total'] if '@total' in teamsdata['statistics']['goals_against']  else '',
                        goals_against_away = teamsdata['statistics']['goals_against']['@away'] if '@away' in teamsdata['statistics']['goals_against']  else '',

                        clean_sheet_home = teamsdata['statistics']['rank']['@home'] if '@home' in teamsdata['statistics']['rank']  else '',
                        clean_sheet_total = teamsdata['statistics']['rank']['@total'] if '@total' in teamsdata['statistics']['rank']  else '',
                        clean_sheet_away = teamsdata['statistics']['rank']['@away'] if '@away' in teamsdata['statistics']['rank']  else '',

                        avg_goals_per_game_conceded_home = teamsdata['statistics']['avg_goals_per_game_conceded']['@home'] if '@home' in teamsdata['statistics']['avg_goals_per_game_conceded']  else '',
                        avg_goals_per_game_conceded_total = teamsdata['statistics']['avg_goals_per_game_conceded']['@total'] if '@total' in teamsdata['statistics']['avg_goals_per_game_conceded']  else '',
                        avg_goals_per_game_conceded_away = teamsdata['statistics']['avg_goals_per_game_conceded']['@away'] if '@away' in teamsdata['statistics']['avg_goals_per_game_conceded']  else '',

                        avg_first_goal_conceded_home = teamsdata['statistics']['avg_first_goal_conceded']['@home'] if '@home' in teamsdata['statistics']['avg_first_goal_conceded']  else '',
                        avg_first_goal_conceded_total = teamsdata['statistics']['avg_first_goal_conceded']['@total'] if '@total' in teamsdata['statistics']['avg_first_goal_conceded']  else '',
                        avg_first_goal_conceded_away = teamsdata['statistics']['avg_first_goal_conceded']['@away'] if '@away' in teamsdata['statistics']['avg_first_goal_conceded']  else '',

                        avg_first_goal_scored_home = teamsdata['statistics']['avg_first_goal_scored']['@home'] if '@home' in teamsdata['statistics']['avg_first_goal_scored']  else '',
                        avg_first_goal_scored_total = teamsdata['statistics']['avg_first_goal_scored']['@total'] if '@total' in teamsdata['statistics']['avg_first_goal_scored']  else '',
                        avg_first_goal_scored_away = teamsdata['statistics']['avg_first_goal_scored']['@away'] if '@away' in teamsdata['statistics']['avg_first_goal_scored']  else '',

                        avg_goals_per_game_scored_home = teamsdata['statistics']['avg_goals_per_game_scored']['@home'] if '@home' in teamsdata['statistics']['avg_goals_per_game_scored']  else '',
                        avg_goals_per_game_scored_total = teamsdata['statistics']['avg_goals_per_game_scored']['@total'] if '@total' in teamsdata['statistics']['avg_goals_per_game_scored']  else '',
                        avg_goals_per_game_scored_away = teamsdata['statistics']['avg_goals_per_game_scored']['@away'] if '@away' in teamsdata['statistics']['avg_goals_per_game_scored']  else '',

                        scoring_minutes = json.dumps(teamsdata['statistics']['scoring_minutes']['period']) if 'scoring_minutes' in teamsdata['statistics']  else '',
                    )
                    
                
                
                storeTeamSquadPlayer(teamsdata['squad'],team_id)

                if 'transfers' in teamsdata:
                    transfer = teamsdata['transfers']
                    StoreTransfermPlayerIN(transfer['in'],team_id)
                    StoreTransfermPlayerOUT(transfer['out'],team_id)
                
                if 'sidelined' in teamsdata:
                    StoreSideline(teamsdata['sidelined'],team_id)
                if 'trophies' in teamsdata:
                    StoreTeamsTrophy(teamsdata['trophies'],team_id)
                # if  'detailed_stats' in teamsdata:
                #     Storedetailed_stats(teamsdata['detailed_stats'],team_id)
        return teamsdata
    except:
        return 0

def storeTeamSquadPlayer(squad,team_id,match_id):
    dmt_app_log = 'logs/debug.log'
    logger = logging.getLogger('LibGlobalServe.py')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logHandler = handlers.RotatingFileHandler(dmt_app_log, maxBytes=5000000, backupCount=10)
    logHandler.setLevel(logging.INFO)
    # Here we set our logHandler's formatter
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    try:
        if "player" not in squad:
            return 0
        elif type(squad['player']) is list:
            players = squad['player']
            for player in players:
                cnt =  TeamPlayerSquadGoalserve.objects.filter(match_id =match_id,team_id = team_id,player_id = int(player['id'])).count()
                if cnt ==0:
                    TeamPlayerSquadGoalserve.objects.create(
                        match_id =match_id,
                        team_id = team_id,
                        age = player['age'] if 'age' in player  else '',
                        appearences = player['appearences'] if 'appearences' in player  else '',
                        assists = player['assists'] if 'assists' in player  else '',
                        blocks = player['blocks'] if 'blocks' in player  else '',
                        clearances = player['clearances'] if 'clearances' in player  else '',
                        crossesAccurate = player['crossesAccurate'] if 'crossesAccurate' in player  else '',
                        crossesTotal = player['crossesTotal'] if 'crossesTotal' in player  else '',
                        dispossesed = player['dispossesed'] if 'dispossesed' in player  else '',
                        dribbleAttempts = player['dribbleAttempts'] if 'dribbleAttempts' in player  else '',
                        dribbleSucc = player['dribbleSucc'] if 'dribbleSucc' in player  else '',
                        duelsTotal = player['duelsTotal'] if 'duelsTotal' in player  else '',
                        duelsWon = player['duelsWon'] if 'duelsWon' in player  else '',
                        fouldDrawn = player['fouldDrawn'] if 'fouldDrawn' in player  else '',
                        foulsCommitted = player['foulsCommitted'] if 'foulsCommitted' in player  else '',
                        goals = player['goals'] if 'goals' in player  else '',
                        goalsConceded = player['goalsConceded'] if 'goalsConceded' in player  else '',
                        player_id = player['id'] if 'id' in player  else '',
                        injured = player['injured'] if 'injured' in player  else '',
                        insideBoxSaves = player['insideBoxSaves'] if 'insideBoxSaves' in player  else '',
                        interceptions = player['interceptions'] if 'interceptions' in player  else '',
                        isCaptain = player['isCaptain'] if 'isCaptain' in player  else '',
                        keyPasses = player['keyPasses'] if 'keyPasses' in player  else '',
                        lineups = player['lineups'] if 'lineups' in player  else '',
                        minutes = player['minutes'] if 'minutes' in player  else '',
                        name = player['name'] if 'name' in player  else '',
                        number = player['number'] if 'number' in player  else '',
                        pAccuracy = player['pAccuracy'] if 'pAccuracy' in player  else '',
                        passes = player['passes'] if 'passes' in player  else '',
                        penComm = player['penComm'] if 'penComm' in player  else '',
                        penMissed = player['penMissed'] if 'penMissed' in player  else '',
                        penSaved = player['penSaved'] if 'penSaved' in player  else '',
                        penScored = player['penScored'] if 'penScored' in player  else '',
                        penWon = player['penWon'] if 'penWon' in player  else '',
                        position = player['position'] if 'position' in player  else '',
                        rating = player['rating'] if 'rating' in player  else '',
                        redcards = player['redcards'] if 'redcards' in player  else '',
                        saves = player['saves'] if 'saves' in player  else '',
                        shotsOn = player['shotsOn'] if 'shotsOn' in player  else '',
                        shotsTotal = player['shotsTotal'] if 'shotsTotal' in player  else '',
                        substitutes_on_bench = player['substitutes_on_bench'] if 'substitutes_on_bench' in player  else '',
                        substitute_in = player['substitute_in'] if 'substitute_in' in player  else '',
                        substitute_out = player['substitute_out'] if 'substitute_out' in player  else '',
                        tackles = player['tackles'] if 'tackles' in player  else '',
                        woordworks = player['woordworks'] if 'woordworks' in player  else '',
                        yellowcards = player['yellowcards'] if 'yellowcards' in player  else '',
                        yellowred = player['yellowred'] if 'yellowred' in player  else '',
                    )
        elif type(squad['player']) is dict:
            player = squad['player']
            cnt =  TeamPlayerSquadGoalserve.objects.filter(match_id =match_id,team_id = team_id,player_id = int(player['id'])).count()
            if cnt ==0:
                TeamPlayerSquadGoalserve.objects.create(
                    match_id =match_id,
                    team_id = team_id,
                    age = player['age'] if 'age' in player  else '',
                    appearences = player['appearences'] if 'appearences' in player  else '',
                    assists = player['assists'] if 'assists' in player  else '',
                    blocks = player['blocks'] if 'blocks' in player  else '',
                    clearances = player['clearances'] if 'clearances' in player  else '',
                    crossesAccurate = player['crossesAccurate'] if 'crossesAccurate' in player  else '',
                    crossesTotal = player['crossesTotal'] if 'crossesTotal' in player  else '',
                    dispossesed = player['dispossesed'] if 'dispossesed' in player  else '',
                    dribbleAttempts = player['dribbleAttempts'] if 'dribbleAttempts' in player  else '',
                    dribbleSucc = player['dribbleSucc'] if 'dribbleSucc' in player  else '',
                    duelsTotal = player['duelsTotal'] if 'duelsTotal' in player  else '',
                    duelsWon = player['duelsWon'] if 'duelsWon' in player  else '',
                    fouldDrawn = player['fouldDrawn'] if 'fouldDrawn' in player  else '',
                    foulsCommitted = player['foulsCommitted'] if 'foulsCommitted' in player  else '',
                    goals = player['goals'] if 'goals' in player  else '',
                    goalsConceded = player['goalsConceded'] if 'goalsConceded' in player  else '',
                    player_id = player['id'] if 'id' in player  else '',
                    injured = player['injured'] if 'injured' in player  else '',
                    insideBoxSaves = player['insideBoxSaves'] if 'insideBoxSaves' in player  else '',
                    interceptions = player['interceptions'] if 'interceptions' in player  else '',
                    isCaptain = player['isCaptain'] if 'isCaptain' in player  else '',
                    keyPasses = player['keyPasses'] if 'keyPasses' in player  else '',
                    lineups = player['lineups'] if 'lineups' in player  else '',
                    minutes = player['minutes'] if 'minutes' in player  else '',
                    name = player['name'] if 'name' in player  else '',
                    number = player['number'] if 'number' in player  else '',
                    pAccuracy = player['pAccuracy'] if 'pAccuracy' in player  else '',
                    passes = player['passes'] if 'passes' in player  else '',
                    penComm = player['penComm'] if 'penComm' in player  else '',
                    penMissed = player['penMissed'] if 'penMissed' in player  else '',
                    penSaved = player['penSaved'] if 'penSaved' in player  else '',
                    penScored = player['penScored'] if 'penScored' in player  else '',
                    penWon = player['penWon'] if 'penWon' in player  else '',
                    position = player['position'] if 'position' in player  else '',
                    rating = player['rating'] if 'rating' in player  else '',
                    redcards = player['redcards'] if 'redcards' in player  else '',
                    saves = player['saves'] if 'saves' in player  else '',
                    shotsOn = player['shotsOn'] if 'shotsOn' in player  else '',
                    shotsTotal = player['shotsTotal'] if 'shotsTotal' in player  else '',
                    substitutes_on_bench = player['substitutes_on_bench'] if 'substitutes_on_bench' in player  else '',
                    substitute_in = player['substitute_in'] if 'substitute_in' in player  else '',
                    substitute_out = player['substitute_out'] if 'substitute_out' in player  else '',
                    tackles = player['tackles'] if 'tackles' in player  else '',
                    woordworks = player['woordworks'] if 'woordworks' in player  else '',
                    yellowcards = player['yellowcards'] if 'yellowcards' in player  else '',
                    yellowred = player['yellowred'] if 'yellowred' in player  else '',
                )
    except:
        logger.info('Error : storeTeamSquadPlayer'+str(team_id))
    return 1

def StoreTransfermPlayerIN(transfers,team_id,match_id):
    # print(transfers)
    # if isinstance(transfers, list) and '@id' in transfers:
    dmt_app_log = 'logs/debug.log'
    logger = logging.getLogger('LibGlobalServe.py')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logHandler = handlers.RotatingFileHandler(dmt_app_log, maxBytes=5000000, backupCount=10)
    logHandler.setLevel(logging.INFO)
    # Here we set our logHandler's formatter
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    try:
        if type(transfers['player']) is dict:
            cnt =  TeamPlayerTransferINGoalserve.objects.filter(match_id =match_id,team_id = team_id,player_id = int(player['id'])).count()
            if cnt ==0:
                TeamPlayerTransferINGoalserve.objects.create(
                    match_id =match_id,
                    team_id = team_id,
                    age = player['age'] if 'age' in player  else '',
                    date = player['date'] if 'date' in player  else '0000-00-00',
                    from_team = player['from'] if 'from' in player  else '',
                    player_id = player['id'] if 'id' in player  else '',
                    name = player['name'] if 'name' in player  else '',
                    position = player['position'] if 'position' in player  else '',
                    from_team_id = player['team_id'] if 'team_id' in player  else '',
                    from_type = player['type'] if 'type' in player  else '',
                    transfer_type = 'IN',
                )
        elif type(transfers['player']) is list:
            # print(transfers)
            players = transfers['player']
            for player in players:
                cnt =  TeamPlayerTransferINGoalserve.objects.filter(match_id =match_id,team_id = team_id,player_id = player['id']).count()
                if cnt ==0:
                    TeamPlayerTransferINGoalserve.objects.create(
                        match_id =match_id,
                        team_id = team_id,
                        age = player['age'] if 'age' in player  else '',
                        date = player['date'] if 'date' in player  else '0000-00-00',
                        from_team = player['from'] if 'from' in player  else '',
                        player_id = player['id'] if 'id' in player  else '',
                        name = player['name'] if 'name' in player  else '',
                        position = player['position'] if 'position' in player  else '',
                        from_team_id = player['team_id'] if 'team_id' in player  else '',
                        from_type = player['type'] if 'type' in player  else '',
                        transfer_type = 'IN',
                    )
    except:
        logger.info('Error : StoreTransfermPlayerIN'+str(team_id))
    return 1

def StoreTransfermPlayerOUT(transfers,team_id,match_id):
    dmt_app_log = 'logs/debug.log'
    logger = logging.getLogger('LibGlobalServe.py')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logHandler = handlers.RotatingFileHandler(dmt_app_log, maxBytes=5000000, backupCount=10)
    logHandler.setLevel(logging.INFO)
    # Here we set our logHandler's formatter
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    try:
        if type(transfers['player']) is dict:
            cnt =  TeamPlayerTransferOUTGoalserve.objects.filter(match_id =match_id,team_id = team_id,player_id = int(player['id'])).count()
            if cnt ==0:
                TeamPlayerTransferOUTGoalserve.objects.create(
                    match_id =match_id,
                    team_id = team_id,
                    age = player['age'] if 'age' in player  else '',
                    date = player['date'] if 'date' in player  else '0000-00-00',
                    to_team = player['to'] if 'to' in player  else '',
                    player_id = player['id'] if 'id' in player  else '',
                    name = player['name'] if 'name' in player  else '',
                    position = player['position'] if 'position' in player  else '',
                    to_team_id = player['team_id'] if 'team_id' in player  else '',
                    from_type = player['type'] if 'type' in player  else '',
                    transfer_type = 'OUT',
                )
        elif type(transfers['player']) is list:
            players = transfers['player']
            # print(players)
            for player in players:
                cnt =  TeamPlayerTransferOUTGoalserve.objects.filter(match_id =match_id,team_id = team_id,player_id = player['id']).count()
                if cnt ==0:
                    TeamPlayerTransferOUTGoalserve.objects.create(
                        match_id =match_id,
                        team_id = team_id,
                        age = player['age'] if 'age' in player  else '',
                        date = player['date'] if 'date' in player  else '0000-00-00',
                        to_team = player['to'] if 'to' in player  else '',
                        player_id = player['id'] if 'id' in player  else '',
                        name = player['name'] if 'name' in player  else '',
                        position = player['position'] if 'position' in player  else '',
                        to_team_id = player['team_id'] if 'team_id' in player  else '',
                        from_type = player['type'] if 'type' in player  else '',
                        transfer_type = 'OUT',
                    )
    except:
        logger.info('Error : StoreTransfermPlayerOUT'+str(team_id))
    return 1

def StoreSideline(transfers,team_id,match_id):
    print('StoreSideline')
    dmt_app_log = 'logs/debug.log'
    logger = logging.getLogger('LibGlobalServe.py')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logHandler = handlers.RotatingFileHandler(dmt_app_log, maxBytes=5000000, backupCount=10)
    logHandler.setLevel(logging.INFO)
    # Here we set our logHandler's formatter
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    try:
        if type(transfers['player']) is list:
            
            players = transfers['player']
            for plr in players:
                cnt =  TeamPlayerSidelineGoalserve.objects.filter(match_id =match_id,team_id = team_id,player_id = int(plr['id'])).count()
                if cnt == 0:
                    print("TeamPlayerSidelineGoalserve-list",cnt)
                    TeamPlayerSidelineGoalserve.objects.create(
                        match_id =match_id,
                        team_id = team_id,
                        name = plr['name'] if 'name' in plr  else '',
                        player_id = plr['id'] if 'id' in plr  else '',
                        description = plr['description'] if 'description' in plr  else '',
                        start_date = plr['start_date'] if 'start_date' in plr  else '0000-00-00',
                        end_date = plr['end_date'] if 'end_date' in plr  else '0000-00-00',
                    )
        elif type(transfers['player']) is dict:
            player = transfers['player']
            cnt =  TeamPlayerSidelineGoalserve.objects.filter(match_id =match_id,team_id = team_id,player_id = int(player['id'])).count()
            if cnt ==0:
                print("TeamPlayerSidelineGoalserve-dict",cnt)
                TeamPlayerSidelineGoalserve.objects.create(
                    match_id =match_id,
                    team_id = team_id,
                    name = player['name'] if 'name' in player  else '',
                    player_id = player['id'] if 'id' in player  else '',
                    description = player['description'] if 'description' in player  else '',
                    start_date = player['start_date'] if 'start_date' in player  else '0000-00-00',
                    end_date = player['end_date'] if 'end_date' in player  else '0000-00-00',
                )
    except:
        logger.info('Error : StoreSideline'+str(team_id)) 
    return 1

def StoreTeamsTrophy(trophyes,team_id):
    dmt_app_log = 'logs/debug.log'
    logger = logging.getLogger('LibGlobalServe.py')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logHandler = handlers.RotatingFileHandler(dmt_app_log, maxBytes=5000000, backupCount=10)
    logHandler.setLevel(logging.INFO)
    # Here we set our logHandler's formatter
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    try:
        if 'trophy' in trophyes:
           for trf in trophyes['trophy']:
                TeamsTrophyGoalserve.objects.create(
                    team_id = team_id,
                    count = trf['count'] if 'count' in trf  else '',
                    country = trf['country'] if 'country' in trf  else '',
                    league = trf['league'] if 'league' in trf  else '',
                    seasons = json.dumps(trf['seasons']) if 'seasons' in trf  else '',
                    status = trf['status'] if 'status' in trf  else '', 
                )
    except:
        logger.info('Error : StoreTeamsTrophy'+str(team_id))
    return 1

def Storedetailed_stats(detailed_stats,team_id):
    dmt_app_log = 'logs/debug.log'
    logger = logging.getLogger('LibGlobalServe.py')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logHandler = handlers.RotatingFileHandler(dmt_app_log, maxBytes=5000000, backupCount=10)
    logHandler.setLevel(logging.INFO)
    # Here we set our logHandler's formatter
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    try:
        if 'league' in detailed_stats:
            details = detailed_stats['league']
            if type(detailed_stats['league']) is dict:
                # print(detailed_stats)
                cnt =  TeamsLeagueStatisticsToGoalserve.objects.filter(team_id = team_id,league_id = int(details['@id'])).count()
                if cnt ==0:
                    ls=TeamsLeagueStatisticsToGoalserve.objects.create(
                        team_id = team_id,
                        league_id = details['id'] if 'id' in details  else '',
                        name = details['name'] if 'name' in details  else '',
                        season = details['season'] if 'season' in details  else '',
                        fulltime_avg_corners_total = details['fulltime']['avg_corners']['total'] if 'total' in  details['fulltime']['avg_corners'] else '',
                        fulltime_avg_corners_home = details['fulltime']['avg_corners']['home'] if 'home' in  details['fulltime']['avg_corners'] else '',
                        fulltime_avg_corners_away = details['fulltime']['avg_corners']['away'] if 'away' in  details['fulltime']['avg_corners'] else '',
                        
                        fulltime_avg_first_goal_conceded_total = details['fulltime']['avg_first_goal_conceded']['total'] if 'total' in  details['fulltime']['avg_first_goal_conceded'] else '',
                        fulltime_avg_first_goal_conceded_home = details['fulltime']['avg_first_goal_conceded']['home'] if 'home' in  details['fulltime']['avg_first_goal_conceded'] else '',
                        fulltime_avg_first_goal_conceded_away = details['fulltime']['avg_first_goal_conceded']['away'] if 'away' in  details['fulltime']['avg_first_goal_conceded'] else '',
                        
                        fulltime_avg_first_goal_scored_total = details['fulltime']['avg_first_goal_scored']['total'] if 'total' in  details['fulltime']['avg_first_goal_scored'] else '',
                        fulltime_avg_first_goal_scored_home = details['fulltime']['avg_first_goal_scored']['home'] if 'home' in  details['fulltime']['avg_first_goal_scored'] else '',
                        fulltime_avg_first_goal_scored_away = details['fulltime']['avg_first_goal_scored']['away'] if 'away' in  details['fulltime']['avg_first_goal_scored'] else '',
                        
                        fulltime_avg_goals_per_game_conceded_total = details['fulltime']['avg_goals_per_game_conceded']['total'] if 'total' in  details['fulltime']['avg_goals_per_game_conceded'] else '',
                        fulltime_avg_goals_per_game_conceded_home = details['fulltime']['avg_goals_per_game_conceded']['home'] if 'home' in  details['fulltime']['avg_goals_per_game_conceded'] else '',
                        fulltime_avg_goals_per_game_conceded_away = details['fulltime']['avg_goals_per_game_conceded']['away'] if 'away' in  details['fulltime']['avg_goals_per_game_conceded'] else '',
                        
                        fulltime_avg_goals_per_game_scored_total = details['fulltime']['avg_goals_per_game_scored']['total'] if 'total' in  details['fulltime']['avg_goals_per_game_scored'] else '',
                        fulltime_avg_goals_per_game_scored_home = details['fulltime']['avg_goals_per_game_scored']['home'] if 'home' in  details['fulltime']['avg_goals_per_game_scored'] else '',
                        fulltime_avg_goals_per_game_scored_away = details['fulltime']['avg_goals_per_game_scored']['away'] if 'away' in  details['fulltime']['avg_goals_per_game_scored'] else '',
                        
                        fulltime_avg_redcards_total = details['fulltime']['avg_redcards']['total'] if 'total' in  details['fulltime']['avg_redcards'] else '',
                        fulltime_avg_redcards_home = details['fulltime']['avg_redcards']['home'] if 'home' in  details['fulltime']['avg_redcards'] else '',
                        fulltime_avg_redcards_away = details['fulltime']['avg_redcards']['away'] if 'away' in  details['fulltime']['avg_redcards'] else '',
                        
                        fulltime_avg_yellowcards_total = details['fulltime']['avg_yellowcards']['total'] if 'total' in  details['fulltime']['avg_yellowcards'] else '',
                        fulltime_avg_yellowcards_home = details['fulltime']['avg_yellowcards']['home'] if 'home' in  details['fulltime']['avg_yellowcards'] else '',
                        fulltime_avg_yellowcards_away = details['fulltime']['avg_yellowcards']['away'] if 'away' in  details['fulltime']['avg_yellowcards'] else '',

                        fulltime_biggest_defeat_total = details['fulltime']['biggest_defeat']['total'] if 'total' in  details['fulltime']['biggest_defeat'] else '',
                        fulltime_biggest_defeat_home = details['fulltime']['biggest_defeat']['total'] if 'total' in  details['fulltime']['biggest_defeat'] else '',
                        fulltime_biggest_defeat_away = details['fulltime']['biggest_defeat']['total'] if 'total' in  details['fulltime']['biggest_defeat'] else '',

                        fulltime_biggest_victory_total = details['fulltime']['biggest_victory']['total'] if 'total' in  details['fulltime']['biggest_victory'] else '',
                        fulltime_biggest_victory_home = details['fulltime']['biggest_victory']['home'] if 'home' in  details['fulltime']['biggest_victory'] else '',
                        fulltime_biggest_victory_away = details['fulltime']['biggest_victory']['away'] if 'away' in  details['fulltime']['biggest_victory'] else '',

                        fulltime_clean_sheet_total = details['fulltime']['clean_sheet']['total'] if 'total' in  details['fulltime']['clean_sheet'] else '',
                        fulltime_clean_sheet_home = details['fulltime']['clean_sheet']['home'] if 'home' in  details['fulltime']['clean_sheet'] else '',
                        fulltime_clean_sheet_away = details['fulltime']['clean_sheet']['away'] if 'away' in  details['fulltime']['clean_sheet'] else '',

                        fulltime_corners_total = details['fulltime']['corners']['total'] if 'total' in  details['fulltime']['corners'] else '',
                        fulltime_corners_home = details['fulltime']['corners']['home'] if 'home' in  details['fulltime']['corners'] else '',
                        fulltime_corners_away = details['fulltime']['corners']['away'] if 'away' in  details['fulltime']['corners'] else '',

                        fulltime_draw_total = details['fulltime']['draw']['total'] if 'total' in  details['fulltime']['draw'] else '',
                        fulltime_draw_home = details['fulltime']['draw']['home'] if 'home' in  details['fulltime']['draw'] else '',
                        fulltime_draw_away = details['fulltime']['draw']['away'] if 'away' in  details['fulltime']['draw'] else '',

                        fulltime_failed_to_score_total = details['fulltime']['failed_to_score']['total'] if 'total' in  details['fulltime']['failed_to_score'] else '',
                        fulltime_failed_to_score_home = details['fulltime']['failed_to_score']['home'] if 'home' in  details['fulltime']['failed_to_score'] else '',
                        fulltime_failed_to_score_away = details['fulltime']['failed_to_score']['away'] if 'away' in  details['fulltime']['failed_to_score'] else '',

                        fulltime_fouls_total = details['fulltime']['fouls']['total'] if 'total' in  details['fulltime']['fouls'] else '',
                        fulltime_fouls_home = details['fulltime']['fouls']['home'] if 'home' in  details['fulltime']['fouls'] else '',
                        fulltime_fouls_away = details['fulltime']['fouls']['away'] if 'away' in  details['fulltime']['fouls'] else '',

                        fulltime_goals_against_total = details['fulltime']['goals_against']['total'] if 'total' in  details['fulltime']['goals_against'] else '',
                        fulltime_goals_against_home = details['fulltime']['goals_against']['home'] if 'home' in  details['fulltime']['goals_against'] else '',
                        fulltime_goals_against_away = details['fulltime']['goals_against']['away'] if 'away' in  details['fulltime']['goals_against'] else '',

                        fulltime_goals_for_total = details['fulltime']['goals_for']['total'] if 'total' in  details['fulltime']['goals_for'] else '',
                        fulltime_goals_for_home = details['fulltime']['goals_for']['home'] if 'home' in  details['fulltime']['goals_for'] else '',
                        fulltime_goals_for_away = details['fulltime']['goals_for']['away'] if 'away' in  details['fulltime']['goals_for'] else '',

                        fulltime_lost_total = details['fulltime']['lost']['total'] if 'total' in  details['fulltime']['lost'] else '',
                        fulltime_lost_home = details['fulltime']['lost']['home'] if 'home' in  details['fulltime']['lost'] else '',
                        fulltime_lost_away = details['fulltime']['lost']['away'] if 'away' in  details['fulltime']['lost'] else '',

                        fulltime_offsides_total = details['fulltime']['offsides']['total'] if 'total' in  details['fulltime']['offsides'] else '',
                        fulltime_offsides_home = details['fulltime']['offsides']['home'] if 'home' in  details['fulltime']['offsides'] else '',
                        fulltime_offsides_away = details['fulltime']['offsides']['away'] if 'away' in  details['fulltime']['offsides'] else '',

                        fulltime_possession_total =details['fulltime']['possession']['total'] if 'total' in  details['fulltime']['possession'] else '',
                        fulltime_possession_home =details['fulltime']['possession']['home'] if 'home' in  details['fulltime']['possession'] else '',
                        fulltime_possession_away =details['fulltime']['possession']['away'] if 'away' in  details['fulltime']['possession'] else '',

                        fulltime_redcards_total = details['fulltime']['possession']['total'] if 'total' in  details['fulltime']['possession'] else '',
                        fulltime_redcards_home = details['fulltime']['possession']['home'] if 'home' in  details['fulltime']['possession'] else '',
                        fulltime_redcards_away = details['fulltime']['possession']['away'] if 'away' in  details['fulltime']['possession'] else '',

                        fulltime_shotsOnGoal_total = details['fulltime']['shotsOnGoal']['total'] if 'total' in  details['fulltime']['shotsOnGoal'] else '',
                        fulltime_shotsOnGoal_home = details['fulltime']['shotsOnGoal']['home'] if 'home' in  details['fulltime']['shotsOnGoal'] else '',
                        fulltime_shotsOnGoal_away = details['fulltime']['shotsOnGoal']['away'] if 'away' in  details['fulltime']['shotsOnGoal'] else '',

                        fulltime_shotsTotal_total = details['fulltime']['shotsTotal']['total'] if 'total' in  details['fulltime']['shotsTotal'] else '',
                        fulltime_shotsTotal_home = details['fulltime']['shotsTotal']['home'] if 'home' in  details['fulltime']['shotsTotal'] else '',
                        fulltime_shotsTotal_away = details['fulltime']['shotsTotal']['away'] if 'away' in  details['fulltime']['shotsTotal'] else '',

                        fulltime_yellowcards_total = details['fulltime']['yellowcards']['total'] if 'total' in  details['fulltime']['yellowcards'] else '',
                        fulltime_yellowcards_home = details['fulltime']['yellowcards']['home'] if 'home' in  details['fulltime']['yellowcards'] else '',
                        fulltime_yellowcards_away = details['fulltime']['yellowcards']['away'] if 'away' in  details['fulltime']['yellowcards'] else '',

                        fulltime_win_total = details['fulltime']['win']['total'] if 'total' in  details['fulltime']['win'] else '',
                        fulltime_win_home = details['fulltime']['win']['home'] if 'home' in  details['fulltime']['win'] else '',
                        fulltime_win_away = details['fulltime']['win']['away'] if 'away' in  details['fulltime']['win'] else '',
                        
                        firsthalf_avg_corners_total = details['firsthalf']['avg_corners']['total'] if 'total' in  details['firsthalf']['avg_corners'] else '',
                        firsthalf_avg_corners_home = details['firsthalf']['avg_corners']['home'] if 'home' in  details['firsthalf']['avg_corners'] else '',
                        firsthalf_avg_corners_away = details['firsthalf']['avg_corners']['away'] if 'away' in  details['firsthalf']['avg_corners'] else '',
                        
                        # firsthalf_avg_first_goal_conceded_total = details['firsthalf']['avg_first_goal_conceded']['total'] if 'total' in  details['firsthalf']['avg_first_goal_conceded'] else '',
                        # firsthalf_avg_first_goal_conceded_home = details['firsthalf']['avg_first_goal_conceded']['home'] if 'home' in  details['firsthalf']['avg_first_goal_conceded'] else '',
                        # firsthalf_avg_first_goal_conceded_away = details['firsthalf']['avg_first_goal_conceded']['away'] if 'away' in  details['firsthalf']['avg_first_goal_conceded'] else '',
                        
                        # firsthalf_avg_first_goal_scored_total = details['firsthalf']['avg_first_goal_scored']['total'] if 'total' in  details['firsthalf']['avg_first_goal_scored'] else '',
                        # firsthalf_avg_first_goal_scored_home = details['firsthalf']['avg_first_goal_scored']['home'] if 'home' in  details['firsthalf']['avg_first_goal_scored'] else '',
                        # firsthalf_avg_first_goal_scored_away = details['firsthalf']['avg_first_goal_scored']['away'] if 'away' in  details['firsthalf']['avg_first_goal_scored'] else '',
                        
                        firsthalf_avg_goals_per_game_conceded_total = details['firsthalf']['avg_goals_per_game_conceded']['total'] if 'total' in  details['firsthalf']['avg_goals_per_game_conceded'] else '',
                        firsthalf_avg_goals_per_game_conceded_home = details['firsthalf']['avg_goals_per_game_conceded']['home'] if 'home' in  details['firsthalf']['avg_goals_per_game_conceded'] else '',
                        firsthalf_avg_goals_per_game_conceded_away = details['firsthalf']['avg_goals_per_game_conceded']['away'] if 'away' in  details['firsthalf']['avg_goals_per_game_conceded'] else '',
                        
                        firsthalf_avg_goals_per_game_scored_total = details['firsthalf']['avg_goals_per_game_scored']['total'] if 'total' in  details['firsthalf']['avg_goals_per_game_scored'] else '',
                        firsthalf_avg_goals_per_game_scored_home = details['firsthalf']['avg_goals_per_game_scored']['home'] if 'home' in  details['firsthalf']['avg_goals_per_game_scored'] else '',
                        firsthalf_avg_goals_per_game_scored_away = details['firsthalf']['avg_goals_per_game_scored']['away'] if 'away' in  details['firsthalf']['avg_goals_per_game_scored'] else '',
                        
                        firsthalf_avg_redcards_total = details['firsthalf']['avg_redcards']['total'] if 'total' in  details['firsthalf']['avg_redcards'] else '',
                        firsthalf_avg_redcards_home = details['firsthalf']['avg_redcards']['home'] if 'home' in  details['firsthalf']['avg_redcards'] else '',
                        firsthalf_avg_redcards_away = details['firsthalf']['avg_redcards']['away'] if 'away' in  details['firsthalf']['avg_redcards'] else '',
                        
                        firsthalf_avg_yellowcards_total = details['firsthalf']['avg_yellowcards']['total'] if 'total' in  details['firsthalf']['avg_yellowcards'] else '',
                        firsthalf_avg_yellowcards_home = details['firsthalf']['avg_yellowcards']['home'] if 'home' in  details['firsthalf']['avg_yellowcards'] else '',
                        firsthalf_avg_yellowcards_away = details['firsthalf']['avg_yellowcards']['away'] if 'away' in  details['firsthalf']['avg_yellowcards'] else '',

                        # firsthalf_biggest_defeat_total = details['firsthalf']['biggest_defeat']['total'] if 'total' in  details['firsthalf']['biggest_defeat'] else '',
                        # firsthalf_biggest_defeat_home = details['firsthalf']['biggest_defeat']['home'] if 'home' in  details['firsthalf']['biggest_defeat'] else '',
                        # firsthalf_biggest_defeat_away = details['firsthalf']['biggest_defeat']['away'] if 'away' in  details['firsthalf']['biggest_defeat'] else '',

                        # firsthalf_biggest_victory_total = details['firsthalf']['biggest_victory']['total'] if 'total' in  details['firsthalf']['biggest_victory'] else '',
                        # firsthalf_biggest_victory_home = details['firsthalf']['biggest_victory']['total'] if 'total' in  details['firsthalf']['biggest_victory'] else '',
                        # firsthalf_biggest_victory_away = details['firsthalf']['biggest_victory']['total'] if 'total' in  details['firsthalf']['biggest_victory'] else '',

                        firsthalf_clean_sheet_total = details['firsthalf']['clean_sheet']['total'] if 'total' in  details['firsthalf']['clean_sheet'] else '',
                        firsthalf_clean_sheet_home = details['firsthalf']['clean_sheet']['total'] if 'total' in  details['firsthalf']['clean_sheet'] else '',
                        firsthalf_clean_sheet_away = details['firsthalf']['clean_sheet']['total'] if 'total' in  details['firsthalf']['clean_sheet'] else '',

                        firsthalf_corners_total = details['firsthalf']['corners']['total'] if 'total' in  details['firsthalf']['corners'] else '',
                        firsthalf_corners_home = details['firsthalf']['corners']['home'] if 'home' in  details['firsthalf']['corners'] else '',
                        firsthalf_corners_away = details['firsthalf']['corners']['away'] if 'away' in  details['firsthalf']['corners'] else '',

                        firsthalf_draw_total = details['firsthalf']['draw']['total'] if 'total' in  details['firsthalf']['draw'] else '',
                        firsthalf_draw_home = details['firsthalf']['draw']['home'] if 'home' in  details['firsthalf']['draw'] else '',
                        firsthalf_draw_away = details['firsthalf']['draw']['away'] if 'away' in  details['firsthalf']['draw'] else '',

                        firsthalf_failed_to_score_total = details['firsthalf']['failed_to_score']['total'] if 'total' in  details['firsthalf']['failed_to_score'] else '',
                        firsthalf_failed_to_score_home = details['firsthalf']['failed_to_score']['home'] if 'home' in  details['firsthalf']['failed_to_score'] else '',
                        firsthalf_failed_to_score_away = details['firsthalf']['failed_to_score']['away'] if 'away' in  details['firsthalf']['failed_to_score'] else '',

                        firsthalf_fouls_total = details['firsthalf']['fouls']['total'] if 'total' in  details['firsthalf']['fouls'] else '',
                        firsthalf_fouls_home = details['firsthalf']['fouls']['home'] if 'home' in  details['firsthalf']['fouls'] else '',
                        firsthalf_fouls_away = details['firsthalf']['fouls']['away'] if 'away' in  details['firsthalf']['fouls'] else '',

                        firsthalf_goals_against_total = details['firsthalf']['goals_against']['total'] if 'total' in  details['firsthalf']['goals_against'] else '',
                        firsthalf_goals_against_home = details['firsthalf']['goals_against']['home'] if 'home' in  details['firsthalf']['goals_against'] else '',
                        firsthalf_goals_against_away = details['firsthalf']['goals_against']['away'] if 'away' in  details['firsthalf']['goals_against'] else '',

                        firsthalf_goals_for_total = details['firsthalf']['goals_for']['total'] if 'total' in  details['firsthalf']['goals_for'] else '',
                        firsthalf_goals_for_home = details['firsthalf']['goals_for']['home'] if 'home' in  details['firsthalf']['goals_for'] else '',
                        firsthalf_goals_for_away = details['firsthalf']['goals_for']['away'] if 'away' in  details['firsthalf']['goals_for'] else '',

                        firsthalf_lost_total =  details['firsthalf']['lost']['total'] if 'total' in  details['firsthalf']['lost'] else '',
                        firsthalf_lost_home =  details['firsthalf']['lost']['home'] if 'home' in  details['firsthalf']['lost'] else '',
                        firsthalf_lost_away =  details['firsthalf']['lost']['away'] if 'away' in  details['firsthalf']['lost'] else '',

                        firsthalf_offsides_total = details['firsthalf']['offsides']['total'] if 'total' in  details['firsthalf']['offsides'] else '',
                        firsthalf_offsides_home = details['firsthalf']['offsides']['home'] if 'home' in  details['firsthalf']['offsides'] else '',
                        firsthalf_offsides_away = details['firsthalf']['offsides']['away'] if 'away' in  details['firsthalf']['offsides'] else '',

                        firsthalf_possession_total = details['firsthalf']['possession']['total'] if 'total' in  details['firsthalf']['possession'] else '',
                        firsthalf_possession_home = details['firsthalf']['possession']['home'] if 'home' in  details['firsthalf']['possession'] else '',
                        firsthalf_possession_away = details['firsthalf']['possession']['away'] if 'away' in  details['firsthalf']['possession'] else '',

                        firsthalf_redcards_total = details['firsthalf']['redcards']['total'] if 'total' in  details['firsthalf']['redcards'] else '',
                        firsthalf_redcards_home = details['firsthalf']['redcards']['home'] if 'home' in  details['firsthalf']['redcards'] else '',
                        firsthalf_redcards_away = details['firsthalf']['redcards']['away'] if 'away' in  details['firsthalf']['redcards'] else '',

                        firsthalf_shotsOnGoal_total = details['firsthalf']['shotsOnGoal']['total'] if 'total' in  details['firsthalf']['shotsOnGoal'] else '',
                        firsthalf_shotsOnGoal_home = details['firsthalf']['shotsOnGoal']['home'] if 'home' in  details['firsthalf']['shotsOnGoal'] else '',
                        firsthalf_shotsOnGoal_away = details['firsthalf']['shotsOnGoal']['away'] if 'away' in  details['firsthalf']['shotsOnGoal'] else '',

                        firsthalf_shotsTotal_total = details['firsthalf']['shotsTotal']['total'] if 'total' in  details['firsthalf']['shotsTotal'] else '',
                        firsthalf_shotsTotal_home = details['firsthalf']['shotsTotal']['home'] if 'home' in  details['firsthalf']['shotsTotal'] else '',
                        firsthalf_shotsTotal_away = details['firsthalf']['shotsTotal']['away'] if 'away' in  details['firsthalf']['shotsTotal'] else '',

                        firsthalf_yellowcards_total = details['firsthalf']['yellowcards']['total'] if 'total' in  details['firsthalf']['yellowcards'] else '',
                        firsthalf_yellowcards_home = details['firsthalf']['yellowcards']['home'] if 'home' in  details['firsthalf']['yellowcards'] else '',
                        firsthalf_yellowcards_away = details['firsthalf']['yellowcards']['away'] if 'away' in  details['firsthalf']['yellowcards'] else '',

                        firsthalf_win_total = details['firsthalf']['win']['total'] if 'total' in  details['firsthalf']['win'] else '',
                        firsthalf_win_home = details['firsthalf']['win']['home'] if 'home' in  details['firsthalf']['win'] else '',
                        firsthalf_win_away = details['firsthalf']['win']['away'] if 'away' in  details['firsthalf']['win'] else '',  


                        secondhalf_avg_corners_total = details['secondhalf']['avg_corners']['total'] if 'total' in  details['secondhalf']['avg_corners'] else '',
                        secondhalf_avg_corners_home = details['secondhalf']['avg_corners']['home'] if 'home' in  details['secondhalf']['avg_corners'] else '',
                        secondhalf_avg_corners_away = details['secondhalf']['avg_corners']['away'] if 'away' in  details['secondhalf']['avg_corners'] else '',
                        
                        # secondhalf_avg_first_goal_conceded_total = details['secondhalf']['avg_first_goal_conceded']['total'] if 'total' in  details['secondhalf']['avg_first_goal_conceded'] else '',
                        # secondhalf_avg_first_goal_conceded_home = details['secondhalf']['avg_first_goal_conceded']['home'] if 'home' in  details['secondhalf']['avg_first_goal_conceded'] else '',
                        # secondhalf_avg_first_goal_conceded_away = details['secondhalf']['avg_first_goal_conceded']['away'] if 'away' in  details['secondhalf']['avg_first_goal_conceded'] else '',
                        
                        # secondhalf_avg_first_goal_scored_total = details['secondhalf']['avg_first_goal_scored']['total'] if 'total' in  details['secondhalf']['avg_first_goal_scored'] else '',
                        # secondhalf_avg_first_goal_scored_home = details['secondhalf']['avg_first_goal_scored']['home'] if 'home' in  details['secondhalf']['avg_first_goal_scored'] else '',
                        # secondhalf_avg_first_goal_scored_away = details['secondhalf']['avg_first_goal_scored']['total'] if 'total' in  details['secondhalf']['avg_first_goal_scored'] else '',
                        
                        secondhalf_avg_goals_per_game_conceded_total = details['secondhalf']['avg_goals_per_game_conceded']['total'] if 'total' in  details['secondhalf']['avg_goals_per_game_conceded'] else '',
                        secondhalf_avg_goals_per_game_conceded_home = details['secondhalf']['avg_goals_per_game_conceded']['home'] if 'home' in  details['secondhalf']['avg_goals_per_game_conceded'] else '',
                        secondhalf_avg_goals_per_game_conceded_away = details['secondhalf']['avg_goals_per_game_conceded']['away'] if 'away' in  details['secondhalf']['avg_goals_per_game_conceded'] else '',
                        
                        secondhalf_avg_goals_per_game_scored_total =  details['secondhalf']['avg_goals_per_game_scored']['total'] if 'total' in  details['secondhalf']['avg_goals_per_game_scored'] else '',
                        secondhalf_avg_goals_per_game_scored_home =  details['secondhalf']['avg_goals_per_game_scored']['home'] if 'home' in  details['secondhalf']['avg_goals_per_game_scored'] else '',
                        secondhalf_avg_goals_per_game_scored_away =  details['secondhalf']['avg_goals_per_game_scored']['away'] if 'away' in  details['secondhalf']['avg_goals_per_game_scored'] else '',
                        
                        secondhalf_avg_redcards_total = details['secondhalf']['avg_redcards']['total'] if 'total' in  details['secondhalf']['avg_redcards'] else '',
                        secondhalf_avg_redcards_home = details['secondhalf']['avg_redcards']['home'] if 'home' in  details['secondhalf']['avg_redcards'] else '',
                        secondhalf_avg_redcards_away = details['secondhalf']['avg_redcards']['away'] if 'away' in  details['secondhalf']['avg_redcards'] else '',
                        
                        secondhalf_avg_yellowcards_total = details['secondhalf']['avg_yellowcards']['total'] if 'total' in  details['secondhalf']['avg_yellowcards'] else '',
                        secondhalf_avg_yellowcards_home = details['secondhalf']['avg_yellowcards']['home'] if 'home' in  details['secondhalf']['avg_yellowcards'] else '',
                        secondhalf_avg_yellowcards_away = details['secondhalf']['avg_yellowcards']['away'] if 'away' in  details['secondhalf']['avg_yellowcards'] else '',

                        # secondhalf_biggest_defeat_total = details['secondhalf']['biggest_defeat']['total'] if 'total' in  details['secondhalf']['biggest_defeat'] else '',
                        # secondhalf_biggest_defeat_home = details['secondhalf']['biggest_defeat']['home'] if 'home' in  details['secondhalf']['biggest_defeat'] else '',
                        # secondhalf_biggest_defeat_away = details['secondhalf']['biggest_defeat']['away'] if 'away' in  details['secondhalf']['biggest_defeat'] else '',

                        # secondhalf_biggest_victory_total = details['secondhalf']['biggest_victory']['total'] if 'total' in  details['secondhalf']['biggest_victory'] else '',
                        # secondhalf_biggest_victory_home = details['secondhalf']['biggest_victory']['total'] if 'total' in  details['secondhalf']['biggest_victory'] else '',
                        # secondhalf_biggest_victory_away = details['secondhalf']['biggest_victory']['total'] if 'total' in  details['secondhalf']['biggest_victory'] else '',

                        secondhalf_clean_sheet_total = details['secondhalf']['clean_sheet']['total'] if 'total' in  details['secondhalf']['clean_sheet'] else '',
                        secondhalf_clean_sheet_home = details['secondhalf']['clean_sheet']['home'] if 'home' in  details['secondhalf']['clean_sheet'] else '',
                        secondhalf_clean_sheet_away = details['secondhalf']['clean_sheet']['away'] if 'away' in  details['secondhalf']['clean_sheet'] else '',

                        secondhalf_corners_total = details['secondhalf']['corners']['total'] if 'total' in  details['secondhalf']['corners'] else '',
                        secondhalf_corners_home = details['secondhalf']['corners']['home'] if 'home' in  details['secondhalf']['corners'] else '',
                        secondhalf_corners_away = details['secondhalf']['corners']['away'] if 'away' in  details['secondhalf']['corners'] else '',

                        secondhalf_draw_total =  details['secondhalf']['draw']['total'] if 'total' in  details['secondhalf']['draw'] else '',
                        secondhalf_draw_home =  details['secondhalf']['draw']['home'] if 'home' in  details['secondhalf']['draw'] else '',
                        secondhalf_draw_away =  details['secondhalf']['draw']['away'] if 'away' in  details['secondhalf']['draw'] else '',

                        secondhalf_failed_to_score_total = details['secondhalf']['failed_to_score']['total'] if 'total' in  details['secondhalf']['failed_to_score'] else '',
                        secondhalf_failed_to_score_home = details['secondhalf']['failed_to_score']['home'] if 'home' in  details['secondhalf']['failed_to_score'] else '',
                        secondhalf_failed_to_score_away = details['secondhalf']['failed_to_score']['away'] if 'away' in  details['secondhalf']['failed_to_score'] else '',

                        secondhalf_fouls_total = details['secondhalf']['failed_to_score']['total'] if 'total' in  details['secondhalf']['failed_to_score'] else '',
                        secondhalf_fouls_home = details['secondhalf']['failed_to_score']['total'] if 'total' in  details['secondhalf']['failed_to_score'] else '',
                        secondhalf_fouls_away = details['secondhalf']['failed_to_score']['total'] if 'total' in  details['secondhalf']['failed_to_score'] else '',

                        secondhalf_goals_against_total = details['secondhalf']['goals_against']['total'] if 'total' in  details['secondhalf']['goals_against'] else '',
                        secondhalf_goals_against_home = details['secondhalf']['goals_against']['home'] if 'home' in  details['secondhalf']['goals_against'] else '',
                        secondhalf_goals_against_away = details['secondhalf']['goals_against']['away'] if 'away' in  details['secondhalf']['goals_against'] else '',

                        secondhalf_goals_for_total = details['secondhalf']['goals_for']['total'] if 'total' in  details['secondhalf']['goals_for'] else '',
                        secondhalf_goals_for_home = details['secondhalf']['goals_for']['home'] if 'home' in  details['secondhalf']['goals_for'] else '',
                        secondhalf_goals_for_away = details['secondhalf']['goals_for']['away'] if 'away' in  details['secondhalf']['goals_for'] else '',

                        secondhalf_lost_total = details['secondhalf']['lost']['total'] if 'total' in  details['secondhalf']['lost'] else '',
                        secondhalf_lost_home = details['secondhalf']['lost']['home'] if 'home' in  details['secondhalf']['lost'] else '',
                        secondhalf_lost_away = details['secondhalf']['lost']['away'] if 'away' in  details['secondhalf']['lost'] else '',

                        secondhalf_offsides_total = details['secondhalf']['offsides']['total'] if 'total' in  details['secondhalf']['offsides'] else '',
                        secondhalf_offsides_home = details['secondhalf']['offsides']['home'] if 'home' in  details['secondhalf']['offsides'] else '',
                        secondhalf_offsides_away = details['secondhalf']['offsides']['away'] if 'away' in  details['secondhalf']['offsides'] else '',

                        secondhalf_possession_total = details['secondhalf']['possession']['total'] if 'total' in  details['secondhalf']['possession'] else '',
                        secondhalf_possession_home = details['secondhalf']['possession']['home'] if 'home' in  details['secondhalf']['possession'] else '',
                        secondhalf_possession_away = details['secondhalf']['possession']['away'] if 'away' in  details['secondhalf']['possession'] else '',

                        secondhalf_redcards_total = details['secondhalf']['redcards']['total'] if 'total' in  details['secondhalf']['redcards'] else '',
                        secondhalf_redcards_home = details['secondhalf']['redcards']['home'] if 'home' in  details['secondhalf']['redcards'] else '',
                        secondhalf_redcards_away = details['secondhalf']['redcards']['away'] if 'away' in  details['secondhalf']['redcards'] else '',

                        secondhalf_shotsOnGoal_total = details['secondhalf']['shotsOnGoal']['total'] if 'total' in  details['secondhalf']['shotsOnGoal'] else '',
                        secondhalf_shotsOnGoal_home = details['secondhalf']['shotsOnGoal']['home'] if 'home' in  details['secondhalf']['shotsOnGoal'] else '',
                        secondhalf_shotsOnGoal_away = details['secondhalf']['shotsOnGoal']['away'] if 'away' in  details['secondhalf']['shotsOnGoal'] else '',

                        secondhalf_shotsTotal_total = details['secondhalf']['shotsTotal']['total'] if 'total' in  details['secondhalf']['shotsTotal'] else '',
                        secondhalf_shotsTotal_home = details['secondhalf']['shotsTotal']['home'] if 'home' in  details['secondhalf']['shotsTotal'] else '',
                        secondhalf_shotsTotal_away = details['secondhalf']['shotsTotal']['away'] if 'away' in  details['secondhalf']['shotsTotal'] else '',

                        secondhalf_yellowcards_total = details['secondhalf']['yellowcards']['total'] if 'total' in  details['secondhalf']['yellowcards'] else '',
                        secondhalf_yellowcards_home = details['secondhalf']['yellowcards']['home'] if 'home' in  details['secondhalf']['yellowcards'] else '',
                        secondhalf_yellowcards_away = details['secondhalf']['yellowcards']['away'] if 'away' in  details['secondhalf']['yellowcards'] else '',

                        secondhalf_win_total = details['secondhalf']['win']['total'] if 'total' in  details['secondhalf']['win'] else '',
                        secondhalf_win_home = details['secondhalf']['win']['home'] if 'home' in  details['secondhalf']['win'] else '',
                        secondhalf_win_away = details['secondhalf']['win']['away'] if 'away' in  details['secondhalf']['win'] else '',

                        scoring_minutes  =  json.dumps(details['scoring_minutes']['period']) if 'period' in details['scoring_minutes']  else '',
                        goals_conceded_minutes  = json.dumps(details['goals_conceded_minutes']['period']) if 'period' in details['goals_conceded_minutes']  else '',
                        redcard_minutes  = json.dumps(details['redcard_minutes']['period']) if 'period' in details['redcard_minutes']  else '',
                    )
                    # ls.save()
                    
                        
            elif type(detailed_stats['league']) is list:
                for trf in details:
                    
                    print(trf['name'])
                    print("---------------")
                    cnt =  TeamsLeagueStatisticsToGoalserve.objects.filter(team_id = team_id,league_id = int(trf['id'])).count()
                    if cnt == 0:
                        print(cnt)
                        ls=TeamsLeagueStatisticsToGoalserve.objects.create(
                            team_id = team_id,
                            league_id = trf['id'] if 'id' in trf  else '',
                            name = trf['name'] if 'name' in trf  else '',
                            season = trf['season'] if 'season' in trf  else '',
                            fulltime_avg_corners_total = trf['fulltime']['avg_corners']['total'] if 'total' in  trf['fulltime']['avg_corners'] else '',
                            fulltime_avg_corners_home = trf['fulltime']['avg_corners']['home'] if 'home' in  trf['fulltime']['avg_corners'] else '',
                            fulltime_avg_corners_away = trf['fulltime']['avg_corners']['away'] if 'away' in  trf['fulltime']['avg_corners'] else '',
                            
                            fulltime_avg_first_goal_conceded_total = trf['fulltime']['avg_first_goal_conceded']['total'] if 'total' in  trf['fulltime']['avg_first_goal_conceded'] else '',
                            fulltime_avg_first_goal_conceded_home = trf['fulltime']['avg_first_goal_conceded']['home'] if 'home' in  trf['fulltime']['avg_first_goal_conceded'] else '',
                            fulltime_avg_first_goal_conceded_away = trf['fulltime']['avg_first_goal_conceded']['away'] if 'away' in  trf['fulltime']['avg_first_goal_conceded'] else '',
                            
                            fulltime_avg_first_goal_scored_total = trf['fulltime']['avg_first_goal_scored']['total'] if 'total' in  trf['fulltime']['avg_first_goal_scored'] else '',
                            fulltime_avg_first_goal_scored_home = trf['fulltime']['avg_first_goal_scored']['home'] if 'home' in  trf['fulltime']['avg_first_goal_scored'] else '',
                            fulltime_avg_first_goal_scored_away = trf['fulltime']['avg_first_goal_scored']['away'] if 'away' in  trf['fulltime']['avg_first_goal_scored'] else '',
                            
                            fulltime_avg_goals_per_game_conceded_total = trf['fulltime']['avg_goals_per_game_conceded']['total'] if 'total' in  trf['fulltime']['avg_goals_per_game_conceded'] else '',
                            fulltime_avg_goals_per_game_conceded_home = trf['fulltime']['avg_goals_per_game_conceded']['home'] if 'home' in  trf['fulltime']['avg_goals_per_game_conceded'] else '',
                            fulltime_avg_goals_per_game_conceded_away = trf['fulltime']['avg_goals_per_game_conceded']['away'] if 'away' in  trf['fulltime']['avg_goals_per_game_conceded'] else '',
                            
                            fulltime_avg_goals_per_game_scored_total = trf['fulltime']['avg_goals_per_game_scored']['total'] if 'total' in  trf['fulltime']['avg_goals_per_game_scored'] else '',
                            fulltime_avg_goals_per_game_scored_home = trf['fulltime']['avg_goals_per_game_scored']['home'] if 'home' in  trf['fulltime']['avg_goals_per_game_scored'] else '',
                            fulltime_avg_goals_per_game_scored_away = trf['fulltime']['avg_goals_per_game_scored']['away'] if 'away' in  trf['fulltime']['avg_goals_per_game_scored'] else '',
                            
                            fulltime_avg_redcards_total = trf['fulltime']['avg_redcards']['total'] if 'total' in  trf['fulltime']['avg_redcards'] else '',
                            fulltime_avg_redcards_home = trf['fulltime']['avg_redcards']['home'] if 'home' in  trf['fulltime']['avg_redcards'] else '',
                            fulltime_avg_redcards_away = trf['fulltime']['avg_redcards']['away'] if 'away' in  trf['fulltime']['avg_redcards'] else '',
                            
                            fulltime_avg_yellowcards_total = trf['fulltime']['avg_yellowcards']['total'] if 'total' in  trf['fulltime']['avg_yellowcards'] else '',
                            fulltime_avg_yellowcards_home = trf['fulltime']['avg_yellowcards']['home'] if 'home' in  trf['fulltime']['avg_yellowcards'] else '',
                            fulltime_avg_yellowcards_away = trf['fulltime']['avg_yellowcards']['away'] if 'away' in  trf['fulltime']['avg_yellowcards'] else '',

                            fulltime_biggest_defeat_total = trf['fulltime']['biggest_defeat']['total'] if 'total' in  trf['fulltime']['biggest_defeat'] else '',
                            fulltime_biggest_defeat_home = trf['fulltime']['biggest_defeat']['total'] if 'total' in  trf['fulltime']['biggest_defeat'] else '',
                            fulltime_biggest_defeat_away = trf['fulltime']['biggest_defeat']['total'] if 'total' in  trf['fulltime']['biggest_defeat'] else '',

                            fulltime_biggest_victory_total = trf['fulltime']['biggest_victory']['total'] if 'total' in  trf['fulltime']['biggest_victory'] else '',
                            fulltime_biggest_victory_home = trf['fulltime']['biggest_victory']['home'] if 'home' in  trf['fulltime']['biggest_victory'] else '',
                            fulltime_biggest_victory_away = trf['fulltime']['biggest_victory']['away'] if 'away' in  trf['fulltime']['biggest_victory'] else '',

                            fulltime_clean_sheet_total = trf['fulltime']['clean_sheet']['total'] if 'total' in  trf['fulltime']['clean_sheet'] else '',
                            fulltime_clean_sheet_home = trf['fulltime']['clean_sheet']['home'] if 'home' in  trf['fulltime']['clean_sheet'] else '',
                            fulltime_clean_sheet_away = trf['fulltime']['clean_sheet']['away'] if 'away' in  trf['fulltime']['clean_sheet'] else '',

                            fulltime_corners_total = trf['fulltime']['corners']['total'] if 'total' in  trf['fulltime']['corners'] else '',
                            fulltime_corners_home = trf['fulltime']['corners']['home'] if 'home' in  trf['fulltime']['corners'] else '',
                            fulltime_corners_away = trf['fulltime']['corners']['away'] if 'away' in  trf['fulltime']['corners'] else '',

                            fulltime_draw_total = trf['fulltime']['draw']['total'] if 'total' in  trf['fulltime']['draw'] else '',
                            fulltime_draw_home = trf['fulltime']['draw']['home'] if 'home' in  trf['fulltime']['draw'] else '',
                            fulltime_draw_away = trf['fulltime']['draw']['away'] if 'away' in  trf['fulltime']['draw'] else '',

                            fulltime_failed_to_score_total = trf['fulltime']['failed_to_score']['total'] if 'total' in  trf['fulltime']['failed_to_score'] else '',
                            fulltime_failed_to_score_home = trf['fulltime']['failed_to_score']['home'] if 'home' in  trf['fulltime']['failed_to_score'] else '',
                            fulltime_failed_to_score_away = trf['fulltime']['failed_to_score']['away'] if 'away' in  trf['fulltime']['failed_to_score'] else '',

                            fulltime_fouls_total = trf['fulltime']['fouls']['total'] if 'total' in  trf['fulltime']['fouls'] else '',
                            fulltime_fouls_home = trf['fulltime']['fouls']['home'] if 'home' in  trf['fulltime']['fouls'] else '',
                            fulltime_fouls_away = trf['fulltime']['fouls']['away'] if 'away' in  trf['fulltime']['fouls'] else '',

                            fulltime_goals_against_total = trf['fulltime']['goals_against']['total'] if 'total' in  trf['fulltime']['goals_against'] else '',
                            fulltime_goals_against_home = trf['fulltime']['goals_against']['home'] if 'home' in  trf['fulltime']['goals_against'] else '',
                            fulltime_goals_against_away = trf['fulltime']['goals_against']['away'] if 'away' in  trf['fulltime']['goals_against'] else '',

                            fulltime_goals_for_total = trf['fulltime']['goals_for']['total'] if 'total' in  trf['fulltime']['goals_for'] else '',
                            fulltime_goals_for_home = trf['fulltime']['goals_for']['home'] if 'home' in  trf['fulltime']['goals_for'] else '',
                            fulltime_goals_for_away = trf['fulltime']['goals_for']['away'] if 'away' in  trf['fulltime']['goals_for'] else '',

                            fulltime_lost_total = trf['fulltime']['lost']['total'] if 'total' in  trf['fulltime']['lost'] else '',
                            fulltime_lost_home = trf['fulltime']['lost']['home'] if 'home' in  trf['fulltime']['lost'] else '',
                            fulltime_lost_away = trf['fulltime']['lost']['away'] if 'away' in  trf['fulltime']['lost'] else '',

                            fulltime_offsides_total = trf['fulltime']['offsides']['total'] if 'total' in  trf['fulltime']['offsides'] else '',
                            fulltime_offsides_home = trf['fulltime']['offsides']['home'] if 'home' in  trf['fulltime']['offsides'] else '',
                            fulltime_offsides_away = trf['fulltime']['offsides']['away'] if 'away' in  trf['fulltime']['offsides'] else '',

                            fulltime_possession_total =trf['fulltime']['possession']['total'] if 'total' in  trf['fulltime']['possession'] else '',
                            fulltime_possession_home =trf['fulltime']['possession']['home'] if 'home' in  trf['fulltime']['possession'] else '',
                            fulltime_possession_away =trf['fulltime']['possession']['away'] if 'away' in  trf['fulltime']['possession'] else '',

                            fulltime_redcards_total = trf['fulltime']['possession']['total'] if 'total' in  trf['fulltime']['possession'] else '',
                            fulltime_redcards_home = trf['fulltime']['possession']['home'] if 'home' in  trf['fulltime']['possession'] else '',
                            fulltime_redcards_away = trf['fulltime']['possession']['away'] if 'away' in  trf['fulltime']['possession'] else '',

                            fulltime_shotsOnGoal_total = trf['fulltime']['shotsOnGoal']['total'] if 'total' in  trf['fulltime']['shotsOnGoal'] else '',
                            fulltime_shotsOnGoal_home = trf['fulltime']['shotsOnGoal']['home'] if 'home' in  trf['fulltime']['shotsOnGoal'] else '',
                            fulltime_shotsOnGoal_away = trf['fulltime']['shotsOnGoal']['away'] if 'away' in  trf['fulltime']['shotsOnGoal'] else '',

                            fulltime_shotsTotal_total = trf['fulltime']['shotsTotal']['total'] if 'total' in  trf['fulltime']['shotsTotal'] else '',
                            fulltime_shotsTotal_home = trf['fulltime']['shotsTotal']['home'] if 'home' in  trf['fulltime']['shotsTotal'] else '',
                            fulltime_shotsTotal_away = trf['fulltime']['shotsTotal']['away'] if 'away' in  trf['fulltime']['shotsTotal'] else '',

                            fulltime_yellowcards_total = trf['fulltime']['yellowcards']['total'] if 'total' in  trf['fulltime']['yellowcards'] else '',
                            fulltime_yellowcards_home = trf['fulltime']['yellowcards']['home'] if 'home' in  trf['fulltime']['yellowcards'] else '',
                            fulltime_yellowcards_away = trf['fulltime']['yellowcards']['away'] if 'away' in  trf['fulltime']['yellowcards'] else '',

                            fulltime_win_total = trf['fulltime']['win']['total'] if 'total' in  trf['fulltime']['win'] else '',
                            fulltime_win_home = trf['fulltime']['win']['home'] if 'home' in  trf['fulltime']['win'] else '',
                            fulltime_win_away = trf['fulltime']['win']['away'] if 'away' in  trf['fulltime']['win'] else '',
                            
                            firsthalf_avg_corners_total = trf['firsthalf']['avg_corners']['total'] if 'total' in  trf['firsthalf']['avg_corners'] else '',
                            firsthalf_avg_corners_home = trf['firsthalf']['avg_corners']['home'] if 'home' in  trf['firsthalf']['avg_corners'] else '',
                            firsthalf_avg_corners_away = trf['firsthalf']['avg_corners']['away'] if 'away' in  trf['firsthalf']['avg_corners'] else '',
                            
                            # firsthalf_avg_first_goal_conceded_total = trf['firsthalf']['avg_first_goal_conceded']['total'] if 'total' in  trf['firsthalf']['avg_first_goal_conceded'] else '',
                            # firsthalf_avg_first_goal_conceded_home = trf['firsthalf']['avg_first_goal_conceded']['home'] if 'home' in  trf['firsthalf']['avg_first_goal_conceded'] else '',
                            # firsthalf_avg_first_goal_conceded_away = trf['firsthalf']['avg_first_goal_conceded']['away'] if 'away' in  trf['firsthalf']['avg_first_goal_conceded'] else '',
                            
                            # firsthalf_avg_first_goal_scored_total = trf['firsthalf']['avg_first_goal_scored']['total'] if 'total' in  trf['firsthalf']['avg_first_goal_scored'] else '',
                            # firsthalf_avg_first_goal_scored_home = trf['firsthalf']['avg_first_goal_scored']['home'] if 'home' in  trf['firsthalf']['avg_first_goal_scored'] else '',
                            # firsthalf_avg_first_goal_scored_away = trf['firsthalf']['avg_first_goal_scored']['away'] if 'away' in  trf['firsthalf']['avg_first_goal_scored'] else '',
                            
                            firsthalf_avg_goals_per_game_conceded_total = trf['firsthalf']['avg_goals_per_game_conceded']['total'] if 'total' in  trf['firsthalf']['avg_goals_per_game_conceded'] else '',
                            firsthalf_avg_goals_per_game_conceded_home = trf['firsthalf']['avg_goals_per_game_conceded']['home'] if 'home' in  trf['firsthalf']['avg_goals_per_game_conceded'] else '',
                            firsthalf_avg_goals_per_game_conceded_away = trf['firsthalf']['avg_goals_per_game_conceded']['away'] if 'away' in  trf['firsthalf']['avg_goals_per_game_conceded'] else '',
                            
                            firsthalf_avg_goals_per_game_scored_total = trf['firsthalf']['avg_goals_per_game_scored']['total'] if 'total' in  trf['firsthalf']['avg_goals_per_game_scored'] else '',
                            firsthalf_avg_goals_per_game_scored_home = trf['firsthalf']['avg_goals_per_game_scored']['home'] if 'home' in  trf['firsthalf']['avg_goals_per_game_scored'] else '',
                            firsthalf_avg_goals_per_game_scored_away = trf['firsthalf']['avg_goals_per_game_scored']['away'] if 'away' in  trf['firsthalf']['avg_goals_per_game_scored'] else '',
                            
                            firsthalf_avg_redcards_total = trf['firsthalf']['avg_redcards']['total'] if 'total' in  trf['firsthalf']['avg_redcards'] else '',
                            firsthalf_avg_redcards_home = trf['firsthalf']['avg_redcards']['home'] if 'home' in  trf['firsthalf']['avg_redcards'] else '',
                            firsthalf_avg_redcards_away = trf['firsthalf']['avg_redcards']['away'] if 'away' in  trf['firsthalf']['avg_redcards'] else '',
                            
                            firsthalf_avg_yellowcards_total = trf['firsthalf']['avg_yellowcards']['total'] if 'total' in  trf['firsthalf']['avg_yellowcards'] else '',
                            firsthalf_avg_yellowcards_home = trf['firsthalf']['avg_yellowcards']['home'] if 'home' in  trf['firsthalf']['avg_yellowcards'] else '',
                            firsthalf_avg_yellowcards_away = trf['firsthalf']['avg_yellowcards']['away'] if 'away' in  trf['firsthalf']['avg_yellowcards'] else '',

                            # firsthalf_biggest_defeat_total = trf['firsthalf']['biggest_defeat']['total'] if 'total' in  trf['firsthalf']['biggest_defeat'] else '',
                            # firsthalf_biggest_defeat_home = trf['firsthalf']['biggest_defeat']['home'] if 'home' in  trf['firsthalf']['biggest_defeat'] else '',
                            # firsthalf_biggest_defeat_away = trf['firsthalf']['biggest_defeat']['away'] if 'away' in  trf['firsthalf']['biggest_defeat'] else '',

                            # firsthalf_biggest_victory_total = trf['firsthalf']['biggest_victory']['total'] if 'total' in  trf['firsthalf']['biggest_victory'] else '',
                            # firsthalf_biggest_victory_home = trf['firsthalf']['biggest_victory']['total'] if 'total' in  trf['firsthalf']['biggest_victory'] else '',
                            # firsthalf_biggest_victory_away = trf['firsthalf']['biggest_victory']['total'] if 'total' in  trf['firsthalf']['biggest_victory'] else '',

                            firsthalf_clean_sheet_total = trf['firsthalf']['clean_sheet']['total'] if 'total' in  trf['firsthalf']['clean_sheet'] else '',
                            firsthalf_clean_sheet_home = trf['firsthalf']['clean_sheet']['total'] if 'total' in  trf['firsthalf']['clean_sheet'] else '',
                            firsthalf_clean_sheet_away = trf['firsthalf']['clean_sheet']['total'] if 'total' in  trf['firsthalf']['clean_sheet'] else '',

                            firsthalf_corners_total = trf['firsthalf']['corners']['total'] if 'total' in  trf['firsthalf']['corners'] else '',
                            firsthalf_corners_home = trf['firsthalf']['corners']['home'] if 'home' in  trf['firsthalf']['corners'] else '',
                            firsthalf_corners_away = trf['firsthalf']['corners']['away'] if 'away' in  trf['firsthalf']['corners'] else '',

                            firsthalf_draw_total = trf['firsthalf']['draw']['total'] if 'total' in  trf['firsthalf']['draw'] else '',
                            firsthalf_draw_home = trf['firsthalf']['draw']['home'] if 'home' in  trf['firsthalf']['draw'] else '',
                            firsthalf_draw_away = trf['firsthalf']['draw']['away'] if 'away' in  trf['firsthalf']['draw'] else '',

                            firsthalf_failed_to_score_total = trf['firsthalf']['failed_to_score']['total'] if 'total' in  trf['firsthalf']['failed_to_score'] else '',
                            firsthalf_failed_to_score_home = trf['firsthalf']['failed_to_score']['home'] if 'home' in  trf['firsthalf']['failed_to_score'] else '',
                            firsthalf_failed_to_score_away = trf['firsthalf']['failed_to_score']['away'] if 'away' in  trf['firsthalf']['failed_to_score'] else '',

                            firsthalf_fouls_total = trf['firsthalf']['fouls']['total'] if 'total' in  trf['firsthalf']['fouls'] else '',
                            firsthalf_fouls_home = trf['firsthalf']['fouls']['home'] if 'home' in  trf['firsthalf']['fouls'] else '',
                            firsthalf_fouls_away = trf['firsthalf']['fouls']['away'] if 'away' in  trf['firsthalf']['fouls'] else '',

                            firsthalf_goals_against_total = trf['firsthalf']['goals_against']['total'] if 'total' in  trf['firsthalf']['goals_against'] else '',
                            firsthalf_goals_against_home = trf['firsthalf']['goals_against']['home'] if 'home' in  trf['firsthalf']['goals_against'] else '',
                            firsthalf_goals_against_away = trf['firsthalf']['goals_against']['away'] if 'away' in  trf['firsthalf']['goals_against'] else '',

                            firsthalf_goals_for_total = trf['firsthalf']['goals_for']['total'] if 'total' in  trf['firsthalf']['goals_for'] else '',
                            firsthalf_goals_for_home = trf['firsthalf']['goals_for']['home'] if 'home' in  trf['firsthalf']['goals_for'] else '',
                            firsthalf_goals_for_away = trf['firsthalf']['goals_for']['away'] if 'away' in  trf['firsthalf']['goals_for'] else '',

                            firsthalf_lost_total =  trf['firsthalf']['lost']['total'] if 'total' in  trf['firsthalf']['lost'] else '',
                            firsthalf_lost_home =  trf['firsthalf']['lost']['home'] if 'home' in  trf['firsthalf']['lost'] else '',
                            firsthalf_lost_away =  trf['firsthalf']['lost']['away'] if 'away' in  trf['firsthalf']['lost'] else '',

                            firsthalf_offsides_total = trf['firsthalf']['offsides']['total'] if 'total' in  trf['firsthalf']['offsides'] else '',
                            firsthalf_offsides_home = trf['firsthalf']['offsides']['home'] if 'home' in  trf['firsthalf']['offsides'] else '',
                            firsthalf_offsides_away = trf['firsthalf']['offsides']['away'] if 'away' in  trf['firsthalf']['offsides'] else '',

                            firsthalf_possession_total = trf['firsthalf']['possession']['total'] if 'total' in  trf['firsthalf']['possession'] else '',
                            firsthalf_possession_home = trf['firsthalf']['possession']['home'] if 'home' in  trf['firsthalf']['possession'] else '',
                            firsthalf_possession_away = trf['firsthalf']['possession']['away'] if 'away' in  trf['firsthalf']['possession'] else '',

                            firsthalf_redcards_total = trf['firsthalf']['redcards']['total'] if 'total' in  trf['firsthalf']['redcards'] else '',
                            firsthalf_redcards_home = trf['firsthalf']['redcards']['home'] if 'home' in  trf['firsthalf']['redcards'] else '',
                            firsthalf_redcards_away = trf['firsthalf']['redcards']['away'] if 'away' in  trf['firsthalf']['redcards'] else '',

                            firsthalf_shotsOnGoal_total = trf['firsthalf']['shotsOnGoal']['total'] if 'total' in  trf['firsthalf']['shotsOnGoal'] else '',
                            firsthalf_shotsOnGoal_home = trf['firsthalf']['shotsOnGoal']['home'] if 'home' in  trf['firsthalf']['shotsOnGoal'] else '',
                            firsthalf_shotsOnGoal_away = trf['firsthalf']['shotsOnGoal']['away'] if 'away' in  trf['firsthalf']['shotsOnGoal'] else '',

                            firsthalf_shotsTotal_total = trf['firsthalf']['shotsTotal']['total'] if 'total' in  trf['firsthalf']['shotsTotal'] else '',
                            firsthalf_shotsTotal_home = trf['firsthalf']['shotsTotal']['home'] if 'home' in  trf['firsthalf']['shotsTotal'] else '',
                            firsthalf_shotsTotal_away = trf['firsthalf']['shotsTotal']['away'] if 'away' in  trf['firsthalf']['shotsTotal'] else '',

                            firsthalf_yellowcards_total = trf['firsthalf']['yellowcards']['total'] if 'total' in  trf['firsthalf']['yellowcards'] else '',
                            firsthalf_yellowcards_home = trf['firsthalf']['yellowcards']['home'] if 'home' in  trf['firsthalf']['yellowcards'] else '',
                            firsthalf_yellowcards_away = trf['firsthalf']['yellowcards']['away'] if 'away' in  trf['firsthalf']['yellowcards'] else '',

                            firsthalf_win_total = trf['firsthalf']['win']['total'] if 'total' in  trf['firsthalf']['win'] else '',
                            firsthalf_win_home = trf['firsthalf']['win']['home'] if 'home' in  trf['firsthalf']['win'] else '',
                            firsthalf_win_away = trf['firsthalf']['win']['away'] if 'away' in  trf['firsthalf']['win'] else '',  


                            secondhalf_avg_corners_total = trf['secondhalf']['avg_corners']['total'] if 'total' in  trf['secondhalf']['avg_corners'] else '',
                            secondhalf_avg_corners_home = trf['secondhalf']['avg_corners']['home'] if 'home' in  trf['secondhalf']['avg_corners'] else '',
                            secondhalf_avg_corners_away = trf['secondhalf']['avg_corners']['away'] if 'away' in  trf['secondhalf']['avg_corners'] else '',
                            
                            # secondhalf_avg_first_goal_conceded_total = trf['secondhalf']['avg_first_goal_conceded']['total'] if 'total' in  trf['secondhalf']['avg_first_goal_conceded'] else '',
                            # secondhalf_avg_first_goal_conceded_home = trf['secondhalf']['avg_first_goal_conceded']['home'] if 'home' in  trf['secondhalf']['avg_first_goal_conceded'] else '',
                            # secondhalf_avg_first_goal_conceded_away = trf['secondhalf']['avg_first_goal_conceded']['away'] if 'away' in  trf['secondhalf']['avg_first_goal_conceded'] else '',
                            
                            # secondhalf_avg_first_goal_scored_total = trf['secondhalf']['avg_first_goal_scored']['total'] if 'total' in  trf['secondhalf']['avg_first_goal_scored'] else '',
                            # secondhalf_avg_first_goal_scored_home = trf['secondhalf']['avg_first_goal_scored']['home'] if 'home' in  trf['secondhalf']['avg_first_goal_scored'] else '',
                            # secondhalf_avg_first_goal_scored_away = trf['secondhalf']['avg_first_goal_scored']['total'] if 'total' in  trf['secondhalf']['avg_first_goal_scored'] else '',
                            
                            secondhalf_avg_goals_per_game_conceded_total = trf['secondhalf']['avg_goals_per_game_conceded']['total'] if 'total' in  trf['secondhalf']['avg_goals_per_game_conceded'] else '',
                            secondhalf_avg_goals_per_game_conceded_home = trf['secondhalf']['avg_goals_per_game_conceded']['home'] if 'home' in  trf['secondhalf']['avg_goals_per_game_conceded'] else '',
                            secondhalf_avg_goals_per_game_conceded_away = trf['secondhalf']['avg_goals_per_game_conceded']['away'] if 'away' in  trf['secondhalf']['avg_goals_per_game_conceded'] else '',
                            
                            secondhalf_avg_goals_per_game_scored_total =  trf['secondhalf']['avg_goals_per_game_scored']['total'] if 'total' in  trf['secondhalf']['avg_goals_per_game_scored'] else '',
                            secondhalf_avg_goals_per_game_scored_home =  trf['secondhalf']['avg_goals_per_game_scored']['home'] if 'home' in  trf['secondhalf']['avg_goals_per_game_scored'] else '',
                            secondhalf_avg_goals_per_game_scored_away =  trf['secondhalf']['avg_goals_per_game_scored']['away'] if 'away' in  trf['secondhalf']['avg_goals_per_game_scored'] else '',
                            
                            secondhalf_avg_redcards_total = trf['secondhalf']['avg_redcards']['total'] if 'total' in  trf['secondhalf']['avg_redcards'] else '',
                            secondhalf_avg_redcards_home = trf['secondhalf']['avg_redcards']['home'] if 'home' in  trf['secondhalf']['avg_redcards'] else '',
                            secondhalf_avg_redcards_away = trf['secondhalf']['avg_redcards']['away'] if 'away' in  trf['secondhalf']['avg_redcards'] else '',
                            
                            secondhalf_avg_yellowcards_total = trf['secondhalf']['avg_yellowcards']['total'] if 'total' in  trf['secondhalf']['avg_yellowcards'] else '',
                            secondhalf_avg_yellowcards_home = trf['secondhalf']['avg_yellowcards']['home'] if 'home' in  trf['secondhalf']['avg_yellowcards'] else '',
                            secondhalf_avg_yellowcards_away = trf['secondhalf']['avg_yellowcards']['away'] if 'away' in  trf['secondhalf']['avg_yellowcards'] else '',

                            # secondhalf_biggest_defeat_total = trf['secondhalf']['biggest_defeat']['total'] if 'total' in  trf['secondhalf']['biggest_defeat'] else '',
                            # secondhalf_biggest_defeat_home = trf['secondhalf']['biggest_defeat']['home'] if 'home' in  trf['secondhalf']['biggest_defeat'] else '',
                            # secondhalf_biggest_defeat_away = trf['secondhalf']['biggest_defeat']['away'] if 'away' in  trf['secondhalf']['biggest_defeat'] else '',

                            # secondhalf_biggest_victory_total = trf['secondhalf']['biggest_victory']['total'] if 'total' in  trf['secondhalf']['biggest_victory'] else '',
                            # secondhalf_biggest_victory_home = trf['secondhalf']['biggest_victory']['total'] if 'total' in  trf['secondhalf']['biggest_victory'] else '',
                            # secondhalf_biggest_victory_away = trf['secondhalf']['biggest_victory']['total'] if 'total' in  trf['secondhalf']['biggest_victory'] else '',

                            secondhalf_clean_sheet_total = trf['secondhalf']['clean_sheet']['total'] if 'total' in  trf['secondhalf']['clean_sheet'] else '',
                            secondhalf_clean_sheet_home = trf['secondhalf']['clean_sheet']['home'] if 'home' in  trf['secondhalf']['clean_sheet'] else '',
                            secondhalf_clean_sheet_away = trf['secondhalf']['clean_sheet']['away'] if 'away' in  trf['secondhalf']['clean_sheet'] else '',

                            secondhalf_corners_total = trf['secondhalf']['corners']['total'] if 'total' in  trf['secondhalf']['corners'] else '',
                            secondhalf_corners_home = trf['secondhalf']['corners']['home'] if 'home' in  trf['secondhalf']['corners'] else '',
                            secondhalf_corners_away = trf['secondhalf']['corners']['away'] if 'away' in  trf['secondhalf']['corners'] else '',

                            secondhalf_draw_total =  trf['secondhalf']['draw']['total'] if 'total' in  trf['secondhalf']['draw'] else '',
                            secondhalf_draw_home =  trf['secondhalf']['draw']['home'] if 'home' in  trf['secondhalf']['draw'] else '',
                            secondhalf_draw_away =  trf['secondhalf']['draw']['away'] if 'away' in  trf['secondhalf']['draw'] else '',

                            secondhalf_failed_to_score_total = trf['secondhalf']['failed_to_score']['total'] if 'total' in  trf['secondhalf']['failed_to_score'] else '',
                            secondhalf_failed_to_score_home = trf['secondhalf']['failed_to_score']['home'] if 'home' in  trf['secondhalf']['failed_to_score'] else '',
                            secondhalf_failed_to_score_away = trf['secondhalf']['failed_to_score']['away'] if 'away' in  trf['secondhalf']['failed_to_score'] else '',

                            secondhalf_fouls_total = trf['secondhalf']['failed_to_score']['total'] if 'total' in  trf['secondhalf']['failed_to_score'] else '',
                            secondhalf_fouls_home = trf['secondhalf']['failed_to_score']['total'] if 'total' in  trf['secondhalf']['failed_to_score'] else '',
                            secondhalf_fouls_away = trf['secondhalf']['failed_to_score']['total'] if 'total' in  trf['secondhalf']['failed_to_score'] else '',

                            secondhalf_goals_against_total = trf['secondhalf']['goals_against']['total'] if 'total' in  trf['secondhalf']['goals_against'] else '',
                            secondhalf_goals_against_home = trf['secondhalf']['goals_against']['home'] if 'home' in  trf['secondhalf']['goals_against'] else '',
                            secondhalf_goals_against_away = trf['secondhalf']['goals_against']['away'] if 'away' in  trf['secondhalf']['goals_against'] else '',

                            secondhalf_goals_for_total = trf['secondhalf']['goals_for']['total'] if 'total' in  trf['secondhalf']['goals_for'] else '',
                            secondhalf_goals_for_home = trf['secondhalf']['goals_for']['home'] if 'home' in  trf['secondhalf']['goals_for'] else '',
                            secondhalf_goals_for_away = trf['secondhalf']['goals_for']['away'] if 'away' in  trf['secondhalf']['goals_for'] else '',

                            secondhalf_lost_total = trf['secondhalf']['lost']['total'] if 'total' in  trf['secondhalf']['lost'] else '',
                            secondhalf_lost_home = trf['secondhalf']['lost']['home'] if 'home' in  trf['secondhalf']['lost'] else '',
                            secondhalf_lost_away = trf['secondhalf']['lost']['away'] if 'away' in  trf['secondhalf']['lost'] else '',

                            secondhalf_offsides_total = trf['secondhalf']['offsides']['total'] if 'total' in  trf['secondhalf']['offsides'] else '',
                            secondhalf_offsides_home = trf['secondhalf']['offsides']['home'] if 'home' in  trf['secondhalf']['offsides'] else '',
                            secondhalf_offsides_away = trf['secondhalf']['offsides']['away'] if 'away' in  trf['secondhalf']['offsides'] else '',

                            secondhalf_possession_total = trf['secondhalf']['possession']['total'] if 'total' in  trf['secondhalf']['possession'] else '',
                            secondhalf_possession_home = trf['secondhalf']['possession']['home'] if 'home' in  trf['secondhalf']['possession'] else '',
                            secondhalf_possession_away = trf['secondhalf']['possession']['away'] if 'away' in  trf['secondhalf']['possession'] else '',

                            secondhalf_redcards_total = trf['secondhalf']['redcards']['total'] if 'total' in  trf['secondhalf']['redcards'] else '',
                            secondhalf_redcards_home = trf['secondhalf']['redcards']['home'] if 'home' in  trf['secondhalf']['redcards'] else '',
                            secondhalf_redcards_away = trf['secondhalf']['redcards']['away'] if 'away' in  trf['secondhalf']['redcards'] else '',

                            secondhalf_shotsOnGoal_total = trf['secondhalf']['shotsOnGoal']['total'] if 'total' in  trf['secondhalf']['shotsOnGoal'] else '',
                            secondhalf_shotsOnGoal_home = trf['secondhalf']['shotsOnGoal']['home'] if 'home' in  trf['secondhalf']['shotsOnGoal'] else '',
                            secondhalf_shotsOnGoal_away = trf['secondhalf']['shotsOnGoal']['away'] if 'away' in  trf['secondhalf']['shotsOnGoal'] else '',

                            secondhalf_shotsTotal_total = trf['secondhalf']['shotsTotal']['total'] if 'total' in  trf['secondhalf']['shotsTotal'] else '',
                            secondhalf_shotsTotal_home = trf['secondhalf']['shotsTotal']['home'] if 'home' in  trf['secondhalf']['shotsTotal'] else '',
                            secondhalf_shotsTotal_away = trf['secondhalf']['shotsTotal']['away'] if 'away' in  trf['secondhalf']['shotsTotal'] else '',

                            secondhalf_yellowcards_total = trf['secondhalf']['yellowcards']['total'] if 'total' in  trf['secondhalf']['yellowcards'] else '',
                            secondhalf_yellowcards_home = trf['secondhalf']['yellowcards']['home'] if 'home' in  trf['secondhalf']['yellowcards'] else '',
                            secondhalf_yellowcards_away = trf['secondhalf']['yellowcards']['away'] if 'away' in  trf['secondhalf']['yellowcards'] else '',

                            secondhalf_win_total = trf['secondhalf']['win']['total'] if 'total' in  trf['secondhalf']['win'] else '',
                            secondhalf_win_home = trf['secondhalf']['win']['home'] if 'home' in  trf['secondhalf']['win'] else '',
                            secondhalf_win_away = trf['secondhalf']['win']['away'] if 'away' in  trf['secondhalf']['win'] else '',

                            scoring_minutes  =  json.dumps(trf['scoring_minutes']['period']) if 'period' in trf['scoring_minutes']  else '',
                            goals_conceded_minutes  = json.dumps(trf['goals_conceded_minutes']['period']) if 'period' in trf['goals_conceded_minutes']  else '',
                            redcard_minutes  = json.dumps(trf['redcard_minutes']['period']) if 'period' in trf['redcard_minutes']  else '',
                        )
                        # ls.save()
                        

            # print("Storedetailed_stats error")
            # print(detailed_stats)
            # print("--------------------")
    except:
        logger.info('Error : Storedetailed_stats'+str(team_id))       
    return 1

def StoreTeamDetail():
    # from django.utils.timezone import datetime #important if using timezones
    # queryObj = {
    #     'formated_date__gte': datetime.today(),
    #     'league_id':1204
    # }
    # data =  MatchGoalserve.objects.all().filter(**queryObj)
    leagues = LeagueIdGolaServe()
    data =  MatchGoalserve.objects.all().filter(league_id__in=leagues)
    for dt in data:
        print("ID:-",dt.match_id)
        print('Local team:-',dt.localteam_id)
        # Local Team
        cnt =  TeamStatisticsGoalserve.objects.filter(match_id =dt.match_id, team_id=dt.localteam_id).count()
        if cnt ==0:
            team_data = teamRequests(dt.localteam_id,dt.match_id)
            # print(team_data)
            if 'id' in team_data:
                storeTeamAndStatistics(team_data)
            # storeTeamSquadPlayer(team_data['squad'],dt.localteam_id,dt.match_id)
            # if 'transfers' in team_data:
            #     transfer = team_data['transfers']
            #     StoreTransfermPlayerIN(transfer['in'],dt.localteam_id,dt.match_id)
            #     StoreTransfermPlayerOUT(transfer['out'],dt.localteam_id,dt.match_id)
            if 'sidelined' in team_data and team_data['sidelined'] :
                StoreSideline(team_data['sidelined'],dt.localteam_id,dt.match_id)
            if 'trophies' in team_data and team_data['trophies']:
                StoreTeamsTrophy(team_data['trophies'],dt.localteam_id)
            if  'detailed_stats' in team_data and team_data['detailed_stats']:
                Storedetailed_stats(team_data['detailed_stats'],dt.localteam_id)
        # Visitor Team
        cnt =  TeamStatisticsGoalserve.objects.filter(match_id =dt.match_id, team_id=dt.visitorteam_id).count()
        if cnt ==0:
            print('visiter team:-',dt.visitorteam_id)
            team_data = teamRequests(dt.visitorteam_id,dt.match_id)
            # storeTeamAndStatistics(team_data)
            # storeTeamSquadPlayer(team_data['squad'],dt.visitorteam_id,dt.match_id)
            # if 'transfers' in team_data:
            #     transfer = team_data['transfers']
            #     StoreTransfermPlayerIN(transfer['in'],dt.visitorteam_id,dt.match_id)
            #     StoreTransfermPlayerOUT(transfer['out'],dt.visitorteam_id,dt.match_id)
            if 'sidelined' in team_data and team_data['sidelined'] :
                StoreSideline(team_data['sidelined'],dt.visitorteam_id,dt.match_id)
            if 'trophies' in team_data and team_data['trophies']:
                StoreTeamsTrophy(team_data['trophies'],dt.visitorteam_id)
            if  'detailed_stats' in team_data and team_data['detailed_stats']:
                Storedetailed_stats(team_data['detailed_stats'],dt.visitorteam_id)

        # storeTeamAndStatistics(dt.visitorteam_id)
    # return 1
    # teamList = [{
    # 'match_id': 4319139,
    # 'team1_id': 6620,
    # 'team2_id': 6682
    # }]
    # teamRequests(team['team1_id'], team['match_id'])
    # team_data = teamstats(teamList)

    return team_data
def GetPopularMatch():
    leagues = LeagueIdGolaServe()
    day_list = ['d1','d2','d3','d4','d5','d6','d7']
    match_ids = []
    for league in leagues:
        url = "http://www.goalserve.com/getfeed/c05d9fc7d36540dcdfaa08d9e34f661d/standings/"+str(league)+".xml?json=1"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()
        data = data['standings']['tournament']['team']
        top5teams_id = []
        for i in range(5):
            datum = data[i]
            top5teams_id.append(int(datum['@id']))
        team_pairs = []
        for i in top5teams_id:
            for j in top5teams_id:
                if i is not j:
                    team_pairs.append({'team1': i, 'team2': j})
        ### for finding the matches             
        for i in day_list:
            url = "http://www.goalserve.com/getfeed/c05d9fc7d36540dcdfaa08d9e34f661d/soccernew/"+i+"?json=1"
            payload={}
            headers = {}
            response = requests.request("GET", url, headers=headers, data=payload)
            data1 = response.json()
            data1 = data1['scores']['category']
            for datum in data1:
                if datum['@id'] == str(league):
                    match_list = datum['matches']['match']
                    # print(match_list)
                    for team_pair in team_pairs:
                        for match in match_list:
                            try:
                                if (match['localteam']['@id'] == str(team_pair['team1'])) and (match['visitorteam']['@id'] == str(team_pair['team2'])):
                                    match_ids.append(int(match['@id']))
                            except:
                                print("error")
    return match_ids

def storeTeamAndStatistics(teamsdata):
    print(teamsdata)
    cnt =  TeamStatisticsGoalserve.objects.filter(match_id =teamsdata['match_id'], team_id=teamsdata['id']).count()
    if cnt ==0:
        dmt_app_log = 'logs/debug.log'
        logger = logging.getLogger('LibGlobalServe.py')
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logHandler = handlers.RotatingFileHandler(dmt_app_log, maxBytes=5000000, backupCount=10)
        logHandler.setLevel(logging.INFO)
        # Here we set our logHandler's formatter
        logHandler.setFormatter(formatter)
        logger.addHandler(logHandler)
        # try:
        print('Team_id:-',teamsdata['id'])
        TeamStatisticsGoalserve.objects.create(
            match_id =teamsdata['match_id'],
            team_id = teamsdata['id'],
            is_national_team = teamsdata['is_national_team'],
            name = teamsdata['name'],
            fullname = teamsdata['fullname'],
            country = teamsdata['country'],
            founded = teamsdata['founded'],
            league_rank = teamsdata['leagues']['league_rank'] if teamsdata['leagues'] != None and 'league_rank' in teamsdata['leagues']  else '',
            league_ids = json.dumps(teamsdata['leagues']['league_id']) if teamsdata['leagues'] != None and 'league_id' in teamsdata['leagues']  else '',
            
            venue_name = teamsdata['venue_name'] if 'venue_name' in teamsdata  else '',
            venue_id = teamsdata['venue_id'] if 'venue_id' in teamsdata  else 0,
            # venue_city = None if (teamsdata['venue_city'].get("cdata-section") is None) or (teamsdata['venue_city']['cdata-section'] is None) or (not teamsdata['venue_city']['cdata-section']) else teamsdata['venue_city']['cdata-section'],
            venue_city = teamsdata['venue_city']['cdata-section'] if teamsdata['venue_city'] != None else '',
            
            venue_capacity = teamsdata['venue_capacity'] if 'venue_capacity' in teamsdata  else '',
            
            venue_image = teamsdata['venue_image'] if 'venue_image' in teamsdata  else '',
            image = teamsdata['image'] if 'image' in teamsdata  else '',
            # coach_id = None if (teamsdata['coach'].get("id") is None) or (teamsdata['coach']['id'] is None) or (not teamsdata['coach']['id']) else teamsdata['coach']['id'],
            coach_id = teamsdata['coach']['id'] if teamsdata['coach']!= None else '',
            coach_name =  teamsdata['coach']['name'] if teamsdata['coach']!= None else '',

            rank_home = teamsdata['statistics']['rank']['home'] if 'rank' in teamsdata['statistics'] and 'home' in teamsdata['statistics']['rank']  else '',
            rank_total = teamsdata['statistics']['rank']['total'] if 'rank' in teamsdata['statistics'] and 'total' in teamsdata['statistics']['rank']  else '',
            rank_away = teamsdata['statistics']['rank']['away'] if 'rank' in teamsdata['statistics'] and 'away' in teamsdata['statistics']['rank']  else '',

            win_home = teamsdata['statistics']['win']['home'] if 'win' in teamsdata['statistics'] and 'home' in teamsdata['statistics']['win']  else '',
            win_total = teamsdata['statistics']['win']['total'] if 'win' in teamsdata['statistics'] and 'total' in teamsdata['statistics']['win']  else '',
            win_away = teamsdata['statistics']['win']['away'] if 'win' in teamsdata['statistics'] and 'away' in teamsdata['statistics']['win']  else '',

            draw_home = teamsdata['statistics']['draw']['home'] if 'draw' in teamsdata['statistics'] and 'home' in teamsdata['statistics']['draw']  else '',
            draw_total = teamsdata['statistics']['draw']['total'] if 'draw' in teamsdata['statistics'] and 'total' in teamsdata['statistics']['draw']  else '',
            draw_away = teamsdata['statistics']['draw']['away'] if 'draw' in teamsdata['statistics'] and 'away' in teamsdata['statistics']['draw']  else '',

            lost_home = teamsdata['statistics']['lost']['home'] if 'lost' in teamsdata['statistics'] and 'home' in teamsdata['statistics']['lost']  else '',
            lost_total = teamsdata['statistics']['lost']['total'] if 'lost' in teamsdata['statistics'] and 'total' in teamsdata['statistics']['lost']  else '',
            lost_away = teamsdata['statistics']['lost']['away'] if 'lost' in teamsdata['statistics'] and 'away' in teamsdata['statistics']['lost']  else '',

            goals_for_home = teamsdata['statistics']['goals_for']['home'] if 'goals_for' in teamsdata['statistics'] and 'home' in teamsdata['statistics']['goals_for']  else '',
            goals_for_total = teamsdata['statistics']['goals_for']['total'] if 'goals_for' in teamsdata['statistics'] and 'total' in teamsdata['statistics']['goals_for']  else '',
            goals_for_away = teamsdata['statistics']['goals_for']['away'] if 'goals_for' in teamsdata['statistics'] and 'away' in teamsdata['statistics']['goals_for']  else '',

            goals_against_home = teamsdata['statistics']['goals_against']['home'] if 'goals_against' in teamsdata['statistics'] and 'home' in teamsdata['statistics']['goals_against']  else '',
            goals_against_total = teamsdata['statistics']['goals_against']['total'] if 'goals_against' in teamsdata['statistics'] and 'total' in teamsdata['statistics']['goals_against']  else '',
            goals_against_away = teamsdata['statistics']['goals_against']['away'] if 'goals_against' in teamsdata['statistics'] and 'away' in teamsdata['statistics']['goals_against']  else '',

            clean_sheet_home = teamsdata['statistics']['clean_sheet']['home'] if 'clean_sheet' in teamsdata['statistics'] and 'home' in teamsdata['statistics']['clean_sheet']  else '',
            clean_sheet_total = teamsdata['statistics']['clean_sheet']['total'] if 'clean_sheet' in teamsdata['statistics'] and 'total' in teamsdata['statistics']['clean_sheet']  else '',
            clean_sheet_away = teamsdata['statistics']['clean_sheet']['away'] if 'clean_sheet' in teamsdata['statistics'] and 'away' in teamsdata['statistics']['clean_sheet']  else '',

            avg_goals_per_game_conceded_home = teamsdata['statistics']['avg_goals_per_game_conceded']['home'] if 'avg_goals_per_game_conceded' in teamsdata['statistics'] and 'home' in teamsdata['statistics']['avg_goals_per_game_conceded']  else '',
            avg_goals_per_game_conceded_total = teamsdata['statistics']['avg_goals_per_game_conceded']['total'] if 'avg_goals_per_game_conceded' in teamsdata['statistics'] and 'total' in teamsdata['statistics']['avg_goals_per_game_conceded']  else '',
            avg_goals_per_game_conceded_away = teamsdata['statistics']['avg_goals_per_game_conceded']['away'] if 'avg_goals_per_game_conceded' in teamsdata['statistics'] and 'away' in teamsdata['statistics']['avg_goals_per_game_conceded']  else '',

            avg_first_goal_conceded_home = teamsdata['statistics']['avg_first_goal_conceded']['home'] if 'avg_first_goal_conceded' in teamsdata['statistics'] and 'home' in teamsdata['statistics']['avg_first_goal_conceded']  else '',
            avg_first_goal_conceded_total = teamsdata['statistics']['avg_first_goal_conceded']['total'] if 'avg_first_goal_conceded' in teamsdata['statistics'] and 'total' in teamsdata['statistics']['avg_first_goal_conceded']  else '',
            avg_first_goal_conceded_away = teamsdata['statistics']['avg_first_goal_conceded']['away'] if 'avg_first_goal_conceded' in teamsdata['statistics'] and 'away' in teamsdata['statistics']['avg_first_goal_conceded']  else '',

            avg_first_goal_scored_home = teamsdata['statistics']['avg_first_goal_scored']['home'] if 'avg_first_goal_scored' in teamsdata['statistics'] and 'home' in teamsdata['statistics']['avg_first_goal_scored']  else '',
            avg_first_goal_scored_total = teamsdata['statistics']['avg_first_goal_scored']['total'] if 'avg_first_goal_scored' in teamsdata['statistics'] and 'total' in teamsdata['statistics']['avg_first_goal_scored']  else '',
            avg_first_goal_scored_away = teamsdata['statistics']['avg_first_goal_scored']['away'] if 'avg_first_goal_scored' in teamsdata['statistics'] and 'away' in teamsdata['statistics']['avg_first_goal_scored']  else '',

            avg_goals_per_game_scored_home = teamsdata['statistics']['avg_goals_per_game_scored']['home'] if 'avg_goals_per_game_scored' in teamsdata['statistics'] and 'home' in teamsdata['statistics']['avg_goals_per_game_scored']  else '',
            avg_goals_per_game_scored_total = teamsdata['statistics']['avg_goals_per_game_scored']['total'] if 'avg_goals_per_game_scored' in teamsdata['statistics'] and 'total' in teamsdata['statistics']['avg_goals_per_game_scored']  else '',
            avg_goals_per_game_scored_away = teamsdata['statistics']['avg_goals_per_game_scored']['away'] if 'avg_goals_per_game_scored' in teamsdata['statistics'] and 'away' in teamsdata['statistics']['avg_goals_per_game_scored']  else '',

            scoring_minutes = json.dumps(teamsdata['statistics']['scoring_minutes']) if 'scoring_minutes' in teamsdata['statistics']  else '',
        )
        # except:

        #     logger.info('Error : storeTeamAndStatistics'+str(teamsdata['id']))
        return 1


def GetLeague():
    leagues = LeagueIdGolaServe()
    data =  LeagueGoalserve.objects.all().filter(league_id__in=leagues)
    for dt in data:
        print("ID:-",dt.league_id)
        lg = StorePlayerByLeague(dt.league_id)
    StorePlayerStatistics()
    return 1

def StorePlayerByLeague(league_id):
    url = "https://www.goalserve.com/getfeed/c05d9fc7d36540dcdfaa08d9e34f661d/soccerleague/"+str(league_id)+"?json=1"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    data = None if data['league'] is None else data['league']
    if data is None:
        return None
    else:
        league_id = data['@id']
        league_name = data['@name']
        iscup = data['@iscup']
        country = data['@country']

        if 'team' in data:
            teamlist = data['team']
            for tm in teamlist:
                # print(tm)
                team_name = tm['@name']
                team_id= tm['@id']
                venue_name =''
                venue_id = ''
                if 'venue' in teamlist and tm['venue'] !='' :
                    venue_name = tm['venue']['@name'] if '@name' in tm['venue']  else ''
                    venue_id = tm['venue']['@id'] if '@id' in tm['venue']  else ''

                if 'squad' in tm:
                    if 'player' in tm['squad'] and type(tm['squad']['player']) is list:
                        players = tm['squad']['player']

                        for plr in players:
                            cnt =  PlayerGoalserve.objects.filter(team_id=team_id,player_id=plr['@id']).count()
                            if cnt ==0:

                                PlayerGoalserve.objects.create(
                                    league_id = league_id,
                                    league_name = league_name,
                                    iscup = iscup,
                                    country =country,
                                    team_id = team_id,   
                                    team_name = team_name,    
                                    venue_id = venue_id,   
                                    venue_name = venue_name, 
                                    age = plr['@age'] if '@age' in plr  else '' ,  
                                    appearences =  plr['@appearences'] if '@appearences' in plr  else '' ,    
                                    assists =  plr['@assists'] if '@assists' in plr  else '' ,    
                                    blocks =  plr['@blocks'] if '@blocks' in plr  else '' ,    
                                    clearances =  plr['@clearances'] if '@clearances' in plr  else '' ,    
                                    crossesAccurate =  plr['@crossesAccurate'] if '@crossesAccurate' in plr  else '' ,    
                                    crossesTotal =  plr['@crossesTotal'] if '@crossesTotal' in plr  else '' ,    
                                    dispossesed =  plr['@dispossesed'] if '@dispossesed' in plr  else '' ,    
                                    dribbleAttempts =  plr['@dribbleAttempts'] if '@dribbleAttempts' in plr  else '' ,    
                                    dribbleSucc =  plr['@dribbleSucc'] if '@dribbleSucc' in plr  else '' ,    
                                    duelsTotal =  plr['@duelsTotal'] if '@duelsTotal' in plr  else '' ,    
                                    duelsWon =  plr['@duelsWon'] if '@duelsWon' in plr  else '' ,    
                                    fouldDrawn =  plr['@fouldDrawn'] if '@fouldDrawn' in plr  else '' ,    
                                    foulsCommitted =  plr['@foulsCommitted'] if '@foulsCommitted' in plr  else '' ,    
                                    goals =  plr['@goals'] if '@goals' in plr  else '' ,    
                                    goalsConceded =  plr['@goalsConceded'] if '@goalsConceded' in plr  else '' ,    
                                    player_id =  plr['@id'] if '@id' in plr  else '' ,    
                                    injured =  plr['@injured'] if '@injured' in plr  else '' ,    
                                    insideBoxSaves =  plr['@insideBoxSaves'] if '@insideBoxSaves' in plr  else '' ,    
                                    interceptions =  plr['@interceptions'] if '@interceptions' in plr  else '' ,    
                                    isCaptain =  plr['@isCaptain'] if '@isCaptain' in plr  else '' ,    
                                    keyPasses =  plr['@keyPasses'] if '@keyPasses' in plr  else '' ,    
                                    lineups =  plr['@lineups'] if '@lineups' in plr  else '' ,    
                                    minutes =  plr['@minutes'] if '@minutes' in plr  else '' ,    
                                    name =  plr['@name'] if '@name' in plr  else '' ,    
                                    number =  plr['@number'] if '@number' in plr  else '' ,    
                                    pAccuracy =  plr['@pAccuracy'] if '@pAccuracy' in plr  else '' ,    
                                    passes =  plr['@passes'] if '@passes' in plr  else '' ,    
                                    penComm =  plr['@penComm'] if '@penComm' in plr  else '' ,    
                                    penMissed =  plr['@penMissed'] if '@penMissed' in plr  else '' ,    
                                    penSaved =  plr['@penSaved'] if '@penSaved' in plr  else '' ,    
                                    penScored =  plr['@penScored'] if '@penScored' in plr  else '' ,    
                                    penWon =  plr['@penWon'] if '@penWon' in plr  else '' ,    
                                    position =  plr['@position'] if '@position' in plr  else '' ,    
                                    rating =  plr['@rating'] if '@rating' in plr  else '' ,    
                                    redcards =  plr['@redcards'] if '@redcards' in plr  else '' ,    
                                    saves =  plr['@saves'] if '@saves' in plr  else '' ,    
                                    shotsOn =  plr['@shotsOn'] if '@shotsOn' in plr  else '' ,    
                                    shotsTotal =  plr['@shotsTotal'] if '@shotsTotal' in plr  else '' ,    
                                    substitutes_on_bench =  plr['@substitutes_on_bench'] if '@substitutes_on_bench' in plr  else '' ,    
                                    substitute_in =  plr['@substitute_in'] if '@substitute_in' in plr  else '' ,    
                                    substitute_out =  plr['@substitute_out'] if '@substitute_out' in plr  else '' ,    
                                    tackles =  plr['@tackles'] if '@tackles' in plr  else '' ,    
                                    woordworks =  plr['@woordworks'] if '@woordworks' in plr  else '' ,    
                                    yellowcards =  plr['@yellowcards'] if '@yellowcards' in plr  else '' ,    
                                    yellowred =  plr['@yellowred'] if '@yellowred' in plr  else ''    
                                ) 
    return 1

def StorePlayerStatistics():
    leagues = LeagueIdGolaServe()
    data =  PlayerGoalserve.objects.all().filter(league_id__in=leagues)
    for dt in data:
        print("Player ID:-",dt.player_id)
        plr = playerstat(dt.player_id)
        cnt =  PlayerStatisticsGoalserve.objects.filter(team_id=plr['player']['teamid'],player_id=plr['player']['id']).count()
        if cnt ==0:
            PlayerStatisticsGoalserve.objects.create(
                player_id = plr['player']['id'] if 'id' in plr['player']  else '' ,  
                category = plr['category'] if 'category' in plr  else '' ,   
                common_name = plr['player']['common_name'] if 'common_name' in plr['player']  else '' ,   
                age = plr['player']['age'] if 'age' in plr['player']  else '' ,   
                birthcountry = plr['player']['birthcountry'] if 'birthcountry' in plr['player']  else '' ,   
                birthdate = plr['player']['birthdate'] if 'birthdate' in plr['player']  else '' ,   
                birthplace = plr['player']['birthplace'] if 'birthplace' in plr['player']  else '' ,   
                firstname = plr['player']['firstname'] if 'firstname' in plr['player']  else '' ,   
                lastname = plr['player']['lastname'] if 'lastname' in plr['player']  else '' ,   
                height = plr['player']['height'] if 'height' in plr['player']  else '' ,   
                image = plr['player']['image'] if 'image' in plr['player']  else '' ,   
                name = plr['player']['name'] if 'name' in plr['player']  else '' ,   
                nationality = plr['player']['nationality'] if 'nationality' in plr['player']  else '' ,  
                position = plr['player']['position'] if 'position' in plr['player']  else '' ,  
                weight = plr['player']['weight'] if 'weight' in plr['player']  else '' ,  
                team =plr['player']['team'] if 'team' in plr['player']  else '',
                team_id=plr['player']['teamid'] if 'teamid' in plr['player']  else '',

                statistics = json.dumps(plr['player']['statistic']) if 'statistic' in plr['player']  else '' ,
                statistic_club = json.dumps(plr['player']['statistic_cups']) if 'statistic_cups' in plr['player']  else '',
                statistic_popular_intl_club = json.dumps(plr['player']['statistic_cups_intl']) if 'statistic_cups_intl' in plr['player']  else '',
                statistic_international_club = json.dumps(plr['player']['statistic_intl']) if 'statistic_intl' in plr['player']  else '',
                overall_clubs = json.dumps(plr['player']['overall_clubs']) if 'overall_clubs' in plr['player']  else '',
                
                trophies =json.dumps(plr['player']['trophies']) if 'trophies' in plr['player']  else '',
                transfers =json.dumps(plr['player']['transfers']) if 'transfers' in plr['player']  else ''
            )
    return plr
   

def TeamStatistics(team_id,match_id,name,goals):

    team_data = teamRequests(team_id,match_id)
    if type(team_data) is dict:
        if 'id' in team_data:
            storeTeamAndStatistics(team_data)
       
        if team_data['squad']:
            storeTeamSquadPlayer(team_data['squad'],team_id,match_id)
        if 'transfers' in team_data:
            transfer = team_data['transfers']
            print(transfer)
            if 'in' in transfer and type(transfer['in']) is list:
                StoreTransfermPlayerIN(transfer['in'],team_id,match_id)
            if 'out' in transfer and type(transfer['out']) is list:
                StoreTransfermPlayerOUT(transfer['out'],team_id,match_id)
        if 'sidelined' in team_data and team_data['sidelined'] :
            StoreSideline(team_data['sidelined'],team_id,match_id)
        if 'trophies' in team_data and team_data['trophies']:
            StoreTeamsTrophy(team_data['trophies'],team_id)
        if  'detailed_stats' in team_data and team_data['detailed_stats']:
            Storedetailed_stats(team_data['detailed_stats'],team_id)

def GetLiveScore():
    url = "https://www.goalserve.com/getfeed/c05d9fc7d36540dcdfaa08d9e34f661d/soccernew/home?json=1"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    data = None if data['scores']['category'] is None else data['scores']['category']
    if data is None:
        return None
    else:
        return data

        
def GetTeamImageLeagueDetail(team_id):

    url = "http://www.goalserve.com/getfeed/c05d9fc7d36540dcdfaa08d9e34f661d/soccerstats/team/"+str(team_id)+"?json=1"
    # print(url)
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    # print(response)
    try:
        data = response.json()
        data = None if data['teams'] is None else data['teams']
        if data is None:
            return None
        else:
            modified_stat_data = {
                'name': None if (data['team'].get("name") is None) or (data['team']['name'] is None) or (not data['team']['name']) else data['team']['name'],
                'fullname': None if (data['team'].get("fullname") is None) or (data['team']['fullname'] is None) or (not data['team']['fullname']) else data['team']['fullname'],
                'country': None if (data['team'].get("country") is None) or (data['team']['country'] is None) or (not data['team']['country']) else data['team']['country'],
                'founded': None if (data['team'].get("founded") is None) or (data['team']['founded'] is None) or (not data['team']['founded']) else data['team']['founded'],
                'leagues':None if (data['team'].get("leagues") is None) or (data['team']['leagues'] is None) or (not data['team']['leagues']) else {
                    'league_id': None if (data['team']['leagues'].get("league_id") is None) or (data['team']['leagues']['league_id'] is None) or (not data['team']['leagues']['league_id']) else leagues(data['team']['leagues']['league_id'])
                },
                'image': None if (data['team'].get("image") is None) or (data['team']['image'] is None) or (not data['team']['image']) else data['team']['image']
            }
            return modified_stat_data
    except:
        return None
            
def predictionSave(match_id):
    from django.utils.timezone import datetime #important if using timezones
    from datetime import datetime, timedelta
    headtohead=[]
    final_res = []
    localteam ={}
    visiterteam ={}
    leagueByTeamId =[]
    teamDetail =[]
    league_id = 0
    final_h2h ={}
    league_ids=LeagueIdGolaServe() 
    fixtures = MatchGoalserve.objects.all().filter(match_id=match_id)
    result = MatchByTeamGoalserveSerializer(fixtures, many=True).data
    # print(result[0]['localteam'])
    league_id =result[0]['league_id']   
    localteam_id =result[0]['localteam_id']
    visitorteam_id =result[0]['visitorteam_id']
    localteam_name =result[0]['localteam_name']
    visitorteam_name =result[0]['visitorteam_name']
    formated_date = str(result[0]['formated_date']) 
    match_name=result[0]['match_name']
    if league_id in league_ids:
        headtohead=head2head(int(localteam_id),int(visitorteam_id))
        prediction=GetPosionDetailFormTeamId(localteam_name,visitorteam_name)
        pred =json.loads(prediction)
        print("+++++++++prediction++++++++")
        print(pred)
        print("----++++++headtohead+++++++----")
        print(headtohead)
        qr0 = 0
        qr1 = 0
        prediction =pred[0]['Predictions']
        result = head2headPrediction(localteam_id,visitorteam_id)
        QR = prediction.split('-')
        ATQualityCR = 0.00
        HTQualityCR =0.00
        HTformpts = int(result['result']['teamFormPoints_team1'])
        ATformpts = int(result['result']['teamFormPoints_team2'])
        HST = int(result['result']['teamShotOnTarget_team1'])
        AST = int(result['result']['teamShotOnTarget_team2'])
        # if QR:
        #     if QR[0] =='N/A':
        #         qr0 = 0
        #     else:
        #         try:
        #             qr0 = int(QR[0])
        #             HTQualityCR= float(qr0 / result['result']['teamShotOnTarget_team1'])
        #         except ZeroDivisionError:
        #             HTQualityCR = 0
                
        #     if QR[1] =='N/A':
        #         qr1 = 0
        #     else:
        #         try:
        #             qr1 = int(QR[1])
        #             ATQualityCR = float(qr1 / result['result']['teamShotOnTarget_team2'])
        #         except ZeroDivisionError:
        #             ATQualityCR = 0
        print(formated_date[0:9])
        EloRating = eloratings(localteam_name,visitorteam_name,formated_date[0:10])
        HTEloRatings = EloRating['HomeTeamElo']
        ATEloRatings = EloRating['AwayTeamElo']
        HomeTeamLP =int(result['result']['teamStandings_team1'])
        AwayTeamLP =int(result['result']['teamStandings_team2'])
        # print(HTformpts,ATformpts,HomeTeamLP,AwayTeamLP,HTQualityCR,ATQualityCR)
        # predictionOdds=GetPredictionByMatch(HTformpts,ATformpts,HomeTeamLP,AwayTeamLP,HTQualityCR,ATQualityCR)
        predictionOdds=GetPredictionByMatch(HTformpts,ATformpts,HomeTeamLP,AwayTeamLP,HST,AST,HTEloRatings,ATEloRatings)
        print("pred-----------------------")
        predOdd=json.loads(predictionOdds)
        print(predOdd)

        cnt =  predictionH2HOddsGoalserve.objects.filter(match_id = match_id).count()
        if cnt == 0:
            print(cnt)
            ls=predictionH2HOddsGoalserve.objects.create(
                match_id = match_id,
                match_name=match_name,
                league_id=league_id,
                Home=pred[0]['Home'],
                Away=pred[0]['Away'],
                HST=HST,
                AST=AST,
                HTEloRatings=HTEloRatings,
                ATEloRatings=ATEloRatings,
                Predictions=pred[0]['Predictions'],
                Home_score=pred[0]['Home_score'],
                Away_score=pred[0]['Away_score'],
                Probability=pred[0]['Probability'],
                under_2_5_goals_probability=pred[0]['under_2_5_goals_probability'],
                under_2_5_odds=pred[0]['under_2_5_odds'],
                over_2_5_goals_probability=pred[0]['over_2_5_goals_probability'],
                over_2_5_odds=pred[0]['over_2_5_odds'],
                home_handicap=pred[0]['home_handicap'],
                away_handicap=pred[0]['away_handicap'],
                prediction =predOdd['prediction'],
                formated_date =formated_date,
                probability_percent_away_win=predOdd['probability_percent']['away_win'],
                probability_percent_draw=predOdd['probability_percent']['draw'],
                probability_percent_home_win=predOdd['probability_percent']['home_win'],

                predicted_decimal_odds_away_odds=predOdd['predicted_decimal_odds']['away_odds'],
                predicted_decimal_odds_draw_odds=predOdd['predicted_decimal_odds']['draw_odds'],
                predicted_decimal_odds_home_odds=predOdd['predicted_decimal_odds']['home_odds'],

                predicted_fractional_odds_away_odds=predOdd['predicted_fractional_odds']['home_odds'],
                predicted_fractional_odds_draw_odds=predOdd['predicted_fractional_odds']['home_odds'],
                predicted_fractional_odds_home_odds=predOdd['predicted_fractional_odds']['home_odds'],

                predicted_american_odds_away_odds=predOdd['predicted_american_odds']['home_odds'],
                predicted_american_odds_draw_odds=predOdd['predicted_american_odds']['home_odds'],
                predicted_american_odds_home_odds=predOdd['predicted_american_odds']['home_odds']
            )
    return (1)   
    
def getMatchTest():
    from django.utils.timezone import datetime #important if using timezones
    today = datetime.today()
    league_ids=LeagueIdGolaServe()    
    response = {}
    queryObj = {}
    one_week_ago = datetime.today() - timedelta(days=30)
    queryObj['formated_date__lte'] = today.strftime('%Y-%m-%d')
    queryObj['formated_date__gte'] = one_week_ago.strftime('%Y-%m-%d')
    queryObj['league_id__in'] =  league_ids  
    fixtures = MatchGoalserve.objects.all().filter(**queryObj)
    for mtch in fixtures:
        predictionSave(mtch.match_id)
        print(mtch.match_id)
    return 1
    

def StoreLiveScoreRedis():
    final_res = []
    data = GetLiveScore()
    if data:
        for dt in data:
            match_name = dt['@name']
            # country =dt['@name'].split(":")
            # if dt['@gid'] in league_ids:
            if 'matches' in dt:
                if 'match' in dt['matches'] and type(dt['matches']['match']) is list:
                    for match in dt['matches']['match']:
                        match_id =  match['@id']
                        # print(match['localteam'])
                        teamdata1 = GetTeamImageLeagueDetail(match['localteam']['@id'])
                        if teamdata1:
                            match['localteam']['@image'] =teamdata1['image']
                        teamdata2 = GetTeamImageLeagueDetail(match['visitorteam']['@id'])
                        if teamdata2:
                            match['visitorteam']['@image'] =teamdata2['image']
                        match['@match_name'] =match_name
                        final_res.append(match)

                if 'match' in dt['matches'] and type(dt['matches']['match']) is dict:
                    matchD = dt['matches']['match']
                    matchD['@match_name'] =match_name
                    match_id =  matchD['@id']
                    teamdata1 = GetTeamImageLeagueDetail(matchD['localteam']['@id'])
                    if teamdata1:
                        matchD['localteam']['@image'] =teamdata1['image']
                    teamdata2 = GetTeamImageLeagueDetail(matchD['visitorteam']['@id'])
                    if teamdata2:
                        matchD['visitorteam']['@image'] =teamdata2['image']
                    final_res.append(matchD)

    redis_instance.set('LiveScore', json.dumps(final_res))
    return (1)   

# def StoreHistoricData():
#     redis_instance.set('HistoricData', json.dumps(final_res))
#     return 1

def StorePredictionSaveBackdata():
    
    leagues = LeagueIdGolaServe()
    data =  MatchGoalserve.objects.all().filter(league_id__in=leagues)
    for dt in data:
       predictionSave(dt.match_id)

    return data