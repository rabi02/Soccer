from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from db_table.models import *
import json
from webservices.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
# from soccer.testData import *

