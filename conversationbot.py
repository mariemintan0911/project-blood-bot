#!/usr/bin/env python
# pylint: disable=C0116
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.1
"""

import logging

from telegram.message import Message
import config
from typing import Dict
import others
import eligibility
import temporary_deferral

from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

START_MENU, START_ELIGIBILITY, ANSWERED, TEMP_DEF_PROMPT, SICK_QUESTION, CHOOSING_ILLNESS, OTHER_ILLNESS, CONTINUE = range(8)

start_keyboard = [
    ['if I pass the Basic Eligibility Quiz'],
    ['reasons for Temporary Deferral'],
    ['reasons for Permanent Deferral'],
    ['how to sign up for 24th July blood drive?'],
    ['Bye Bye Bot Bot!']
]

start_markup = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True)

def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Welcome!! I am Project Blood SG's Bot Bot! What will you like to do today?\n\n\n I want to find out...",
        reply_markup = start_markup,
    )

    return START_MENU

eligibility_keyboard = [
    ['Start', 'Back'],
]

eligibility_markup = ReplyKeyboardMarkup(eligibility_keyboard, one_time_keyboard=True)

def is_eligible(update: Update, context: CallbackContext) -> int:    
    update.message.reply_text(
        text="Hi! Welcome to Project Blood. Let's take an eligibility test",
        reply_markup=eligibility_markup,
    )

    return START_ELIGIBILITY

def bye(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        f'Bye Bye! We hope you enjoyed using this bot and it has helped you understand the prerequisites to donate blood.\n'
        'Disclaimer: The content provided in this telebot is non-exhaustive. Please check out https://www.hsa.gov.sg/blood-donation/can-i-donate for a more comprehensive guide on blood donations.\n\n'
        'Project Blood SG hopes to see you on 24th July!;)\n\n'
        'This bot is brought to you by Bing, Edric and Marie:))'
    )

    return ConversationHandler.END


    
def main():
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(config.TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            START_MENU: [
                MessageHandler(
                    Filters.regex('if I pass the Basic Eligibility Quiz'), is_eligible
                ), 
                MessageHandler(
                    Filters.regex('^reasons for Temporary Deferral$'), temporary_deferral.temporary_deferral_prompt
                ), 
                MessageHandler(
                    Filters.regex('reasons for Permanent Deferral'), others.permanent
                ), 
                MessageHandler(
                    Filters.regex('how to sign up for 24th July blood drive?'), others.sign_up
                ), 
                MessageHandler(
                    Filters.regex('Bye Bye Bot Bot!'), bye
                ), 
            ],
            START_ELIGIBILITY: [
                MessageHandler(
                    Filters.regex('^Start$'), eligibility.question
                ),
                MessageHandler(
                    Filters.regex('Back'), start
                )
            ],
            ANSWERED: [
                MessageHandler(
                    ~Filters.regex('^Back$'), eligibility.answer
                ),
                MessageHandler(
                    Filters.regex('^Back$'), start
                )
            ],
            TEMP_DEF_PROMPT: [
                MessageHandler(
                    ~Filters.regex('Back$'), temporary_deferral.answer
                ),
                MessageHandler(
                    Filters.regex('Back$'), start
                )
            ], 
            SICK_QUESTION: [
                MessageHandler(
                    Filters.regex("^Let's do it!$"), temporary_deferral.sick_question
                ),
                MessageHandler(
                    Filters.regex("^Nah$"), start
                )
            ],
            CHOOSING_ILLNESS: [
                MessageHandler(
                    ~Filters.regex('^Done$'), temporary_deferral.display_illness
                )
            ], 
            CONTINUE: [
                MessageHandler(
                    Filters.regex('^Continue$'), start
                ),
                MessageHandler(
                    ~ Filters.regex('^Continue$'), bye
                )
            ]
        },
        fallbacks=[MessageHandler(Filters.regex('^Bye$'), bye)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
