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
import json
import time
#################### competitions ##################################
def StoreCompetitions():
	import datetime
	from datetime import datetime
	from datetime import date
	from datetime import datetime
	import json
	logError='API Name:StoreCompetitions,Date:'+datetime.today().strftime('%Y-%m-%d %H:%M:%S')
	json_string = str(logError)
	with open('log.txt', 'a', encoding='utf-8') as file:
		file.write(json_string + '\n')
	file.close()
	url = SPORTRADER_API_URL+"/en/competitions.json?api_key="+SPORTRADER_API_KEY
	payload={}
	headers = {}
	ligue_list =['sr:competition:17','sr:competition:23','sr:competition:35','sr:competition:34','sr:competition:8']
	response = requests.request("GET", url, headers=headers, data=payload)
	data = response.json()
	new_data = data["competitions"]
	if 'competitions' in data:
		modified_data=[]
		for info in new_data:

			cnt =  LeagueSportsradar.objects.filter(id=info["id"]).count()
			if cnt == 0:
				print('create',info["id"])
				Ins = LeagueSportsradar.objects.create(
					id = info["id"] if "id" in info else None,
					competition_id = info["id"] if "id" in info else None,
					name = info["name"] if "name" in info else None,
					gender = info["gender"] if "gender" in info else None,
					parent_id = info["parent_id"] if "parent_id" in info else None,
					category_id = info["category"]["id"] if "id" in info["category"] else None,
					category_name = info["category"]["name"] if "id" in info["category"] else None,
					country_code = info["category"]["country_code"] if "country_code" in info["category"] else None,
					is_active= True if info["id"] in ligue_list else False,
				)
			else:
				print('Edit',info["id"])
				data=LeagueSportsradar.objects.filter(id=info["id"]).update(
					competition_id = info["id"] if "id" in info else None,
					name = info["name"] if "name" in info else None,
					gender = info["gender"] if "gender" in info else None,
					parent_id = info["parent_id"] if "parent_id" in info else None,
					category_id = info["category"]["id"] if "id" in info["category"] else None,
					category_name = info["category"]["name"] if "id" in info["category"] else None,
					country_code = info["category"]["country_code"] if "country_code" in info["category"] else None,
					is_active= True if info["id"] in ligue_list else False,
				)
				

	return True

#################### competition seasons ##################################
def CompetitionSeasons():
	from datetime import datetime
	import json
	logError='API Name:CompetitionSeasons,Date:'+datetime.today().strftime('%Y-%m-%d %H:%M:%S')
	json_string = str(logError)
	with open('log.txt', 'a', encoding='utf-8') as file:
		file.write(json_string + '\n')
	file.close()
	Competitions = LeagueSportsradar.objects.all().filter(is_active=True)
	for comp in Competitions:
		url = SPORTRADER_API_URL+"/en/competitions"+comp.id+"/seasons.json?api_key="+SPORTRADER_API_KEY
		payload={}
		headers = {}
		response = requests.request("GET", url, headers=headers, data=payload)
		data = response.json()
		new_data = data["seasons"]
		for info in new_data:
			LeagueSportsradar
			cnt =  LeagueSeasonsSportsradar.objects.filter(id=info["id"]).count()
			if cnt == 0:
				Ins = LeagueSeasonsSportsradar.objects.create(
				
					id=info["id"] if "id" in info else None,
					name= info["name"] if "name" in info else None,
					start_date= info["start_date"] if "start_date" in info else None,
					end_date= info["end_date"] if "end_date" in info else None,
					year= info["year"] if "year" in info else None,
					competition_id= info["competition_id"] if "competition_id" in info else None
				)
			else:
				data = LeagueSportsradar.objects.get(id=info["id"])
				data.name= info["name"] if "name" in info else None
				data.start_date= info["start_date"] if "start_date" in info else None
				data.end_date= info["end_date"] if "end_date" in info else None
				data.year= info["year"] if "year" in info else None
				data.competition_id= info["competition_id"] if "competition_id" in info else None
		time.sleep(5)
	return True

