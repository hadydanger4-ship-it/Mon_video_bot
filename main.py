import telebot
import os
import subprocess
from telebot import types

# REMPLACE PAR TON VRAI TOKEN TELEGRAM
API_TOKEN = '7959982217:AAHC-_xTJiUaxTPw6cA-5i0seorI19-2sGo'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "<b>👋 Envoyez-moi une vidéo pour afficher les options !</b>", parse_mode="HTML")

@bot.message_handler(content_types=['video', 'document'])
def handle_video(message):
    # Récupération de l'ID du fichier
    file_id = message.video.file_id if message.video else message.document.file_id
    
    # Création de la grille (2 colonnes)
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    buttons = [
        types.InlineKeyboardButton("🖼 Thumbnail Extractor", callback_data=f"thumb_{file_id}"),
        types.InlineKeyboardButton("✂️ Video Trimmer", callback_data=f"trim_{file_id}"),
        types.InlineKeyboardButton("🎵 Video To Audio", callback_data=f"toaudio_{file_id}"),
        types.InlineKeyboardButton("🚀 Video Optimizer", callback_data=f"opt_{file_id}"),
        types.InlineKeyboardButton("🎬 Video Converter", callback_data=f"conv_{file_id}"),
        types.InlineKeyboardButton("ℹ️ Media Info", callback_data=f"info_{file_id}")
    ]
    
    markup.add(*buttons)
    markup.row(types.InlineKeyboardButton("Cancel ❌", callback_data="cancel"))
    
    bot.reply_to(message, "<b>Please choose your desired action below 👇</b>", 
                 parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def process_callback(call):
    if call.data == "cancel":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        return

    action, file_id = call.data.split('_')
    chat_id = call.message.chat.id
    
    status_msg = bot.send_message(chat_id, "⏳ Téléchargement et traitement en cours...")

    # 1. Télécharger le fichier
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    input_n = "input_file.mp4"
    output_n = "output_result.mp4"

    with open(input_n, 'wb') as f:
        f.write(downloaded_file)

    # 2. Exécuter l'action demandée
    if action == "opt":
        # Compression (Optimizer)
        cmd = f"ffmpeg -i {input_n} -vcodec libx264 -crf 28 -preset faster {output_n} -y"
    elif action == "conv":
        # Conversion en .mkv
        output_n = "output_result.mkv"
        cmd = f"ffmpeg -i {input_n} -vcodec copy -acodec copy {output_n} -y"
    elif action == "toaudio":
        # Extraction Audio
        output_n = "audio.mp3"
        cmd = f"ffmpeg -i {input_n} -vn -acodec libmp3lame {output_n} -y"
    else:
        bot.edit_message_text("Cette fonction sera codée bientôt !", chat_id, status_msg.message_id)
        return

    subprocess.run(cmd, shell=True)

    # 3. Envoyer le résultat
    with open(output_n, 'rb') as result:
        if action == "toaudio":
            bot.send_audio(chat_id, result)
        else:
            bot.send_video(chat_id, result, caption="✅ Traitement terminé !")

    # Nettoyage
    bot.delete_message(chat_id, status_msg.message_id)
    if os.path.exists(input_n): os.remove(input_n)
    if os.path.exists(output_n): os.remove(output_n)

bot.polling()

