# -*- coding: utf-8 -*-

from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ

@respond_to('こんにちは')
def respond_func(message):
    message.reply('こんにちは！')

@respond_to('おやすみ')
def respond_func(message):
    message.react('x')
    message.reply('まだ夜じゃないよ！')

@listen_to('お腹すいた')
def listen_func(message):
    message.send('一緒にラーメン食べにいく？:ramen::ramen:')