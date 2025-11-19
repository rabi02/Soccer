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
from webservices.serializers import *
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
from django.views import View
from django.views import generic
from rest_framework import generics, status, views, permissions
from webservices.views.CommonFunction import *
from webservices.views.constants import *
# from rest_framework.generics import ListAPIView, CreateAPIView
# class CreateUser(APIView):
#     """ Insert message details """

#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             user = Users.objects.get(email=serializer.data["email"], username=serializer.data['username'])
#             token, auth = Token.objects.get_or_create(user=user)
#             mail_sent = send_onboard_eamil(user.id)
#             data = {
#                 'user_id': user.id,
#                 'token': token.key,
#                 'first_name': serializer.data["first_name"],
#                 'last_name': serializer.data["last_name"],
#                 'email': serializer.data["email"],
#                 "msg": "sent mail link"
#             }
#             return Response({"status": 201, "message": "User Registration success", "data": data}, status=201)
#         else:
#             return Response({"status": 400, "message": "Invalid input", "data": {}}, status=400)

class CreateUser(View):
    """ Insert message details """

    def post(self, request):
        print(request)
        requestdata = JSONParser().parse(request)
        print(requestdata)
        user_id = requestdata['user_id']
        first_name = requestdata['first_name']
        last_name = requestdata['last_name']
        username = requestdata['username']
        email = requestdata['email']
        #phone = requestdata['phone']
        password = make_password(requestdata['password'])
        cnt1 = Users.objects.filter(username=username).count()
        if cnt1 > 0 and user_id == '':
            data = {
                'status': 0,
                'message': 'Username already exist',
            }
            return JsonResponse(data)

        cnt = Users.objects.filter(email=email).count()
        if cnt > 0 and user_id == '':
            data = {
                'status': 0,
                'message': 'Email Id already exist',
            }
            return JsonResponse(data)
        else:
            user = Users.objects.create(
                                        email=email,
                                        first_name=first_name,
                                        last_name=last_name,
                                        username=username,
                                        password=password,
                                    )
            
            user = Users.objects.get(email=email)
            user_id = user.id
            token = Token.objects.get_or_create(user=user)
            auth = Token.objects.get(user_id=user_id)
            user_id = user.id
            first_name = user.first_name
            last_name = user.last_name

        data = {
            'status': 1,
            'user_id': user_id,
            'token': auth.key,
            'first_name': first_name,
            'last_name': last_name,
        }
        mail_sent = send_verify_eamil(user_id)
        return JsonResponse(data)


class VerifyEmail(APIView):
    def get(self, request, token=None):
        try:
            print(token)
            token_obj = Token.objects.get(key=token)
            user_obj = Users.objects.get(id=token_obj.user_id)
            if user_obj.is_verifed_email is True:
                return Response({"status_code": 400, "message": "token invalid!", "data": []}, status=200)
            user_obj.is_verifed_email = True
            user_obj.save()
            data = {"username": user_obj.username}
            return Response({"status_code": 200, "message": "Successfully email verified", "data": data}, status=200)
        except Token.DoesNotExist:
            return Response({"status_code": 400, "message": "Invalid Token", "data": []}, status=200)
        except Users.DoesNotExist:
            return Response({"status_code": 400, "message": "User Doesn't Exists", "data": []}, status=200)

class GetUserProfileData(View):
    """ Get user profile data """

    def post(self, request):
        """ Post request """

        request_data = JSONParser().parse(request)
        response = {}
        error_msg = ''
        user_id = request_data['user_id']
        querySelector = Users.objects
        querySelector = querySelector.filter(id=user_id)

        if querySelector.count() == 1:
            # get user details
            response = UserSerializer(querySelector, many=True).data
        else:
            error_msg = 'User is not found'
            data = {'status': 400, 'message': 'User is not found', "data": []}
        data = {'status': 200, 'message': 'User is not foundsuccess', "data": response}
        return JsonResponse(data)


@csrf_exempt
def getuser(request):
    requestdata = JSONParser().parse(request)
    user_id = requestdata['user_id']
    User = Users.objects.get(id=user_id)
    serializer = UserSerializer(User)
    is_company = 0
    cnt = 0
    company_data = {}
    if User.company_id != '':
        company_id = User.company_id
        cnt = Companies.objects.filter(id=company_id).count()

    if cnt > 0:
        is_company = 1
        company = Companies.objects.get(id=company_id)
        company_serializer = CompanySerializer(company)
        company_data = company_serializer.data

    data = {
        'status': 1,
        'userdata': serializer.data,
        'is_company': is_company,
        'company_data': company_data,
    }
    return JsonResponse(data)


