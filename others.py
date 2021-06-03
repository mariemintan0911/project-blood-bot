from re import sub
from typing import Dict

from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    CallbackContext,
)

START_MENU, START_ELIGIBILITY, ANSWERED, TEMP_DEF_PROMPT, SICK_QUESTION, CHOOSING_ILLNESS, OTHER_ILLNESS, CONTINUE = range(8)


start_keyboard = [
    ['Basic Eligibility Quiz'],
    ['Reasons for Temporary Deferral'],
    ['Reasons for Permanent Deferral'],
    ['How do I sign up for Project Blood upcoming blood drive?'],
    ['Bye Bye Mr Bot man!']
]

start_markup = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True)

def permanent(update: Update, context: CallbackContext) -> int:
  update.message.reply_text(
    'You cannot donate blood if you have any of the following conditions:\n'
    '• Heart or lung disease (those with asymptomatic asthma can still give blood)\n'
    '• Previous or current history of cancer\n'
    '• High blood pressure and taking medication (except diuretics)\n'
    '• Diabetes and taking medication\n'
    '• Abnormal bleeding tendencies or blood disorder\n'
    '• AIDS or symptoms of AIDS, such as unexplained fevers, severe night sweats,unexpected weight loss, swollen glands or chronic diarrhoea\n'
    '• Uncontrolled seizures after infancy\n'
    '• Hepatitis B or C\n'
    '• Syphilis\n'
    '• Underwent major surgery 6 to 12 months ago\n\n'

    'What do you want to find out next?',
    reply_markup = start_markup,
  )
  return START_MENU

def sign_up(update: Update, context: CallbackContext) -> int:
  update.message.reply_text(
    'Booking an appointment is mandatory before entering our premises at Marymount CC on 24 July 2021.\n' 
    'You can book a slot via Singpass or through our forms at www.___\n\n'

    'What do you want to find out next?',
    reply_markup = start_markup,
  )

  return START_MENU
