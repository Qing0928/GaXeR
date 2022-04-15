import hashlib

acc = 'test01'

s = hashlib.sha256()
s.update(acc.encode('utf-8'))

acc256 = s.hexdigest()

print(acc256)

html = '678e82d907d3e6e71f81d5cf3ddacc3671dc618c38a1b7a9f9393a83d025b296'
kotlin = '678e82d907d3e6e71f81d5cf3ddacc3671dc618c38a1b7a9f9393a83d025b296'
if acc256 == kotlin:
    print(True)