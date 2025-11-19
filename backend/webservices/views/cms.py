from django.http import HttpResponse
from django.conf.urls import include, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from db_table.models import *
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.contrib.auth import get_user_model, login
from django.db.models import Q
import json
from django.http import JsonResponse

#import urllib.request
from django.views.decorators.cache import cache_page
from django.core.cache import cache
import random
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ParseError
import hashlib
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
# from webservices.views.Common_function import *
from datetime import datetime
from django.views import View
from django.views import generic
# from elasticsearch import Elasticsearch
# from elasticsearch import Elasticsearch,RequestsHttpConnection
from webservices.serializers import *

class CmsData(View):
    """ Cms view """

    def post(self, request):
        """ Post request """

        response = 0
        error_msg = ''
        request_data = JSONParser().parse(request)

        # generate slug from title and check slug already exists or not
        #slug = slugify(request_data['title'])
        cmsSelector = Blogs.objects.filter(slug=request_data['slug'])

        if cmsSelector.count() == 0:
            blog = Blogs.objects.create(
                                        title = request_data['title'],
                                        user_id = request_data['user_id'],
                                        slug = request_data['slug'],
                                        description = request_data['description'],
                                        meta_title = request_data['meta_title'],
                                        meta_key = request_data['meta_key'],
                                        meta_description = request_data['meta_description'],
                                        created_date = datetime.utcnow(),
                                        id=Blogs.objects.count() + 1
                                    )
            blog.save()
            last_inserted_id=blog.id
            response = 1
           
        else:
            error_msg = 'Slug already exists'


        return ReturnHttpResponse(response, error_msg)


class GetAllCms(View):
    """ Get all cms data """

    def get(self, request):
        """ Get request """

        response = {}
        error_msg = ''

        es = Elasticsearch()
        es = Elasticsearch([settings.ELASTIC_SEARCH_URL],connection_class=RequestsHttpConnection)
        res = es.search(index="blog_data", doc_type="blog", body= '', ignore=400)
        if res:
            response = res['blog_data']= res['hits']['hits']
        else:
            error_msg = 'No cms data found'

        return ReturnHttpResponse(response, error_msg)

class CmsDataView(APIView):
    def get(self,request,slug):
        try:
            cms_obj=Cms.objects.get(slug=slug)
            serializer = CmsSerializer(cms_obj)
            return Response({"code":200,"message":"success","data":serializer.data},status=200)
        except Cms.ObjectDoesNotExist:
            return Response({"code":404,"message":"Not Found"},status=404)

class BlogPublishedView(APIView):
    def get(self,request):
        try:
            blog_objs=Blogs.objects.filter(is_published=True)
            serializer = BlogsSerializer(blog_objs,many=True)
            return Response({"code":200,"message":"success","data":serializer.data},status=200)
        except Blogs.ObjectDoesNotExist:
            return Response({"code":404,"message":"Not Found"},status=404)

class GetSubscription(APIView):
    """ Get all cms data """
    def get(self, request):
        """ Get request """
        try:
            subsription=Subscriptions.objects.filter(is_active=True)
            serializer = SubscriptionSerializer(subsription,many=True)
            return Response({"code":200,"message":"success","data":serializer.data},status=200)
        except Cms.ObjectDoesNotExist:
            return Response({"code":404,"message":"Not Found"},status=404)


class SaveMessage(View):
    """ Cms view """

    def post(self, request):
        """ Post request """

        response = 0
        error_msg = ''
        request_data = JSONParser().parse(request)
        message = Message.objects.create(
                                    message = request_data['message'],
                                    receiver_id = request_data['receiver_id'],
                                    sender_id = request_data['sender_id'],
                                    message_type = request_data['message_type'],
                                    created_date = datetime.utcnow(),
                                    id=Message.objects.count() + 1
                                )
        message.save()
        
        return Response({"message":"success","data":''},status=200)

@csrf_exempt
def SaveMessage(request):
    request_data = JSONParser().parse(request)
    response = 0
    error_msg = ''
    # try:
    message = Message.objects.create(
        message = request_data['message'],
        receiver_id = request_data['receiver_id'],
        sender_id = request_data['sender_id'],
        message_type = request_data['message_type'],
        created_date = datetime.utcnow(),
        id=Message.objects.count() + 1

    )
    message.save()
    data = {"status": 200, "message": "success", "data":''}
    # except:
    #     data = {"status": 400, "message": "Data not found", "data":''}

    return JsonResponse(data)

@csrf_exempt
def GetMessage(request):
    request_data = JSONParser().parse(request)
    try:
        MessageSerializer_data = MessageSerializer(Message.objects.filter (\
                                                                           
                                                                            Q(\
                                                                                sender_id=request_data['sender_id'], \
                                                                                receiver_id=request_data['receiver_id'] \
                                                                            ) | \
                                                                            Q(
                                                                                sender_id=request_data['receiver_id'], \
                                                                                receiver_id=request_data['sender_id'] \
                                                                            )\
                                                                            
                                                                        ), many=True).data
        data = {"status": 200, "message": "success", "data":MessageSerializer_data}
    except:
        data = {"status": 400, "message": "Data not found", "data":''}

    return JsonResponse(data)

@csrf_exempt
def SubscriptionByid(request):
    request_data = JSONParser().parse(request)
    subsription=Subscriptions.objects.filter(id=request_data['id'])
    serializer = SubscriptionSerializer(subsription,many=True)
    data = {"status": 200, "message": "success", "data":serializer.data}
    return JsonResponse(data)

@csrf_exempt
def StorePayment(request):
    request_data = JSONParser().parse(request)
    print(request_data)
    subsrption = UserSubscriptionPayment.objects.create(
        subscription_id = request_data['subscription_id'],
        user_id =  request_data['user_id'],
        username = request_data['username'],
        transaction_id = request_data['detail']['id'],
        payment_status = request_data['detail']['status'],
        currency_code = request_data['detail']['purchase_units'][0]['amount']['currency_code'],
        amount = request_data['detail']['purchase_units'][0]['amount']['value'],
        payee_email = request_data['detail']['purchase_units'][0]['payee']['email_address'],
        merchant_id= request_data['detail']['purchase_units'][0]['payee']['merchant_id'],
        shipping_name = request_data['detail']['purchase_units'][0]['shipping']['name']['full_name'],
        shipping_address=json.dumps(request_data['detail']['purchase_units'][0]['shipping']['address']),
        payment_capture_id= request_data['detail']['purchase_units'][0]['payments']['captures'][0]['id'],
        payer_email = request_data['detail']['payer']['email_address'],
        payer_id = request_data['detail']['payer']['payer_id'],
        shiping_status = request_data['detail']['purchase_units'][0]['payments']['captures'][0]['seller_protection']['status'],
        date_of_payment = request_data['detail']['purchase_units'][0]['payments']['captures'][0]['update_time'],
        dump_response = json.dumps(request_data['detail']),
        id=UserSubscriptionPayment.objects.count() + 1
    )
    #  
    data = {"status": 200, "message": "success", "data":''}
    return JsonResponse(data)