import telebot
from telebot import types

# REMPLACE PAR TON TOKEN
API_TOKEN = '7959982217:AAHC-_xTJiUaxTPw6cA-5i0seorI19-2sGo'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # On crée les boutons comme sur ta photo
    buttons = [
        types.InlineKeyboardButton("🖼 Thumbnail Extractor", callback_data="thumb"),
        types.InlineKeyboardButton("📝 Caption & Buttons Editor", callback_data="caption"),
        types.InlineKeyboardButton("🎬 Metadata Editor", callback_data="metadata"),
        types.InlineKeyboardButton("🎥 Stream Mapper", callback_data="stream_map"),
        types.InlineKeyboardButton("🎵 Stream Extractor", callback_data="stream_ext"),
        types.InlineKeyboardButton("✂️ Video Trimmer", callback_data="trim"),
        types.InlineKeyboardButton("➕ Video Merger", callback_data="merge"),
        types.InlineKeyboardButton("🎵 Video To Audio", callback_data="to_audio"),
        types.InlineKeyboardButton("🚀 Video Optimizer", callback_data="optimize"),
        types.InlineKeyboardButton("📁 Create Archive", callback_data="archive")
    ]
    
    markup.add(*buttons)
    # Bouton Annuler en rouge
    cancel = types.InlineKeyboardButton("Cancel ❌", callback_data="cancel")
    markup.row(cancel)
    
    bot.send_message(message.chat.id, "<b>Please choose your desired action below 👇</b>", 
                     parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cancel":
        bot.delete_message(call.message.chat.id, call.message.message_id)
    else:
        bot.answer_callback_query(call.id, f"Fonction {call.data} bientôt disponible !")

print("Le bot est lancé...")
bot.polling()
