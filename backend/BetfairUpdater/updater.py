from datetime import datetime
import os

from apscheduler.schedulers.background import BackgroundScheduler
from BetfairUpdater import betfair_api
# from webservices.views.LibGoalServeAPI import *
        
def start():
    scheduler = BackgroundScheduler()
    
    # scheduler.add_job(betfair_api.UpdateHomeAwaySoccerstats, 'interval', minutes=100)
    # scheduler.add_job(betfair_api.storeEvent, 'interval', minutes=1000)
    
    # scheduler.add_job(betfair_api.StoreOddsByTeam, 'interval', minutes=30)
    


    # scheduler.add_job(betfair_api.SaveAllData, 'interval', minutes=100)
    # scheduler.add_job(betfair_api.SaveAllLeaguesData, 'interval', minutes=300)
    # scheduler.add_job(betfair_api.SaveAllTeamsData, 'interval', minutes=600)
    # scheduler.add_job(betfair_api.SaveAllSeasonData, 'interval', minutes=900)
    # scheduler.add_job(betfair_api.SaveAllPlayerData, 'interval', minutes=1200)
    # scheduler.add_job(betfair_api.SaveAllTeamsbyPlayerData, 'interval', minutes=1500)
    # scheduler.add_job(betfair_api.SavePlayerSatistics, 'interval', minutes=150)
    # scheduler.add_job(betfair_api.Saveodds, 'interval', minutes=450)
    # scheduler.add_job(betfair_api.SaveAllFixtureData, 'interval', minutes=2000)

    # scheduler.add_job(betfair_api.UpdateTeamSeasonLeagueStatisticsSportsMonk, 'interval', minutes=2000)
    

    # scheduler.add_job(betfair_api.SaveAllTeamStatitics, 'interval', minutes=310)
    
    # scheduler.add_job(betfair_api.SaveAllTeamStatitics, 'interval', minutes=310)
    # scheduler.add_job(betfair_api.UpdateFixtureByDate, 'interval', minutes=1)
    # Store Team By Season Name
    # scheduler.add_job(betfair_api.SaveTeamBySeasonSportsMonk, 'interval', minutes=310)
    
    #Goal Serve
    # scheduler.add_job(betfair_api.MatchTeamStatGOALSERVE, 'interval', minutes=200)
    # scheduler.add_job(betfair_api.LiveScoreRedis, 'interval', minutes=3)

    #----------Betfair Scheduler----------------------------------------------------
    # scheduler.add_job(betfair_api.storeEvent, 'interval', minutes=100)
    # scheduler.add_job(betfair_api.storeDailySummeryDetail, 'interval', minutes=5)
    # scheduler.add_job(betfair_api.StoreSportsRadar, 'interval', minutes=8)
    # scheduler.add_job(betfair_api.storeSofascoreLiveScoreDetail, 'interval', minutes=1000)
    scheduler.add_job(betfair_api.storeEvent, 'interval', minutes=2500)
    scheduler.add_job(betfair_api.storeDailySummeryDetail, 'interval', minutes=720)
    scheduler.add_job(betfair_api.StoreSportsRadar, 'interval', minutes=4500)
    scheduler.add_job(betfair_api.UpdateBetfairOrder, 'interval', minutes=1000)
    scheduler.start()
    

