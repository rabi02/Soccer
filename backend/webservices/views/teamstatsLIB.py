import requests
import json
from datetime import datetime
from webservices.views.BitfairLib import *
day_list = ['d1','d2','d3','d4','d5','d6','d7']
from django.utils.timezone import datetime #important if using timezones
import logging
import logging.handlers as handlers
def dateUTCFormat(dateStr):
	return datetime.strptime(dateStr, '%d.%m.%y').strftime('%Y-%m-%d')

def scoringPeriod(periods):
	periodList = []
	if type(periods) is dict:
		data = {
			'min': None if (periods.get("@min") is None) or (periods['@min'] is None) or (not periods['@min']) else periods['@min'],
			'pct': None if (periods.get("@pct") is None) or (periods['@pct'] is None) or (not periods['@pct']) else periods['@pct'],
			'count': None if (periods.get("@count") is None) or (periods['@count'] is None) or (not periods['@count']) else int(periods['@count'])
		}
		return [data]
	if type(periods) is list:
			for info in periods:
				data = {
					'min': None if (info.get("@min") is None) or (info['@min'] is None) or (not info['@min']) else info['@min'],
					'pct': None if (info.get("@pct") is None) or (info['@pct'] is None) or (not info['@pct']) else info['@pct'],
					'count': None if (info.get("@count") is None) or (info['@count'] is None) or (not info['@count']) else int(info['@count'])
				}
				periodList.append(data)
			return periodList

def leagues(leagues):
	league = []
	if type(leagues) is dict:
		data = int(leagues)
		return [data]
	if type(leagues) is list:
			for info in leagues:
				data = int(info)
				league.append(data)
			return league

