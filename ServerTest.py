import requests

da = {'acc':'test03', 'ps':'937E8D5FBB48BD4949536CD65B8D35C426B80D2F830C5C308E2CDEC422AE2244'}
print(f'{da}\n----------------------------------------')
response = requests.post("https://127.0.0.1/signup", json=da, verify=False).text
print(response)