from django.conf import settings
from django.shortcuts import render
from db_table.models import *
from django.views import View
from django.template import RequestContext
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import admin
import os
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from BetfairUpdater.SoccerCalculation import *
from webservices.serializers import *
from webservices.views.BitfairLib import *
from webservices.views.LibRapidAPI import *
from webservices.views.CommonFunction import *
from webservices.views.bitfairapi import *
from webservices.views.constants import *
from soccer.scrap import *
from django.utils import timezone
# from webservices.views.Common_function import *
from datetime import datetime
from django.http import HttpResponseRedirect
import string 
from django.utils.text import slugify 
import random 
from django.db.models import Q
from django.db.models import Count
from django.db.models import Sum
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
def login(request):
	logout(request)
	return render(request,'../templates/ltr/login.html')
def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/admin/login/?next=/admin/')
@login_required(login_url="/admin/login/")
def index(request):
	import datetime
	from django.utils.timezone import datetime #important if using timezones
	today = datetime.today()
	league_search = request.GET.get('league', '')
	league_ids=LeagueIdGolaServe()
	queryObj = {}
	one_week_ago = datetime.today() + timedelta(days=7)
	queryObj['formated_date__gte'] = today.strftime('%Y-%m-%d')
	# queryObj['formated_date__lte'] = one_week_ago.strftime('%Y-%m-%d')
	if 'league' in request.GET:
		league_search =int(league_search)
		queryObj['league_id'] = league_search
	else:
		queryObj['league_id__in'] =  league_ids
	
	fixtures = MatchGoalserve.objects.all().filter(**queryObj)[:4]

	result = MatchByTeamGoalserveSerializer(fixtures, many=True).data
	# print(queryObj)
	user =Users.objects.all().filter(~Q(last_login=None),Q(is_superuser=False)).order_by('-last_login')[:10]
	payment = UserSubscriptionPayment.objects.all().order_by('-date_of_payment')[:10]
	# rapid=testRapid()
	prediction = predictionH2HOddsGoalserve.objects.all().order_by('-formated_date')[:3]
	league=GatAllActiveLeagueByGoalServe()
	return render(request, '../templates/ltr/index.html',{'result':result,'user_res':user,'BASEURL':BASEURL,'payment':payment,'prediction':prediction,'league_search':league_search,'league':league})

@login_required(login_url="/login/")
def replymessage(request):
	print(request.POST.get('message'))
	
	message = Message.objects.create(
		message = request.POST.get('message'),
		receiver_id = request.POST.get('receiver_id'),
		sender_id = request.POST.get('sender_id'),
		message_type = 'message',
		created_date = datetime.utcnow()
	)
	message.save()
	
	return HttpResponseRedirect('/admin/db_table/chat/'+request.POST.get('receiver_id')+'/'+request.POST.get('sender_id'))
def smp(request):
	page = request.GET.get('page', 1)
	league_search = request.GET.get('league', '')
	season_search = request.GET.get('season', '')
	# print(request.GET)
	queryObj = {}
	if 'league' in request.GET:
		league_search =int(league_search)
		queryObj['league_id'] = league_search

	if 'season' in request.GET:
		season_search =int(season_search)
		queryObj['season_id'] = season_search
	start = 20 * int(page)
	end = int(page)
	if len(queryObj) > 0:
		smp_list = SeasonMatchPlan.objects.all().filter(**queryObj).order_by('-match_id')[:start:end]
	else:
		smp_list = SeasonMatchPlan.objects.all().order_by('-match_id')[:start:end]
	for resp in smp_list:
		res =[]
		# print(resp.league_id)
		res = getallSmpIdResult(resp.league_id,resp.home_team_id,resp.away_team_id,resp.season_id)
		# print(res['league'])
		resp.league_name=res['league']
		resp.season_name=res['season']
		resp.home_team_name=res['home_team']
		resp.away_team_name=res['away_team']
	paginator = Paginator(smp_list, 10)
	try:
		smp_list = paginator.page(page)
	except PageNotAnInteger:
		smp_list = paginator.page(1)
	except EmptyPage:
		smp_list = paginator.page(paginator.num_pages)

	leaguelist = Leagues.objects.all().filter(active=True,collection_datasource="www.worldfootball.net")
	seasonlist = AllSeason.objects.all().filter(is_active=True,collection_datasource="www.worldfootball.net")
	return render(request,'../templates/admin/season_match_plan.html',{'season_search':season_search,'league_search':league_search, 'smp_list': smp_list,'leaguelist':leaguelist,'seasonlist':seasonlist })

def getallSmpIdResult(league_id,home_team_id,away_team_id,season_id):
	listData ={}
	# print(league_id)
	league=Leagues.objects.all().filter(league_id=league_id,collection_datasource="www.worldfootball.net").first()
	if league:
		listData['league']=league.name
	else:
		listData['league']=''
	season=AllSeason.objects.all().filter(season_id=season_id,collection_datasource="www.worldfootball.net").first()
	if season:
		listData['season']=season.name
	else:
		listData['season']=''
	
	home_team = Teams.objects.all().filter(team_id=home_team_id,collection_datasource="www.worldfootball.net").first()
	if home_team:
		listData['home_team']=home_team.name
	else:
		listData['home_team']=''

	
	away_team = Teams.objects.all().filter(team_id=away_team_id,collection_datasource="www.worldfootball.net").first()
	
	if away_team:
		listData['away_team'] = away_team.name
	else:
		listData['away_team']=''
	return listData

def probability(request,team_id):
	data = GetTeamwiseProbability(team_id)
	# print(data)
	return render(request,'../templates/admin/probability.html',{ 'teamlist':data})

def playerdetail(request,team_id,match_id):
	user =[]
	data = GetTeamwiseProbability(team_id)
	teaminfo = Teams.objects.all().filter(team_id=team_id,collection_datasource="www.worldfootball.net").first()
	matchteamplayerInfo = MatchTeamPlayerInfo.objects.all().filter(team_id=team_id,match_id=match_id,collection_datasource="www.worldfootball.net")
	# for r in matchteamplayerInfo:

	# 	i = 0
	# 	d = {}
	# 	print(r[i])
	# 	while i < len(x):
	# 		d[x[i][0]] = r[i]
	# 		i = i+1
	# 	user.append(d)
	# print(user)
	for resp in matchteamplayerInfo:
		# print(resp.player_id)
		player_id =int(resp.player_id)
		player =  PlayerList.objects.all().filter(player_id=player_id,collection_datasource="www.worldfootball.net")
		# resp.PlayerList = PlayerListSerializer(player, many=True).data
		resp.PlayerList = player
		Playercareer = PlayerCareer.objects.all().filter(player_id=player_id,collection_datasource="www.worldfootball.net")
		# resp.PlayerCareer = PlayerCareerSerializer(Playercareer, many=True).data
		resp.PlayerCareer = Playercareer
	# playerInfo = PlayerList.all().filter(player_id=player_id,collection_datasource="www.worldfootball.net").first()
	# playerDetail = PlayerCareer.all().filter(player_id=player_id,collection_datasource="www.worldfootball.net")
	return render(request,'../templates/admin/playerdetail.html',{'teaminfo':teaminfo,'matchteamplayerInfo':matchteamplayerInfo,'teamlist':data})

def oddsManager(request,home_team_id,away_team_id):
	home_team = Teams.objects.all().filter(team_id=home_team_id,collection_datasource="www.worldfootball.net").first()
	home_team_result = SeasonLeagueTeamInfo.objects.filter(team_id = home_team_id).values('team_id').order_by('team_id').annotate(total_match=Sum('t_mp')).annotate(total_win=Sum('t_w')).annotate(total_loss=Sum('t_l')).annotate(total_drow=Sum('t_d'))
	away_team = Teams.objects.all().filter(team_id=away_team_id,collection_datasource="www.worldfootball.net").first()
	away_team_result = SeasonLeagueTeamInfo.objects.filter(team_id = away_team_id).values('team_id').order_by('team_id').annotate(total_match=Sum('t_mp')).annotate(total_win=Sum('t_w')).annotate(total_loss=Sum('t_l')).annotate(total_drow=Sum('t_d'))
	total_match = home_team_result[0]['total_match'] + away_team_result[0]['total_match']
	
	HomePrice = (home_team_result[0]['total_win'] + away_team_result[0]['total_loss']) * 100 / total_match
	DrawPrice = (home_team_result[0]['total_drow'] + away_team_result[0]['total_drow']) * 100 / total_match
	AwayPrice = (home_team_result[0]['total_loss'] + away_team_result[0]['total_win'])* 100 / total_match	
	
	home = 100 / HomePrice
	draw = 100 / DrawPrice
	away = 100 / AwayPrice
	
	res ={}
	res['home_team_name'] = home_team.name
	res['home_team_id'] = home_team.team_id
	res['away_team_name'] = away_team.name
	res['away_team_id'] = away_team.team_id 
	res['home'] = round(home - 0.005, 2)			#Home  Odds
	res['draw'] = round(draw - 0.005, 2)			#Draw  Odds
	res['away'] = round(away - 0.005, 2)			#Away Team Odds
	# print(res['home'])
	res['home_odd_prb'] = round((1 / res['home'] *100) - 0.005, 2) 	#Home  Odds percentage
	res['draw_odd_prb'] = round((1 / res['draw'] *100) - 0.005, 2)	#Draw  Odds percentage
	res['away_odd_prb'] = round((1 / res['away'] *100) - 0.005, 2)	#Away  Odds percentage

	#Calculate Assian Handicap

	
	return render(request,'../templates/admin/odds_manager.html',{'res':res})

