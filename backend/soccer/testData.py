import requests
from bs4 import BeautifulSoup
import argparse
import mysql.connector
import certifi
import urllib3

http = urllib3.PoolManager( cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

################################################################
# This is the sample instructions to insert the match plan and match-player info.
# insert_match_plan("2014-2015", "eng-premier-league", 1,5)  match 1~ 5 eg: England 1 ~ 380
# direct write the info for inserting..... for saving time.
#################################################################
# mydb = mysql.connector.connect(
# 	host="localhost",
# 	user="root",
# 	passwd="",
# 	database="soccer"
# )
# mydb = mysql.connector.connect(
#   host="localhost",
#   user="sportsbeting",
#   passwd="Bwow[EshS7Z7v6s]",
#   database="sportsbeting"
# )
# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   passwd="",
#   database="soccer"
# )
# URL : http://dev1.myvtd.site/phpmyadmin
# database name : sportsbeting
# password : Bwow[EshS7Z7v6s]
# user name : sportsbeting

# mycursor = mydb.cursor()
def switch_season(argument):
	switcher = {
	  
		"2020": 64,
		"2020-2021" : 799,
		"2021"		: 844,
		'2021-2022' : 857,
	}
	return switcher.get(argument, "null")
def switch_league(argument):
	switcher = {
		"esp-primera-division": 16,  #spain
		"eng-premier-league": 6,   #England
		"bundesliga": 8,   #Germany
		"ita-serie-a" : 11,  #italy
		"fra-ligue-1" : 7,   #france
		"ned-eredivisie": 12,  #Netherland
		"aut-bundesliga": 1,  #Austria
		"por-primeira-liga": 14,  #portugal
		"por-liga-sagres": 14,
		"por-liga-zon-sagres":14,
		"gre-superleague": 9,   #Greece
		"gre-super-league": 9,   #Greece
		"tur-sueperlig": 19,   #Turkey
		"nor-eliteserien": 13,  #Norway
		"nor-tippeligaen":13,
		"swe-allsvenskan": 17,  #Sweden
		"sui-super-league": 18,   #Swiztland
		"den-superliga": 5,     #Denmark
		"den-sas-ligaen":5,
		"ukr-premyer-liga": 20,     #Ukraine       
		"bul-parva-liga" : 2 , #bulgaria
		"cze-1-fotbalova-liga": 3,      #Chezch
		"cze-gambrinus-liga": 3,
		"cro-1-hnl": 4 ,          #Croatia
		"hun-nb-i": 10,     #Hungary
		"hun-nb1": 10,
		"hun-otp-liga":10,
		"srb-super-liga": 15    #Serbia
	}
	return switcher.get(argument, "null")

added_matches_count = 0
added_player_count = 0
def getTeamImage(team_name):
	from slugify import slugify
	src ='';
	try:
		URL = f"https://www.worldfootball.net/teams/{slugify(team_name)}/"
		page = requests.get(URL)
		soup = BeautifulSoup(page.content, "html.parser")
		results = soup.find('div', class_="emblem")

		img = results.find_all("img")
		for ev_tr in img:
			src = ev_tr['src']
		print(src)
	except:
		src = ''
	return(src)
def doing_scraping_match_plan(season=None , league=None, firstMatch = None, lastMatch = None, newInsertFlag = False ):
	 
	#global added_matches_count
	print(f"---------------------------------{season}-{league}- start-----------------------------------------")
	if season:
		URL = f"https://www.worldfootball.net/all_matches/{league}-{season}/"
	else:
		URL = f"https://www.worldfootball.net/all_matches/eng-premier-league-2014-2015/"
		print("Enter the season !")
		return
	print(URL)
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, "html.parser")
	results = soup.find('table', class_="standard_tabelle")
	
	tr_results = results.find_all("tr")
	for ev_tr in tr_results:
		if ev_tr.find_all("td"):
			pass
		else:
			tr_results.remove(ev_tr)

	match_date=""
	if lastMatch ==  None :
		lastMatch = len(tr_results)
	if firstMatch == None:        # when the fist match start is not defined
		firstMatch = 1
	
	
	for i in range(firstMatch-1,lastMatch):

		all_td = tr_results[i].find_all("td")
		# print (all_td)
		print(all_td[0]);
		print(all_td[1]);
		print(all_td[2]);
		print(all_td[3]);
		print(all_td[4]);
		print(all_td[5]);
		print(all_td[6]);
		print('********************************************');
		if(len(all_td)) :
			print(f"------------------{season}-{league}- {i + 1}th Match process start --------------------")
			if all_td[0].text !="":
				match_date = convert_strDate_sqlDateFormat(all_td[0].text)
				
			match_total_result = all_td[5].text
			start_time = all_td[1].text
			match_status = all_td[6]
		# 	sql = f'SELECT team_id FROM team_list WHERE team_name = "{all_td[2].text}" UNION ' \
		# 		  f'SELECT team_id FROM team_list WHERE team_name = "{all_td[4].text}"'
		# 	#print(sql)
		# 	mycursor.execute(sql)
		# 	myresult = mycursor.fetchall()
		# 	home_team_id = myresult[0][0]
		# 	away_team_id = myresult[1][0]
			
		# 	total_home_score = "-"
		# 	total_away_score = "-"
		# 	half_home_score = "-"
		# 	half_away_score = "-"

		# 	#sql = f"SELECT * from season_match_plan where season_id = {switch_season(season)} and league_id = {switch_league(league)} and home_team_id = {home_team_id} and away_team_id = {away_team_id} and date = '{match_date}'"
			
		# 	if not newInsertFlag:   										# if this is option for updating the match schedule. then we must update 
		# 		print("    There is already info for match, so we will check update status.")
		# 		sql = f"SELECT * from season_match_plan where season_id = {switch_season(season)} and league_id = {switch_league(league)} and home_team_id = {home_team_id} and away_team_id = {away_team_id}"
		# 		mycursor.execute(sql)
		# 		myresult = mycursor.fetchall()
		# 		count_of_match = len(myresult)
		# 		if count_of_match == 1:										# when the match is only one in this league, so not repeated game
		# 			print("   there is only one game in this league !")
		# 			status = ""                                        
		# 			current_match_id = myresult[0][0]												
		# 			sql = f"SELECT * from match_team_player_info where match_id = {current_match_id}"
		# 			mycursor.execute(sql)
		# 			myresult = mycursor.fetchall()
		# 			if len(myresult):                                       # match info is in match_team_player_info , this is already completed game no need to update
		# 				print("    No need to update!")
		# 			else:                                                   # Need to update , will check the status of the match and decide the update
		# 				if "(" in match_total_result:                       # if the match was finished
		# 					print("   Match was finished , will update soon")
		# 					total = match_total_result.split(" ")[0]
		# 					half = match_total_result.split(" ")[1]
		# 					status = "END"
		# 					if len(total.split(":")) > 1:
		# 						total_home_score = total.split(":")[0].strip()
		# 						total_away_score = total.split(":")[1].strip()
		# 						if len(half.split(":")) > 1:
		# 							half_home_score = half.split(":")[0][1:]
		# 							half_away_score = half.split(":")[1][:-1]
		# 					print(f"   {match_date}, {home_team_id}, {away_team_id},{total_home_score}-{total_away_score},{half_home_score}-{half_away_score} ")
		# 					sql = f"UPDATE season_match_plan set date = '{match_date}', time = '{start_time}', total_home_score = {total_home_score}, half_home_score = {half_home_score}, total_away_score = {total_away_score} , half_away_score = {half_away_score} , status = '{status}' where match_id = {current_match_id}"
							
		# 					mycursor.execute(sql)
		# 					mydb.commit()

		# 					sql = f"UPDATE season_match_plan AS a SET WN = WEEK(a.date - INTERVAL 1 DAY)+1 , c_WN = (SELECT WEEK  FROM date_week_map AS b WHERE a.date = b.date ) where match_id = {current_match_id}"
		# 					mycursor.execute(sql)
		# 					mydb.commit()

		# 					print("    1 completed game updated, ID: ", current_match_id, " in match_plan")

		# 					if all_td[5].find("a"):
		# 						href_info = all_td[5].find("a")['href']
		# 						url = "https://www.worldfootball.net"+href_info
		# 						insert_match_team_player_info(url , current_match_id, home_team_id, away_team_id)

		# 				else:  
		# 					status = ""                                             # if the match is yet planned or resch
		# 					if "resch" in match_total_result :
		# 						status = "resch"
		# 						sql = f"UPDATE season_match_plan set date = '{match_date}' , time = '{start_time}', status = '{status}' where match_id = {current_match_id}"
		# 						mycursor.execute(sql)
		# 						mydb.commit()
		# 						sql = f"UPDATE season_match_plan AS a SET WN = WEEK(a.date - INTERVAL 1 DAY)+1 ,c_WN = (SELECT WEEK  FROM date_week_map AS b WHERE a.date = b.date ) where match_id = {current_match_id}"
		# 						mycursor.execute(sql)
		# 						mydb.commit()
		# 						print("    1 resch game updated, ID: ", current_match_id, " in match_plan")
		# 					elif len (match_status.find_all("img")):
		# 						status = "LIVE"
		# 						sql = f"UPDATE season_match_plan set date = '{match_date}' , time = '{start_time}', status = '{status}' where match_id = {current_match_id}"
		# 						mycursor.execute(sql)
		# 						mydb.commit()
		# 						sql = f"UPDATE season_match_plan AS a SET WN = WEEK(a.date - INTERVAL 1 DAY)+1 ,c_WN = (SELECT WEEK  FROM date_week_map AS b WHERE a.date = b.date ) where match_id = {current_match_id}"
		# 						mycursor.execute(sql)
		# 						mydb.commit()
		# 						print("    1 LIVE game updated, ID: ", current_match_id, " in match_plan")
		# 					elif "dec" in match_total_result :
		# 						print("    this is dec game")
		# 					elif '-' not in match_total_result:				# END game but no half score
		# 						print("   Special Match was finished , will update soon")
		# 						total = match_total_result.split(" ")[0]
								
		# 						status = "END"
		# 						if len(total.split(":")) > 1:
		# 							total_home_score = total.split(":")[0].strip()
		# 							total_away_score = total.split(":")[1].strip()
		# 							half_home_score = total_home_score
		# 							half_away_score = total_away_score
								
		# 						print(f"   {match_date}, {home_team_id}, {away_team_id},{total_home_score}-{total_away_score},{half_home_score}-{half_away_score} ")
		# 						sql = f"UPDATE season_match_plan set date = '{match_date}', time = '{start_time}', total_home_score = {total_home_score}, half_home_score = {half_home_score}, total_away_score = {total_away_score} , half_away_score = {half_away_score} , status = '{status}' where match_id = {current_match_id}"
								
		# 						mycursor.execute(sql)
		# 						mydb.commit()

		# 						sql = f"UPDATE season_match_plan AS a SET WN = WEEK(a.date - INTERVAL 1 DAY)+1 , c_WN = (SELECT WEEK  FROM date_week_map AS b WHERE a.date = b.date ) where match_id = {current_match_id}"
		# 						mycursor.execute(sql)
		# 						mydb.commit()

		# 						print("    1 completed game updated, ID: ", current_match_id, " in match_plan")

		# 						if all_td[5].find("a"):
		# 							href_info = all_td[5].find("a")['href']
		# 							url = "https://www.worldfootball.net"+href_info
		# 							insert_match_team_player_info(url , current_match_id, home_team_id, away_team_id)
		# 					else:
		# 						sql = f"UPDATE season_match_plan set date = '{match_date}' , time = '{start_time}', status = '{status}' where match_id = {current_match_id}"
		# 						print(sql)
		# 						mycursor.execute(sql)
		# 						mydb.commit()
		# 						sql = f"UPDATE season_match_plan AS a SET WN = WEEK(a.date - INTERVAL 1 DAY)+1 ,c_WN = (SELECT WEEK  FROM date_week_map AS b WHERE a.date = b.date ) where match_id = {current_match_id}"
		# 						mycursor.execute(sql)
		# 						mydb.commit()
		# 						print("    1 planned game updated, ID: ", current_match_id, " in match_plan")
				
		# 		if count_of_match > 1 :										# if the match is repeated game,eg: Croatia, Hungary
		# 			print("    there are many same matches in this league, so will check the fixture carefully")
		# 			if "(" in match_total_result:							# if the match is ended game
		# 				sql = f"SELECT * from season_match_plan where season_id = {switch_season(season)} and league_id = {switch_league(league)} and home_team_id = {home_team_id} and away_team_id = {away_team_id} and status = 'END' and date = '{match_date}'"
		# 				mycursor.execute(sql)
		# 				ended_Match_array = mycursor.fetchall()
		# 				if len(ended_Match_array):							# if matching date-ended game is existing in DB
		# 					print("    No need to update")
		# 				else : 												# no matching ended game exist in DB find match id and update andinsert
		# 					sql = f"SELECT * from season_match_plan where season_id = {switch_season(season)} and league_id = {switch_league(league)} and home_team_id = {home_team_id} and away_team_id = {away_team_id} and status != 'END' order by date"
		# 					mycursor.execute(sql)
		# 					myresult = mycursor.fetchall()
		# 					if len(myresult):								# finding first not-ended  game in DB and update and insert them.
		# 						print("   Match was finished , will update soon")
		# 						current_match_id = myresult[0][0]
		# 						total = match_total_result.split(" ")[0]
		# 						half = match_total_result.split(" ")[1]
		# 						status = "END"
		# 						if len(total.split(":")) > 1:
		# 							total_home_score = total.split(":")[0].strip()
		# 							total_away_score = total.split(":")[1].strip()
		# 							if len(half.split(":")) > 1:
		# 								half_home_score = half.split(":")[0][1:]
		# 								half_away_score = half.split(":")[1][:-1]
		# 						print(f"   {match_date}, {home_team_id}, {away_team_id},{total_home_score}-{total_away_score},{half_home_score}-{half_away_score} ")
		# 						sql = f"UPDATE season_match_plan set date = '{match_date}', time = '{start_time}', total_home_score = {total_home_score}, half_home_score = {half_home_score}, total_away_score = {total_away_score} , half_away_score = {half_away_score} , status = '{status}' where match_id = {current_match_id}"
								
		# 						mycursor.execute(sql)
		# 						mydb.commit()
		# 						sql = f"UPDATE season_match_plan AS a SET WN = WEEK(a.date - INTERVAL 1 DAY)+1 ,c_WN = (SELECT WEEK  FROM date_week_map AS b WHERE a.date = b.date ) where match_id = {current_match_id}"
		# 						mycursor.execute(sql)
		# 						mydb.commit()
		# 						print("    1 completed game updated, ID: ", current_match_id, " in match_plan")

		# 						if all_td[5].find("a"):
		# 							href_info = all_td[5].find("a")['href']
		# 							url = "https://www.worldfootball.net"+href_info
		# 							insert_match_team_player_info(url , current_match_id, home_team_id, away_team_id)

		# 			else :													# if the match is yet planned or resch game						
		# 				status = ""
		# 				if "resch" in match_total_result :
		# 					sql = f"SELECT * from season_match_plan where season_id = {switch_season(season)} and league_id = {switch_league(league)} and home_team_id = {home_team_id} and away_team_id = {away_team_id} and status = 'resch' and date ='{match_date}'"
		# 					mycursor.execute(sql)
		# 					result = mycursor.fetchall()
		# 					if len(result):
		# 						print("    No need to update")
		# 					else:
		# 						#sql = f"SELECT * from season_match_plan where season_id = {switch_season(season)} and league_id = {switch_league(league)} and home_team_id = {home_team_id} and away_team_id = {away_team_id} and status = ''"
		# 						sql = f"SELECT * from season_match_plan where season_id = {switch_season(season)} and league_id = {switch_league(league)} and home_team_id = {home_team_id} and away_team_id = {away_team_id} and status != 'END'"
		# 						mycursor.execute(sql)
		# 						result = mycursor.fetchall()
		# 						if len(result):
		# 							current_match_id = result[0][0]
		# 							status = "resch"
		# 							sql = f"UPDATE season_match_plan set date = '{match_date}' , time = '{start_time}', status = '{status}' where match_id = {current_match_id}"
		# 							mycursor.execute(sql)
		# 							mydb.commit()
		# 							sql = f"UPDATE season_match_plan AS a SET WN = WEEK(a.date - INTERVAL 1 DAY)+1 ,c_WN = (SELECT WEEK  FROM date_week_map AS b WHERE a.date = b.date ) where match_id = {current_match_id}"
		# 							mycursor.execute(sql)
		# 							mydb.commit()
		# 							print("    1 resch game updated, ID: ", current_match_id, " in match_plan")
		# 				elif len (match_status.find_all("img")):				# Live Match
		# 					sql = f"SELECT * from season_match_plan where season_id = {switch_season(season)} and league_id = {switch_league(league)} and home_team_id = {home_team_id} and away_team_id = {away_team_id} and status = 'LIVE' and date ='{match_date}'"
		# 					mycursor.execute(sql)
		# 					result = mycursor.fetchall()
		# 					if len(result):
		# 						print("    No need to update")
		# 					else:
		# 						sql = f"SELECT * from season_match_plan where season_id = {switch_season(season)} and league_id = {switch_league(league)} and home_team_id = {home_team_id} and away_team_id = {away_team_id} and status != 'END'"
		# 						mycursor.execute(sql)
		# 						result = mycursor.fetchall()
		# 						if len(result):
		# 							current_match_id = result[0][0]
		# 							status = "LIVE"
		# 							sql = f"UPDATE season_match_plan set date = '{match_date}' , time = '{start_time}', status = '{status}' where match_id = {current_match_id}"
		# 							mycursor.execute(sql)
		# 							mydb.commit()
		# 							sql = f"UPDATE season_match_plan AS a SET WN = WEEK(a.date - INTERVAL 1 DAY)+1 ,c_WN = (SELECT WEEK  FROM date_week_map AS b WHERE a.date = b.date ) where match_id = {current_match_id}"
		# 							mycursor.execute(sql)
		# 							mydb.commit()
		# 							print("    1 LIVE game updated, ID: ", current_match_id, " in match_plan")
		# 				elif "dec" in match_total_result:
		# 					print("    this is dec game")
		# 				elif '-' not in match_total_result:
		# 					print("   Special Match was finished , will update soon")
		# 					sql = f"SELECT * from season_match_plan where season_id = {switch_season(season)} and league_id = {switch_league(league)} and home_team_id = {home_team_id} and away_team_id = {away_team_id} and status = 'END' and date = '{match_date}'"
		# 					mycursor.execute(sql)
		# 					ended_Match_array = mycursor.fetchall()
		# 					if len(ended_Match_array):							# if matching date-ended game is existing in DB
		# 						print("    No need to update")
		# 					else : 												# no matching ended game exist in DB find match id and update andinsert
		# 						sql = f"SELECT * from season_match_plan where season_id = {switch_season(season)} and league_id = {switch_league(league)} and home_team_id = {home_team_id} and away_team_id = {away_team_id} and status != 'END' order by date"
		# 						mycursor.execute(sql)
		# 						myresult = mycursor.fetchall()
		# 						if len(myresult):								# finding first not-ended  game in DB and update and insert them.
		# 							print("   Match was finished , will update soon")
		# 							current_match_id = myresult[0][0]
		# 							total = match_total_result.split(" ")[0]
									
		# 							status = "END"
		# 							if len(total.split(":")) > 1:
		# 								total_home_score = total.split(":")[0].strip()
		# 								total_away_score = total.split(":")[1].strip()
		# 								half_home_score = total_home_score
		# 								half_away_score = total_away_score
		# 							print(f"   {match_date}, {home_team_id}, {away_team_id},{total_home_score}-{total_away_score},{half_home_score}-{half_away_score} ")
		# 							sql = f"UPDATE season_match_plan set date = '{match_date}', time = '{start_time}', total_home_score = {total_home_score}, half_home_score = {half_home_score}, total_away_score = {total_away_score} , half_away_score = {half_away_score} , status = '{status}' where match_id = {current_match_id}"
									
		# 							mycursor.execute(sql)
		# 							mydb.commit()
		# 							sql = f"UPDATE season_match_plan AS a SET WN = WEEK(a.date - INTERVAL 1 DAY)+1 ,c_WN = (SELECT WEEK  FROM date_week_map AS b WHERE a.date = b.date ) where match_id = {current_match_id}"
		# 							mycursor.execute(sql)
		# 							mydb.commit()
		# 							print("    1 completed game updated, ID: ", current_match_id, " in match_plan")

		# 							if all_td[5].find("a"):
		# 								href_info = all_td[5].find("a")['href']
		# 								url = "https://www.worldfootball.net"+href_info
		# 								insert_match_team_player_info(url , current_match_id, home_team_id, away_team_id)
		# 				else:
		# 					sql = f"SELECT * from season_match_plan where season_id = {switch_season(season)} and league_id = {switch_league(league)} and home_team_id = {home_team_id} and away_team_id = {away_team_id} and status = 'LIVE' and date ='{match_date}'"
		# 					mycursor.execute(sql)
		# 					result = mycursor.fetchall()
		# 					if len(result):
		# 						print("    No need to update")
		# 					else:
		# 						sql = f"SELECT * from season_match_plan where season_id = {switch_season(season)} and league_id = {switch_league(league)} and home_team_id = {home_team_id} and away_team_id = {away_team_id} and status != 'END'"
		# 						mycursor.execute(sql)
		# 						result = mycursor.fetchall()
		# 						if len(result):
		# 							current_match_id = result[0][0]
		# 							status = "LIVE"
		# 							sql = f"UPDATE season_match_plan set date = '{match_date}' , time = '{start_time}', status = '{status}' where match_id = {current_match_id}"
		# 							mycursor.execute(sql)
		# 							mydb.commit()
		# 							sql = f"UPDATE season_match_plan AS a SET WN = WEEK(a.date - INTERVAL 1 DAY)+1 ,c_WN = (SELECT WEEK  FROM date_week_map AS b WHERE a.date = b.date ) where match_id = {current_match_id}"
		# 							mycursor.execute(sql)
		# 							mydb.commit()
		# 							print("    1 Planned game updated, ID: ", current_match_id, " in match_plan")
		# 	if newInsertFlag:                                               # if this is option for new inserting, then we must insert the game into DB
		# 		print("This is new game for this season and league, so we will insert this!")
		# 		status = ""
		# 		if "(" in match_total_result:                           	# if the match was finished
		# 			print("   Match was finished ")
		# 			total = match_total_result.split(" ")[0]
		# 			half = match_total_result.split(" ")[1]
		# 			status = "END"
		# 			if len(total.split(":")) > 1:
		# 				total_home_score = total.split(":")[0].strip()
		# 				total_away_score = total.split(":")[1].strip()
		# 				if len(half.split(":")) > 1:
		# 					half_home_score = half.split(":")[0][1:]
		# 					half_away_score = half.split(":")[1][:-1]
		# 			print(f"   {match_date}, {home_team_id}, {away_team_id},{total_home_score}-{total_away_score},{half_home_score}-{half_away_score} ")
		# 			sql = "INSERT INTO season_match_plan (season_id, league_id , date, time, home_team_id , away_team_id , " \
		# 				"total_home_score, half_home_score, total_away_score, half_away_score, status)" \
		# 				"VALUES (%s, %s , %s, %s, %s, %s, %s, %s, %s, %s , %s)"
		# 			val = (switch_season(season), switch_league(league),match_date, start_time,home_team_id, away_team_id,total_home_score , \
		# 				half_home_score,total_away_score , half_away_score, status)
		# 			mycursor.execute(sql, val)
		# 			last_match_id = mycursor.lastrowid
		# 			mydb.commit()
		# 			print("    1 completed game inserted, ID: ", mycursor.lastrowid, " in match_plan")
					
					
		# 			sql = f"UPDATE season_match_plan AS a SET WN = WEEK(a.date - INTERVAL 1 DAY)+1 , c_WN = (SELECT WEEK  FROM date_week_map AS b WHERE a.date = b.date ) where match_id = {last_match_id}"
		# 			mycursor.execute(sql)
		# 			mydb.commit()

		# 			if all_td[5].find("a"):
		# 				href_info = all_td[5].find("a")['href']
		# 				url = "https://www.worldfootball.net"+href_info
		# 				insert_match_team_player_info(url , last_match_id, home_team_id, away_team_id)

		# 		else:                                                   # if the match is planned
		# 			print(f"   {match_date}, {home_team_id}, {away_team_id},{total_home_score}-{total_away_score},{half_home_score}-{half_away_score} ")
		# 			print("    Match is planned , not finished yet.")

		# 			if len (match_status.find_all("img")):
		# 				status = "LIVE"

		# 			if "resch" in match_total_result :
		# 				status = "resch"

		# 			sql = "INSERT INTO season_match_plan (season_id, league_id , date, time,home_team_id , away_team_id , " \
		# 				"total_home_score, half_home_score, total_away_score, half_away_score, status)" \
		# 				"VALUES (%s, %s ,%s, %s, %s, %s, %s, %s, %s, %s, %s)"
		# 			val = (switch_season(season), switch_league(league),match_date, start_time, home_team_id, away_team_id,total_home_score , \
		# 				half_home_score,total_away_score , half_away_score, status)
		# 			mycursor.execute(sql, val)
		# 			mydb.commit()
		# 			print("    1 planned game inserted, ID: ", mycursor.lastrowid, " in match_plan")
		# 			last_match_id = mycursor.lastrowid
		# 			sql = f"UPDATE season_match_plan AS a SET WN = WEEK(a.date - INTERVAL 1 DAY)+1 , c_WN = (SELECT WEEK  FROM date_week_map AS b WHERE a.date = b.date ) where match_id = {last_match_id}"
		# 			mycursor.execute(sql)
		# 			mydb.commit()

		# 	print(f"------------------{season}-{league}- {i + 1}th Match process end --------------------")
		# 	i += 1
		# 	#return


	print(f"---------------------------------{season}-{league} end -----------------------------------------")
