'''
Author: yuan
Date: 2021-04-14 03:29:03
LastEditTime: 2021-04-14 13:22:34
FilePath: /line-chatbot/config.py
'''
import configparser
from linebot import (
    LineBotApi, WebhookHandler
)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Config(metaclass=Singleton):

    def __init__(self, file='config.ini'):
        self.config = configparser.ConfigParser()
        self.open_file(file)
        self.Channel_Secret = self.config['line_bot']['Channel_Secret']
        self.Channel_Access_Token = self.config['line_bot']['Channel_Access_Token']

        self.handler = None
        self.line_bot_api = None
        self.line_bot_init()

    def open_file(self, file):
        self.config.read(file)
        if not self.config.sections():
            raise configparser.Error('config.ini not exists')

    def line_bot_init(self):
        self.handler = WebhookHandler(self.Channel_Secret)
        self.line_bot_api = LineBotApi(self.Channel_Access_Token)
