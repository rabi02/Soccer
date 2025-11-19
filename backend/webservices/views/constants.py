import json
from django.conf import settings
import redis
BetfairUsername='harding.darren4@gmail.com'
BetfairPassword='Galaxy2007()!'
BeatfairAuthenticationKey='NPnsvRDbdcM3gARaJG9Go0lnjJQtDhf84uUk5bUx1TM='
BeatfairApplicationKey= '87bDCv3LEKLoIsP7'

#Key by Client
# football_token = "7pHLrgSSyqiv52oBDeEtGHVs3UvSv9zJfuTaKFbaMWTazWzl1KK8OuTt9B5c"
#Key By Rabi
football_token = "gG0rbWIOwHbcKVz2pbZXHwlgYHPzb6HVpNVVoGPvZhdMmqCSWeoe9a4AHBSR"
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
redis_instance = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT, db=0)

SITEURL = 'https://aisportstrading.com'
BASEURL = 'https://aisportstrading.com:8000/'

AIURL ='https://aisportstrading.com:8002/'
# AIMODELURL ='https://aisportstrading.com:8004/'
AIMODELURL ='http://aisportstrading.com:8006/'
RAPIDAPI_HOST ='api-football-v1.p.rapidapi.com'
# RAPIDAPI_KEY ='ece33c90acmshe7a66df0ed99d01p1c7462jsnb1d8cfacb8fc'
RAPIDAPI_KEY ='2841468d88msh973d7b157ad27b7p183873jsnc5f315479eeb'
ELASTIC_SEARCH_URL = 'http://soccerfrontend.myvtd.site:9200/'
SPORTRADER_KEY ='rssdrah69y8wmwkm3s3k2njn'
# Triel Key Sportsradar
# SPORTRADER_API_KEY = 'u5yk3f8aj5gq2b2ufgkj2hvp'
# SPORTRADER_API_URL = 'https://api.sportradar.com/soccer/trial/v4'
# Production Key Sportsradar
SPORTRADER_API_KEY = '58a5hbhysexwsv3nw9r9kffz'
SPORTRADER_API_URL = 'https://api.sportradar.com/soccer/production/v4'