from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.utils import IntegrityError
from .models import MyUser
from functools import wraps
import jwt
from django.contrib.auth.hashers import make_password,check_password
from jwt.exceptions import DecodeError,InvalidSignatureError,InvalidAlgorithmError,ExpiredSignatureError
from datetime import datetime, timedelta

# from jwt.exceptions.InvalidSignatureError import signature

import bcrypt 

# Create your views here.
def login_required(function):
    @ wraps(function)
    def wrap(req):
        if "Authorization" not in req.headers:
            return Response({"error":"Token required"},status=401)
        token=(req.headers["Authorization"].split(" ")[1])
        try:
            details=jwt.decode(token,"keys",algorithms="HS256")
        except ExpiredSignatureError:
            return Response({"message":"token exp"},status=400)
        except DecodeError:
            return Response({"message":"incorrct token"},status=400)
        except InvalidSignatureError:
            return Response({"message":"secrect not given"},status=400)
        except InvalidAlgorithmError:
            return Response({"message":"Algorithms error "},status=400)
        print(details)
        return function(req)
        
       
    return wrap


@api_view(["POST"])
def register(req):
    data=req.data
    try:
        hashed_password = make_password(data.get("password"))
        MyUser.objects.create(username=data.get("username"),password=hashed_password)
        return Response({"message":"data"},status=201)
    except IntegrityError:
        return Response({"message":"already exists"},status=400)
@api_view(["POST"])
def login(req):
    data=req.data
    isUser=MyUser.objects.filter(username=data["username"]).first()
    # print(check_password(data["password"],isUser.password))
    if isUser==None:
        return Response({"error":"user not found go to register"},status=404)
    if not check_password(data["password"],isUser.password):
        return Response({"message":"wrong password"},status=400)
    token=jwt.encode({"id":isUser.id,"exp":datetime.utcnow()+timedelta(minutes=3)},"keys","HS256")
    print(token)
    return Response({"message":"loggin done","token":token},status=200)

@api_view(["GET"])
@login_required
def greet(req):
    # print(req.he)
    return Response({"mess":"everything is correct"})
    # print()
print(".......................",greet.__name__)
@api_view(["POST"])
@login_required
def createtitle(req):
    data=req.data
    MyUser.objects.create(title=data.get("title"))
    # MyUser.objects.create(age=data.get("age"))
    return Response({"message":"title created by user"})
@api_view(["PUT"])
@login_required
def delete(req):
    data=req.data
    MyUser.objects.update()
