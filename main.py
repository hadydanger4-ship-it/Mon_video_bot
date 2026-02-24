import telebot
import os
import subprocess
from telebot import types

API_TOKEN = '7959982217:AAHC-_xTJiUaxTPw6cA-5i0seorI19-2sGo'
bot = telebot.TeleBot(API_TOKEN)

# Dossier temporaire pour les vidéos
if not os.path.exists('downloads'):
    os.makedirs('downloads')

@bot.message_handler(content_types=['video'])
def handle_video(message):
    bot.reply_to(message, "✅ Vidéo reçue ! Choisis une action :", reply_markup=main_menu())

def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btns = [
        types.InlineKeyboardButton("🚀 Video Optimizer", callback_data="optimize"),
        types.InlineKeyboardButton("🎬 Video Converter", callback_data="convert")
    ]
    markup.add(*btns)
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    
    if call.data == "optimize":
        bot.send_message(chat_id, "⏳ Optimisation en cours (réduction de taille)...")
        # Ici on ajoute la logique FFmpeg pour compresser
        # Exemple : ffmpeg -i input.mp4 -vcodec libx264 -crf 28 output.mp4
        bot.answer_callback_query(call.id, "Traitement lancé !")
        
    elif call.data == "convert":
        bot.send_message(chat_id, "⏳ Conversion en cours...")
        bot.answer_callback_query(call.id, "Traitement lancé !")

bot.polling()

