from pymongo import MongoClient

mongoclient = MongoClient('mongodb://account:pass@localhost:27017')
mongodb = mongoclient.gaxer
mongocollection = mongodb.user
document = [{"name":"炭烤A5和牛", "age":"22"}]

mongocollection.insert_many(document)

result = list(mongocollection.find({}))
print(result)