def convert_strDate_sqlDateFormat(str_date):
	#  23/10/2020  - > 2020-10-23
	list = str_date.split('/');
	date = list[2] + '-' + list[1] + '-' + list[0];
	return date;

def ScrapTeamDataByLeague(URL,source):
	firstMatch = None
	lastMatch = None
	
	if source == 'worldfootball.net':
		page = requests.get(URL)
		soup = BeautifulSoup(page.content, "html.parser")
		results = soup.find('table', class_="standard_tabelle")
	
	if source == 'int.soccerway.com':
		headers = {
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
		}
		page = requests.get(URL,headers=headers)
		soup = BeautifulSoup(page.content, "html.parser")
		results = soup.find('table', class_="leaguetable sortable table detailed-table")
	
	print(results)
	tr_results = results.find_all("tr")
	for ev_tr in tr_results:
		if ev_tr.find_all("td"):
			pass
		else:
			tr_results.remove(ev_tr)

	match_date=""
	if lastMatch ==  None :
		lastMatch = len(tr_results)
	if firstMatch == None:        # when the fist match start is not defined
		firstMatch = 1
	for i in range(firstMatch-1,lastMatch):

		all_td = tr_results[i].find_all("td")

		print("**************************")
		print(all_td[0].text)
		print(all_td[1].text)
		print(all_td[2].text)
		print(all_td[3].text)
		print(all_td[4].text)
		print(all_td[5].text)
		print(all_td[6].text)
		print("--------------")
		# if(len(all_td)) :
		# 	if all_td[0].text !="":
		# 		match_date = convert_strDate_sqlDateFormat(all_td[0].text)
		# print(match_date)
	return 0
				
