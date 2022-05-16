from sanic import Sanic
from sanic import json, text
#from sanic.response import file
from pymongo import MongoClient
from datetime import datetime
import hashlib
import time
import logging

client = MongoClient('mongodb://root:mongo0928@localhost:27017')
db = client.gaxer
collection = db.user

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s [%(levelname)s] %(message)s', 
    datefmt='%Y-%m-%d %H:%M', 
    handlers=[logging.FileHandler('ServerLog.log', 'w', 'utf8')]
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
            acc = request.form.get("acc")
            ps = request.form.get("ps")
        except Exception:
            return text('Argument Error', status=200)
        if (len(ps) != 64) or (len(acc) <= 0):
            return text('Argument Error', status=200)
        else:
            result = list(collection.find({"account":f"{acc}"}))
            if result:
                logging.info(f'from {request.ip}/signup\nalready use')
                return text('already use', status=200)
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

@app.post('/signin')
async def signin(request):
    try:
        acc = request.form.get("acc")
        ps = request.form.get("ps")
        result =  list(collection.find({"account":f"{acc}"}, {"_id":0, "account":1, "profile":1}))
        if result:
            usinfo = result[0]
            if usinfo['profile']['pass'] != ps:
                logging.info(f'from {request.ip}/signin\npass error')
                return text('pass error', status=200)
            else:
                tok = usinfo['profile']['token']
                logging.info(f'from {request.ip}/signin\nacc:{acc}\ntoken:{tok}')
                return text(tok, status=200)
        else:
            logging.info(f'from {request.ip}/signin\ninvalid user')
            return text('invalid user')
    except Exception as e:
        return text(e)