def detailedStats(leagues):
	leaguelist = []
	if type(leagues) is dict:
		data = {
			'name': None if (leagues.get("@name") is None) or (leagues['@name'] is None) or (not leagues['@name']) else leagues['@name'],
			'season': None if (leagues.get("@season") is None) or (leagues['@season'] is None) or (not leagues['@season']) else leagues['@season'],
			'id': None if (leagues.get("@id") is None) or (leagues['@id'] is None) or (not leagues['@id']) else int(leagues['@id']),
			'fulltime': None if (leagues.get("fulltime") is None) or (leagues['fulltime'] is None) or (not leagues['fulltime']) else {
				'win': None if (leagues['fulltime'].get("win") is None) or (leagues['fulltime']['win'] is None) or (not leagues['fulltime']['win']) else {
					'total': None if (leagues['fulltime']['win'].get("@total") is None) or (leagues['fulltime']['win']['@total'] is None) or (not leagues['fulltime']['win']['@total']) else int(leagues['fulltime']['win']['@total']),
					'home': None if (leagues['fulltime']['win'].get("@home") is None) or (leagues['fulltime']['win']['@home'] is None) or (not leagues['fulltime']['win']['@home']) else int(leagues['fulltime']['win']['@home']),
					'away': None if (leagues['fulltime']['win'].get("@away") is None) or (leagues['fulltime']['win']['@away'] is None) or (not leagues['fulltime']['win']['@away']) else int(leagues['fulltime']['win']['@away'])
				},
				'lost': None if (leagues['fulltime'].get("lost") is None) or (leagues['fulltime']['lost'] is None) or (not leagues['fulltime']['lost']) else {
					'total': None if (leagues['fulltime']['lost'].get("@total") is None) or (leagues['fulltime']['lost']['@total'] is None) or (not leagues['fulltime']['lost']['@total']) else int(leagues['fulltime']['lost']['@total']),
					'home': None if (leagues['fulltime']['lost'].get("@home") is None) or (leagues['fulltime']['lost']['@home'] is None) or (not leagues['fulltime']['lost']['@home']) else int(leagues['fulltime']['lost']['@home']),
					'away': None if (leagues['fulltime']['lost'].get("@away") is None) or (leagues['fulltime']['lost']['@away'] is None) or (not leagues['fulltime']['lost']['@away']) else int(leagues['fulltime']['lost']['@away'])
				},
				'draw': None if(leagues['fulltime'].get("draw") is None) or  (leagues['fulltime']['draw'] is None) or (not leagues['fulltime']['draw']) else {
					'total': None if (leagues['fulltime']['draw'].get("@total") is None) or (leagues['fulltime']['draw']['@total'] is None) or (not leagues['fulltime']['draw']['@total']) else int(leagues['fulltime']['draw']['@total']),
					'home': None if (leagues['fulltime']['draw'].get("@home") is None) or (leagues['fulltime']['draw']['@home'] is None) or (not leagues['fulltime']['draw']['@home']) else int(leagues['fulltime']['draw']['@home']),
					'away': None if (leagues['fulltime']['draw'].get("@away") is None) or (leagues['fulltime']['draw']['@away'] is None) or (not leagues['fulltime']['draw']['@away']) else int(leagues['fulltime']['draw']['@away'])
				},
				'goals_for': None if (leagues['fulltime'].get("goals_for") is None) or (leagues['fulltime']['goals_for'] is None) or (not leagues['fulltime']['goals_for']) else {
					'total': None if (leagues['fulltime']['goals_for'].get("@total") is None) or (leagues['fulltime']['goals_for']['@total'] is None) or (not leagues['fulltime']['goals_for']['@total']) else int(leagues['fulltime']['goals_for']['@total']),
					'home': None if (leagues['fulltime']['goals_for'].get("@home") is None) or (leagues['fulltime']['goals_for']['@home'] is None) or (not leagues['fulltime']['goals_for']['@home']) else int(leagues['fulltime']['goals_for']['@home']),
					'away': None if (leagues['fulltime']['goals_for'].get("@away") is None) or (leagues['fulltime']['goals_for']['@away'] is None) or (not leagues['fulltime']['goals_for']['@away']) else int(leagues['fulltime']['goals_for']['@away'])
				},
				'goals_against': None if (leagues['fulltime'].get("goals_against") is None) or (leagues['fulltime']['goals_against'] is None) or (not leagues['fulltime']['goals_against']) else {
					'total': None if (leagues['fulltime']['goals_against'].get("@total") is None) or (leagues['fulltime']['goals_against']['@total'] is None) or (not leagues['fulltime']['goals_against']['@total']) else int(leagues['fulltime']['goals_against']['@total']),
					'home': None if (leagues['fulltime']['goals_against'].get("@home") is None) or (leagues['fulltime']['goals_against']['@home'] is None) or (not leagues['fulltime']['goals_against']['@home']) else int(leagues['fulltime']['goals_against']['@home']),
					'away': None if (leagues['fulltime']['goals_against'].get("@away") is None) or (leagues['fulltime']['goals_against']['@away'] is None) or (not leagues['fulltime']['goals_against']['@away']) else int(leagues['fulltime']['goals_against']['@away'])
				},
				'clean_sheet': None if (leagues['fulltime'].get("clean_sheet") is None) or (leagues['fulltime']['clean_sheet'] is None) or (not leagues['fulltime']['clean_sheet']) else {
					'total': None if (leagues['fulltime']['clean_sheet'].get("@total") is None) or (leagues['fulltime']['clean_sheet']['@total'] is None) or (not leagues['fulltime']['clean_sheet']['@total']) else int(leagues['fulltime']['clean_sheet']['@total']),
					'home': None if (leagues['fulltime']['clean_sheet'].get("@home") is None) or (leagues['fulltime']['clean_sheet']['@home'] is None) or (not leagues['fulltime']['clean_sheet']['@home']) else int(leagues['fulltime']['clean_sheet']['@home']),
					'away': None if (leagues['fulltime']['clean_sheet'].get("@away") is None) or (leagues['fulltime']['clean_sheet']['@away'] is None) or (not leagues['fulltime']['clean_sheet']['@away']) else int(leagues['fulltime']['clean_sheet']['@away'])
				},
				'avg_goals_per_game_scored': None if (leagues['fulltime'].get("avg_goals_per_game_scored") is None) or (leagues['fulltime']['avg_goals_per_game_scored'] is None) or (not leagues['fulltime']['avg_goals_per_game_scored']) else {
					'total': None if (leagues['fulltime']['avg_goals_per_game_scored'].get("@total") is None) or (leagues['fulltime']['avg_goals_per_game_scored']['@total'] is None) or (not leagues['fulltime']['avg_goals_per_game_scored']['@total']) else float(leagues['fulltime']['avg_goals_per_game_scored']['@total']),
					'home': None if (leagues['fulltime']['avg_goals_per_game_scored'].get("@home") is None) or (leagues['fulltime']['avg_goals_per_game_scored']['@home'] is None) or (not leagues['fulltime']['avg_goals_per_game_scored']['@home']) else float(leagues['fulltime']['avg_goals_per_game_scored']['@home']),
					'away': None if (leagues['fulltime']['avg_goals_per_game_scored'].get("@away") is None) or (leagues['fulltime']['avg_goals_per_game_scored']['@away'] is None) or (not leagues['fulltime']['avg_goals_per_game_scored']['@away']) else float(leagues['fulltime']['avg_goals_per_game_scored']['@away'])
				},
				'avg_goals_per_game_conceded': None if (leagues['fulltime'].get("avg_goals_per_game_conceded") is None) or (leagues['fulltime']['avg_goals_per_game_conceded'] is None) or (not leagues['fulltime']['avg_goals_per_game_conceded']) else {
					'total': None if (leagues['fulltime']['avg_goals_per_game_scored'].get("@total") is None) or (leagues['fulltime']['avg_goals_per_game_conceded']['@total'] is None) or (not leagues['fulltime']['avg_goals_per_game_conceded']['@total']) else float(leagues['fulltime']['avg_goals_per_game_conceded']['@total']),
					'home': None if (leagues['fulltime']['avg_goals_per_game_scored'].get("@home") is None) or (leagues['fulltime']['avg_goals_per_game_conceded']['@home'] is None) or (not leagues['fulltime']['avg_goals_per_game_conceded']['@home']) else float(leagues['fulltime']['avg_goals_per_game_conceded']['@home']),
					'away': None if (leagues['fulltime']['avg_goals_per_game_scored'].get("@away") is None) or (leagues['fulltime']['avg_goals_per_game_conceded']['@away'] is None) or (not leagues['fulltime']['avg_goals_per_game_conceded']['@away']) else float(leagues['fulltime']['avg_goals_per_game_conceded']['@away'])
				},
				'biggest_victory': None if (leagues['fulltime'].get("biggest_victory") is None) or (leagues['fulltime']['biggest_victory'] is None) or (not leagues['fulltime']['biggest_victory']) else {
					'total': None if (leagues['fulltime']['biggest_victory'].get("@total") is None) or (leagues['fulltime']['biggest_victory']['@total'] is None) or (not leagues['fulltime']['biggest_victory']['@total']) else leagues['fulltime']['biggest_victory']['@total'],
					'home': None if (leagues['fulltime']['biggest_victory'].get("@home") is None) or (leagues['fulltime']['biggest_victory']['@home'] is None) or (not leagues['fulltime']['biggest_victory']['@home']) else leagues['fulltime']['biggest_victory']['@home'],
					'away': None if (leagues['fulltime']['biggest_victory'].get("@away") is None) or (leagues['fulltime']['biggest_victory']['@away'] is None) or (not leagues['fulltime']['biggest_victory']['@away']) else leagues['fulltime']['biggest_victory']['@away']
				},
				'biggest_defeat': None if (leagues['fulltime'].get("biggest_defeat") is None) or (leagues['fulltime']['biggest_defeat'] is None) or (not leagues['fulltime']['biggest_defeat']) else {
					'total': None if (leagues['fulltime']['biggest_defeat'].get("@total") is None) or (leagues['fulltime']['biggest_defeat']['@total'] is None) or (not leagues['fulltime']['biggest_defeat']['@total']) else leagues['fulltime']['biggest_defeat']['@total'],
					'home': None if (leagues['fulltime']['biggest_defeat'].get("@home") is None) or (leagues['fulltime']['biggest_defeat']['@home'] is None) or (not leagues['fulltime']['biggest_defeat']['@home']) else leagues['fulltime']['biggest_defeat']['@home'],
					'away': None if (leagues['fulltime']['biggest_defeat'].get("@away") is None) or (leagues['fulltime']['biggest_defeat']['@away'] is None) or (not leagues['fulltime']['biggest_defeat']['@away']) else leagues['fulltime']['biggest_defeat']['@away']
				},
				'avg_first_goal_scored': None if (leagues['fulltime'].get("avg_first_goal_scored") is None) or (leagues['fulltime']['avg_first_goal_scored'] is None) or (not leagues['fulltime']['avg_first_goal_scored']) else {
					'total': None if (leagues['fulltime']['avg_first_goal_scored'].get("@total") is None) or (leagues['fulltime']['avg_first_goal_scored']['@total'] is None) or (not leagues['fulltime']['avg_first_goal_scored']['@total']) else int(leagues['fulltime']['avg_first_goal_scored']['@total']),
					'home': None if (leagues['fulltime']['avg_first_goal_scored'].get("@home") is None) or (leagues['fulltime']['avg_first_goal_scored']['@home'] is None) or (not leagues['fulltime']['avg_first_goal_scored']['@home']) else int(leagues['fulltime']['avg_first_goal_scored']['@home']),
					'away': None if (leagues['fulltime']['avg_first_goal_scored'].get("@away") is None) or (leagues['fulltime']['avg_first_goal_scored']['@away'] is None) or (not leagues['fulltime']['avg_first_goal_scored']['@away']) else int(leagues['fulltime']['avg_first_goal_scored']['@away'])
				},
				'avg_first_goal_conceded': None if (leagues['fulltime'].get("avg_first_goal_conceded") is None) or (leagues['fulltime']['avg_first_goal_conceded'] is None) or (not leagues['fulltime']['avg_first_goal_conceded']) else {
					'total': None if (leagues['fulltime']['avg_first_goal_conceded'].get("@total") is None) or (leagues['fulltime']['avg_first_goal_conceded']['@total'] is None) or (not leagues['fulltime']['avg_first_goal_conceded']['@total']) else int(leagues['fulltime']['avg_first_goal_conceded']['@total']),
					'home': None if (leagues['fulltime']['avg_first_goal_conceded'].get("@home") is None) or (leagues['fulltime']['avg_first_goal_conceded']['@home'] is None) or (not leagues['fulltime']['avg_first_goal_conceded']['@home']) else int(leagues['fulltime']['avg_first_goal_conceded']['@home']),
					'away': None if (leagues['fulltime']['avg_first_goal_conceded'].get("@away") is None) or (leagues['fulltime']['avg_first_goal_conceded']['@away'] is None) or (not leagues['fulltime']['avg_first_goal_conceded']['@away']) else int(leagues['fulltime']['avg_first_goal_conceded']['@away'])
				},
				'failed_to_score': None if (leagues['fulltime'].get("failed_to_score") is None) or (leagues['fulltime']['failed_to_score'] is None) or (not leagues['fulltime']['failed_to_score']) else {
					'total': None if (leagues['fulltime']['failed_to_score'].get("@total") is None) or (leagues['fulltime']['failed_to_score']['@total'] is None) or (not leagues['fulltime']['failed_to_score']['@total']) else int(leagues['fulltime']['failed_to_score']['@total']),
					'home': None if (leagues['fulltime']['failed_to_score'].get("@home") is None) or (leagues['fulltime']['failed_to_score']['@home'] is None) or (not leagues['fulltime']['failed_to_score']['@home']) else int(leagues['fulltime']['failed_to_score']['@home']),
					'away': None if (leagues['fulltime']['failed_to_score'].get("@away") is None) or (leagues['fulltime']['failed_to_score']['@away'] is None) or (not leagues['fulltime']['failed_to_score']['@away']) else int(leagues['fulltime']['failed_to_score']['@away'])
				},
				'shotsTotal': None if (leagues['fulltime'].get("shotsTotal") is None) or (leagues['fulltime']['shotsTotal'] is None) or (not leagues['fulltime']['shotsTotal']) else {
					'total': None if (leagues['fulltime']['shotsTotal'].get("@total") is None) or (leagues['fulltime']['shotsTotal']['@total'] is None) or (not leagues['fulltime']['shotsTotal']['@total']) else int(leagues['fulltime']['shotsTotal']['@total']),
					'home': None if (leagues['fulltime']['shotsTotal'].get("@home") is None) or (leagues['fulltime']['shotsTotal']['@home'] is None) or (not leagues['fulltime']['shotsTotal']['@home']) else int(leagues['fulltime']['shotsTotal']['@home']),
					'away': None if (leagues['fulltime']['shotsTotal'].get("@away") is None) or (leagues['fulltime']['shotsTotal']['@away'] is None) or (not leagues['fulltime']['shotsTotal']['@away']) else int(leagues['fulltime']['shotsTotal']['@away'])
				},
				'shotsOnGoal': None if (leagues['fulltime'].get("shotsOnGoal") is None) or (leagues['fulltime']['shotsOnGoal'] is None) or (not leagues['fulltime']['shotsOnGoal']) else {
					'total': None if (leagues['fulltime']['shotsOnGoal'].get("@total") is None) or (leagues['fulltime']['shotsOnGoal']['@total'] is None) or (not leagues['fulltime']['shotsOnGoal']['@total']) else int(leagues['fulltime']['shotsOnGoal']['@total']),
					'home': None if (leagues['fulltime']['shotsOnGoal'].get("@home") is None) or (leagues['fulltime']['shotsOnGoal']['@home'] is None) or (not leagues['fulltime']['shotsOnGoal']['@home']) else int(leagues['fulltime']['shotsOnGoal']['@home']),
					'away': None if (leagues['fulltime']['shotsOnGoal'].get("@away") is None) or (leagues['fulltime']['shotsOnGoal']['@away'] is None) or (not leagues['fulltime']['shotsOnGoal']['@away']) else int(leagues['fulltime']['shotsOnGoal']['@away'])
				},
				'corners': None if (leagues['fulltime'].get("corners") is None) or (leagues['fulltime']['corners'] is None) or (not leagues['fulltime']['corners']) else {
					'total': None if (leagues['fulltime']['corners'].get("@total") is None) or (leagues['fulltime']['corners']['@total'] is None) or (not leagues['fulltime']['corners']['@total']) else int(leagues['fulltime']['corners']['@total']),
					'home': None if (leagues['fulltime']['corners'].get("@home") is None) or (leagues['fulltime']['corners']['@home'] is None) or (not leagues['fulltime']['corners']['@home']) else int(leagues['fulltime']['corners']['@home']),
					'away': None if (leagues['fulltime']['corners'].get("@away") is None) or (leagues['fulltime']['corners']['@away'] is None) or (not leagues['fulltime']['corners']['@away']) else int(leagues['fulltime']['corners']['@away'])
				},
				'avg_corners': None if (leagues['fulltime'].get("avg_corners") is None) or (leagues['fulltime']['avg_corners'] is None) or (not leagues['fulltime']['avg_corners']) else {
					'total': None if (leagues['fulltime']['avg_corners'].get("@total") is None) or (leagues['fulltime']['avg_corners']['@total'] is None) or (not leagues['fulltime']['avg_corners']['@total']) else float(leagues['fulltime']['avg_corners']['@total']),
					'home': None if (leagues['fulltime']['avg_corners'].get("@home") is None) or (leagues['fulltime']['avg_corners']['@home'] is None) or (not leagues['fulltime']['avg_corners']['@home']) else float(leagues['fulltime']['avg_corners']['@home']),
					'away': None if (leagues['fulltime']['avg_corners'].get("@away") is None) or (leagues['fulltime']['avg_corners']['@away'] is None) or (not leagues['fulltime']['avg_corners']['@away']) else float(leagues['fulltime']['avg_corners']['@away'])
				},
				'offsides': None if (leagues['fulltime'].get("offsides") is None) or (leagues['fulltime']['offsides'] is None) or (not leagues['fulltime']['offsides']) else {
					'total': None if (leagues['fulltime']['offsides'].get("@total") is None) or (leagues['fulltime']['offsides']['@total'] is None) or (not leagues['fulltime']['offsides']['@total']) else int(leagues['fulltime']['offsides']['@total']),
					'home': None if (leagues['fulltime']['offsides'].get("@home") is None) or (leagues['fulltime']['offsides']['@home'] is None) or (not leagues['fulltime']['offsides']['@home']) else int(leagues['fulltime']['offsides']['@home']),
					'away': None if (leagues['fulltime']['offsides'].get("@away") is None) or (leagues['fulltime']['offsides']['@away'] is None) or (not leagues['fulltime']['offsides']['@away']) else int(leagues['fulltime']['offsides']['@away'])
				},
				'possession': None if (leagues['fulltime'].get("possession") is None) or (leagues['fulltime']['possession'] is None) or (not leagues['fulltime']['possession']) else {
					'total': None if (leagues['fulltime']['possession'].get("@total") is None) or (leagues['fulltime']['possession']['@total'] is None) or (not leagues['fulltime']['possession']['@total']) else int(leagues['fulltime']['possession']['@total']),
					'home': None if (leagues['fulltime']['possession'].get("@home") is None) or (leagues['fulltime']['possession']['@home'] is None) or (not leagues['fulltime']['possession']['@home']) else int(leagues['fulltime']['possession']['@home']),
					'away': None if (leagues['fulltime']['possession'].get("@away") is None) or (leagues['fulltime']['possession']['@away'] is None) or (not leagues['fulltime']['possession']['@away']) else int(leagues['fulltime']['possession']['@away'])
				},
				'fouls': None if (leagues['fulltime'].get("fouls") is None) or (leagues['fulltime']['fouls'] is None) or (not leagues['fulltime']['fouls']) else {
					'total': None if (leagues['fulltime']['fouls'].get("@total") is None) or (leagues['fulltime']['fouls']['@total'] is None) or (not leagues['fulltime']['fouls']['@total']) else int(leagues['fulltime']['fouls']['@total']),
					'home': None if (leagues['fulltime']['fouls'].get("@home") is None) or (leagues['fulltime']['fouls']['@home'] is None) or (not leagues['fulltime']['fouls']['@home']) else int(leagues['fulltime']['fouls']['@home']),
					'away': None if (leagues['fulltime']['fouls'].get("@away") is None) or (leagues['fulltime']['fouls']['@away'] is None) or (not leagues['fulltime']['fouls']['@away']) else int(leagues['fulltime']['fouls']['@away'])
				},
				'yellowcards': None if (leagues['fulltime'].get("yellowcards") is None) or (leagues['fulltime']['yellowcards'] is None) or (not leagues['fulltime']['yellowcards']) else {
					'total': None if (leagues['fulltime']['yellowcards'].get("@total") is None) or (leagues['fulltime']['yellowcards']['@total'] is None) or (not leagues['fulltime']['yellowcards']['@total']) else int(leagues['fulltime']['yellowcards']['@total']),
					'home': None if (leagues['fulltime']['yellowcards'].get("@home") is None) or (leagues['fulltime']['yellowcards']['@home'] is None) or (not leagues['fulltime']['yellowcards']['@home']) else int(leagues['fulltime']['yellowcards']['@home']),
					'away': None if (leagues['fulltime']['yellowcards'].get("@away") is None) or (leagues['fulltime']['yellowcards']['@away'] is None) or (not leagues['fulltime']['yellowcards']['@away']) else int(leagues['fulltime']['yellowcards']['@away'])
				},
				'redcards': None if (leagues['fulltime'].get("redcards") is None) or (leagues['fulltime']['redcards'] is None) or (not leagues['fulltime']['redcards']) else {
					'total': None if (leagues['fulltime']['redcards'].get("@total") is None) or (leagues['fulltime']['redcards']['@total'] is None) or (not leagues['fulltime']['redcards']['@total']) else int(leagues['fulltime']['redcards']['@total']),
					'home': None if (leagues['fulltime']['redcards'].get("@total") is None) or (leagues['fulltime']['redcards']['@home'] is None) or (not leagues['fulltime']['redcards']['@home']) else int(leagues['fulltime']['redcards']['@home']),
					'away': None if (leagues['fulltime']['redcards'].get("@total") is None) or (leagues['fulltime']['redcards']['@away'] is None) or (not leagues['fulltime']['redcards']['@away']) else int(leagues['fulltime']['redcards']['@away'])
				},
				'avg_yellowcards': None if (leagues['fulltime'].get("avg_yellowcards") is None) or (leagues['fulltime']['avg_yellowcards'] is None) or (not leagues['fulltime']['avg_yellowcards']) else {
					'total': None if (leagues['fulltime']['avg_yellowcards'].get("@total") is None) or (leagues['fulltime']['avg_yellowcards']['@total'] is None) or (not leagues['fulltime']['avg_yellowcards']['@total']) else float(leagues['fulltime']['avg_yellowcards']['@total']),
					'home': None if (leagues['fulltime']['avg_yellowcards'].get("@home") is None) or (leagues['fulltime']['avg_yellowcards']['@home'] is None) or (not leagues['fulltime']['avg_yellowcards']['@home']) else float(leagues['fulltime']['avg_yellowcards']['@home']),
					'away': None if (leagues['fulltime']['avg_yellowcards'].get("@away") is None) or (leagues['fulltime']['avg_yellowcards']['@away'] is None) or (not leagues['fulltime']['avg_yellowcards']['@away']) else float(leagues['fulltime']['avg_yellowcards']['@away'])
				},
				'avg_redcards': None if (leagues['fulltime'].get("avg_redcards") is None) or (leagues['fulltime']['avg_redcards'] is None) or (not leagues['fulltime']['avg_redcards']) else {
					'total': None if (leagues['fulltime']['avg_redcards'].get("@total") is None) or (leagues['fulltime']['avg_redcards']['@total'] is None) or (not leagues['fulltime']['avg_redcards']['@total']) else float(leagues['fulltime']['avg_redcards']['@total']),
					'home': None if (leagues['fulltime']['avg_redcards'].get("@home") is None) or (leagues['fulltime']['avg_redcards']['@home'] is None) or (not leagues['fulltime']['avg_redcards']['@home']) else float(leagues['fulltime']['avg_redcards']['@home']),
					'away': None if (leagues['fulltime']['avg_redcards'].get("@away") is None) or (leagues['fulltime']['avg_redcards']['@away'] is None) or (not leagues['fulltime']['avg_redcards']['@away']) else float(leagues['fulltime']['avg_redcards']['@away'])
				}
			},
			'firsthalf': None if (leagues.get("firsthalf") is None) or (leagues['firsthalf'] is None) or (not leagues['firsthalf']) else {
				'win': None if (leagues['firsthalf'].get("win") is None) or (leagues['firsthalf']['win'] is None) or (not leagues['firsthalf']['win']) else {
					'total': None if (leagues['firsthalf']['win'].get("@total") is None) or (leagues['firsthalf']['win']['@total'] is None) or (not leagues['firsthalf']['win']['@total']) else int(leagues['firsthalf']['win']['@total']),
					'home': None if (leagues['firsthalf']['win'].get("@home") is None) or (leagues['firsthalf']['win']['@home'] is None) or (not leagues['firsthalf']['win']['@home']) else int(leagues['firsthalf']['win']['@home']),
					'away': None if (leagues['firsthalf']['win'].get("@away") is None) or (leagues['firsthalf']['win']['@away'] is None) or (not leagues['firsthalf']['win']['@away']) else int(leagues['firsthalf']['win']['@away'])
				},
				'lost': None if (leagues['firsthalf'].get("lost") is None) or (leagues['firsthalf']['lost'] is None) or (not leagues['firsthalf']['lost']) else {
					'total': None if (leagues['firsthalf']['lost'].get("@total") is None) or (leagues['firsthalf']['lost']['@total'] is None) or (not leagues['firsthalf']['lost']['@total']) else int(leagues['firsthalf']['lost']['@total']),
					'home': None if (leagues['firsthalf']['lost'].get("@home") is None) or (leagues['firsthalf']['lost']['@home'] is None) or (not leagues['firsthalf']['lost']['@home']) else int(leagues['firsthalf']['lost']['@home']),
					'away': None if (leagues['firsthalf']['lost'].get("@away") is None) or (leagues['firsthalf']['lost']['@away'] is None) or (not leagues['firsthalf']['lost']['@away']) else int(leagues['firsthalf']['lost']['@away'])
				},
				'draw': None if (leagues['firsthalf'].get("draw") is None) or (leagues['firsthalf']['draw'] is None) or (not leagues['firsthalf']['draw']) else {
					'total': None if (leagues['firsthalf']['draw'].get("@total") is None) or (leagues['firsthalf']['draw']['@total'] is None) or (not leagues['firsthalf']['draw']['@total']) else int(leagues['firsthalf']['draw']['@total']),
					'home': None if (leagues['firsthalf']['draw'].get("@home") is None) or (leagues['firsthalf']['draw']['@home'] is None) or (not leagues['firsthalf']['draw']['@home']) else int(leagues['firsthalf']['draw']['@home']),
					'away': None if (leagues['firsthalf']['draw'].get("@away") is None) or (leagues['firsthalf']['draw']['@away'] is None) or (not leagues['firsthalf']['draw']['@away']) else int(leagues['firsthalf']['draw']['@away'])
				},
				'win_halftime': None if (leagues['firsthalf'].get("win_halftime") is None) or (leagues['firsthalf']['win_halftime'] is None) or (not leagues['firsthalf']['win_halftime']) else {
					'ft_win': None if (leagues['firsthalf']['win_halftime'].get("@ft_win") is None) or (leagues['firsthalf']['win_halftime']['@ft_win'] is None) or (not leagues['firsthalf']['win_halftime']['@ft_win']) else int(leagues['firsthalf']['win_halftime']['@ft_win']),
					'ft_draw': None if (leagues['firsthalf']['win_halftime'].get("@ft_draw") is None) or (leagues['firsthalf']['win_halftime']['@ft_draw'] is None) or (not leagues['firsthalf']['win_halftime']['@ft_draw']) else int(leagues['firsthalf']['win_halftime']['@ft_draw']),
					'ft_lost': None if (leagues['firsthalf']['win_halftime'].get("@ft_lost") is None) or (leagues['firsthalf']['win_halftime']['@ft_lost'] is None) or (not leagues['firsthalf']['win_halftime']['@ft_lost']) else int(leagues['firsthalf']['win_halftime']['@ft_lost'])
				},
				'draw_halftime': None if (leagues['firsthalf'].get("draw_halftime") is None) or (leagues['firsthalf']['draw_halftime'] is None) or (not leagues['firsthalf']['draw_halftime']) else {
					'ft_win': None if (leagues['firsthalf']['draw_halftime'].get("@ft_win") is None) or (leagues['firsthalf']['draw_halftime']['@ft_win'] is None) or (not leagues['firsthalf']['draw_halftime']['@ft_win']) else int(leagues['firsthalf']['draw_halftime']['@ft_win']),
					'ft_draw': None if (leagues['firsthalf']['draw_halftime'].get("@ft_draw") is None) or (leagues['firsthalf']['draw_halftime']['@ft_draw'] is None) or (not leagues['firsthalf']['draw_halftime']['@ft_draw']) else int(leagues['firsthalf']['draw_halftime']['@ft_draw']),
					'ft_lost': None if (leagues['firsthalf']['draw_halftime'].get("@ft_lost") is None) or (leagues['firsthalf']['draw_halftime']['@ft_lost'] is None) or (not leagues['firsthalf']['draw_halftime']['@ft_lost']) else int(leagues['firsthalf']['draw_halftime']['@ft_lost'])
				},
				'lost_halftime': None if (leagues['firsthalf'].get("lost_halftime") is None) or (leagues['firsthalf']['lost_halftime'] is None) or (not leagues['firsthalf']['lost_halftime']) else {
					'ft_win': None if (leagues['firsthalf']['lost_halftime'].get("@ft_win") is None) or (leagues['firsthalf']['lost_halftime']['@ft_win'] is None) or (not leagues['firsthalf']['lost_halftime']['@ft_win']) else int(leagues['firsthalf']['lost_halftime']['@ft_win']),
					'ft_draw': None if (leagues['firsthalf']['lost_halftime'].get("@ft_draw") is None) or (leagues['firsthalf']['lost_halftime']['@ft_draw'] is None) or (not leagues['firsthalf']['lost_halftime']['@ft_draw']) else int(leagues['firsthalf']['lost_halftime']['@ft_draw']),
					'ft_lost': None if (leagues['firsthalf']['lost_halftime'].get("@ft_lost") is None) or (leagues['firsthalf']['lost_halftime']['@ft_lost'] is None) or (not leagues['firsthalf']['lost_halftime']['@ft_lost']) else int(leagues['firsthalf']['lost_halftime']['@ft_lost'])
				},
				'goals_for': None if (leagues['firsthalf'].get("goals_for") is None) or (leagues['firsthalf']['goals_for'] is None) or (not leagues['firsthalf']['goals_for']) else {
					'total': None if (leagues['firsthalf']['goals_for'].get("@total") is None) or (leagues['firsthalf']['goals_for']['@total'] is None) or (not leagues['firsthalf']['goals_for']['@total']) else int(leagues['firsthalf']['goals_for']['@total']),
					'home': None if (leagues['firsthalf']['goals_for'].get("@home") is None) or (leagues['firsthalf']['goals_for']['@home'] is None) or (not leagues['firsthalf']['goals_for']['@home']) else int(leagues['firsthalf']['goals_for']['@home']),
					'away': None if (leagues['firsthalf']['goals_for'].get("@away") is None) or (leagues['firsthalf']['goals_for']['@away'] is None) or (not leagues['firsthalf']['goals_for']['@away']) else int(leagues['firsthalf']['goals_for']['@away'])
				},
				'goals_against': None if (leagues['firsthalf'].get("goals_against") is None) or (leagues['firsthalf']['goals_against'] is None) or (not leagues['firsthalf']['goals_against']) else {
					'total': None if (leagues['firsthalf']['goals_against'].get("@total") is None) or (leagues['firsthalf']['goals_against']['@total'] is None) or (not leagues['firsthalf']['goals_against']['@total']) else int(leagues['firsthalf']['goals_against']['@total']),
					'home': None if (leagues['firsthalf']['goals_against'].get("@home") is None) or (leagues['firsthalf']['goals_against']['@home'] is None) or (not leagues['firsthalf']['goals_against']['@home']) else int(leagues['firsthalf']['goals_against']['@home']),
					'away': None if (leagues['firsthalf']['goals_against'].get("@away") is None) or (leagues['firsthalf']['goals_against']['@away'] is None) or (not leagues['firsthalf']['goals_against']['@away']) else int(leagues['firsthalf']['goals_against']['@away'])
				},
				'goals_for_additiional_time': None if (leagues['firsthalf'].get("goals_for_additiional_time") is None) or (leagues['firsthalf']['goals_for_additiional_time'] is None) or (not leagues['firsthalf']['goals_for_additiional_time']) else {
					'total': None if (leagues['firsthalf']['goals_for_additiional_time'].get("@total") is None) or (leagues['firsthalf']['goals_for_additiional_time']['@total'] is None) or (not leagues['firsthalf']['goals_for_additiional_time']['@total']) else int(leagues['firsthalf']['goals_for_additiional_time']['@total']),
					'home': None if (leagues['firsthalf']['goals_for_additiional_time'].get("@home") is None) or (leagues['firsthalf']['goals_for_additiional_time']['@home'] is None) or (not leagues['firsthalf']['goals_for_additiional_time']['@home']) else int(leagues['firsthalf']['goals_for_additiional_time']['@home']),
					'away': None if (leagues['firsthalf']['goals_for_additiional_time'].get("@away") is None) or (leagues['firsthalf']['goals_for_additiional_time']['@away'] is None) or (not leagues['firsthalf']['goals_for_additiional_time']['@away']) else int(leagues['firsthalf']['goals_for_additiional_time']['@away'])
				},
				'goals_against_additiional_time': None if (leagues['firsthalf'].get("goals_against_additiional_time") is None) or (leagues['firsthalf']['goals_against_additiional_time'] is None) or (not leagues['firsthalf']['goals_against_additiional_time']) else {
					'total': None if (leagues['firsthalf']['goals_against_additiional_time'].get("@total") is None) or (leagues['firsthalf']['goals_against_additiional_time']['@total'] is None) or (not leagues['firsthalf']['goals_against_additiional_time']['@total']) else int(leagues['firsthalf']['goals_against_additiional_time']['@total']),
					'home': None if (leagues['firsthalf']['goals_against_additiional_time'].get("@home") is None) or (leagues['firsthalf']['goals_against_additiional_time']['@home'] is None) or (not leagues['firsthalf']['goals_against_additiional_time']['@home']) else int(leagues['firsthalf']['goals_against_additiional_time']['@home']),
					'away': None if (leagues['firsthalf']['goals_against_additiional_time'].get("@away") is None) or (leagues['firsthalf']['goals_against_additiional_time']['@away'] is None) or (not leagues['firsthalf']['goals_against_additiional_time']['@away']) else int(leagues['firsthalf']['goals_against_additiional_time']['@away'])
				},
				'clean_sheet': None if (leagues['firsthalf'].get("clean_sheet") is None) or (leagues['firsthalf']['clean_sheet'] is None) or (not leagues['firsthalf']['clean_sheet']) else {
					'total': None if (leagues['firsthalf']['clean_sheet'].get("@total") is None) or (leagues['firsthalf']['clean_sheet']['@total'] is None) or (not leagues['firsthalf']['clean_sheet']['@total']) else int(leagues['firsthalf']['clean_sheet']['@total']),
					'home': None if (leagues['firsthalf']['clean_sheet'].get("@home") is None) or (leagues['firsthalf']['clean_sheet']['@home'] is None) or (not leagues['firsthalf']['clean_sheet']['@home']) else int(leagues['firsthalf']['clean_sheet']['@home']),
					'away': None if (leagues['firsthalf']['clean_sheet'].get("@away") is None) or (leagues['firsthalf']['clean_sheet']['@away'] is None) or (not leagues['firsthalf']['clean_sheet']['@away']) else int(leagues['firsthalf']['clean_sheet']['@away'])
				},
				'avg_goals_per_game_scored': None if (leagues['firsthalf'].get("avg_goals_per_game_scored") is None) or (leagues['firsthalf']['avg_goals_per_game_scored'] is None) or (not leagues['firsthalf']['avg_goals_per_game_scored']) else {
					'total': None if (leagues['firsthalf']['avg_goals_per_game_scored'].get("@total") is None) or (leagues['firsthalf']['avg_goals_per_game_scored']['@total'] is None) or (not leagues['firsthalf']['avg_goals_per_game_scored']['@total']) else float(leagues['firsthalf']['avg_goals_per_game_scored']['@total']),
					'home': None if (leagues['firsthalf']['avg_goals_per_game_scored'].get("@home") is None) or (leagues['firsthalf']['avg_goals_per_game_scored']['@home'] is None) or (not leagues['firsthalf']['avg_goals_per_game_scored']['@home']) else float(leagues['firsthalf']['avg_goals_per_game_scored']['@home']),
					'away': None if (leagues['firsthalf']['avg_goals_per_game_scored'].get("@away") is None) or (leagues['firsthalf']['avg_goals_per_game_scored']['@away'] is None) or (not leagues['firsthalf']['avg_goals_per_game_scored']['@away']) else float(leagues['firsthalf']['avg_goals_per_game_scored']['@away'])
				},
				'avg_goals_per_game_conceded': None if (leagues['firsthalf'].get("avg_goals_per_game_conceded") is None) or (leagues['firsthalf']['avg_goals_per_game_conceded'] is None) or (not leagues['firsthalf']['avg_goals_per_game_conceded']) else {
					'total': None if (leagues['firsthalf']['avg_goals_per_game_conceded'].get("@total") is None) or (leagues['firsthalf']['avg_goals_per_game_conceded']['@total'] is None) or (not leagues['firsthalf']['avg_goals_per_game_conceded']['@total']) else float(leagues['firsthalf']['avg_goals_per_game_conceded']['@total']),
					'home': None if (leagues['firsthalf']['avg_goals_per_game_conceded'].get("@home") is None) or (leagues['firsthalf']['avg_goals_per_game_conceded']['@home'] is None) or (not leagues['firsthalf']['avg_goals_per_game_conceded']['@home']) else float(leagues['firsthalf']['avg_goals_per_game_conceded']['@home']),
					'away': None if (leagues['firsthalf']['avg_goals_per_game_conceded'].get("@away") is None) or (leagues['firsthalf']['avg_goals_per_game_conceded']['@away'] is None) or (not leagues['firsthalf']['avg_goals_per_game_conceded']['@away']) else float(leagues['firsthalf']['avg_goals_per_game_conceded']['@away'])
				},
				'failed_to_score': None if (leagues['firsthalf'].get("failed_to_score") is None) or (leagues['firsthalf']['failed_to_score'] is None) or (not leagues['firsthalf']['failed_to_score']) else {
					'total': None if (leagues['firsthalf']['failed_to_score'].get("@total") is None) or (leagues['firsthalf']['failed_to_score']['@total'] is None) or (not leagues['firsthalf']['failed_to_score']['@total']) else int(leagues['firsthalf']['failed_to_score']['@total']),
					'home': None if (leagues['firsthalf']['failed_to_score'].get("@home") is None) or (leagues['firsthalf']['failed_to_score']['@home'] is None) or (not leagues['firsthalf']['failed_to_score']['@home']) else int(leagues['firsthalf']['failed_to_score']['@home']),
					'away': None if (leagues['firsthalf']['failed_to_score'].get("@away") is None) or (leagues['firsthalf']['failed_to_score']['@away'] is None) or (not leagues['firsthalf']['failed_to_score']['@away']) else int(leagues['firsthalf']['failed_to_score']['@away'])
				},
				'shotsTotal': None if (leagues['firsthalf'].get("shotsTotal") is None) or (leagues['firsthalf']['shotsTotal'] is None) or (not leagues['firsthalf']['shotsTotal']) else {
					'total': None if (leagues['firsthalf']['shotsTotal'].get("@total") is None) or (leagues['firsthalf']['shotsTotal']['@total'] is None) or (not leagues['firsthalf']['shotsTotal']['@total']) else int(leagues['firsthalf']['shotsTotal']['@total']),
					'home': None if (leagues['firsthalf']['shotsTotal'].get("@home") is None) or (leagues['firsthalf']['shotsTotal']['@home'] is None) or (not leagues['firsthalf']['shotsTotal']['@home']) else int(leagues['firsthalf']['shotsTotal']['@home']),
					'away': None if (leagues['firsthalf']['shotsTotal'].get("@away") is None) or (leagues['firsthalf']['shotsTotal']['@away'] is None) or (not leagues['firsthalf']['shotsTotal']['@away']) else int(leagues['firsthalf']['shotsTotal']['@away'])
				},
				'shotsOnGoal': None if (leagues['firsthalf'].get("shotsOnGoal") is None) or (leagues['firsthalf']['shotsOnGoal'] is None) or (not leagues['firsthalf']['shotsOnGoal']) else {
					'total': None if (leagues['firsthalf']['shotsOnGoal'].get("@total") is None) or (leagues['firsthalf']['shotsOnGoal']['@total'] is None) or (not leagues['firsthalf']['shotsOnGoal']['@total']) else int(leagues['firsthalf']['shotsOnGoal']['@total']),
					'home': None if (leagues['firsthalf']['shotsOnGoal'].get("@home") is None) or (leagues['firsthalf']['shotsOnGoal']['@home'] is None) or (not leagues['firsthalf']['shotsOnGoal']['@home']) else int(leagues['firsthalf']['shotsOnGoal']['@home']),
					'away': None if (leagues['firsthalf']['shotsOnGoal'].get("@away") is None) or (leagues['firsthalf']['shotsOnGoal']['@away'] is None) or (not leagues['firsthalf']['shotsOnGoal']['@away']) else int(leagues['firsthalf']['shotsOnGoal']['@away'])
				},
				'corners': None if (leagues['firsthalf'].get("corners") is None) or (leagues['firsthalf']['corners'] is None) or (not leagues['firsthalf']['corners']) else {
					'total': None if (leagues['firsthalf']['corners'].get("@total") is None) or (leagues['firsthalf']['corners']['@total'] is None) or (not leagues['firsthalf']['corners']['@total']) else int(leagues['firsthalf']['corners']['@total']),
					'home': None if (leagues['firsthalf']['corners'].get("@home") is None) or (leagues['firsthalf']['corners']['@home'] is None) or (not leagues['firsthalf']['corners']['@home']) else int(leagues['firsthalf']['corners']['@home']),
					'away': None if (leagues['firsthalf']['corners'].get("@away") is None) or (leagues['firsthalf']['corners']['@away'] is None) or (not leagues['firsthalf']['corners']['@away']) else int(leagues['firsthalf']['corners']['@away'])
				},
				'avg_corners': None if (leagues['firsthalf'].get("avg_corners") is None) or (leagues['firsthalf']['avg_corners'] is None) or (not leagues['firsthalf']['avg_corners']) else {
					'total': None if (leagues['firsthalf']['avg_corners'].get("@total") is None) or (leagues['firsthalf']['avg_corners']['@total'] is None) or (not leagues['firsthalf']['avg_corners']['@total']) else float(leagues['firsthalf']['avg_corners']['@total']),
					'home': None if (leagues['firsthalf']['avg_corners'].get("@home") is None) or (leagues['firsthalf']['avg_corners']['@home'] is None) or (not leagues['firsthalf']['avg_corners']['@home']) else float(leagues['firsthalf']['avg_corners']['@home']),
					'away': None if (leagues['firsthalf']['avg_corners'].get("@away") is None) or (leagues['firsthalf']['avg_corners']['@away'] is None) or (not leagues['firsthalf']['avg_corners']['@away']) else float(leagues['firsthalf']['avg_corners']['@away'])
				},
				'offsides': None if (leagues['firsthalf'].get("offsides") is None) or (leagues['firsthalf']['offsides'] is None) or (not leagues['firsthalf']['offsides']) else {
					'total': None if (leagues['firsthalf']['offsides'].get("@total") is None) or (leagues['firsthalf']['offsides']['@total'] is None) or (not leagues['firsthalf']['offsides']['@total']) else int(leagues['firsthalf']['offsides']['@total']),
					'home': None if (leagues['firsthalf']['offsides'].get("@home") is None) or (leagues['firsthalf']['offsides']['@home'] is None) or (not leagues['firsthalf']['offsides']['@home']) else int(leagues['firsthalf']['offsides']['@home']),
					'away': None if (leagues['firsthalf']['offsides'].get("@away") is None) or (leagues['firsthalf']['offsides']['@away'] is None) or (not leagues['firsthalf']['offsides']['@away']) else int(leagues['firsthalf']['offsides']['@away'])
				},
				'possession': None if (leagues['firsthalf'].get("possession") is None) or (leagues['firsthalf']['possession'] is None) or (not leagues['firsthalf']['possession']) else {
					'total': None if (leagues['firsthalf']['possession'].get("@total") is None) or (leagues['firsthalf']['possession']['@total'] is None) or (not leagues['firsthalf']['possession']['@total']) else int(leagues['firsthalf']['possession']['@total']),
					'home': None if (leagues['firsthalf']['possession'].get("@home") is None) or (leagues['firsthalf']['possession']['@home'] is None) or (not leagues['firsthalf']['possession']['@home']) else int(leagues['firsthalf']['possession']['@home']),
					'away': None if (leagues['firsthalf']['possession'].get("@away") is None) or (leagues['firsthalf']['possession']['@away'] is None) or (not leagues['firsthalf']['possession']['@away']) else int(leagues['firsthalf']['possession']['@away'])
				},
				'fouls': None if (leagues['firsthalf'].get("fouls") is None) or (leagues['firsthalf']['fouls'] is None) or (not leagues['firsthalf']['fouls']) else {
					'total': None if (leagues['firsthalf']['fouls'].get("@total") is None) or (leagues['firsthalf']['fouls']['@total'] is None) or (not leagues['firsthalf']['fouls']['@total']) else int(leagues['firsthalf']['fouls']['@total']),
					'home': None if (leagues['firsthalf']['fouls'].get("@home") is None) or (leagues['firsthalf']['fouls']['@home'] is None) or (not leagues['firsthalf']['fouls']['@home']) else int(leagues['firsthalf']['fouls']['@home']),
					'away': None if (leagues['firsthalf']['fouls'].get("@away") is None) or (leagues['firsthalf']['fouls']['@away'] is None) or (not leagues['firsthalf']['fouls']['@away']) else int(leagues['firsthalf']['fouls']['@away'])
				},
				'yellowcards': None if (leagues['firsthalf'].get("yellowcards") is None) or (leagues['firsthalf']['yellowcards'] is None) or (not leagues['firsthalf']['yellowcards']) else {
					'total': None if (leagues['firsthalf']['yellowcards'].get("@total") is None) or (leagues['firsthalf']['yellowcards']['@total'] is None) or (not leagues['firsthalf']['yellowcards']['@total']) else int(leagues['firsthalf']['yellowcards']['@total']),
					'home': None if (leagues['firsthalf']['yellowcards'].get("@home") is None) or (leagues['firsthalf']['yellowcards']['@home'] is None) or (not leagues['firsthalf']['yellowcards']['@home']) else int(leagues['firsthalf']['yellowcards']['@home']),
					'away': None if (leagues['firsthalf']['yellowcards'].get("@away") is None) or (leagues['firsthalf']['yellowcards']['@away'] is None) or (not leagues['firsthalf']['yellowcards']['@away']) else int(leagues['firsthalf']['yellowcards']['@away'])
				},
				'redcards': None if (leagues['firsthalf'].get("redcards") is None) or (leagues['firsthalf']['redcards'] is None) or (not leagues['firsthalf']['redcards']) else {
					'total': None if (leagues['firsthalf']['redcards'].get("@total") is None) or (leagues['firsthalf']['redcards']['@total'] is None) or (not leagues['firsthalf']['redcards']['@total']) else int(leagues['firsthalf']['redcards']['@total']),
					'home': None if (leagues['firsthalf']['redcards'].get("@home") is None) or (leagues['firsthalf']['redcards']['@home'] is None) or (not leagues['firsthalf']['redcards']['@home']) else int(leagues['firsthalf']['redcards']['@home']),
					'away': None if (leagues['firsthalf']['redcards'].get("@away") is None) or (leagues['firsthalf']['redcards']['@away'] is None) or (not leagues['firsthalf']['redcards']['@away']) else int(leagues['firsthalf']['redcards']['@away'])
				},
				'avg_yellowcards': None if (leagues['firsthalf'].get("avg_yellowcards") is None) or (leagues['firsthalf']['avg_yellowcards'] is None) or (not leagues['firsthalf']['avg_yellowcards']) else {
					'total': None if (leagues['firsthalf']['avg_yellowcards'].get("@total") is None) or (leagues['firsthalf']['avg_yellowcards']['@total'] is None) or (not leagues['firsthalf']['avg_yellowcards']['@total']) else float(leagues['firsthalf']['avg_yellowcards']['@total']),
					'home': None if (leagues['firsthalf']['avg_yellowcards'].get("@home") is None) or (leagues['firsthalf']['avg_yellowcards']['@home'] is None) or (not leagues['firsthalf']['avg_yellowcards']['@home']) else float(leagues['firsthalf']['avg_yellowcards']['@home']),
					'away': None if (leagues['firsthalf']['avg_yellowcards'].get("@away") is None) or (leagues['firsthalf']['avg_yellowcards']['@away'] is None) or (not leagues['firsthalf']['avg_yellowcards']['@away']) else float(leagues['firsthalf']['avg_yellowcards']['@away'])
				},
				'avg_redcards': None if (leagues['firsthalf'].get("avg_redcards") is None) or (leagues['firsthalf']['avg_redcards'] is None) or (not leagues['firsthalf']['avg_redcards']) else {
					'total': None if (leagues['firsthalf']['avg_redcards'].get("@total") is None) or (leagues['firsthalf']['avg_redcards']['@total'] is None) or (not leagues['firsthalf']['avg_redcards']['@total']) else float(leagues['firsthalf']['avg_redcards']['@total']),
					'home': None if (leagues['firsthalf']['avg_redcards'].get("@home") is None) or (leagues['firsthalf']['avg_redcards']['@home'] is None) or (not leagues['firsthalf']['avg_redcards']['@home']) else float(leagues['firsthalf']['avg_redcards']['@home']),
					'away': None if (leagues['firsthalf']['avg_redcards'].get("@away") is None) or (leagues['firsthalf']['avg_redcards']['@away'] is None) or (not leagues['firsthalf']['avg_redcards']['@away']) else float(leagues['firsthalf']['avg_redcards']['@away'])
				}
			},
			'secondhalf': None if (leagues.get("secondhalf") is None) or (leagues['secondhalf'] is None) or (not leagues['secondhalf']) else {
				'win': None if (leagues['secondhalf'].get("win") is None) or (leagues['secondhalf']['win'] is None) or (not leagues['secondhalf']['win']) else {
					'total': None if (leagues['secondhalf']['win'].get("@total") is None) or (leagues['secondhalf']['win']['@total'] is None) or (not leagues['secondhalf']['win']['@total']) else int(leagues['secondhalf']['win']['@total']),
					'home': None if (leagues['secondhalf']['win'].get("@home") is None) or (leagues['secondhalf']['win']['@home'] is None) or (not leagues['secondhalf']['win']['@home']) else int(leagues['secondhalf']['win']['@home']),
					'away': None if (leagues['secondhalf']['win'].get("@away") is None) or (leagues['secondhalf']['win']['@away'] is None) or (not leagues['secondhalf']['win']['@away']) else int(leagues['secondhalf']['win']['@away'])
				},
				'lost': None if(leagues['secondhalf'].get("lost") is None) or  (leagues['secondhalf']['lost'] is None) or (not leagues['secondhalf']['lost']) else {
					'total': None if (leagues['secondhalf']['lost'].get("@total") is None) or (leagues['secondhalf']['lost']['@total'] is None) or (not leagues['secondhalf']['lost']['@total']) else int(leagues['secondhalf']['lost']['@total']),
					'home': None if (leagues['secondhalf']['lost'].get("@home") is None) or (leagues['secondhalf']['lost']['@home'] is None) or (not leagues['secondhalf']['lost']['@home']) else int(leagues['secondhalf']['lost']['@home']),
					'away': None if (leagues['secondhalf']['lost'].get("@away") is None) or (leagues['secondhalf']['lost']['@away'] is None) or (not leagues['secondhalf']['lost']['@away']) else int(leagues['secondhalf']['lost']['@away'])
				},
				'draw': None if (leagues['secondhalf'].get("draw") is None) or (leagues['secondhalf']['draw'] is None) or (not leagues['secondhalf']['draw']) else {
					'total': None if (leagues['secondhalf']['draw'].get("@total") is None) or (leagues['secondhalf']['draw']['@total'] is None) or (not leagues['secondhalf']['draw']['@total']) else int(leagues['secondhalf']['draw']['@total']),
					'home': None if (leagues['secondhalf']['draw'].get("@home") is None) or (leagues['secondhalf']['draw']['@home'] is None) or (not leagues['secondhalf']['draw']['@home']) else int(leagues['secondhalf']['draw']['@home']),
					'away': None if (leagues['secondhalf']['draw'].get("@away") is None) or (leagues['secondhalf']['draw']['@away'] is None) or (not leagues['secondhalf']['draw']['@away']) else int(leagues['secondhalf']['draw']['@away'])
				},
				'goals_for': None if (leagues['secondhalf'].get("goals_for") is None) or (leagues['secondhalf']['goals_for'] is None) or (not leagues['secondhalf']['goals_for']) else {
					'total': None if (leagues['secondhalf']['goals_for'].get("@total") is None) or (leagues['secondhalf']['goals_for']['@total'] is None) or (not leagues['secondhalf']['goals_for']['@total']) else int(leagues['secondhalf']['goals_for']['@total']),
					'home': None if (leagues['secondhalf']['goals_for'].get("@home") is None) or (leagues['secondhalf']['goals_for']['@home'] is None) or (not leagues['secondhalf']['goals_for']['@home']) else int(leagues['secondhalf']['goals_for']['@home']),
					'away': None if (leagues['secondhalf']['goals_for'].get("@away") is None) or (leagues['secondhalf']['goals_for']['@away'] is None) or (not leagues['secondhalf']['goals_for']['@away']) else int(leagues['secondhalf']['goals_for']['@away'])
				},
				'goals_against': None if (leagues['secondhalf'].get("goals_against") is None) or (leagues['secondhalf']['goals_against'] is None) or (not leagues['secondhalf']['goals_against']) else {
					'total': None if (leagues['secondhalf']['goals_against'].get("@total") is None) or (leagues['secondhalf']['goals_against']['@total'] is None) or (not leagues['secondhalf']['goals_against']['@total']) else int(leagues['secondhalf']['goals_against']['@total']),
					'home': None if (leagues['secondhalf']['goals_against'].get("@home") is None) or (leagues['secondhalf']['goals_against']['@home'] is None) or (not leagues['secondhalf']['goals_against']['@home']) else int(leagues['secondhalf']['goals_against']['@home']),
					'away': None if (leagues['secondhalf']['goals_against'].get("@away") is None) or (leagues['secondhalf']['goals_against']['@away'] is None) or (not leagues['secondhalf']['goals_against']['@away']) else int(leagues['secondhalf']['goals_against']['@away'])
				},
				'goals_for_additiional_time': None if (leagues['secondhalf'].get("goals_for_additiional_time") is None) or (leagues['secondhalf']['goals_for_additiional_time'] is None) or (not leagues['secondhalf']['goals_for_additiional_time']) else {
					'total': None if (leagues['secondhalf']['goals_for_additiional_time'].get("@total") is None) or (leagues['secondhalf']['goals_for_additiional_time']['@total'] is None) or (not leagues['secondhalf']['goals_for_additiional_time']['@total']) else int(leagues['secondhalf']['goals_for_additiional_time']['@total']),
					'home': None if (leagues['secondhalf']['goals_for_additiional_time'].get("@home") is None) or (leagues['secondhalf']['goals_for_additiional_time']['@home'] is None) or (not leagues['secondhalf']['goals_for_additiional_time']['@home']) else int(leagues['secondhalf']['goals_for_additiional_time']['@home']),
					'away': None if (leagues['secondhalf']['goals_for_additiional_time'].get("@away") is None) or (leagues['secondhalf']['goals_for_additiional_time']['@away'] is None) or (not leagues['secondhalf']['goals_for_additiional_time']['@away']) else int(leagues['secondhalf']['goals_for_additiional_time']['@away'])
				},
				'goals_against_additiional_time': None if (leagues['secondhalf'].get("goals_against_additiional_time") is None) or (leagues['secondhalf']['goals_against_additiional_time'] is None) or (not leagues['secondhalf']['goals_against_additiional_time']) else {
					'total': None if (leagues['secondhalf']['goals_against_additiional_time'].get("@total") is None) or (leagues['secondhalf']['goals_against_additiional_time']['@total'] is None) or (not leagues['secondhalf']['goals_against_additiional_time']['@total']) else int(leagues['secondhalf']['goals_against_additiional_time']['@total']),
					'home': None if (leagues['secondhalf']['goals_against_additiional_time'].get("@home") is None) or (leagues['secondhalf']['goals_against_additiional_time']['@home'] is None) or (not leagues['secondhalf']['goals_against_additiional_time']['@home']) else int(leagues['secondhalf']['goals_against_additiional_time']['@home']),
					'away': None if (leagues['secondhalf']['goals_against_additiional_time'].get("@away") is None) or (leagues['secondhalf']['goals_against_additiional_time']['@away'] is None) or (not leagues['secondhalf']['goals_against_additiional_time']['@away']) else int(leagues['secondhalf']['goals_against_additiional_time']['@away'])
				},
				'clean_sheet': None if (leagues['secondhalf'].get("clean_sheet") is None) or (leagues['secondhalf']['clean_sheet'] is None) or (not leagues['secondhalf']['clean_sheet']) else {
					'total': None if (leagues['secondhalf']['clean_sheet'].get("@total") is None) or (leagues['secondhalf']['clean_sheet']['@total'] is None) or (not leagues['secondhalf']['clean_sheet']['@total']) else int(leagues['secondhalf']['clean_sheet']['@total']),
					'home': None if (leagues['secondhalf']['clean_sheet'].get("@home") is None) or (leagues['secondhalf']['clean_sheet']['@home'] is None) or (not leagues['secondhalf']['clean_sheet']['@home']) else int(leagues['secondhalf']['clean_sheet']['@home']),
					'away': None if (leagues['secondhalf']['clean_sheet'].get("@away") is None) or (leagues['secondhalf']['clean_sheet']['@away'] is None) or (not leagues['secondhalf']['clean_sheet']['@away']) else int(leagues['secondhalf']['clean_sheet']['@away'])
				},
				'avg_goals_per_game_scored': None if (leagues['secondhalf'].get("avg_goals_per_game_scored") is None) or (leagues['secondhalf']['avg_goals_per_game_scored'] is None) or (not leagues['secondhalf']['avg_goals_per_game_scored']) else {
					'total': None if (leagues['secondhalf']['avg_goals_per_game_scored'].get("@total") is None) or (leagues['secondhalf']['avg_goals_per_game_scored']['@total'] is None) or (not leagues['secondhalf']['avg_goals_per_game_scored']['@total']) else float(leagues['secondhalf']['avg_goals_per_game_scored']['@total']),
					'home': None if (leagues['secondhalf']['avg_goals_per_game_scored'].get("@home") is None) or (leagues['secondhalf']['avg_goals_per_game_scored']['@home'] is None) or (not leagues['secondhalf']['avg_goals_per_game_scored']['@home']) else float(leagues['secondhalf']['avg_goals_per_game_scored']['@home']),
					'away': None if (leagues['secondhalf']['avg_goals_per_game_scored'].get("@away") is None) or (leagues['secondhalf']['avg_goals_per_game_scored']['@away'] is None) or (not leagues['secondhalf']['avg_goals_per_game_scored']['@away']) else float(leagues['secondhalf']['avg_goals_per_game_scored']['@away'])
				},
				'avg_goals_per_game_conceded': None if (leagues['secondhalf'].get("avg_goals_per_game_conceded") is None) or (leagues['secondhalf']['avg_goals_per_game_conceded'] is None) or (not leagues['secondhalf']['avg_goals_per_game_conceded']) else {
					'total': None if (leagues['secondhalf']['avg_goals_per_game_conceded'].get("@total") is None) or (leagues['secondhalf']['avg_goals_per_game_conceded']['@total'] is None) or (not leagues['secondhalf']['avg_goals_per_game_conceded']['@total']) else float(leagues['secondhalf']['avg_goals_per_game_conceded']['@total']),
					'home': None if (leagues['secondhalf']['avg_goals_per_game_conceded'].get("@home") is None) or (leagues['secondhalf']['avg_goals_per_game_conceded']['@home'] is None) or (not leagues['secondhalf']['avg_goals_per_game_conceded']['@home']) else float(leagues['secondhalf']['avg_goals_per_game_conceded']['@home']),
					'away': None if (leagues['secondhalf']['avg_goals_per_game_conceded'].get("@away") is None) or (leagues['secondhalf']['avg_goals_per_game_conceded']['@away'] is None) or (not leagues['secondhalf']['avg_goals_per_game_conceded']['@away']) else float(leagues['secondhalf']['avg_goals_per_game_conceded']['@away'])
				},
				'failed_to_score': None if (leagues['secondhalf'].get("failed_to_score") is None) or (leagues['secondhalf']['failed_to_score'] is None) or (not leagues['secondhalf']['failed_to_score']) else {
					'total': None if (leagues['secondhalf']['failed_to_score'].get("@total") is None) or (leagues['secondhalf']['failed_to_score']['@total'] is None) or (not leagues['secondhalf']['failed_to_score']['@total']) else int(leagues['secondhalf']['failed_to_score']['@total']),
					'home': None if (leagues['secondhalf']['failed_to_score'].get("@home") is None) or (leagues['secondhalf']['failed_to_score']['@home'] is None) or (not leagues['secondhalf']['failed_to_score']['@home']) else int(leagues['secondhalf']['failed_to_score']['@home']),
					'away': None if (leagues['secondhalf']['failed_to_score'].get("@away") is None) or (leagues['secondhalf']['failed_to_score']['@away'] is None) or (not leagues['secondhalf']['failed_to_score']['@away']) else int(leagues['secondhalf']['failed_to_score']['@away'])
				},
				'shotsTotal': None if (leagues['secondhalf'].get("shotsTotal") is None) or (leagues['secondhalf']['shotsTotal'] is None) or (not leagues['secondhalf']['shotsTotal']) else {
					'total': None if (leagues['secondhalf']['shotsTotal'].get("@total") is None) or (leagues['secondhalf']['shotsTotal']['@total'] is None) or (not leagues['secondhalf']['shotsTotal']['@total']) else int(leagues['secondhalf']['shotsTotal']['@total']),
					'home': None if (leagues['secondhalf']['shotsTotal'].get("@home") is None) or (leagues['secondhalf']['shotsTotal']['@home'] is None) or (not leagues['secondhalf']['shotsTotal']['@home']) else int(leagues['secondhalf']['shotsTotal']['@home']),
					'away': None if (leagues['secondhalf']['shotsTotal'].get("@away") is None) or (leagues['secondhalf']['shotsTotal']['@away'] is None) or (not leagues['secondhalf']['shotsTotal']['@away']) else int(leagues['secondhalf']['shotsTotal']['@away'])
				},
				'shotsOnGoal': None if (leagues['secondhalf'].get("shotsOnGoal") is None) or (leagues['secondhalf']['shotsOnGoal'] is None) or (not leagues['secondhalf']['shotsOnGoal']) else {
					'total': None if (leagues['secondhalf']['shotsOnGoal'].get("@total") is None) or (leagues['secondhalf']['shotsOnGoal']['@total'] is None) or (not leagues['secondhalf']['shotsOnGoal']['@total']) else int(leagues['secondhalf']['shotsOnGoal']['@total']),
					'home': None if (leagues['secondhalf']['shotsOnGoal'].get("@home") is None) or (leagues['secondhalf']['shotsOnGoal']['@home'] is None) or (not leagues['secondhalf']['shotsOnGoal']['@home']) else int(leagues['secondhalf']['shotsOnGoal']['@home']),
					'away': None if (leagues['secondhalf']['shotsOnGoal'].get("@away") is None) or (leagues['secondhalf']['shotsOnGoal']['@away'] is None) or (not leagues['secondhalf']['shotsOnGoal']['@away']) else int(leagues['secondhalf']['shotsOnGoal']['@away'])
				},
				'corners': None if (leagues['secondhalf'].get("corners") is None) or (leagues['secondhalf']['corners'] is None) or (not leagues['secondhalf']['corners']) else {
					'total': None if (leagues['secondhalf']['corners'].get("@total") is None) or (leagues['secondhalf']['corners']['@total'] is None) or (not leagues['secondhalf']['corners']['@total']) else int(leagues['secondhalf']['corners']['@total']),
					'home': None if (leagues['secondhalf']['corners'].get("@home") is None) or (leagues['secondhalf']['corners']['@home'] is None) or (not leagues['secondhalf']['corners']['@home']) else int(leagues['secondhalf']['corners']['@home']),
					'away': None if (leagues['secondhalf']['corners'].get("@away") is None) or (leagues['secondhalf']['corners']['@away'] is None) or (not leagues['secondhalf']['corners']['@away']) else int(leagues['secondhalf']['corners']['@away'])
				},
				'avg_corners': None if (leagues['secondhalf'].get("avg_corners") is None) or (leagues['secondhalf']['avg_corners'] is None) or (not leagues['secondhalf']['avg_corners']) else {
					'total': None if (leagues['secondhalf']['avg_corners'].get("@total") is None) or (leagues['secondhalf']['avg_corners']['@total'] is None) or (not leagues['secondhalf']['avg_corners']['@total']) else float(leagues['secondhalf']['avg_corners']['@total']),
					'home': None if (leagues['secondhalf']['avg_corners'].get("@home") is None) or (leagues['secondhalf']['avg_corners']['@home'] is None) or (not leagues['secondhalf']['avg_corners']['@home']) else float(leagues['secondhalf']['avg_corners']['@home']),
					'away': None if (leagues['secondhalf']['avg_corners'].get("@away") is None) or (leagues['secondhalf']['avg_corners']['@away'] is None) or (not leagues['secondhalf']['avg_corners']['@away']) else float(leagues['secondhalf']['avg_corners']['@away'])
				},
				'offsides': None if (leagues['secondhalf'].get("offsides") is None) or (leagues['secondhalf']['offsides'] is None) or (not leagues['secondhalf']['offsides']) else {
					'total': None if (leagues['secondhalf']['offsides'].get("@total") is None) or (leagues['secondhalf']['offsides']['@total'] is None) or (not leagues['secondhalf']['offsides']['@total']) else int(leagues['secondhalf']['offsides']['@total']),
					'home': None if (leagues['secondhalf']['offsides'].get("@home") is None) or (leagues['secondhalf']['offsides']['@home'] is None) or (not leagues['secondhalf']['offsides']['@home']) else int(leagues['secondhalf']['offsides']['@home']),
					'away': None if (leagues['secondhalf']['offsides'].get("@away") is None) or (leagues['secondhalf']['offsides']['@away'] is None) or (not leagues['secondhalf']['offsides']['@away']) else int(leagues['secondhalf']['offsides']['@away'])
				},
				'possession': None if (leagues['secondhalf'].get("possession") is None) or (leagues['secondhalf']['possession'] is None) or (not leagues['secondhalf']['possession']) else {
					'total': None if (leagues['secondhalf']['possession'].get("@total") is None) or (leagues['secondhalf']['possession']['@total'] is None) or (not leagues['secondhalf']['possession']['@total']) else int(leagues['secondhalf']['possession']['@total']),
					'home': None if (leagues['secondhalf']['possession'].get("@home") is None) or (leagues['secondhalf']['possession']['@home'] is None) or (not leagues['secondhalf']['possession']['@home']) else int(leagues['secondhalf']['possession']['@home']),
					'away': None if (leagues['secondhalf']['possession'].get("@away") is None) or (leagues['secondhalf']['possession']['@away'] is None) or (not leagues['secondhalf']['possession']['@away']) else int(leagues['secondhalf']['possession']['@away'])
				},
				'fouls': None if (leagues['secondhalf'].get("fouls") is None) or (leagues['secondhalf']['fouls'] is None) or (not leagues['secondhalf']['fouls']) else {
					'total': None if (leagues['secondhalf']['fouls'].get("@total") is None) or (leagues['secondhalf']['fouls']['@total'] is None) or (not leagues['secondhalf']['fouls']['@total']) else int(leagues['secondhalf']['fouls']['@total']),
					'home': None if (leagues['secondhalf']['fouls'].get("@home") is None) or (leagues['secondhalf']['fouls']['@home'] is None) or (not leagues['secondhalf']['fouls']['@home']) else int(leagues['secondhalf']['fouls']['@home']),
					'away': None if (leagues['secondhalf']['fouls'].get("@away") is None) or (leagues['secondhalf']['fouls']['@away'] is None) or (not leagues['secondhalf']['fouls']['@away']) else int(leagues['secondhalf']['fouls']['@away'])
				},
				'yellowcards': None if (leagues['secondhalf'].get("yellowcards") is None) or (leagues['secondhalf']['yellowcards'] is None) or (not leagues['secondhalf']['yellowcards']) else {
					'total': None if (leagues['secondhalf']['yellowcards'].get("@total") is None) or (leagues['secondhalf']['yellowcards']['@total'] is None) or (not leagues['secondhalf']['yellowcards']['@total']) else int(leagues['secondhalf']['yellowcards']['@total']),
					'home': None if (leagues['secondhalf']['yellowcards'].get("@home") is None) or (leagues['secondhalf']['yellowcards']['@home'] is None) or (not leagues['secondhalf']['yellowcards']['@home']) else int(leagues['secondhalf']['yellowcards']['@home']),
					'away': None if (leagues['secondhalf']['yellowcards'].get("@away") is None) or (leagues['secondhalf']['yellowcards']['@away'] is None) or (not leagues['secondhalf']['yellowcards']['@away']) else int(leagues['secondhalf']['yellowcards']['@away'])
				},
				'redcards': None if (leagues['secondhalf'].get("redcards") is None) or (leagues['secondhalf']['redcards'] is None) or (not leagues['secondhalf']['redcards']) else {
					'total': None if (leagues['secondhalf']['redcards'].get("@total") is None) or (leagues['secondhalf']['redcards']['@total'] is None) or (not leagues['secondhalf']['redcards']['@total']) else int(leagues['secondhalf']['redcards']['@total']),
					'home': None if (leagues['secondhalf']['redcards'].get("@home") is None) or (leagues['secondhalf']['redcards']['@home'] is None) or (not leagues['secondhalf']['redcards']['@home']) else int(leagues['secondhalf']['redcards']['@home']),
					'away': None if (leagues['secondhalf']['redcards'].get("@away") is None) or (leagues['secondhalf']['redcards']['@away'] is None) or (not leagues['secondhalf']['redcards']['@away']) else int(leagues['secondhalf']['redcards']['@away'])
				},
				'avg_yellowcards': None if (leagues['secondhalf'].get("avg_yellowcards") is None) or (leagues['secondhalf']['avg_yellowcards'] is None) or (not leagues['secondhalf']['avg_yellowcards']) else {
					'total': None if (leagues['secondhalf']['avg_yellowcards'].get("@total") is None) or (leagues['secondhalf']['avg_yellowcards']['@total'] is None) or (not leagues['secondhalf']['avg_yellowcards']['@total']) else float(leagues['secondhalf']['avg_yellowcards']['@total']),
					'home': None if (leagues['secondhalf']['avg_yellowcards'].get("@home") is None) or (leagues['secondhalf']['avg_yellowcards'].get("@home") is None) or (leagues['secondhalf']['avg_yellowcards']['@home'] is None) or (not leagues['secondhalf']['avg_yellowcards']['@home']) else float(leagues['secondhalf']['avg_yellowcards']['@home']),
					'away': None if (leagues['secondhalf']['avg_yellowcards'].get("@away") is None) or (leagues['secondhalf']['avg_yellowcards'].get("@away") is None) or (leagues['secondhalf']['avg_yellowcards']['@away'] is None) or (not leagues['secondhalf']['avg_yellowcards']['@away']) else float(leagues['secondhalf']['avg_yellowcards']['@away'])
				},
				'avg_redcards': None if (leagues['secondhalf'].get("avg_redcards") is None) or (leagues['secondhalf']['avg_redcards'] is None) or (not leagues['secondhalf']['avg_redcards']) else {
					'total': None if (leagues['secondhalf']['avg_redcards'].get("@total") is None) or (leagues['secondhalf']['avg_redcards']['@total'] is None) or (not leagues['secondhalf']['avg_redcards']['@total']) else float(leagues['secondhalf']['avg_redcards']['@total']),
					'home': None if (leagues['secondhalf']['avg_redcards'].get("@home") is None) or (leagues['secondhalf']['avg_redcards'].get("@home") is None) or (leagues['secondhalf']['avg_redcards']['@home'] is None) or (not leagues['secondhalf']['avg_redcards']['@home']) else float(leagues['secondhalf']['avg_redcards']['@home']),
					'away': None if (leagues['secondhalf']['avg_redcards'].get("@away") is None) or (leagues['secondhalf']['avg_redcards'].get("@away") is None) or (leagues['secondhalf']['avg_redcards']['@away'] is None) or (not leagues['secondhalf']['avg_redcards']['@away']) else float(leagues['secondhalf']['avg_redcards']['@away'])
				}
			},
			'scoring_minutes': None if (leagues.get("scoring_minutes") is None) or (leagues['scoring_minutes'] is None) or (not leagues['scoring_minutes']) else {
				'period': None if (leagues['scoring_minutes'].get("period") is None) or (leagues['scoring_minutes']['period'] is None) or (not leagues['scoring_minutes']['period']) else scoringPeriod(leagues['scoring_minutes']['period'])
			},
			'goals_conceded_minutes': None if (leagues.get("goals_conceded_minutes") is None) or (leagues['goals_conceded_minutes'] is None) or (not leagues['goals_conceded_minutes']) else {
				'period': None if (leagues['goals_conceded_minutes'].get("period") is None) or (leagues['goals_conceded_minutes']['period'] is None) or (not leagues['goals_conceded_minutes']['period']) else scoringPeriod(leagues['goals_conceded_minutes']['period'])
			},
			'yellowcard_minutes': None if (leagues.get("yellowcard_minutes") is None) or (leagues['yellowcard_minutes'] is None) or (not leagues['yellowcard_minutes']) else {
				'period': None if (leagues['yellowcard_minutes'].get("period") is None) or (leagues['yellowcard_minutes']['period'] is None) or (not leagues['yellowcard_minutes']['period']) else scoringPeriod(leagues['yellowcard_minutes']['period'])
			},
			'redcard_minutes': None if (leagues.get("redcard_minutes") is None) or (leagues['redcard_minutes'] is None) or (not leagues['redcard_minutes']) else {
				'period': None if (leagues['redcard_minutes'].get("period") is None) or (leagues['redcard_minutes']['period'] is None) or (not leagues['redcard_minutes']['period']) else scoringPeriod(leagues['redcard_minutes']['period'])
			}
		}
		return [data]
	if type(leagues) is list:
			for info in leagues:
				data = {
					'name': None if (info.get("@name") is None) or (info['@name'] is None) or (not info['@name']) else info['@name'],
					'season': None if (info.get("@season") is None) or (info['@season'] is None) or (not info['@season']) else info['@season'],
					'id': None if (info.get("@id") is None) or (info['@id'] is None) or (not info['@id']) else int(info['@id']),
					'fulltime': None if (info.get("fulltime") is None) or (info['fulltime'] is None) or (not info['fulltime']) else {
						'win': None if (info['fulltime'].get("win") is None) or (info['fulltime']['win'] is None) or (not info['fulltime']['win']) else {
							'total': None if (info['fulltime']['win'].get("@total") is None) or (info['fulltime']['win']['@total'] is None) or (not info['fulltime']['win']['@total']) else int(info['fulltime']['win']['@total']),
							'home': None if (info['fulltime']['win'].get("@home") is None) or (info['fulltime']['win']['@home'] is None) or (not info['fulltime']['win']['@home']) else int(info['fulltime']['win']['@home']),
							'away': None if (info['fulltime']['win'].get("@away") is None) or (info['fulltime']['win']['@away'] is None) or (not info['fulltime']['win']['@away']) else int(info['fulltime']['win']['@away'])
						},
						'lost': None if (info['fulltime'].get("lost") is None) or (info['fulltime']['lost'] is None) or (not info['fulltime']['lost']) else {
							'total': None if (info['fulltime']['lost'].get("@total") is None) or (info['fulltime']['lost']['@total'] is None) or (not info['fulltime']['lost']['@total']) else int(info['fulltime']['lost']['@total']),
							'home': None if (info['fulltime']['lost'].get("@home") is None) or (info['fulltime']['lost']['@home'] is None) or (not info['fulltime']['lost']['@home']) else int(info['fulltime']['lost']['@home']),
							'away': None if (info['fulltime']['lost'].get("@away") is None) or (info['fulltime']['lost']['@away'] is None) or (not info['fulltime']['lost']['@away']) else int(info['fulltime']['lost']['@away'])
						},
						'draw': None if(info['fulltime'].get("draw") is None) or  (info['fulltime']['draw'] is None) or (not info['fulltime']['draw']) else {
							'total': None if (info['fulltime']['draw'].get("@total") is None) or (info['fulltime']['draw']['@total'] is None) or (not info['fulltime']['draw']['@total']) else int(info['fulltime']['draw']['@total']),
							'home': None if (info['fulltime']['draw'].get("@home") is None) or (info['fulltime']['draw']['@home'] is None) or (not info['fulltime']['draw']['@home']) else int(info['fulltime']['draw']['@home']),
							'away': None if (info['fulltime']['draw'].get("@away") is None) or (info['fulltime']['draw']['@away'] is None) or (not info['fulltime']['draw']['@away']) else int(info['fulltime']['draw']['@away'])
						},
						'goals_for': None if (info['fulltime'].get("goals_for") is None) or (info['fulltime']['goals_for'] is None) or (not info['fulltime']['goals_for']) else {
							'total': None if (info['fulltime']['goals_for'].get("@total") is None) or (info['fulltime']['goals_for']['@total'] is None) or (not info['fulltime']['goals_for']['@total']) else int(info['fulltime']['goals_for']['@total']),
							'home': None if (info['fulltime']['goals_for'].get("@home") is None) or (info['fulltime']['goals_for']['@home'] is None) or (not info['fulltime']['goals_for']['@home']) else int(info['fulltime']['goals_for']['@home']),
							'away': None if (info['fulltime']['goals_for'].get("@away") is None) or (info['fulltime']['goals_for']['@away'] is None) or (not info['fulltime']['goals_for']['@away']) else int(info['fulltime']['goals_for']['@away'])
						},
						'goals_against': None if (info['fulltime'].get("goals_against") is None) or (info['fulltime']['goals_against'] is None) or (not info['fulltime']['goals_against']) else {
							'total': None if (info['fulltime']['goals_against'].get("@total") is None) or (info['fulltime']['goals_against']['@total'] is None) or (not info['fulltime']['goals_against']['@total']) else int(info['fulltime']['goals_against']['@total']),
							'home': None if (info['fulltime']['goals_against'].get("@home") is None) or (info['fulltime']['goals_against']['@home'] is None) or (not info['fulltime']['goals_against']['@home']) else int(info['fulltime']['goals_against']['@home']),
							'away': None if (info['fulltime']['goals_against'].get("@away") is None) or (info['fulltime']['goals_against']['@away'] is None) or (not info['fulltime']['goals_against']['@away']) else int(info['fulltime']['goals_against']['@away'])
						},
						'clean_sheet': None if (info['fulltime'].get("clean_sheet") is None) or (info['fulltime']['clean_sheet'] is None) or (not info['fulltime']['clean_sheet']) else {
							'total': None if (info['fulltime']['clean_sheet'].get("@total") is None) or (info['fulltime']['clean_sheet']['@total'] is None) or (not info['fulltime']['clean_sheet']['@total']) else int(info['fulltime']['clean_sheet']['@total']),
							'home': None if (info['fulltime']['clean_sheet'].get("@home") is None) or (info['fulltime']['clean_sheet']['@home'] is None) or (not info['fulltime']['clean_sheet']['@home']) else int(info['fulltime']['clean_sheet']['@home']),
							'away': None if (info['fulltime']['clean_sheet'].get("@away") is None) or (info['fulltime']['clean_sheet']['@away'] is None) or (not info['fulltime']['clean_sheet']['@away']) else int(info['fulltime']['clean_sheet']['@away'])
						},
						'avg_goals_per_game_scored': None if (info['fulltime'].get("avg_goals_per_game_scored") is None) or (info['fulltime']['avg_goals_per_game_scored'] is None) or (not info['fulltime']['avg_goals_per_game_scored']) else {
							'total': None if (info['fulltime']['avg_goals_per_game_scored'].get("@total") is None) or (info['fulltime']['avg_goals_per_game_scored']['@total'] is None) or (not info['fulltime']['avg_goals_per_game_scored']['@total']) else float(info['fulltime']['avg_goals_per_game_scored']['@total']),
							'home': None if (info['fulltime']['avg_goals_per_game_scored'].get("@home") is None) or (info['fulltime']['avg_goals_per_game_scored']['@home'] is None) or (not info['fulltime']['avg_goals_per_game_scored']['@home']) else float(info['fulltime']['avg_goals_per_game_scored']['@home']),
							'away': None if (info['fulltime']['avg_goals_per_game_scored'].get("@away") is None) or (info['fulltime']['avg_goals_per_game_scored']['@away'] is None) or (not info['fulltime']['avg_goals_per_game_scored']['@away']) else float(info['fulltime']['avg_goals_per_game_scored']['@away'])
						},
						'avg_goals_per_game_conceded': None if (info['fulltime'].get("avg_goals_per_game_conceded") is None) or (info['fulltime']['avg_goals_per_game_conceded'] is None) or (not info['fulltime']['avg_goals_per_game_conceded']) else {
							'total': None if (info['fulltime']['avg_goals_per_game_scored'].get("@total") is None) or (info['fulltime']['avg_goals_per_game_conceded']['@total'] is None) or (not info['fulltime']['avg_goals_per_game_conceded']['@total']) else float(info['fulltime']['avg_goals_per_game_conceded']['@total']),
							'home': None if (info['fulltime']['avg_goals_per_game_scored'].get("@home") is None) or (info['fulltime']['avg_goals_per_game_conceded']['@home'] is None) or (not info['fulltime']['avg_goals_per_game_conceded']['@home']) else float(info['fulltime']['avg_goals_per_game_conceded']['@home']),
							'away': None if (info['fulltime']['avg_goals_per_game_scored'].get("@away") is None) or (info['fulltime']['avg_goals_per_game_conceded']['@away'] is None) or (not info['fulltime']['avg_goals_per_game_conceded']['@away']) else float(info['fulltime']['avg_goals_per_game_conceded']['@away'])
						},
						'biggest_victory': None if (info['fulltime'].get("biggest_victory") is None) or (info['fulltime']['biggest_victory'] is None) or (not info['fulltime']['biggest_victory']) else {
							'total': None if (info['fulltime']['biggest_victory'].get("@total") is None) or (info['fulltime']['biggest_victory']['@total'] is None) or (not info['fulltime']['biggest_victory']['@total']) else info['fulltime']['biggest_victory']['@total'],
							'home': None if (info['fulltime']['biggest_victory'].get("@home") is None) or (info['fulltime']['biggest_victory']['@home'] is None) or (not info['fulltime']['biggest_victory']['@home']) else info['fulltime']['biggest_victory']['@home'],
							'away': None if (info['fulltime']['biggest_victory'].get("@away") is None) or (info['fulltime']['biggest_victory']['@away'] is None) or (not info['fulltime']['biggest_victory']['@away']) else info['fulltime']['biggest_victory']['@away']
						},
						'biggest_defeat': None if (info['fulltime'].get("biggest_defeat") is None) or (info['fulltime']['biggest_defeat'] is None) or (not info['fulltime']['biggest_defeat']) else {
							'total': None if (info['fulltime']['biggest_defeat'].get("@total") is None) or (info['fulltime']['biggest_defeat']['@total'] is None) or (not info['fulltime']['biggest_defeat']['@total']) else info['fulltime']['biggest_defeat']['@total'],
							'home': None if (info['fulltime']['biggest_defeat'].get("@home") is None) or (info['fulltime']['biggest_defeat']['@home'] is None) or (not info['fulltime']['biggest_defeat']['@home']) else info['fulltime']['biggest_defeat']['@home'],
							'away': None if (info['fulltime']['biggest_defeat'].get("@away") is None) or (info['fulltime']['biggest_defeat']['@away'] is None) or (not info['fulltime']['biggest_defeat']['@away']) else info['fulltime']['biggest_defeat']['@away']
						},
						'avg_first_goal_scored': None if (info['fulltime'].get("avg_first_goal_scored") is None) or (info['fulltime']['avg_first_goal_scored'] is None) or (not info['fulltime']['avg_first_goal_scored']) else {
							'total': None if (info['fulltime']['avg_first_goal_scored'].get("@total") is None) or (info['fulltime']['avg_first_goal_scored']['@total'] is None) or (not info['fulltime']['avg_first_goal_scored']['@total']) else int(info['fulltime']['avg_first_goal_scored']['@total']),
							'home': None if (info['fulltime']['avg_first_goal_scored'].get("@home") is None) or (info['fulltime']['avg_first_goal_scored']['@home'] is None) or (not info['fulltime']['avg_first_goal_scored']['@home']) else int(info['fulltime']['avg_first_goal_scored']['@home']),
							'away': None if (info['fulltime']['avg_first_goal_scored'].get("@away") is None) or (info['fulltime']['avg_first_goal_scored']['@away'] is None) or (not info['fulltime']['avg_first_goal_scored']['@away']) else int(info['fulltime']['avg_first_goal_scored']['@away'])
						},
						'avg_first_goal_conceded': None if (info['fulltime'].get("avg_first_goal_conceded") is None) or (info['fulltime']['avg_first_goal_conceded'] is None) or (not info['fulltime']['avg_first_goal_conceded']) else {
							'total': None if (info['fulltime']['avg_first_goal_conceded'].get("@total") is None) or (info['fulltime']['avg_first_goal_conceded']['@total'] is None) or (not info['fulltime']['avg_first_goal_conceded']['@total']) else int(info['fulltime']['avg_first_goal_conceded']['@total']),
							'home': None if (info['fulltime']['avg_first_goal_conceded'].get("@home") is None) or (info['fulltime']['avg_first_goal_conceded']['@home'] is None) or (not info['fulltime']['avg_first_goal_conceded']['@home']) else int(info['fulltime']['avg_first_goal_conceded']['@home']),
							'away': None if (info['fulltime']['avg_first_goal_conceded'].get("@away") is None) or (info['fulltime']['avg_first_goal_conceded']['@away'] is None) or (not info['fulltime']['avg_first_goal_conceded']['@away']) else int(info['fulltime']['avg_first_goal_conceded']['@away'])
						},
						'failed_to_score': None if (info['fulltime'].get("failed_to_score") is None) or (info['fulltime']['failed_to_score'] is None) or (not info['fulltime']['failed_to_score']) else {
							'total': None if (info['fulltime']['failed_to_score'].get("@total") is None) or (info['fulltime']['failed_to_score']['@total'] is None) or (not info['fulltime']['failed_to_score']['@total']) else int(info['fulltime']['failed_to_score']['@total']),
							'home': None if (info['fulltime']['failed_to_score'].get("@home") is None) or (info['fulltime']['failed_to_score']['@home'] is None) or (not info['fulltime']['failed_to_score']['@home']) else int(info['fulltime']['failed_to_score']['@home']),
							'away': None if (info['fulltime']['failed_to_score'].get("@away") is None) or (info['fulltime']['failed_to_score']['@away'] is None) or (not info['fulltime']['failed_to_score']['@away']) else int(info['fulltime']['failed_to_score']['@away'])
						},
						'shotsTotal': None if (info['fulltime'].get("shotsTotal") is None) or (info['fulltime']['shotsTotal'] is None) or (not info['fulltime']['shotsTotal']) else {
							'total': None if (info['fulltime']['shotsTotal'].get("@total") is None) or (info['fulltime']['shotsTotal']['@total'] is None) or (not info['fulltime']['shotsTotal']['@total']) else int(info['fulltime']['shotsTotal']['@total']),
							'home': None if (info['fulltime']['shotsTotal'].get("@home") is None) or (info['fulltime']['shotsTotal']['@home'] is None) or (not info['fulltime']['shotsTotal']['@home']) else int(info['fulltime']['shotsTotal']['@home']),
							'away': None if (info['fulltime']['shotsTotal'].get("@away") is None) or (info['fulltime']['shotsTotal']['@away'] is None) or (not info['fulltime']['shotsTotal']['@away']) else int(info['fulltime']['shotsTotal']['@away'])
						},
						'shotsOnGoal': None if (info['fulltime'].get("shotsOnGoal") is None) or (info['fulltime']['shotsOnGoal'] is None) or (not info['fulltime']['shotsOnGoal']) else {
							'total': None if (info['fulltime']['shotsOnGoal'].get("@total") is None) or (info['fulltime']['shotsOnGoal']['@total'] is None) or (not info['fulltime']['shotsOnGoal']['@total']) else int(info['fulltime']['shotsOnGoal']['@total']),
							'home': None if (info['fulltime']['shotsOnGoal'].get("@home") is None) or (info['fulltime']['shotsOnGoal']['@home'] is None) or (not info['fulltime']['shotsOnGoal']['@home']) else int(info['fulltime']['shotsOnGoal']['@home']),
							'away': None if (info['fulltime']['shotsOnGoal'].get("@away") is None) or (info['fulltime']['shotsOnGoal']['@away'] is None) or (not info['fulltime']['shotsOnGoal']['@away']) else int(info['fulltime']['shotsOnGoal']['@away'])
						},
						'corners': None if (info['fulltime'].get("corners") is None) or (info['fulltime']['corners'] is None) or (not info['fulltime']['corners']) else {
							'total': None if (info['fulltime']['corners'].get("@total") is None) or (info['fulltime']['corners']['@total'] is None) or (not info['fulltime']['corners']['@total']) else int(info['fulltime']['corners']['@total']),
							'home': None if (info['fulltime']['corners'].get("@home") is None) or (info['fulltime']['corners']['@home'] is None) or (not info['fulltime']['corners']['@home']) else int(info['fulltime']['corners']['@home']),
							'away': None if (info['fulltime']['corners'].get("@away") is None) or (info['fulltime']['corners']['@away'] is None) or (not info['fulltime']['corners']['@away']) else int(info['fulltime']['corners']['@away'])
						},
						'avg_corners': None if (info['fulltime'].get("avg_corners") is None) or (info['fulltime']['avg_corners'] is None) or (not info['fulltime']['avg_corners']) else {
							'total': None if (info['fulltime']['avg_corners'].get("@total") is None) or (info['fulltime']['avg_corners']['@total'] is None) or (not info['fulltime']['avg_corners']['@total']) else float(info['fulltime']['avg_corners']['@total']),
							'home': None if (info['fulltime']['avg_corners'].get("@home") is None) or (info['fulltime']['avg_corners']['@home'] is None) or (not info['fulltime']['avg_corners']['@home']) else float(info['fulltime']['avg_corners']['@home']),
							'away': None if (info['fulltime']['avg_corners'].get("@away") is None) or (info['fulltime']['avg_corners']['@away'] is None) or (not info['fulltime']['avg_corners']['@away']) else float(info['fulltime']['avg_corners']['@away'])
						},
						'offsides': None if (info['fulltime'].get("offsides") is None) or (info['fulltime']['offsides'] is None) or (not info['fulltime']['offsides']) else {
							'total': None if (info['fulltime']['offsides'].get("@total") is None) or (info['fulltime']['offsides']['@total'] is None) or (not info['fulltime']['offsides']['@total']) else int(info['fulltime']['offsides']['@total']),
							'home': None if (info['fulltime']['offsides'].get("@home") is None) or (info['fulltime']['offsides']['@home'] is None) or (not info['fulltime']['offsides']['@home']) else int(info['fulltime']['offsides']['@home']),
							'away': None if (info['fulltime']['offsides'].get("@away") is None) or (info['fulltime']['offsides']['@away'] is None) or (not info['fulltime']['offsides']['@away']) else int(info['fulltime']['offsides']['@away'])
						},
						'possession': None if (info['fulltime'].get("possession") is None) or (info['fulltime']['possession'] is None) or (not info['fulltime']['possession']) else {
							'total': None if (info['fulltime']['possession'].get("@total") is None) or (info['fulltime']['possession']['@total'] is None) or (not info['fulltime']['possession']['@total']) else int(info['fulltime']['possession']['@total']),
							'home': None if (info['fulltime']['possession'].get("@home") is None) or (info['fulltime']['possession']['@home'] is None) or (not info['fulltime']['possession']['@home']) else int(info['fulltime']['possession']['@home']),
							'away': None if (info['fulltime']['possession'].get("@away") is None) or (info['fulltime']['possession']['@away'] is None) or (not info['fulltime']['possession']['@away']) else int(info['fulltime']['possession']['@away'])
						},
						'fouls': None if (info['fulltime'].get("fouls") is None) or (info['fulltime']['fouls'] is None) or (not info['fulltime']['fouls']) else {
							'total': None if (info['fulltime']['fouls'].get("@total") is None) or (info['fulltime']['fouls']['@total'] is None) or (not info['fulltime']['fouls']['@total']) else int(info['fulltime']['fouls']['@total']),
							'home': None if (info['fulltime']['fouls'].get("@home") is None) or (info['fulltime']['fouls']['@home'] is None) or (not info['fulltime']['fouls']['@home']) else int(info['fulltime']['fouls']['@home']),
							'away': None if (info['fulltime']['fouls'].get("@away") is None) or (info['fulltime']['fouls']['@away'] is None) or (not info['fulltime']['fouls']['@away']) else int(info['fulltime']['fouls']['@away'])
						},
						'yellowcards': None if (info['fulltime'].get("yellowcards") is None) or (info['fulltime']['yellowcards'] is None) or (not info['fulltime']['yellowcards']) else {
							'total': None if (info['fulltime']['yellowcards'].get("@total") is None) or (info['fulltime']['yellowcards']['@total'] is None) or (not info['fulltime']['yellowcards']['@total']) else int(info['fulltime']['yellowcards']['@total']),
							'home': None if (info['fulltime']['yellowcards'].get("@home") is None) or (info['fulltime']['yellowcards']['@home'] is None) or (not info['fulltime']['yellowcards']['@home']) else int(info['fulltime']['yellowcards']['@home']),
							'away': None if (info['fulltime']['yellowcards'].get("@away") is None) or (info['fulltime']['yellowcards']['@away'] is None) or (not info['fulltime']['yellowcards']['@away']) else int(info['fulltime']['yellowcards']['@away'])
						},
						'redcards': None if (info['fulltime'].get("redcards") is None) or (info['fulltime']['redcards'] is None) or (not info['fulltime']['redcards']) else {
							'total': None if (info['fulltime']['redcards'].get("@total") is None) or (info['fulltime']['redcards']['@total'] is None) or (not info['fulltime']['redcards']['@total']) else int(info['fulltime']['redcards']['@total']),
							'home': None if (info['fulltime']['redcards'].get("@total") is None) or (info['fulltime']['redcards']['@home'] is None) or (not info['fulltime']['redcards']['@home']) else int(info['fulltime']['redcards']['@home']),
							'away': None if (info['fulltime']['redcards'].get("@total") is None) or (info['fulltime']['redcards']['@away'] is None) or (not info['fulltime']['redcards']['@away']) else int(info['fulltime']['redcards']['@away'])
						},
						'avg_yellowcards': None if (info['fulltime'].get("avg_yellowcards") is None) or (info['fulltime']['avg_yellowcards'] is None) or (not info['fulltime']['avg_yellowcards']) else {
							'total': None if (info['fulltime']['avg_yellowcards'].get("@total") is None) or (info['fulltime']['avg_yellowcards']['@total'] is None) or (not info['fulltime']['avg_yellowcards']['@total']) else float(info['fulltime']['avg_yellowcards']['@total']),
							'home': None if (info['fulltime']['avg_yellowcards'].get("@home") is None) or (info['fulltime']['avg_yellowcards']['@home'] is None) or (not info['fulltime']['avg_yellowcards']['@home']) else float(info['fulltime']['avg_yellowcards']['@home']),
							'away': None if (info['fulltime']['avg_yellowcards'].get("@away") is None) or (info['fulltime']['avg_yellowcards']['@away'] is None) or (not info['fulltime']['avg_yellowcards']['@away']) else float(info['fulltime']['avg_yellowcards']['@away'])
						},
						'avg_redcards': None if (info['fulltime'].get("avg_redcards") is None) or (info['fulltime']['avg_redcards'] is None) or (not info['fulltime']['avg_redcards']) else {
							'total': None if (info['fulltime']['avg_redcards'].get("@total") is None) or (info['fulltime']['avg_redcards']['@total'] is None) or (not info['fulltime']['avg_redcards']['@total']) else float(info['fulltime']['avg_redcards']['@total']),
							'home': None if (info['fulltime']['avg_redcards'].get("@home") is None) or (info['fulltime']['avg_redcards']['@home'] is None) or (not info['fulltime']['avg_redcards']['@home']) else float(info['fulltime']['avg_redcards']['@home']),
							'away': None if (info['fulltime']['avg_redcards'].get("@away") is None) or (info['fulltime']['avg_redcards']['@away'] is None) or (not info['fulltime']['avg_redcards']['@away']) else float(info['fulltime']['avg_redcards']['@away'])
						}
					},
					'firsthalf': None if (info.get("firsthalf") is None) or (info['firsthalf'] is None) or (not info['firsthalf']) else {
						'win': None if (info['firsthalf'].get("win") is None) or (info['firsthalf']['win'] is None) or (not info['firsthalf']['win']) else {
							'total': None if (info['firsthalf']['win'].get("@total") is None) or (info['firsthalf']['win']['@total'] is None) or (not info['firsthalf']['win']['@total']) else int(info['firsthalf']['win']['@total']),
							'home': None if (info['firsthalf']['win'].get("@home") is None) or (info['firsthalf']['win']['@home'] is None) or (not info['firsthalf']['win']['@home']) else int(info['firsthalf']['win']['@home']),
							'away': None if (info['firsthalf']['win'].get("@away") is None) or (info['firsthalf']['win']['@away'] is None) or (not info['firsthalf']['win']['@away']) else int(info['firsthalf']['win']['@away'])
						},
						'lost': None if (info['firsthalf'].get("lost") is None) or (info['firsthalf']['lost'] is None) or (not info['firsthalf']['lost']) else {
							'total': None if (info['firsthalf']['lost'].get("@total") is None) or (info['firsthalf']['lost']['@total'] is None) or (not info['firsthalf']['lost']['@total']) else int(info['firsthalf']['lost']['@total']),
							'home': None if (info['firsthalf']['lost'].get("@home") is None) or (info['firsthalf']['lost']['@home'] is None) or (not info['firsthalf']['lost']['@home']) else int(info['firsthalf']['lost']['@home']),
							'away': None if (info['firsthalf']['lost'].get("@away") is None) or (info['firsthalf']['lost']['@away'] is None) or (not info['firsthalf']['lost']['@away']) else int(info['firsthalf']['lost']['@away'])
						},
						'draw': None if (info['firsthalf'].get("draw") is None) or (info['firsthalf']['draw'] is None) or (not info['firsthalf']['draw']) else {
							'total': None if (info['firsthalf']['draw'].get("@total") is None) or (info['firsthalf']['draw']['@total'] is None) or (not info['firsthalf']['draw']['@total']) else int(info['firsthalf']['draw']['@total']),
							'home': None if (info['firsthalf']['draw'].get("@home") is None) or (info['firsthalf']['draw']['@home'] is None) or (not info['firsthalf']['draw']['@home']) else int(info['firsthalf']['draw']['@home']),
							'away': None if (info['firsthalf']['draw'].get("@away") is None) or (info['firsthalf']['draw']['@away'] is None) or (not info['firsthalf']['draw']['@away']) else int(info['firsthalf']['draw']['@away'])
						},
						'win_halftime': None if (info['firsthalf'].get("win_halftime") is None) or (info['firsthalf']['win_halftime'] is None) or (not info['firsthalf']['win_halftime']) else {
							'ft_win': None if (info['firsthalf']['win_halftime'].get("@ft_win") is None) or (info['firsthalf']['win_halftime']['@ft_win'] is None) or (not info['firsthalf']['win_halftime']['@ft_win']) else int(info['firsthalf']['win_halftime']['@ft_win']),
							'ft_draw': None if (info['firsthalf']['win_halftime'].get("@ft_draw") is None) or (info['firsthalf']['win_halftime']['@ft_draw'] is None) or (not info['firsthalf']['win_halftime']['@ft_draw']) else int(info['firsthalf']['win_halftime']['@ft_draw']),
							'ft_lost': None if (info['firsthalf']['win_halftime'].get("@ft_lost") is None) or (info['firsthalf']['win_halftime']['@ft_lost'] is None) or (not info['firsthalf']['win_halftime']['@ft_lost']) else int(info['firsthalf']['win_halftime']['@ft_lost'])
						},
						'draw_halftime': None if (info['firsthalf'].get("draw_halftime") is None) or (info['firsthalf']['draw_halftime'] is None) or (not info['firsthalf']['draw_halftime']) else {
							'ft_win': None if (info['firsthalf']['draw_halftime'].get("@ft_win") is None) or (info['firsthalf']['draw_halftime']['@ft_win'] is None) or (not info['firsthalf']['draw_halftime']['@ft_win']) else int(info['firsthalf']['draw_halftime']['@ft_win']),
							'ft_draw': None if (info['firsthalf']['draw_halftime'].get("@ft_draw") is None) or (info['firsthalf']['draw_halftime']['@ft_draw'] is None) or (not info['firsthalf']['draw_halftime']['@ft_draw']) else int(info['firsthalf']['draw_halftime']['@ft_draw']),
							'ft_lost': None if (info['firsthalf']['draw_halftime'].get("@ft_lost") is None) or (info['firsthalf']['draw_halftime']['@ft_lost'] is None) or (not info['firsthalf']['draw_halftime']['@ft_lost']) else int(info['firsthalf']['draw_halftime']['@ft_lost'])
						},
						'lost_halftime': None if (info['firsthalf'].get("lost_halftime") is None) or (info['firsthalf']['lost_halftime'] is None) or (not info['firsthalf']['lost_halftime']) else {
							'ft_win': None if (info['firsthalf']['lost_halftime'].get("@ft_win") is None) or (info['firsthalf']['lost_halftime']['@ft_win'] is None) or (not info['firsthalf']['lost_halftime']['@ft_win']) else int(info['firsthalf']['lost_halftime']['@ft_win']),
							'ft_draw': None if (info['firsthalf']['lost_halftime'].get("@ft_draw") is None) or (info['firsthalf']['lost_halftime']['@ft_draw'] is None) or (not info['firsthalf']['lost_halftime']['@ft_draw']) else int(info['firsthalf']['lost_halftime']['@ft_draw']),
							'ft_lost': None if (info['firsthalf']['lost_halftime'].get("@ft_lost") is None) or (info['firsthalf']['lost_halftime']['@ft_lost'] is None) or (not info['firsthalf']['lost_halftime']['@ft_lost']) else int(info['firsthalf']['lost_halftime']['@ft_lost'])
						},
						'goals_for': None if (info['firsthalf'].get("goals_for") is None) or (info['firsthalf']['goals_for'] is None) or (not info['firsthalf']['goals_for']) else {
							'total': None if (info['firsthalf']['goals_for'].get("@total") is None) or (info['firsthalf']['goals_for']['@total'] is None) or (not info['firsthalf']['goals_for']['@total']) else int(info['firsthalf']['goals_for']['@total']),
							'home': None if (info['firsthalf']['goals_for'].get("@home") is None) or (info['firsthalf']['goals_for']['@home'] is None) or (not info['firsthalf']['goals_for']['@home']) else int(info['firsthalf']['goals_for']['@home']),
							'away': None if (info['firsthalf']['goals_for'].get("@away") is None) or (info['firsthalf']['goals_for']['@away'] is None) or (not info['firsthalf']['goals_for']['@away']) else int(info['firsthalf']['goals_for']['@away'])
						},
						'goals_against': None if (info['firsthalf'].get("goals_against") is None) or (info['firsthalf']['goals_against'] is None) or (not info['firsthalf']['goals_against']) else {
							'total': None if (info['firsthalf']['goals_against'].get("@total") is None) or (info['firsthalf']['goals_against']['@total'] is None) or (not info['firsthalf']['goals_against']['@total']) else int(info['firsthalf']['goals_against']['@total']),
							'home': None if (info['firsthalf']['goals_against'].get("@home") is None) or (info['firsthalf']['goals_against']['@home'] is None) or (not info['firsthalf']['goals_against']['@home']) else int(info['firsthalf']['goals_against']['@home']),
							'away': None if (info['firsthalf']['goals_against'].get("@away") is None) or (info['firsthalf']['goals_against']['@away'] is None) or (not info['firsthalf']['goals_against']['@away']) else int(info['firsthalf']['goals_against']['@away'])
						},
						'goals_for_additiional_time': None if (info['firsthalf'].get("goals_for_additiional_time") is None) or (info['firsthalf']['goals_for_additiional_time'] is None) or (not info['firsthalf']['goals_for_additiional_time']) else {
							'total': None if (info['firsthalf']['goals_for_additiional_time'].get("@total") is None) or (info['firsthalf']['goals_for_additiional_time']['@total'] is None) or (not info['firsthalf']['goals_for_additiional_time']['@total']) else int(info['firsthalf']['goals_for_additiional_time']['@total']),
							'home': None if (info['firsthalf']['goals_for_additiional_time'].get("@home") is None) or (info['firsthalf']['goals_for_additiional_time']['@home'] is None) or (not info['firsthalf']['goals_for_additiional_time']['@home']) else int(info['firsthalf']['goals_for_additiional_time']['@home']),
							'away': None if (info['firsthalf']['goals_for_additiional_time'].get("@away") is None) or (info['firsthalf']['goals_for_additiional_time']['@away'] is None) or (not info['firsthalf']['goals_for_additiional_time']['@away']) else int(info['firsthalf']['goals_for_additiional_time']['@away'])
						},
						'goals_against_additiional_time': None if (info['firsthalf'].get("goals_against_additiional_time") is None) or (info['firsthalf']['goals_against_additiional_time'] is None) or (not info['firsthalf']['goals_against_additiional_time']) else {
							'total': None if (info['firsthalf']['goals_against_additiional_time'].get("@total") is None) or (info['firsthalf']['goals_against_additiional_time']['@total'] is None) or (not info['firsthalf']['goals_against_additiional_time']['@total']) else int(info['firsthalf']['goals_against_additiional_time']['@total']),
							'home': None if (info['firsthalf']['goals_against_additiional_time'].get("@home") is None) or (info['firsthalf']['goals_against_additiional_time']['@home'] is None) or (not info['firsthalf']['goals_against_additiional_time']['@home']) else int(info['firsthalf']['goals_against_additiional_time']['@home']),
							'away': None if (info['firsthalf']['goals_against_additiional_time'].get("@away") is None) or (info['firsthalf']['goals_against_additiional_time']['@away'] is None) or (not info['firsthalf']['goals_against_additiional_time']['@away']) else int(info['firsthalf']['goals_against_additiional_time']['@away'])
						},
						'clean_sheet': None if (info['firsthalf'].get("clean_sheet") is None) or (info['firsthalf']['clean_sheet'] is None) or (not info['firsthalf']['clean_sheet']) else {
							'total': None if (info['firsthalf']['clean_sheet'].get("@total") is None) or (info['firsthalf']['clean_sheet']['@total'] is None) or (not info['firsthalf']['clean_sheet']['@total']) else int(info['firsthalf']['clean_sheet']['@total']),
							'home': None if (info['firsthalf']['clean_sheet'].get("@home") is None) or (info['firsthalf']['clean_sheet']['@home'] is None) or (not info['firsthalf']['clean_sheet']['@home']) else int(info['firsthalf']['clean_sheet']['@home']),
							'away': None if (info['firsthalf']['clean_sheet'].get("@away") is None) or (info['firsthalf']['clean_sheet']['@away'] is None) or (not info['firsthalf']['clean_sheet']['@away']) else int(info['firsthalf']['clean_sheet']['@away'])
						},
						'avg_goals_per_game_scored': None if (info['firsthalf'].get("avg_goals_per_game_scored") is None) or (info['firsthalf']['avg_goals_per_game_scored'] is None) or (not info['firsthalf']['avg_goals_per_game_scored']) else {
							'total': None if (info['firsthalf']['avg_goals_per_game_scored'].get("@total") is None) or (info['firsthalf']['avg_goals_per_game_scored']['@total'] is None) or (not info['firsthalf']['avg_goals_per_game_scored']['@total']) else float(info['firsthalf']['avg_goals_per_game_scored']['@total']),
							'home': None if (info['firsthalf']['avg_goals_per_game_scored'].get("@home") is None) or (info['firsthalf']['avg_goals_per_game_scored']['@home'] is None) or (not info['firsthalf']['avg_goals_per_game_scored']['@home']) else float(info['firsthalf']['avg_goals_per_game_scored']['@home']),
							'away': None if (info['firsthalf']['avg_goals_per_game_scored'].get("@away") is None) or (info['firsthalf']['avg_goals_per_game_scored']['@away'] is None) or (not info['firsthalf']['avg_goals_per_game_scored']['@away']) else float(info['firsthalf']['avg_goals_per_game_scored']['@away'])
						},
						'avg_goals_per_game_conceded': None if (info['firsthalf'].get("avg_goals_per_game_conceded") is None) or (info['firsthalf']['avg_goals_per_game_conceded'] is None) or (not info['firsthalf']['avg_goals_per_game_conceded']) else {
							'total': None if (info['firsthalf']['avg_goals_per_game_conceded'].get("@total") is None) or (info['firsthalf']['avg_goals_per_game_conceded']['@total'] is None) or (not info['firsthalf']['avg_goals_per_game_conceded']['@total']) else float(info['firsthalf']['avg_goals_per_game_conceded']['@total']),
							'home': None if (info['firsthalf']['avg_goals_per_game_conceded'].get("@home") is None) or (info['firsthalf']['avg_goals_per_game_conceded']['@home'] is None) or (not info['firsthalf']['avg_goals_per_game_conceded']['@home']) else float(info['firsthalf']['avg_goals_per_game_conceded']['@home']),
							'away': None if (info['firsthalf']['avg_goals_per_game_conceded'].get("@away") is None) or (info['firsthalf']['avg_goals_per_game_conceded']['@away'] is None) or (not info['firsthalf']['avg_goals_per_game_conceded']['@away']) else float(info['firsthalf']['avg_goals_per_game_conceded']['@away'])
						},
						'failed_to_score': None if (info['firsthalf'].get("failed_to_score") is None) or (info['firsthalf']['failed_to_score'] is None) or (not info['firsthalf']['failed_to_score']) else {
							'total': None if (info['firsthalf']['failed_to_score'].get("@total") is None) or (info['firsthalf']['failed_to_score']['@total'] is None) or (not info['firsthalf']['failed_to_score']['@total']) else int(info['firsthalf']['failed_to_score']['@total']),
							'home': None if (info['firsthalf']['failed_to_score'].get("@home") is None) or (info['firsthalf']['failed_to_score']['@home'] is None) or (not info['firsthalf']['failed_to_score']['@home']) else int(info['firsthalf']['failed_to_score']['@home']),
							'away': None if (info['firsthalf']['failed_to_score'].get("@away") is None) or (info['firsthalf']['failed_to_score']['@away'] is None) or (not info['firsthalf']['failed_to_score']['@away']) else int(info['firsthalf']['failed_to_score']['@away'])
						},
						'shotsTotal': None if (info['firsthalf'].get("shotsTotal") is None) or (info['firsthalf']['shotsTotal'] is None) or (not info['firsthalf']['shotsTotal']) else {
							'total': None if (info['firsthalf']['shotsTotal'].get("@total") is None) or (info['firsthalf']['shotsTotal']['@total'] is None) or (not info['firsthalf']['shotsTotal']['@total']) else int(info['firsthalf']['shotsTotal']['@total']),
							'home': None if (info['firsthalf']['shotsTotal'].get("@home") is None) or (info['firsthalf']['shotsTotal']['@home'] is None) or (not info['firsthalf']['shotsTotal']['@home']) else int(info['firsthalf']['shotsTotal']['@home']),
							'away': None if (info['firsthalf']['shotsTotal'].get("@away") is None) or (info['firsthalf']['shotsTotal']['@away'] is None) or (not info['firsthalf']['shotsTotal']['@away']) else int(info['firsthalf']['shotsTotal']['@away'])
						},
						'shotsOnGoal': None if (info['firsthalf'].get("shotsOnGoal") is None) or (info['firsthalf']['shotsOnGoal'] is None) or (not info['firsthalf']['shotsOnGoal']) else {
							'total': None if (info['firsthalf']['shotsOnGoal'].get("@total") is None) or (info['firsthalf']['shotsOnGoal']['@total'] is None) or (not info['firsthalf']['shotsOnGoal']['@total']) else int(info['firsthalf']['shotsOnGoal']['@total']),
							'home': None if (info['firsthalf']['shotsOnGoal'].get("@home") is None) or (info['firsthalf']['shotsOnGoal']['@home'] is None) or (not info['firsthalf']['shotsOnGoal']['@home']) else int(info['firsthalf']['shotsOnGoal']['@home']),
							'away': None if (info['firsthalf']['shotsOnGoal'].get("@away") is None) or (info['firsthalf']['shotsOnGoal']['@away'] is None) or (not info['firsthalf']['shotsOnGoal']['@away']) else int(info['firsthalf']['shotsOnGoal']['@away'])
						},
						'corners': None if (info['firsthalf'].get("corners") is None) or (info['firsthalf']['corners'] is None) or (not info['firsthalf']['corners']) else {
							'total': None if (info['firsthalf']['corners'].get("@total") is None) or (info['firsthalf']['corners']['@total'] is None) or (not info['firsthalf']['corners']['@total']) else int(info['firsthalf']['corners']['@total']),
							'home': None if (info['firsthalf']['corners'].get("@home") is None) or (info['firsthalf']['corners']['@home'] is None) or (not info['firsthalf']['corners']['@home']) else int(info['firsthalf']['corners']['@home']),
							'away': None if (info['firsthalf']['corners'].get("@away") is None) or (info['firsthalf']['corners']['@away'] is None) or (not info['firsthalf']['corners']['@away']) else int(info['firsthalf']['corners']['@away'])
						},
						'avg_corners': None if (info['firsthalf'].get("avg_corners") is None) or (info['firsthalf']['avg_corners'] is None) or (not info['firsthalf']['avg_corners']) else {
							'total': None if (info['firsthalf']['avg_corners'].get("@total") is None) or (info['firsthalf']['avg_corners']['@total'] is None) or (not info['firsthalf']['avg_corners']['@total']) else float(info['firsthalf']['avg_corners']['@total']),
							'home': None if (info['firsthalf']['avg_corners'].get("@home") is None) or (info['firsthalf']['avg_corners']['@home'] is None) or (not info['firsthalf']['avg_corners']['@home']) else float(info['firsthalf']['avg_corners']['@home']),
							'away': None if (info['firsthalf']['avg_corners'].get("@away") is None) or (info['firsthalf']['avg_corners']['@away'] is None) or (not info['firsthalf']['avg_corners']['@away']) else float(info['firsthalf']['avg_corners']['@away'])
						},
						'offsides': None if (info['firsthalf'].get("offsides") is None) or (info['firsthalf']['offsides'] is None) or (not info['firsthalf']['offsides']) else {
							'total': None if (info['firsthalf']['offsides'].get("@total") is None) or (info['firsthalf']['offsides']['@total'] is None) or (not info['firsthalf']['offsides']['@total']) else int(info['firsthalf']['offsides']['@total']),
							'home': None if (info['firsthalf']['offsides'].get("@home") is None) or (info['firsthalf']['offsides']['@home'] is None) or (not info['firsthalf']['offsides']['@home']) else int(info['firsthalf']['offsides']['@home']),
							'away': None if (info['firsthalf']['offsides'].get("@away") is None) or (info['firsthalf']['offsides']['@away'] is None) or (not info['firsthalf']['offsides']['@away']) else int(info['firsthalf']['offsides']['@away'])
						},
						'possession': None if (info['firsthalf'].get("possession") is None) or (info['firsthalf']['possession'] is None) or (not info['firsthalf']['possession']) else {
							'total': None if (info['firsthalf']['possession'].get("@total") is None) or (info['firsthalf']['possession']['@total'] is None) or (not info['firsthalf']['possession']['@total']) else int(info['firsthalf']['possession']['@total']),
							'home': None if (info['firsthalf']['possession'].get("@home") is None) or (info['firsthalf']['possession']['@home'] is None) or (not info['firsthalf']['possession']['@home']) else int(info['firsthalf']['possession']['@home']),
							'away': None if (info['firsthalf']['possession'].get("@away") is None) or (info['firsthalf']['possession']['@away'] is None) or (not info['firsthalf']['possession']['@away']) else int(info['firsthalf']['possession']['@away'])
						},
						'fouls': None if (info['firsthalf'].get("fouls") is None) or (info['firsthalf']['fouls'] is None) or (not info['firsthalf']['fouls']) else {
							'total': None if (info['firsthalf']['fouls'].get("@total") is None) or (info['firsthalf']['fouls']['@total'] is None) or (not info['firsthalf']['fouls']['@total']) else int(info['firsthalf']['fouls']['@total']),
							'home': None if (info['firsthalf']['fouls'].get("@home") is None) or (info['firsthalf']['fouls']['@home'] is None) or (not info['firsthalf']['fouls']['@home']) else int(info['firsthalf']['fouls']['@home']),
							'away': None if (info['firsthalf']['fouls'].get("@away") is None) or (info['firsthalf']['fouls']['@away'] is None) or (not info['firsthalf']['fouls']['@away']) else int(info['firsthalf']['fouls']['@away'])
						},
						'yellowcards': None if (info['firsthalf'].get("yellowcards") is None) or (info['firsthalf']['yellowcards'] is None) or (not info['firsthalf']['yellowcards']) else {
							'total': None if (info['firsthalf']['yellowcards'].get("@total") is None) or (info['firsthalf']['yellowcards']['@total'] is None) or (not info['firsthalf']['yellowcards']['@total']) else int(info['firsthalf']['yellowcards']['@total']),
							'home': None if (info['firsthalf']['yellowcards'].get("@home") is None) or (info['firsthalf']['yellowcards']['@home'] is None) or (not info['firsthalf']['yellowcards']['@home']) else int(info['firsthalf']['yellowcards']['@home']),
							'away': None if (info['firsthalf']['yellowcards'].get("@away") is None) or (info['firsthalf']['yellowcards']['@away'] is None) or (not info['firsthalf']['yellowcards']['@away']) else int(info['firsthalf']['yellowcards']['@away'])
						},
						'redcards': None if (info['firsthalf'].get("redcards") is None) or (info['firsthalf']['redcards'] is None) or (not info['firsthalf']['redcards']) else {
							'total': None if (info['firsthalf']['redcards'].get("@total") is None) or (info['firsthalf']['redcards']['@total'] is None) or (not info['firsthalf']['redcards']['@total']) else int(info['firsthalf']['redcards']['@total']),
							'home': None if (info['firsthalf']['redcards'].get("@home") is None) or (info['firsthalf']['redcards']['@home'] is None) or (not info['firsthalf']['redcards']['@home']) else int(info['firsthalf']['redcards']['@home']),
							'away': None if (info['firsthalf']['redcards'].get("@away") is None) or (info['firsthalf']['redcards']['@away'] is None) or (not info['firsthalf']['redcards']['@away']) else int(info['firsthalf']['redcards']['@away'])
						},
						'avg_yellowcards': None if (info['firsthalf'].get("avg_yellowcards") is None) or (info['firsthalf']['avg_yellowcards'] is None) or (not info['firsthalf']['avg_yellowcards']) else {
							'total': None if (info['firsthalf']['avg_yellowcards'].get("@total") is None) or (info['firsthalf']['avg_yellowcards']['@total'] is None) or (not info['firsthalf']['avg_yellowcards']['@total']) else float(info['firsthalf']['avg_yellowcards']['@total']),
							'home': None if (info['firsthalf']['avg_yellowcards'].get("@home") is None) or (info['firsthalf']['avg_yellowcards']['@home'] is None) or (not info['firsthalf']['avg_yellowcards']['@home']) else float(info['firsthalf']['avg_yellowcards']['@home']),
							'away': None if (info['firsthalf']['avg_yellowcards'].get("@away") is None) or (info['firsthalf']['avg_yellowcards']['@away'] is None) or (not info['firsthalf']['avg_yellowcards']['@away']) else float(info['firsthalf']['avg_yellowcards']['@away'])
						},
						'avg_redcards': None if (info['firsthalf'].get("avg_redcards") is None) or (info['firsthalf']['avg_redcards'] is None) or (not info['firsthalf']['avg_redcards']) else {
							'total': None if (info['firsthalf']['avg_redcards'].get("@total") is None) or (info['firsthalf']['avg_redcards']['@total'] is None) or (not info['firsthalf']['avg_redcards']['@total']) else float(info['firsthalf']['avg_redcards']['@total']),
							'home': None if (info['firsthalf']['avg_redcards'].get("@home") is None) or (info['firsthalf']['avg_redcards']['@home'] is None) or (not info['firsthalf']['avg_redcards']['@home']) else float(info['firsthalf']['avg_redcards']['@home']),
							'away': None if (info['firsthalf']['avg_redcards'].get("@away") is None) or (info['firsthalf']['avg_redcards']['@away'] is None) or (not info['firsthalf']['avg_redcards']['@away']) else float(info['firsthalf']['avg_redcards']['@away'])
						}
					},
					'secondhalf': None if (info.get("secondhalf") is None) or (info['secondhalf'] is None) or (not info['secondhalf']) else {
						'win': None if (info['secondhalf'].get("win") is None) or (info['secondhalf']['win'] is None) or (not info['secondhalf']['win']) else {
							'total': None if (info['secondhalf']['win'].get("@total") is None) or (info['secondhalf']['win']['@total'] is None) or (not info['secondhalf']['win']['@total']) else int(info['secondhalf']['win']['@total']),
							'home': None if (info['secondhalf']['win'].get("@home") is None) or (info['secondhalf']['win']['@home'] is None) or (not info['secondhalf']['win']['@home']) else int(info['secondhalf']['win']['@home']),
							'away': None if (info['secondhalf']['win'].get("@away") is None) or (info['secondhalf']['win']['@away'] is None) or (not info['secondhalf']['win']['@away']) else int(info['secondhalf']['win']['@away'])
						},
						'lost': None if(info['secondhalf'].get("lost") is None) or  (info['secondhalf']['lost'] is None) or (not info['secondhalf']['lost']) else {
							'total': None if (info['secondhalf']['lost'].get("@total") is None) or (info['secondhalf']['lost']['@total'] is None) or (not info['secondhalf']['lost']['@total']) else int(info['secondhalf']['lost']['@total']),
							'home': None if (info['secondhalf']['lost'].get("@home") is None) or (info['secondhalf']['lost']['@home'] is None) or (not info['secondhalf']['lost']['@home']) else int(info['secondhalf']['lost']['@home']),
							'away': None if (info['secondhalf']['lost'].get("@away") is None) or (info['secondhalf']['lost']['@away'] is None) or (not info['secondhalf']['lost']['@away']) else int(info['secondhalf']['lost']['@away'])
						},
						'draw': None if (info['secondhalf'].get("draw") is None) or (info['secondhalf']['draw'] is None) or (not info['secondhalf']['draw']) else {
							'total': None if (info['secondhalf']['draw'].get("@total") is None) or (info['secondhalf']['draw']['@total'] is None) or (not info['secondhalf']['draw']['@total']) else int(info['secondhalf']['draw']['@total']),
							'home': None if (info['secondhalf']['draw'].get("@home") is None) or (info['secondhalf']['draw']['@home'] is None) or (not info['secondhalf']['draw']['@home']) else int(info['secondhalf']['draw']['@home']),
							'away': None if (info['secondhalf']['draw'].get("@away") is None) or (info['secondhalf']['draw']['@away'] is None) or (not info['secondhalf']['draw']['@away']) else int(info['secondhalf']['draw']['@away'])
						},
						'goals_for': None if (info['secondhalf'].get("goals_for") is None) or (info['secondhalf']['goals_for'] is None) or (not info['secondhalf']['goals_for']) else {
							'total': None if (info['secondhalf']['goals_for'].get("@total") is None) or (info['secondhalf']['goals_for']['@total'] is None) or (not info['secondhalf']['goals_for']['@total']) else int(info['secondhalf']['goals_for']['@total']),
							'home': None if (info['secondhalf']['goals_for'].get("@home") is None) or (info['secondhalf']['goals_for']['@home'] is None) or (not info['secondhalf']['goals_for']['@home']) else int(info['secondhalf']['goals_for']['@home']),
							'away': None if (info['secondhalf']['goals_for'].get("@away") is None) or (info['secondhalf']['goals_for']['@away'] is None) or (not info['secondhalf']['goals_for']['@away']) else int(info['secondhalf']['goals_for']['@away'])
						},
						'goals_against': None if (info['secondhalf'].get("goals_against") is None) or (info['secondhalf']['goals_against'] is None) or (not info['secondhalf']['goals_against']) else {
							'total': None if (info['secondhalf']['goals_against'].get("@total") is None) or (info['secondhalf']['goals_against']['@total'] is None) or (not info['secondhalf']['goals_against']['@total']) else int(info['secondhalf']['goals_against']['@total']),
							'home': None if (info['secondhalf']['goals_against'].get("@home") is None) or (info['secondhalf']['goals_against']['@home'] is None) or (not info['secondhalf']['goals_against']['@home']) else int(info['secondhalf']['goals_against']['@home']),
							'away': None if (info['secondhalf']['goals_against'].get("@away") is None) or (info['secondhalf']['goals_against']['@away'] is None) or (not info['secondhalf']['goals_against']['@away']) else int(info['secondhalf']['goals_against']['@away'])
						},
						'goals_for_additiional_time': None if (info['secondhalf'].get("goals_for_additiional_time") is None) or (info['secondhalf']['goals_for_additiional_time'] is None) or (not info['secondhalf']['goals_for_additiional_time']) else {
							'total': None if (info['secondhalf']['goals_for_additiional_time'].get("@total") is None) or (info['secondhalf']['goals_for_additiional_time']['@total'] is None) or (not info['secondhalf']['goals_for_additiional_time']['@total']) else int(info['secondhalf']['goals_for_additiional_time']['@total']),
							'home': None if (info['secondhalf']['goals_for_additiional_time'].get("@home") is None) or (info['secondhalf']['goals_for_additiional_time']['@home'] is None) or (not info['secondhalf']['goals_for_additiional_time']['@home']) else int(info['secondhalf']['goals_for_additiional_time']['@home']),
							'away': None if (info['secondhalf']['goals_for_additiional_time'].get("@away") is None) or (info['secondhalf']['goals_for_additiional_time']['@away'] is None) or (not info['secondhalf']['goals_for_additiional_time']['@away']) else int(info['secondhalf']['goals_for_additiional_time']['@away'])
						},
						'goals_against_additiional_time': None if (info['secondhalf'].get("goals_against_additiional_time") is None) or (info['secondhalf']['goals_against_additiional_time'] is None) or (not info['secondhalf']['goals_against_additiional_time']) else {
							'total': None if (info['secondhalf']['goals_against_additiional_time'].get("@total") is None) or (info['secondhalf']['goals_against_additiional_time']['@total'] is None) or (not info['secondhalf']['goals_against_additiional_time']['@total']) else int(info['secondhalf']['goals_against_additiional_time']['@total']),
							'home': None if (info['secondhalf']['goals_against_additiional_time'].get("@home") is None) or (info['secondhalf']['goals_against_additiional_time']['@home'] is None) or (not info['secondhalf']['goals_against_additiional_time']['@home']) else int(info['secondhalf']['goals_against_additiional_time']['@home']),
							'away': None if (info['secondhalf']['goals_against_additiional_time'].get("@away") is None) or (info['secondhalf']['goals_against_additiional_time']['@away'] is None) or (not info['secondhalf']['goals_against_additiional_time']['@away']) else int(info['secondhalf']['goals_against_additiional_time']['@away'])
						},
						'clean_sheet': None if (info['secondhalf'].get("clean_sheet") is None) or (info['secondhalf']['clean_sheet'] is None) or (not info['secondhalf']['clean_sheet']) else {
							'total': None if (info['secondhalf']['clean_sheet'].get("@total") is None) or (info['secondhalf']['clean_sheet']['@total'] is None) or (not info['secondhalf']['clean_sheet']['@total']) else int(info['secondhalf']['clean_sheet']['@total']),
							'home': None if (info['secondhalf']['clean_sheet'].get("@home") is None) or (info['secondhalf']['clean_sheet']['@home'] is None) or (not info['secondhalf']['clean_sheet']['@home']) else int(info['secondhalf']['clean_sheet']['@home']),
							'away': None if (info['secondhalf']['clean_sheet'].get("@away") is None) or (info['secondhalf']['clean_sheet']['@away'] is None) or (not info['secondhalf']['clean_sheet']['@away']) else int(info['secondhalf']['clean_sheet']['@away'])
						},
						'avg_goals_per_game_scored': None if (info['secondhalf'].get("avg_goals_per_game_scored") is None) or (info['secondhalf']['avg_goals_per_game_scored'] is None) or (not info['secondhalf']['avg_goals_per_game_scored']) else {
							'total': None if (info['secondhalf']['avg_goals_per_game_scored'].get("@total") is None) or (info['secondhalf']['avg_goals_per_game_scored']['@total'] is None) or (not info['secondhalf']['avg_goals_per_game_scored']['@total']) else float(info['secondhalf']['avg_goals_per_game_scored']['@total']),
							'home': None if (info['secondhalf']['avg_goals_per_game_scored'].get("@home") is None) or (info['secondhalf']['avg_goals_per_game_scored']['@home'] is None) or (not info['secondhalf']['avg_goals_per_game_scored']['@home']) else float(info['secondhalf']['avg_goals_per_game_scored']['@home']),
							'away': None if (info['secondhalf']['avg_goals_per_game_scored'].get("@away") is None) or (info['secondhalf']['avg_goals_per_game_scored']['@away'] is None) or (not info['secondhalf']['avg_goals_per_game_scored']['@away']) else float(info['secondhalf']['avg_goals_per_game_scored']['@away'])
						},
						'avg_goals_per_game_conceded': None if (info['secondhalf'].get("avg_goals_per_game_conceded") is None) or (info['secondhalf']['avg_goals_per_game_conceded'] is None) or (not info['secondhalf']['avg_goals_per_game_conceded']) else {
							'total': None if (info['secondhalf']['avg_goals_per_game_conceded'].get("@total") is None) or (info['secondhalf']['avg_goals_per_game_conceded']['@total'] is None) or (not info['secondhalf']['avg_goals_per_game_conceded']['@total']) else float(info['secondhalf']['avg_goals_per_game_conceded']['@total']),
							'home': None if (info['secondhalf']['avg_goals_per_game_conceded'].get("@home") is None) or (info['secondhalf']['avg_goals_per_game_conceded']['@home'] is None) or (not info['secondhalf']['avg_goals_per_game_conceded']['@home']) else float(info['secondhalf']['avg_goals_per_game_conceded']['@home']),
							'away': None if (info['secondhalf']['avg_goals_per_game_conceded'].get("@away") is None) or (info['secondhalf']['avg_goals_per_game_conceded']['@away'] is None) or (not info['secondhalf']['avg_goals_per_game_conceded']['@away']) else float(info['secondhalf']['avg_goals_per_game_conceded']['@away'])
						},
						'failed_to_score': None if (info['secondhalf'].get("failed_to_score") is None) or (info['secondhalf']['failed_to_score'] is None) or (not info['secondhalf']['failed_to_score']) else {
							'total': None if (info['secondhalf']['failed_to_score'].get("@total") is None) or (info['secondhalf']['failed_to_score']['@total'] is None) or (not info['secondhalf']['failed_to_score']['@total']) else int(info['secondhalf']['failed_to_score']['@total']),
							'home': None if (info['secondhalf']['failed_to_score'].get("@home") is None) or (info['secondhalf']['failed_to_score']['@home'] is None) or (not info['secondhalf']['failed_to_score']['@home']) else int(info['secondhalf']['failed_to_score']['@home']),
							'away': None if (info['secondhalf']['failed_to_score'].get("@away") is None) or (info['secondhalf']['failed_to_score']['@away'] is None) or (not info['secondhalf']['failed_to_score']['@away']) else int(info['secondhalf']['failed_to_score']['@away'])
						},
						'shotsTotal': None if (info['secondhalf'].get("shotsTotal") is None) or (info['secondhalf']['shotsTotal'] is None) or (not info['secondhalf']['shotsTotal']) else {
							'total': None if (info['secondhalf']['shotsTotal'].get("@total") is None) or (info['secondhalf']['shotsTotal']['@total'] is None) or (not info['secondhalf']['shotsTotal']['@total']) else int(info['secondhalf']['shotsTotal']['@total']),
							'home': None if (info['secondhalf']['shotsTotal'].get("@home") is None) or (info['secondhalf']['shotsTotal']['@home'] is None) or (not info['secondhalf']['shotsTotal']['@home']) else int(info['secondhalf']['shotsTotal']['@home']),
							'away': None if (info['secondhalf']['shotsTotal'].get("@away") is None) or (info['secondhalf']['shotsTotal']['@away'] is None) or (not info['secondhalf']['shotsTotal']['@away']) else int(info['secondhalf']['shotsTotal']['@away'])
						},
						'shotsOnGoal': None if (info['secondhalf'].get("shotsOnGoal") is None) or (info['secondhalf']['shotsOnGoal'] is None) or (not info['secondhalf']['shotsOnGoal']) else {
							'total': None if (info['secondhalf']['shotsOnGoal'].get("@total") is None) or (info['secondhalf']['shotsOnGoal']['@total'] is None) or (not info['secondhalf']['shotsOnGoal']['@total']) else int(info['secondhalf']['shotsOnGoal']['@total']),
							'home': None if (info['secondhalf']['shotsOnGoal'].get("@home") is None) or (info['secondhalf']['shotsOnGoal']['@home'] is None) or (not info['secondhalf']['shotsOnGoal']['@home']) else int(info['secondhalf']['shotsOnGoal']['@home']),
							'away': None if (info['secondhalf']['shotsOnGoal'].get("@away") is None) or (info['secondhalf']['shotsOnGoal']['@away'] is None) or (not info['secondhalf']['shotsOnGoal']['@away']) else int(info['secondhalf']['shotsOnGoal']['@away'])
						},
						'corners': None if (info['secondhalf'].get("corners") is None) or (info['secondhalf']['corners'] is None) or (not info['secondhalf']['corners']) else {
							'total': None if (info['secondhalf']['corners'].get("@total") is None) or (info['secondhalf']['corners']['@total'] is None) or (not info['secondhalf']['corners']['@total']) else int(info['secondhalf']['corners']['@total']),
							'home': None if (info['secondhalf']['corners'].get("@home") is None) or (info['secondhalf']['corners']['@home'] is None) or (not info['secondhalf']['corners']['@home']) else int(info['secondhalf']['corners']['@home']),
							'away': None if (info['secondhalf']['corners'].get("@away") is None) or (info['secondhalf']['corners']['@away'] is None) or (not info['secondhalf']['corners']['@away']) else int(info['secondhalf']['corners']['@away'])
						},
						'avg_corners': None if (info['secondhalf'].get("avg_corners") is None) or (info['secondhalf']['avg_corners'] is None) or (not info['secondhalf']['avg_corners']) else {
							'total': None if (info['secondhalf']['avg_corners'].get("@total") is None) or (info['secondhalf']['avg_corners']['@total'] is None) or (not info['secondhalf']['avg_corners']['@total']) else float(info['secondhalf']['avg_corners']['@total']),
							'home': None if (info['secondhalf']['avg_corners'].get("@home") is None) or (info['secondhalf']['avg_corners']['@home'] is None) or (not info['secondhalf']['avg_corners']['@home']) else float(info['secondhalf']['avg_corners']['@home']),
							'away': None if (info['secondhalf']['avg_corners'].get("@away") is None) or (info['secondhalf']['avg_corners']['@away'] is None) or (not info['secondhalf']['avg_corners']['@away']) else float(info['secondhalf']['avg_corners']['@away'])
						},
						'offsides': None if (info['secondhalf'].get("offsides") is None) or (info['secondhalf']['offsides'] is None) or (not info['secondhalf']['offsides']) else {
							'total': None if (info['secondhalf']['offsides'].get("@total") is None) or (info['secondhalf']['offsides']['@total'] is None) or (not info['secondhalf']['offsides']['@total']) else int(info['secondhalf']['offsides']['@total']),
							'home': None if (info['secondhalf']['offsides'].get("@home") is None) or (info['secondhalf']['offsides']['@home'] is None) or (not info['secondhalf']['offsides']['@home']) else int(info['secondhalf']['offsides']['@home']),
							'away': None if (info['secondhalf']['offsides'].get("@away") is None) or (info['secondhalf']['offsides']['@away'] is None) or (not info['secondhalf']['offsides']['@away']) else int(info['secondhalf']['offsides']['@away'])
						},
						'possession': None if (info['secondhalf'].get("possession") is None) or (info['secondhalf']['possession'] is None) or (not info['secondhalf']['possession']) else {
							'total': None if (info['secondhalf']['possession'].get("@total") is None) or (info['secondhalf']['possession']['@total'] is None) or (not info['secondhalf']['possession']['@total']) else int(info['secondhalf']['possession']['@total']),
							'home': None if (info['secondhalf']['possession'].get("@home") is None) or (info['secondhalf']['possession']['@home'] is None) or (not info['secondhalf']['possession']['@home']) else int(info['secondhalf']['possession']['@home']),
							'away': None if (info['secondhalf']['possession'].get("@away") is None) or (info['secondhalf']['possession']['@away'] is None) or (not info['secondhalf']['possession']['@away']) else int(info['secondhalf']['possession']['@away'])
						},
						'fouls': None if (info['secondhalf'].get("fouls") is None) or (info['secondhalf']['fouls'] is None) or (not info['secondhalf']['fouls']) else {
							'total': None if (info['secondhalf']['fouls'].get("@total") is None) or (info['secondhalf']['fouls']['@total'] is None) or (not info['secondhalf']['fouls']['@total']) else int(info['secondhalf']['fouls']['@total']),
							'home': None if (info['secondhalf']['fouls'].get("@home") is None) or (info['secondhalf']['fouls']['@home'] is None) or (not info['secondhalf']['fouls']['@home']) else int(info['secondhalf']['fouls']['@home']),
							'away': None if (info['secondhalf']['fouls'].get("@away") is None) or (info['secondhalf']['fouls']['@away'] is None) or (not info['secondhalf']['fouls']['@away']) else int(info['secondhalf']['fouls']['@away'])
						},
						'yellowcards': None if (info['secondhalf'].get("yellowcards") is None) or (info['secondhalf']['yellowcards'] is None) or (not info['secondhalf']['yellowcards']) else {
							'total': None if (info['secondhalf']['yellowcards'].get("@total") is None) or (info['secondhalf']['yellowcards']['@total'] is None) or (not info['secondhalf']['yellowcards']['@total']) else int(info['secondhalf']['yellowcards']['@total']),
							'home': None if (info['secondhalf']['yellowcards'].get("@home") is None) or (info['secondhalf']['yellowcards']['@home'] is None) or (not info['secondhalf']['yellowcards']['@home']) else int(info['secondhalf']['yellowcards']['@home']),
							'away': None if (info['secondhalf']['yellowcards'].get("@away") is None) or (info['secondhalf']['yellowcards']['@away'] is None) or (not info['secondhalf']['yellowcards']['@away']) else int(info['secondhalf']['yellowcards']['@away'])
						},
						'redcards': None if (info['secondhalf'].get("redcards") is None) or (info['secondhalf']['redcards'] is None) or (not info['secondhalf']['redcards']) else {
							'total': None if (info['secondhalf']['redcards'].get("@total") is None) or (info['secondhalf']['redcards']['@total'] is None) or (not info['secondhalf']['redcards']['@total']) else int(info['secondhalf']['redcards']['@total']),
							'home': None if (info['secondhalf']['redcards'].get("@home") is None) or (info['secondhalf']['redcards']['@home'] is None) or (not info['secondhalf']['redcards']['@home']) else int(info['secondhalf']['redcards']['@home']),
							'away': None if (info['secondhalf']['redcards'].get("@away") is None) or (info['secondhalf']['redcards']['@away'] is None) or (not info['secondhalf']['redcards']['@away']) else int(info['secondhalf']['redcards']['@away'])
						},
						'avg_yellowcards': None if (info['secondhalf'].get("avg_yellowcards") is None) or (info['secondhalf']['avg_yellowcards'] is None) or (not info['secondhalf']['avg_yellowcards']) else {
							'total': None if (info['secondhalf']['avg_yellowcards'].get("@total") is None) or (info['secondhalf']['avg_yellowcards']['@total'] is None) or (not info['secondhalf']['avg_yellowcards']['@total']) else float(info['secondhalf']['avg_yellowcards']['@total']),
							'home': None if (info['secondhalf']['avg_yellowcards'].get("@home") is None) or (info['secondhalf']['avg_yellowcards']['@home'] is None) or (not info['secondhalf']['avg_yellowcards']['@home']) else float(info['secondhalf']['avg_yellowcards']['@home']),
							'away': None if (info['secondhalf']['avg_yellowcards'].get("@away") is None) or (info['secondhalf']['avg_yellowcards']['@away'] is None) or (not info['secondhalf']['avg_yellowcards']['@away']) else float(info['secondhalf']['avg_yellowcards']['@away'])
						},
						'avg_redcards': None if (info['secondhalf'].get("avg_redcards") is None) or (info['secondhalf']['avg_redcards'] is None) or (not info['secondhalf']['avg_redcards']) else {
							'total': None if (info['secondhalf']['avg_redcards'].get("@total") is None) or (info['secondhalf']['avg_redcards']['@total'] is None) or (not info['secondhalf']['avg_redcards']['@total']) else float(info['secondhalf']['avg_redcards']['@total']),
							'home': None if (info['secondhalf']['avg_redcards'].get("@home") is None) or (info['secondhalf']['avg_redcards']['@home'] is None) or (not info['secondhalf']['avg_redcards']['@home']) else float(info['secondhalf']['avg_redcards']['@home']),
							'away': None if (info['secondhalf']['avg_redcards'].get("@away") is None) or (info['secondhalf']['avg_redcards']['@away'] is None) or (not info['secondhalf']['avg_redcards']['@away']) else float(info['secondhalf']['avg_redcards']['@away'])
						}
					},
					'scoring_minutes': None if (info.get("scoring_minutes") is None) or (info['scoring_minutes'] is None) or (not info['scoring_minutes']) else {
						'period': None if (info['scoring_minutes'].get("period") is None) or (info['scoring_minutes']['period'] is None) or (not info['scoring_minutes']['period']) else scoringPeriod(info['scoring_minutes']['period'])
					},
					'goals_conceded_minutes': None if (info.get("goals_conceded_minutes") is None) or (info['goals_conceded_minutes'] is None) or (not info['goals_conceded_minutes']) else {
						'period': None if (info['goals_conceded_minutes'].get("period") is None) or (info['goals_conceded_minutes']['period'] is None) or (not info['goals_conceded_minutes']['period']) else scoringPeriod(info['goals_conceded_minutes']['period'])
					},
					'yellowcard_minutes': None if (info.get("yellowcard_minutes") is None) or (info['yellowcard_minutes'] is None) or (not info['yellowcard_minutes']) else {
						'period': None if (info['yellowcard_minutes'].get("period") is None) or (info['yellowcard_minutes']['period'] is None) or (not info['yellowcard_minutes']['period']) else scoringPeriod(info['yellowcard_minutes']['period'])
					},
					'redcard_minutes': None if (info.get("redcard_minutes") is None) or (info['redcard_minutes'] is None) or (not info['redcard_minutes']) else {
						'period': None if (info['redcard_minutes'].get("period") is None) or (info['redcard_minutes']['period'] is None) or (not info['redcard_minutes']['period']) else scoringPeriod(info['redcard_minutes']['period'])
					}
				}
				leaguelist.append(data)
			return leaguelist