def ScrapAHByTeam(URL):

	from selenium import webdriver

	path_to_chromedriver = URL
	browser = webdriver.Chrome(executable_path = path_to_chromedriver)
	
	# if source == 'int.soccerway.com':
	# 	headers = {
	# 		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
	# 	}
	# 	page = requests.get(URL,headers=headers)
	# 	soup = BeautifulSoup(page.content, "html.parser")
	# 	results = soup.find('table', class_="leaguetable sortable table detailed-table")
	
	print(browser)
	# tr_results = results.find_all("tr")
	# for ev_tr in tr_results:
	# 	if ev_tr.find_all("td"):
	# 		pass
	# 	else:
	# 		tr_results.remove(ev_tr)

	# match_date=""
	# if lastMatch ==  None :
	# 	lastMatch = len(tr_results)
	# if firstMatch == None:        # when the fist match start is not defined
	# 	firstMatch = 1
	# for i in range(firstMatch-1,lastMatch):

	# 	all_td = tr_results[i].find_all("td")

	# 	print("**************************")
	# 	print(all_td[0].text)
	# 	print(all_td[1].text)
	# 	print(all_td[2].text)
	# 	print(all_td[3].text)
	# 	print(all_td[4].text)
	# 	print(all_td[5].text)
	# 	print(all_td[6].text)
	# 	print("--------------")
	# 	# if(len(all_td)) :
	# 	# 	if all_td[0].text !="":
	# 	# 		match_date = convert_strDate_sqlDateFormat(all_td[0].text)
	# 	# print(match_date)
	return 0

