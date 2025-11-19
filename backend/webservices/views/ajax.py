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
# from webservices.views.CommonFunction import *
from webservices.views.bitfairapi import *
from datetime import datetime
from django.views import View
from django.views import generic
from webservices.serializers import *
from db_table.models import *
import re
from datetime import datetime, timedelta
from BetfairUpdater.SoccerCalculation import *
# from soccer.testData import *
from django.utils.text import slugify 
import random 
import string 
from soccer.scrap import *
#Probability And AI
@csrf_exempt
def GetAjaxPredictionOdds(request):
    # print(request)
    requestdata = JSONParser().parse(request)
    print(requestdata)
    # Get Team Standing Value
    qr0 = 0
    qr1 = 0
    prediction =requestdata['Predictions']

    result = head2headPrediction(requestdata['localteam_id'],requestdata['visiterteam_id'])

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
    
    EloRating = eloratings(requestdata['localteam_name'],requestdata['visiterteam_name'],requestdata['formated_date'])
    HTEloRatings = EloRating['HomeTeamElo']
    ATEloRatings = EloRating['AwayTeamElo']
    HomeTeamLP =int(result['result']['teamStandings_team1'])
    AwayTeamLP =int(result['result']['teamStandings_team2'])
    # print(HTformpts,ATformpts,HomeTeamLP,AwayTeamLP,HTQualityCR,ATQualityCR)
    predictionOdds=GetPredictionByMatch(HTformpts,ATformpts,HomeTeamLP,AwayTeamLP,HST,AST,HTEloRatings,ATEloRatings)
    # print("pred-----------------------")
   


    pred=json.loads(predictionOdds)
    
    html = ''
    # for pred in pred:
    # try:
    if pred['prediction'] == 'H':
        html+='<h3 class="card-title">'+requestdata['localteam_name']+' Team Win</h3>'
    if pred['prediction'] == 'D':
        html+='<h3 class="card-title">'+requestdata['localteam_name']+'VS'+requestdata['visiterteam_name']+' Match Draw</h3>'
    if pred['prediction'] == 'A':
        html+='<h3 class="card-title">'+requestdata['visiterteam_name']+' Team Win</h3>'
    html+='<div class="row"><div class="col-6 col-sm-6 col-lg-6"><div class="card"><h6 class="card-title">Probability%</h6><div class="card-body text-center"><div class="h5 m-0 font-weight-bold">Home Odds<span class="badge text-green">'
    html+=str(pred['probability_percent']['home_win'])+'</span></div>'
    html+='<div class="h5 m-0 font-weight-bold">Draw Odds <span class="badge text-green">'
    html+=str(pred['probability_percent']['draw'])+'</span></div>'
    html+='<div class="h5 m-0 font-weight-bold">Away Odds <span class="badge text-green">'+str(pred['probability_percent']['away_win'])+'</span>'
    html+='</div></div></div></div>'
    html+='<div class="col-6 col-sm-6 col-lg-6"><div class="card">'
    html+='<h6 class="card-title">Decimal Odds</h6>'
    html+='<div class="card-body text-center">'
    html+='<div class="h5 m-0 font-weight-bold">'
    html+='Home Odds <span class="badge text-green">'+str(pred['predicted_decimal_odds']['home_odds'])+'</span>'
    html+='</div>'
    html+='<div class="h5 m-0 font-weight-bold">'
    html+='Draw Odds<span class="badge text-green">'+str(pred['predicted_decimal_odds']['draw_odds'])+'</span>'
    html+='</div>'
    html+='<div class="h5 m-0 font-weight-bold">'
    html+='Away Odds <span class="badge text-green">'+str(pred['predicted_decimal_odds']['away_odds'])+'</span>'
    html+='</div></div></div></div>'
    html+='<div class="col-6 col-sm-6 col-lg-6">'
    html+='<div class="card">'
    html+='<h6 class="card-title">Fractional Odds</h6>'
    html+='<div class="card-body text-center">'
    html+='<div class="h5 m-0 font-weight-bold">'
    html+='Home Odds <span class="badge text-green">'+str(pred['predicted_fractional_odds']['home_odds'])+'</span>'
    html+='</div>'
    html+='<div class="h5 m-0 font-weight-bold">'
    html+='Draw <span class="badge text-green">'+str(pred['predicted_fractional_odds']['draw_odds'])+'</span>'
    html+='</div>'
    html+='<div class="h5 m-0 font-weight-bold">'
    html+='Away Odds <span class="badge text-green">'+str(pred['predicted_fractional_odds']['away_odds'])+'</span>'
    html+='</div></div></div></div>'
    html+='<div class="col-6 col-sm-6 col-lg-6">'
    html+='<div class="card">'
    html+='<h6 class="card-title">American Odds</h6>'
    html+='<div class="card-body text-center">'
    html+='<div class="h5 m-0 font-weight-bold">'
    html+='Home Odds <span class="badge text-green">'+str(pred['predicted_american_odds']['home_odds'])+'</span>'
    html+='</div>'
    html+='<div class="h5 m-0 font-weight-bold">'
    html+='Draw Odds<span class="badge text-green">'+str(pred['predicted_american_odds']['draw_odds'])+'</span>'
    html+='</div>'
    html+='<div class="h5 m-0 font-weight-bold">'
    html+='Away Odds <span class="badge text-green">'+str(pred['predicted_american_odds']['away_odds'])+'</span>'
    html+='</div></div></div></div></div>'
    # except:
    #     html='<div class="alert alert-danger" role="alert"><button type="button" class="btn-close" data-bs-dismiss="alert" aria-hidden="true">×</button>Prediction Odds Result Not Found !</div>'
    
    data = {'status':200, 'message': 'success', "html": html}
    return JsonResponse(data)
