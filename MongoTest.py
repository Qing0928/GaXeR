from pymongo import MongoClient
from pprint import pprint
mongoclient = MongoClient('mongodb://root:mongo0928@localhost:27017')
mongodb = mongoclient.gaxer
mongocollection = mongodb.user
document = [{"info":{"name":"炭烤A5和牛", "age":"22", "addr":"大智街50號"}}]

#mongocollection.insert_many(document)
#mongocollection.update_one({"account":"test01"}, {"$set":{"gas2":""}}, upsert=True)
target = 'test01'
result = list(mongocollection.find({"profile.pass":f"{target}"}, {"_id":0}))
pprint(result)
pprint(str(result))
print(f"fsting test {target}")
#print(type(result))