import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from telegram import Update
import os

# === Token del bot desde variable de entorno ===
TOKEN = os.getenv("TOKEN")

# === Acceso a Google Sheets ===
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Bot clientes Fox").sheet1
telefonos = [str(x) for x in sheet.col_values(2)[1:]]

# === Respuesta del bot ===
def responder(update: Update, context: CallbackContext):
    texto = update.message.text.strip()
    chat_id = update.effective_chat.id

    if texto.lower() == "hola":
        context.bot.send_message(chat_id=chat_id, text="👋 ¡Hola! Escribe tu número de teléfono para validar acceso.")
    elif texto in telefonos:
        context.bot.send_message(chat_id=chat_id, text="✅ Número verificado. ¡Bienvenido!")
    else:
        context.bot.send_message(chat_id=chat_id, text="❌ Número no reconocido. Contacta con soporte.")

# === Iniciar bot ===
updater = Updater(token=TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, responder))

print("✅ Bot activo y esperando mensajes...")
updater.start_polling()
updater.idle()
