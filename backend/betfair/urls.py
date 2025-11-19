"""betfair URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from db_table import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/login/', admin.site.urls),
    
    path('admin/logout', views.logout_view, name='logout_view'),
    # path('admin/login', views.login, name='login'),
    path('admin/db_table/smp/', views.smp, name='smp_list'),
    path('admin/db_table/odds-manager/<int:home_team_id>/<int:away_team_id>', views.oddsManager, name='odds-manager'),
    path('admin/db_table/probability/<int:team_id>', views.probability, name='probability'),
    path('admin/db_table/playerdetail/<int:team_id>/<int:match_id>', views.playerdetail, name='playerdetail'),
    path('admin/db_table/singleplayerdetail/<int:player_id>', views.singleplayerdetail, name='singleplayerdetail'),
    path('admin/db_table/replymessage', views.replymessage, name='replymessage'),
    path('admin/db_table/GetScrapingData/', views.GetScrapingData, name='GetScrapingData'),
    path('admin/db_table/SaveScrapingData/', views.SaveScrapingData, name='SaveScrapingData'),
    path('admin/db_table/scraplist/', views.scraplist, name='scraplist'),
    path('admin/db_table/RunScrapingTool/<str:slug>', views.RunScrapingTool, name='RunScrapingTool'),
    path('admin/db_table/Creamlist/', views.Creamlist, name='Creamlist'),
    path('admin/db_table/ShowPlayerByTeamGraph/', views.ShowPlayerByTeamGraph, name='ShowPlayerByTeamGraph'),
    path('admin/db_table/ShowByTeamGraph/', views.ShowByTeamGraph, name='ShowByTeamGraph'),
    path('admin/db_table/OddsProbability/', views.OddsProbability, name='OddsProbability'),
    path('admin/db_table/AssianHandicap/', views.AssianHandicap, name='AssianHandicap'),
    path('admin/db_table/ViewMatchByDate/', views.ViewMatchByDate, name='ViewMatchByDate'),
    path('admin/db_table/ViewMatchByDate_rapid/', views.ViewMatchByDate_rapid, name='ViewMatchByDate_rapid'),
    path('api/',  include('webservices.urls'), name='api'),
    path('admin/db_table/matchDetail/<int:match_id>', views.matchDetail, name='matchDetail'),
    
    path('admin/', views.index),
    path('admin/db_table/HeadtoHeadView/<int:match_id>', views.HeadtoHeadView, name='HeadtoHeadView'),
    path('admin/db_table/HeadtoHeadView_rapid/<int:match_id>/<int:league_id>/<int:home_team>/<int:away_team>', views.HeadtoHeadView_rapid, name='HeadtoHeadView_rapid'),
    path('admin/db_table/prediction/<int:match_id>', views.prediction, name='prediction'),
    path('admin/db_table/tableData/<int:match_id>', views.tableData, name='tableData'),
    path('admin/db_table/OddsData/<int:match_id>', views.OddsData, name='OddsData'),
    path('admin/db_table/TeamList', views.TeamList, name='TeamList'),
    path('admin/db_table/LeagueList', views.LeagueList, name='LeagueList'),
    path('admin/db_table/LeagueAction', views.LeagueAction, name='LeagueAction'),
    
    path('admin/db_table/ViewTeamStatistics/<int:team_id>', views.ViewTeamStatistics, name='ViewTeamStatistics'),
    path('admin/db_table/FixtureList', views.FixtureList, name='FixtureList'),

    path('admin/db_table/UserList', views.UserList, name='UserList'),
    
    path('admin/db_table/UserDetail/<int:user_id>', views.UserDetail, name='UserDetail'),
    path('admin/db_table/NewsList', views.NewsList, name='NewsList'),
    path('admin/db_table/NewsDetail/<int:news_id>', views.NewsDetail, name='NewsDetail'),
    path('admin/db_table/addNews', views.addNews, name='addNews'),
    path('admin/db_table/EditNews/<int:news_id>', views.EditNews, name='EditNews'),
    path('admin/db_table/NewsAction', views.NewsAction, name='NewsAction'),
    
    path('admin/db_table/CmsList', views.CmsList, name='CmsList'),
    path('admin/db_table/addCms', views.addCms, name='addCms'),
    path('admin/db_table/EditCms/<int:cms_id>', views.EditCms, name='EditCms'),
    path('admin/db_table/CmsAction', views.CmsAction, name='CmsAction'),

    path('admin/db_table/AffiliateDetail/<int:user_id>', views.AffiliateDetail, name='AffiliateDetail'),
    path('admin/db_table/AffiliateList', views.AffiliateList, name='AffiliateList'),
    path('admin/db_table/addAffiliate', views.addAffiliate, name='addAffiliate'),
    path('admin/db_table/EditAffiliate/<int:user_id>', views.EditAffiliate, name='EditAffiliate'),
    path('admin/db_table/AffiliateAction', views.AffiliateAction, name='AffiliateAction'),


    path('admin/db_table/SubscriptionsDetail/<int:subscription_id>', views.SubscriptionsDetail, name='SubscriptionsDetail'),
    path('admin/db_table/SubscriptionList', views.SubscriptionList, name='SubscriptionList'),
    path('admin/db_table/addSubscriptions', views.addSubscriptions, name='addSubscriptions'),
    path('admin/db_table/EditSubscriptions/<int:subscription_id>', views.EditSubscriptions, name='EditSubscriptions'),
    path('admin/db_table/SubscriptionsAction', views.SubscriptionsAction, name='SubscriptionsAction'),

    path('admin/db_table/squardList', views.squardList, name='squardList'),
    path('admin/db_table/ViewSquardStatistics/<int:player_id>', views.ViewSquardStatistics, name='ViewSquardStatistics'),
    path('admin/db_table/PaymentList', views.PaymentList, name='PaymentList'),
    path('admin/db_table/PaymentDetail/<int:payment_id>', views.PaymentDetail, name='PaymentDetail'),
    
    path('admin/db_table/PredictionList', views.PredictionList, name='PredictionList'),
    path('admin/db_table/PredictionDetail/<int:match_id>', views.PredictionDetail, name='PredictionDetail'),
    
    path('admin/db_table/BannerList', views.BannerList, name='BannerList'),
    path('admin/db_table/addBanner', views.addBanner, name='addBanner'),
    path('admin/db_table/EditBanner/<str:slug>', views.EditBanner, name='EditBanner'),
    path('admin/db_table/BannerAction', views.BannerAction, name='BannerAction'),

    path('admin/db_table/NotificationList', views.NotificationList, name='NotificationList'),
    path('admin/db_table/NotificationAction', views.NotificationAction, name='NotificationAction'),
    path('admin/db_table/EditNotification/<str:slug>', views.EditNotification, name='EditNotification'),
    path('admin/db_table/addNotification', views.addNotification, name='addNotification'),
    path('admin/db_table/MessageList', views.MessageList, name='MessageList'),
    path('admin/db_table/chat/<int:sender_id>/<int:receiver_id>', views.chat, name='chat'),

    path('admin/db_table/CsvList', views.CsvList, name='CsvList'),
    path('admin/db_table/UploadCsv', views.UploadCsv, name='UploadCsv'),
    path('admin/db_table/EditCsv/<int:id>', views.EditCsv, name='EditCsv'),
    path('admin/db_table/PocessCSV/<int:id>', views.PocessCSV, name='PocessCSV'),

    path('admin/db_table/ExcelList', views.ExcelList, name='ExcelList'),
    path('admin/db_table/Uploadexcel', views.Uploadexcel, name='Uploadexcel'),
    path('admin/db_table/EditExcel/<int:id>', views.EditExcel, name='EditExcel'),
    
]

from rest_framework.authtoken import views

urlpatterns += [
	path('api-token-auth/', views.obtain_auth_token)
]

admin.site.site_header = "Soccerstreet bets Admin"
admin.site.site_title = "Soccerstreet bets Admin Portal"
admin.site.index_title = "Welcome to Soccerstreet bets Admin Portal"
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.IMAGE_URL, document_root=settings.IMAGE_ROOT)