def singleplayerdetail(request,player_id):
	result ={}
	player_id =int(player_id)
	# print(player_id)
	total_match =0
	total_goal =0
	total_s_in = 0
	total_s_out =0
	total_yellow =0
	total_s_yellow = 0
	total_red = 0
	total_start =0
	number =0
	result['total_match'] = 0
	result['total_goal']= 0
	result['total_s_in']= 0
	result['total_s_out']= 0
	result['total_yellow'] = 0
	result['total_s_yellow']  = 0
	result['total_red'] = 0
	result['total_start'] = 0
	result['avg_match'] = 0
	
	result['avg_matchP'] =0
	result['avg_goal'] = 0
	result['avg_goalP'] =0
	result['avg_s_in'] = 0
	result['avg_s_inP'] =0
	result['avg_s_out'] = 0
	result['avg_s_outP'] =0
	result['avg_yellow'] = 0
	result['avg_yellowP'] =0
	result['avg_s_yellow'] = 0
	result['avg_s_yellowP'] =0
	result['avg_red'] = 0
	result['avg_redP'] =0

	player =  PlayerList.objects.all().filter(player_id=player_id,collection_datasource="www.worldfootball.net")[:1]
	Playercareer = PlayerCareer.objects.all().filter(player_id=player_id,collection_datasource="www.worldfootball.net")	
	if Playercareer:
		for resp in Playercareer:
			number = number+1
			team_detail =  Teams.objects.all().filter(team_id=resp.team_id,collection_datasource="www.worldfootball.net").first()
			league_detail =  Leagues.objects.all().filter(league_id=resp.league_id,collection_datasource="www.worldfootball.net").first()
			season_detail =  AllSeason.objects.all().filter(season_id=resp.season_id,collection_datasource="www.worldfootball.net").first()
			resp.season_name = season_detail.name
			resp.league_name = league_detail.league_dname
			resp.team_name = team_detail.name
			total_match = total_match+resp.matches
			total_goal = total_goal +resp.goals
			total_s_in = total_s_in +resp.s_in
			total_s_out = total_s_out +resp.s_out
			total_yellow = total_yellow +resp.yellow
			total_s_yellow = total_s_yellow +resp.s_yellow
			total_red = total_red +resp.red
			total_start = total_start + resp.started
		result['total_match'] = total_match
		result['total_goal']= total_goal
		result['total_s_in']= total_s_in
		result['total_s_out']= total_s_out
		result['total_yellow'] = total_yellow
		result['total_s_yellow']  = total_s_yellow
		result['total_red'] = total_red
		result['total_start'] = total_start

		result['avg_match'] = round(total_match/number - 0.005, 2)
		result['avg_matchP'] =round((1 / result['avg_match'] *100) - 0.005, 2)
		
		result['avg_goal'] = round(total_goal/number - 0.005, 2)
		result['avg_goalP'] =round((1 / result['avg_goal'] *100) - 0.005, 2)

		result['avg_s_in'] = round(total_s_in/number - 0.005, 2)
		result['avg_s_inP'] =round((1 / result['avg_s_in'] *100) - 0.005, 2)

		result['avg_s_out'] = round(total_s_out/number - 0.005, 2)
		result['avg_s_outP'] =round((1 / result['avg_s_out'] *100) - 0.005, 2)

		result['avg_yellow'] = round(total_yellow/number - 0.005, 2)
		result['avg_yellowP'] =round((1 / result['avg_yellow'] *100) - 0.005, 2)

		result['avg_s_yellow'] = round(total_s_yellow/number - 0.005, 2)
		result['avg_s_yellowP'] =round((1 / result['avg_s_yellow'] *100) - 0.005, 2)

		result['avg_red'] = round(total_red/number - 0.005, 2)
		result['avg_redP'] =round((1 / result['avg_red'] *100) - 0.005, 2)
		

	return render(request,'../templates/admin/singleplayerdetail.html',{'avg_psg':result,'player':player,'Playercareer':Playercareer})

def GetScrapingData(request):
	return render(request,'../templates/ltr/get_scrap_data.html')

def SaveScrapingData(request):
	# print(request)
	# scrapname = request.POST.post('scrapname')
	# scrap_url = request.POST.post('scrap_url')
	# scrap_element_class = request.POST.post('scrap_element_class')
	# print(request.POST['scrapname'])
	
	data =ScrapTool(scrap_type=request.POST['scrap_type'],exemptColumn=request.POST['exemptColumn'],slug=unique_slug_generator(request.POST['scrapname']),scrapname=request.POST['scrapname'],scrap_url=request.POST['scrap_url'],scrap_element_class=request.POST['scrap_element_class'],scrap_element_type=request.POST['scrap_element_type'])
	data.save()
	return HttpResponseRedirect('/admin/db_table/scraplist')

def RunScrapingTool(request,slug):
	
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
	# 	scrapname=request.POST['scrapname'],
	# 	scrap_url=request.POST['scrap_url'],
	# 	scrap_element_class=request.POST['scrap_element_class']
	# )

	return HttpResponseRedirect('/admin/db_table/scraplist')
def scraplist(request):
	scrap_list = ScrapTool.objects.all()
	return render(request,'../templates/ltr/scraplist.html',{'scrap_list':scrap_list})

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

def Creamlist(request):
	cream = request.GET.get('cream', '')
	cream_list = []
	if 'cream' in request.GET:
		if cream == '1':
			cream_list = CreamTeam.objects.all().filter(cream_status='Cream')
			# queryObj['cream_status'] = 'Cream'

		if cream == '2':
			cream_list = CreamTeam.objects.all().filter(cream_status='Nearly Cream')
			# queryObj['cream_status'] = 'Nearly Cream'	
		if cream == '3':
			# queryObj['cream_status'] = 'Not Cream'
			cream_list = CreamTeam.objects.all().filter(cream_status='Not Cream')
		# print(queryObj)
		# cream_list = CreamTeam.objects.all().filter(**queryObj)
	else:
		cream_list = CreamTeam.objects.all()
	# result = CreamTeamSerializer(cream_list, many=True).data
	# print(result)
	for resp in cream_list:
		team_detail =  Teams.objects.all().filter(team_id=resp.team_id,collection_datasource="www.worldfootball.net").first()
		season_detail =  AllSeason.objects.all().filter(season_id=resp.season_id,collection_datasource="www.worldfootball.net").first()
		resp.season_name = season_detail.name
		resp.team_name = team_detail.name
	return render(request,'../templates/admin/CreamList.html',{'cream_list':cream_list})

def ShowPlayerByTeamGraph(request):
	team_search = 0
	player_search =0
	team_id = request.GET.get('team', '')
	data = []
	label = []
	playerlist = []
	print(team_id)
	if 'team' in request.GET:
		team_search = request.GET.get('team', '')
		team_id =int(team_search)
		print('team_search')
		playerlist =  PlayerList.objects.all().filter(now_team_id=team_id,collection_datasource="www.worldfootball.net")
	if 'player' in request.GET:
		player_search = request.GET.get('player', '')
		player_id =int(player_search)
		playercareer = PlayerCareer.objects.all().filter(player_id = player_id,collection_datasource="www.worldfootball.net").order_by('season_id')
		for resp in playercareer:
			data.append(resp.goals)
			season = AllSeason.objects.all().values('name').filter(season_id = resp.season_id,collection_datasource="www.worldfootball.net")
			label.append(season[0]['name'])

	
	teamlist = Teams.objects.all().filter(collection_datasource="www.worldfootball.net")
	return render(request,'../templates/admin/ShowPlayerByTeamGraph.html',{'teamlist':teamlist,'team_search':team_id,'player_search':player_search,'playerlist':playerlist,'data':data,'label':label})
def ShowByTeamGraph(request):
	team_search = 0
	player_search =0
	team_id = request.GET.get('team', 0)
	data = []
	label = []
	
	if 'team' in request.GET:
		team_search = request.GET.get('team', '')
		team_id =int(team_search)
		print('team_search')
		team = PlayerCareer.objects.filter(team_id = team_id).values('team_id','season_id').order_by('team_id').annotate(total_goals=Sum('goals'))
		for resp in team:
			data.append(resp['total_goals'])
			season = AllSeason.objects.all().values('name').filter(season_id = resp['season_id'],collection_datasource="www.worldfootball.net")
			label.append(season[0]['name'])
			# print(resp['total_goals'])
			# print(resp['season_id'])
		
		
	teamlist = Teams.objects.all().filter(collection_datasource="www.worldfootball.net")
	return render(request,'../templates/admin/ShowByTeamGraph.html',{'teamlist':teamlist,'team_search':team_id,'data':data,'label':label})

