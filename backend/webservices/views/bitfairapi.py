from django.utils.dateparse import parse_date
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
import json, base64, ast
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
from datetime import datetime, timedelta
from mimetypes import MimeTypes
import urllib
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
import re
import os
from django.apps import apps
from django.views import View
import requests
import json
from db_table.models import *
from webservices.views.constants import *
from webservices.views.BitfairLib import *
import redis
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import datetime


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
            flag = resp["extra"]["flag"]
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


def str_to_date(str_date):
    match = re.search("\d{2}/\d{2}/\d{4}", str_date)
    obj_date = datetime.datetime.strptime(match.group(), "%d/%m/%Y").date()
    return obj_date

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
                            overall=nnresp["overall"],
                            home=nnresp["home"],
                            away=nnresp["away"],
                            total=nnresp["total"],
                            total_goals_difference = ans["total"]["goal_difference"],
                            total_points = ans["total"]["total_points"],

                            overall_games_played = ans["overall"]['games_played'],
                            overall_won = ans["overall"]['won'],
                            overall_draw = ans["overall"]['draw'],
                            overall_lost = ans["overall"]['lost'],
                            overall_goals_scored = ans["overall"]['goals_scored'],
                            overall_goals_against = ans["overall"]['goals_against'],
                            overall_points = ans["overall"]['points'],

                            home_games_played = ans["home"]['games_played'],
                            home_won = ans["home"]['won'],
                            home_draw = ans["home"]['draw'],
                            home_lost = ans["home"]['lost'],
                            home_goals_scored = ans["home"]['goals_scored'],
                            home_goals_against = ans["home"]['goals_against'],
                            home_points = ans["home"]['points'],

                            away_games_played = ans["away"]['games_played'],
                            away_won = ans["away"]['won'],
                            away_draw = ans["away"]['draw'],
                            away_lost = ans["away"]['lost'],
                            away_goals_scored = ans["away"]['games_played'],
                            away_goals_against = ans["away"]['games_played'],
                            away_points = ans["away"]['games_played'],
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
                        overall=chrrsp["overall"],
                        home=chrrsp["home"],
                        away=chrrsp["away"],
                        total=chrrsp["total"],
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
        get_teams(request, id=resp["localteam_id"])
        get_teams(request, id=resp["visitorteam_id"])
        get_seasonlist(request, season_id=resp["season_id"])
        get_team_stats(request='', team_id=resp["localteam_id"])
        get_team_stats(request='', team_id=resp["visitorteam_id"])
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
                weather_report=resp["weather_report"],
                commentaries=resp["commentaries"],
                attendance=resp["attendance"],
                pitch=resp["pitch"],
                details=resp["details"],
                neutral_venue=resp["neutral_venue"],
                winning_odds_calculated=resp["winning_odds_calculated"],
                formations=resp["formations"],
                scores=resp["scores"],
                time=resp["time"],
                coaches=resp["coaches"],
                standings=resp["standings"],
                assistants=resp["assistants"],
                leg=resp["leg"],
                colors=resp["colors"],
                deleted=resp["deleted"],
                is_placeholder=resp["is_placeholder"],
                time_date=resp["time"]["starting_at"]["date"]
            )
        else:
            data = MatchFixtureUpdate.objects.get(matchid=resp["id"])
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
            data.weather_report = resp["weather_report"]
            data.commentaries = resp["commentaries"]
            data.attendance = resp["attendance"]
            data.pitch = resp["pitch"]
            data.details = resp["details"]
            data.neutral_venue = resp["neutral_venue"]
            data.winning_odds_calculated = resp["winning_odds_calculated"]
            data.formations = resp["formations"]
            data.scores = resp["scores"]
            data.time = resp["time"]
            data.coaches = resp["coaches"]
            data.standings = resp["standings"]
            data.assistants = resp["assistants"]
            data.leg = resp["leg"]
            data.colors = resp["colors"]
            data.deleted = resp["deleted"]
            data.is_placeholder = resp["is_placeholder"]
            data.time_date = resp["time"]["starting_at"]["date"]
            data.save()
    return res

