# -*- coding: utf-8 -*-

from slackbot.bot import Bot

import logging
logging.getLogger().setLevel(logging.INFO)

def main():
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    print('start slackbot')
    main()