@csrf_protect
def OddsProbability(request):
	res ={}
	if request.POST:
		# print(request.POST)
		hometeam = request.POST['hometeam']
		awayteam = request.POST['awayteam']
		home_team = Teams.objects.all().filter(team_id=hometeam,collection_datasource="www.worldfootball.net").first()
		away_team = Teams.objects.all().filter(team_id=awayteam,collection_datasource="www.worldfootball.net").first()

		home_team_result = SeasonLeagueTeamInfo.objects.filter(team_id = hometeam).values('team_id').order_by('team_id').annotate(total_match=Sum('t_mp')).annotate(total_win=Sum('t_w')).annotate(total_loss=Sum('t_l')).annotate(total_drow=Sum('t_d'))
		away_team_result = SeasonLeagueTeamInfo.objects.filter(team_id = awayteam).values('team_id').order_by('team_id').annotate(total_match=Sum('t_mp')).annotate(total_win=Sum('t_w')).annotate(total_loss=Sum('t_l')).annotate(total_drow=Sum('t_d'))
		total_match = home_team_result[0]['total_match'] + away_team_result[0]['total_match']
		
		HomePrice = (home_team_result[0]['total_win'] + away_team_result[0]['total_loss']) * 100 / total_match
		DrawPrice = (home_team_result[0]['total_drow'] + away_team_result[0]['total_drow']) * 100 / total_match
		AwayPrice = (home_team_result[0]['total_loss'] + away_team_result[0]['total_win'])* 100 / total_match	
		
		home = 100 / HomePrice
		draw = 100 / DrawPrice
		away = 100 / AwayPrice
		
		res['home_team_detail'] = home_team_result[0]
		res['away_team_detail'] = away_team_result[0]
		res['home_team_name'] = home_team.name
		res['home_team_id'] = home_team.team_id
		res['away_team_name'] = away_team.name
		res['away_team_id'] = away_team.team_id 
		
		res['home'] = round(home - 0.005, 2)			#Home  Odds
		res['draw'] = round(draw - 0.005, 2)			#Draw  Odds
		res['away'] = round(away - 0.005, 2)			#Away Team Odds

		# print(home)
		# print(res['home'],res['draw'],res['away'])

		res['home_odd_prb'] = round((1 / res['home'] *100) - 0.005, 2) 	#Home  Odds percentage
		res['draw_odd_prb'] = round((1 / res['draw'] *100) - 0.005, 2)	#Draw  Odds percentage
		res['away_odd_prb'] = round((1 / res['away'] *100) - 0.005, 2)	#Away  Odds percentage

		# print(res['home_odd_prb'])
		# print(res['draw_odd_prb'])
		# print(res['away_odd_prb'])

		import numpy
		a =	[
				['home_team_name','away_team_name','home_win','home_draw','home_loss','away_win','away_draw','away_loss','home_odds','away_odds','draw'],
				[
					str(res['home_team_name']),
					str(res['away_team_name']),
					str(res['home_team_detail']['total_win']),
					str(res['home_team_detail']['total_drow']),
					str(res['home_team_detail']['total_loss']),
					str(res['away_team_detail']['total_win']),
					str(res['away_team_detail']['total_drow']),
					str(res['away_team_detail']['total_loss']),
					str(res['home']),
					str(res['away']),
					str(res['draw'])
				]
			]
		
		print(a)
		file_name = res['home_team_name'] +'-VS-'+res['away_team_name']+'-Odds.csv'
		import pandas as pd
		df = pd.DataFrame(a)
		df.to_csv(file_name, index=False, header=False)

	teamlist = Teams.objects.all().filter(collection_datasource="www.worldfootball.net")
	return render(request,'../templates/admin/OddsProbability.html',{'teamlist':teamlist,'res':res})

def AssianHandicap(request):
	league_search = request.GET.get('league', '')
	season_search = request.GET.get('season', '')
	match_search = request.GET.get('season', '')
	queryObj = {}
	result=[]
	matchdata=[]
	matchdetail =[]
	stack_value=''
	odds_value =''
	if 'league' in request.GET:
		league_search =int(league_search)
		queryObj['league_id'] = league_search

	if 'season' in request.GET:
		season_search =int(season_search)
		queryObj['season_id'] = season_search

	if 'league' in request.GET and 'season' in request.GET:
		# print(queryObj)
		smp_list = SeasonMatchPlan.objects.all().filter(**queryObj).order_by('-match_id')
		matchdata = MatchNameSerializer(smp_list, many=True).data
		# print(matchdata)
	league=Leagues.objects.all().filter(~Q(name=None),Q(collection_datasource="www.worldfootball.net"))
	season_detail =  AllSeason.objects.all().filter(collection_datasource="www.worldfootball.net")
	if request.POST:
		SingleMatch = SeasonMatchPlan.objects.all().filter(match_id=match)
		stack_value = request.GET.get('stack_value', '')
		odds_value = request.GET.get('odds_value', '')
		away_team_id = 0
		matchdetail = MatchNameSerializer(SingleMatch, many=True).data
		if ah_bets == '+0.25':
			result['backed_team_wins_profit'] = (stack_value * odds_value) - stack_value
			result['backed_team_draws_profit'] = ((stack_value / 2 ) + ((stack_value / 2) * odds_value)) - stack_value
			result['backed_team_loses_profit'] = 0 - stack_value
		if ah_bets == '-0.25':
			result['backed_team_wins_profit'] = (stack_value * odds_value) - stack_value
			result['backed_team_draws_profit'] = (stack_value / 2) - stack_value
			result['backed_team_loses_profit'] = 0 - stack_value
		if ah_bets == '+0.5':
			result['backed_team_wins_profit'] = (stack_value * odds_value) - stack_value
			result['backed_team_draws_profit'] = (stack_value * odds_value) - stack_value
			result['backed_team_loses_profit'] = 0 - stack_value

		if ah_bets == '-0.5':
			result['backed_team_wins_profit'] = (stack_value * odds_value) - stack_value
			result['backed_team_draws_profit'] = 0 - stack_value
			result['backed_team_loses_profit'] = 0 - stack_value

		if ah_bets == '+0.75':
			result['backed_team_wins_profit'] = (stack_value * odds_value) - stack_value
			result['backed_team_draws_profit'] = (stack_value * odds_value) - stack_value
			result['backed_team_loses_profit_1goal'] = (stack_value / 2) - stack_value
			result['backed_team_loses_profit_2goal'] = 0 - stack_value

		if ah_bets == '-0.75':
			result['backed_team_wins_profit_2goal'] = (stack_value * odds_value) - stack_value
			result['backed_team_win_1goal'] =((stack_value / 2 ) + ((odds_value / 2) * odds)) - stack_value
			result['backed_team_draws_profit'] = 0 - stack_value
			result['backed_team_loses_profit'] = 0 - stack_value

		if ah_bets == '+1':
			result['backed_team_wins_profit'] = (stack_value * odds_value) - stack_value
			result['backed_team_draws_profit'] = (stack_value * odds_value) - stack_value
			result['backed_team_loses_profit_1goal'] = stack_value - stack_value
			result['backed_team_loses_profit_2goal'] = 0 - stack_value

		if ah_bets == '-1':
			result['backed_team_wins_profit_2goal'] = (stack_value * odds_value) - stack_value
			result['backed_team_win_1goal'] =stack_value - stack_value
			result['backed_team_draws_profit'] = 0 - stack_value
			result['backed_team_loses_profit'] = 0 - stack_value

		if ah_bets == '+1.25':
			result['backed_team_wins_profit'] = (stack_value * odds_value) - stack_value
			result['backed_team_draws_profit'] = (stack_value * odds_value) - stack_value
			result['backed_team_loses_profit_1goal'] = ((stack_value / 2) + ((stack_value / 2) * odds_value)) - stack_value
			result['backed_team_loses_profit_2goal'] = 0 - stack_value

		if ah_bets == '-1.25':
			result['backed_team_wins_profit_2goal'] = (stack_value * odds_value) - stack_value
			result['backed_team_win_1goal'] = (stack_value / 2) - stack_value
			result['backed_team_draws_profit'] = 0 - stack_value
			result['backed_team_loses_profit'] = 0 - stack_value

		if ah_bets == '+1.5':
			result['backed_team_wins_profit'] = (stack_value * odds_value) - stack_value
			result['backed_team_draws_profit'] = (stack_value * odds_value) - stack_value
			result['backed_team_loses_profit_1goal'] = (stack_value * odds_value) - stack_value
			result['backed_team_loses_profit_2goal'] = 0 - stack_value

		if ah_bets == '-1.5':
			result['backed_team_wins_profit_2goal'] = (stack_value * odds_value) - stack_value
			result['backed_team_win_1goal'] = (stack_value / 2) - stack_value
			result['backed_team_draws_profit'] = 0 - stack_value
			result['backed_team_loses_profit'] = 0 - stack_value

		if ah_bets == '+1.75':
			result['backed_team_wins_profit'] = (stack_value * odds_value) - stack_value
			result['backed_team_draws_profit'] = (stack_value * odds_value) - stack_value
			result['backed_team_loses_profit_1goal'] = (stack_value * odds_value) - stack_value
			result['backed_team_loses_profit_2goal'] = (stack_value / 2) - stack_value
			result['backed_team_loses_profit_3goal'] = 0 - stack_value

		if ah_bets == '-1.75':
			result['backed_team_loses_profit_3goal'] = (stack_value * odds_value) - stack_value
			result['backed_team_wins_profit_2goal'] =  ((stack_value / 2) + ((stack_value / 2) * odds)) - stack_value
			result['backed_team_win_1goal'] = 0 - stack_value
			result['backed_team_draws_profit'] = 0 - stack_value
			result['backed_team_loses_profit'] = 0 - stack_value	

		if ah_bets == '+2':
			result['backed_team_wins_profit'] = (stack_value * odds_value) - stack_value
			result['backed_team_draws_profit'] = (stack_value * odds_value) - stack_value
			result['backed_team_loses_profit_1goal'] = (stack_value * odds_value) - stack_value
			result['backed_team_loses_profit_2goal'] = stack_value - stack_value
			result['backed_team_loses_profit_3goal'] = 0 - stack_value

		if ah_bets == '-2':
			result['backed_team_loses_profit_3goal'] = (stack_value * odds_value) - stack_value
			result['backed_team_wins_profit_2goal'] =  stack_value - stack_value
			result['backed_team_win_1goal'] = 0 - stack_value
			result['backed_team_draws_profit'] = 0 - stack_value
			result['backed_team_loses_profit'] = 0 - stack_value	
	return render(request,'../templates/admin/AssianHandicap.html',
		{
		'league':league,
		'season_detail':season_detail,
		'result':result,
		'league_search':league_search,
		'season_search':season_search,
		'matchdata':matchdata,
		
		'matchdetail':matchdetail,
		'stack_value':stack_value,
		'odds_value':odds_value
		})