class UserLogin(View):
    def post(self, request):
        requestdata = JSONParser().parse(request)
        user_mail = requestdata['email']
        user_passw = requestdata['password']
        cnt = Users.objects.filter(email=user_mail).count()
        if cnt != 0:
            User = Users.objects.get(email=user_mail)

        else:
            data = {
                'status': 0,
                'message': 'Username / password mismatch.'
            }
            return JsonResponse(data)
        print(user_passw)
        password_check = User.check_password(user_passw)
        print(password_check)
        token = Token.objects.get_or_create(user=User)
        auth = Token.objects.get(user_id=User.id)
        Users.objects.filter(username=user_mail).update(last_login=datetime.now())
        if password_check == True:
            data = {
                'status': 1,
                'first_name': User.first_name,
                'last_name': User.last_name,
                'token': auth.key,
                'user_id': User.id,
                'username': User.username,
                'email': User.email,
            }
        else:
            data = {
                'status': 0,
                'message': 'Username / password mismatch.'
            }

        return JsonResponse(data)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if Users.objects.filter(email=email).exists():
            user = Users.objects.get(email=email)
            to_email = user.email
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            url = SITEURL+"resetpassword/" + uidb64 + "/" + str(token)
            subject = "Reset your passsword"
            body = "Hi,\n Use link below to reset your password\n" + url
            send_mail(subject, body, settings.EMAIL_HOST_USER, [to_email])
            data = {
                "status": 200,
                "message": 'We have sent you a link to reset your password',
                "data": []
            }
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response({"status": 400, "message": "Your mail is not registered with us", "data": []}, status=400)


class SetNewPasswordView(generics.GenericAPIView):
    """
        An endpoint for reset password.
    """
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64="0000", token=None):
        try:
            if "uidb64" in request.GET and request.GET["uidb64"] != "":
                uidb64 = request.GET["uidb64"]
            if "token" in request.GET and request.GET["token"] != "":
                token = request.GET["token"]
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = Users.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"status": 400, "message": "Invalid Token Please Request New One.", "data": []},
                                status=400)
            else:
                return Response({"status": 200, "message": "Token is valid", "data": []}, status=200)
        except:
            return Response({"status": 400, "message": "Invalid Token Please Request New One.", "data": []}, status=400)

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"status": 200, "message": "password reset success"}, status=200)


class UpdatePassword(APIView):
    """
    An endpoint for changing password.
    """
    # permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        requestdata = JSONParser().parse(request)
        old_password=requestdata['old_password']
        new_password=requestdata['new_password']
        user_id=requestdata['user_id']
        User = Users.objects.get(id=user_id)
        password_check = User.check_password(old_password)
        password=make_password(new_password)
       
        if password_check == True:
            Users.objects.filter(id=user_id).update(password=password)
            return Response({"status": 200, "message": "password updated successfully", "data": {}}, status=200)
        else:
            return Response({"status": 0, "message": "Old Password not match.", "data": {}})
    

