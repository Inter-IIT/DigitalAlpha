import asyncio
from django.shortcuts import render
from . import utils
import sys
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pymongo
from dotenv import load_dotenv
import datetime
import os
import json
from bson.objectid import ObjectId
from bson import BSON
from bson import json_util
load_dotenv()
MONGODB_URI = os.environ['MONGODB_URI']

client = pymongo.MongoClient(MONGODB_URI)

db1 = client['tech-meet']
db_only=db1['comp']
db= db1['info']

db_form = db1['form-data']


def parse_json(data):
    return json.loads(json_util.dumps(data))


def getAll(request):
    try:
        q = request.GET.get('q')
        if q.isdigit():
            data = db.find({'cik': int(q)})
        else:
            data = db.find({'$or': [
                {'ticker': {'$regex': f'^{q}'}},
                {'title': {'$regex': f'^{q}'}},
            ]})
        return JsonResponse(parse_json({'status': 'success', 'data': data}),status=200)
    except:
        return JsonResponse(parse_json({'status': 'fail'}),status=404)


def getStrict(request):
    try:
        q = request.GET.get('q')
        print(q)
        if q.isdigit():
            data = db.find_one({'cik': int(q)})
        else:
            data = db.find_one({'ticker': q})
        return JsonResponse(parse_json({'status': 'success', 'data': data}),status=200)
    except:
        return JsonResponse(parse_json({'status': 'fail'}),status=404)


def getBS(request):
    try:
        raw = json.loads(request.body)
        # print(raw['ticker'])
        # data=raw['data']
        db=list(db_form.find({'date': {"$gte": raw['date']}, 'cik': int(raw['cik'])},{'date':1,'data':1,'_id':0}))

        ans=[]

        for r in db:
            d=r['data']
            d['date']=r['date']
            year=r['date'].split('-')[0]
            d['year']=year
            ans.append(d)
        
        # data = db_form.find({'ticker': raw['ticker']})
        return JsonResponse(parse_json({'status': 'success', 'data': ans}),status=200)
    except:
        return JsonResponse(parse_json({'status': 'fail'}),status=404)

#request body of form
# {
#     "date":"2017-01-01",
#     "cik":796343 
# }

def getId(request, pk):
    try:
        data = db.find_one({"_id": ObjectId(pk)})

        return JsonResponse(parse_json({'status': 'success', 'data': data}),status=200)
    except:
        return JsonResponse(parse_json({'status': 'fail'}),status=404)