@app.get('/upload')
async def update(request):
    try:
        #https://gaxer.ddns.net/upload\?tok=123456abcd&sw=True&battery=88&fire=170000&temp=31&gas=29.52&remaining=1950.3&safe=0000&dev=gas1
        #https://127.0.0.1/upload\?tok=123456abcd&sw=True&battery=88&fire=170000&temp=31&gas=29.52&remaining=1950.3&safe=0010&dev=gas1
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
        dev = request.args.get("dev")
        #print(request.query_args)
        if (tok == None) or (battery == None) or (fire == None) or (temp == None) or (gas == None) or (remaining == None) or (dev == None):
            return text('Argument Error', status=200)
        if tokencheck(list(collection.find({"profile.token":f"{tok}"}, {"profile.token":1, "_id":0}))) == False:
            return text('toekn invalid', status=200)
        else:
            collection.update_many(
                {"profile.token":f"{tok}"},
                {
                    "$push":{
                        f"{dev}.data":{
                            "time":tstamp,
                            "fire":float(fire), 
                            "temp":float(temp),
                            "gas":float(gas),
                            "remaining":float(remaining)
                            }
                    },
                    "$set":{
                        f"{dev}.battery":float(battery), 
                        f"{dev}.safe":str(safe)
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
        #https://gaxer.ddns.net/data\?dev=gas1&tok=123456abcd&record=3&dev=gas1
        #https://127.0.0.1/data\?tok=123456abcd&record=3&dev=gas1
        tok = request.args.get("tok")
        record = int(request.args.get("record"))
        dev = request.args.get("dev")
        if (tok == None) or (record == None) or (dev == None):
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
                {"$unwind":f"${dev}.data"},
                {"$match":{
                    f"{dev}.data.time":{"$lt":tstamp}}
                },
                {"$sort":{f"{dev}.data.time":-1}},
                {"$project":{
                    f"{dev}.data":1, "_id":0}
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
    #https://gaxer.ddns.net/swstatus\?tok=123456abcd&dev=gas1
    #https://127.0.0.1/swstatus\?tok=123456abcd&dev=gas1
    try:
        tok = request.args.get("tok")
        dev = request.args.get("dev")
        if tok == None:
            return text('Argument Error', status=200)
        if tokencheck(list(collection.find({"profile.token":f"{tok}"}, {"profile.token":1, "_id":0}))) == False:
            return text('toekn invalid', status=200)
        else:
            result = list(collection.find({"profile.token":f"{tok}"}, {f"{dev}.uswitch":1, "_id":0}))
            sw = dict(result[0])
            sw_stat = sw[dev]['uswitch']
            logging.info(f'from {request.ip}/swstatus\n{tok}\n{sw_stat}')
            return text(sw_stat, status=200)
    except Exception as e:
        logging.warning(str(e))
        return text(str(e), status=200)

@app.get('/swupdate')
async def swupdate(request):
    #https://gaxer.ddns.net/swupdate\?tok=123456abcd&sw=True
    #https://127.0.0.1/swupdate\?tok=123456abc&sw=True&dev=gas1
    try:
        tok = request.args.get("tok")
        sw = request.args.get("sw")
        dev = request.args.get("dev")
        swCheck = ['True', 'False']
        if (tok == None) or (dev == None):
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
                        f"{dev}.uswitch":f"{sw}"
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
    #https://gaxer.ddns.net/resident\?dev=gas1&tok=123456abcd&dev=gas1
    #https://127.0.0.1/resident\?dev=gas1&tok=123456abcd&dev=gas1
    try:
        tok = request.args.get("tok")
        dev = request.args.get("dev")
        if (tok == None) or (dev == None):
            return text('Argument Error', status=200)
        if tokencheck(list(collection.find({"profile.token":f"{tok}"}, {"profile.token":1, "_id":0}))) == False:
            return text('toekn invalid', status=200)
        else:
            battery_gas_info = {'battery':0, 'gas':0, 'temp':0}
            result = list(collection.find({"profile.token":f"{tok}"}, {f"{dev}.battery":1, "_id":0}))
            battery_gas_info["battery"] = result[0][dev]['battery']
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            struct_time = time.strptime(now, '%Y-%m-%d %H:%M:%S')
            tstamp = int(time.mktime(struct_time))
            result = list(collection.aggregate([
                {"$match":{
                    "profile.token":f"{tok}"}
                    }, 
                {"$unwind":f"${dev}.data"},
                {"$match":{
                    f"{dev}.data.time":{"$lt":tstamp}}
                    }, 
                {"$sort":{f"{dev}.data.time":-1}},
                {"$project":{
                    f"{dev}.data.gas":1, f"{dev}.data.temp":1, "_id":0}
                    }, 
                {"$limit":1}
                ])
                )
            battery_gas_info["gas"] = result[0][dev]['data']['gas']
            battery_gas_info["temp"] = result[0][dev]['data']['temp']
            logging.info(f'from{request.ip}/resdient\n{tok}\n{battery_gas_info}')
            return json(battery_gas_info, status=200)
    except Exception as e:
        logging.warning(str(e))
        print(e)

@app.get("/safestatus")
async def safestatus(request):
    #https://gaxer.ddns.net/safestatus\?dev=gas1&tok=123456abcd&dev=gas1
    #https://127.0.0.1/safestatus\?dev=gas1&tok=123456abcd&dev=gas1
    try:
        tok = request.args.get("tok")
        dev = request.args.get("dev")
        if (tok == None) or (dev == None):
            return text('Argument Error', status=200)
        if tokencheck(list(collection.find({"profile.token":f"{tok}"}, {"profile.token":1, "_id":0}))) == False:
            return text('toekn invalid', status=200)
        else:
            result = list(collection.find({"profile.token":f"{tok}"}, {f"{dev}.safe":1, "_id":0}))
            safe = result[0]
            safestat = safe[dev]['safe']
            logging.info(f'from{request.ip}/safestatus\n{tok}\n{safestat}')
            return text(safestat, status=200)
    except Exception as e:
        logging.warning(str(e))
        return text(str(e), status=200)

@app.get("/devlist")
async def devlist(request):
    #https://127.0.0.1/devlist\?tok=123456abcd
    try:
        tok = request.args.get("tok")
        if tok == None:
            return text('Argument Error', status=200)
        if tokencheck(list(collection.find({"profile.token":f"{tok}"}, {"profile.token":1, "_id":0}))) == False:
            return text('token invalid', status=200)
        else:
            result = list(collection.find({"profile.token":f"{tok}"}, {"_id":0, "account":0, "profile":0}))
            dev = {"devList":""}    
            dev["devList"] = list(result[0].keys())
            #print(dev)
            return json(dev, status=200)
    except Exception as e:
        logging.warning(str(e))
        return text(str(e), status=200)

@app.get("/alert")
async def alert(request):
    #https://127.0.0.1/alert\?tok=123456abcd
    try:
        tok = request.args.get("tok")
        if tok == None:
            return text('Argument Error', status=200)
        if tokencheck(list(collection.find({"profile.token":f"{tok}"}, {"profile.token":1, "_id":0}))) == False:
            return text('token invalid', status=200)
        else:
            result = list(collection.find({"profile.token":f"{tok}", "safe":{"$ne":"0000"}}, {"_id":0, "account":0, "profile":0}))
            problem = {"alert":[]}
            alertdev = result[0].keys()
            for i in alertdev:
                problem["alert"].append({f"{i}":result[0][i]['safe']})
        return json(problem, status=200)
    except Exception as e:
        return text(str(e), status=200)

''''''
if __name__ == '__main__':
    ssl = {
        "cert":"gaxer_ddns_net.pem-chain", 
        "key":"key.pem"
    }
    app.run(host='0.0.0.0', port='443', debug=True, access_log=True, ssl = ssl)