@csrf_protect
def ViewMatchByDate(request):
	import datetime
	from django.utils.timezone import datetime #important if using timezones
	today = datetime.today()
	league_ids=LeagueIdGolaServe()
	response = {}
	queryObj = {}
	start_limit =15
	end_limit =30
	date1 =''
	date2 =''
	league_id =''
	print(request.POST)
	if request.POST:
		queryObj = {}
		date1 = request.POST['todate']
		date2 = request.POST['fromdate']
		if 'League' in request.POST and request.POST['League'] !='':
			queryObj['league_id'] =  request.POST['League']
			one_week_ago = datetime.today() + timedelta(days=7)
			queryObj['formated_date__gte'] = today.strftime('%Y-%m-%d')
			queryObj['formated_date__lte'] = one_week_ago.strftime('%Y-%m-%d')
		else:
			queryObj['league_id__in'] =  league_ids
		
		

		if 'fromdate' in request.POST and request.POST['fromdate'] !='':
			date2 = request.POST['fromdate']
			queryObj['formated_date__lte'] = request.POST['fromdate']
		
		if 'todate' in request.POST and request.POST['todate'] !='':
			queryObj['formated_date__gte'] = request.POST['todate']

		if 'today' in request.POST and request.POST['today'] !='':
			queryObj['formated_date'] = datetime.today().strftime('%Y-%m-%d')
	
	else:
		queryObj = {}
		one_week_ago = datetime.today() + timedelta(days=7)
		queryObj['formated_date__gte'] = today.strftime('%Y-%m-%d')
		queryObj['formated_date__lte'] = one_week_ago.strftime('%Y-%m-%d')
		# queryObj['league_id__in'] =  league_ids
	print(queryObj)
	fixtures = MatchGoalserve.objects.all().filter(**queryObj)[3:9]
	for fix in fixtures:
		print(fix.match_id)
	result = MatchByTeamGoalserveSerializerOptional(fixtures, many=True).data	
	league=GatAllActiveLeagueByGoalServe()
	# dn=download_prediction(fixtures)
	return render(request,'../templates/ltr/ViewMatchByDate_org.html',
		{'league':league,'final_res':result,'start_limit':start_limit,'end_limit':end_limit,'League':league_id,'todate':date1,'fromdate':date2})

@csrf_protect
def ViewMatchByDate_rapid(request):
	import datetime
	from datetime import datetime
	from datetime import datetime, timedelta
	import datetime as dt
	# from django.utils.timezone import datetime #important if using timezones
	today = datetime.today().strftime('%Y-%m-%d')
	final_res = []
	league_id=39
	
	result = json.loads(getFxtureByLeagueRAPIDAPI(39,2021))
	
	for item in result['response']:
		date2 = item['fixture']['date']
		new_date=(date2[0:10])
		date1 = dt.datetime.strptime(new_date,'%Y-%m-%d')
		# date1 = new_date.strftime('%Y-%m-%d ')
		# date1 = datetime.fromisoformat(item['fixture']['date']+'z'[:-1])
		newdate1= date1.strftime('%Y-%m-%d')
		if newdate1 > today :
			final_res.append(item)
			# print("-------")
			# print(item)
	return render(request,'../templates/ltr/ViewMatchByDate.html',{'final_res':final_res})

@csrf_protect
def matchDetail(request,match_id):
	
	final_res = []
	fixtures = MatchFixtureUpdate.objects.all().filter(matchid=match_id)
	result = MatchFixtureUpdateSerializer(fixtures, many=True).data

	for index, item in enumerate(result):
    
		req_data = {}
		# print(item["season_id"])
		# get_seasonlist(request, id=item["season_id"])
		# print(item["localteam_id"])
		# print(item["visitorteam_id"])
		item['localPlayer'] = GetPlayerByteamId(item["localteam_id"])
		item['visiterPlayer'] = GetPlayerByteamId(item["visitorteam_id"])
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
		localteam_Detail = GetSeasonNameAndTeamStatDetails(item["localteam_id"])
		visitorteam_Detail = GetSeasonNameAndTeamStatDetails(item["visitorteam_id"])

		
		# localteam = graphPlotTeam(localteam_Detail,'localteam')
		# visitorteam = graphPlotTeam(visitorteam_Detail,'visitorteam')
		localteam = 'media/localteam.png'
		visitorteam = 'media/visitorteam.png'
	return render(request,'../templates/ltr/MatchDetail.html',{'final_res':final_res,'localteam_Detail':localteam,'visitorteam_Detail':visitorteam})
def graphPlotTeam(team_detail,team_name):
	import datetime
	from io import BytesIO
	import base64
	import matplotlib.pyplot as plt
	import numpy as np
	x_axis =[]
	qty = []
	file_name =''
	# print(team_detail)
	if team_detail:
		# print(team_detail)
		for rec in team_detail:
			
			# print(rec['season'])
			x_axis.append(rec['season'])
			goal= json.loads(rec['goals_for'])
			
			qty.append(goal['total'])

		# objects = ['12/10/2019','12/11/2020','15/10/2020']
		y_pos = np.arange(len(x_axis))
		
		plt.bar(y_pos, qty, align='center', alpha=0.5)
		plt.xticks(y_pos, x_axis)
		plt.ylabel('Goal')
		plt.xlabel('Season')
		plt.title('Team Graph')
		file_name = 'media/'+team_name+'.png'
		plt.savefig(file_name)
		print(file_name)
	return file_name

@csrf_exempt
def HeadtoHeadView(request,match_id):
	headtohead=[]
	final_res = []
	localteam ={}
	visiterteam ={}
	leagueByTeamId =[]
	teamDetail =[]
	league_id = 0
	final_h2h ={}
	fixtures = MatchGoalserve.objects.all().filter(match_id=match_id)
	result = MatchByTeamGoalserveSerializer(fixtures, many=True).data
	final_h2h['localteam'] = result[0]['localteam'][0]
	final_h2h['visiterteam'] = result[0]['visitorteam'][0]
	# print(result[0]['localteam'])
	league_id =result[0]['league_id']	
	localteam_id =result[0]['localteam_id']
	visitorteam_id =result[0]['visitorteam_id']
	
	localteam_name =result[0]['localteam_name']
	visitorteam_name =result[0]['visitorteam_name']

	finalh2h = TeamStatisticsGoalserve.objects.all().filter(league_ids__contains=league_id)
	teamDetail = TeamStatisticsGoalserveSerializer(finalh2h, many=True).data
	headtohead=head2head(int(localteam_id),int(visitorteam_id))
	prediction=GetPosionDetailFormTeamId(localteam_name,visitorteam_name)
	
	return render(request,'../templates/ltr/headtohead_org.html',{
		'match_id':match_id,
		'final_res':result,
		'headtohead':headtohead,
		'localteam':localteam,
		'visiterteam':visiterteam,
		'teamDetail':teamDetail,
		'final_h2h':final_h2h,
		'prediction':json.loads(prediction)
		}
	)

@csrf_exempt
def HeadtoHeadView_rapid(request,match_id,league_id,home_team,away_team):
	headtohead=[]
	matchDetail = []
	final_res = []
	localteam =[]
	visiterteam =[]
	leagueByTeamId =[]
	teamDetail =[]
	season_id ='2019'
	final_h2h ={}
	# print(league_id)
	TeamlistByLeague = json.loads(getTeamByLeague(4))
	# print(TeamlistByLeague['api'])
	i =0
	for item in TeamlistByLeague['api']['teams']:
		if i<5:
			Teamdtl = json.loads(TeamStatisticsByLeagueandSeason(item['team_id'],season_id,league_id))
			# print(Teamdtl)
			teamDetail.append(Teamdtl['response'])
		i = i+1
	match=json.loads(GetFixtureByFixtureId(match_id))
	# print(match['response'])
	if match:
		matchDetail = match['response'][0]
	# print(matchDetail[0])
	# print(localteam)
	# headtohead=head2head(int(home_team),int(away_team))
	# prediction=GetPosionDetailFormTeamId(localteam.team.name,visiterteam.team.name)
	return render(request,'../templates/ltr/headtohead.html',{'match_id':match_id,'headtohead':[],'matchDetail':matchDetail,'teamDetail':teamDetail,'final_h2h':[],'prediction':[]})
	
@csrf_exempt
def prediction(request,match_id):
	headtohead=[]
	final_res = []
	localteam ={}
	visiterteam ={}
	leagueByTeamId =[]
	teamDetail =[]
	league_id = 0
	final_h2h ={}
	fixtures = MatchGoalserve.objects.all().filter(match_id=match_id)
	result = MatchByTeamGoalserveSerializer(fixtures, many=True).data
	final_h2h['localteam'] = result[0]['localteam'][0]
	final_h2h['visiterteam'] = result[0]['visitorteam'][0]
	# print(result[0]['localteam'])
	league_id =result[0]['league_id']	
	localteam_id =result[0]['localteam_id']
	visitorteam_id =result[0]['visitorteam_id']
	localteam_name =result[0]['localteam_name']
	visitorteam_name =result[0]['visitorteam_name']
	finalh2h = TeamStatisticsGoalserve.objects.all().filter(league_ids__contains=league_id)
	teamDetail = TeamStatisticsGoalserveSerializer(finalh2h, many=True).data
	headtohead=head2head(int(localteam_id),int(visitorteam_id))
	prediction=GetPosionDetailFormTeamId(localteam_name,visitorteam_name)
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
	predictionOdds = []		# predictionOdds=GetPredictionByMatch(LPreprocess['HTFormPts'],VPreprocess['ATFormPts'],HomeTeamLP,AwayTeamLP,qr0,qr1)

	return render(request,'../templates/ltr/prediction.html',{
		'match_id':match_id,
		'final_res':result,
		'final_h2h':final_h2h,
		'headtohead':headtohead,
		'localteam':localteam,
		'visiterteam':visiterteam,
		'teamDetail':teamDetail,
		'prediction':json.loads(prediction),
		'predictionOdds':predictionOdds
		}
	)

