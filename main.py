from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

BOT_TOKEN = "7864349018:AAFgaHF8MZ6VOQ4Kq0jcZmQqKSDMNCB-WtY" 

players = {}
CHOOSING_COUNTRY = 1

countries = ["🇩🇪 آلمان", "🇯🇵 ژاپن", "🇺🇸 آمریکا", "🇫🇷 فرانسه"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❗️لطفا برای شروع /register را بزنید.")

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in players:
        await update.message.reply_text("✅ شما قبلاً ثبت‌نام کرده‌اید.")
        return ConversationHandler.END

    markup = ReplyKeyboardMarkup([[c] for c in countries], resize_keyboard=True)
    await update.message.reply_text("🌍 یک کشور انتخاب کنید:", reply_markup=markup)
    return CHOOSING_COUNTRY

async def country_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    country = update.message.text
    if country not in countries:
        await update.message.reply_text("❌ کشور نامعتبر است.")
        return CHOOSING_COUNTRY

    players[user_id] = {
        "username": update.effective_user.username or "بی‌نام",
        "country": country,
        "resources": 1_000_000
    }

    await update.message.reply_text(f"✅ ثبت‌نام شدید!\n🌍 کشور: {country}\n💰 منابع: 1,000,000", reply_markup=None)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ عملیات لغو شد.")
    return ConversationHandler.END

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in players:
        await update.message.reply_text("❌ شما ثبت‌نام نکرده‌اید!")
        return

    player = players[user_id]
    username = player["username"]
    country = player["country"]
    resources = player["resources"]

    await update.message.reply_text(
        f"📋 اطلاعات پروفایل:\n"
        f"👤 نام کاربری: @{username}\n"
        f"🌍 کشور: {country}\n"
        f"💰 منابع: {resources:,}"
    )

async def camp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in players:
        await update.message.reply_text("❌ شما ثبت‌نام نکرده‌اید!")
        return

    await update.message.reply_text(
        "🍢 اردوگاه آماده‌سازی:\n"
        "🪖 تمرینات نظامی\n"
        "💰 ارتقاء منابع\n"
        "⬆️ افزایش قدرت\n"
        "🛠 ارتقاء تجهیزات..."
    )

app = ApplicationBuilder().token(BOT_TOKEN).build()

register_handler = ConversationHandler(
    entry_points=[CommandHandler("register", register)],
    states={CHOOSING_COUNTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, country_chosen)]},
    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(CommandHandler("start", start))
app.add_handler(register_handler)
app.add_handler(CommandHandler("profile", profile))
app.add_handler(CommandHandler("camp", camp))

app.run_polling()
