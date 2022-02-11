'''
Author: yuan
Date: 2021-04-14 03:24:03
LastEditTime: 2021-04-18 08:39:27
FilePath: /line-chatbot/app.py
'''
from flask import Flask, abort, render_template, request
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage)

from config import Config
from interface import (gossiping, movie, 
                        #   netflix,  # init_task()
                       tvbs_news, oil_price, ptt_beauty, ptt_soft_job, ptt_tech_job, rate, tech_news,
                       beverage_50lan,
                       beverage_coco, beverage_whitealley, beverage_milkshop,
                       beverage_chingshin, beverage_maculife,
                       beverage_presotea, beverage_dayungs,
                       start_template, ptt_template, news_template, movie_template,
                       beverage_template, beverage_template1, beverage_template2,
                       Factory, Template_Factory)
from my_dict import MyDict

app = Flask(__name__)
config = Config()
handler = config.handler


class Bot:
    # task_map = {
    #     MyDict.tvbs_news: tvbs_news,
    #     MyDict.ptt_beauty: ptt_beauty,
    #     MyDict.ptt_soft_job: ptt_soft_job,
    #     MyDict.ptt_tech_job: ptt_tech_job,
    #     MyDict.gossiping: gossiping,
    #     MyDict.movie: movie,
    #     # MyDict.netflix: netflix,
    #     MyDict.tech_news: tech_news,
    #     MyDict.oil_price: oil_price,
    #     MyDict.rate: rate,
    #     MyDict.beverage_50lan: beverage_50lan,
    #     MyDict.beverage_coco: beverage_coco,
    #     MyDict.beverage_whitealley: beverage_whitealley,
    #     MyDict.beverage_milkshop: beverage_milkshop,
    #     # MyDict.beverage_comebuy: beverage_comebuy,
    #     MyDict.beverage_chingshin: beverage_chingshin,
    #     MyDict.beverage_maculife: beverage_maculife,
    #     MyDict.beverage_presotea: beverage_presotea,
    #     MyDict.beverage_dayungs: beverage_dayungs,

    # }

    # template_map = {
    #     MyDict.start_word: start_template,
    #     MyDict.ptt_template: ptt_template,
    #     MyDict.news_template: news_template,
    #     MyDict.movie_template: movie_template,
    #     MyDict.beverage_template: beverage_template,
    #     MyDict.beverage_template1: beverage_template1,
    #     MyDict.beverage_template2: beverage_template2

    # }
    task_map = MyDict

    def __init__(self, val):
        self.val = val

    def get_fun(self):
        action_fun = Bot.task_map.get(self.val)
        factory = None
        print(f"self.val:{self.val}")
        printf(f"task_map:{task_map}")
        if self.val in Bot.task_map.values():
            factory = Factory
        elif self.val in Bot.task_map.values():
            # action_fun = Bot.task_map.get(self.val)
            factory = Template_Factory
        return factory, action_fun

    def lower(self):
        self.val = self.val.lower()


@app.route("/")
def index():
    # return "Hello, yuan !  No UI. This is LINE chatbot  "
    title = 'Web Chat Bot'
    data = [v for k, v in vars(Bot.task_map).items() if not k.startswith('__')]
    return render_template('index.html',
                           title=title,
                           data=data)


@ app.route("/callback", methods=['POST'])
def callback():

    print('callback')
    # get X-Line-Signature header value
    signature = request.headers['X_LINE_SIGNATURE']
    # get request body as texts
    body = request.get_data(as_text=True)
    print(body)
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
    print(message)
    bot = Bot(message)
    # factory is class name , action_func is method name
    factory_class, action_func = bot.get_fun()
    print(action_func.__name__)
    print(factory_class)
    task = factory_class(action_func, event)  # object
    action_func(task)


if __name__ == "__main__":
    # app.config["host"] = "0.0.0.0"
    app.run(port=8000, debug=True)