#################### competition season competitiors  ##################################
def CompetitionSeasonsCompetitiors():
	from datetime import datetime
	import json
	logError='API Name:CompetitionSeasonsCompetitiors,Date:'+datetime.today().strftime('%Y-%m-%d %H:%M:%S')
	json_string = str(logError)
	with open('log.txt', 'a', encoding='utf-8') as file:
		file.write(json_string + '\n')
	file.close()
	Competitions = LeagueSeasonsSportsradar.objects.all()
	for comp in Competitions:
		url = SPORTRADER_API_URL+"/en/competitions"+comp.id+"/competitors.json?api_key="+SPORTRADER_API_KEY
		payload={}
		headers = {}
		response = requests.request("GET", url, headers=headers, data=payload)
		data = response.json()
		new_data = data["season_competitors"]
		for info in new_data:
			LeagueSportsradar
			cnt =  LeagueSeasonsCompetitorsSportsradar.objects.filter(id=info["id"]).count()
			if cnt == 0:
				Ins = LeagueSeasonsCompetitorsSportsradar.objects.create(
				
					id=info["id"] if "id" in info else None,
					name= info["name"] if "name" in info else None,
					short_name= info["short_name"] if "short_name" in info else None,
					abbreviation= info["abbreviation"] if "abbreviation" in info else None,
					season_id= comp.id
				)
			else:
				data = LeagueSeasonsCompetitorsSportsradar.objects.get(id=info["id"])
				data.name= info["name"] if "name" in info else None
				data.short_name= info["short_name"] if "short_name" in info else None
				data.abbreviation= info["abbreviation"] if "abbreviation" in info else None
				data.season_id= comp.id
		time.sleep(5)
	return True