def trophiesList(trophies):
	trophylist = []
	if type(trophies) is dict:
		data = {
			'country': None if (trophies.get("@country") is None) or (trophies['@country'] is None) or (not trophies['@country']) else trophies['@country'],
			'league': None if (trophies.get("@league") is None) or (trophies['@league'] is None) or (not trophies['@league']) else trophies['@league'],
			'status': None if (trophies.get("@status") is None) or (trophies['@status'] is None) or (not trophies['@status']) else trophies['@status'],
			'count': None if (trophies.get("@count") is None) or (trophies['@count'] is None) or (not trophies['@count']) else int(trophies['@count']),
			'seasons': None if (trophies.get("@seasons") is None) or (trophies['@seasons'] is None) or (not trophies['@seasons']) else trophies['@seasons'].split(', ')
		}
		return [data]
	if type(trophies) is list:
			for info in trophies:
				data = {
					'country': None if (info.get("@country") is None) or (info['@country'] is None) or (not info['@country']) else info['@country'],
					'league': None if (info.get("@league") is None) or (info['@league'] is None) or (not info['@league']) else info['@league'],
					'status': None if (info.get("@status") is None) or (info['@status'] is None) or (not info['@status']) else info['@status'],
					'count': None if (info.get("@count") is None) or (info['@count'] is None) or (not info['@count']) else int(info['@count']),
					'seasons': None if (info.get("@seasons") is None) or (info['@seasons'] is None) or (not info['@seasons']) else info['@seasons'].split(', ')
				}
				trophylist.append(data)
			return trophylist

