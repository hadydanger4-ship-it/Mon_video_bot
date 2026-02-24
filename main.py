import telebot
import os
import subprocess
from telebot import types

API_TOKEN = '7959982217:AAHC-_xTJiUaxTPw6cA-5i0seorI19-2sGo'
bot = telebot.TeleBot(API_TOKEN)

# On stocke l'ID de la dernière vidéo ici
last_video_id = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "👋 Envoyez-moi une vidéo !")

@bot.message_handler(content_types=['video', 'document'])
def handle_video(message):
    file_id = None
    if message.video:
        file_id = message.video.file_id
    elif message.document and message.document.mime_type.startswith('video'):
        file_id = message.document.file_id

    if file_id:
        # On enregistre l'ID pour cet utilisateur
        last_video_id[message.chat.id] = file_id
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        btns = [
            types.InlineKeyboardButton("🚀 Optimizer", callback_data="opt"),
            types.InlineKeyboardButton("🎬 Converter", callback_data="conv"),
            types.InlineKeyboardButton("🎵 Audio", callback_data="audio")
        ]
        markup.add(*btns)
        bot.reply_to(message, "<b>Choisissez une action :</b>", parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    if chat_id not in last_video_id:
        bot.answer_callback_query(call.id, "Erreur : Renvoyez la vidéo.")
        return

    file_id = last_video_id[chat_id]
    action = call.data
    
    bot.edit_message_text("⏳ Traitement lancé... Patientez.", chat_id, call.message.message_id)

    # Téléchargement
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    input_p = "input.mp4"
    output_p = "output.mp4"

    with open(input_p, 'wb') as f:
        f.write(downloaded_file)

    if action == "opt":
        cmd = f"ffmpeg -i {input_p} -vcodec libx264 -crf 28 {output_p} -y"
    elif action == "conv":
        output_p = "output.mkv"
        cmd = f"ffmpeg -i {input_p} -vcodec copy {output_p} -y"
    elif action == "audio":
        output_p = "audio.mp3"
        cmd = f"ffmpeg -i {input_p} -vn {output_p} -y"

    subprocess.run(cmd, shell=True)

    with open(output_p, 'rb') as f:
        if action == "audio":
            bot.send_audio(chat_id, f)
        else:
            bot.send_video(chat_id, f)

    os.remove(input_p)
    os.remove(output_p)

bot.polling()