#################### league_season_schedules_sportsradar  ##################################
def CompetitionSeasonsSchedulesCompetitiors():
	from datetime import datetime
	import json
	logError='API Name:CompetitionSeasonsSchedulesCompetitiors,Date:'+datetime.today().strftime('%Y-%m-%d %H:%M:%S')
	json_string = str(logError)
	with open('log.txt', 'a', encoding='utf-8') as file:
		file.write(json_string + '\n')
	file.close()
	Competitions = LeagueSeasonsSportsradar.objects.all()
	for comp in Competitions:
		url = SPORTRADER_API_URL+"/en/competitions"+comp.id+"/schedules.json?api_key="+SPORTRADER_API_KEY
		payload={}
		headers = {}
		response = requests.request("GET", url, headers=headers, data=payload)
		data = response.json()
		new_data = data["schedules"]
		for info in new_data:
			LeagueSportsradar
			cnt =  LeagueSeasonsSchedulesCompetitorsSportsradar.objects.filter(sport_event_id=info["sport_event"]["id"]).count()
			if cnt == 0:
				Ins = LeagueSeasonsSchedulesCompetitorsSportsradar.objects.create(
					sport_event_id =  info["sport_event"]["id"] if "id" in info["sport_event"] else None,
					sport_event_start_time =  info["sport_event"]["start_time"] if "start_time" in info["sport_event"] else None,
					sport_event_start_time_confirmed =  info["sport_event"]["start_time_confirmed"] if "start_time_confirmed" in info["sport_event"] else None,
					sport_event_context_category_id =  info["sport_event"]["sport_event_context"]["category"]["id"] if "id" in info["sport_event"]["sport_event_context"]["category"] else None,
					sport_event_context_category_name =  info["sport_event"]["sport_event_context"]["category"]["name"] if "name" in info["sport_event"]["sport_event_context"]["category"] else None,
					sport_event_context_category_country_code =  info["sport_event"]["sport_event_context"]["category"]["country_code"] if "country_code" in info["sport_event"]["sport_event_context"]["category"] else None,
					sport_event_context_competition_id =  info["sport_event"]["sport_event_context"]["competition"]["id"] if "id" in info["sport_event"]["sport_event_context"]["competition"] else None,
					sport_event_context_competition_name =  info["sport_event"]["sport_event_context"]["competition"]["name"] if "name" in info["sport_event"]["sport_event_context"]["competition"] else None,
					sport_event_context_competition_gender =  info["sport_event"]["sport_event_context"]["competition"]["gender"] if "gender" in info["sport_event"]["sport_event_context"]["competition"] else None,
					sport_event_context_season_id =  info["sport_event"]["sport_event_context"]["season"]["id"] if "id" in info["sport_event"]["sport_event_context"]["season"] else None,
					sport_event_context_season_name =  info["sport_event"]["sport_event_context"]["season"]["name"] if "name" in info["sport_event"]["sport_event_context"]["season"] else None,
					sport_event_context_season_start_date =  info["sport_event"]["sport_event_context"]["season"]["start_date"] if "start_date" in info["sport_event"]["sport_event_context"]["season"] else None,
					sport_event_context_season_end_date =  info["sport_event"]["sport_event_context"]["season"]["end_date"] if "end_date" in info["sport_event"]["sport_event_context"]["season"] else None,
					sport_event_context_season_year =  info["sport_event"]["sport_event_context"]["season"]["year"] if "year" in info["sport_event"]["sport_event_context"]["season"] else None,
					sport_event_context_season_competition_id =  info["sport_event"]["sport_event_context"]["season"]["competition_id"] if "competition_id" in info["sport_event"]["sport_event_context"]["season"] else None,
					sport_event_context_stage_order =  info["sport_event"]["sport_event_context"]["stage"]["order"] if "order" in info["sport_event"]["sport_event_context"]["stage"] else None,
					sport_event_context_stage_type =  info["sport_event"]["sport_event_context"]["stage"]["type"] if "type" in info["sport_event"]["sport_event_context"]["stage"] else None,
					sport_event_context_stage_phase =  info["sport_event"]["sport_event_context"]["stage"]["phase"] if "phase" in info["sport_event"]["sport_event_context"]["stage"] else None,
					sport_event_context_stage_start_date =  info["sport_event"]["sport_event_context"]["stage"]["start_date"] if "start_date" in info["sport_event"]["sport_event_context"]["stage"] else None,
					sport_event_context_stage_end_date =  info["sport_event"]["sport_event_context"]["stage"]["end_date"] if "end_date" in info["sport_event"]["sport_event_context"]["stage"] else None,
					sport_event_context_stage_year =  info["sport_event"]["sport_event_context"]["stage"]["year"] if "year" in info["sport_event"]["sport_event_context"]["stage"] else None,
					sport_event_context_groups =  json.dumps(info["sport_event"]["sport_event_context"]["groups"]) if "groups" in info["sport_event"]["sport_event_context"] else None,
					sport_event_competitors =  json.dumps(info["sport_event"]["competitors"]) if "competitors" in info["sport_event"] else None,
					sport_event_venue =  json.dumps(info["sport_event"]["venue"]) if "venue" in info["sport_event"] else None,
					sport_event_status =  json.dumps(info["sport_event_status"]) if "sport_event_status" in info else None,
					season_id= comp.id
				)
			else:
				data = LeagueSeasonsSchedulesCompetitorsSportsradar.objects.get(sport_event_id=info["sport_event"]["id"])
				data.sport_event_start_time =  info["sport_event"]["start_time"] if "start_time" in info["sport_event"] else None,
				data.sport_event_start_time_confirmed =  info["sport_event"]["start_time_confirmed"] if "start_time_confirmed" in info["sport_event"] else None,
				data.sport_event_context_category_id =  info["sport_event"]["sport_event_context"]["category"]["id"] if "id" in info["sport_event"]["sport_event_context"]["category"] else None,
				data.sport_event_context_category_name =  info["sport_event"]["sport_event_context"]["category"]["name"] if "name" in info["sport_event"]["sport_event_context"]["category"] else None,
				data.sport_event_context_category_country_code =  info["sport_event"]["sport_event_context"]["category"]["country_code"] if "country_code" in info["sport_event"]["sport_event_context"]["category"] else None,
				data.sport_event_context_competition_id =  info["sport_event"]["sport_event_context"]["competition"]["id"] if "id" in info["sport_event"]["sport_event_context"]["competition"] else None,
				data.sport_event_context_competition_name =  info["sport_event"]["sport_event_context"]["competition"]["name"] if "name" in info["sport_event"]["sport_event_context"]["competition"] else None,
				data.sport_event_context_competition_gender =  info["sport_event"]["sport_event_context"]["competition"]["gender"] if "gender" in info["sport_event"]["sport_event_context"]["competition"] else None,
				data.sport_event_context_season_id =  info["sport_event"]["sport_event_context"]["season"]["id"] if "id" in info["sport_event"]["sport_event_context"]["season"] else None,
				data.sport_event_context_season_name =  info["sport_event"]["sport_event_context"]["season"]["name"] if "name" in info["sport_event"]["sport_event_context"]["season"] else None,
				data.sport_event_context_season_start_date =  info["sport_event"]["sport_event_context"]["season"]["start_date"] if "start_date" in info["sport_event"]["sport_event_context"]["season"] else None,
				data.sport_event_context_season_end_date =  info["sport_event"]["sport_event_context"]["season"]["end_date"] if "end_date" in info["sport_event"]["sport_event_context"]["season"] else None,
				data.sport_event_context_season_year =  info["sport_event"]["sport_event_context"]["season"]["year"] if "year" in info["sport_event"]["sport_event_context"]["season"] else None,
				data.sport_event_context_season_competition_id =  info["sport_event"]["sport_event_context"]["season"]["competition_id"] if "competition_id" in info["sport_event"]["sport_event_context"]["season"] else None,
				data.sport_event_context_stage_order =  info["sport_event"]["sport_event_context"]["stage"]["order"] if "order" in info["sport_event"]["sport_event_context"]["stage"] else None,
				data.sport_event_context_stage_type =  info["sport_event"]["sport_event_context"]["stage"]["type"] if "type" in info["sport_event"]["sport_event_context"]["stage"] else None,
				data.sport_event_context_stage_phase =  info["sport_event"]["sport_event_context"]["stage"]["phase"] if "phase" in info["sport_event"]["sport_event_context"]["stage"] else None,
				data.sport_event_context_stage_start_date =  info["sport_event"]["sport_event_context"]["stage"]["start_date"] if "start_date" in info["sport_event"]["sport_event_context"]["stage"] else None,
				data.sport_event_context_stage_end_date =  info["sport_event"]["sport_event_context"]["stage"]["end_date"] if "end_date" in info["sport_event"]["sport_event_context"]["stage"] else None,
				data.sport_event_context_stage_year =  info["sport_event"]["sport_event_context"]["stage"]["year"] if "year" in info["sport_event"]["sport_event_context"]["stage"] else None,
				data.sport_event_context_groups =  json.dumps(info["sport_event"]["sport_event_context"]["groups"]) if "groups" in info["sport_event"]["sport_event_context"] else None,
				data.sport_event_competitors =  json.dumps(info["sport_event"]["competitors"]) if "competitors" in info["sport_event"] else None,
				data.sport_event_venue =  json.dumps(info["sport_event"]["venue"]) if "venue" in info["sport_event"] else None,
				data.sport_event_status =  json.dumps(info["sport_event_status"]) if "sport_event_status" in info else None,
				data.season_id= comp.id
		time.sleep(5)
	return True