@csrf_exempt
def tableData(request,match_id):
	headtohead=[]
	final_res = []
	localteam ={}
	visiterteam ={}
	leagueByTeamId =[]
	teamDetail =[]
	league_id = 0
	final_h2h ={}
	fixtures = MatchFixtureUpdate.objects.all().filter(matchid=match_id)
	result = MatchFixtureUpdateSerializer(fixtures, many=True).data
	win_tot=0
	win =[]
	goal_for_tot=0
	goals_against_tot=0
	goal_for =[]
	goals_against =[]
	for index, item in enumerate(result):
		req_data = {}
		item['localPlayer'] = GetPlayerByteamId(item["localteam_id"])
		item['visiterPlayer'] = GetPlayerByteamId(item["visitorteam_id"])
		league_id = item["league_id"]
		league_res = GetLeagueByLeagueId(item["league_id"])
		item['league_response'] = league_res
		local_team_id_res = GetTimeSessionByteamId(item["localteam_id"])
		# print(local_team_id_res['teams'][0]['name'])
		localteam ['name'] = local_team_id_res['teams'][0]['name']
		localteam ['logo_path'] = local_team_id_res['teams'][0]['logo_path']
		item['local_team_id_response'] =local_team_id_res
		visitorteam_id_res = GetTimeSessionByteamId(item["visitorteam_id"])
		visiterteam ['name'] = visitorteam_id_res['teams'][0]['name']
		visiterteam ['logo_path'] = visitorteam_id_res['teams'][0]['logo_path']
		item['visiterteamisitorteam_id_response'] =visitorteam_id_res
		
		item['new_date'] =json.loads(item['time'])
		# print(item['new_date'])
		if 'venue_id' in item:
			item['venue']=GetVenueById(item["venue_id"])
		if item["winnerteam_id"] == item["localteam_id"]:
			item['winner_team'] =local_team_id_res
			# req_data.update({"winner_team": local_team_id_response})
		elif item["winnerteam_id"] == item["visitorteam_id"]:
			item['winner_team'] =visitorteam_id_res

			# req_data.update({"winner_team": visitorteam_id_response})
		else:
			item['winner_team'] = None
		
		final_res.append(item)
		# print(item['localteam_id'])
		# print(item['visitorteam_id'])
		# print(league_id)
		fixtures = MatchFixtureUpdate.objects.all().filter(league_id=league_id).order_by('-id')[:10]
		for rec in fixtures:
			leagueByTeamId.append(rec.localteam_id)
			leagueByTeamId.append(rec.visitorteam_id)

		# print(leagueByTeamId)
		releted_teams = Teams.objects.all().filter(team_id__in=leagueByTeamId)[:10]
		teambyleague_result = TeamAndTeamStatisticsDetailSerializer(releted_teams, many=True).data
		for res in teambyleague_result:
			totmatch =0
			for splt in res['teamdetail']:
				totmatch =0
				win= json.loads(splt['win'])
				draw= json.loads(splt['draw'])
				lost= json.loads(splt['lost'])
				goals_for = json.loads(splt['goals_for'])
				goals_against = json.loads(splt['goals_against'])
				avg_goals_per_game_scored = json.loads(splt['avg_goals_per_game_scored'])
				if win['total']:
					# print(win)
					win_tot =win['total']
					totmatch = totmatch + int(win['total'])
				if draw['total']:
					# print(draw)
					totmatch =totmatch + int(draw['total'])

				if draw['total']:
					# print(lost)
					totmatch =totmatch + int(lost['total'])
				if goal_for:
					goal_for_tot = goals_for['total']
				if goals_against:
					goals_against_tot = goals_against['total']

			teamDetail.append({'name':res['name'],'totmatch':totmatch,'win':win_tot,'goal_for':goal_for_tot,'goals_against':goals_against_tot})
	return render(request,'../templates/ltr/tableData.html',{'match_id':match_id,'final_res':final_res,'headtohead':headtohead,'localteam':localteam,'visiterteam':visiterteam,'teamDetail':teamDetail})

@csrf_exempt
def OddsData(request,match_id):
	headtohead=[]
	final_res = []
	localteam ={}
	visiterteam ={}
	leagueByTeamId =[]
	teamDetail =[]
	league_id = 0
	final_h2h ={}
	fixtures = MatchFixtureUpdate.objects.all().filter(matchid=match_id)
	result = MatchFixtureUpdateSerializer(fixtures, many=True).data
	win_tot=0
	win =[]
	goal_for_tot=0
	goals_against_tot=0
	goal_for =[]
	goals_against =[]
	for index, item in enumerate(result):
		req_data = {}
		item['localPlayer'] = GetPlayerByteamId(item["localteam_id"])
		item['visiterPlayer'] = GetPlayerByteamId(item["visitorteam_id"])
		league_id = item["league_id"]
		league_res = GetLeagueByLeagueId(item["league_id"])
		item['league_response'] = league_res
		local_team_id_res = GetTimeSessionByteamId(item["localteam_id"])
		# print(local_team_id_res['teams'][0]['name'])
		localteam ['name'] = local_team_id_res['teams'][0]['name']
		localteam ['logo_path'] = local_team_id_res['teams'][0]['logo_path']
		item['local_team_id_response'] =local_team_id_res
		visitorteam_id_res = GetTimeSessionByteamId(item["visitorteam_id"])
		visiterteam ['name'] = visitorteam_id_res['teams'][0]['name']
		visiterteam ['logo_path'] = visitorteam_id_res['teams'][0]['logo_path']
		item['visiterteamisitorteam_id_response'] =visitorteam_id_res
		
		item['new_date'] =json.loads(item['time'])
		# print(item['new_date'])
		if 'venue_id' in item:
			item['venue']=GetVenueById(item["venue_id"])
		if item["winnerteam_id"] == item["localteam_id"]:
			item['winner_team'] =local_team_id_res
			# req_data.update({"winner_team": local_team_id_response})
		elif item["winnerteam_id"] == item["visitorteam_id"]:
			item['winner_team'] =visitorteam_id_res

			# req_data.update({"winner_team": visitorteam_id_response})
		else:
			item['winner_team'] = None
		
		final_res.append(item)
		# print(item['localteam_id'])
		# print(item['visitorteam_id'])
		# print(league_id)
		fixtures = MatchFixtureUpdate.objects.all().filter(league_id=league_id).order_by('-id')[:10]
		for rec in fixtures:
			leagueByTeamId.append(rec.localteam_id)
			leagueByTeamId.append(rec.visitorteam_id)

		# print(leagueByTeamId)
		releted_teams = Teams.objects.all().filter(team_id__in=leagueByTeamId)[:10]
		teambyleague_result = TeamAndTeamStatisticsDetailSerializer(releted_teams, many=True).data
		for res in teambyleague_result:
			totmatch =0
			for splt in res['teamdetail']:
				totmatch =0
				win= json.loads(splt['win'])
				draw= json.loads(splt['draw'])
				lost= json.loads(splt['lost'])
				goals_for = json.loads(splt['goals_for'])
				goals_against = json.loads(splt['goals_against'])
				avg_goals_per_game_scored = json.loads(splt['avg_goals_per_game_scored'])
				if win['total']:
					# print(win)
					win_tot =win['total']
					totmatch = totmatch + int(win['total'])
				if draw['total']:
					# print(draw)
					totmatch =totmatch + int(draw['total'])

				if draw['total']:
					# print(lost)
					totmatch =totmatch + int(lost['total'])
				if goal_for:
					goal_for_tot = goals_for['total']
				if goals_against:
					goals_against_tot = goals_against['total']

			teamDetail.append({'name':res['name'],'totmatch':totmatch,'win':win_tot,'goal_for':goal_for_tot,'goals_against':goals_against_tot})
	return render(request,'../templates/ltr/OddsData.html',{'match_id':match_id,'final_res':final_res,'headtohead':headtohead,'localteam':localteam,'visiterteam':visiterteam,'teamDetail':teamDetail})

@csrf_exempt
def TeamList(request):
	result =[]
	start_limit =15
	end_limit =30
	league_ids= LeagueIdGolaServe()
	league_search = request.GET.get('league', '')
	league = LeagueGoalserve.objects.all().filter(league_id__in=league_ids)
	league_detail = LeagueGoalserveSerializer(league, many=True).data
	if league_search:
		# print(season_search)
		team = TeamStatisticsGoalserve.objects.all().filter(league_ids__contains=league_search)
	else:
		team = TeamStatisticsGoalserve.objects.all().filter(league_ids__contains=1204)
	
	if team:
		result = TeamStatisticsGoalserveSerializer(team, many=True).data
	
	return render(request,'../templates/ltr/TeamList.html',{"result":result,"league_detail":league_detail,'league_search':league_search})

@csrf_exempt
def ViewTeamStatistics(request,team_id):
	team = TeamStatisticsGoalserve.objects.all().filter(team_id=team_id)[:1]
	result = TeamStatisticsGoalserveSerializer(team, many=True).data
	return render(request,'../templates/ltr/TeamStatistics.html',{'final_result':result,'result':result[0],'team_id':team_id})

@csrf_exempt
def LeagueList(request):

	# SaveLeaguetoLeagueOtherSource()
	league_search = request.GET.get('league', '')
	league = LeagueGoalserve.objects.all().filter()
	if league_search == '1':
		# print(league_search)
		league = LeagueGoalserve.objects.all().filter(is_active=True)
	if league_search == '0':
		league = LeagueGoalserve.objects.all().filter(is_active=False)
	league_detail = LeagueGoalserveSerializer(league, many=True).data
	return render(request,'../templates/ltr/LeagueList.html',{"league_search":league_search,"league_detail":league_detail})
@csrf_exempt
def LeagueAction(request):

	if request.POST:
		# print(request.POST['action'])
		# print(request.POST)
		data = LeagueGoalserve.objects.get(league_id=request.POST['id'])
		if request.POST['action'] == 'active':
			data.is_active = True 
		if request.POST['action'] == 'inactive':
			data.is_active = False 
			# print(data)
		data.save()
	return HttpResponseRedirect('/admin/db_table/LeagueList')

