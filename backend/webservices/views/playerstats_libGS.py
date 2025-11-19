import requests
from datetime import datetime
# import json

def dateUTC2Format(dateStr):
	return datetime.strptime(dateStr, '%d/%m/%Y').strftime('%Y-%m-%d')

def dateUTCFormat(dateStr):
	return datetime.strptime(dateStr, '%d.%m.%y').strftime('%Y-%m-%d')


def sidelinedItems(items):
	itemList = []
	if type(items) is dict:
		data = {
			'type': None if (items.get("@type") is None) or (items['@type'] is None) or (not items['@type']) else items['@type'],
			'date_start': None if (items.get("@date_start") is None) or (items['@date_start'] is None) or (not items['@date_start']) else dateUTCFormat(items['@date_start']),
			'date_end': None if (items.get("@date_end") is None) or (items['@date_end'] is None) or (not items['@date_end']) else dateUTCFormat(items['@date_end'])
		}
		return [data]
	if type(items) is list:
			for info in items:
				data = {
					'type': None if (info.get("@type") is None) or (info['@type'] is None) or (not info['@type']) else info['@type'],
					'date_start': None if (info.get("@date_start") is None) or (info['@date_start'] is None) or (not info['@date_start']) else dateUTCFormat(info['@date_start']),
					'date_end': None if (info.get("@date_end") is None) or (info['@date_end'] is None) or (not info['@date_end']) else dateUTCFormat(info['@date_end'])
				}
				itemList.append(data)
			return itemList

def trophiesTrophy(trophies):
	trophyList = []
	if type(trophies) is dict:
		data = {
			'country': None if (trophies.get("@country") is None) or (trophies['@country'] is None) or (not trophies['@country']) else trophies['@country'],
			'league': None if (trophies.get("@league") is None) or (trophies['@league'] is None) or (not trophies['@league']) else trophies['@league'],
			'status': None if (trophies.get("@status") is None) or (trophies['@status'] is None) or (not trophies['@status']) else trophies['@status'],
			'count': None if (trophies.get("@count") is None) or (trophies['@count'] is None) or (not trophies['@count']) else int(trophies['@count']),
			'seasons': None if (trophies.get("@seasons") is None) or (trophies['@seasons'] is None) or (not trophies['@seasons']) else trophies['@seasons'].split(', '),
		}
		return [data]
	if type(trophies) is list:
			for info in trophies:
				data = {
					'country': None if (info.get("@country") is None) or (info['@country'] is None) or (not info['@country']) else info['@country'],
					'league': None if (info.get("@league") is None) or (info['@league'] is None) or (not info['@league']) else info['@league'],
					'status': None if (info.get("@status") is None) or (info['@status'] is None) or (not info['@status']) else info['@status'],
					'count': None if (info.get("@count") is None) or (info['@count'] is None) or (not info['@count']) else int(info['@count']),
					'seasons': None if (info.get("@seasons") is None) or (info['@seasons'] is None) or (not info['@seasons']) else info['@seasons'].split(', '),
				}
				trophyList.append(data)
			return trophyList

