import telebot
import os
import subprocess
from telebot import types

# REMPLACE PAR TON TOKEN
API_TOKEN = '7959982217:AAHC-_xTJiUaxTPw6cA-5i0seorI19-2sGo'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "<b>Envoyez-moi une vidéo pour voir les options !</b>", parse_mode="HTML")

@bot.message_handler(content_types=['video', 'document'])
def handle_video(message):
    # On récupère l'ID du fichier (vidéo ou document)
    file_id = message.video.file_id if message.video else message.document.file_id
    
    # Création de la grille comme sur ta photo
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    buttons = [
        types.InlineKeyboardButton("🖼 Thumbnail Extractor", callback_data=f"thumb_{file_id}"),
        types.InlineKeyboardButton("📝 Caption Editor", callback_data=f"caption_{file_id}"),
        types.InlineKeyboardButton("🎬 Metadata Editor", callback_data=f"meta_{file_id}"),
        types.InlineKeyboardButton("🎥 Stream Mapper", callback_data=f"map_{file_id}"),
        types.InlineKeyboardButton("✂️ Video Trimmer", callback_data=f"trim_{file_id}"),
        types.InlineKeyboardButton("🎵 Video To Audio", callback_data=f"toaudio_{file_id}"),
        types.InlineKeyboardButton("🚀 Video Optimizer", callback_data=f"opt_{file_id}"),
        types.InlineKeyboardButton("🎬 Video Converter", callback_data=f"conv_{file_id}"),
        types.InlineKeyboardButton("ℹ️ Media Info", callback_data=f"info_{file_id}")
    ]
    
    markup.add(*buttons)
    cancel = types.InlineKeyboardButton("Cancel ❌", callback_data="cancel")
    markup.row(cancel)
    
    bot.reply_to(message, "<b>Please choose your desired action below 👇</b>", 
                 parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def process_callback(call):
    if call.data == "cancel":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        return

    # On sépare l'action et l'ID du fichier
    data = call.data.split('_')
    action = data[0]
    file_id = data[1]

    if action == "opt":
        bot.answer_callback_query(call.id, "Optimisation lancée...")
        # (Logique FFmpeg ici comme vu précédemment)
    elif action == "conv":
        bot.answer_callback_query(call.id, "Conversion lancée...")
    else:
        bot.answer_callback_query(call.id, f"L'action {action} arrive bientôt !")

bot.polling()

