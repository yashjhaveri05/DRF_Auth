from django.shortcuts import render
from django.contrib import auth
from rest_framework import generics, status, mixins, permissions
from rest_framework.response import Response
from api.serializers import UserSerializer,RegisterSerializer,FavouriteSerializer
from django.contrib.auth.models import User
from .models import Favourite
from django.http import JsonResponse
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from django.contrib.auth import login, logout
#from rest_framework.decorators import (api_view,permission_classes,authentication_classes)
#from rest_framework.permissions import IsAuthenticatedOrReadOnly

class UserCreate(APIView):
    def post(self, request, format='json'):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def signin(request):
    if request.method == "POST":
        try:
            email = request.data.get("email")
            password = request.data.get("password")

            email_db = User.objects.filter(email=email)
            if not email_db:
                data = {
                    "user_id": "not registered",
                    "login_type": "signup"
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                for user in email_db:
                    userid = user.pk
                    if user.check_password(password):
                        token, _ = Token.objects.get_or_create(user=user)
                        login(request, user)
                        data = {
                            "user_id": userid,
                            "login_type": "signin",
                            "message": " login successful",
                            "Token": token.key,
                        }
                        return Response(data, status=status.HTTP_200_OK)
                    else:
                        data = {
                            "user_id": "",
                            "login_type": "signin",
                            "message": " login unsuccessful "
                        }
                        return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return JsonResponse(
                data={"Message": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    else:
        return JsonResponse(
            data={"Message": "Only POST request allowed"},
            status=status.HTTP_400_BAD_REQUEST,
        )

class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response("Logout Successful",status=status.HTTP_200_OK)

@api_view(['GET'])
def UserDetails(request,pk):
    if request.method == 'GET':
        favourites = Favourite.objects.filter(user=pk)
        if favourites:
            serializer = FavouriteSerializer(favourites, many=True)
            return Response(serializer.data)
        else:
            return Response("No Favourites Added")

@api_view(['POST'])
def FavouriteAdd(request,pk):
    if request.method == 'POST':
        user = User.objects.get(id=pk)
        favourites = request.data.get("favourites")
        favourite = Favourite.objects.create(user=user,favourites=favourites)
        serializer = FavouriteSerializer(favourite, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def FavouriteDelete(request,pk):
    try:
        user = User.objects.get(id=pk)
        favourites = request.data.get("favourites")
        favourite = Favourite.objects.get(user=user,favourites=favourites)
    except Favourite.DoesNotExist:
        return Response("Not Found",status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        favourite.delete()
        return Response("Favourite Deleted", status=status.HTTP_400_BAD_REQUEST)
