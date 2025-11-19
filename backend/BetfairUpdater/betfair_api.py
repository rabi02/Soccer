from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from webservices.views.BitfairLib import *
# from webservices.views.LibGoalServeAPI import *
# from webservices.views.bitfairapi import *
from BetfairApi.BetfairExchangeAPI import *
from SportsRadar.SportsradarApi import *
from db_table.models import *
from soccer.scrap import *
import json
from webservices.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.text import slugify 
import random 
import string 
# from soccer.testData import *
 
def testapi():
    print("i am here")

def fixturesupdate_api(request):
    endpoint = "https://soccer.sportmonks.com/api/v2.0/fixtures/updates"
    url = endpoint + "?api_token=" + football_token
    response = requests.get(url)
    res = json.dumps(json.loads(response.text), indent=3)
    return res

@csrf_exempt
def SaveAllData(request=''):
    response = fixturesupdate_api(request)
    # league_id_list = []
    # season_id_list = []
    # team_id_list = []
    # countries_id_list = []
    # player_id_list = []
    fixture_data_save = fixtureupdate_save(response)
    # fixtures = MatchFixtureUpdate.objects.all()
    # for obj in fixtures:
    #     league_id_list.append(obj.league_id)
    #     season_id_list.append(obj.season_id)
    #     team_id_list.append(obj.localteam_id)
    #     team_id_list.append(obj.visitorteam_id)
    # # league response save:
    # for id in league_id_list:
    #     league_res = get_leagues(request, id=id)
    #     # league_data_save = leagues_save(league_res)
    #
    # # season response save:
    # season_id_list = list(set(season_id_list))
    # for id in season_id_list:
    #     season_res = get_standingseasonlist(request, season_id=id)
    #     # season_data_save = season_save(season_res)
    # # team response save:
    # team_id_list = list(set(team_id_list))
    # for id in team_id_list:
    #     team_res = get_teams(request, id=id)
    #     # team_data_save = team_save(team_res)

    # countries_res = get_countries(request)
    # countries_data_save =  countries_save(countries_res)
    # countries = Countries.objects.all()
    # for obj in countries:
    #     countries_id_list.append(obj.country_id)
    # # player response save by country_id:
    # for id in countries_id_list:
    #     player_res = get_player(request, country_id=id)
    #     # player_data_save = player_save(player_res)
    # player =  Players.objects.all()
    # for obj in player:
    #     player_id_list.append(obj.team_id)
    # #  team response save by player team_id:
    # player_id_list = list(set(player_id_list))
    # for id in player_id_list:
    #     team_res = get_teams(request, id=id)
    #     team_data_save = team_save(team_res)


    data = {"status": 200, "message": "All data saved success", "data": {}}
    return JsonResponse(data)

@csrf_exempt
def SavePlayerSatistics(request=''):
    player_id_list = []
    player = Players.objects.all()
    for obj in player:
        print(obj.player_id)
        league_res = get_player_stats(request, player_id=obj.player_id,parent_player_id=obj.id)
    data = {"status": 200, "message": "All PlayerSatistics data saved success", "data": {}}
    return JsonResponse(data)

@csrf_exempt
def Saveodds(request=''):
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
def RemoveDuplicatePlayer(request=''):
    rows = Players.objects.all()
    for row in rows:
        try:
            Players.objects.get(player_id=row.player_id)
        except:
            row.delete()

def SaveAllLeaguesData(request=''):
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
def SaveAllTeamsData(request=''):
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
def SaveAllTeamsbyPlayerData(request=''):
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
def SaveAllSeasonData(request=''):
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
def SaveAllPlayerData(request=''):
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
def SaveAllFixtureData(request=''):
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
def SaveAllTeamStatitics(request =''):
    from db_table.models import Teams
    # team = Teams.objects.all()
    # for obj in team:
    #     team_stats = get_team_stats(request, team_id=obj.team_id)
    # data = {"status": 200, "message": "All PlayerSatistics data saved success"}
    team = Teams.objects.all().filter(collection_datasource="www.worldfootball.net")
    for obj in team:
        if obj.logo_path =='':
            print(obj.id)
            logo_path = getTeamImage(obj.name)
            print(logo_path)
            Teams.objects.filter(id=obj.id).update(logo_path=logo_path)
    data = {"status": 200, "message": "All PlayerSatistics data saved success"}
    return JsonResponse(data)