@csrf_exempt
def squardList(request):
	start_limit =15
	end_limit =30
	# SaveLeaguetoLeagueOtherSource()
	league_ids= LeagueIdGolaServe()
	league_search = request.GET.get('league', '')
	team_search= request.GET.get('team', '')
	league = LeagueGoalserve.objects.all().filter(league_id__in=league_ids)
	league_detail = LeagueGoalserveSerializer(league, many=True).data
	team = TeamStatisticsGoalserve.objects.all().filter(league_ids__contains=1204)
	team_detail = TeamStatisticsGoalserveSerializer(team, many=True).data
	league_detail = LeagueGoalserveSerializer(league, many=True).data
	league_search = request.GET.get('league', '')
	player = PlayerGoalserve.objects.all().filter()
	if team_search:
		# print(season_search)
		player = PlayerGoalserve.objects.all().filter(team_id=team_search)
	player_detail = PlayerGoalserveSerializer(player, many=True).data
	return render(request,'../templates/ltr/squardList.html',{"league_search":league_search,"team_search":team_search,"player_detail":player_detail,'league_detail':league_detail,'team_detail':team_detail})
@csrf_exempt
def FixtureList(request):
	result =[]
	start_limit =15
	end_limit =30
	league_search =''
	# SaveLeaguetoLeagueOtherSource()
	if 'League' in request.POST and request.POST['League'] !='':
		league =  request.POST['League']
		if league_search:
			# print(league_search)
			league = Leagues.objects.all().filter(name__contains='league_search')
		# league_detail = AllLeagueSerializer(league, many=True).data
	fixtures = MatchFixtureUpdate.objects.all().filter().order_by('-id')[:15]
	# result = MatchFixtureUpdateSerializer(fixtures, many=True).data
	for item in fixtures:
		# print(item.matchid)
		league_name =''
		country_name =''
		season_name = ''
		local_team_name =''
		visiter_team_name =''
		winner_team_name =''
		req_data = {}
		league  = GetLeagueByLeagueId(item.league_id)
		if league:
			league_name = league[0]['name']
			country_name = league[0]['country']['country_name']
		# print(league[0]['country']['country_name'])
		season = AllSeason.objects.all().filter(season_id=item.season_id).first()
		if season:
			season_name= season.name
		localteam = Teams.objects.all().filter(~Q(collection_datasource="www.worldfootball.net"),team_id=item.localteam_id).first()
		if localteam:
			local_team_name =localteam.name
		visitorteam = Teams.objects.all().filter(~Q(collection_datasource="www.worldfootball.net"),team_id=item.visitorteam_id).first()
		if visitorteam:
			visiter_team_name =visitorteam.name
		if item.winnerteam_id:
			if item.winnerteam_id == item.localteam_id:
				winner_team_name =localteam.name
			if item.winnerteam_id == item.visitorteam_id:
				winner_team_name =visitorteam.name
		result.append({
			'matchid':item.matchid,
			'league_name':league_name,
			'country_name':country_name,
			'season_name':season_name,
			'local_team_name':local_team_name,
			'visiter_team_name':visiter_team_name,
			'winner_team_name':winner_team_name,
			})
		# print(result)
		# print("---------------------")	
	return render(request,'../templates/ltr/FixtureList.html',{"league_search":league_search,"result":result,'start_limit':start_limit,'end_limit':end_limit})

@csrf_exempt
def UserList(request):
	user_search =''
	start_limit =15
	end_limit =30
	# SaveLeaguetoLeagueOtherSource()
	
	user = Users.objects.all().filter(is_superuser=False)
	user_detail = UserSerializer(user, many=True).data
	return render(request,'../templates/ltr/UserList.html',{"user_search":user_search,"user_detail":user_detail,'start_limit':start_limit,'end_limit':end_limit})


@csrf_exempt
def UserDetail(request,user_id):
	user_search =''
	start_limit =15
	end_limit =30
	# SaveLeaguetoLeagueOtherSource()
	
	user = Users.objects.all().filter(id=user_id)
	user_detail = UserSerializer(user, many=True).data
	return render(request,'../templates/ltr/UserDetail.html',{"user_search":user_search,"user_detail":user_detail[0],'start_limit':start_limit,'end_limit':end_limit})

@csrf_exempt
def NewsList(request):
	blog = Blogs.objects.all().filter(is_deleted=False)
	news = BlogsSerializer(blog, many=True).data
	return render(request,'../templates/ltr/NewsList.html',{"news":news})

@csrf_exempt
def NewsAction(request):

	if request.POST:
		# print(request.POST['action'])
		# print(request.POST)
		data = Blogs.objects.get(id=request.POST['id'])
		if request.POST['action'] == 'delete':
			data.is_deleted = True
			# print(data)
		if request.POST['action'] == 'publish':
			data.is_published = True 
		if request.POST['action'] == 'unpublish':
			data.is_published = False 
			# print(data)
		data.save()
	return HttpResponseRedirect('/admin/db_table/NewsList')

@csrf_exempt
def NewsDetail(request,news_id):
	user_search =''
	start_limit =15
	end_limit =30
	# SaveLeaguetoLeagueOtherSource()
	
	blog = Blogs.objects.all().filter(id=news_id)
	user_detail = BlogsSerializer(user, many=True).data
	return render(request,'../templates/ltr/NewsDetail.html',{"user_search":user_search,"user_detail":user_detail[0],'start_limit':start_limit,'end_limit':end_limit})

@csrf_exempt
def EditNews(request,news_id):
	user_search =''
	start_limit =15
	end_limit =30
	# SaveLeaguetoLeagueOtherSource()
	
	blog = Blogs.objects.all().filter(id=news_id)
	user_detail = BlogsSerializer(blog, many=True).data
	return render(request,'../templates/ltr/addNews.html',{"news":user_detail[0]})

@csrf_exempt
def addNews(request):
	message=''
	news=[]
	if request.POST:
		print(request.POST['title'])
		id =request.POST['id']
		title = request.POST['title']
		
		description = request.POST['description']
		meta_title = request.POST['meta_title']
		meta_key = request.POST['meta_key']
		meta_description = request.POST['meta_description']
		if request.POST['id'] !='':
			data = Blogs.objects.get(id=request.POST['id'])
			data.title = title
			data.description = description,
			data.meta_title = meta_title,
			data.meta_key =meta_key,
			data.meta_description = meta_description
			data.save()
			message='Data Updated Successfully'
		else:
			slug = slug_generatorNews(request.POST['title'])
			blug = Blogs.objects.create(
				title = title,
				slug = slug,
				description = description,
				meta_title = meta_title,
				meta_key =meta_key,
				meta_description = meta_description
			)
			message='Data Saved Successfully'
	return render(request,'../templates/ltr/addNews.html',{'message':message,"news":[]})

def slug_generatorNews(scrapname,new_slug = None): 
    if new_slug is not None: 
        slug = new_slug 
    else: 
        slug = slugify(scrapname) 
    qs_exists = Blogs.objects.filter(slug = slug).exists() 
      
    if qs_exists: 
        new_slug = "{slug}-{randstr}".format( 
            slug = slug, randstr = random_string_generator(size = 4)) 
              
        return slug_generator(scrapname, new_slug = new_slug) 
    return slug

def slug_generatorCms(scrapname,new_slug = None): 
    if new_slug is not None: 
        slug = new_slug 
    else: 
        slug = slugify(scrapname) 
    qs_exists = Cms.objects.filter(slug = slug).exists() 
      
    if qs_exists: 
        new_slug = "{slug}-{randstr}".format( 
            slug = slug, randstr = random_string_generator(size = 4)) 
              
        return slug_generator(scrapname, new_slug = new_slug) 
    return slug

@csrf_exempt
def CmsList(request):
	blog = Cms.objects.all().filter(is_deleted=False)
	news = CmsSerializer(blog, many=True).data
	return render(request,'../templates/ltr/CmsList.html',{"cms":news})

@csrf_exempt
def CmsDetail(request,cms_id):
	user_search =''
	start_limit =15
	end_limit =30
	# SaveLeaguetoLeagueOtherSource()
	
	blog = Cms.objects.all().filter(id=cms_id)
	user_detail = CmsSerializer(user, many=True).data
	return render(request,'../templates/ltr/CmsDetail.html',{"user_search":user_search,"user_detail":user_detail[0],'start_limit':start_limit,'end_limit':end_limit})

@csrf_exempt
def CmsAction(request):

	if request.POST:
		# print(request.POST['action'])
		print(request.POST)
		data = Cms.objects.get(id=request.POST['id'])
		if request.POST['action'] == 'delete':
			data.is_deleted = True
			print(data)
		if request.POST['action'] == 'publish':
			data.is_published = True 
		if request.POST['action'] == 'unpublish':
			data.is_published = False 
			print(data)
		data.save()
	return HttpResponseRedirect('/admin/db_table/CmsList')

@csrf_exempt
def EditCms(request,cms_id):
	user_search =''
	message=''
	start_limit =15
	end_limit =30
	# SaveLeaguetoLeagueOtherSource()
	
	blog = Cms.objects.all().filter(id=cms_id)
	user_detail = CmsSerializer(blog, many=True).data
	return render(request,'../templates/ltr/addCms.html',{'message':message,"cms":user_detail[0]})

@csrf_exempt
def addCms(request):
	message=''
	cms=[]
	if request.POST:
		print(request.POST['title'])
		id =request.POST['id']
		title = request.POST['title']
		description = request.POST['description']
		meta_title = request.POST['meta_title']
		meta_key = request.POST['meta_key']
		meta_description = request.POST['meta_description']
		if request.POST['id'] !='':
			data = Cms.objects.get(id=request.POST['id'])
			data.title = title
			data.description = description,
			data.meta_title = meta_title,
			data.meta_key =meta_key,
			data.meta_description = meta_description
			data.save()
			message='Data Updated Successfully'
		else:
			slug = slug_generatorCms(request.POST['title'])
			blug = Cms.objects.create(
				title = title,
				slug = slug,
				description = description,
				meta_title = meta_title,
				meta_key =meta_key,
				meta_description = meta_description
			)
			message='Data Saved Successfully'
	return render(request,'../templates/ltr/addCms.html',{'message':message,"cms":[]})


