from re import sub
from typing import Dict
import conversationbot

from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    ConversationHandler,
    CallbackContext,
)

START_MENU, START_ELIGIBILITY, ANSWERED, TEMP_DEF_PROMPT, SICK_QUESTION, CHOOSING_ILLNESS, OTHER_ILLNESS, CONTINUE = range(8)

subquestion_keyboard = [['I had COVID/ taken COVID vaccine'],
                        ['I was sick the past 6 months'], #Chickenpox, measles or mumps  Cold Flu sore throat..Dengue Fever..Diarrhoea..Fever
                        ['I have taken medication/antibiotics the past 6 months'],
                        ['I am diagnosed with a mental health condition'],
                        ['I am sexually active'],
                        ['I recently gotten a vaccine/immunisation'],
                        ['Back']          
                        ]


                        
subquestions =  ['I had COVID/ taken COVID vaccine',
                'I was sick the past 6 months', #Chickenpox, measles or mumps  Cold Flu sore throat..Dengue Fever..Diarrhoea..Fever
                'I have taken medication/antibiotics the past 6 months',
                'I am diagnosed with a mental health condition',
                'I am sexually active',
                'I recently gotten a vaccine/immunisation'
                ]

subquestion_markup = ReplyKeyboardMarkup(subquestion_keyboard, one_time_keyboard=True)

start_keyboard = [
    ['Basic Eligibility Quiz'],
    ['Reasons for Temporary Deferral'],
    ['Reasons for Permanent Deferral'],
    ['How do I sign up for Project Blood upcoming blood drive?'],
    ['Bye Bye Mr Bot man!']
]

start_markup = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True)

def temporary_deferral_prompt(update: Update, context: CallbackContext) -> int:
  update.message.reply_text(
    "Here are some reasons why you may not be able to donate temporarily. Find out why:",
    reply_markup=subquestion_markup
  )

  return TEMP_DEF_PROMPT

find_out_keyboard = [["Let's do it!", "Nah"]]

find_out_markup = ReplyKeyboardMarkup(find_out_keyboard, one_time_keyboard=True)

continue_keyboard = [['Continue', 'Nah']]

continue_markup = ReplyKeyboardMarkup(continue_keyboard, one_time_keyboard=True)

subanswers = ['If you had COVID-19, please wait 28 days after clinical recovery. \nIf you have taken Pfizer-Biontech Vaccine:, \nNo side effects : wait 3 days after vaccination. \nSide effects exlcuding fever, muscle ache, joint pain & rash: wait 1 week after side effects are RESOLVED. \nSide effects such as fever, muscle ache, joint pain & rash: wait 4 weeks after side effects are RESOLVED.'
,'','Do NOT stop taking your medication.\nYou should not discontinue or stop taking medications prescribed or recommended by your physicians in order to donate blood.\nSome medications may affect your eligibility to donate blood. If the medication you are taking is not in this list or if you need further clarification, please call 6213 0626 and speak to our medical staff to determine if you are eligible to donate.\n\nPlease postphone your donation:\nAt least 1 days(24 hours) after:\n-Taking Antibiotics for Acne\n\nAt least 3 days after:\n-Taking Traditional Chinese Medicine\n-Asprin\n-Most prescription medication(excluding paracetamol, anti-histamines or sedatives)\n\nAt least 1 week after:\n-Taking antibiotics\n\nAt least 4 weeks after:\n-Isotretinoin\n\nFor Paracetamol/Panadol:\nYou may donate blood if you are taking paracetamol for pain relief (not for fever or flu), provided you are well on the day of the donation and do not experience any symptoms.'
,'If you have anxiety disorder, obsessive disorder or depression, you may be able to donate blood if you have been certified mentally fit for blood donation by your treating psychiatrist and you are well on the day of donation.\nIt is important that you are able to consent to the donation process and fully understand all the information and questions contained in the Donor Health Assessment Questionnaire and Declaration Form. This is a statutory declaration that carries legal responsibilities and implications.\nFor more information or if you need further clarification, please call 6213 0626 and speak to our medical staff.'
,'You should not donate blood for at least 12 months after the last sexual contact if:\nYou are a female donor who has engaged in sexual activity with a man whom you know, or suspect, to have had sex with another man.\nYou have engaged in sexual activity with someone whom you know, or suspect, to have AIDS or HIV.\nYou have paid for sex.\nYou have engaged in sexual activity with any of the following:\n-Someone whom you have known for 6 months or less.\n-More than one partner.\n-Someone diagnosed with syphilis, gonorrhoea or any other sexually transmitted diseases.\n\nNote: The term "sexual activity" means any of the activities below whether or not a condom or other protection was used:\n-Vaginal sex (contact between penis and vagina)\n-Oral sex (mouth or tongue on someone’s vagina, penis, or anus)\n-Anal sex (contact between penis and anus)'
,'If the vaccine or immunisation is not in this list, or if you need further clarification, please call 6213 0626 to determine if you are eligible to donate.\nAs long as you are well at the time of donation, there is no waiting period or deferral if you received the following vaccines:\nAnthrax\nCholera\nDiphtheria\nHepatitis A\nHPV (cervical cancer)\nInfluenza / Flu vaccine (by injection)\nMeningococcal\nPertussis\nPneumococcal\nPolio (by injection)\nRabies\nTetanus\nTyphoid (by injection)\n\nWait for at least 2 weeks if you received the Hepatitis B vaccine.\n\nWait for at least 4 weeks if you received the following vaccines:\nBCG\nChickenpox\nDengue\nGerman measles (rubella)\nInfluenza / Flu vaccine (by intranasal spray)\nMMR (measles, mumps, rubella)\nShingles (varicella zoster)\nYellow fever\n\nWait for at least 12 months if you received vaccines :\nHepatitis B immune globulin (post exposure)\nhuman rabies immunoglobulin (a component of rabies post-exposure vaccination)']

