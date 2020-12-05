import sys
if __name__ == '__main__':
    print ('직접실행불가')
    sys.exit(0)

# python -m pip install python-telegram-bot --upgrade
import time
from telegram import ChatAction
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler
from bs4 import BeautifulSoup

import carwlShoppingMall

class TeleGramBotManager:

    def __init__(self, id, q, dec_key):
        self.objCarwlShoppingMall = q.get()

        self.BOT_TOKEN='iyhI2cFhKcosAP7jDEhg3pHsYfwjGcQQovJO8I9emi0qWoUCeXmjGBAxNDhD5cVM'

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            'Referer': 'https://kornorms.korean.go.kr/example/exampleList.do?regltn_code=0003',
        }

        data = {
            'inpText': self.BOT_TOKEN,
            'inpKey': dec_key,
            'sleBlockSize': '256',
            'direction': 'Decrypt'
        }

        result = self.objCarwlShoppingMall.webRequest('POST', 'https://aesencryption.net/', header_dict=headers, params_dict=data)

        soup_obj = BeautifulSoup(result, "html.parser")
        dec_data = soup_obj.find("textarea", {"id": "taOutText"})
        if dec_data != None:
            self.BOT_TOKEN = dec_data.text.strip()

        self.updater = Updater( token=self.BOT_TOKEN, use_context=True )
        self.dispatcher = self.updater.dispatcher

        self.start_buttons_handler = CommandHandler( 'start', self.cmd_start_buttons )
        self.reg_buttons_handler = CommandHandler( 'reg', self.cmd_reg_buttons, pass_args=True )
        self.available_buttons_handler = CommandHandler( 'available', self.cmd_available_buttons, pass_args=True )
        self.help_buttons_handler = CommandHandler( 'help', self.cmd_help_buttons )

        self.dispatcher.add_handler(self.start_buttons_handler)
        self.dispatcher.add_handler(self.reg_buttons_handler)
        self.dispatcher.add_handler(self.available_buttons_handler)
        self.dispatcher.add_handler(self.help_buttons_handler)

        self.updater.start_polling()
        self.updater.idle()
    

    def cmd_start_buttons(self, update, context):
        context.bot.send_message(
            chat_id=update.message.chat_id
            , text='안녕하세요. 사고싶다에 오신걸 환영합니다. /help를 입력하여 사용법을 확인해 주세요'
        )

    def cmd_help_buttons(self, update, context):
        text_msg = '안녕하세요. 사고싶다에 오신걸 환영합니다.\n'
        text_msg += '명령어를 안내합니다.\n'
        text_msg += '/start - 사고싶다 시작\n'
        text_msg += '/help - 사고싶다 봇 안내\n'
        text_msg += '/reg [검색어] - 상품이 쇼핑몰들에 등록되었는지 확인\n'
        text_msg += '/available [쿠팡 혹은 신세계 구매 페이지 URL] - URL의 상품이 구매 가능한지 확인\n'
        context.bot.send_message(
            chat_id=update.message.chat_id
            , text=text_msg
        )

    def cmd_reg_buttons(self, update, context):
        searchWord = ''
        for word in context.args:
            searchWord += word
            searchWord += ' '
        try:
            result = self.objCarwlShoppingMall.getGoodsRegisteredBySearch(searchWord)
        except Exception as e:
            print('예외 발생')
            print(e)
            result = '오류가 발생하였습니다. 해당메세지를 관리자에게 전달해 주세요' + '\n' + e
            context.bot.send_message(
                chat_id=update.message.chat_id
                , text=result
            )
            pass
        
        result_temp = ''
        count = 1
        for line in result.split('\n'):
            result_temp += line + '\n'
            if count % 10 == 0:
                context.bot.send_message(
                    chat_id=update.message.chat_id
                    , text=result_temp
                )
                result_temp = ''
            count += 1
            
        if result_temp.strip() != '':
            context.bot.send_message(
                chat_id=update.message.chat_id
                , text=result_temp
            )
        
    def cmd_available_buttons(self, update, context):
        if len(context.args) == 1:
            site_url = context.args[0]
            try:
                result = self.objCarwlShoppingMall.getGoodsPurchaseAvailableByURL(site_url)
            except Exception as e:
                print('예외 발생')
                print(e)
                result = '오류가 발생하였습니다. 해당메세지를 관리자에게 전달해 주세요' + '\n' + e
                context.bot.send_message(
                    chat_id=update.message.chat_id
                    , text=result
                )
                pass
        elif len(context.args) == 0:
            result = '사이트 URL을 입력해 주세요.'
        else:
            result = '사이트 URL은 공백없이 입력되어야 합니다.'

        context.bot.send_message(
            chat_id=update.message.chat_id
            , text=result
        )

    
    
