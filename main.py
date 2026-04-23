import os
import logging
from dotenv import load_dotenv
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# .env faylidagi o'zgaruvchilarni yuklash
load_dotenv()

# Loglarni sozlash (bot ishlayotganini terminalda ko'rish uchun)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Salom {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Yordam kerakmi?")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)

def main() -> None:
    # Tokenni .env fayldan olish
    token = os.getenv("TOKEN")

    # Agarda token topilmasa, botni to'xtatish
    if not token:
        print("XATOLIK: .env fayli ichida TOKEN topilmadi yoki fayl noto'g'ri yaratilgan!")
        return

    # Botni yaratish
    application = Application.builder().token(token).build()

    # Buyruqlarni ro'yxatga olish
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Xabarlarga javob berish (Echo)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Botni yurgizish
    print("Bot ishga tushdi...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

# DIQQAT: Mana bu qismda __ belgilariga e'tibor bering
if __name__ == "__main__":
    main()