def ScrapData(url,HtmlElement,exemptField):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, "html.parser")
	results = soup.find('table', class_=HtmlElement)
	# print(results)
	final_result = []
	if results:
		final_result = GetScrapData(results,exemptField)

	else:
		headers = {
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
		}
		page = requests.get(url,headers=headers)
		soup = BeautifulSoup(page.content, "html.parser")
		results = soup.find('table', class_=HtmlElement)
		final_result = GetScrapData(results,exemptField)
	print(final_result)
	return final_result
def GetScrapData(results,exemptField):
	listarr =[]
	if results:
		thead_results = results.find_all("thead")
		tr_results = results.find_all("tr")
		all_th =[]
		for ev_tr  in tr_results:
			if ev_tr.find_all("td"):
				pass
			elif ev_tr.find_all("th"):
				th_result = ev_tr
				all_th = th_result.find_all("th")
				tr_results.remove(ev_tr)
			else:
				tr_results.remove(ev_tr)
		# print(all_th)
		# print(len(all_th))
		lastMatch = len(tr_results)
		firstMatch = 1
		alldata =[]
		for i in range(firstMatch-1,lastMatch):
			all_td = tr_results[i].find_all("td")

			eachrecord =[]
			for j in range(0,len(all_th)):
				eachcell =[]
				if j not in exemptField:
					# print(j)
					try:
						if all_td[j].find("img"):
							images = all_td[j].find('img')['src']
							eachcell={all_th[j].text:images}

						elif all_td[j].find("a"):
							href_info = all_td[j].find("a")['href']
							text = all_td[j].text
							eachcell={all_th[j].text:text}
						else:
							text = all_td[j].text
							eachcell={all_th[j].text:text}
						eachrecord.append(eachcell)
					except NameError:
						print(NameError)
					except:
						print('error')

			alldata.append(eachrecord)




	return alldata	
