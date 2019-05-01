from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from flask import jsonify, abort, request, Flask

import os
import requests
import json

# Create your views here.
def index(request):
	return render(request, 'rec/index.html')

@csrf_exempt
def command(request):
	api_key = "" #insert Last.fm API key here
	param = request.POST.get("text", "")
	song_name = "null"

	base_url = "http://ws.audioscrobbler.com/2.0/?method=artist."

	similar_url = base_url + "getsimilar&artist=" + param + "&api_key=" + api_key + "&format=json"
	resp = requests.get(url = similar_url)
	data = resp.json()

	similar1_name = data['similarartists']['artist'][0]['name']
	similar2_name = data['similarartists']['artist'][1]['name']
	similar3_name = data['similarartists']['artist'][2]['name']

	tracks_url_1 = base_url + "gettoptracks&artist=" + similar1_name + "&api_key=" + api_key + "&format=json"
	resp1 = requests.get(url = tracks_url_1)
	data1 = resp1.json()
	track1_name = data1['toptracks']['track'][0]['name']
	track1_url = data1['toptracks']['track'][0]['url']

	tracks_url_2 = base_url + "gettoptracks&artist=" + similar2_name + "&api_key=" + api_key + "&format=json"
	resp2 = requests.get(url = tracks_url_2)
	data2 = resp2.json()
	track2_name = data2['toptracks']['track'][0]['name']
	track2_url = data2['toptracks']['track'][0]['url']

	tracks_url_3 = base_url + "gettoptracks&artist=" + similar3_name + "&api_key=" + api_key + "&format=json"
	resp3 = requests.get(url = tracks_url_3)
	data3 = resp3.json()
	track3_name = data3['toptracks']['track'][0]['name']
	track3_url = data3['toptracks']['track'][0]['url']


	message = "*Here are your recommendations!* \n 1. *" + similar1_name + "* \n　<" + track1_url + "|Check out *" + track1_name + "* here!> \n 2. *" + similar2_name + "* \n　<" + track2_url + "|Check out *" + track2_name + "* here!> \n 3. *" + similar3_name + "* \n　<" + track3_url + "|Check out *" + track3_name + "* here!>"

	return JsonResponse(
		{
			"response_type": "in_channel",
            "text": message
		}
	)