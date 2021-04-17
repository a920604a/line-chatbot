'''
Author: yuan
Date: 2021-04-14 05:53:15
LastEditTime: 2021-04-17 01:26:52
FilePath: /line-chatbot/interface.py
'''

from linebot.models import (
    ImageSendMessage,
    TextSendMessage, )

from config import Config
from serve import (Beverage, Gossiping, Movie, Netflix, News, OilPrice,
                   PttBeauty, PttSoftJob, PttTechJob, Rate, Technews)

# from serve import


config = Config()
line_bot_api = config.line_bot_api


class Factory:
    def __init__(self, func=None, event=None):
        self.name = func.__name__
        self.event = event

    def reply_message(self, obj):
        line_bot_api.reply_message(self.event.reply_token, obj)


def news(self):
    task = News()
    self.reply_message(TextSendMessage(text=task.parser()))


def ptt_beauty(self):
    task = PttBeauty()  # over 18
    self.reply_message(TextSendMessage(text=task.parser()))


def gossiping(self):
    task = Gossiping()  # over 18
    self.reply_message(TextSendMessage(text=task.parser()))


def ptt_soft_job(self):
    task = PttSoftJob()
    self.reply_message(TextSendMessage(text=task.parser()))


def ptt_tech_job(self):
    task = PttTechJob()
    self.reply_message(TextSendMessage(text=task.parser()))


def movie(self):
    task = Movie()
    self.reply_message(TextSendMessage(task.parser()))


def netflix(self):  # optimize
    task = Netflix()
    self.reply_message(TextSendMessage(task.parser()))


def technews(self):
    task = Technews()
    self.reply_message(TextSendMessage(task.parser()))


def oil_price(self):
    task = OilPrice()
    self.reply_message(TextSendMessage(task.parser()))


def rate(self):  # not finish
    task = Rate()
    self.reply_message(TextSendMessage(task.parser()))


def beverage(self):  # reply menu image and beverage price
    task = Beverage()
    for k, _url in Beverage.menu.items():
        print(k, _url)
    self.reply_message(ImageSendMessage(
        original_content_url=_url, preview_image_url=_url))
