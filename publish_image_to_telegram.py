import telegram
from dotenv import load_dotenv
from os import environ

load_dotenv()
chat_id = environ.get('CHAT_ID')

bot = telegram.Bot(token=environ.get('BOT_TOKEN'))
print(bot.get_me())
# bot.send_message(chat_id=chat_id, text='Hi there!?')
bot.send_photo(photo=open('images/epic/epic_2.png', 'rb'), chat_id=chat_id)