#################### season competitor profile  ##################################
def CompitatioLeagueSeasonCompetitorsProfilSportsradar():
	from datetime import datetime
	import json
	logError='API Name:CompitatioLeagueSeasonCompetitorsProfilSportsradar,Date:'+datetime.today().strftime('%Y-%m-%d %H:%M:%S')
	json_string = str(logError)
	with open('log.txt', 'a', encoding='utf-8') as file:
		file.write(json_string + '\n')
	file.close()
	Competitions = LeagueSeasonsCompetitorsSportsradar.objects.all()
	for team in Competitions:
		url = SPORTRADER_API_URL+"/en/competitions"+team.id+"/profile.json?api_key="+SPORTRADER_API_KEY
		payload={}
		headers = {}
		response = requests.request("GET", url, headers=headers, data=payload)
		data = response.json()
		cnt =  LeagueSeasonsCompetitorsProfileSportsradar.objects.filter(competitor_id=team.id).count()

		if cnt == 0:
			Ins = LeagueSeasonsCompetitorsProfileSportsradar.objects.create(
				competitor_id= data["competitor"]["id"] if "id" in data["competitor"] else None,
				competitor_name= data["competitor"]["name"] if "name" in data["competitor"] else None,
				competitor_country= data["competitor"]["country"] if "country" in data["competitor"] else None,
				competitor_country_code= data["competitor"]["country_code"] if "country_code" in data["competitor"] else None,
				competitor_abbreviation= data["competitor"]["abbreviation"] if "abbreviation" in data["competitor"] else None,
				competitor_gender= data["competitor"]["gender"] if "gender" in data["competitor"] else None,
				category_id= data["category"]["id"] if "id" in data["category"] else None,
				category_name= data["category"]["name"] if "name" in data["category"] else None,
				category_country_code= data["category"]["country_code"] if "country_code" in data["category"] else None,
				sport= json.dumps(data["sport"])if "sport" in data else None,
				jerseys= json.dumps(data["jerseys"]) if "jerseys" in data else None,
				manager= json.dumps(data["manager"]) if "manager" in data else None,
				venue= json.dumps(data["venue"]) if "venue" in data else None,
				players= (data["players"]) if "players" in data else None
			)
		else:
			data = LeagueSeasonsCompetitorsProfileSportsradar.objects.get(competitor_id=data["competitor"]["id"])
			data.competitor_name= data["competitor"]["name"] if "name" in data["competitor"] else None,
			data.competitor_country= data["competitor"]["country"] if "country" in data["competitor"] else None,
			data.competitor_country_code= data["competitor"]["country_code"] if "country_code" in data["competitor"] else None,
			data.competitor_abbreviation= data["competitor"]["abbreviation"] if "abbreviation" in data["competitor"] else None,
			data.competitor_gender= data["competitor"]["gender"] if "gender" in data["competitor"] else None,
			data.category_id= data["category"]["id"] if "id" in data["category"] else None,
			data.category_name= data["category"]["name"] if "name" in data["category"] else None,
			data.category_country_code= data["category"]["country_code"] if "country_code" in data["category"] else None,
			data.sport= json.dumps(data["sport"])if "sport" in data else None,
			data.jerseys= json.dumps(data["jerseys"]) if "jerseys" in data else None,
			data.manager= json.dumps(data["manager"]) if "manager" in data else None,
			data.venue= json.dumps(data["venue"]) if "venue" in data else None,
			data.players= (data["players"]) if "players" in data else None
		
	return true

