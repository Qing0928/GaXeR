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
'''result = list(mongocollection.find(
    {"profile.token":"123456abcd"}, 
    {"_id":0, "profile":0, "account":0, "gas1.battery":0, "gas1.uswitch":0}
    ).limit(1))
pprint(result)
result = list(mongocollection.find(
    {"gas1.data.time":{
        "$gt":1646405285
    }},  
    {"_id":0, "profile":0, "account":0, "gas1.battery":0, "gas1.uswitch":0,}))
pprint(result)
mongocollection.update_one(
    {"account":"test01"}, 
    {"$push":{
        "gas1.data":{
            "time":1646469163, 
            "fire":1689949, 
            "temp":29.8, 
            "gas":33, 
            "remaining":1940.63
            }}}
)
result = list(mongocollection.aggregate([
    {"$match":{
        "account":"test02"}
        }, 
    {"$unwind":"$gas1.data"},
    {"$match":{
        "gas1.data.temp":{"$gt":29}}
        }, 
    {"$project":{
        "gas1.data":1, "_id":0}
        }, 
    {"$limit":5}
    ])
    )
print(result)
'''
mongocollection.update_many(
    {"account":"test01"},
    {
        "$push":{
                "gas1.data":{
                "time":1646471042, 
                "fire":1689949, 
                "temp":29.8, 
                "gas":29, 
                "remaining":1948
                }
            }, 
        "$set":{
            "gas1.uswitch":"False", 
            "gas1.battery":89
            }   
    }, upsert=True
)
#print(type(result))
mongoclient.close()