def statisticIntlClub(clubs):
	clubList = []
	if type(clubs) is dict:
		data = {
			'name': None if (clubs.get("@name") is None) or (clubs['@name'] is None) or (not clubs['@name']) else clubs['@name'],
			'id': None if (clubs.get("@id") is None) or (clubs['@id'] is None) or (not clubs['@id']) else int(clubs['@id']),
			'league': None if (clubs.get("@league") is None) or (clubs['@league'] is None) or (not clubs['@league']) else clubs['@league'],
			'league_id': None if (clubs.get("@league_id") is None) or (clubs['@league_id'] is None) or (not clubs['@league_id']) else int(clubs['@league_id']),
			'season': None if (clubs.get("@season") is None) or (clubs['@season'] is None) or (not clubs['@season']) else clubs['@season'],
			'minutes': None if (clubs.get("@minutes") is None) or (clubs['@minutes'] is None) or (not clubs['@minutes']) else int(clubs['@minutes']),
			'appearences': None if (clubs.get("@appearences") is None) or (clubs['@appearences'] is None) or (not clubs['@appearences']) else int(clubs['@appearences']),
			'lineups': None if (clubs.get("@lineups") is None) or (clubs['@lineups'] is None) or (not clubs['@lineups']) else int(clubs['@lineups']),
			'substitute_in': None if (clubs.get("@substitute_in") is None) or (clubs['@substitute_in'] is None) or (not clubs['@substitute_in']) else int(clubs['@substitute_in']),
			'substitute_out': None if (clubs.get("@substitute_out") is None) or (clubs['@substitute_out'] is None) or (not clubs['@substitute_out']) else int(clubs['@substitute_out']),
			'substitutes_on_bench': None if (clubs.get("@substitutes_on_bench") is None) or (clubs['@substitutes_on_bench'] is None) or (not clubs['@substitutes_on_bench']) else int(clubs['@substitutes_on_bench']),
			'goals': None if (clubs.get("@goals") is None) or (clubs['@goals'] is None) or (not clubs['@goals']) else int(clubs['@goals']),
			'yellowcards': None if (clubs.get("@yellowcards") is None) or (clubs['@yellowcards'] is None) or (not clubs['@yellowcards']) else int(clubs['@yellowcards']),
			'yellowred': None if (clubs.get("@yellowred") is None) or (clubs['@yellowred'] is None) or (not clubs['@yellowred']) else int(clubs['@yellowred']),
			'redcards': None if (clubs.get("@redcards") is None) or (clubs['@redcards'] is None) or (not clubs['@redcards']) else int(clubs['@redcards']),
			'isCaptain': None if (clubs.get("@isCaptain") is None) or (clubs['@isCaptain'] is None) or (not clubs['@isCaptain']) else int(clubs['@isCaptain']),
			'shotsTotal': None if (clubs.get("@shotsTotal") is None) or (clubs['@shotsTotal'] is None) or (not clubs['@shotsTotal']) else int(clubs['@shotsTotal']),
			'shotsOn': None if (clubs.get("@shotsOn") is None) or (clubs['@shotsOn'] is None) or (not clubs['@shotsOn']) else int(clubs['@shotsOn']),
			'goalsConceded': None if (clubs.get("@goalsConceded") is None) or (clubs['@goalsConceded'] is None) or (not clubs['@goalsConceded']) else int(clubs['@goalsConceded']),
			'assists': None if (clubs.get("@assists") is None) or (clubs['@assists'] is None) or (not clubs['@assists']) else int(clubs['@assists']),
			'fouldDrawn': None if (clubs.get("@fouldDrawn") is None) or (clubs['@fouldDrawn'] is None) or (not clubs['@fouldDrawn']) else int(clubs['@fouldDrawn']),
			'foulsCommitted': None if (clubs.get("@foulsCommitted") is None) or (clubs['@foulsCommitted'] is None) or (not clubs['@foulsCommitted']) else int(clubs['@foulsCommitted']),
			'tackles': None if (clubs.get("@tackles") is None) or (clubs['@tackles'] is None) or (not clubs['@tackles']) else int(clubs['@tackles']),
			'blocks': None if (clubs.get("@blocks") is None) or (clubs['@blocks'] is None) or (not clubs['@blocks']) else int(clubs['@blocks']),
			'crossesTotal': None if (clubs.get("@crossesTotal") is None) or (clubs['@crossesTotal'] is None) or (not clubs['@crossesTotal']) else int(clubs['@crossesTotal']),
			'crossesAccurate': None if (clubs.get("@crossesAccurate") is None) or (clubs['@crossesAccurate'] is None) or (not clubs['@crossesAccurate']) else int(clubs['@crossesAccurate']),
			'interceptions': None if (clubs.get("@interceptions") is None) or (clubs['@interceptions'] is None) or (not clubs['@interceptions']) else int(clubs['@interceptions']),
			'clearances': None if (clubs.get("@clearances") is None) or (clubs['@clearances'] is None) or (not clubs['@clearances']) else int(clubs['@clearances']),
			'dispossesed': None if (clubs.get("@dispossesed") is None) or (clubs['@dispossesed'] is None) or (not clubs['@dispossesed']) else int(clubs['@dispossesed']),
			'saves': None if (clubs.get("@saves") is None) or (clubs['@saves'] is None) or (not clubs['@saves']) else int(clubs['@saves']),
			'insideBoxSaves': None if (clubs.get("@insideBoxSaves") is None) or (clubs['@insideBoxSaves'] is None) or (not clubs['@insideBoxSaves']) else int(clubs['@insideBoxSaves']),
			'duelsTotal': None if (clubs.get("@duelsTotal") is None) or (clubs['@duelsTotal'] is None) or (not clubs['@duelsTotal']) else int(clubs['@duelsTotal']),
			'duelsWon': None if (clubs.get("@duelsWon") is None) or (clubs['@duelsWon'] is None) or (not clubs['@duelsWon']) else int(clubs['@duelsWon']),
			'dribbleAttempts': None if (clubs.get("@dribbleAttempts") is None) or (clubs['@dribbleAttempts'] is None) or (not clubs['@dribbleAttempts']) else int(clubs['@dribbleAttempts']),
			'dribbleSucc': None if (clubs.get("@dribbleSucc") is None) or (clubs['@dribbleSucc'] is None) or (not clubs['@dribbleSucc']) else int(clubs['@dribbleSucc']),
			'penComm': None if (clubs.get("@penComm") is None) or (clubs['@penComm'] is None) or (not clubs['@penComm']) else int(clubs['@penComm']),
			'penWon': None if (clubs.get("@penWon") is None) or (clubs['@penWon'] is None) or (not clubs['@penWon']) else int(clubs['@penWon']),
			'penScored': None if (clubs.get("@penScored") is None) or (clubs['@penScored'] is None) or (not clubs['@penScored']) else int(clubs['@penScored']),
			'penMissed': None if (clubs.get("@penMissed") is None) or (clubs['@penMissed'] is None) or (not clubs['@penMissed']) else int(clubs['@penMissed']),
			'penSaved': None if (clubs.get("@penSaved") is None) or (clubs['@penSaved'] is None) or (not clubs['@penSaved']) else int(clubs['@penSaved']),
			'passes': None if (clubs.get("@passes") is None) or (clubs['@passes'] is None) or (not clubs['@passes']) else int(clubs['@passes']),
			'pAccuracy': None if (clubs.get("@pAccuracy") is None) or (clubs['@pAccuracy'] is None) or (not clubs['@pAccuracy']) else int(clubs['@pAccuracy']),
			'keyPasses': None if (clubs.get("@keyPasses") is None) or (clubs['@keyPasses'] is None) or (not clubs['@keyPasses']) else int(clubs['@keyPasses']),
			'woordworks': None if (clubs.get("@woordworks") is None) or (clubs['@woordworks'] is None) or (not clubs['@woordworks']) else int(clubs['@woordworks']),
			'rating': None if (clubs.get("@rating") is None) or (clubs['@rating'] is None) or (not clubs['@rating']) else float(clubs['@rating'])

		}
		return [data]
	if type(clubs) is list:
			for info in clubs:
				data = {
					'name': None if (info.get("@name") is None) or (info['@name'] is None) or (not info['@name']) else info['@name'],
					'id': None if (info.get("@id") is None) or (info['@id'] is None) or (not info['@id']) else int(info['@id']),
					'league': None if (info.get("@league") is None) or (info['@league'] is None) or (not info['@league']) else info['@league'],
					'league_id': None if (info.get("@league_id") is None) or (info['@league_id'] is None) or (not info['@league_id']) else int(info['@league_id']),
					'season': None if (info.get("@season") is None) or (info['@season'] is None) or (not info['@season']) else info['@season'],
					'minutes': None if (info.get("@minutes") is None) or (info['@minutes'] is None) or (not info['@minutes']) else int(info['@minutes']),
					'appearences': None if (info.get("@appearences") is None) or (info['@appearences'] is None) or (not info['@appearences']) else int(info['@appearences']),
					'lineups': None if (info.get("@lineups") is None) or (info['@lineups'] is None) or (not info['@lineups']) else int(info['@lineups']),
					'substitute_in': None if (info.get("@substitute_in") is None) or (info['@substitute_in'] is None) or (not info['@substitute_in']) else int(info['@substitute_in']),
					'substitute_out': None if (info.get("@substitute_out") is None) or (info['@substitute_out'] is None) or (not info['@substitute_out']) else int(info['@substitute_out']),
					'substitutes_on_bench': None if (info.get("@substitutes_on_bench") is None) or (info['@substitutes_on_bench'] is None) or (not info['@substitutes_on_bench']) else int(info['@substitutes_on_bench']),
					'goals': None if (info.get("@goals") is None) or (info['@goals'] is None) or (not info['@goals']) else int(info['@goals']),
					'yellowcards': None if (info.get("@yellowcards") is None) or (info['@yellowcards'] is None) or (not info['@yellowcards']) else int(info['@yellowcards']),
					'yellowred': None if (info.get("@yellowred") is None) or (info['@yellowred'] is None) or (not info['@yellowred']) else int(info['@yellowred']),
					'redcards': None if (info.get("@redcards") is None) or (info['@redcards'] is None) or (not info['@redcards']) else int(info['@redcards']),
					'isCaptain': None if (info.get("@isCaptain") is None) or (info['@isCaptain'] is None) or (not info['@isCaptain']) else int(info['@isCaptain']),
					'shotsTotal': None if (info.get("@shotsTotal") is None) or (info['@shotsTotal'] is None) or (not info['@shotsTotal']) else int(info['@shotsTotal']),
					'shotsOn': None if (info.get("@shotsOn") is None) or (info['@shotsOn'] is None) or (not info['@shotsOn']) else int(info['@shotsOn']),
					'goalsConceded': None if (info.get("@goalsConceded") is None) or (info['@goalsConceded'] is None) or (not info['@goalsConceded']) else int(info['@goalsConceded']),
					'assists': None if (info.get("@assists") is None) or (info['@assists'] is None) or (not info['@assists']) else int(info['@assists']),
					'fouldDrawn': None if (info.get("@fouldDrawn") is None) or (info['@fouldDrawn'] is None) or (not info['@fouldDrawn']) else int(info['@fouldDrawn']),
					'foulsCommitted': None if (info.get("@foulsCommitted") is None) or (info['@foulsCommitted'] is None) or (not info['@foulsCommitted']) else int(info['@foulsCommitted']),
					'tackles': None if (info.get("@tackles") is None) or (info['@tackles'] is None) or (not info['@tackles']) else int(info['@tackles']),
					'blocks': None if (info.get("@blocks") is None) or (info['@blocks'] is None) or (not info['@blocks']) else int(info['@blocks']),
					'crossesTotal': None if (info.get("@crossesTotal") is None) or (info['@crossesTotal'] is None) or (not info['@crossesTotal']) else int(info['@crossesTotal']),
					'crossesAccurate': None if (info.get("@crossesAccurate") is None) or (info['@crossesAccurate'] is None) or (not info['@crossesAccurate']) else int(info['@crossesAccurate']),
					'interceptions': None if (info.get("@interceptions") is None) or (info['@interceptions'] is None) or (not info['@interceptions']) else int(info['@interceptions']),
					'clearances': None if (info.get("@clearances") is None) or (info['@clearances'] is None) or (not info['@clearances']) else int(info['@clearances']),
					'dispossesed': None if (info.get("@dispossesed") is None) or (info['@dispossesed'] is None) or (not info['@dispossesed']) else int(info['@dispossesed']),
					'saves': None if (info.get("@saves") is None) or (info['@saves'] is None) or (not info['@saves']) else int(info['@saves']),
					'insideBoxSaves': None if (info.get("@insideBoxSaves") is None) or (info['@insideBoxSaves'] is None) or (not info['@insideBoxSaves']) else int(info['@insideBoxSaves']),
					'duelsTotal': None if (info.get("@duelsTotal") is None) or (info['@duelsTotal'] is None) or (not info['@duelsTotal']) else int(info['@duelsTotal']),
					'duelsWon': None if (info.get("@duelsWon") is None) or (info['@duelsWon'] is None) or (not info['@duelsWon']) else int(info['@duelsWon']),
					'dribbleAttempts': None if (info.get("@dribbleAttempts") is None) or (info['@dribbleAttempts'] is None) or (not info['@dribbleAttempts']) else int(info['@dribbleAttempts']),
					'dribbleSucc': None if (info.get("@dribbleSucc") is None) or (info['@dribbleSucc'] is None) or (not info['@dribbleSucc']) else int(info['@dribbleSucc']),
					'penComm': None if (info.get("@penComm") is None) or (info['@penComm'] is None) or (not info['@penComm']) else int(info['@penComm']),
					'penWon': None if (info.get("@penWon") is None) or (info['@penWon'] is None) or (not info['@penWon']) else int(info['@penWon']),
					'penScored': None if (info.get("@penScored") is None) or (info['@penScored'] is None) or (not info['@penScored']) else int(info['@penScored']),
					'penMissed': None if (info.get("@penMissed") is None) or (info['@penMissed'] is None) or (not info['@penMissed']) else int(info['@penMissed']),
					'penSaved': None if (info.get("@penSaved") is None) or (info['@penSaved'] is None) or (not info['@penSaved']) else int(info['@penSaved']),
					'passes': None if (info.get("@passes") is None) or (info['@passes'] is None) or (not info['@passes']) else int(info['@passes']),
					'pAccuracy': None if (info.get("@pAccuracy") is None) or (info['@pAccuracy'] is None) or (not info['@pAccuracy']) else int(info['@pAccuracy']),
					'keyPasses': None if (info.get("@keyPasses") is None) or (info['@keyPasses'] is None) or (not info['@keyPasses']) else int(info['@keyPasses']),
					'woordworks': None if (info.get("@woordworks") is None) or (info['@woordworks'] is None) or (not info['@woordworks']) else int(info['@woordworks']),
					'rating': None if (info.get("@rating") is None) or (info['@rating'] is None) or (not info['@rating']) else float(info['@rating'])

				}
				clubList.append(data)
			return clubList


