from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from webservices.views.BitfairLib import *
from webservices.views.bitfairapi import *
from db_table.models import *
import json
from webservices.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
# from soccer.testData import *
def fixturesupdate_api(request):
    endpoint = "https://soccer.sportmonks.com/api/v2.0/fixtures/updates"
    url = endpoint + "?api_token=" + football_token
    response = requests.get(url)
    res = json.dumps(json.loads(response.text), indent=3)
    return res


@csrf_exempt
def SaveAllData(request):
    result = MatchFixtureUpdate.objects.all().filter()
    for resp in result:
        get_teams(request, id=resp.localteam_id)
        get_teams(request, id=resp.visitorteam_id)
        get_seasonlist(request, id=resp.season_id)
        get_team_stats(request='', team_id=resp.localteam_id)
        get_team_stats(request='', team_id=resp.visitorteam_id)
    data = {"status": 200, "message": "All data saved success", "data": {}}
    return JsonResponse(data)

@csrf_exempt
def SavePlayerSatistics(request):
    player_id_list = []
    player = Players.objects.all()
    for obj in player:
        print(obj.player_id)
        league_res = get_player_stats(request, player_id=obj.player_id,parent_player_id=obj.id)
    data = {"status": 200, "message": "All PlayerSatistics data saved success", "data": {}}
    return JsonResponse(data)

@csrf_exempt
def Saveodds(request):
    fixture_id_list = []
    fixtures = MatchFixtureUpdate.objects.all()
    for obj in fixtures:
        fixture_id_list.append(obj.matchid)
    # PlayerSatistics response save:
    fixture_id_list = list(set(fixture_id_list))
    for id in fixture_id_list:
        odds_res = get_oddsbyfixtureidList(request, fixture_id=id)
        # odds_data_save = odds_save(odds_res)

    data = {"status": 200, "message": "All odds data saved success", "data": {}}
    return JsonResponse(data)

@csrf_exempt
def RemoveDuplicatePlayer(request):
    for row in AllSeason.objects.all().filter(collection_datasource='www.soccerstats.com').reverse():
        if AllSeason.objects.filter(season_id = row.season_id).count() > 1:
            print(row.season_id)
            row.delete()

def SaveAllLeaguesData(request):
    league_id_list = []
    fixtures = MatchFixtureUpdate.objects.all()
    for obj in fixtures:
        league_id_list.append(obj.league_id)
    # leagues response save:
    league_id_list = list(set(league_id_list))
    for id in league_id_list:
        league_res = get_leagues(request, id=id)
        # league_data_save = leagues_save(league_res)

    data = {"status": 200, "message": "All league data saved success", "data": {}}
    return JsonResponse(data)

@csrf_exempt
def SaveAllTeamsData(request):
    team_id_list = []
    fixtures = MatchFixtureUpdate.objects.all()
    for obj in fixtures:
        team_id_list.append(obj.localteam_id)
        team_id_list.append(obj.visitorteam_id)
    # leagues response save:
    team_id_list = list(set(team_id_list))
    for id in team_id_list:
        team_res = get_teams(request, id=id)
        # team_data_save = team_save(team_res)

    data = {"status": 200, "message": "All team data saved success", "data": {}}
    return JsonResponse(data)

@csrf_exempt
def SaveAllTeamsbyPlayerData(request):
    countries_id_list = []
    countries = Countries.objects.all()
    for obj in countries:
        countries_id_list.append(obj.country_id)
    # teams response save:
    countries_id_list = list(set(countries_id_list))
    for id in countries_id_list:
        team_res = get_teams(request, country_id=id)
        # team_data_save = team_save(team_res)

    data = {"status": 200, "message": "All team data saved success", "data": {}}
    return JsonResponse(data)


@csrf_exempt
def SaveAllSeasonData(request):
    season_id_list = []
    fixtures = MatchFixtureUpdate.objects.all()
    for obj in fixtures:
        season_id_list.append(obj.season_id)
    # season response save:
    season_id_list = list(set(season_id_list))
    for id in season_id_list:
        season_res = get_standingseasonlist(request, season_id=id)
        # season_data_save = season_save(season_res)

    data = {"status": 200, "message": "All season data saved success", "data": {}}
    return JsonResponse(data)

@csrf_exempt
def SaveAllPlayerData(request):
    countries_id_list = []
    countries = Countries.objects.all()
    for obj in countries:
        countries_id_list.append(obj.country_id)
    # player response save by country_id:
    countries_id_list = list(set(countries_id_list))
    for id in countries_id_list:
        player_res = get_player(request, country_id=id)
        # player_data_save = player_save(player_res)

    data = {"status": 200, "message": "All player data saved success", "data": {}}
    return JsonResponse(data)

@csrf_exempt
def SaveAllFixtureData(request):
    response = fixturesupdate_api(request)
    fixture_data_save = fixtureupdate_save(response)
    fixture_id_list = []
    fixtures = MatchFixtureUpdate.objects.all()
    for obj in fixtures:
        fixture_id_list.append(obj.matchid)
    # fixture response save:
    fixture_id_list = list(set(fixture_id_list))
    for id in fixture_id_list:
        fixture_res = get_match_fixture(request, fixture_id=id)
        # league_data_save = leagues_save(fixture_res)

    data = {"status": 200, "message": "All fixture data saved success", "data": {}}
    return JsonResponse(data)

@csrf_exempt
def SaveAllTeamStatitics(request):
    from db_table.models import Teams
    record = Teams.objects.all().filter(logo_path="",collection_datasource="www.worldfootball.net")
    for obj in record:
        # print(obj.name)
        # print(obj.logo_path)
        # if obj.logo_path == None:
        print(obj.name)
        print(obj.id)
        logo_path = getTeamImage(obj.name)
        print(logo_path)
        Teams.objects.filter(id=obj.id).update(logo_path=logo_path)
    data = {"status": 200, "message": "All PlayerSatistics data saved success"}
    return JsonResponse(data)