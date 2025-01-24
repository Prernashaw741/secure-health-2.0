from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from django.db import IntegrityError


class loginView(APIView):
    def post(self,request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if(username != None) and (password != None):
            try:
                db = User.objects.get(username = username, password = password)
                response = Response({
                    "status" : 200
                },status=200)
                response.set_cookie(key="uid",value=db.pk)
                return response
            except User.DoesNotExist:
                return Response(status = 404)

        else:
            return Response(data = {
                "status" : 400,
                "message" : "Invalid Credentials"
            }, status = 400)


class RegisterView(APIView):
    def post(self, request):
        first_name = request.data.get('first_name', None)
        last_name = request.data.get('last_name', None)
        username = request.data.get('username', None)
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        if None in [first_name, last_name, username, email, password]:
            return Response(status = 400)
        else:
            try:
                db = User.objects.create(first_name = first_name, last_name = last_name, username = username, email = email, password = password)
                return Response(status=200)
            except IntegrityError as e:
                return Response(data = {
                    "status" : "Already Exists"
                }, status = 400)

class ForgotPasswordView(APIView):
    def post(self, request):
        username = request.data.get('username', None)
        new_password = request.data.get('password', None)
        email = request.data.get('email', None)
        if username and email and not new_password:
            try:
                db = User.objects.get(username = username, email = email)
                return Response(data = {
                    'message' : 'User Verified'
                }, status = 200)
            except User.DoesNotExist:
                return Response(data = {
                    'message' : 'User Not Found'
                }, status = 404)
        elif username and email and new_password:
            try:
                db = User.objects.get(username = username, email = email)
                db.password = new_password
                db.save()
                return Response(data = {
                    'message' : 'Password Changed'
                }, status = 200)
            except User.DoesNotExist:
                return Response(data = {
                    'message' : 'User Not Found'
                }, status = 404)
        else:
            return Response({'error' : 'Invalid Input'},status = 400)