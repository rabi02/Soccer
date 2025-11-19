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
mydb = mysql.connector.connect(
  host="localhost",
  user="sportsbeting",
  passwd="Bwow[EshS7Z7v6s]",
  database="sportsbeting"
)
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

mycursor = mydb.cursor()
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
def storeLeague():
	import json
	sql = f"SELECT  league_id,league_dname,league_title,img_src,slug_name from  league";
	mycursor.execute(sql)
	myresult = mycursor.fetchall()

	for result in myresult:
		PARAMS = {'league_id':result[0],'league_dname':result[1],'name':result[2],'logo_path':result[3],'slug_name':result[4],'collection_datasource':'www.worldfootball.net'}
		print(PARAMS)
		r = requests.post('http://sportsbetting.myvtd.site:8642/api/StoreLeagueOtherDataSource',data=json.dumps(PARAMS))
		print(r)
		print('--------------------')
def storeTeam ():
	import json
	sql = f"SELECT team_id,team_name,team_name_odd,img_src,league_id from team_list";
	mycursor.execute(sql)
	myresult = mycursor.fetchall()

	for result in myresult:
		PARAMS = {'team_id':result[0],'name':result[1],'team_name_odd':result[2],'logo_path':result[3],'league_id':result[4],'collection_datasource':'www.worldfootball.net'}
		print(PARAMS)
		r = requests.post('http://sportsbetting.myvtd.site:8642/api/StoreTeamOtherDataSource',data=json.dumps(PARAMS))
		print(r)
		print('--------------------')
def storeSeason():
	import json
	sql = f"SELECT * from season";
	mycursor.execute(sql)
	myresult = mycursor.fetchall()

	for result in myresult:
		PARAMS = {'season_id':result[0],'season_title':result[1],'collection_datasource':'www.worldfootball.net'}
		print(PARAMS)
		r = requests.post('http://sportsbetting.myvtd.site:8642/api/StoreSeasonOtherDataSource',data=json.dumps(PARAMS))
		print(r)
		print('--------------------')
def storeSeasonMatchPlan():
	import json
	sql = f"SELECT * from season_match_plan";
	mycursor.execute(sql)
	myresult = mycursor.fetchall()

	for result in myresult:
		PARAMS = {
			'match_id' :result[0] if result[0]  else 0,
			'season_id' :result[1] if result[1]  else 0,
			'league_id' :result[2] if result[2]  else 0,
			'date' :str(result[3]) if result[3]  else '',
			'time' :result[4] if result[4]  else '',
			'home_team_id' :result[5] if result[5]  else 0,
			'away_team_id' :result[6] if result[6]  else 0,
			'total_home_score' :result[7] if result[7]  else 0,
			'half_home_score' :result[8] if result[8]  else 0,
			'total_away_score' :result[9] if result[9]  else 0,
			'half_away_score' :result[10] if result[10]  else 0,
			'status' :result[11] if result[11]  else '',
			'Home_TGPR' :result[12] if result[12]  else '',
			'Away_TGPR' :result[13] if result[13]  else '',
			'D_Home_RS_8' :result[14] if result[14]  else '',
			'D_Home_ranking_8' :result[15] if result[15]  else '',
			'D_Home_RS_6' :result[16] if result[16]  else '',
			'D_Home_ranking_6' :result[17] if result[17]  else '',
			'home_team_score' :result[18] if result[18]  else '',
			'home_team_strength' :result[19] if result[19]  else '',
			'away_team_score' :result[20] if result[20]  else '',
			'away_team_strength' :result[21] if result[21]  else '',
			'D_Away_RS_8' :result[22] if result[22]  else '',
			'D_Away_ranking_8' :result[23] if result[23]  else '',
			'D_Away_RS_6' :result[24] if result[24]  else '',
			'D_Away_ranking_6' :result[25] if result[25]  else '',
			'HPPG' :result[26] if result[26]  else '',
			'HGDPG' :result[27] if result[27]  else '',
			'APPG' :result[28] if result[28]  else '',
			'AGDPG' :result[29] if result[29]  else '',
			'WN' :result[30] if result[30]  else 0,
			'c_WN' :result[31] if result[31]  else 0,
			'DSL_refer_id' :result[32] if result[32]  else 0,
			'DCL_refer_id' :result[33] if result[33]  else 0,
			'CL_mo_refer_id' :result[34] if result[34]  else 0,
			'collection_datasource':'www.worldfootball.net'
		}
		data =json.dumps(PARAMS)
		# print(data)
		r = requests.post('http://sportsbetting.myvtd.site:8642/api/StoreSeasonMatchPlanOtherDataSource',data=data)
		print(r)
		print('--------------------')
def storeMatchTeamPlayerInfo():
	import json
	sql = f"SELECT * from match_team_player_info where id > 1762";
	mycursor.execute(sql)
	myresult = mycursor.fetchall()

	for result in myresult:
		PARAMS = {
			'id' :result[0] if result[0]  else 0,
			'match_id' :result[1] if result[1]  else 0,
			'team_id' :result[2] if result[2]  else 0,
			'player_id' :result[3] if result[3]  else '',
			'goals' :result[4] if result[4]  else 0,
			'assists' :result[5] if result[5]  else 0,
			'collection_datasource':'www.worldfootball.net'
		}
		data =json.dumps(PARAMS)
		# print(data)
		r = requests.post('http://localhost:8000/api/StoreMatchTeamPlayerInfoOtherDataSource',data=data)
		print(r)
		print('--------------------') 