@csrf_exempt
def StorePlayerListOtherDataSource(request =''):
    from db_table.models import PlayerList
    data = storePlayerList()
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
        cnt = PlayerList.objects.all().filter(player_id=request_data["player_id"],collection_datasource=request_data["collection_datasource"]).count()
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
def StorePlayerCareerOtherDataSource(request =''):
    from db_table.models import PlayerCareer
    data = storePlayerCareer()
    for result in data:
        request_data = {
            'id' :result[0] if result[0]  else 0,
            'player_id' :result[1] if result[1]  else 0,
            'flag' :result[2] if result[2]  else '',
            'season_id' :result[3] if result[3]  else 0,
            'team_id' :result[4] if result[4]  else '',
            'matches' :result[5] if result[5]  else 0,
            'goals' :result[6] if result[6]  else 0,
            'started' :result[7] if result[7]  else 0,
            's_in' :result[8] if result[8]  else 0,
            's_out' :result[9] if result[9]  else 0,
            'yellow' :result[10] if result[10]  else 0,
            's_yellow' :result[11] if result[11]  else 0,
            'red' :result[12] if result[12]  else 0,
            'collection_datasource':'www.worldfootball.net'
        }
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
def StoreMatchTeamPlayerInfoOtherDataSource(request = ''):
    from db_table.models import MatchTeamPlayerInfo
    myresult = storeMatchTeamPlayerInfo()
    for result in myresult:
        request_data = {
            'id' :result[0] if result[0]  else 0,
            'match_id' :result[1] if result[1]  else 0,
            'team_id' :result[2] if result[2]  else 0,
            'player_id' :result[3] if result[3]  else '',
            'goals' :result[4] if result[4]  else 0,
            'assists' :result[5] if result[5]  else 0,
            'collection_datasource':'www.worldfootball.net'
        }
    
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
def RunScraping():
    from db_table.models import ScrapTool
    scrap_list = ScrapTool.objects.all()
    for obj in scrap_list:
        scrap_url = obj.scrap_url
        scrap_element_class = obj.scrap_element_class
        scrap_type =obj.scrap_type
        arr=[]
        if 'exemptColumn' in obj:
            exemptColumn = obj.exemptColumn
            if exemptColumn:
                arr=exemptColumn.split(',')
       
        data = ScrapData(scrap_url,scrap_element_class,arr,scrap_type)
        if data:
            ScrapTool.objects.filter(slug=slug).update(scrap_return_reult=json.dumps(data))
        
    data ={"status": 200, "message": "success", "data":''}
    return JsonResponse(data)

@csrf_exempt
def StoreOddsByTeam():
    from db_table.models import SeasonMatchPlan
    scrap_list = SeasonMatchPlan.objects.all()
    for obj in scrap_list:
       
        home_team_result = SeasonLeagueTeamInfo.objects.filter(team_id = obj.home_team_id).values('team_id').order_by('team_id').annotate(total_match=Sum('t_mp')).annotate(total_win=Sum('t_w')).annotate(total_loss=Sum('t_l')).annotate(total_drow=Sum('t_d'))
        away_team_result = SeasonLeagueTeamInfo.objects.filter(team_id = obj.away_team_id).values('team_id').order_by('team_id').annotate(total_match=Sum('t_mp')).annotate(total_win=Sum('t_w')).annotate(total_loss=Sum('t_l')).annotate(total_drow=Sum('t_d'))
        total_match = home_team_result[0]['total_match'] + away_team_result[0]['total_match']
        HomePrice = (home_team_result[0]['total_win'] + away_team_result[0]['total_loss']) * 100 / total_match
        DrawPrice = (home_team_result[0]['total_drow'] + away_team_result[0]['total_drow']) * 100 / total_match
        AwayPrice = (home_team_result[0]['total_loss'] + away_team_result[0]['total_win'])* 100 / total_match   
        home = 100 / HomePrice
        draw = 100 / DrawPrice
        away = 100 / AwayPrice
        cnt = OddCalculation.objects.filter(match_id=obj.match_id).count()
        if cnt == 0:
            data =OddCalculation(match_id=obj.match_id,Home=round(home - 0.005, 2),Draw=round(draw - 0.005, 2),Away= round(away - 0.005, 2),collection_datasource='www.worldfootball.net')
            data.save()
    data ={"status": 200, "message": "success", "data":''}
    return JsonResponse(data)

@csrf_exempt
def GetLeaguewiseTeamDetail(request):
    leaguelist = Leagues.objects.all().filter(active=True,collection_datasource="www.worldfootball.net")
    for lg in leaguelist:
        print(lg.name)
    data ={"status": 200, "message": "success", "data":''}
    return JsonResponse(data)

