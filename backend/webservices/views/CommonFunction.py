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
# from .Common_function import *
import PIL
from PIL import Image
from io import BytesIO
import shutil
import json
from datetime import datetime, timedelta
# for file upload //
# from webservices.forms import UploadImageTempForm
from PIL import Image
import glob
from mimetypes import MimeTypes
import urllib
from django.utils import timezone

from django.contrib.auth import get_user_model
# from boto.s3.key import Key
# from boto.s3.connection import S3Connection
# from boto.s3.connection import S3Connection, Bucket, Key
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
import re
import os
from django.apps import apps
from django.views import View
from django.http import HttpResponse
from db_table.models import Users
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from betfair import settings
import re
from webservices.serializers import *
from webservices.views.constants import *
import csv
# For MailGun Mail Fire

class JSONResponse(HttpResponse):
	"""
	An HttpResponse that renders its content into JSON.
	"""
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		# kwargs['access_control_allow_origin'] = '*'
		super(JSONResponse, self).__init__(content, **kwargs)

# class AssetsImages(View):

# 	def post(self, request, format=None):

# 		responseErrors 	= []
# 		responseSuccess = []
# 		responseData 	= {}
# 		data 			= {}
# 		user 			= request.user
# 		filename 		= ''
# 		Image_detail 	= []
# 		form = UploadImageTempForm(request.POST, request.FILES)
		
# 		if form.is_valid():
# 			ipAddress = request.META['REMOTE_ADDR']
# 			# referance_no = form.cleaned_data['referance_no']
# 			for eachFile in form.cleaned_data['images']:
# 				extension = eachFile.name.rsplit('.', 1)[1]
# 				im = Image.open(eachFile)
# 				validator = validate_file_extension(extension.lower())
# 				if validator == 'True':
# 					filenameObj = uploaded_file(eachFile,'asset/')
# 					newname 	= filenameObj['file_name']
# 					print(filenameObj)
# 					#created_file_name = newname
# 					if filenameObj:
# 						Image_detail.append({'isdefault':False,'file':filenameObj['file_path'],'file_name':str(newname)})
						
# 						asset = Assets.objects.create(
# 							imageurl 	= filenameObj['file_path']         ,
# 							image_name 	= newname,
# 							date  		= time_to_num(),
# 						)
# 						last_inserted_id=asset.id
# 						data = {
# 							'status':'UPLOADED',
# 							'message': 'ok',
# 							'id':last_inserted_id,
# 						}
# 						responseData['uploads'] = data

# 			return returnResponse(True, responseData, responseSuccess, responseErrors)
# 		else:
# 			return returnResponse(False, responseData, responseSuccess, responseErrors)
# 	def get(self, request, id,timeout=60,format=None):
# 		response = 0
# 		error_msg = ''
# 		responseErrors 	= []
# 		responseSuccess = []
# 		responseData 	= {}
# 		asset_id = id
# 		#timeout = requestdata['timeout'] if 'timeout' in requestdata else 60
# 		if asset_id:
# 			result = Assets.objects.filter(pk =asset_id).values()
# 			responseData['data'] = result
# 			return returnResponse(True, responseData, responseSuccess, responseErrors)
# 		else:
# 			return returnResponse(False, responseData, responseSuccess, responseErrors)
# 	def patch(self, request,format=None):
# 		""" patch request """
# 		responseErrors 	= []
# 		responseSuccess = []
# 		responseData 	= {}
# 		requestdata = JSONParser().parse(request)
# 		response = 0
# 		error_msg = ''
# 		id = requestdata['id'] if 'id' in requestdata else ''
# 		status = requestdata['status'] if 'status' in requestdata else 'active'
# 		if id:
# 			update_val = Assets.objects.filter(pk =id).update(status=status)
# 			return returnResponse(True, responseData, responseSuccess, responseErrors)
# 		else:
# 			return returnResponse(False, responseData, responseSuccess, responseErrors)

# class AssetsList(View):
# 	def get(self, request,format=None):
# 		response = 0
# 		error_msg = ''
# 		responseErrors 	= []
# 		responseSuccess = []
# 		responseData 	= {}
# 		result = Assets.objects.all().values('id','date')
# 		responseData['data'] = result
# 		return returnResponse(True, responseData, responseSuccess, responseErrors)

def send_onboard_eamil(user_id):
	if Users.objects.filter(id=user_id).exists():
		user = Users.objects.get(id=user_id)
		to_email=user.email
		if user.is_verifed_email is False:
			token = Token.objects.get(user=user)
			url = "http://127.0.0.1:8000/" + "api/verify_email/" + str(token)
			subject = "Verify Email"
			body = "Hi,\n Please click below link to verify your email\n" + url
			send_mail(subject, body, settings.EMAIL_HOST_USER, [to_email])
		subject = "welcome Email"
		body = "Hi,\n"+ user.username+"\n"+"<h1>Welcome To The Bitfair</h1>\n"
		send_mail(subject, body, settings.EMAIL_HOST_USER, [to_email])
		return True


def password_validation(password):
	pattern = "^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$"
	result = re.findall(pattern, password)
	if result:
		return []
	else:
		return ["Should have minimum 8 characters.","Should have at least one number.","Should have at least one uppercase and one lowercase character.","Should have at least one special symbol."]


def get_leaves(item, key=None, key_prefix=""):
    """
    This function converts nested dictionary structure to flat
    """
    if isinstance(item, dict):
        leaves = {}
        """Iterates the dictionary and go to leaf node after that calls to get_leaves function recursively to go to leaves level"""
        for item_key in item.keys():
            """Some times leaves and parents or some other leaves might have same key that's why adding leave node key to distinguish"""
            temp_key_prefix = item_key if (key_prefix == "") else (key_prefix + "_" + str(item_key))
            leaves.update(get_leaves(item[item_key], item_key, temp_key_prefix))
        return leaves
    elif isinstance(item, list):
        leaves = {}
        elements = []
        """Iterates the list and go to leaf node after that if it is leave then simply add value to current key's list or
        calls to get_leaves function recursively to go to leaves level"""
        for element in item:
            if isinstance(element, dict) or isinstance(element, list):
                leaves.update(get_leaves(element, key, key_prefix))
            else:
                elements.append(element)
        if len(elements) > 0:
            leaves[key] = elements
        return leaves
    else:
        return {key_prefix: item}


def save_to_csv(response, file_path):
    data_rows = []
    for item in response:
        row = get_leaves(item)
        data_rows.append(row)

    output_to_csv = open(file_path, "w")

    header = []
    for key in data_rows[0].keys():
        header.append(key)
    
    dict_csv_writer = csv.DictWriter(output_to_csv, fieldnames=header)
    dict_csv_writer.writeheader()
    dict_csv_writer.writerows(data_rows)
    output_to_csv.close()


		
def send_verify_eamil(user_id):
    if Users.objects.filter(id=user_id).exists():
        user = Users.objects.get(id=user_id)
        to_email=user.email
        if user.is_verifed_email is False:
            token = Token.objects.get(user=user)
            url = SITEURL + "verify/" + str(token)
            subject = "Verify Email"
            body = "Hi,\n Please click below link to verify your email\n" + url
            send_mail(subject, body, settings.EMAIL_HOST_USER, [to_email])
        subject = "welcome Email"
        body = "Hi,\n"+ user.username+"\n"+"<h1>Welcome To The Soccer Street Bets</h1>\n"
        send_mail(subject, body, settings.EMAIL_HOST_USER, [to_email])
        return True




