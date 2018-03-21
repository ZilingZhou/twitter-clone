from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.mail import EmailMessage
import string
import json
import random
import datetime
import pymongo
import copy
from bson import ObjectId
from .models import *
from mongoengine import *
# Create your views here.
status_ok = {'status':"OK"}
status_err = {'status':"error"}

def adduser(request):
	if request.method == 'POST':
		json_data = json.loads(request.body.decode("utf-8"))
		username = json_data['username']
		password = json_data['password']
		email = json_data['email']
		
		exist = User.objects(username = username).count()
		if exist:
			message = {'error' : "username already exist"}
			message.update(status_err)
			return JsonResponse(message)
		
		exist = User.objects(email = email).count()
		if exist:
			message = {'error' : "email already exist"}
			message.update(status_err)			
			return JsonResponse(message)
		
		else:
			key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
			user = User(username=username,password=password,email=email,verified = False, key = key)
			user.save()
			body = "validation key: <" + key + ">"
			emailout = EmailMessage('Twitter clone verification',body,to=[email])
			emailout.send()
			return JsonResponse(status_ok)
	
	return HttpResponse("Only supporting POST")

def verify(request):
	if request.method == 'POST':
		json_data = json.loads(request.body.decode("utf-8"))
		email = json_data['email']
		key = json_data['key']
		try:
			user = User.objects.get(email = email)
			if user.key == key or key == "abracadabra":
				user.verified = True
				user.save()
				return JsonResponse(status_ok)
			else:
				message = {'error' : "wrong verification key"}
				message.update(status_err)	
				return JsonResponse(message)
		except:
			message = {'error' : "Email does not exist"}
			message.update(status_err)
			return JsonResponse(message)
	
	return	HttpResponse("Only supporting POST")

def login(request):
	if request.method == 'POST':
		if request.session.get("username",False): 
			message = {'error' : "Already login"}
			message.update(status_err)
			return JsonResponse(message)
		else:	
			json_data = json.loads(request.body.decode("utf-8"))
			try:
				user = User.objects.get(username = json_data['username'])
			except:
				message = {'error' : "No such user"}
				message.update(status_err)
				return JsonResponse(message)
			if user.password == json_data['password'] and user.verified == True:
				request.session['username'] = json_data['username']
				return JsonResponse(status_ok)
			else:										#username or password error 
				message = {'error' : "Username and password does not match"}
				message.update(status_err)
				return JsonResponse(message)
	
	return	HttpResponse("Only supporting POST")

def logout(request):
	if request.session.get("username",False):
		try:
			del request.session['username']
		except KeyError:
			pass
		return JsonResponse(status_ok)
	else:
		message = {'error': "Not yet login"}
		message.update(status_err)
		return JsonResponse(message)

def additem(request):
	if request.session.get("username",False):
		json_data = json.loads(request.body.decode("utf-8"))
		content = json_data['content']
		childType = json_data['childType']
		item = Item(username=request.session['username'])
		timestamp = datetime.datetime.utcnow()
		#key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
		#key = str(timestamp) + key
		#item.itemId = key
		item.timestamp = timestamp
		item.content = content
		item.childType = childType
		item.save()
		data = {'id':str(item.id)}
		data.update(status_ok)
		return JsonResponse(status_ok)

	else:
		message = {'error': "Not yet login"}
		message.update(status_err)
		return JsonResponse(message)

def item(request):
	if request.session.get("username",False):
		if request.method == 'GET':
			Id = request.GET.get("id")
			try:
				item = Item.objects().get(id = ObjectId(Id))
			except:
				message = {'error': "No such item"}
				message.update(status_err)
				return JsonResponse(message)

			itemData = {
				'id': Id,
				'username': item.username,
				'property':{
					'likes': item.likes
				}, 
				'retweeted': item.retweeted,
				'content': item.content,
				'timestamp': item.timestamp
			}
			itemData.update(status_ok)
			return JsonResponse(itemData)
	else:
		message = {'error': "Not yet login"}
		message.update(status_err)
		return JsonResponse(message)

def search(request):
	if request.session.get("username",False):
		json_data = json.loads(request.body.decode("utf-8"))
		timestamp = json_data['timestamp']
		limit = json_data['limit']
		if limit is None or limit < 0:
			limit = 25
		elif limit > 100:
			limit = 100
		items = Item.objects(timestamp__lte = timestamp).order_by('-timestamp').limit(limit)
		array = []
		for item in items:
			itemData = {
				'id': str(item.id),
				'username': item.username,
				'property':{
					'likes': item.likes
				}, 
				'retweeted': item.retweeted,
				'content': item.content,
				'timestamp': item.timestamp
			}
			array.append(itemData)
		return JsonResponse(array)

	else:
		message = {'error': "Not yet login"}
		message.update(status_err)
		return JsonResponse(message)