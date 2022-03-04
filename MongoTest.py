from pymongo import MongoClient
from pprint import pprint
import time
from datetime import datetime
mongoclient = MongoClient('mongodb://root:mongo0928@localhost:27017')
mongodb = mongoclient.gaxer
mongocollection = mongodb["user"]
document = [{"info":{"name":"炭烤A5和牛", "age":"22", "addr":"大智街50號"}}]

#mongocollection.insert_many(document)
'''
mongocollection.update_one(
    {"account":"test01"}, 
    {"$set":{"gas2":""}}, 
    upsert=True
    )
target = 'test01'
result = list(mongocollection.find({"profile.pass":f"{target}"}, {"_id":0}))
pprint(result)
pprint(str(result))
print(f"fsting test {target}")
print(type(result))
'''

'''
request_acc = 'test01'
request_sw = 'True'
request_battery = '40'
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
struct_time = time.strptime(now, '%Y-%m-%d %H:%M:%S')
tstamp = int(time.mktime(struct_time))
fire = 169000
temp = 30
gas = 30.00
remaning = 1945.26
result = mongocollection.update_many(
    {"account":f"{request_acc}"}, 
    {"$set":
        {
            "gas1.uswitch":f"{request_sw}", 
            "gas1.battery":f"{request_battery}", 
            f"gas1.{tstamp}.fire":"168000"
        }   
    }, 
    upsert=True)
print(result)
'''

#超級重要
result = mongocollection.update_one(
    {"account":"test01"}, 
    {"$unset":{
        "gas1.1646405281":1
        }
    }
)
#print(result)
result = list(mongocollection.find({"account":"test01"}, {"_id":0, "profile":0}).limit(3))
pprint(result)
#print(type(result))
mongoclient.close()