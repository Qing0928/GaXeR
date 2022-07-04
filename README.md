# GaXeR
## API
### 系統架構圖

![](https://i.imgur.com/xIcnnMB.png)

---

### 網址
https://gaxer.ddns.net

---

### 測試
https://gaxer.ddns.net/test

---

### 感測器上傳資料
https://gaxer.ddns.net/upload\?tok=123456abcd&battery=34&fire=170000&temp=29&gas=29.52&remaining=1940.85&safe=0010

| Example   |            |
| --------- | ---------- |
| tok       | 123456abcd |
| battery   | 34         |
| fire      | 170000     |
| temp      | 29         |
| gas       | 29.52      |
| remaining | 1940.85    |
| safe      | 0010       |

**目前tok都先用123456abcd**

參數皆正確
```htmlmixed=
'ok'
```
缺少參數
```htmlmixed=
'Argument Error'
```
無效的token
```htmlmixed=
'token invalid'
```

---

### 取得最新資料
https://gaxer.ddns.net/data\?tok=123456abcd&record=5


| Argument | Example    |
| -------- | ---------- |
| record   | 5          |
| tok      | 123456abcd |

需要幾筆資料就改record的數值，目前我先輸入了7組測資

**目前tok全部都先用123456abcd**

參數皆正確
```jsonld=
[
  {
    "gas1": 
      {
      "data": 
          {
            "time": 1646471657,
            "fire": 170000.0,
            "temp": 31.0,
            "gas": 29.52,
            "remaining": 1950.3
          }
      }
  }
]
```
缺少參數
```htmlmixed=
'Argument Error'
```
無效的token
```htmlmixed=
'token invalid'
```

---

### 取得開關狀態
https://gaxer.ddns.net/swstatus\?tok=123456abcd

| Argument | Example    |
| -------- | ---------- |
| tok      | 123456abcd |

**目前tok全部都先用123456abcd**

參數皆正確
```htmlmixed=
'Flase' or 'True'
```
缺少參數
```htmlmixed=
'Argument Error'
```
無效的token
```htmlmixed=
'token invalid'
```

---

### 更改開關狀態
https://gaxer.ddns.net/swupdate\?tok=123456abcd&sw=True

| Argument | Example    |
| -------- | ---------- |
| sw       | True       |
| tok      | 123456abcd |

**目前tok全部都先用123456abcd**
**現在會針對sw這個參數值進行偵測，出現True/False以外的值，會回傳Argument Error**

參數皆正確
```htmlmixed=
'ok'
```
缺少參數
```htmlmixed=
'Argument Error'
```
無效的token
```htmlmixed=
'token invalid'
```

---

### 常駐型資料
https://gaxer.ddns.net/resident\?tok=123456abcd

| Argument | Example    |
| -------- | ---------- |
| tok      | 123456abcd |

**目前tok全部都先用123456abcd**

參數皆正確
```jsonld=
{
    "battery": 88,
    "gas": 29.52, 
    "temp":31.0
}
```
缺少參數
```htmlmixed=
'Argument Error'
```
無效的token
```htmlmixed=
'token invalid'
```

---

### 取得裝置狀態碼
https://gaxer.ddns.net/safestatus\?tok=123456abcd

| Argument | Example    |
| -------- | ---------- |
| tok      | 123456abcd |

**目前tok全部都先用123456abcd**

參數皆正確
```htmlmixed=
'0010'
```
缺少參數
```htmlmixed=
'Argument Error'
```
無效的token
```htmlmixed=
'token invalid'
```

#### 狀態碼規則


| 狀態     | 值   |
| -------- | ---- |
| 正常     | 0000 |
| 溫度異常 | 0001 |
| 瓦斯異常 | 0010 |
| 電量不足 | 1000 |
| 火焰異常 | 0100 |

---

### 帳號申請
https://gaxer.ddns.net/signup

**使用的是post而非get，點開網址沒用**

傳過來的json
```jsonld=
{
    "acc":"test03", 
    "ps":"937E8D5FBB48BD4949536CD65B8D35C426B80D2F830C5C308E2CDEC422AE2244"
}
```
ps欄位為app端對使用者密碼進行sha256雜湊過後的結果
回傳的json
```htmlmixed=
"583a28281f4bfdd44741598f4936203ae0bdce11af0dba28045de6347205f8bf" 
```
回傳結果為用戶專屬的token，以用戶的account進行sha256雜湊產生

---

### 登入
https://gaxer.ddns.net/signin

**使用的是post而非get，點開網址沒用**

傳過來的json
```jsonld=
{
    "acc":"test03", 
    "ps":"937E8D5FBB48BD4949536CD65B8D35C426B80D2F830C5C308E2CDEC422AE2244"
}
```
ps欄位為app端對使用者密碼進行sha256雜湊過後的結果
回傳的json
```htmlmixed=
"583a28281f4bfdd44741598f4936203ae0bdce11af0dba28045de6347205f8bf" 
```

帳號錯誤
```htmlmixed=
"invalid user"
```
密碼錯誤
```htmlmixed=
"pass error"
```

---

### 取得用戶裝置清單
https://gaxer.ddns.net/devlist\?tok=678E82D907D3E6E71F81D5CF3DDACC3671DC618C38A1B7A9F9393A83D025B296

回傳結果
```jsonld=
{
  "devList": [
    "gas1"
  ]
}
```
缺少參數
```htmlmixed=
'Argument Error'
```
無效的token
```htmlmixed=
'token invalid'
```

---

### 取得有問題的裝置
https://gaxer.ddns.net/alert\?tok=678E82D907D3E6E71F81D5CF3DDACC3671DC618C38A1B7A9F9393A83D025B296

回傳結果

```jsonld=
{
  "alert": [
    {
      "gas1": "0010"
    },
    {
      "gas2": "0010"
    }
  ]
}
```
缺少參數
```htmlmixed=
'Argument Error'
```
無效的token
```htmlmixed=
'token invalid'
```

---

### 取得裝置所屬群組
https://gaxer.ddns.net/groupcheck\?tok=678E82D907D3E6E71F81D5CF3DDACC3671DC618C38A1B7A9F9393A83D025B296&dev=gas1

| Argument | Example                                                          |
| -------- | ---------------------------------------------------------------- |
| tok      | 678E82D907D3E6E71F81D5CF3DDACC3671DC618C38A1B7A9F9393A83D025B296 |
| dev      | gas1                                                             |

沒有群組
```htmlembedded=
"nan"
```
有群組
```htmlembedded=
"group2F"
```

---

### 註冊群組
https://gaxer.ddns.net/groupregister

**使用的是post而非get，點開網址沒用**

傳過來的form

```jsonld=
{
    "token":"678E82D907D3E6E71F81D5CF3DDACC3671DC618C38A1B7A9F9393A83D025B296", 
    "name":"2F",
    "dev":"{"gas1":"MAC"},{"gas1":"MAC"},"
}
```

---

### 查詢群組資料
#### 簡易

https://gaxer.ddns.net/groupsimple\?tok=678E82D907D3E6E71F81D5CF3DDACC3671DC618C38A1B7A9F9393A83D025B296&group=groupfinal

| Argument | Example                                                          |
| -------- | ---------------------------------------------------------------- |
| tok      | 678E82D907D3E6E71F81D5CF3DDACC3671DC618C38A1B7A9F9393A83D025B296 |
| group      | groupfinal                                                             |

回傳資料
```htmlembedded=
2
```

#### 詳細
https://gaxer.ddns.net/groupdetail\?tok=678E82D907D3E6E71F81D5CF3DDACC3671DC618C38A1B7A9F9393A83D025B296&group=groupfinal

| Argument | Example                                                          |
| -------- | ---------------------------------------------------------------- |
| tok      | 678E82D907D3E6E71F81D5CF3DDACC3671DC618C38A1B7A9F9393A83D025B296 |
| group    | groupfinal                                                       |

回傳資料
```htmlembedded=
24:0A:C4:59:A5:44,34:94:54:24:85:0C
```

---

### 刪除群組
**沒事不要亂點，還在測試**

https://gaxer.ddns.net/ungroup\?tok=678E82D907D3E6E71F81D5CF3DDACC3671DC618C38A1B7A9F9393A83D025B296&group=groupfinal

| Argument | Example                                                          |
| -------- | ---------------------------------------------------------------- |
| tok      | 678E82D907D3E6E71F81D5CF3DDACC3671DC618C38A1B7A9F9393A83D025B296 |
| group    | groupfinal                                                       |

回傳資料
```htmlembedded=
ok
```