def ScrapFromSoccerstats():
    from db_table.models import Leagues
    league_list = Leagues.objects.filter(collection_datasource="www.soccerstats.com").all()
    # for row in league_list:
    #     Leagues.objects.filter(id=row.id).update(league_id=row.id)
    # SaveLeagueSoccerstats()
    league_list = Leagues.objects.filter(collection_datasource="www.soccerstats.com").all()
    i =0
    for resp in league_list:
        
        scrap_url = 'https://www.soccerstats.com/homeaway.asp?league='+resp.slug_name
        scrap_element_class = 'h2h-team1'
        scrap_type ='html'
        scrap_element_type = 'id'
        arr=[]
        exemptColumn = 1
        myrec =[]
        # arr=exemptColumn.split(',')
        print(scrap_url)
        data = ScrapDatasoccerstats(scrap_url,scrap_element_class,arr,scrap_type,scrap_element_type)
        insertHomeAway(data,'home',resp.league_id)
        scrap_element_class = 'h2h-team2'
        data = ScrapDatasoccerstats(scrap_url,scrap_element_class,arr,scrap_type,scrap_element_type)
        insertHomeAway(data,'away',resp.league_id)

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
            cnt = HomeAwayTeamByLeague.objects.filter(league_id=league_id,team_type=team_type,team_name=team_name,collection_datasource='www.soccerstats.com').count()
            if cnt == 0:
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
def UpdateHomeAwaySoccerstats():
    # Update Team and Slug
    from db_table.models import HomeAwayTeamByLeague
    hatl_list = HomeAwayTeamByLeague.objects.filter(collection_datasource="www.soccerstats.com").all()
    for row in hatl_list:
        slug= unique_slug_generator(row.team_name)
        # print(slug)
        HomeAwayTeamByLeague.objects.filter(id=row.id).update(team_id=row.id,team_slug = slug)
    data ={"status": 200, "message": "success"}
    return JsonResponse(data)

#Collect Data from Betfair

def storeEvent():
    res=ListEventBetfair()
    return JsonResponse(res)

def storeDailySummeryDetail():
    res=GetDailySummery()
    res1 =PreparePredictionAndOtherData()
    res2 =StorePredictionDataSportsradarToBetfairExchange()
    return JsonResponse(res)

def StoreSportsRadar():
    try:
        res=StoreCompetitions()
        res=CompetitionSeasons()
        res=CompetitionSeasonsCompetitiors()
        res=CompetitionSeasonsSchedulesCompetitiors()
        res=CompitatioLeagueSeasonCompetitorsProfilSportsradar()
        return True
    except:
        return False
# ---------------SportsMonk---------------------
def UpdateTeamSeasonLeagueStatisticsSportsMonk():
    fixtures = MatchFixtureUpdate.objects.all()
    for resp in fixtures:
        get_teams(request='', id=resp["localteam_id"])
        get_teams(request='', id=resp["visitorteam_id"])
        get_seasonlist(request='', season_id=resp["season_id"])
        get_team_stats(request='', team_id=resp["localteam_id"])
        get_team_stats(request='', team_id=resp["visitorteam_id"])
    data = {"status": 200, "message": "All fixture data saved success", "data": {}}
    return JsonResponse(data)

def UpdateFixtureByDate():
    fixture_by_dateSeries(request='', start_date='2022-01-22', end_date='2022-02-25')
    return 1

def UpdateBetfairOrder():
    try:
        UpdatePlcaeOrderBetfair()
        return 1
    except:
        return False

def SaveTeamBySeasonSportsMonk():
    season_detail =  AllSeason.objects.all().filter(collection_datasource="www.sportmonks.com")
    if season_detail:
        for ssn in season_detail:
            SaveTeamBySeason(ssn.season_id)
    return 1

def MatchTeamStatGOALSERVE():
    StoreMatch()
    team_data = StoreTeamDetail()
    # StoreSeason()
    # GetLeague()
    pdata= StorePlayerStatistics()
    data = {'status':200, 'message': 'success', "data": ''}
    return JsonResponse(data)
    
def LiveScoreRedis():
    team_data = StoreLiveScoreRedis()
    data = {'status':200, 'message': 'success', "data": ''}
    return JsonResponse(data)

def storeSofascoreLiveScoreDetail():
    res=StoreDailySummerySofaScore()
    # res1 =PreparePredictionAndOtherData()
    # res2 =StorePredictionDataSportsradarToBetfairExchange()
    return JsonResponse(res)