def team_dataOld(competitor_id):
    url = SPORTRADER_API_URL+"/en/competitors/"+str(competitor_id)+"/summaries.json?api_key="+SPORTRADER_API_KEY
    payload={}
    headers ={}
    response = requests.request("GET", url, headers=headers, data=payload)
    url2 = "http://44.195.135.131:8000/api/football/sportrader/sportradarSoccerEloRating"
    payload2 = json.dumps({"sportsradar_competitor_id": str(competitor_id)})
    headers2 = {'Content-Type': 'application/json'}
    response2 = requests.request("POST", url2, headers=headers2, data=payload2)
    elo_data = response2.json()
    elo_data = elo_data["data"][0]
    data = response.json()
    sot_value=[]
    formpoint_value=[]
    for match in range(5):
        try:
            if data['summaries'][match]['sport_event_status']['winner_id']==str(competitor_id):
                formpoint_value.append(3)
            elif data['summaries'][match]['sport_event_status']['winner_id']!=str(competitor_id):
                formpoint_value.append(0)
        except:
            formpoint_value.append(1)
    for match in range(5):
        for team in range(2):
            try:
                if data['summaries'][match]['statistics']['totals']['competitors'][team]['id']==str(competitor_id):
                    sot_value.append(data['summaries'][match]['statistics']['totals']['competitors'][team]['statistics']['shots_on_target'])
            except:
                sot_value.append(0)
    return {
        'form_points':sum(formpoint_value),
        'avg_shot_on_target':round((sum(sot_value)/len(sot_value)),2),
        'elo_rating': float(elo_data["elo_rating"])
        
    }
