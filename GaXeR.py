from sanic import Sanic
from sanic import json, text
#from sanic.response import file
from pymongo import MongoClient
import time
from datetime import datetime
from pprint import pprint

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
        #https://gaxer.ddns.net/upload\?acc=test01&sw=True&battery=88&fire=170000&temp=31&gas=29.52&remaining=1950.3
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        struct_time = time.strptime(now, '%Y-%m-%d %H:%M:%S')
        tstamp = int(time.mktime(struct_time))
        account = request.args.get("acc")
        battery = request.args.get("battery")
        fire = request.args.get("fire")
        temp = request.args.get("temp")
        gas = request.args.get("gas")
        remaining = request.args.get("remaining")
        print(request.query_args)
        if (account == None) or (battery == None) or (fire == None) or (temp == None) or (gas == None) or (remaining == None):
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
                        "gas1.battery":int(battery)
                    }
                }, upsert=True
            )
            return text('ok', status=200)
    except Exception as e:
        print(e)
        return text('Argument Error', status=200)

@app.get('/data')
async def single(request):
    try:
        #https://gaxer.ddns.net/data\?tok=123456abcd&record=3
        tok = request.args.get("tok")
        record = int(request.args.get("record"))
        if (tok == None) or (record == None):
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
                {"$limit":record}
            ]))
            return json(result, status=200)
    except Exception as e:
        print(e)

@app.get('/swstatus')
async def swstatus(request):
    #https://gaxer.ddns.net/swstatus\?tok=123456abcd
    try:
        tok = request.args.get("tok")
        if tok == None:
            return text('Argument Error', status=200)
        else:
            result = list(collection.find({"profile.token":f"{tok}"}, {"gas1.uswitch":1, "_id":0}))
            sw = dict(result[0])
        return text(sw['gas1']['uswitch'], status=200)
    except Exception as e:
        print(e)

@app.get('/swupdate')
async def swupdate(request):
    #https://gaxer.ddns.net/swupdate\?tok=123456abcd&sw=True
    try:
        tok = request.args.get("tok")
        sw = request.args.get("sw")
        if tok == None:
            return text('Argument Error', status=200)
        else:
            collection.update_one(
                {"profile.token":f"{tok}"}, 
                {
                    "$set":{
                        "gas1.uswitch":f"{sw}"
                    }
                }, upsert=True
            )
        return text('ok', status=200)
    except Exception as e:
        print(e)

@app.get("/resident")
async def resident(request):
    #https://gaxer.ddns.net/resident\?tok=123456abcd
    try:
        tok = request.args.get("tok")
        if tok == None:
            return text('Argument Error', status=200)
        battery_gas_info = {'battery':0, 'gas':0, 'temp':0}
        result = list(collection.find({"profile.token":f"{tok}"}, {"gas1.battery":1, "_id":0}))
        battery_gas_info["battery"] = result[0]['gas1']['battery']
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
                "gas1.data.gas":1, "gas1.data.temp":1, "_id":0}
                }, 
            {"$limit":1}
            ])
            )
        battery_gas_info["gas"] = result[0]['gas1']['data']['gas']
        battery_gas_info["temp"] = result[0]['gas1']['data']['temp']
        return json(battery_gas_info)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    
    ssl = {
        "cert":"gaxer_ddns_net.pem-chain", 
        "key":"key.pem"
    }
    
   #app.run(host='0.0.0.0', port='443', debug=False, access_log=True)#ssl = ssl