def transfersTransfer(transfers):
	transferList = []
	if type(transfers) is dict:
		data = {
			'date': None if (transfers.get("@date") is None) or (transfers['@date'] is None) or (not transfers['@date']) else dateUTCFormat(transfers['@date']),
			'from': None if (transfers.get("@from") is None) or (transfers['@from'] is None) or (not transfers['@from']) else transfers['@from'],
			'from_id': None if (transfers.get("@from_id") is None) or (transfers['@from_id'] is None) or (not transfers['@from_id']) else int(transfers['@from_id']),
			'to': None if (transfers.get("@to") is None) or (transfers['@to'] is None) or (not transfers['@to']) else transfers['@to'],
			'to_id': None if (transfers.get("@to_id") is None) or (transfers['@to_id'] is None) or (not transfers['@to_id']) else int(transfers['@to_id']),
			'type': None if (transfers.get("@type") is None) or (transfers['@type'] is None) or (not transfers['@type']) else transfers['@type']
		}
		return [data]
	if type(transfers) is list:
			for info in transfers:
				data = {
					'date': None if (info.get("@date") is None) or (info['@date'] is None) or (not info['@date']) else dateUTCFormat(info['@date']),
					'from': None if (info.get("@from") is None) or (info['@from'] is None) or (not info['@from']) else info['@from'],
					'from_id': None if (info.get("@from_id") is None) or (info['@from_id'] is None) or (not info['@from_id']) else int(info['@from_id']),
					'to': None if (info.get("@to") is None) or (info['@to'] is None) or (not info['@to']) else info['@to'],
					'to_id': None if (info.get("@to_id") is None) or (info['@to_id'] is None) or (not info['@to_id']) else int(info['@to_id']),
					'type': None if (info.get("@type") is None) or (info['@type'] is None) or (not info['@type']) else info['@type']
				}
				transferList.append(data)
			return transferList


