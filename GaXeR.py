from sanic import Sanic
from sanic import json, text
#from sanic.response import file
from pymongo import MongoClient
from datetime import datetime
import hashlib
import time
from pprint import pprint
import logging

client = MongoClient('mongodb://root:mongo0928@localhost:27017')
db = client.gaxer
collection = db.user

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s [%(levelname)s] %(message)s', 
    datefmt='%Y-%m-%d %H:%M', 
    handlers=[logging.FileHandler('ServerLog.log', 'a', 'utf8')]
)

def tokencheck(token):
    if token:
        return True
    else:
        return False

app = Sanic('GaXeR')
@app.get('/test')
async def test(request):
    try:
        #https://gaxer.ddns.net/test
        #https://127.0.0.1/test
        logging.info(f'from {request.ip}/test\nHello World')
        return text('Hello World', status=200)
    except Exception as e:
        logging.warning(str(e))
        return text(str(e), status=200)

@app.post('/signup')
async def signup(request):
    try:
        #https://gaxer.ddns.net/signup
        #https://127.0.0.1/signup
        try:
            acc = request.json["acc"]
            ps = request.json["ps"]
        except Exception:
            return text('Argument Error', status=200)
        if (len(ps) != 64) or (len(acc) <= 0):
            return text('Argument Error', status=200)
        else:
            s = hashlib.sha256()
            s.update(acc.encode('utf-8'))
            tok = s.hexdigest()
            collection.insert_one(
                {
                    "account":f"{acc}", 
                    "profile":{
                        "pass":f"{ps}", 
                        "token":f"{tok}"
                    }
                }
            )
            logging.info(f'from {request.ip}/signup\naccount:{acc}\ntoken:{tok}')
            return text(tok, status=200)
    except Exception as e:
        logging.warning(str(e))
        return text(e)

@app.get('/upload')
async def update(request):
    try:
        #https://gaxer.ddns.net/upload\?tok=123456abcd&sw=True&battery=88&fire=170000&temp=31&gas=29.52&remaining=1950.3&safe=0000
        #https://127.0.0.1/upload\?tok=123456abcd&sw=True&battery=88&fire=170000&temp=31&gas=29.52&remaining=1950.3&safe=0010
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        struct_time = time.strptime(now, '%Y-%m-%d %H:%M:%S')
        tstamp = int(time.mktime(struct_time))
        tok = request.args.get("tok")
        battery = request.args.get("battery")
        fire = request.args.get("fire")
        temp = request.args.get("temp")
        gas = request.args.get("gas")
        remaining = request.args.get("remaining")
        safe = request.args.get("safe")
        #print(request.query_args)
        if (tok == None) or (battery == None) or (fire == None) or (temp == None) or (gas == None) or (remaining == None):
            return text('Argument Error', status=200)
        if tokencheck(list(collection.find({"profile.token":f"{tok}"}, {"profile.token":1, "_id":0}))) == False:
            return text('toekn invalid', status=200)
        else:
            collection.update_many(
                {"profile.token":f"{tok}"},
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
                        "gas1.battery":float(battery), 
                        "gas1.safe":str(safe)
                    }
                }, upsert=True
            )
            logging.info(f'from {request.ip}/upload\n{tok}\n{battery}\n{fire}\n{temp}\n{gas}\n{remaining}\n{safe}')
            return text('ok', status=200)
    except Exception as e:
        logging.warning(str(e))
        return text(str(e), status=200)

@app.get('/data')
async def single(request):
    try:
        #https://gaxer.ddns.net/data\?tok=123456abcd&record=3
        #https://127.0.0.1/data\?tok=123456abcd&record=3
        tok = request.args.get("tok")
        record = int(request.args.get("record"))
        if (tok == None) or (record == None):
            return text('Argument Error', status=200)
        if tokencheck(list(collection.find({"profile.token":f"{tok}"}, {"profile.token":1, "_id":0}))) == False:
            return text('toekn invalid', status=200)
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
            logging.info(f'from {request.ip}/data\n{tok}\n{record}')
            return json(result, status=200)
    except Exception as e:
        logging.warning(str(e))
        return text(str(e), status=200)

@app.get('/swstatus')
async def swstatus(request):
    #https://gaxer.ddns.net/swstatus\?tok=123456abcd
    try:
        tok = request.args.get("tok")
        if tok == None:
            return text('Argument Error', status=200)
        if tokencheck(list(collection.find({"profile.token":f"{tok}"}, {"profile.token":1, "_id":0}))) == False:
            return text('toekn invalid', status=200)
        else:
            result = list(collection.find({"profile.token":f"{tok}"}, {"gas1.uswitch":1, "_id":0}))
            sw = dict(result[0])
            sw_stat = sw['gas1']['uswitch']
            logging.info(f'from {request.ip}/swstatus\n{tok}\n{sw_stat}')
            return text(sw_stat, status=200)
    except Exception as e:
        logging.warning(str(e))
        return text(str(e), status=200)

@app.get('/swupdate')
async def swupdate(request):
    #https://gaxer.ddns.net/swupdate\?tok=123456abcd&sw=True
    #https://127.0.0.1/swupdate\?tok=123456abc&sw=True
    try:
        tok = request.args.get("tok")
        sw = request.args.get("sw")
        swCheck = ['True', 'False']
        if tok == None:
            return text('Argument Error', status=200)
        if tokencheck(list(collection.find({"profile.token":f"{tok}"}, {"profile.token":1, "_id":0}))) == False:
            return text('toekn invalid', status=200)
        elif sw not in swCheck:
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
            logging.info(f'from {request.ip}/swupdate\n{tok}\n{sw}')
            return text('ok', status=200)
    except Exception as e:
        logging.warning(str(e))
        return text(str(e), status=200)

@app.get("/resident")
async def resident(request):
    #https://gaxer.ddns.net/resident\?tok=123456abcd
    try:
        tok = request.args.get("tok")
        if tok == None:
            return text('Argument Error', status=200)
        if tokencheck(list(collection.find({"profile.token":f"{tok}"}, {"profile.token":1, "_id":0}))) == False:
            return text('toekn invalid', status=200)
        else:
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
            logging.info(f'from{request.ip}/resdient\n{tok}\n{battery_gas_info}')
            return json(battery_gas_info, status=200)
    except Exception as e:
        logging.warning(str(e))
        print(e)

@app.get("/safestatus")
async def safestatus(request):
    #https://gaxer.ddns.net/safestatus\?tok=123456abcd
    try:
        tok = request.args.get("tok")
        if tok == None:
            return text('Argument Error', status=200)
        if tokencheck(list(collection.find({"profile.token":f"{tok}"}, {"profile.token":1, "_id":0}))) == False:
            return text('toekn invalid', status=200)
        else:
            result = list(collection.find({"profile.token":f"{tok}"}, {"gas1.safe":1, "_id":0}))
            safe = result[0]
            safestat = safe['gas1']['safe']
            logging.info(f'from{request.ip}/safestatus\n{tok}\n{safestat}')
            return text(safestat, status=200)
    except Exception as e:
        logging.warning(str(e))
        return text(str(e), status=200)

'''if __name__ == '__main__':
    
    ssl = {
        "cert":"gaxer_ddns_net.pem-chain", 
        "key":"key.pem"
    }
    app.run(host='0.0.0.0', port='443', debug=True, access_log=True, ssl = ssl)'''