@csrf_exempt
def AffiliateList(request):
	user_search =''
	start_limit =15
	end_limit =30
	# SaveLeaguetoLeagueOtherSource()
	
	user = AffiliateUser.objects.all()
	user_detail = AffiliateUserSerializer(user, many=True).data
	return render(request,'../templates/ltr/AffiliateList.html',{"user_search":user_search,"user_detail":user_detail,'start_limit':start_limit,'end_limit':end_limit})

@csrf_exempt
def AffiliateDetail(request,user_id):
	user_search =''
	start_limit =15
	end_limit =30
	# SaveLeaguetoLeagueOtherSource()
	
	user = AffiliateUser.objects.all().filter(id=user_id)
	user_detail = AffiliateUserSerializer(user, many=True).data
	return render(request,'../templates/ltr/AffiliateDetail.html',{"user_search":user_search,"user_detail":user_detail[0],'start_limit':start_limit,'end_limit':end_limit})

@csrf_exempt
def AffiliateAction(request):

	if request.POST:
		# print(request.POST['action'])
		print(request.POST)
		data = AffiliateUser.objects.get(id=request.POST['id'])
		if request.POST['action'] == 'active':
			data.is_active = True 
		if request.POST['action'] == 'inactive':
			data.is_active = False 
			print(data)
		data.save()
	return HttpResponseRedirect('/admin/db_table/AffiliateList')

@csrf_exempt
def EditAffiliate(request,user_id):
	user_search =''
	message=''
	start_limit =15
	end_limit =30
	# SaveLeaguetoLeagueOtherSource()
	
	blog = AffiliateUser.objects.all().filter(id=user_id)
	user_detail = AffiliateUserSerializer(blog, many=True).data

	return render(request,'../templates/ltr/addAffiliate.html',{'error_message':'','success_message':'',"affiliate":user_detail[0]})

@csrf_exempt
def addAffiliate(request):
	success_message=''
	error_message =''
	affiliate=[]
	if request.POST:
		print(request.POST)
		id =request.POST['id']
		name = request.POST['name']
		email = request.POST['email']
		country = request.POST['country']
		phone = request.POST['phone']
		password =  make_password(request.POST['password'])
		confpassword = make_password(request.POST['confirm_password'])
		print(password)
		print(confpassword)
		if request.POST['id'] !='':
			# if password == confpassword:
			data = AffiliateUser.objects.get(id=request.POST['id'])
			data.name = name
			data.email = email,
			data.country = country,
			data.phone = phone,
			data.password =password,
			data.confirm_password = confpassword,
			data.save()
			success_message='Data Updated Successfully'
			# else:
			# 	error_message = 'Password and Confirm Password Not Match'
		else:
			# if password == confpassword:
			print(request.POST)
			blug = AffiliateUser.objects.create(
				name = name,
				email = email,
				country = country,
				phone = phone,
				password =password,
				confirm_password = confpassword
			)
			success_message='Data Saved Successfully'
			# else:
			# 	error_message = 'Password and Confirm Password Not Match'
	return render(request,'../templates/ltr/addAffiliate.html',{'error_message':error_message,'success_message':success_message,"affiliate":[]})

@csrf_exempt
def ViewSquardStatistics(request,player_id):
	result=[]
	statistic_popular_intl_club =[]
	transfers =[]
	statistic_international_club =[]
	statistic_popular_intl_club_season=[]
	statistic_popular_intl_clubGoal=[]
	statistic_international_club_season=[]
	statistic_international_clubGoal=[]
	team = PlayerStatisticsGoalserve.objects.all().filter(player_id=player_id)[:1]
	if team:
		# print(team[0].statistic_popular_intl_club)
		if team[0].statistic_popular_intl_club:
			statistic_popular_intl_club = json.loads(team[0].statistic_popular_intl_club)
			# print(statistic_popular_intl_club)
			for item in statistic_popular_intl_club['club']:
				# print(item)
				statistic_popular_intl_club_season.append(item['season'])
				statistic_popular_intl_clubGoal.append(item['goals'])

		if team[0].transfers:
			transfers = json.loads(team[0].transfers)
		
		if team[0].statistic_international_club:
			statistic_international_club = json.loads(team[0].statistic_international_club)
			for item in statistic_popular_intl_club['club']:
				# print(item)
				statistic_international_club_season.append(item['season'])
				statistic_international_clubGoal.append(item['goals'])

		result = PlayerStatisticsGoalserveSerializer(team, many=True).data
	# print(transfers)
	return render(request,'../templates/ltr/playerStatistics.html',{
		'statistic_popular_intl_club':statistic_popular_intl_club['club'],
		'statistic_international_club':statistic_international_club['club'],
		'transfers':transfers,
		'result':result[0],
		'player_id':player_id,
		'statistic_popular_intl_club_season': ",".join(str(x) for x in statistic_popular_intl_club_season),
		'statistic_popular_intl_clubGoal':",".join(str(k) for k in statistic_popular_intl_clubGoal),
		'statistic_international_club_season':statistic_international_club_season,
		'statistic_international_clubGoal':statistic_international_clubGoal,
		}
	)

@csrf_exempt
def SubscriptionList(request):
	user_search =''
	start_limit =15
	end_limit =30
	# SaveLeaguetoLeagueOtherSource()
	subscription = Subscriptions.objects.all()
	Subscriptions_detail = SubscriptionSerializer(subscription, many=True).data
	return render(request,'../templates/ltr/SubscriptionList.html',{"user_search":user_search,"subscriptions_detail":Subscriptions_detail,'start_limit':start_limit,'end_limit':end_limit})

@csrf_exempt
def SubscriptionsDetail(request,subscription_id):
	user_search =''
	start_limit =15
	end_limit =30
	# SaveLeaguetoLeagueOtherSource()
	
	Subscriptions = Subscriptions.objects.all().filter(id=subscription_id)
	Subscriptions_detail = SubscriptionsSerializer(Subscriptions, many=True).data
	return render(request,'../templates/ltr/SubscriptionsDetail.html',{"user_search":user_search,"subscriptions_detail":Subscriptions_detail[0],'start_limit':start_limit,'end_limit':end_limit})

@csrf_exempt
def SubscriptionsAction(request):

	if request.POST:
		# print(request.POST['action'])
		print(request.POST)
		if request.POST['action'] == 'active':
			updt = Subscriptions.objects.filter(id__gte=1).update(is_active=False)
			updt = Subscriptions.objects.filter(id=request.POST['id']).update(is_active=True)
			
		if request.POST['action'] == 'inactive':
			updt = Subscriptions.objects.filter(id=request.POST['id']).update(is_active=False)
	return HttpResponseRedirect('/admin/db_table/SubscriptionList')

@csrf_exempt
def EditSubscriptions(request,subscription_id):
	user_search =''
	message=''
	start_limit =15
	end_limit =30
	# SaveLeaguetoLeagueOtherSource()
	
	blog = Subscriptions.objects.all().filter(id=subscription_id)
	subscription_detail = SubscriptionSerializer(blog, many=True).data

	return render(request,'../templates/ltr/addSubscriptions.html',{'error_message':'','success_message':'',"subscription":subscription_detail[0]})

@csrf_exempt
def addSubscriptions(request):
	success_message=''
	error_message =''
	subscription=[]
	if request.POST:
		print(request.POST)
		id =request.POST['id']
		name = request.POST['name']
		price = request.POST['price']
		if request.POST['id'] !='':
			# if password == confpassword:
			data = Subscriptions.objects.get(id=request.POST['id'])
			data.name = name,
			data.price = int(price)
			data.save()
			success_message='Data Updated Successfully'
			# else:
			# 	error_message = 'Password and Confirm Password Not Match'
		else:
			# if password == confpassword:
			print(request.POST)
			blug = Subscriptions.objects.create(
				name = name,
				price = price,
			)
			success_message='Data Saved Successfully'
			# else:
			# 	error_message = 'Password and Confirm Password Not Match'
	return render(request,'../templates/ltr/addSubscriptions.html',{'error_message':error_message,'success_message':success_message,"subscription":[]})

@csrf_exempt
def PaymentList(request):
	user_search =''
	
	payment = UserSubscriptionPayment.objects.all()
	payment_detail = UserSubscriptionPaymentSerializer(payment, many=True).data
	return render(request,'../templates/ltr/PaymentList.html',{"payment_detail":payment_detail})

@csrf_exempt
def PaymentDetail(request,payment_id):
	Subscriptions = UserSubscriptionPayment.objects.all().filter(id=payment_id)
	Subscriptions_detail = UserSubscriptionPaymentSerializer(Subscriptions, many=True).data
	return render(request,'../templates/ltr/PaymentDetail.html',{"payment_detail":Subscriptions_detail[0]})


@csrf_exempt
def PredictionList(request):
	user_search =''
	queryObj = {}
	if request.POST:
		print(request.POST)
		if 'League' in request.POST and request.POST['League'] !='':
			queryObj['league_id'] =  request.POST['League']
			
		if 'fromdate' in request.POST and request.POST['fromdate'] !='':
			date2 = request.POST['fromdate']
			queryObj['formated_date__lte'] = request.POST['fromdate']

		if 'todate' in request.POST and request.POST['todate'] !='':
			queryObj['formated_date__gte'] = request.POST['todate']
	print(queryObj)
	prediction = predictionH2HOddsGoalserve.objects.all().filter(**queryObj)
	# predictionH2HOddsGoalserveSerializer
	league=GatAllActiveLeagueByGoalServe()
	
	return render(request,'../templates/ltr/PredictionList.html',{"prediction":prediction,'league':league})

@csrf_exempt
def PredictionDetail(request,match_id):
	prediction = predictionH2HOddsGoalserve.objects.all().filter(match_id=match_id)
	prediction_detail =predictionH2HOddsGoalserveSerializer(prediction,many=True).data
	return render(request,'../templates/ltr/PredictionDetail.html',{"prediction":prediction_detail[0]})

