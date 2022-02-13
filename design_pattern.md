# Design Pattern and OOP


## Singleton in config


```python
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
        ...

```


## 繼承