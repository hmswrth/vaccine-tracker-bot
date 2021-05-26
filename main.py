from telegram import *
import constants as key
from telegram.ext import *
from datetime import date
import requests
import json


def vaccine(city):
    city_codes = {'1': '581', '2': '18', '3': '13', '4': '5'}
    today = date.today()
    d = today.strftime('%d-%m-%y')

    url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={city_codes[city]}&date={d}'
    browser_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    print(url)
    response = requests.get(url, headers=browser_header)
    print(response)
    json_data = response.json()
    final_text = ''
    if len(json_data['sessions']) == 0:
       final_text = 'Slots not available'
    else:
       for slots in json_data['sessions']:
          final_text = final_text + "\nName: "+str(slots['name']) + '\n' + "Available Capacity: "+str(slots['available_capacity']) + '\n' + "Min Age Limit: "+str(slots['min_age_limit']) + '\n' + "Vaccine: "+str(slots['vaccine']) + '\n'
          final_text = final_text + '----------------------------------------'
    return final_text


def start(update, context):
    update.message.reply_text(
        'Hi there! I can help you in searching for vaccine availability')

    keyboard = [
        [
            InlineKeyboardButton("Hyderabad", callback_data='1'),
            InlineKeyboardButton("Vizag", callback_data='2'),
        ],
        [
            InlineKeyboardButton("Nellore", callback_data='3'),
            InlineKeyboardButton("Guntur", callback_data='4'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        'Please choose a city to begin:', reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query
    query.answer()

    cities = {'1': "Hyderabad", '2': "Vizag", '3': "Nellore", '4': "Guntur"}
    query.edit_message_text(
        text="Selected city: {}".format(cities[query.data]))

    res = vaccine(query.data)

   #  query.edit_message_text(text=res)

    if len(res) > 4096:
       for x in range(0, len(res), 4096):
          query.edit_message_text(text = res[x:x+4096])
    else:
       query.edit_message_text(text = res)


def main():

    bot = Bot(token=key.API_KEY)
    print(bot.get_me())

    updater = Updater(token=key.API_KEY, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()


main()
