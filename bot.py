from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests

TOKEN = "MASUKKAN_TOKEN_KAMU_DI_SINI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💱 Wann Currency Bot\n\n"
        "Perintah:\n"
        "/rates usd\n"
        "/rates idr\n"
        "/convert 10 usd idr\n"
        "/convert 50000 idr usd\n"
        "/help"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 Cara Pakai\n\n"
        "/rates usd\n"
        "Menampilkan kurs USD ke banyak mata uang.\n\n"
        "/convert 10 usd idr\n"
        "Mengubah USD ke IDR.\n\n"
        "/convert 50000 idr usd\n"
        "Mengubah IDR ke USD."
    )

async def rates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 1:
        await update.message.reply_text("Contoh:\n/rates usd")
        return

    base = context.args[0].upper()

    try:
        url = f"https://api.frankfurter.app/latest?from={base}"
        data = requests.get(url).json()

        if "rates" not in data:
            await update.message.reply_text("Kode mata uang tidak valid.")
            return

        text = f"💱 Kurs {base}\n\n"

        count = 0
        for currency, rate in data["rates"].items():
            text += f"{currency}: {rate}\n"
            count += 1

            if count >= 30:
                break

        await update.message.reply_text(text)

    except:
        await update.message.reply_text("Gagal mengambil data.")

async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) < 3:
        await update.message.reply_text(
            "Contoh:\n/convert 10 usd idr"
        )
        return

    try:
        amount = float(context.args[0])
        from_currency = context.args[1].upper()
        to_currency = context.args[2].upper()

        url = (
            f"https://api.frankfurter.app/latest"
            f"?amount={amount}"
            f"&from={from_currency}"
            f"&to={to_currency}"
        )

        data = requests.get(url).json()

        if "rates" not in data:
            await update.message.reply_text("Kode mata uang tidak valid.")
            return

        result = data["rates"][to_currency]

        await update.message.reply_text(
            f"💸 Hasil Konversi\n\n"
            f"{amount} {from_currency}\n"
            f"= {result} {to_currency}"
        )

    except:
        await update.message.reply_text(
            "Format salah.\nContoh:\n/convert 10 usd idr"
        )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💱 Wann Currency Bot v1.0\n"
        "Made by Wann 🚀"
    )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("rates", rates))
app.add_handler(CommandHandler("convert", convert))
app.add_handler(CommandHandler("about", about))

print("Bot berjalan...")

app.run_polling()