def sidelinedPlayer(players):
	playerlist = []
	if type(players) is dict:
		data = {
			'name': None if (players.get("@name") is None) or (players['@name'] is None) or (not players['@name']) else players['@name'],
			'description': None if (players.get("@description") is None) or (players['@description'] is None) or (not players['@description']) else players['@description'],
			'startdate': None if (players.get("@startdate") is None) or (players['@startdate'] is None) or (not players['@startdate']) else dateUTCFormat(players['@startdate']),
			'enddate': None if (players.get("@enddate") is None) or (players['@enddate'] is None) or (not players['@enddate']) else dateUTCFormat(players['@enddate']),
			'id': None if (players.get("@id") is None) or (players['@id'] is None) or (not players['@id']) else int(players['@id'])
		}
		return [data]
	if type(players) is list:
			for info in players:
				data = {
					'name': None if (info.get("@name") is None) or (info['@name'] is None) or (not info['@name']) else info['@name'],
					'description': None if (info.get("@description") is None) or (info['@description'] is None) or (not info['@description']) else info['@description'],
					'startdate': None if (info.get("@startdate") is None) or (info['@startdate'] is None) or (not info['@startdate']) else dateUTCFormat(info['@startdate']),
					'enddate': None if (info.get("@enddate") is None) or (info['@enddate'] is None) or (not info['@enddate']) else dateUTCFormat(info['@enddate']),
					'id': None if (info.get("@id") is None) or (info['@id'] is None) or (not info['@id']) else int(info['@id'])
				}
				playerlist.append(data)
			return playerlist

