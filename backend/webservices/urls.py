from django.urls import path,include
from django.conf import settings
from rest_framework.routers import DefaultRouter
from django.views.decorators.csrf import csrf_exempt
from webservices.views import *
from webservices import *
from . import views
from webservices.views  import user
from webservices.views  import cms
from webservices.views  import bitfair
from webservices.views  import ajax
from webservices.views  import GoalServe

from webservices.views  import sportradarTenis
from webservices.views  import sportradarSoccer
from webservices.views  import scraping
from webservices.views import scheduler
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('usercreate', csrf_exempt(views.user.CreateUser.as_view())),
    path('get_user_profile_data', csrf_exempt(views.user.GetUserProfileData.as_view())),
    path('userlogin', csrf_exempt(views.user.UserLogin.as_view()), name='user_login'),  
    path('saveblog', csrf_exempt(views.cms.CmsData.as_view()), name='saveblog'),  
    path('getallblogdata', csrf_exempt(views.cms.GetAllCms.as_view()), name='getallblogdata'), 
    path('EventListBitfair',csrf_exempt(views.bitfair.EventListBitfair), name='EventListBitfair'),
    path('verify_email/<str:token>', csrf_exempt(views.user.VerifyEmail.as_view())),
    path('password/reset', views.user.RequestPasswordResetEmail.as_view(),name="password_reset"),
    path('password/reset/confirm',views.user.SetNewPasswordView.as_view(), name='password_reset_done'),
    path('password/change',views.user.UpdatePassword.as_view(), name='password_change'),
    path('EventListBitfair2', csrf_exempt(views.bitfair.EventListBitfair2), name='EventListBitfair2'),
    path('Events', csrf_exempt(views.bitfair.Events), name='Events'),
    path('MarketInformation', csrf_exempt(views.bitfair.MarketInformation), name='MarketInformation'),
    path('HorseRacing', csrf_exempt(views.bitfair.HorseRacing), name='HorseRacing'),
    path('FootballCompetitions', csrf_exempt(views.bitfair.FootballCompetitions), name='FootballCompetitions'),
    path('PlaceOrders', csrf_exempt(views.bitfair.PlaceOrders), name='PlaceOrders'),
    path('AutobetPlaceOrders', csrf_exempt(views.bitfair.AutobetPlaceOrders), name='AutobetPlaceOrders'),
    path('GetTeamByCompitationIdSportsradar', csrf_exempt(views.bitfair.GetTeamByCompitationIdSportsradar), name='GetTeamByCompitationIdSportsradar'),
    path('GetMonthWiseReport', csrf_exempt(views.bitfair.GetMonthWiseReport), name='GetMonthWiseReport'),
    
    path('PlaceOrdersspbet', csrf_exempt(views.bitfair.PlaceOrdersspbet), name='PlaceOrdersspbet'),
    path('ListcurrentOrders', csrf_exempt(views.bitfair.ListcurrentOrders), name='ListcurrentOrders'),
    path('Listmarketbook', csrf_exempt(views.bitfair.Listmarketbook), name='Listmarketbook'),
    path('MarketPrices', csrf_exempt(views.bitfair.MarketPrices), name='MarketPrices'),
    path('profile', csrf_exempt(views.user.Profile.as_view()), name='profile'),
    path('edit_profile', csrf_exempt(views.user.EditProfile.as_view()), name='edit_profile'),
    # countries
    path("football/countries", csrf_exempt(views.bitfair.CountryList), name="country_list"),
    path("football/countries/<int:id>", csrf_exempt(views.bitfair.CountryList), name="country_by_id"),
    # leagues
    path("football/leagues", csrf_exempt(views.bitfair.Leagues), name="all_leagues"),
    path("football/leagues/<int:id>", csrf_exempt(views.bitfair.Leagues), name="leagues_by_id"),
    path("football/<str:country_id>/leagues", csrf_exempt(views.bitfair.LeaguesByCountry), name="leagues_by_country"),
    path("football/search/<str:league_name>", csrf_exempt(views.bitfair.SearchLeagues), name="search_leagues"),
    path("football/GetSaveLeague", csrf_exempt(views.bitfair.GetSaveLeague), name="GetSaveLeague"),
     # players
    path("football/players/<int:id>", csrf_exempt(views.bitfair.Player), name="players"),
    path("football/players/country/<int:country_id>", csrf_exempt(views.bitfair.Player), name="player_by_country"),
    path("football/players/search/<str:name>", csrf_exempt(views.bitfair.Player), name="player_by_name"),
    # teams
    path("football/teams/<int:id>", csrf_exempt(views.bitfair.Team), name="teams"),
    path("football/teams/country/<int:country_id>", csrf_exempt(views.bitfair.Team), name="teams_by_country"),
    path("football/teamssquads/<int:id>/<str:squadplayer>", csrf_exempt(views.bitfair.Teamssquads), name="teamsquads"),
    path("football/teambyseason/<int:id>", csrf_exempt(views.bitfair.Teambyseason), name="teambyseason"),
    path("football/teams/search/<str:team_name>", csrf_exempt(views.bitfair.Searchteambyname), name="teams_by_name"),
    path("football/<int:team_id>/current", csrf_exempt(views.bitfair.Currentleaguesbyteamid), name="current_leaguesby_teamid"),
    path("football/<int:team_id>/history", csrf_exempt(views.bitfair.Allleaguesbyteamid), name="all_leaguesby_teamid"),
    # odds
    path("football/odds/fixture/<int:fixture_id>/bookmarker/<int:bookmarker_id>", csrf_exempt(views.bitfair.OddsList), name="odds_by_id"),
    path("football/odds/fixture/<int:fixture_id>/market/<int:market_id>", csrf_exempt(views.bitfair.OddsMarketList), name="odds_by_marketid"),
    path("football/odds/fixture", csrf_exempt(views.bitfair.OddsbyfixtureidList), name="odds_by_fixtureid"),
    path("football/odds/inplay/fixture/<int:fixture_id>", csrf_exempt(views.bitfair.InplayOddsbyfixtureidList), name="odds_by_inplayfixtureid"),
    # standings
    path("football/standings/season/<int:season_id>", csrf_exempt(views.bitfair.StandingseasonList), name="standing_seasonlist"),
    path("football/standings/season/live/<int:season_id>", csrf_exempt(views.bitfair.StandingliveseasonList), name="standing_liveseasonlist"),
    path("football/standings/season/<int:season_id>/bookmarker/<int:round_id>", csrf_exempt(views.bitfair.Standingbyseasonroundid), name="standing_by_season_roundid"),
    path("football/standings/season/<int:season_id>/date/<str:start_date>", csrf_exempt(views.bitfair.Standingbyseasondate), name="standing_by_seasondate"),
    path("football/corrections/season/<int:season_id>", csrf_exempt(views.bitfair.Correctionsbyseasonid), name="correction_by_seasonid"),
    # fixtures
    path("football/fixtures/<int:fixture_id>", csrf_exempt(views.bitfair.MatchFixtures), name="fixture_by_id"),
    path("football/fixtures/updates", csrf_exempt(views.bitfair.MatchFixtures), name="fixture_updates"),
    path("football/fixtures/date/<str:start_date>", csrf_exempt(views.bitfair.FixtureByDate), name="fixture_by_date"),
    path("football/fixtures/date/<str:start_date>/<str:end_date>",csrf_exempt(views.bitfair.FixtureByDate),name="fixture_date_range"),
    path("football/fixtures/date/<str:start_date>/<str:end_date>/<int:team_id>",csrf_exempt(views.bitfair.FixtureByDate),name="fixture_date_range"),
    path("football/fixtures/multi/<str:id_list>",csrf_exempt(views.bitfair.FixtureByIdList),name="fixture_date_range"),
    # fixture_lineup
    path("football/fixtures/lineup/<int:fixture_id_lineup>", csrf_exempt(views.bitfair.Fixtures), name="fixture_lineup"),
    path("football/fixtures/events/<int:fixture_id_event>", csrf_exempt(views.bitfair.Fixtures), name="fixture_lineup_events"),
    path("football/MatchByLeague", csrf_exempt(views.bitfair.MatchByLeague), name="match_by_league"),
    path("football/save/all", csrf_exempt(views.scheduler.SaveAllData), name="save_all_data"),
    path("football/GetTeamById", csrf_exempt(views.bitfair.GetTeamById), name="GetTeamById"),
    path("football/GetPlayerTeamById", csrf_exempt(views.bitfair.GetPlayerByTeamId), name="GetPlayerTeamById"),
    # path("football/player/search",csrf_exempt(views.scheduler.Playersearch.as_view()), name="player_search"),
    path("football/OvaralTeamPlayer", csrf_exempt(views.bitfair.OvaralTeamPlayer), name="OvaralTeamPlayer"),
    path("football/player/all/search",csrf_exempt(views.bitfair.getallplayer.as_view()), name="player_all_search"),

    # path("football/betfairapi",csrf_exempt(views.bitfairapi.Betfairapi), name="betfairapi"),
    # path("football/player/search",csrf_exempt(views.scheduler.Playersearch.as_view()), name="player_search"),

    path("football/odds",csrf_exempt(views.bitfair.Footballodds.as_view()), name="footballodds"),
    path("football/save/odds", csrf_exempt(views.scheduler.Saveodds), name="save_odds_data"),
    #season statistics
    # path("football/fixtures/player/stats/<int:player_id>",csrf_exempt(views.bitfair.PlayerSatistics),name="player_statistics",),
    path("football/fixtures/season/stats/<int:season_id>",csrf_exempt(views.bitfair.SeasonSatistics),name="season_statistics",),

    #player statistics
    path("football/player-stats",csrf_exempt(views.bitfair.Playerstats.as_view()), name="player-stats"),
    path("football/PlayerstatsByPlayerId",csrf_exempt(views.bitfair.PlayerstatsByPlayerId.as_view()), name="PlayerstatsByPlayerId"),
    path("football/GetLeagueDetail",csrf_exempt(views.bitfair.GetLeagueDetail.as_view()), name="GetLeagueDetail"),
    path("football/save/player/stats", csrf_exempt(views.scheduler.SavePlayerSatistics), name="save_playersatistics_data"),
    path("football/fixtures/player/statistics/<int:player_id>",csrf_exempt(views.bitfair.AllPlayerSatistics),name="allplayer_statistics",),

    #competitions
    path("football/competitions",csrf_exempt(views.bitfair.Competitions.as_view()), name="football_competitions"),

    path('contactus', csrf_exempt(views.user.Contactus.as_view()), name="contactus"),
    path('usernotification', csrf_exempt(views.user.UserNotification.as_view()), name="usernotification"),
    #match schedule
    path("football/historic/data",csrf_exempt(views.bitfair.HistoricData.as_view()), name="historic_data"),
    path("football/match/schedule",csrf_exempt(views.bitfair.MatchSchedule.as_view()), name="match_schedule"),
    path("football/thisweekmatch/schedule",csrf_exempt(views.bitfair.ThisweekMatchSchedule.as_view()), name="thisweekmatch_schedule"),
    path("football/RemoveDuplicatePlayer", csrf_exempt(views.scheduler.RemoveDuplicatePlayer), name="RemoveDuplicatePlayer"),
    path("JsonStringToJsonObject",csrf_exempt(views.bitfair.JsonStringToJsonObject),name="JsonStringToJsonObject",),
    path("football/save/allleagues", csrf_exempt(views.scheduler.SaveAllLeaguesData), name="save_allleagues_data"),
    path("football/save/allteams", csrf_exempt(views.scheduler.SaveAllTeamsData), name="save_allteams_data"),
    path("football/save/allseason", csrf_exempt(views.scheduler.SaveAllSeasonData), name="save_allseason_data"),
    path("football/save/allplayer", csrf_exempt(views.scheduler.SaveAllPlayerData), name="save_allplayer_data"),
    path("football/MatchByLeagueById", csrf_exempt(views.bitfair.MatchByLeagueById), name="MatchByLeagueById"),
    path("football/AllFixture", csrf_exempt(views.bitfair.AllFixture), name="AllFixture"),
    path("football/AllFixerByLeagueId/<int:league_id>", csrf_exempt(views.bitfair.AllFixerByLeagueId), name="AllFixerByLeagueId"),
    path("football/GetSessionByLeagueID",csrf_exempt(views.bitfair.GetSessionByLeagueID), name="GetSessionByLeagueID"),
    path("football/GetTeam",csrf_exempt(views.bitfair.GetTeam), name="GetTeam"),
    path("football/GetSeasonByTeamID/<int:team_id>", csrf_exempt(views.bitfair.GetSeasonByTeamID), name="GetSeasonByTeamID"),
    path("football/GetTeamStatistics",csrf_exempt(views.bitfair.GetTeamStatistics), name="GetTeamStatistics"),
    path("football/LoanInByTeam",csrf_exempt(views.bitfair.LoanInByTeam), name="LoanInByTeam"),
    
    path("football/save/allfixture", csrf_exempt(views.scheduler.SaveAllFixtureData), name="save_allfixture_data"),
    path("football/fixture",csrf_exempt(views.bitfair.FootballFixture.as_view()), name="footballfixture"),

    

    path("football/save/AllTeamsbyPlayerData",csrf_exempt(views.scheduler.SaveAllTeamsbyPlayerData), name="SaveAllTeamsbyPlayerData"),
    path("football/teamdetails",csrf_exempt(views.bitfair.FootballTeamdetailsByTeamId.as_view()), name="football_teamdetails"),
    path("football/seasoon/<int:season_id>", csrf_exempt(views.bitfair.SeasonList), name="season"),
    path("football/seasoon", csrf_exempt(views.bitfair.SeasonList), name="season_list"),
    path('subscription', csrf_exempt(views.user.SubscriptionView.as_view()), name="Subscription"),
    path('affiliateuser/register', csrf_exempt(views.user.AffiliateusersView.as_view()), name="affiliate_users"),
    # path('GetAffiliateList', csrf_exempt(views.user.GetAffiliateList), name="GetAffiliateList"),

    path("football/SeasonByLeagueId/<int:league_id>", csrf_exempt(views.bitfair.SeasonByLeagueId), name="season"),


    path('password-reset/',auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"),name='admin_password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"),name='password_reset_complete'),
    path("football/SaveAllTeamStatitics", csrf_exempt(views.scheduler.SaveAllTeamStatitics), name="SaveAllTeamStatitics"),

    path("cms/<str:slug>",csrf_exempt(views.cms.CmsDataView.as_view()), name='cms'),
    path("blog/published",csrf_exempt(views.cms.BlogPublishedView.as_view()),name='blog'),
    path("subscription/all",csrf_exempt(views.cms.GetSubscription.as_view()),name='subscription'),
    path("SubscriptionByid",csrf_exempt(views.cms.SubscriptionByid),name='SubscriptionByid'),
    path("StorePayment",csrf_exempt(views.cms.StorePayment),name='StorePayment'),

    path("allseasoon", csrf_exempt(views.bitfair.allseasoon), name="allseasoon"),
    path("livescore", csrf_exempt(views.bitfair.livescore), name="livescore"),
    path("SaveMessage", csrf_exempt(views.cms.SaveMessage), name="SaveMessage"),
    path("GetMessage", csrf_exempt(views.cms.GetMessage), name="GetMessage"),
    path("GetLeagues", csrf_exempt(views.bitfair.GetLeagues), name="GetLeagues"),
    path("GetLeagues/<int:id>", csrf_exempt(views.bitfair.GetLeagues), name="GetLeagues"),
    path("GetLeaguesCountryId/<int:country_id>", csrf_exempt(views.bitfair.GetLeaguesCountryId), name="GetLeaguesCountryId"),
    path("GetSeasonByLeagueID/<int:league_id>", csrf_exempt(views.bitfair.GetSeasonByLeagueID), name="GetSeasonByLeagueID"),

    #Collect Data from Other dara source
    path("StoreLeagueOtherDataSource", csrf_exempt(views.bitfair.StoreLeagueOtherDataSource), name="StoreLeagueOtherDataSource"),
    path("StoreTeamOtherDataSource", csrf_exempt(views.bitfair.StoreTeamOtherDataSource), name="StoreTeamOtherDataSource"),
    path("StoreSeasonOtherDataSource", csrf_exempt(views.bitfair.StoreSeasonOtherDataSource), name="StoreSeasonOtherDataSource"),
    path("StoreSeasonMatchPlanOtherDataSource", csrf_exempt(views.bitfair.StoreSeasonMatchPlanOtherDataSource), name="StoreSeasonMatchPlanOtherDataSource"),
    
    path("StoreMatchTeamPlayerInfoOtherDataSource", csrf_exempt(views.bitfair.StoreMatchTeamPlayerInfoOtherDataSource), name="StoreMatchTeamPlayerInfoOtherDataSource"),
    path("StorePlayerCareerOtherDataSource", csrf_exempt(views.bitfair.StorePlayerCareerOtherDataSource), name="StorePlayerCareerOtherDataSource"),
    path("StorePlayerListOtherDataSource", csrf_exempt(views.bitfair.StorePlayerListOtherDataSource), name="StorePlayerListOtherDataSource"),
    path("StoreSeasonLeagueTeamInfoOtherDataSource", csrf_exempt(views.bitfair.StoreSeasonLeagueTeamInfoOtherDataSource), name="StoreSeasonLeagueTeamInfoOtherDataSource"),
    
    path("ScrapToolForVisiter", csrf_exempt(views.scraping.ScrapToolForVisiter), name="ScrapToolForVisiter"),
    path("ScrapTooldownload/<slug>", csrf_exempt(views.scraping.ScrapTooldownload), name="ScrapTooldownload"),
    path("SaveScrapingData", csrf_exempt(views.scraping.SaveScrapingData), name="SaveScrapingData"),
    path("RunScrapingScriptOuterPage/<slug>", csrf_exempt(views.scraping.RunScrapingScriptOuterPage), name="RunScrapingScriptOuterPage"),
    path("ScrapFromSoccerstats", csrf_exempt(views.scraping.ScrapFromSoccerstats), name="ScrapFromSoccerstats"),


    path("saveScrapData", csrf_exempt(views.scraping.saveScrapData), name="saveScrapData"),
    # path("GetTeamDataFromSoccerstats", csrf_exempt(views.scraping.GetTeamDataFromSoccerstats), name="GetTeamDataFromSoccerstats"),
    path("GetSeasonLeagueWiseData/<season_id>", csrf_exempt(views.scraping.GetSeasonLeagueWiseData), name="GetSeasonLeagueWiseData"),
    path("TeamDetailsScrapDataBySoccerSets", csrf_exempt(views.scraping.TeamDetailsScrapDataBySoccerSets), name="TeamDetailsScrapDataBySoccerSets"),
    path("pullDataFromFootballdataCoUk", csrf_exempt(views.scraping.pullDataFromFootballdataCoUk), name="pullDataFromFootballdataCoUk"),
    path("football/GetTeamByLeagueIds", csrf_exempt(views.bitfair.GetTeamByLeagueIds), name="GetTeamByLeagueIds"),

    #API for AI and probability
    path("ai/MatchTeamInfoByLeague", csrf_exempt(views.bitfair.MatchTeamInfoByLeague), name="MatchTeamInfoByLeague"),
    path("ai/GetTeamDetailFromMatch", csrf_exempt(views.bitfair.GetTeamDetailFromMatch), name="GetTeamDetailFromMatch"),
    path("ai/Head2HeadCalculation", csrf_exempt(views.bitfair.Head2HeadCalculation), name="Head2HeadCalculation"),
    path("ai/GetTeamByLeagueName", csrf_exempt(views.bitfair.GetTeamByLeagueName), name="GetTeamByLeagueName"),
    path("ai/GetTeamStatisticsByTeam/<team_id>", csrf_exempt(views.bitfair.GetTeamStatisticsByTeam), name="GetTeamStatisticsByTeam"),
    path("ai/historic_data",csrf_exempt(views.bitfair.Histroydata), name="Histroydata"),

    #Ajax
    path("ajax/GetAjaxPredictionOdds", csrf_exempt(views.ajax.GetAjaxPredictionOdds), name="GetAjaxPredictionOdds"),
    path("ajax/getSeasonByLeague", csrf_exempt(views.ajax.getSeasonByLeague), name="getSeasonByLeague"),
    path("ajax/saveTeamByseasonSportsmonk", csrf_exempt(views.ajax.saveTeamByseasonSportsmonk), name="saveTeamByseasonSportsmonk"),
    path("ajax/GetAjaxViewMatchByDate", csrf_exempt(views.ajax.GetAjaxViewMatchByDate), name="GetAjaxViewMatchByDate"),
    path("ajax/GetAjaxLeagueList", csrf_exempt(views.ajax.GetAjaxLeagueList), name="GetAjaxLeagueList"),
    path("ajax/GetAjaxTeamList", csrf_exempt(views.ajax.GetAjaxTeamList), name="GetAjaxTeamList"),
    path("ajax/getAjaxTeamByLeague", csrf_exempt(views.ajax.getAjaxTeamByLeague), name="getAjaxTeamByLeague"),
    path("football/bannerlist", csrf_exempt(views.bitfair.bannerlist), name="bannerlist"),

    #GoalServe API
    path("goalserve/GoalServeAPI", csrf_exempt(views.GoalServe.GoalServeAPI), name="GoalServeAPI"),
    path("football/MatchByLeagueGoalserve", csrf_exempt(views.GoalServe.MatchByLeagueGoalserve), name="MatchByLeagueGoalserve"),
    path("football/GetTodayOdds", csrf_exempt(views.GoalServe.GetTodayOdds), name="GetTodayOdds"),
    path("football/GetSquadByTeam", csrf_exempt(views.GoalServe.GetSquadByTeam), name="GetSquadByTeam"),
    path("football/GetPlayerInTeam", csrf_exempt(views.GoalServe.GetPlayerInTeam), name="GetPlayerInTeam"),
    path("football/GetPlayerOutTeam", csrf_exempt(views.GoalServe.GetPlayerOutTeam), name="GetPlayerOutTeam"),
    path("football/OvaralTeamPlayerGoalServer", csrf_exempt(views.GoalServe.OvaralTeamPlayerGoalServer), name="OvaralTeamPlayerGoalServer"),
    path("football/GetPrediction/<int:match_id>", csrf_exempt(views.GoalServe.GetPrediction), name="GetPrediction"),
    path("football/UpcomingMatch", csrf_exempt(views.GoalServe.UpcomingMatch), name="UpcomingMatch"),


    path("football/sportrader/getSportsradarMapping", csrf_exempt(views.sportradarSoccer.sportradarMapping), name="sportradarMapping"),
    path("football/sportrader/sportradarSoccerEloRating", csrf_exempt(views.sportradarSoccer.sportradarSoccerEloRating), name="sportradarSoccerEloRating"),
    path("football/sportrader/SaveSoccerEloRating", csrf_exempt(views.sportradarSoccer.SaveSoccerEloRating), name="SaveSoccerEloRating"),

    path("football/sportrader/SportsRaderLiveScore", csrf_exempt(views.sportradarSoccer.SportsRaderLiveScore), name="SportsRaderLiveScore"),

    path("football/sportrader/SofaScoreLiveScore", csrf_exempt(views.sportradarSoccer.SofaScoreLiveScore), name="SofaScoreLiveScore"),
    
    #Tennis API
    path("football/sportrader/sportradarAPI", csrf_exempt(views.sportradarTenis.sportradarAPI), name="UpcomingMatch"),
    path("football/sportrader/CompetitorAI", csrf_exempt(views.sportradarTenis.CompetitorAI), name="CompetitorAI"),
    path("football/sportrader/GetLiveSummeryTennis", csrf_exempt(views.sportradarTenis.GetLiveSummeryTennis), name="GetLiveSummeryTennis"),
    path("football/sportrader/GetHistroyData/<start_date>", csrf_exempt(views.sportradarTenis.GetHistroyData), name="GetHistroyData"),
    path("football/sportrader/EloratingCalculation", csrf_exempt(views.sportradarTenis.EloratingCalculation), name="EloratingCalculation"),
    path("football/sportrader/EloratingView", csrf_exempt(views.sportradarTenis.EloratingView), name="EloratingView"),
    path('TennisComoitation',csrf_exempt(views.bitfair.TennisComoitation), name='TennisComoitation'),
    path('TennisEvent',csrf_exempt(views.bitfair.TennisEvent), name='TennisEvent'),
    path('TennisMarket',csrf_exempt(views.bitfair.TennisMarket), name='TennisMarket'),
    


]