def storePlayerCareer():
	import json
	sql = f"SELECT * from player_career";
	mycursor.execute(sql)
	myresult = mycursor.fetchall()

	for result in myresult:
		PARAMS = {
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
		
		data =json.dumps(PARAMS)
		# print(data)
		r = requests.post('http://sportsbetting.myvtd.site:8642/api/StorePlayerCareerOtherDataSource',data=data)
		print(r)
		print('--------------------') 
def storePlayerList():
	import json
	sql = f"SELECT * from playerlist";
	mycursor.execute(sql)
	myresult = mycursor.fetchall()

	for result in myresult:
		PARAMS = {
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
		
		data =json.dumps(PARAMS)
		# print(data)
		r = requests.post('http://sportsbetting.myvtd.site:8642/api/StorePlayerListOtherDataSource',data=data)
		print(r)
		print('--------------------') 
def storeSeasonLeagueTeamInfo():
	import json
	sql = f"SELECT * from season_league_team_info";
	mycursor.execute(sql)
	myresult = mycursor.fetchall()

	for result in myresult:
		PARAMS = {
			
			'info_id' :result[0] if result[0]  else 0,
			'season_id' :result[1] if result[1]  else 0,
			'league_id' :result[2] if result[2]  else 0,
			'team_id' :result[3] if result[3]  else 0,
			't_mp' :result[4] if result[4]  else 0,
			't_w' :result[5] if result[5]  else 0,
			't_d' :result[6] if result[6]  else 0,
			't_l' :result[7] if result[7]  else 0,
			't_f' :result[8] if result[8]  else 0,
			't_a' :result[9] if result[9]  else 0,
			'h_mp' :result[10] if result[10]  else 0,
			'h_w' :result[11] if result[11]  else 0,
			'h_d' :result[12] if result[12]  else 0,
			'h_l' :result[13] if result[13]  else 0,
			'h_f' :result[14] if result[14]  else 0,
			'h_a' :result[15] if result[15]  else 0,
			'a_mp' :result[16] if result[16]  else 0,
			'a_w' :result[17] if result[17]  else 0,
			'a_d' :result[18] if result[18]  else 0,
			'a_l' :result[19] if result[19]  else 0,
			'a_f' :result[20] if result[20]  else 0,
			'D' :result[21] if result[21]  else 0,
			'P' :result[22] if result[22]  else 0,
			'PPG' :result[23] if result[23]  else'',
			'HPPG' :result[24] if result[24]  else '',
			'H_percent' :result[25] if result[25]  else '',
			'HG' :result[26] if result[26]  else '',
			'HDGPG' :result[27] if result[27]  else '',
			'HRS' :result[28] if result[28]  else '',
			'APPG' :result[29] if result[29]  else '',
			'A_percent' :result[30] if result[30]  else '',
			'AG' :result[31] if result[31]  else '',
			'ADGPG' :result[32] if result[32]  else '',
			'ARS' :result[33] if result[33]  else '',
			'S_H_ranking' :result[34] if result[34]  else '',
			'S_A_ranking' :result[35] if result[35]  else '',
			'collection_datasource':'www.worldfootball.net'
		}
		data =json.dumps(PARAMS)
		# print(data)
		r = requests.post('http://sportsbetting.myvtd.site:8642/api/StoreSeasonLeagueTeamInfoOtherDataSource',data=data)
		print(r)
		print('--------------------') 

def main():
	# storeSeasonLeagueTeamInfo()
	# storePlayerList()
	# storePlayerCareer()
	storeMatchTeamPlayerInfo()
	
	# storeSeason()
	# storeMatchTeamPlayerInfo()
	# storePlayerCareer()
	# storePlayerList()
	# storeSeasonLeagueTeamInfo()
	# doing_scraping_match_plan("2020-2021","aut-bundesliga")   # maximum 380 - 10 * 38
	# doing_scraping_match_plan("2020-2021","aut-bundesliga")			# maximum 132 - 6 * 22
	# doing_scraping_match_plan("2020-2021","eng-premier-league")		# maximum 380 - 10 * 38
	# doing_scraping_match_plan("2020-2021","bul-parva-liga")			# maximum 182 - 7 * 26 
	# doing_scraping_match_plan("2020-2021","fra-ligue-1")			# maximum 380 -  38 * 10
	# doing_scraping_match_plan("2020-2021","ned-eredivisie")			# maximum 306 -  9 * 34
	# doing_scraping_match_plan("2020-2021","bundesliga")				# maximum 306 -  9 * 34
	# doing_scraping_match_plan("2020-2021","ita-serie-a")			# maximum 380 -  10 * 38
	# doing_scraping_match_plan("2020-2021","por-primeira-liga")	
	# doing_scraping_match_plan("2020-2021","gre-super-league")
	# storeSeasonMatchPlan()
	# doing_scraping_match_plan("2020-2021","tur-sueperlig")
	# doing_scraping_match_plan("2021",	  "nor-eliteserien")
	# doing_scraping_match_plan("2021",	  "swe-allsvenskan")
	# doing_scraping_match_plan("2020-2021","sui-super-league")
	# doing_scraping_match_plan("2020-2021","den-superliga")
	# doing_scraping_match_plan("2020-2021","ukr-premyer-liga")
	# doing_scraping_match_plan("2020-2021","hun-nb-i")
	# doing_scraping_match_plan("2020-2021","cze-1-fotbalova-liga")
	# doing_scraping_match_plan("2020-2021","cro-1-hnl")
	# doing_scraping_match_plan("2020-2021","srb-super-liga")

	# print("")
	# print(f"-------- total added matches number is {added_matches_count} -------------")
	# print(f"-------- total added players number is {added_player_count} -------------")

if __name__ == "__main__":
    main()