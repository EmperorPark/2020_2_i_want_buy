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

import pprint

class TeleGramBotManager:

    def __init__(self, id, q):
        with open('../tele_key.txt', 'r') as file_handle:
            self.line_txt = file_handle.readline()

        self.BOT_TOKEN=self.line_txt.strip()

        self.updater = Updater( token=self.BOT_TOKEN, use_context=True )
        self.dispatcher = self.updater.dispatcher

        self.task_buttons_handler = CommandHandler( 'tasks', self.cmd_task_buttons )
        self.start_buttons_handler = CommandHandler( 'start', self.cmd_start_buttons )
        self.reg_buttons_handler = CommandHandler( 'reg', self.cmd_reg_buttons )
        self.available_buttons_handler = CommandHandler( 'available', self.cmd_available_buttons )
        self.say_buttons_handler = CommandHandler( 'say', self.say, pass_args=True)
        self.button_callback_handler = CallbackQueryHandler( self.cb_button )    

        self.dispatcher.add_handler(self.task_buttons_handler)
        self.dispatcher.add_handler(self.start_buttons_handler)
        self.dispatcher.add_handler(self.reg_buttons_handler)
        self.dispatcher.add_handler(self.available_buttons_handler)
        self.dispatcher.add_handler(self.say_buttons_handler)
        self.dispatcher.add_handler(self.button_callback_handler)

        self.updater.start_polling()
        self.updater.idle()
    
    def cmd_task_buttons(self, update, context):
        task_buttons = [[
            InlineKeyboardButton( '1.상품 등록 확인', callback_data=1 )
            , InlineKeyboardButton( '2.상품 판매확인', callback_data=2 )
        ], [
            InlineKeyboardButton( '3.취소', callback_data=3 )
        ]]
        
        reply_markup = InlineKeyboardMarkup( task_buttons )
        
        context.bot.send_message(
            chat_id=update.message.chat_id
            , text='작업을 선택해주세요.'
            , reply_markup=reply_markup
        )

    def cmd_start_buttons(self, update, context):
        context.bot.send_message(
            chat_id=update.message.chat_id
            , text='안녕하세요. 사고싶다에 오신걸 환영합니다.'
        )
    
    def say(self, update, context):
        output_message = str(update.message.chat_id) + '은 이렇게 말했습니다.\n' + str(context.args)
        update.message.reply_text(output_message)

    def cmd_reg_buttons(self, update, context):
        context.bot.send_message(
            chat_id=update.message.chat_id
            , text='구현중.'
        )

    def cmd_available_buttons(self, update, context):
        context.bot.send_message(
            chat_id=update.message.chat_id
            , text='구현중.'
        )

    def cb_button(self, update, context):
        query = update.callback_query
        data = query.data
        
        context.bot.send_chat_action(
            chat_id=update.effective_user.id
            , action=ChatAction.TYPING
        )
        
        if data == '3':
            context.bot.edit_message_text(
                text='작업이 취소되었습니다.'
                , chat_id=query.message.chat_id
                , message_id=query.message.message_id
            )
        else:
            context.bot.edit_message_text(
                text='[{}] 작업이 진행중입니다.'.format( data )
                , chat_id=query.message.chat_id
                , message_id=query.message.message_id
            )
            
            if data == '1':
                self.crawl_navernews()
            elif data == '2':
                self.crawl_zigbang()
            
            context.bot.send_message(
                chat_id=update.effective_chat.id
                , text='[{}] 작업을 완료하였습니다.'.format( data )
            )
        
    def crawl_navernews(self):
        time.sleep( 5 )
        print( '네이버에서 뉴스를 수집했다.' )
        
    def crawl_zigbang(self):
        time.sleep( 5 )
        print( '직방에서 매물을 수집했다.' )
        
    
