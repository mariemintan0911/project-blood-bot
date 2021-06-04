from typing import Dict

from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    CallbackContext,
)

START_MENU, START_ELIGIBILITY, ANSWERED, TEMP_DEF_PROMPT, SICK_QUESTION, CHOOSING_ILLNESS, OTHER_ILLNESS, CONTINUE = range(8)

answer_keyboard = [
    ['Yes', 'No'],
    ['Back']
]

index = -1

questions = ['Lets Start! Are you 16-60 years old?(Age is determined by birthday. Parental consent is needed for 16 and 17 year olds - hsa.gov.sg/parent_consent)',
            'Are you above 45kg',
            'Are you generally in good health? (No symptoms of infection for at least one week, e.g. sore throat, cough, flu, diarrhoea, and no fever in the last 4 weeks)',
            'Have you visited or lived in the United Kingdom between 1980 and 1996 for a cumulative period of 3 months or longer? Have you visited or lived in France since 1980 for a cumulative period of 5 years or longer?',
            'Are you experiencing heavy menstrual flow or cramps? Are you pregnant or breastfeeding your child now?',
            'Have you done dental work recently?',
            'Have you taken herbal supplements or traditional herbal remedies recently?',
            'Have you had a piercing or a tattoo recently, done with non-disposable needles?',
            'Do you have diabetes or hypertension (high blood pressure)?',
            'Have you travelled overseas to a malaria endemic area in the past 4 months? (Visit hsa.gov.sg/travel_deferral for the latest list of malaria endemic areas.)',
            ]

answers = ['Yes','Yes','Yes','No','No','No','No','No','No','No']

wrong_answers = ['No','No','No','Yes','Yes','Yes','Yes','Yes','Yes','Yes']



answer_markup = ReplyKeyboardMarkup(answer_keyboard, one_time_keyboard=True)

def question(update: Update, context: CallbackContext) -> int:
    global index
    if index == 9:
       return eligible(update, context)
    index = index + 1
    update.message.reply_text(
        f"{questions[index]}",
        reply_markup=answer_markup,
    )
    
    return ANSWERED

def answer(update: Update, context: CallbackContext) -> int:
    global index
    if update.message.text == wrong_answers[index]:
        return not_eligible(update, context)
    elif update.message.text == answers[index]:
        return question(update, context)
    return ANSWERED

start_keyboard = [
    ['if I pass the Basic Eligibility Quiz'],
    ['reasons for Temporary Deferral'],
    ['reasons for Permanent Deferral'],
    ['how to sign up for 24th July blood drive?'],
    ['Bye Bye Bot Bot!']
]

start_markup = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True)

def not_eligible(update: Update, context: CallbackContext) -> int:  
    global index
    index = -1
    update.message.reply_text(
        f"Sorry you did not pass the pass the eligibility test :( \nThe question above was why you are unable to donate.\nTo find out more, please visit https://www.hsa.gov.sg/blood-donation/can-i-donate.\n\n"
        'Do click on the other options to learn about other possible deferral reasons!',
        reply_markup = start_markup,
    )

    return START_MENU

def eligible(update: Update, context: CallbackContext) -> int:
    global index
    index = -1
    update.message.reply_text(
        f"Yay! you have passed our basic requirement test! However, there are other factors to consider before donating blood!\n\n"
        'Click on the other options to learn more about possible deferral reasons!',

        reply_markup = start_markup,
    )
    return START_MENU
