'''
Author: yuan
Date: 2021-04-14 03:24:03
LastEditTime: 2021-04-17 01:25:39
FilePath: /line-chatbot/app.py
'''
from flask import Flask, abort, render_template, request
from flask_bootstrap import Bootstrap
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent, TextMessage)

from config import Config
from interface import (beverage, gossiping, movie, netflix,  # init_task()
                       news, oil_price, ptt_beauty, ptt_soft_job, ptt_tech_job, rate, technews,  Factory)
from my_dict import MyDict

app = Flask(__name__)
bootstrap = Bootstrap(app)
config = Config()
handler = config.handler
# line_bot_api = config.line_bot_api


class Bot:
    task_map = {
        MyDict.news: news,
        MyDict.ptt_beauty: ptt_beauty,
        MyDict.ptt_soft_job: ptt_soft_job,
        MyDict.ptt_tech_job: ptt_tech_job,
        MyDict.gossiping: gossiping,
        MyDict.movie: movie,
        MyDict.netflix: netflix,
        MyDict.technews: technews,
        MyDict.oil_price: oil_price,
        MyDict.rate: rate,
        MyDict.beverage: beverage
    }

    def __init__(self, val):
        self.val = val

    def get_fun(self):
        if self.val in Bot.task_map:
            action_fun = self.task_map.get(self.val)
        else:
            action_fun = 'default'
        return Factory, action_fun


@app.route("/")
def index():
    # return "Hello, yuan !  No UI. This is LINE chatbot  "
    title = 'Web Chat Bot'
    return render_template('index.html',
                           title=title,
                           data=MyDict.show_attribute())


@ app.route("/callback", methods=['POST'])
def callback():

    print('callback')
    # get X-Line-Signature header value
    signature = request.headers['X_LINE_SIGNATURE']
    # get request body as texts
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        # handle webhook body
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@ handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(f'event: {event}')
    message = event.message.text
    bot = Bot(message)
    # factory is class name , action_func is method name
    factory_class, action_func = bot.get_fun()
    print(action_func.__name__)
    task = factory_class(action_func, event)
    action_func(task)


if __name__ == "__main__":
    # app.config["host"] = "0.0.0.0"
    app.run(port=8000, debug=True)