class Profile(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        try:
            user = Users.objects.get(id=request.user.id)
            if "postal_code" in request.data:
                user.postal_code = request.data["postal_code"]
            if "address1" in request.data:
                user.address1 = request.data["address1"]
            if "address2" in request.data:
                user.address2 = request.data["address2"]
            if "city" in request.data:
                user.city = request.data["city"]
            if "country" in request.data:
                user.country = request.data["country"]
            if "mobile" in request.data:
                user.mobile = request.data["mobile"]
            if "photo" in request.data:
                user.photo = request.data["photo"]

            user.save()
            return Response(
                {"status": 200, "message": "profile updated successfully", "data": {"username": request.user.username}}, status=200
            )
        except Users.DoesNotExist:
            return Response({"status": 400, "message": "profile not updated.", "data": {}}, status=400)

    def get(self,request):
        user=Users.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response({"status": 200, "message": "profile updated successfully", "data": serializer.data}, status=200)

class EditProfile(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):

        try:
            
            user = Users.objects.get(id=request.data["id"])
            if "first_name" in request.data:
                user.first_name = request.data["first_name"]
            if "last_name" in request.data:
                user.last_name = request.data["last_name"]
            if "postal_code" in request.data:
                user.postal_code = request.data["postal_code"]
            if "address1" in request.data:
                user.address1 = request.data["address1"]
            if "address2" in request.data:
                user.address2 = request.data["address2"]
            if "city" in request.data:
                user.city = request.data["city"]
            if "country" in request.data:
                user.country = request.data["country"]
            if "mobile" in request.data:
                user.mobile = request.data["mobile"]

            user.save()
            return Response(
                {"status": 200, "message": "profile edited successfully", "data": request.data}, status=200
            )
        except Users.DoesNotExist:
            return Response({"status": 400, "message": "profile not edited.", "data": request.data}, status=400)

class Contactus(APIView):
    def post(self, request):
        serializer = ContactusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response({"status": 200, "message": "contactus successfully", "data": serializer.data}, status=200)

class UserNotification(APIView):
    # permission_classes = (IsAuthenticated,)

    def put(self, request):
        try:
            user = Users.objects.get(id=request.data["id"])
            if "email_notification" in request.data:
                user.email_notification = request.data["email_notification"]
            if "sms_notification" in request.data:
                user. sms_notification = request.data["sms_notification"]
            if "whatsapp_notification" in request.data:
                user. whatsapp_notification = request.data["whatsapp_notification"]
            if "phone_notification" in request.data:
                user.phone_notification = request.data["phone_notification"]
            if "site_notification" in request.data:
                user.site_notification = request.data["site_notification"]
            user.save()
            return Response(
                {"status": 200, "message": " UserNotification updated successfully", "data": request.data}, status=200
            )
        except Users.DoesNotExist:
            return Response({"status": 400, "message": "UserNotification not updated .", "data": request.data}, status=400)


class SubscriptionView(APIView):
    """
    An endpoint for Subscription.
    """
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        requestdata = JSONParser().parse(request)
        print(requestdata)
        subscription_id = requestdata['subscription_id']
        user_id = request.user.id
        mode_of_payment = requestdata['mode_of_payment']
        make_payment = requestdata['make_payment']
        date_of_payment = requestdata['date_of_payment']
        is_subscription = requestdata['is_subscription']
        is_payment = requestdata['is_payment']

        subscription = Subscription.objects.create(
            subscription_id=subscription_id,
            user_id_id=user_id,
            mode_of_payment=mode_of_payment,
            make_payment=make_payment,
            date_of_payment=date_of_payment,
            is_subscription=is_subscription,
            is_payment=is_payment,
        )
        data = {
            'status': 200,
            'subscription_id': subscription_id,
            'user_id': request.user.id,
            'mode_of_payment': mode_of_payment,
            'make_payment': make_payment,
            'date_of_payment': date_of_payment,
        }
        return JsonResponse(data)


class AffiliateusersView(APIView):
    """
    An endpoint for Affiliateusers.
    """

    def post(self, request):
        requestdata = JSONParser().parse(request)
        print("view",requestdata)

        name = requestdata.get('name',None)
        email = requestdata.get('email',None)
        phone = requestdata.get('phone',None)
        country = requestdata.get('country',None)
        password = requestdata.get('password',None)
        confirm_password = requestdata.get('confirm_password',None)

        if password!=confirm_password:
            raise serializers.ValidationError("passwords must be same")
        password = make_password(requestdata['password'])
        confirm_password = make_password(requestdata['confirm_password'])

        cnt1 = AffiliateUser.objects.filter(name=name).count()
        if cnt1 > 0 :
            raise serializers.ValidationError("name already exist")

        cnt = AffiliateUser.objects.filter(email=email).count()
        if cnt > 0 :
            raise serializers.ValidationError("email already exist")



        affiliateuser = AffiliateUser.objects.create(
            name=name,
            email=email,
            phone=phone,
            country=country,
            password=password,
            confirm_password=confirm_password,

        )

        data = {
            'status': 200,
            'name': name,
            'email':email,
            'phone': phone,
            'country': country,
        }
        return JsonResponse(data)

# class AffiliateusersView(APIView):
#     def post(self, request):
#         print(request.data)
#         serializer = AffiliateRegisterSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             print('valid')
#             serializer.save()
#             print("saved")
#             # data = {
#             #     'user_id': user.id,
#             #     'name': serializer.data["name"],
#             #     'email': serializer.data["email"],
#             #     'phone': serializer.data["phone"],
#             #     'country': serializer.data["country"],
#             #     # "msg": "sent mail link"
#             # }
#             return Response({"status": 201, "message": "AffiliateUser Registration success", "data": serializer.data}, status=201)
#         else:
#             return Response({"status": 400, "message": "Invalid input", "data": {}}, status=400)
#

# def users_count(request):
#     count = Users.objects.all.count()
#     return render(request,'admin/index.html',{
#         'count' : count
#     })
@csrf_exempt
def GetAffiliateList(request):
    
    affliate = AffiliateUser.objects.all().filter(is_active=True)
    serializer =AffiliateUserSerializer(affliate, many=True).data
    # return JsonResponse(serializer)
    return JsonResponse({"status": 200, "message": "success", "data": serializer}, status=200)