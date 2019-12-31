import sys
from weibo import Client


## 微连接 移动应用 申请
API_KEY = "xxxxx"
API_SECRET = "xxxxxxxxxxxxxxxxxxxxxxxxxx"
REDIRECT_URI = "https://api.weibo.com/oauth2/default.html"
c = Client(API_KEY, API_SECRET, REDIRECT_URI)

# 通过手动操作，访问 authorize_url 得到 access或者authorize code
url = c.authorize_url
print(url)
code = input()
c.set_code(code)

out = open("res.txt", 'w', encoding="utf8")

## 获取公共微博
d = c.get('statuses/public_timeline', count = 200)

for i in range(len(d['statuses'])):
    cc = d['statuses'][i]['text'].strip()
    cc = cc.replace('\u200b', '').replace('\n', '    ').strip()
    out.write(cc + '\n')