def tranferInPlayers(InPlayers):
	playerList = []
	if 'in' in InPlayers and InPlayers['in'] != None :
		if 'player' in InPlayers['in']:
			players = InPlayers['in']['player']
			if type(players) is dict:
				data = {
					'id': None if (players.get("@id") is None) or (players['@id'] is None) or (not players['@id']) else int(players['@id']),
					'name': None if (players.get("@name") is None) or (players['@name'] is None) or (not players['@name']) else players['@name'],
					'date': None if (players.get("@date") is None) or (players['@date'] is None) or (not players['@date']) else dateUTCFormat(players['@date']),
					'age': None if (players.get("@age") is None) or (players['@age'] is None) or (not players['@age']) else int(players['@age']),
					'position': None if (players.get("@position") is None) or (players['@position'] is None) or (not players['@position']) else players['@position'],
					'from': None if (players.get("@from") is None) or (players['@from'] is None) or (not players['@from']) else players['@from'],
					'team_id': None if (players.get("@team_id") is None) or (players['@team_id'] is None) or (not players['@team_id']) else int(players['@team_id']),
					'type': None if (players.get("@type") is None) or (players['@type'] is None) or (not players['@type']) else players['@type']
				}
				return [data]
			if type(players) is list:
				for info in players:
					data = {
						'id': None if (info.get("@id") is None) or (info['@id'] is None) or (not info['@id']) else int(info['@id']),
						'name': None if (info.get("@name") is None) or (info['@name'] is None) or (not info['@name']) else info['@name'],
						'date': None if (info.get("@date") is None) or (info['@date'] is None) or (not info['@date']) else dateUTCFormat(info['@date']),
						'age': None if (info.get("@age") is None) or (info['@age'] is None) or (not info['@age']) else int(info['@age']),
						'position': None if (info.get("@position") is None) or (info['@position'] is None) or (not info['@position']) else info['@position'],
						'from': None if (info.get("@from") is None) or (info['@from'] is None) or (not info['@from']) else info['@from'],
						'team_id': None if (info.get("@team_id") is None) or (info['@team_id'] is None) or (not info['@team_id']) else int(info['@team_id']),
						'type': None if (info.get("@type") is None) or (info['@type'] is None) or (not info['@type']) else info['@type']
					}
					playerList.append(data)
				return playerList
	return playerList
