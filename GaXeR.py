import re
from unittest import result
from sanic import Sanic
from sanic import json, text
#from sanic.response import file
from pymongo import MongoClient
import time
from datetime import datetime

client = MongoClient('mongodb://root:mongo0928@localhost:27017')
db = client.gaxer
collection = db.user

app = Sanic('GaXeR')
@app.get('/test')
async def test(request):
    try:
        #https://gaxer.ddns.net/test
        print('from {}'.format(request.ip))
        return text('Hello World', status=200)
    except Exception as e:
        print(e)
        
@app.get('/upload')
async def update(request):
    try:
        '''print(request.args)
        print(request.args.get("hum"))
        print(request.args.getlist("hum"))'''
        #https://gaxer.ddns.net/upload\?acc=test01&sw=True&battery=88&fire=170000&temp=31&gas=29.52&remaining=1950.3
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        struct_time = time.strptime(now, '%Y-%m-%d %H:%M:%S')
        tstamp = int(time.mktime(struct_time))
        account = request.args.get("acc")
        sw = request.args.get("sw")
        battery = request.args.get("battery")
        fire = request.args.get("fire")
        temp = request.args.get("temp")
        gas = request.args.get("gas")
        remaining = request.args.get("remaining")
        print(request.query_args)
        if (account == None) or (sw == None) or (battery == None) or (fire == None) or (temp == None) or (gas == None) or (remaining == None):
            return text('Argument Error', status=200)
        else:
            collection.update_many(
                {"account":f"{account}"},
                {
                    "$push":{
                        "gas1.data":{
                            "time":tstamp,
                            "fire":float(fire), 
                            "temp":float(temp),
                            "gas":float(gas),
                            "remaining":float(remaining)
                            }
                    },
                    "$set":{
                        "gas1.uswitch":f"{sw}", 
                        "gas1.battery":int(battery)
                    }
                }, upsert=True
            )
            return text('ok', status=200)
    except Exception as e:
        print(e)
        return text('Argument Error', status=200)

@app.get('/single')
async def single(request):
    try:
        #https://gaxer.ddns.net/single\?tok=123456abcd
        tok = request.args.get("tok")

        if tok == None:
            return text('Argument Error', status=200)
        else:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            struct_time = time.strptime(now, '%Y-%m-%d %H:%M:%S')
            tstamp = int(time.mktime(struct_time))
            result = list(collection.aggregate([
                {"$match":{
                    "profile.token":f"{tok}"}
                },
                {"$unwind":"$gas1.data"},
                {"$match":{
                    "gas1.data.time":{"$lt":tstamp}}
                },
                {"$sort":{"gas1.data.time":-1}},
                {"$project":{
                    "gas1.data":1, "_id":0}
                },
                {"$limit":1}
            ]))
            #print(result)
            return json(result, status=200)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    ssl = {
        "cert":".\gaxer_ddns_net.pem-chain", 
        "key":".\key.pem"
    }
    app.run(host='0.0.0.0', port='1234', debug=False, access_log=True, ssl=ssl)