def team_data(competition_id,competitor_id):
	res = '[]'
	# SaveSoccerEloRating(competitor_id)
	json_req={ "competition_id": competition_id,"competitor_id": competitor_id}
	url = AIMODELURL + "team_data/"
	response = requests.post(url, json=json_req)
	print('Teamdata Detail')
	print(response.text)
	print(competition_id,competitor_id)
	print("-----------------")
	if response.text!= 'Internal Server Error':

		res =json.dumps(json.loads(response.text))
		SaveSoccerEloRating(competitor_id,json.loads(response.text))
	return res
def GetPosionAndProbabilityDetailFormTeamId(home_team_id,away_team_id):
	
	res = '[]'
	json_req={ "HomeTeam": [home_team_id],"AwayTeam": [away_team_id]}
	payload = json.dumps(json_req)
	print(payload)
	headers = {'Content-Type': 'application/json'}
	url = AIMODELURL + "poisson_prediction/"
	response = requests.request("POST", url, headers=headers, data=payload, verify=False)
	print(response.text)
	if response.text!= 'Internal Server Error':
		res =json.dumps(json.loads(response.text))

	print('poisson_prediction ---')
	print(res)
	print("===============")
	return res
def GetPredictionDataWithSportsradar(ht_form_points,at_form_points,ht_avg_shot_on_target,at_avg_shot_on_target,ht_elo_rating,at_elo_rating,competition_id):
	import json
	res = '[]'
	url = AIMODELURL + "soccer_prediction/"
	json_req={
		'ht_form_points': ht_form_points,
		'at_form_points': at_form_points,
		'ht_avg_shot_on_target': ht_avg_shot_on_target,
		'at_avg_shot_on_target': at_avg_shot_on_target,
		'ht_elo_rating': ht_elo_rating,
		'at_elo_rating': at_elo_rating,
		'competition_id':competition_id
	}
	
	payload = json.dumps(json_req)
	# print(payload)
	headers = {'Content-Type': 'application/json'}

	response = requests.post(url,headers=headers, data=payload)
	# response = requests.post(url, json=json_req)
	# print(response.text)
	if response.text!= 'Internal Server Error':
		res =json.dumps(json.loads(response.text))
	print('soccer_prediction -------')
	print(res)
	print("*******************")
	return res
def SaveSoccerEloRating(compitator_id,request_data):
   
    print(compitator_id)
    cnt =  SportsradarSoccerEloRating.objects.filter(sportsradar_competitor_id=compitator_id).count()
    print(cnt)
    if cnt == 0:
        ins = SportsradarSoccerEloRating.objects.create(
            sportsradar_competitor_id=request_data['sportsradar_competitor_id'],
            sportsradar_competitor_short_name = request_data['sportsradar_competitor_short_name'],
            clubelo_team_name = request_data['clubelo_team_name'],
            betfair_team_name = request_data['betfair_team_name'],
            form_points= request_data['form_points'],
            elo_rating= request_data['elo_rating'],
           
        )
    # else:
    #     data = SportsradarSoccerEloRating.objects.get(sportsradar_competitor_id__contains=str(compitator_id))
    #     data.sportsradar_competitor_short_name = request_data['sportsradar_competitor_short_name']
    #     data.clubelo_team_name = request_data['clubelo_team_name']
    #     data.betfair_team_name = request_data['betfair_team_name']
    #     data.elo_rating= request_data['elo_rating']
    #     data.save()
    if cnt > 0:
    	print(request_data['elo_rating'])
    	data = SportsradarSoccerEloRating.objects.filter(sportsradar_competitor_id__contains=str(compitator_id)).update(
    		elo_rating= request_data['elo_rating'],
    		form_points= request_data['form_points'],
    		avg_shot_on_target= request_data['avg_shot_on_target']
    	)
    return(True)