def tranferOutPlayers(OutPlayers):
	playerList = []
	if 'out' in OutPlayers  and OutPlayers['out'] != None:
		if 'player' in OutPlayers['out']:
			players = OutPlayers['out']['player']
			if type(players) is dict:
				data = {
					'id': None if (players.get("@id") is None) or (players['@id'] is None) or (not players['@id']) else int(players['@id']),
					'name': None if (players.get("@name") is None) or (players['@name'] is None) or (not players['@name']) else players['@name'],
					'date': None if (players.get("@date") is None) or (players['@date'] is None) or (not players['@date']) else dateUTCFormat(players['@date']),
					'age': None if (players.get("@age") is None) or (players['@age'] is None) or (not players['@age']) else int(players['@age']),
					'position': None if (players.get("@position") is None) or (players['@position'] is None) or (not players['@position']) else players['@position'],
					'to': None if (players.get("@to") is None) or (players['@to'] is None) or (not players['@to']) else players['@to'],
					'team_id': None if (players.get("@team_id") is None) or (players['@team_id'] is None) or (not players['@team_id']) else int(players['@team_id']),
					'type': None if (players.get("@type") is None) or (players['@type'] is None) or (not players['@type']) else players['@type']
				}
				return [data]
			if type(players) is list:
				for info in players:
					data = {
						'id': None if (info.get("@id") is None) or (info['@id'] is None) or (not info['@id']) else int(info['@id']),
						'name': None if (info.get("@name") is None) or (info['@name'] is None) or (not info['@name']) else info['@name'],
						'date': None if (info.get("@date") is None) or (info['@date'] is None) or (not info['@date']) else dateUTCFormat(info['@date']),
						'age': None if (info.get("@age") is None) or (info['@age'] is None) or (not info['@age']) else int(info['@age']),
						'position': None if (info.get("@position") is None) or (info['@position'] is None) or (not info['@position']) else info['@position'],
						'to': None if (info.get("@to") is None) or (info['@to'] is None) or (not info['@to']) else info['@to'],
						'team_id': None if (info.get("@team_id") is None) or (info['@team_id'] is None) or (not info['@team_id']) else int(info['@team_id']),
						'type': None if (info.get("@type") is None) or (info['@type'] is None) or (not info['@type']) else info['@type']
					}
					playerList.append(data)
				return playerList
	return playerList	
