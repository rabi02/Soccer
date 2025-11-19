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
import requests
import json
from db_table.models import *
from webservices.views.constants import *
import redis
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from webservices.serializers import *
import datetime
import re
from django.db.models import Q
from django.db.models import Count
from django.db.models import Sum

def GetTeamwiseProbability(team_id):
	team = Teams.objects.all().filter(team_id=team_id,collection_datasource="www.worldfootball.net").first()
	result = SeasonLeagueTeamInfo.objects.filter(team_id = team_id).values('team_id').order_by('team_id').annotate(total_match=Sum('t_mp')).annotate(total_win=Sum('t_w')).annotate(total_loss=Sum('t_l')).annotate(total_drow=Sum('t_d'))
	pd = result[0]['total_drow'] *100 /result[0]['total_match']
	pl = result[0]['total_loss'] *100/result[0]['total_match']
	pw = result[0]['total_win'] *100/result[0]['total_match']
	res ={}
	res['total_draw'] = result[0]['total_drow']
	res['total_match'] = result[0]['total_match']
	res['total_loss'] = result[0]['total_loss']
	res['total_win'] = result[0]['total_win']
	res['Pwin'] = "{:.2f}".format(pw)			#Win Probability
	res['Plost'] = "{:.2f}".format(pl)			#Lost Probability
	res['Pdraw'] = "{:.2f}".format(pd)			#Draw Probability
	res['team_name']= team.name
	
	return res