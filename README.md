# line bot 實作 django 


###### tags: `tutorials`

## product : [use heroku platform](https://dashboard.heroku.com/apps)
https://yuan-line-chatbot.herokuapp.com/callback

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
## TODO list

- 優化 飲料菜單
- 提供影片功能