def answer(update: Update, context: CallbackContext) -> int:
  response = update.message.text

  if response == subquestion_keyboard[1][0]:
    update.message.reply_text(
      "Let's find out why",
      reply_markup=find_out_markup
    ) 
    return SICK_QUESTION
  else: 
    update.message.reply_text(
      subanswers[subquestions.index(response)] + "\n\n"
      'What do you want to find out next?',
      reply_markup = start_markup,
    )
  return START_MENU


sick_question_keyboard=  [["Chickenpox, Measles or Mumps"],
                     ["Cold, Flu and Sore Throat"],
                     ["Dengue Fever"], ["Diarrhoea"], ["Fever"]]

sick_question_markup = ReplyKeyboardMarkup(sick_question_keyboard, one_time_keyboard=True)

def sick_question(update: Update, context: CallbackContext) -> int:
  update.message.reply_text(
    "Oh no:( What were you sick with?",
    reply_markup=sick_question_markup
  )

  return CHOOSING_ILLNESS

illnesses = ["Chickenpox, Measles or Mumps", "Cold, Flu and Sore Throat","Dengue Fever", "Diarrhoea", "Fever"]

illness_explanatory = ['If you have chickenpox, rubella, measles or mumps, you can donate blood 4 weeks after full recovery.\nIf you had close contact with someone diagnosed to have chickenpox, measles, rubella or hand foot and mouth disease, you can donate 4 weeks after the date of last contact.',
'You should not donate blood if you have an upper respiratory tract infection, such as cold, flu, sore throat or any other symptoms of infection.\nYou should wait for 1 week after recovery, as it may be harmful to you and the recipients if you donate blood when you have an infection. If you also have fever, the waiting period is 4 weeks.',
'If you have dengue fever, you can donate blood 6 months after full recovery. If a household member has recently been diagnosed with dengue fever and you live in a dengue hotstpot identified by MOH, you should wait 4 weeks before donating blood.',
'You should wait for 1 week after recovery, as it may be harmful to you and the recipients if you donate blood when you are ill or have an infection.',
'You should not donate if you are having fever.\nYou should wait for 4 weeks after recovery, as it may be harmful to you and the recipients if you donate blood when you are ill or have an infection.']

def display_illness(update: Update, context: CallbackContext) -> int:
  response = update.message.text
  update.message.reply_text(
    illness_explanatory[illnesses.index(response)] + "\n\n"
    'Do you want to find out more about other illnesses?',
    reply_markup=find_out_markup,
  )
  return SICK_QUESTION

def bye(update: Update, context: CallbackContext) -> int:
  update.message.reply_text(
    "Yeet"
  )
  return ConversationHandler.END  