def squadPlayers(playersList):
	playerList = []
	if type(playersList) is dict:
		data = {
			'id': None if (playersList.get("@id") is None) or (playersList['@id'] is None) or (not playersList['@id']) else int(playersList['@id']),
			'name': None if (playersList.get("@name") is None) or (playersList['@name'] is None) or (not playersList['@name']) else playersList['@name'],
			'number': None if (playersList.get("@number") is None) or (playersList['@number'] is None) or (not playersList['@name']) else str(playersList['@number']),
			'age': None if (playersList.get("@age") is None) or (playersList['@age'] is None) or (not playersList['@age']) else str(playersList['@age']),
			'position': None if (playersList.get("@position") is None) or (playersList['@position'] is None) or (not playersList['@position']) else playersList['@position'],
			'injured': None if (playersList.get("@injured") is None) or (playersList['@injured'] is None) or (not playersList['@injured']) else playersList['@injured'],
			'minutes': None if (playersList.get("@minutes") is None) or (playersList['@minutes'] is None) or (not playersList['@minutes']) else str(playersList['@minutes']),
			'appearences': None if (playersList.get("@appearences") is None) or (playersList['@appearences'] is None) or (not playersList['@appearences']) else str(playersList['@appearences']),
			'lineups': None if (playersList.get("@lineups") is None) or (playersList['@lineups'] is None) or (not playersList['@lineups']) else str(playersList['@lineups']),
			'substitute_in': None if (playersList.get("@substitute_in") is None) or (playersList['@substitute_in'] is None) or (not playersList['@substitute_in']) else str(playersList['@substitute_in']),
			'substitute_out': None if (playersList.get("@substitute_out") is None) or (playersList['@substitute_out'] is None) or (not playersList['@substitute_out']) else str(playersList['@substitute_out']),
			'substitutes_on_bench': None if (playersList.get("@substitutes_on_bench") is None) or (playersList['@substitutes_on_bench'] is None) or (not playersList['@substitutes_on_bench']) else str(playersList['@substitutes_on_bench']),
			'goals': 0 if (playersList.get("@goals") is None) or (playersList['@goals'] is None) or (not playersList['@goals']) else str(playersList['@goals']),
			'assists': 0 if (playersList.get("@assists") is None) or (playersList['@assists'] is None) or (not playersList['@assists']) else str(playersList['@assists']),
			'yellowcards': 0 if (playersList.get("@yellowcards") is None) or (playersList['@yellowcards'] is None) or (not playersList['@yellowcards']) else str(playersList['@yellowcards']),
			'yellowred': 0 if (playersList.get("@yellowred") is None) or (playersList['@yellowred'] is None) or (not playersList['@yellowred']) else str(playersList['@yellowred']),
			'redcards': 0 if (playersList.get("@redcards") is None) or (playersList['@redcards'] is None) or (not playersList['@redcards']) else str(playersList['@redcards']),
			'isCaptain': 0 if (playersList.get("@isCaptain") is None) or (playersList['@isCaptain'] is None) or (not playersList['@isCaptain']) else str(playersList['@isCaptain']),
			'shotsTotal': 0 if (playersList.get("@shotsTotal") is None) or (playersList['@shotsTotal'] is None) or (not playersList['@shotsTotal']) else str(playersList['@shotsTotal']),
			'shotsOn': 0 if (playersList.get("@shotsOn") is None) or (playersList['@shotsOn'] is None) or (not playersList['@shotsOn']) else str(playersList['@shotsOn']),
			'goalsConceded': 0 if (playersList.get("@goalsConceded") is None) or (playersList['@goalsConceded'] is None) or (not playersList['@goalsConceded']) else str(playersList['@goalsConceded']),
			'fouldDrawn': 0 if (playersList.get("@fouldDrawn") is None) or (playersList['@fouldDrawn'] is None) or (not playersList['@fouldDrawn']) else str(playersList['@fouldDrawn']),
			'foulsCommitted': 0 if (playersList.get("@foulsCommitted") is None) or (playersList['@foulsCommitted'] is None) or (not playersList['@foulsCommitted']) else str(playersList['@foulsCommitted']),
			'tackles': 0 if (playersList.get("@tackles") is None) or (playersList['@tackles'] is None) or (not playersList['@tackles']) else str(playersList['@tackles']),
			'blocks': 0 if (playersList.get("@blocks") is None) or (playersList['@blocks'] is None) or (not playersList['@blocks']) else str(playersList['@blocks']),
			'crossesTotal': 0 if (playersList.get("@crossesTotal") is None) or (playersList['@crossesTotal'] is None) or (not playersList['@crossesTotal']) else str(playersList['@crossesTotal']),
			'crossesAccurate': 0 if (playersList.get("@crossesAccurate") is None) or (playersList['@crossesAccurate'] is None) or (not playersList['@crossesAccurate']) else str(playersList['@crossesAccurate']),
			'interceptions': 0 if (playersList.get("@interceptions") is None) or (playersList['@interceptions'] is None) or (not playersList['@interceptions']) else str(playersList['@interceptions']),
			'clearances': 0 if (playersList.get("@clearances") is None) or (playersList['@clearances'] is None) or (not playersList['@clearances']) else str(playersList['@clearances']),
			'dispossesed': 0 if (playersList.get("@dispossesed") is None) or (playersList['@dispossesed'] is None) or (not playersList['@dispossesed']) else str(playersList['@dispossesed']),
			'saves': 0 if (playersList.get("@saves") is None) or (playersList['@saves'] is None) or (not playersList['@saves']) else str(playersList['@saves']),
			'insideBoxSaves': 0 if (playersList.get("@insideBoxSaves") is None) or (playersList['@insideBoxSaves'] is None) or (not playersList['@insideBoxSaves']) else str(playersList['@insideBoxSaves']),
			'duelsTotal': 0 if (playersList.get("@duelsTotal") is None) or (playersList['@duelsTotal'] is None) or (not playersList['@duelsTotal']) else str(playersList['@duelsTotal']),
			'duelsWon': 0 if (playersList.get("@duelsWon") is None) or (playersList['@duelsWon'] is None) or (not playersList['@duelsWon']) else str(playersList['@duelsWon']),
			'dribbleAttempts': 0 if (playersList.get("@dribbleAttempts") is None) or (playersList['@dribbleAttempts'] is None) or (not playersList['@dribbleAttempts']) else str(playersList['@dribbleAttempts']),
			'dribbleSucc': 0 if (playersList.get("@dribbleSucc") is None) or (playersList['@dribbleSucc'] is None) or (not playersList['@dribbleSucc']) else str(playersList['@dribbleSucc']),
			'penComm': 0 if (playersList.get("@penComm") is None) or (playersList['@penComm'] is None) or (not playersList['@penComm']) else str(playersList['@penComm']),
			'penWon': 0 if (playersList.get("@penWon") is None) or (playersList['@penWon'] is None) or (not playersList['@penWon']) else str(playersList['@penWon']),
			'penScored': 0 if (playersList.get("@penScored") is None) or (playersList['@penScored'] is None) or (not playersList['@penScored']) else str(playersList['@penScored']),
			'penMissed': 0 if (playersList.get("@penMissed") is None) or (playersList['@penMissed'] is None) or (not playersList['@penMissed']) else str(playersList['@penMissed']),
			'penSaved': 0 if (playersList.get("@penSaved") is None) or (playersList['@penSaved'] is None) or (not playersList['@penSaved']) else str(playersList['@penSaved']),
			'passes': 0 if (playersList.get("@passes") is None) or (playersList['@passes'] is None) or (not playersList['@passes']) else str(playersList['@passes']),
			'pAccuracy': 0 if (playersList.get("@pAccuracy") is None) or (playersList['@pAccuracy'] is None) or (not playersList['@pAccuracy']) else str(playersList['@pAccuracy']),
			'keyPasses': 0 if (playersList.get("@keyPasses") is None) or (playersList['@keyPasses'] is None) or (not playersList['@keyPasses']) else str(playersList['@keyPasses']),
			'woordworks': 0 if (playersList.get("@woordworks") is None) or (playersList['@woordworks'] is None) or (not playersList['@woordworks']) else str(playersList['@woordworks']),
			'rating': 0 if (playersList.get("@rating") is None) or (playersList['@rating'] is None) or (not playersList['@rating']) else float(playersList['@rating'])
		}
		return [data]
	if type(playersList) is list:
			for info in playersList:
				data = {
					'id': None if (info.get("@id") is None) or (info['@id'] is None) or (not info['@id']) else int(info['@id']),
					'name': None if (info.get("@name") is None) or (info['@name'] is None) or (not info['@name']) else info['@name'],
					'number': None if (info.get("@number") is None) or (info['@number'] is None) or(not info['@number']) else str(info['@number']),
					'age': None if (info.get("@age") is None) or (info['@age'] is None) or (not info['@age']) else str(info['@age']),
					'position': None if (info.get("@position") is None) or (info['@position'] is None) or (not info['@position']) else info['@position'],
					'injured': None if (info.get("@injured") is None) or (info['@injured'] is None) or (not info['@injured']) else info['@injured'],
					'minutes': None if (info.get("@minutes") is None) or (info['@minutes'] is None) or (not info['@minutes']) else str(info['@minutes']),
					'appearences': None if (info.get("@appearences") is None) or (info['@appearences'] is None) or (not info['@appearences']) else str(info['@appearences']),
					'lineups': None if (info.get("@lineups") is None) or (info['@lineups'] is None) or (not info['@lineups']) else str(info['@lineups']),
					'substitute_in': None if (info.get("@substitute_in") is None) or (info['@substitute_in'] is None) or (not info['@substitute_in']) else str(info['@substitute_in']),
					'substitute_out': None if (info.get("@substitute_out") is None) or (info['@substitute_out'] is None) or (not info['@substitute_out']) else str(info['@substitute_out']),
					'substitutes_on_bench': None if (info.get("@substitutes_on_bench") is None) or (info['@substitutes_on_bench'] is None) or (not info['@substitutes_on_bench']) else str(info['@substitutes_on_bench']),
					'goals': 0 if (info.get("@goals") is None) or (info['@goals'] is None) or (not info['@goals']) else str(info['@goals']),
					'assists': 0 if (info.get("@assists") is None) or (info['@assists'] is None) or (not info['@assists']) else str(info['@assists']),
					'yellowcards': 0 if (info.get("@yellowcards") is None) or (info['@yellowcards'] is None) or (not info['@yellowcards']) else str(info['@yellowcards']),
					'yellowred': 0 if (info.get("@yellowred") is None) or (info['@yellowred'] is None) or (not info['@yellowred']) else str(info['@yellowred']),
					'redcards': 0 if (info.get("@redcards") is None) or (info['@redcards'] is None) or (not info['@redcards']) else str(info['@redcards']),
					'isCaptain': 0 if (info.get("@isCaptain") is None) or (info['@isCaptain'] is None) or (not info['@isCaptain']) else str(info['@isCaptain']),
					'shotsTotal': 0 if (info.get("@shotsTotal") is None) or (info['@shotsTotal'] is None) or (not info['@shotsTotal']) else str(info['@shotsTotal']),
					'shotsOn': 0 if (info.get("@shotsOn") is None) or (info['@shotsOn'] is None) or (not info['@shotsOn']) else str(info['@shotsOn']),
					'goalsConceded': 0 if (info.get("@goalsConceded") is None) or (info['@goalsConceded'] is None) or (not info['@goalsConceded']) else str(info['@goalsConceded']),
					'fouldDrawn': 0 if (info.get("@fouldDrawn") is None) or (info['@fouldDrawn'] is None) or (not info['@fouldDrawn']) else str(info['@fouldDrawn']),
					'foulsCommitted': 0 if (info.get("@foulsCommitted") is None) or (info['@foulsCommitted'] is None) or (not info['@foulsCommitted']) else str(info['@foulsCommitted']),
					'tackles': 0 if (info.get("@tackles") is None) or (info['@tackles'] is None) or (not info['@tackles']) else str(info['@tackles']),
					'blocks': 0 if (info.get("@blocks") is None) or (info['@blocks'] is None) or (not info['@blocks']) else str(info['@blocks']),
					'crossesTotal': 0 if (info.get("@crossesTotal") is None) or (info['@crossesTotal'] is None) or (not info['@crossesTotal']) else str(info['@crossesTotal']),
					'crossesAccurate': 0 if (info.get("@crossesAccurate") is None) or (info['@crossesAccurate'] is None) or (not info['@crossesAccurate']) else str(info['@crossesAccurate']),
					'interceptions': 0 if (info.get("@interceptions") is None) or (info['@interceptions'] is None) or (not info['@interceptions']) else str(info['@interceptions']),
					'clearances': 0 if (info.get("@clearances") is None) or (info['@clearances'] is None) or (not info['@clearances']) else str(info['@clearances']),
					'dispossesed': 0 if (info.get("@dispossesed") is None) or (info['@dispossesed'] is None) or (not info['@dispossesed']) else str(info['@dispossesed']),
					'saves': 0 if (info.get("@saves") is None) or (info['@saves'] is None) or (not info['@saves']) else str(info['@saves']),
					'insideBoxSaves': 0 if (info.get("@insideBoxSaves") is None) or (info['@insideBoxSaves'] is None) or (not info['@insideBoxSaves']) else str(info['@insideBoxSaves']),
					'duelsTotal': 0 if (info.get("@duelsTotal") is None) or (info['@duelsTotal'] is None) or (not info['@duelsTotal']) else str(info['@duelsTotal']),
					'duelsWon': 0 if (info.get("@duelsWon") is None) or (info['@duelsWon'] is None) or (not info['@duelsWon']) else str(info['@duelsWon']),
					'dribbleAttempts': 0 if (info.get("@dribbleAttempts") is None) or (info['@dribbleAttempts'] is None) or (not info['@dribbleAttempts']) else str(info['@dribbleAttempts']),
					'dribbleSucc': 0 if (info.get("@dribbleSucc") is None) or (info['@dribbleSucc'] is None) or (not info['@dribbleSucc']) else str(info['@dribbleSucc']),
					'penComm': 0 if (info.get("@penComm") is None) or (info['@penComm'] is None) or (not info['@penComm']) else str(info['@penComm']),
					'penWon': 0 if (info.get("@penWon") is None) or (info['@penWon'] is None) or (not info['@penWon']) else str(info['@penWon']),
					'penScored': 0 if (info.get("@penScored") is None) or (info['@penScored'] is None) or (not info['@penScored']) else str(info['@penScored']),
					'penMissed': 0 if (info.get("@penMissed") is None) or (info['@penMissed'] is None) or (not info['@penMissed']) else str(info['@penMissed']),
					'penSaved': 0 if (info.get("@penSaved") is None) or (info['@penSaved'] is None) or (not info['@penSaved']) else str(info['@penSaved']),
					'passes': 0 if (info.get("@passes") is None) or (info['@passes'] is None) or (not info['@passes']) else str(info['@passes']),
					'pAccuracy': 0 if (info.get("@pAccuracy") is None) or (info['@pAccuracy'] is None) or (not info['@pAccuracy']) else str(info['@pAccuracy']),
					'keyPasses': 0 if (info.get("@keyPasses") is None) or (info['@keyPasses'] is None) or (not info['@keyPasses']) else str(info['@keyPasses']),
					'woordworks': 0 if (info.get("@woordworks") is None) or (info['@woordworks'] is None) or (not info['@woordworks']) else str(info['@woordworks']),
					'rating': 0 if (info.get("@rating") is None) or (info['@rating'] is None) or (not info['@rating']) else float(info['@rating'])
				}
				playerList.append(data)
			return playerList

