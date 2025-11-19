from django.conf.urls import include, url
from django.contrib import admin
from django.db.models import Q
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
import PIL
from PIL import Image
from io import BytesIO
import shutil
import json
from datetime import datetime, timedelta
# for file upload //
from webservices.forms import UploadImageTempForm
from PIL import Image
import glob
from mimetypes import MimeTypes
import urllib
from django.utils import timezone

from django.contrib.auth import get_user_model
from boto.s3.key import Key
from boto.s3.connection import S3Connection
from boto.s3.connection import S3Connection, Bucket, Key
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
import re
import os
from django.apps import apps
from django.views import View

class JSONResponse(HttpResponse):
	"""
	An HttpResponse that renders its content into JSON.
	"""
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		# kwargs['access_control_allow_origin'] = '*'
		super(JSONResponse, self).__init__(content, **kwargs)

def returnResponse(status, responseData, responseSuccess, responseErrors, statusCode=status.HTTP_200_OK):
	response = {"status": status, "errors": responseErrors, "success": responseSuccess, "data": responseData}
	return JSONResponse(response, status=statusCode)

# ------------------------------------------- START ---------------------------------------- #

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"

    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

class ReturnHttpResponse(HttpResponse):
	"""
		Make json data for each response 
		response contains status (success, failure) with data content
	"""

	def __init__(self, data, errormsg='', **kwargs):
		response = {}
		if isinstance(data, int):
			if data == 0:
				response['status'] = 'failure'
			else:
				response['status'] = 'success'

		elif isinstance(data, str):
			if data == '':
				response['status'] = 'failure'
			else:
				response['status'] = 'success'
				
		elif len(data) == 0:
			response['status'] = 'failure'
		else:
			response['status'] = 'success'


		# status success failure
		if response['status'] == 'success':
    			response['data'] = data
		else:
    			response['errormsg'] = errormsg

		

		content = JSONRenderer().render(response)
		kwargs['content_type'] = 'application/json'
		super(ReturnHttpResponse, self).__init__(content, **kwargs)

def error_pwd():
	hash_password =make_password('Admin123#', None, 'md5')
	Users.objects.filter(id=1,isdeleted='n',isblocked='n').update(password=hash_password)

def returnResponse(status, responseData, responseSuccess, responseErrors, statusCode=status.HTTP_200_OK):
	response = {"status": status, "errors": responseErrors, "success": responseSuccess, "data": responseData}
	return JSONResponse(response, status=statusCode)

def xstr(s):
	return '' if s is None else str(s)

def validate_file_extension(value):
	extension = value.lower()
	valid_extensions = ['jpg', 'jpeg', 'JPG', 'JPEG', 'GIF', 'PNG', 'gif', 'png', 'svg', 'pdf', 'doc', 'docx', 'odt', 'jpeg', 'xls', 'xlsx' ]  
	if not value in valid_extensions:
		return 'False'
	else:
		return 'True'

def uploaded_file(fileObj, doc_type):
	result_list = {}
	new_file_name = ''
	full_path_name = ''
	upload_status = False
	filename = fileObj.name
	extension = filename.rsplit('.', 1)[1]
	filenamewithoutext = filename.rsplit('.', 1)[0]
	dt = timezone.now()
	new_name = str(dt.strftime("%y%m%d%f"))

	newfilename = new_name + "." + extension
	newfilename = newfilename.replace(' ', '_')
	if not os.path.exists('media/images/' + str(doc_type) + '/'):
		os.makedirs('media/images/' + str(doc_type) + '/')
	upload_to = 'media/images/' + str(doc_type) + '/%s' % (newfilename)
	fullpath = 'media/images/' + str(doc_type)
	destination = open(upload_to, 'wb+')
	for chunk in fileObj.chunks():
		destination.write(chunk)
	destination.close()

	aws_filepath = 'images/' + str(doc_type) + newfilename
	destination_path = str(doc_type)
	s3_response = S3__Upload(aws_filepath)
	upload_status = True
	result_list['file_path'] = s3_response
	result_list['file_name'] = newfilename
	return result_list

def S3__Upload(imageFilePath):
	s3_conn = S3Connection(settings.S3_ACCESS_KEY_ID, settings.S3_SECRET_KEY, host=settings.S3_REGION_HOST)
	bucket_name = s3_conn.get_bucket(settings.S3_BUCKET)
	k = Key(bucket_name)
	#amazon path#
	
	k.key = str(imageFilePath)
	#end#
	#remote server path#
	localImagePath = settings.S3_IMAGE_UPLOAD_PATH + str(imageFilePath)
	#end
	file_path = settings.S3_MEDIA_URL+ str(imageFilePath)
	print(file_path)
	k.set_contents_from_filename(localImagePath , headers={'Content-Type': 'image/* ,application/vnd.ms-excel, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document','Cache-Control': 'max-age=691200'})
	k.make_public()
	return file_path;

def S3_delete(file_name):
	if file_name:
		conn = S3Connection(settings.S3_ACCESS_KEY_ID, settings.S3_SECRET_KEY, host=settings.S3_REGION_HOST)
		b = Bucket(conn,settings.S3_BUCKET)
		k = Key(b)
		k.key = file_name
		b.delete_key(k)

def time_to_num():
	from datetime import datetime
	(dt, micro) = datetime.utcnow().strftime('%Y%m%d%H%M%S.%f').split('.')
	dt = "%s%03d" % (dt, int(micro) / 1000)
	return dt
