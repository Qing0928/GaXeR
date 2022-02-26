from tkinter import E
from sanic import Sanic
from sanic import json, text

app = Sanic('GaXeR')

@app.get('/test')
async def test(request):
    try:
        print('from {}'.format(request.ip))
        return text('Hello World')
    
    except Exception as e:
        print(e)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='9002', debug=False, access_log=True)