<!--
 * @Author: yuan
 * @Date: 2021-04-17 04:13:49
 * @LastEditTime: 2021-04-18 08:29:39
 * @FilePath: /line-chatbot/README.md
-->
line bot 實作 django 
===

###### tags: `tutorials`
## develop : Ngrok tool https://5d60310b044b.ngrok.io/callback
## product : use heroku platform https://yuan-line-chatbot.herokuapp.com/callback


## 註冊為Line Developer
1. 前往[Line Developer](https://developers.line.biz/en/)註冊成為Line deeveloper
2. Create new provider
![](https://i.imgur.com/FyIKma6.png)
3. Create a Message API channel
![](https://i.imgur.com/ohjfrrh.png)
4. register some thing 
![](https://i.imgur.com/1sSWyS0.png)
5. 完成後，可以看到如下畫面
![](https://i.imgur.com/TdrAY3M.png)



[line-chat-bot](https://github.com/line/line-bot-sdk-python)
```bash=
sudo apt-get install python3-pip
pip3 install line-bot-sdk
sudo apt install python3-django
pip3 install beautifulsoup4
pip3 install requests
```


## django LINE Bot應用程式(APP)
1. download Python package
```bash=
django-admin startproject mylinebot .  #建立Django專案
python3  manage.py startapp beveragebot  #建立Django應用程式
python3 manage.py migrate  #執行資料遷移(Migration)

```
2. create app
```bash=
django-admin startproject mylinebot .  #建立Django專案
 
python3 manage.py startapp beveragebot  #建立Django應用程式
 
python3 manage.py migrate  #執行資料遷移(Migration)
```
![](https://i.imgur.com/K7t72JU.png)READM
- 專案架構如下圖
![](https://i.imgur.com/SfAAvPr.png)
 
3. Line 憑證
- 開啟Django專案主程式下的settings.py檔案，增加LINE Developers上所取得的兩個憑證設定
```python=
LINE_CHANNEL_ACCESS_TOKEN = 'Messaging API的Channel access token'
 
LINE_CHANNEL_SECRET = 'Basic settings的Channel Secret'
```

- 在Django專案setting.py INSTALL_APPS的地方，加上剛剛所建立的Django應用程式(APP)，如下範例：
```python=
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'beveragebot.apps.BeveragebotConfig',
]
```
4. 開發LINE Bot應用程式

```python=

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):

    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            ## todo some algorithm.
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text=event.message.text)
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

```


5. add urls
- Django應用程式urls.py
```python=

from django.urls import path
from . import views
 
urlpatterns = [
    path('callback', views.callback)
]
```
- Django專案主程式urls.py
```python=

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('beveragebot/', include('beveragebot.urls')) #包含應用程式的網址
]
```




## [flask LINE BOT 應用程式(APP)](https://github.com/line/line-bot-sdk-python)
```python=
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()

```
## 用Ngrok讓網址能夠公開
1. 前往[Ngrok官網](https://ngrok.com/)下載
![](https://i.imgur.com/NGaCXeM.png)

2. 解壓縮，認證，公開port
![](https://i.imgur.com/oVzsYNt.png)

3. 在django setting.py

```
ALLOWED_HOSTS = ['654b1edf967e.ngrok.io','localhost']
```
## 大功告成
- 執行LINE Bot應用程式(APP)`python manage.py runserver`
## 設定LINE Webhook URL
- 修改Message API-> Webhook settings
![](https://i.imgur.com/rfevtOK.png)

- 修改Message API-> LINE Official Account features ->Auto-reply messages
 ![](https://i.imgur.com/G6VfSUZ.png)
 
 
## 部署至heroku
```
curl https://cli-assets.heroku.com/install-ubuntu.sh | sh
heroku login -i
heroku create yuan-line-chatbot[你-APP-的名字]

```

#### prepare Procfile, requirement.txt runtme.txt[optional]
- Procfile
- 假設我們所執行的檔案是app_core
web: gunicorn app_core:app –preload


```bash=

git init
heroku git:remote -a yuan-line-chatbot
# set git remote heroku to https://git.heroku.com/yuan-line-chatbot.git
# git config  檢查

git add .
# git status 檢查

git config user.email "a920604a@gmail.com"
git config user.name "Chen Yu-An" 

git commit -m "v1"   
git push heroku master
# remote: Verifying deploy... done.
# To https://git.heroku.com/yuan-line-chatbot.git
#  * [new branch]      master -> master
```
## 結果
![](https://i.imgur.com/pX5pqyI.png)