def GetScrapDataOrg(results,exemptField):
	listarr =[]
	if results:
		tr_results = results.find_all("tr")
		all_th =[]
		for ev_tr  in tr_results:
			if ev_tr.find_all("td"):
				pass
			elif ev_tr.find_all("th"):
				th_result = ev_tr
				all_th = th_result.find_all("th")
				tr_results.remove(ev_tr)
			else:
				tr_results.remove(ev_tr)
		# print(all_th)
		# print(len(all_th))
		lastMatch = len(tr_results)
		firstMatch = 1
		alldata =[]
		for i in range(firstMatch-1,lastMatch):
			all_td = tr_results[i].find_all("td")

			eachrecord =[]
			for j in range(0,len(all_th)):
				eachcell =[]
				if j not in exemptField:
					# print(j)
					try:
						if all_td[j].find("img"):
							images = all_td[j].find('img')['src']
							eachcell={'field_name':all_th[j].text,'value_type':'src','value':images}

						elif all_td[j].find("a"):
							href_info = all_td[j].find("a")['href']
							text = all_td[j].text
							eachcell={'field_name':all_th[j].text,'value_type':'href','value':href_info,'text':text}
						else:
							text = all_td[j].text
							eachcell={'field_name':all_th[j].text,'value_type':'text','value':text}
						eachrecord.append(eachcell)
					except NameError:
						print(NameError)
					except:
						print('error')

			alldata.append(eachrecord)




	return alldata	

def main():
	arr=[]
	# ScrapTeamDataByLeague('https://www.worldfootball.net/alltime_table/eng-premier-league/','worldfootball.net')
	# ScrapTeamDataByLeague('https://int.soccerway.com/national/austria/bundesliga/2020-2021/regular-season/r63649/','int.soccerway.com')
	# doing_scraping_match_plan("2020-2021","tur-sueperlig")
	# ScrapAHByTeam("https://www.oddsportal.com/soccer/algeria/super-cup/usm-alger-cr-belouizdad-6sPRGDJR/?r=1#ah;2")
	ScrapData('https://tradingeconomics.com/calendar','table table-hover table-condensed',arr)
	# arr=[1,11,12]
	# ScrapData('https://int.soccerway.com/national/austria/bundesliga/2020-2021/regular-season/r63649/','leaguetable sortable table detailed-table',arr)
if __name__ == "__main__":
    main()