@csrf_exempt
def getSeasonByLeague(request):
    requestdata = JSONParser().parse(request)
    season_detail =  AllSeason.objects.all().filter(league_id=requestdata['league_id'])
    select =''
    if season_detail:
        for ssn in season_detail:
            # print(ssn.season_id)
            select += '<option value="'+str(ssn.season_id)+'">'+ssn.name+'</option>'
    data = {'status':200, 'message': 'success', "html": select}
    return JsonResponse(data)
@csrf_exempt
def saveTeamByseasonSportsmonk(request):
    requestdata = JSONParser().parse(request)
    # print(requestdata['season_id'])
    SaveTeamBySeason(requestdata['season_id'])
    data = {'status':200, 'message': 'success', "html": ''}
    return JsonResponse(data)

@csrf_exempt
def GetAjaxViewMatchByDate(request):
    requestdata = JSONParser().parse(request)
    # print(requestdata)
    import datetime
    from django.utils.timezone import datetime #important if using timezones
    today = datetime.today()
    final_res = []
    league_ids=LeagueIdGolaServe()
    queryObj = {}    
    date1 =''
    date2 =''
    league_id =''
    end_limit = int(requestdata['end_limit'])
    start_limit = int(requestdata['start_limit'])
    if requestdata:
        
        response = {}
        # query OBJ     
        if 'todate' in requestdata and requestdata['todate'] !='':
            date1 = requestdata['todate']
            queryObj['formated_date__gte'] = requestdata['todate']

        if 'fromdate' in requestdata and requestdata['fromdate'] !='':
            date2 = requestdata['fromdate']
            queryObj['formated_date__lte'] = requestdata['fromdate']

        if 'today' in requestdata and requestdata['today'] !='':
            queryObj['formated_date__contains'] = datetime.today().strftime('%Y-%m-%d')

        if 'League' in requestdata and requestdata['League'] !='':
                queryObj['league_id'] =  requestdata['League']
                queryObj['formated_date__gte'] = today.strftime('%Y-%m-%d')
                queryObj['formated_date__lte'] = one_week_ago.strftime('%Y-%m-%d')
    
    if len(queryObj) == 0:
        one_week_ago = datetime.today() + timedelta(days=7)
        queryObj['formated_date__gte'] = today.strftime('%Y-%m-%d')
        queryObj['formated_date__lte'] = one_week_ago.strftime('%Y-%m-%d')
        queryObj['league_id__in'] =  league_ids
    print(queryObj)
    fixtures = MatchGoalserve.objects.all().filter(**queryObj)[start_limit:end_limit]
    result = MatchByTeamGoalserveSerializerOptional(fixtures, many=True).data   

    for index, item in enumerate(result):
        print(item)
        final_res.append({
            "match_id":item['match_id'],
            "localteam_name":item['localteam_name'],
            "localteam_logo_path":item['localteam']['image'],
            "visiterteam_name":item['visitorteam_name'],
            "visiterteam_logo_path":item['visitorteam']['image'],
            "time_date":str(item['string_date'])+' : '+str(item['time_status']),
            "venue":item['venue']
        })
    # print(final_res)
    data = {'status':200, 'message': 'success', "htmldata": final_res,'start_limit':end_limit,'end_limit':end_limit+15}
    return JsonResponse(data)

