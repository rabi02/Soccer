from django.conf.urls import include, url
from django.contrib import admin
from django.db.models import Q
from django.http import JsonResponse
from db_table.models import *
from django.http import Http404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from webservices.serializers import *
from rest_framework.views import APIView
from django.views import View
from rest_framework.response import Response
from rest_framework import status
from rest_framework import pagination
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
import os
import socket
import urllib.request
from django.contrib.auth import get_user_model
from .Common_function import *
import PIL
from PIL import Image
import cloudinary
import cloudinary.uploader
import cloudinary.api
import shutil
import json
from datetime import datetime, timedelta
# for file upload //
from webservices.forms import UploadImageTempForm
from PIL import Image
import glob
from mimetypes import MimeTypes
from django.utils import timezone
from django.contrib.auth import get_user_model
from boto.s3.key import Key
from boto.s3.connection import S3Connection
from boto.s3.connection import S3Connection, Bucket, Key
from django.db.models import Sum
from pyparsing import anyOpenTag, anyCloseTag
from xml.sax.saxutils import unescape as unescape
from importlib import reload
from django.views.decorators.csrf import csrf_exempt
from django.core.mail.message import EmailMessage
from django.utils.text import slugify
import re
import os
from django.apps import apps
# For MailGun Mail Fire
import smtplib
from email.mime.text import MIMEText
from elasticsearch import Elasticsearch,RequestsHttpConnection
from decimal import *
from webservices.views.CommonFunction import *
from django.views.generic import View

def SaveElasticMatch(match_id,matchArr):
	""" Save ad data to Elastic Search """	
	from datetime import datetime
	from elasticsearch import Elasticsearch
	es = Elasticsearch(settings.ELASTIC_SEARCH_URL)
	matchArr.objectID: base64.b64encode(bytes(str(match_id), "utf-8")).decode("utf-8"),
	res = es.index(index="MatchDetail", doc_type='match', id=match_id, body=json.dumps(matchArr))
	return 1