def playerstat(playerId):
	url = "http://www.goalserve.com/getfeed/c05d9fc7d36540dcdfaa08d9e34f661d/soccerstats/player/"+str(playerId)+"?json=1"

	payload={}
	headers = {}

	response = requests.request("GET", url, headers=headers, data=payload)
	data = response.json()
	data = None if data['players'] is None else data['players']
	if data is None:
		return None
	else:
		modified_stat_data = {
			'category': None if (data.get("@category") is None) or (data['@category'] is None) or (not data['@category']) else data['@category'],
			'player': None if (data.get("player") is None) or (data['player'] is None) or (not data['player']) else {
					'common_name': None if (data['player'].get("@common_name") is None) or (data['player']['@common_name'] is None) or (not data['player']['@common_name']) else data['player']['@common_name'],
					'id': None if (data['player'].get("@id") is None) or (data['player']['@id'] is None) or (not data['player']['@id']) else int(data['player']['@id']),
					'name': None if (data['player'].get("name") is None) or (data['player']['name'] is None) or (not data['player']['name']) else data['player']['name'],
					'firstname': None if (data['player'].get("firstname") is None) or (data['player']['firstname'] is None) or (not data['player']['firstname']) else data['player']['firstname'],
					'lastname': None if (data['player'].get("lastname") is None) or (data['player']['lastname'] is None) or (not data['player']['lastname']) else data['player']['lastname'],
					'team': None if (data['player'].get("team") is None) or (data['player']['team'] is None) or (not data['player']['team']) else data['player']['team'],
					'teamid': None if (data['player'].get("teamid") is None) or (data['player']['teamid'] is None) or (not data['player']['teamid']) else int(data['player']['teamid']),
					'nationality': None if (data['player'].get("nationality") is None) or (data['player']['nationality'] is None) or (not data['player']['nationality']) else data['player']['nationality'],
					'birthdate': None if (data['player'].get("birthdate") is None) or (data['player']['birthdate'] is None) or (not data['player']['birthdate']) else dateUTC2Format(data['player']['birthdate']),
					'age': None if (data['player'].get("age") is None) or (data['player']['age'] is None) or (not data['player']['age']) else int(data['player']['age']),
					'birthcountry': None if (data['player'].get("birthcountry") is None) or (data['player']['birthcountry'] is None) or (not data['player']['birthcountry']) else data['player']['birthcountry'],
					'birthplace': None if (data['player'].get("birthplace") is None) or (data['player']['birthplace'] is None) or (not data['player']['birthplace']) else data['player']['birthplace'],
					'position': None if (data['player'].get("position") is None) or (data['player']['position'] is None) or (not data['player']['position']) else data['player']['position'],
					'height': None if (data['player'].get("height") is None) or (data['player']['height'] is None) or (not data['player']['height']) else data['player']['height'],
					'weight': None if (data['player'].get("weight") is None) or (data['player']['weight'] is None) or (not data['player']['weight']) else data['player']['weight'],
					'preferredFoot': None if (data['player'].get("preferredFoot") is None) or (data['player']['preferredFoot'] is None) or (not data['player']['preferredFoot']) else data['player']['preferredFoot'],
					'marketValueEUR': None if (data['player'].get("marketValueEUR") is None) or (data['player']['marketValueEUR'] is None) or (not data['player']['marketValueEUR']) else int(data['player']['marketValueEUR']),
					'image': None if (data['player'].get("image") is None) or (data['player']['image'] is None) or (not data['player']['image']) else data['player']['image'],
					'statistic': None if (data['player'].get("statistic") is None) or (data['player']['statistic'] is None) or (not data['player']['statistic']) else {
						'club': None if (data['player']['statistic'].get("club") is None) or (data['player']['statistic']['club'] is None) or (not data['player']['statistic']['club']) else statisticIntlClub(data['player']['statistic']['club'])
					},
					'statistic_cups': None if (data['player'].get("statistic_cups") is None) or (data['player']['statistic_cups'] is None) or (not data['player']['statistic_cups']) else {
						'club': None if (data['player']['statistic_cups'].get("club") is None) or (data['player']['statistic_cups']['club'] is None) or (not data['player']['statistic_cups']['club']) else statisticIntlClub(data['player']['statistic_cups']['club'])
					},
					'statistic_cups_intl': None if (data['player'].get("statistic_cups_intl") is None) or (data['player']['statistic_cups_intl'] is None) or (not data['player']['statistic_cups_intl']) else {
						'club': None if (data['player']['statistic_cups_intl'].get("club") is None) or (data['player']['statistic_cups_intl']['club'] is None) or (not data['player']['statistic_cups_intl']['club']) else statisticIntlClub(data['player']['statistic_cups_intl']['club'])
					},
					'statistic_intl': None if (data['player'].get("statistic_intl") is None) or (data['player']['statistic_intl'] is None) or (not data['player']['statistic_intl']) else {
						'club': None if (data['player']['statistic_intl'].get("club") is None) or (data['player']['statistic_intl']['club'] is None) or (not data['player']['statistic_intl']['club']) else statisticIntlClub(data['player']['statistic_intl']['club'])
					},
					'trophies': None if (data['player'].get("trophies") is None) or (data['player']['trophies'] is None) or (not data['player']['trophies']) else {
						'trophy': None if (data['player']['trophies'].get("trophy") is None) or (data['player']['trophies']['trophy'] is None) or (not data['player']['trophies']['trophy']) else trophiesTrophy(data['player']['trophies']['trophy'])
					},
					'transfers': None if (data['player'].get("transfers") is None) or (data['player']['transfers'] is None) or (not data['player']['transfers']) else {
						'transfer': None if (data['player']['transfers'].get("transfer") is None) or (data['player']['transfers']['transfer'] is None) or (not data['player']['transfers']['transfer']) else transfersTransfer(data['player']['transfers']['transfer'])
					},
					'sidelined': None if (data['player'].get("sidelined") is None) or (data['player']['sidelined'] is None) or (not data['player']['sidelined']) else {
						'item': None if (data['player']['sidelined'].get("item") is None) or (data['player']['sidelined']['item'] is None) or (not data['player']['sidelined']['item']) else sidelinedItems(data['player']['sidelined']['item'])
					},
					'overall_clubs': None if (data['player'].get("overall_clubs") is None) or (data['player']['overall_clubs'] is None) or (not data['player']['overall_clubs']) else {
						'stats': None if (data['player']['overall_clubs'].get("stats") is None) or (data['player']['overall_clubs']['stats'] is None) or (not data['player']['overall_clubs']['stats']) else {
							'appearences': None if (data['player']['overall_clubs']['stats'].get("@appearences") is None) or (data['player']['overall_clubs']['stats']['@appearences'] is None) or (not data['player']['overall_clubs']['stats']['@appearences']) else int(data['player']['overall_clubs']['stats']['@appearences']),
							'lineups': None if (data['player']['overall_clubs']['stats'].get("@lineups") is None) or (data['player']['overall_clubs']['stats']['@lineups'] is None) or (not data['player']['overall_clubs']['stats']['@lineups']) else int(data['player']['overall_clubs']['stats']['@lineups']),
							'substitute_in': None if (data['player']['overall_clubs']['stats'].get("@substitute_in") is None) or (data['player']['overall_clubs']['stats']['@substitute_in'] is None) or (not data['player']['overall_clubs']['stats']['@substitute_in']) else int(data['player']['overall_clubs']['stats']['@substitute_in']),
							'isCaptain': None if (data['player']['overall_clubs']['stats'].get("@isCaptain") is None) or (data['player']['overall_clubs']['stats']['@isCaptain'] is None) or (not data['player']['overall_clubs']['stats']['@isCaptain']) else int(data['player']['overall_clubs']['stats']['@isCaptain']),
							'shotsTotal': None if (data['player']['overall_clubs']['stats'].get("@shotsTotal") is None) or (data['player']['overall_clubs']['stats']['@shotsTotal'] is None) or (not data['player']['overall_clubs']['stats']['@shotsTotal']) else int(data['player']['overall_clubs']['stats']['@shotsTotal']),
							'shotsOn': None if (data['player']['overall_clubs']['stats'].get("@shotsOn") is None) or (data['player']['overall_clubs']['stats']['@shotsOn'] is None) or (not data['player']['overall_clubs']['stats']['@shotsOn']) else int(data['player']['overall_clubs']['stats']['@shotsOn']),
							'goalsConceded': None if (data['player']['overall_clubs']['stats'].get("@goalsConceded") is None) or (data['player']['overall_clubs']['stats']['@goalsConceded'] is None) or (not data['player']['overall_clubs']['stats']['@goalsConceded']) else int(data['player']['overall_clubs']['stats']['@goalsConceded']),
							'assists': None if (data['player']['overall_clubs']['stats'].get("@assists") is None) or (data['player']['overall_clubs']['stats']['@assists'] is None) or (not data['player']['overall_clubs']['stats']['@assists']) else int(data['player']['overall_clubs']['stats']['@assists']),
							'fouldDrawn': None if (data['player']['overall_clubs']['stats'].get("@fouldDrawn") is None) or (data['player']['overall_clubs']['stats']['@fouldDrawn'] is None) or (not data['player']['overall_clubs']['stats']['@fouldDrawn']) else int(data['player']['overall_clubs']['stats']['@fouldDrawn']),
							'foulsCommitted': None if (data['player']['overall_clubs']['stats'].get("@foulsCommitted") is None) or (data['player']['overall_clubs']['stats']['@foulsCommitted'] is None) or (not data['player']['overall_clubs']['stats']['@foulsCommitted']) else int(data['player']['overall_clubs']['stats']['@foulsCommitted']),
							'tackles': None if (data['player']['overall_clubs']['stats'].get("@tackles") is None) or (data['player']['overall_clubs']['stats']['@tackles'] is None) or (not data['player']['overall_clubs']['stats']['@tackles']) else int(data['player']['overall_clubs']['stats']['@tackles']),
							'blocks': None if (data['player']['overall_clubs']['stats'].get("@blocks") is None) or (data['player']['overall_clubs']['stats']['@blocks'] is None) or (not data['player']['overall_clubs']['stats']['@blocks']) else int(data['player']['overall_clubs']['stats']['@blocks']),
							'crossesTotal': None if (data['player']['overall_clubs']['stats'].get("@crossesTotal") is None) or (data['player']['overall_clubs']['stats']['@crossesTotal'] is None) or (not data['player']['overall_clubs']['stats']['@crossesTotal']) else int(data['player']['overall_clubs']['stats']['@crossesTotal']),
							'crossesAccurate': None if (data['player']['overall_clubs']['stats'].get("@crossesAccurate") is None) or (data['player']['overall_clubs']['stats']['@crossesAccurate'] is None) or (not data['player']['overall_clubs']['stats']['@crossesAccurate']) else int(data['player']['overall_clubs']['stats']['@crossesAccurate']),
							'interceptions': None if (data['player']['overall_clubs']['stats'].get("@interceptions") is None) or (data['player']['overall_clubs']['stats']['@interceptions'] is None) or (not data['player']['overall_clubs']['stats']['@interceptions']) else int(data['player']['overall_clubs']['stats']['@interceptions']),
							'clearances': None if (data['player']['overall_clubs']['stats'].get("@clearances") is None) or (data['player']['overall_clubs']['stats']['@clearances'] is None) or (not data['player']['overall_clubs']['stats']['@clearances']) else int(data['player']['overall_clubs']['stats']['@clearances']),
							'dispossesed': None if (data['player']['overall_clubs']['stats'].get("@dispossesed") is None) or (data['player']['overall_clubs']['stats']['@dispossesed'] is None) or (not data['player']['overall_clubs']['stats']['@dispossesed']) else int(data['player']['overall_clubs']['stats']['@dispossesed']),
							'saves': None if (data['player']['overall_clubs']['stats'].get("@saves") is None) or (data['player']['overall_clubs']['stats']['@saves'] is None) or (not data['player']['overall_clubs']['stats']['@saves']) else int(data['player']['overall_clubs']['stats']['@saves']),
							'insideBoxSaves': None if (data['player']['overall_clubs']['stats'].get("@insideBoxSaves") is None) or (data['player']['overall_clubs']['stats']['@insideBoxSaves'] is None) or (not data['player']['overall_clubs']['stats']['@insideBoxSaves']) else int(data['player']['overall_clubs']['stats']['@insideBoxSaves']),
							'duelsTotal': None if (data['player']['overall_clubs']['stats'].get("@duelsTotal") is None) or (data['player']['overall_clubs']['stats']['@duelsTotal'] is None) or (not data['player']['overall_clubs']['stats']['@duelsTotal']) else int(data['player']['overall_clubs']['stats']['@duelsTotal']),
							'duelsWon': None if (data['player']['overall_clubs']['stats'].get("@duelsWon") is None) or (data['player']['overall_clubs']['stats']['@duelsWon'] is None) or (not data['player']['overall_clubs']['stats']['@duelsWon']) else int(data['player']['overall_clubs']['stats']['@duelsWon']),
							'dribbleAttempts': None if (data['player']['overall_clubs']['stats'].get("@dribbleAttempts") is None) or (data['player']['overall_clubs']['stats']['@dribbleAttempts'] is None) or (not data['player']['overall_clubs']['stats']['@dribbleAttempts']) else int(data['player']['overall_clubs']['stats']['@dribbleAttempts']),
							'dribbleSucc': None if (data['player']['overall_clubs']['stats'].get("@dribbleSucc") is None) or (data['player']['overall_clubs']['stats']['@dribbleSucc'] is None) or (not data['player']['overall_clubs']['stats']['@dribbleSucc']) else int(data['player']['overall_clubs']['stats']['@dribbleSucc']),
							'penComm': None if (data['player']['overall_clubs']['stats'].get("@penComm") is None) or (data['player']['overall_clubs']['stats']['@penComm'] is None) or (not data['player']['overall_clubs']['stats']['@penComm']) else int(data['player']['overall_clubs']['stats']['@penComm']),
							'penWon': None if (data['player']['overall_clubs']['stats'].get("@penWon") is None) or (data['player']['overall_clubs']['stats']['@penWon'] is None) or (not data['player']['overall_clubs']['stats']['@penWon']) else int(data['player']['overall_clubs']['stats']['@penWon']),
							'penScored': None if (data['player']['overall_clubs']['stats'].get("@penScored") is None) or (data['player']['overall_clubs']['stats']['@penScored'] is None) or (not data['player']['overall_clubs']['stats']['@penScored']) else int(data['player']['overall_clubs']['stats']['@penScored']),
							'penMissed': None if (data['player']['overall_clubs']['stats'].get("@penMissed") is None) or (data['player']['overall_clubs']['stats']['@penMissed'] is None) or (not data['player']['overall_clubs']['stats']['@penMissed']) else int(data['player']['overall_clubs']['stats']['@penMissed']),
							'penSaved': None if (data['player']['overall_clubs']['stats'].get("@penSaved") is None) or (data['player']['overall_clubs']['stats']['@penSaved'] is None) or (not data['player']['overall_clubs']['stats']['@penSaved']) else int(data['player']['overall_clubs']['stats']['@penSaved']),
							'passes': None if (data['player']['overall_clubs']['stats'].get("@passes") is None) or (data['player']['overall_clubs']['stats']['@passes'] is None) or (not data['player']['overall_clubs']['stats']['@passes']) else int(data['player']['overall_clubs']['stats']['@passes']),
							'pAccuracy': None if (data['player']['overall_clubs']['stats'].get("@pAccuracy") is None) or (data['player']['overall_clubs']['stats']['@pAccuracy'] is None) or (not data['player']['overall_clubs']['stats']['@pAccuracy']) else int(data['player']['overall_clubs']['stats']['@pAccuracy']),
							'keyPasses': None if (data['player']['overall_clubs']['stats'].get("@keyPasses") is None) or (data['player']['overall_clubs']['stats']['@keyPasses'] is None) or (not data['player']['overall_clubs']['stats']['@keyPasses']) else int(data['player']['overall_clubs']['stats']['@keyPasses']),
							'woordworks': None if (data['player']['overall_clubs']['stats'].get("@woordworks") is None) or (data['player']['overall_clubs']['stats']['@woordworks'] is None) or (not data['player']['overall_clubs']['stats']['@woordworks']) else int(data['player']['overall_clubs']['stats']['@woordworks']),
							'minutesPlayed': None if (data['player']['overall_clubs']['stats'].get("@minutesPlayed") is None) or (data['player']['overall_clubs']['stats']['@minutesPlayed'] is None) or (not data['player']['overall_clubs']['stats']['@minutesPlayed']) else int(data['player']['overall_clubs']['stats']['@minutesPlayed']),
							'rating': None if (data['player']['overall_clubs']['stats'].get("@rating") is None) or (data['player']['overall_clubs']['stats']['@rating'] is None) or (not data['player']['overall_clubs']['stats']['@rating']) else float(data['player']['overall_clubs']['stats']['@rating']),
						}
					}
			}

		}
		# with open("playerstats.json", 'w') as f:
		# 	f.write(json.dumps(modified_stat_data, indent=3))
		return modified_stat_data



# player_data = playerstat(61954)