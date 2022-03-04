from sanic import Sanic
from sanic import json, text
#from sanic.response import file
from pymongo import MongoClient
client = MongoClient('mongodb://root:mongo0928@localhost:27017')
db = client.gaxer
collection = db.user

app = Sanic('GaXeR')

@app.get('/test')
async def test(request):
    try:
        print('from {}'.format(request.ip))
        #return text(status=200)
        return text('Hello World', status=200)
    except Exception as e:
        print(e)
        
@app.get('upload')
async def update(request):
    try:
        '''print(request.args)
        print(request.args.get("hum"))
        print(request.args.getlist("hum"))'''
        
        return text('ok', status=200)
    except Exception as e:
        print(e)

@app.get('data')
async def data(request):
    try:
        result = list(collection.find({"profile.pass":"test01"}, {"_id":0}))
        return json(result, status=200)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    ssl = {
        "cert":".\gaxer_ddns_net.pem-chain", 
        "key":".\key.pem"
    }
    app.run(host='0.0.0.0', port='1234', debug=False, access_log=True, ssl=ssl)