@csrf_exempt
def GetAjaxLeagueList(request):
    final_res = []
    requestdata = JSONParser().parse(request)
    end_limit = int(requestdata['end_limit'])
    start_limit = int(requestdata['start_limit'])
    league_search =requestdata['league_search']
    league = Leagues.objects.all().filter()[start_limit:end_limit]
    if league_search:
        # print(season_search)
        league = Leagues.objects.all().filter(name__contains='league_search')[start_limit:end_limit]
    league_detail = AllLeagueSerializer(league, many=True).data
    for index, item in enumerate(league_detail):
        final_res.append({
            "league_id":item['league_id'],
            "name":item['name'],
            "logo_path":item['logo_path'],
            "type":item['type'],
            "country_name":item['country']['country_name'],
        })

    # print(league_detail)
    data = {'status':200, 'message': 'success', "htmldata": final_res,'start_limit':end_limit,'end_limit':end_limit+15,'league_search':league_search}
    return JsonResponse(data)

@csrf_exempt
def GetAjaxTeamList(request):
    final_res = []
    requestdata = JSONParser().parse(request)
    end_limit = int(requestdata['end_limit'])
    start_limit = int(requestdata['start_limit'])
    season_search =requestdata['league_search']
    if season_search:
        # print(season_search)
        team = Teams.objects.all().filter(season_id=season_search)[start_limit:end_limit]
    else:
        team = Teams.objects.all().filter()[start_limit:end_limit]
    
    if team:
        result = TeamCountrySeasonSerializer(team, many=True).data
    
    for index, item in enumerate(result):
        country_name = ''
        season_name =''
        country = Countries.objects.all().filter(country_id=item["country_id"]).first()
        if country:
            country_name=country.name

        season = AllSeason.objects.all().filter(season_id=item["current_season_id"]).first()
        if season:
            season_name=season.name
        final_res.append({
            "team_id":item['team_id'],
            "name":item['name'],
            "logo_path":item['logo_path'],
            "country":country_name,
            "season":season_name,
            "season_id":item['season_id'],
        })
    # print(league_detail)
    data = {'status':200, 'message': 'success', "htmldata": final_res,'start_limit':end_limit,'end_limit':end_limit+15,'season_search':season_search}
    return JsonResponse(data)

@csrf_exempt
def getAjaxTeamByLeague(request):
    requestdata = JSONParser().parse(request)
    season_detail =  TeamStatisticsGoalserve.objects.all().filter(league_ids__contains=requestdata['league_id'])
    select =''
    if season_detail:
        for ssn in season_detail:
            # print(ssn.season_id)
            select += '<option value="'+str(ssn.team_id)+'">'+ssn.name+'</option>'
    data = {'status':200, 'message': 'success', "html": select}
    return JsonResponse(data)