@csrf_exempt
def BannerList(request):
	banner = Banner.objects.all()
	Banner_detail = BannerSerializer(banner, many=True).data
	return render(request,'../templates/ltr/BannerList.html',{"Banner_detail":Banner_detail})

@csrf_exempt
def BannerAction(request):

	if request.POST:
		# print(request.POST['action'])
		print(request.POST)
		data = Banner.objects.get(id=request.POST['id'])
		if request.POST['action'] == 'delete':
			data.is_delete = True 
			print(data)
		if request.POST['action'] == 'publish':
			data.is_active = True 
			data.save()
		if request.POST['action'] == 'unpublish':
			data.is_active = False 
			print(data)
			data.save()
	return HttpResponseRedirect('/admin/db_table/BannerList')

@csrf_exempt
def EditBanner(request,slug):
	user_search =''
	message=''
	start_limit =15
	end_limit =30
	# SaveLeaguetoLeagueOtherSource()
	
	banner = Banner.objects.all().filter(slug=slug)
	banner_detail = BannerSerializer(banner, many=True).data

	return render(request,'../templates/ltr/addBanner.html',{'error_message':'','success_message':'',"banner_detail":banner_detail[0]})

@csrf_exempt
def addBanner(request):
	success_message=''
	error_message =''
	affiliate=[]

	if request.POST:
		# print(request.POST)
		
		title = request.POST['title']
		description = request.POST['description']
		image = request.FILES['image']
		
		if request.POST['id'] !='':
			# if password == confpassword:
			data = Banner.objects.get(id=request.POST['id'])
			data.title = title
			data.description = description,
			data.image = image,
			data.save()
			success_message='Data Updated Successfully'
			# else:
			# 	error_message = 'Password and Confirm Password Not Match'
		else:
			# if password == confpassword:
			# print(request.POST)
			slug = slug_generatorBanner(request.POST['title'])
			blug = Banner.objects.create(
				title = title,
				description = description,
				slug = slug,
				image = image,
				id=Banner.objects.count() + 1
			)
			success_message='Data Saved Successfully'
			# else:
			# 	error_message = 'Password and Confirm Password Not Match'
	return render(request,'../templates/ltr/addBanner.html',{'error_message':error_message,'success_message':success_message,"banner_detail":[]})
def slug_generatorBanner(scrapname,new_slug = None): 
    if new_slug is not None: 
        slug = new_slug 
    else: 
        slug = slugify(scrapname) 
    qs_exists = Banner.objects.filter(slug = slug).exists() 
      
    if qs_exists: 
        new_slug = "{slug}-{randstr}".format( 
            slug = slug, randstr = random_string_generator(size = 4)) 
              
        return slug_generatorBanner(scrapname, new_slug = new_slug) 
    return slug

@csrf_exempt
def NotificationList(request):
	banner = Notification.objects.all()
	Notification_detail = NotificationSerializer(banner, many=True).data
	return render(request,'../templates/ltr/NotificationList.html',{"Notification_detail":Notification_detail})

@csrf_exempt
def NotificationAction(request):

	if request.POST:
		# print(request.POST['action'])
		print(request.POST)
		data = Notification.objects.get(id=request.POST['id'])
		data.is_delete = True 
		data.save()
	return HttpResponseRedirect('/admin/db_table/NotificationList')

@csrf_exempt
def addNotification(request):
	success_message=''
	error_message =''
	if request.POST:
		# print(request.POST)
		title = request.POST['title']
		description = request.POST['description']
		if request.POST['id'] !='':
			# if password == confpassword:
			data = Notification.objects.get(id=request.POST['id'])
			data.title = title
			data.description = description,
			data.save()
			success_message='Data Updated Successfully'
			# else:
			# 	error_message = 'Password and Confirm Password Not Match'
		else:
			slug =slug_generatorNotification(title)
			blug = Notification.objects.create(
				title = title,
				description = description,
				id=Notification.objects.count() + 1
			)
			success_message='Data Saved Successfully'
	return render(request,'../templates/ltr/addNotification.html',{'error_message':error_message,'success_message':success_message,"notification_detail":[]})

@csrf_exempt
def EditNotification(request,slug):
	user_search =''
	message=''
	banner = Notification.objects.all().filter(slug=slug)
	banner_detail = NotificationSerializer(banner, many=True).data

	return render(request,'../templates/ltr/addNotification.html',{'error_message':'','success_message':'',"notification_detail":banner_detail[0]})

def slug_generatorNotification(scrapname,new_slug = None): 
    if new_slug is not None: 
        slug = new_slug 
    else: 
        slug = slugify(scrapname) 
    qs_exists = Notification.objects.filter(slug = slug).exists() 
      
    if qs_exists: 
        new_slug = "{slug}-{randstr}".format( 
            slug = slug, randstr = random_string_generator(size = 4)) 
              
        return slug_generatorNotification(scrapname, new_slug = new_slug) 
    return slug

@csrf_exempt
def MessageList(request):
	current_user = request.user
	# print(current_user.id)
	sender_ids=[]
	message_ids=[]
	ad_ids_array =Message.objects.filter(Q(sender_id=current_user.id) | Q(receiver_id=current_user.id))
	for msg in ad_ids_array :
		print(msg.sender_id)
		if msg.sender_id not in sender_ids:
			if msg.sender_id != current_user.id:
				sender_ids.append(msg.sender_id)
				message_ids.append(msg.id)

	message =Message.objects.filter(id__in=message_ids).order_by('-id')
	detail = MessageSerializer(message, many=True).data
	return render(request,'../templates/ltr/MessageList.html',{"message_detail":detail})

@csrf_exempt
def chat(request,sender_id,receiver_id):
	recipant_id = 0
	current_user = request.user
	if current_user.id != sender_id :
		recipant_id = sender_id
	else:
		recipant_id = receiver_id
	recipant = Users.objects.all().filter(id=recipant_id).first()
	message =Message.objects.filter( \
                                    Q(\
                                        sender_id=sender_id, \
                                        receiver_id=receiver_id \
                                    ) | \
                                    Q(
                                        sender_id=receiver_id, \
                                        receiver_id=sender_id \
                                    )\
                                )
	detail = MessageSerializer(message, many=True).data

	return render(request,'../templates/ltr/chat.html',
		{
			'detail':detail,
			'recipant_id':recipant_id,
			'recipant':recipant,
			'current_user_id':current_user.id,

		}
	)

@csrf_exempt
def UploadCsv(request):
	success_message=''
	error_message =''
	csv_detail =[]
	if request.POST:
		league = request.POST['league']
		csv_file = request.FILES['csv_file']
		
		if request.POST['id'] !='':
			# if password == confpassword:
			data = UploadCSV.objects.get(id=request.POST['id'])
			data.league = league
			data.csv_file = csv_file,
			data.save()
			success_message='Data Updated Successfully'
			
		else:
			blug = UploadCSV.objects.create(
				league = league,
				csv_file = csv_file,
				id=UploadCSV.objects.count() + 1
			)
			success_message='Data Saved Successfully'
			
	return render(request,'../templates/ltr/UploadCSV.html',{'error_message':error_message,'success_message':success_message,"csv_detail":[]})
	

@csrf_exempt
def CsvList(request):
	detail =UploadCSV.objects.filter(is_deleted=False).all()
	return render(request,'../templates/ltr/CsvList.html',{"csv_detail":detail,'success_message':'','error_message':''})

@csrf_exempt
def EditCsv(request,id):
	
	csv = UploadCSV.objects.all().filter(id=id)
	csv_detail = UploadCSVSerializer(csv, many=True).data

	return render(request,'../templates/ltr/UploadCSV.html',{'error_message':'','success_message':'',"csv_detail":csv_detail[0]})

@csrf_exempt
def PocessCSV(request,id):
	success_message =''
	error_message =''
	csv = UploadCSV.objects.all().filter(id=id)
	csv_detail = UploadCSVSerializer(csv, many=True).data
	csv_url = str(SITEURL)+':8000'+str(csv_detail[0]['csv_file'])
	# print(csv_url)
	import requests
	import json
	url = AIMODELURL+"uploadcsv/"
	payload = json.dumps({
		"Url": "https://www.football-data.co.uk/mmz4281/2122/E0.csv"
	})
	headers = {
		'Content-Type': 'application/json'
	}
	response = requests.request("POST", url, headers=headers, data=payload)
	res = json.dumps(json.loads(response.text), indent=3)
	json_res = json.loads(res)
	if json_res['status'] == 200:
		csv.is_process = True,
		csv.save()
		success_message = json_res['message']
	else:
		error_message = json_res['message']
	print(json_res['status'])
	return HttpResponseRedirect('/admin/db_table/CsvList')

@csrf_exempt
def Uploadexcel(request):
	success_message=''
	error_message =''
	csv_detail =[]
	if request.POST:
		league = request.POST['league']
		excel_file = request.FILES['excel_file']
		
		if request.POST['id'] !='':
			# if password == confpassword:
			data = UploadExcel.objects.get(id=request.POST['id'])
			data.league = league
			data.excel_file = excel_file,
			data.save()
			success_message='Data Updated Successfully'
			
		else:

			blug = UploadExcel.objects.create(
				league = league,
				excel_file = excel_file,
				id=UploadExcel.objects.count() + 1
			)
			print(blug)
			success_message='Data Saved Successfully'
			
	return render(request,'../templates/ltr/UploadExcel.html',{'error_message':error_message,'success_message':success_message,"csv_detail":[]})
	

@csrf_exempt
def ExcelList(request):
	detail =UploadExcel.objects.filter(is_deleted=False).all()
	return render(request,'../templates/ltr/ExcelList.html',{"excel_detail":detail,'success_message':'','error_message':''})

@csrf_exempt
def EditExcel(request,id):
	
	csv = UploadExcel.objects.all().filter(id=id)
	csv_detail = UploadExcelSerializer(csv, many=True).data

	return render(request,'../templates/ltr/UploadExcel.html',{'error_message':'','success_message':'',"csv_detail":csv_detail[0]})