def test_data(day_list):
	leagues = LeagueIdGolaServe()
	headTwoHeadId = []
	for i in day_list:
		print("Iteration started for upcoming matches of day : ", i)
		# filename = i + '.json'
		url = "http://www.goalserve.com/getfeed/c05d9fc7d36540dcdfaa08d9e34f661d/soccernew/"+i+"?json=1"
		payload={}
		headers = {}
		response = requests.request("GET", url, headers=headers, data=payload)
		data = response.json()
		# print(data)
		data = data['scores']['category']
		for info in data:
			if int(info['@id']) in leagues:
				new_data = info['matches']['match']
				if type(new_data) is dict:
					if (not(new_data['localteam']['@id'])) or (not(new_data['visitorteam']['@id'])):
						break
					else:
						single_data = {
							'team1_id': int(new_data['localteam']['@id']),
							'team2_id': int(new_data['visitorteam']['@id']),
							'match_id': int(new_data['@id'])
						}
						# print(single_data)
						headTwoHeadId.append(single_data)
				if type(new_data) is list:
					for info in new_data:
						if (not(info['localteam']['@id'])) or (not(info['visitorteam']['@id'])):
							break
						single_data = {
						'team1_id': int(info['localteam']['@id']),
						'team2_id': int(info['visitorteam']['@id']),
						'match_id': int(info['@id'])
						}
						# print(single_data)
						headTwoHeadId.append(single_data)

		# 	headTwoHeadId.append(single_data)
		# print("Iteration completion for one day and head2head id length: ", len(headTwoHeadId))
	with open("h2hteamlist15022022.json", 'w') as f:
			f.write(json.dumps(headTwoHeadId, indent=3))
	return headTwoHeadId

def teamRequests(team, matchId):
	url = "http://www.goalserve.com/getfeed/c05d9fc7d36540dcdfaa08d9e34f661d/soccerstats/team/"+str(team)+"?json=1"
	print(url)
	payload={}
	headers = {}
	response = requests.request("GET", url, headers=headers, data=payload)
	# try:
	data = response.json()
	data = None if data['teams'] is None else data['teams']
	if data is None:
		logger.info('Error : teaminfo'+str(teamsdata['id']))
		return None
	else:
		
			# print(data['team']['transfers']['in'])
		modified_stat_data = {
			'match_id': matchId,
			'id': None if (data['team'].get("@id") is None) or (data['team']['@id'] is None) or (not data['team']['@id']) else int(data['team']['@id']),
			'is_national_team': None if (data['team'].get("@is_national_team") is None) or (data['team']['@is_national_team'] is None) or (not data['team']['@is_national_team']) else bool(data['team']['@is_national_team']),
			'name': None if (data['team'].get("name") is None) or (data['team']['name'] is None) or (not data['team']['name']) else data['team']['name'],
			'fullname': None if (data['team'].get("fullname") is None) or (data['team']['fullname'] is None) or (not data['team']['fullname']) else data['team']['fullname'],
			'country': None if (data['team'].get("country") is None) or (data['team']['country'] is None) or (not data['team']['country']) else data['team']['country'],
			'founded': None if (data['team'].get("founded") is None) or (data['team']['founded'] is None) or (not data['team']['founded']) else data['team']['founded'],
			'leagues':None if (data['team'].get("leagues") is None) or (data['team']['leagues'] is None) or (not data['team']['leagues']) else {
				'league_rank': None if (data['team']['leagues'].get("@league_rank") is None) or (data['team']['leagues']['@league_rank'] is None) or (not data['team']['leagues']['@league_rank']) else int(data['team']['leagues']['@league_rank']),
				'league_id': None if (data['team']['leagues'].get("league_id") is None) or (data['team']['leagues']['league_id'] is None) or (not data['team']['leagues']['league_id']) else leagues(data['team']['leagues']['league_id'])
			},
			'venue_name': None if (data['team'].get("venue_name") is None) or (data['team']['venue_name'] is None) or (not data['team']['venue_name']) else data['team']['venue_name'],
			'venue_id': None if (data['team'].get("venue_id") is None) or (data['team']['venue_id'] is None) or (not data['team']['venue_id']) else int(data['team']['venue_id']),
			'venue_surface': None if (data['team'].get("venue_surface") is None) or (data['team']['venue_surface'] is None) or (not data['team']['venue_surface']) else data['team']['venue_surface'],
			'venue_address': None if (data['team'].get("venue_address") is None) or (data['team']['venue_address'] is None) or (not data['team']['venue_address']) else {
				'cdata-section': None if (data['team']['venue_address'].get("#cdata-section") is None) or (data['team']['venue_address']['#cdata-section'] is None) or (not data['team']['venue_address']['#cdata-section']) else data['team']['venue_address']['#cdata-section']
			},
			'venue_city': None if (data['team'].get("venue_city") is None) or (data['team']['venue_city'] is None) or (not data['team']['venue_city']) else {
				'cdata-section': None if (data['team']['venue_city'].get("#cdata-section") is None) or (data['team']['venue_city']['#cdata-section'] is None) or (not data['team']['venue_city']['#cdata-section']) else data['team']['venue_city']['#cdata-section']
			},
			'venue_capacity': None if (data['team'].get("venue_capacity") is None) or (data['team']['venue_capacity'] is None) or (not data['team']['venue_capacity']) else int(data['team']['venue_capacity']),
			'venue_image': None if (data['team'].get("venue_image") is None) or (data['team']['venue_image'] is None) or (not data['team']['venue_image']) else data['team']['venue_image'],
			'image': None if (data['team'].get("image") is None) or (data['team']['image'] is None) or (not data['team']['image']) else data['team']['image'],
			'squad': None if (data['team'].get("squad") is None) or (data['team']['squad'] is None) or (not data['team']['squad']) else {
				'player': None if (data['team']['squad'].get("player") is None) or (data['team']['squad']['player'] is None) or (not data['team']['squad']['player']) else squadPlayers(data['team']['squad']['player'])
			},
			'coach': None if (data['team'].get("coach") is None) or (data['team']['coach'] is None) or (not data['team']['@id']) else {
				'name': None if (data['team']['coach'].get("@name") is None) or (data['team']['coach']['@name'] is None) or (not data['team']['coach']['@name']) else data['team']['coach']['@name'],
				'id': None if (data['team']['coach'].get("@id") is None) or (data['team']['coach']['@id'] is None) or (not data['team']['coach']['@id']) else int(data['team']['coach']['@id'])
			},

			'transfers': None if (data['team'].get("transfers") is None) or (data['team']['transfers'] is None) or (not data['team']['transfers']) else {
				'in':tranferInPlayers(data['team']['transfers']),
				'out': tranferOutPlayers(data['team']['transfers']),
			},
			'statistics': None if (data['team'].get("statistics") is None) or (data['team']['statistics'] is None) or (not data['team']['statistics']) else {
				# 'rank': None if (data['team']['statistics'].get("rank") is None) or (data['team']['statistics']['rank'] is None) or (not data['team']['statistics']['rank']['@total']) else int(data['team']['statistics']['rank']['@total']),
				'rank': None if (data['team']['statistics'].get("rank") is None) or (data['team']['statistics']['rank'] is None) or (not data['team']['statistics']['rank']) else {
					'total': None if (data['team']['statistics']['rank'].get("@total") is None) or (data['team']['statistics']['rank']['@total'] is None) or (not data['team']['statistics']['rank']['@total']) else int(data['team']['statistics']['rank']['@total']),
					'home': None if (data['team']['statistics']['rank'].get("@home") is None) or (not data['team']['statistics']['rank']['@home']) else int(data['team']['statistics']['rank']['@home']),
					'away': None if (data['team']['statistics']['rank'].get("@away")  is None) or (not data['team']['statistics']['rank']['@away']) else int(data['team']['statistics']['rank']['@away'])
				},
				'win': None if (data['team']['statistics'].get("win") is None) or (data['team']['statistics']['win'] is None) or (not data['team']['statistics']['win']) else {
					'total': None if (data['team']['statistics']['win'].get("@total") is None) or (data['team']['statistics']['win']['@total'] is None) or (not data['team']['statistics']['win']['@total']) else int(data['team']['statistics']['win']['@total']),
					'home': None if (data['team']['statistics']['win']['@home'] is None) or (not data['team']['statistics']['win']['@home']) else int(data['team']['statistics']['win']['@home']),
					'away': None if (data['team']['statistics']['win']['@away'] is None) or (not data['team']['statistics']['win']['@away']) else int(data['team']['statistics']['win']['@away'])
				},
				'draw': None if (data['team']['statistics'].get("draw") is None) or (data['team']['statistics']['draw'] is None) or (not data['team']['statistics']['draw']) else {
					'total': None if (data['team']['statistics']['draw'].get("@total") is None) or (data['team']['statistics']['draw']['@total'] is None) or (not data['team']['statistics']['draw']['@total']) else int(data['team']['statistics']['draw']['@total']),
					'home': None if (data['team']['statistics']['draw'].get("@home") is None) or (data['team']['statistics']['draw']['@home'] is None) or (not data['team']['statistics']['draw']['@home']) else int(data['team']['statistics']['draw']['@home']),
					'away': None if (data['team']['statistics']['draw'].get("@away") is None) or (data['team']['statistics']['draw']['@away'] is None) or (not data['team']['statistics']['draw']['@away']) else int(data['team']['statistics']['draw']['@away'])
				},
				'lost': None if (data['team']['statistics'].get("lost") is None) or (data['team']['statistics']['lost'] is None) or (not data['team']['statistics']['lost']) else {
					'total': None if (data['team']['statistics']['lost'].get("@total") is None) or (data['team']['statistics']['lost']['@total'] is None) or (not data['team']['statistics']['lost']['@total']) else int(data['team']['statistics']['lost']['@total']),
					'home': None if (data['team']['statistics']['lost'].get("@home") is None) or (data['team']['statistics']['lost']['@home'] is None) or (not data['team']['statistics']['lost']['@home']) else int(data['team']['statistics']['lost']['@home']),
					'away': None if (data['team']['statistics']['lost'].get("@away") is None) or (data['team']['statistics']['lost']['@away'] is None) or (not data['team']['statistics']['lost']['@away']) else int(data['team']['statistics']['lost']['@away'])
				},
				'goals_for': None if (data['team']['statistics'].get("goals_for") is None) or (data['team']['statistics']['goals_for'] is None) or (not data['team']['statistics']['goals_for']) else {
					'total': None if (data['team']['statistics']['goals_for'].get("@total") is None) or (data['team']['statistics']['goals_for']['@total'] is None) or (not data['team']['statistics']['goals_for']['@total']) else int(data['team']['statistics']['goals_for']['@total']),
					'home': None if (data['team']['statistics']['goals_for'].get("@home") is None) or (data['team']['statistics']['goals_for']['@home'] is None) or (not data['team']['statistics']['goals_for']['@home']) else int(data['team']['statistics']['goals_for']['@home']),
					'away': None if (data['team']['statistics']['goals_for'].get("@away") is None) or (data['team']['statistics']['goals_for']['@away'] is None) or (not data['team']['statistics']['goals_for']['@away']) else int(data['team']['statistics']['goals_for']['@away'])
				},
				'goals_against': None if (data['team']['statistics'].get("goals_against") is None) or (data['team']['statistics']['goals_against'] is None) or (not data['team']['statistics']['goals_against']) else {
					'total': None if (data['team']['statistics']['goals_against'].get("@total") is None) or (data['team']['statistics']['goals_against']['@total'] is None) or (not data['team']['statistics']['goals_against']['@total']) else int(data['team']['statistics']['goals_against']['@total']),
					'home': None if (data['team']['statistics']['goals_against'].get("@home") is None) or (data['team']['statistics']['goals_against']['@home'] is None) or (not data['team']['statistics']['goals_against']['@home']) else int(data['team']['statistics']['goals_against']['@home']),
					'away': None if (data['team']['statistics']['goals_against'].get("@away") is None) or (data['team']['statistics']['goals_against']['@away'] is None) or (not data['team']['statistics']['goals_against']['@away']) else int(data['team']['statistics']['goals_against']['@away'])
				},
				'clean_sheet': None if (data['team']['statistics'].get("clean_sheet") is None) or (data['team']['statistics']['clean_sheet'] is None) or (not data['team']['statistics']['clean_sheet']) else {
					'total': None if (data['team']['statistics']['clean_sheet'].get("@total") is None) or (data['team']['statistics']['clean_sheet']['@total'] is None) or (not data['team']['statistics']['clean_sheet']['@total']) else int(data['team']['statistics']['clean_sheet']['@total']),
					'home': None if (data['team']['statistics']['clean_sheet'].get("@home") is None) or (data['team']['statistics']['clean_sheet']['@home'] is None) or (not data['team']['statistics']['clean_sheet']['@home']) else int(data['team']['statistics']['clean_sheet']['@home']),
					'away': None if (data['team']['statistics']['clean_sheet'].get("@away") is None) or (data['team']['statistics']['clean_sheet']['@away'] is None) or (not data['team']['statistics']['clean_sheet']['@away']) else int(data['team']['statistics']['clean_sheet']['@away'])
				},
				'avg_goals_per_game_scored': None if (data['team']['statistics'].get("avg_goals_per_game_scored") is None) or (data['team']['statistics']['avg_goals_per_game_scored'] is None) or (not data['team']['statistics']['avg_goals_per_game_scored']) else {
					'total': None if (data['team']['statistics']['avg_goals_per_game_scored'].get("@total") is None) or (data['team']['statistics']['avg_goals_per_game_scored']['@total'] is None) or (not data['team']['statistics']['avg_goals_per_game_scored']['@total']) else float(data['team']['statistics']['avg_goals_per_game_scored']['@total']),
					'home': None if (data['team']['statistics']['avg_goals_per_game_scored'].get("@home") is None) or (data['team']['statistics']['avg_goals_per_game_scored']['@home'] is None) or (not data['team']['statistics']['avg_goals_per_game_scored']['@home']) else float(data['team']['statistics']['avg_goals_per_game_scored']['@home']),
					'away': None if (data['team']['statistics']['avg_goals_per_game_scored'].get("@away") is None) or (data['team']['statistics']['avg_goals_per_game_scored']['@away'] is None) or (not data['team']['statistics']['avg_goals_per_game_scored']['@away']) else float(data['team']['statistics']['avg_goals_per_game_scored']['@away'])
				},
				'avg_goals_per_game_conceded': None if (data['team']['statistics'].get("avg_goals_per_game_conceded") is None) or (data['team']['statistics']['avg_goals_per_game_conceded'] is None) or (not data['team']['statistics']['avg_goals_per_game_conceded']) else {
					'total': None if (data['team']['statistics']['avg_goals_per_game_conceded'].get("@total") is None) or (data['team']['statistics']['avg_goals_per_game_conceded']['@total'] is None) or (not data['team']['statistics']['avg_goals_per_game_conceded']['@total']) else float(data['team']['statistics']['avg_goals_per_game_conceded']['@total']),
					'home': None if (data['team']['statistics']['avg_goals_per_game_conceded'].get("@home") is None) or (data['team']['statistics']['avg_goals_per_game_conceded']['@home'] is None) or (not data['team']['statistics']['avg_goals_per_game_conceded']['@home']) else float(data['team']['statistics']['avg_goals_per_game_conceded']['@home']),
					'away': None if (data['team']['statistics']['avg_goals_per_game_conceded'].get("@away") is None) or (data['team']['statistics']['avg_goals_per_game_conceded']['@away'] is None) or (not data['team']['statistics']['avg_goals_per_game_conceded']['@away']) else float(data['team']['statistics']['avg_goals_per_game_conceded']['@away'])
				},
				'avg_first_goal_scored': None if (data['team']['statistics'].get("avg_first_goal_scored") is None) or (data['team']['statistics']['avg_first_goal_scored'] is None) or (not data['team']['statistics']['avg_first_goal_scored']) else {
					'total': None if (data['team']['statistics']['avg_first_goal_scored'].get("@total") is None) or (data['team']['statistics']['avg_first_goal_scored']['@total'] is None) or (not data['team']['statistics']['avg_first_goal_scored']['@total']) else data['team']['statistics']['avg_first_goal_scored']['@total'],
					'home': None if (data['team']['statistics']['avg_first_goal_scored'].get("@home") is None) or (data['team']['statistics']['avg_first_goal_scored']['@home'] is None) or (not data['team']['statistics']['avg_first_goal_scored']['@home']) else data['team']['statistics']['avg_first_goal_scored']['@home'],
					'away': None if (data['team']['statistics']['avg_first_goal_scored'].get("@away") is None) or (data['team']['statistics']['avg_first_goal_scored']['@away'] is None) or (not data['team']['statistics']['avg_first_goal_scored']['@away']) else data['team']['statistics']['avg_first_goal_scored']['@away']
				},
				'avg_first_goal_conceded': None if (data['team']['statistics'].get("avg_first_goal_conceded") is None) or (data['team']['statistics']['avg_first_goal_conceded'] is None) or (not data['team']['statistics']['avg_first_goal_conceded']) else {
					'total': None if (data['team']['statistics']['avg_first_goal_conceded'].get("@total") is None) or (data['team']['statistics']['avg_first_goal_conceded']['@total'] is None) or (not data['team']['statistics']['avg_first_goal_conceded']['@total']) else data['team']['statistics']['avg_first_goal_conceded']['@total'],
					'home': None if (data['team']['statistics']['avg_first_goal_conceded'].get("@home") is None) or (data['team']['statistics']['avg_first_goal_conceded']['@home'] is None) or (not data['team']['statistics']['avg_first_goal_conceded']['@home']) else data['team']['statistics']['avg_first_goal_conceded']['@home'],
					'away': None if (data['team']['statistics']['avg_first_goal_conceded'].get("@away") is None) or (data['team']['statistics']['avg_first_goal_conceded']['@away'] is None) or (not data['team']['statistics']['avg_first_goal_conceded']['@away']) else data['team']['statistics']['avg_first_goal_conceded']['@away']
				},
				'failed_to_score': None if (data['team']['statistics'].get("failed_to_score") is None) or (data['team']['statistics']['failed_to_score'] is None) or (not data['team']['statistics']['failed_to_score']) else {
					'total': None if (data['team']['statistics']['failed_to_score'].get("@total") is None) or (data['team']['statistics']['failed_to_score']['@total'] is None) or (not data['team']['statistics']['failed_to_score']['@total']) else int(data['team']['statistics']['failed_to_score']['@total']),
					'home': None if (data['team']['statistics']['failed_to_score'].get("@home") is None) or (data['team']['statistics']['failed_to_score']['@home'] is None) or (not data['team']['statistics']['failed_to_score']['@home']) else int(data['team']['statistics']['failed_to_score']['@home']),
					'away': None if (data['team']['statistics']['failed_to_score'].get("@away") is None) or (data['team']['statistics']['failed_to_score']['@away'] is None) or (not data['team']['statistics']['failed_to_score']['@away']) else int(data['team']['statistics']['failed_to_score']['@away'])
				},
				'scoring_minutes': None if (data['team']['statistics'].get("scoring_minutes") is None) or (data['team']['statistics']['scoring_minutes'] is None) or (not data['team']['statistics']['scoring_minutes']) else {
					'period': None if (data['team']['statistics']['scoring_minutes'].get("period") is None) or (data['team']['statistics']['scoring_minutes']['period'] is None) or (not data['team']['statistics']['scoring_minutes']['period']) else scoringPeriod(data['team']['statistics']['scoring_minutes']['period'])
				}
			},
			'detailed_stats': None if (data['team'].get("detailed_stats") is None) or (data['team']['detailed_stats'] is None) or (not data['team']['detailed_stats']) else {
				'league': None if (data['team']['detailed_stats'].get("league") is None) or (data['team']['detailed_stats']['league'] is None) or (not data['team']['detailed_stats']['league']) else detailedStats(data['team']['detailed_stats']['league'])
			},
			'sidelined': None if (data['team'].get("sidelined") is None) or (data['team']['sidelined'] is None) or (not data['team']['sidelined']) else {
				'player': None if (data['team']['sidelined'].get("player") is None) or (data['team']['sidelined']['player'] is None) or (not data['team']['sidelined']['player']) else sidelinedPlayer(data['team']['sidelined']['player'])

			},
			'trophies': None if (data['team'].get("trophies") is None) or (data['team']['trophies'] is None) or (not data['team']['trophies']) else {
				'trophy': None if (data['team']['trophies'].get("trophy") is None) or (data['team']['trophies']['trophy'] is None) or (not data['team']['trophies']['trophy']) else trophiesList(data['team']['trophies']['trophy'])
			}
		}
		# print(modified_stat_data)
		return modified_stat_data
	# except:
	# 	return None

def teamstats(teamList):
	teamStatList = []
	for team in teamList:
		team1_stat = teamRequests(team['team1_id'], team['match_id'])
		teamStatList.append(team1_stat)
		# with open("teamstatsforteam1.json", 'w') as f:
		# 	f.write(json.dumps(team1_stat, indent=3))
		team2_stat = teamRequests(team['team2_id'], team['match_id'])
		teamStatList.append(team2_stat)
	return teamStatList

# teamList = [{
# 	'match_id': 4319139,
# 	'team1_id': 9427,
# 	'team2_id': 9287
# 	}]

# team_data = teamstats(teamList)