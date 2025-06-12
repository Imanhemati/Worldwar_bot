
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

BOT_TOKEN = "توکن_ربات_اینجا"

players = {}
CHOOSING_COUNTRY = 1

countries = ["🇩🇪 آلمان", "🇯🇵 ژاپن", "🇺🇸 آمریکا", "🇫🇷 فرانسه", "🇷🇺 روسیه", "🇨🇳 چین", "🇬🇧 بریتانیا", "🇮🇳 هند", "🇧🇷 برزیل", "🇨🇦 کانادا"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎖️ سلام فرمانده! به ربات جنگ جهانی سوم خوش اومدی.")

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in players:
        await update.message.reply_text("⚠️ شما قبلاً ثبت‌نام کرده‌اید.")
        return ConversationHandler.END

    markup = ReplyKeyboardMarkup([[c] for c in countries], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("🌍 لطفاً کشور مورد نظر خود را انتخاب کنید:", reply_markup=markup)
    return CHOOSING_COUNTRY

async def country_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    country = update.message.text
    if country not in countries:
        await update.message.reply_text("❌ کشور نامعتبره. لطفاً از لیست انتخاب کن.")
        return CHOOSING_COUNTRY

    players[user_id] = {
        "username": update.effective_user.username or "ناشناس",
        "country": country,
        "resources": 1_000_000
    }

    await update.message.reply_text(f"✅ ثبت‌نام کامل شد!
🇨🇴 کشور: {country}
💰 ارک: 1,000,000", reply_markup=None)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ ثبت‌نام لغو شد.")
    return ConversationHandler.END

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in players:
        await update.message.reply_text("❌ شما هنوز ثبت‌نام نکرده‌اید. لطفاً با /register ثبت‌نام کنید.")
        return
    player = players[user_id]
    username = player["username"]
    country = player["country"]
    resources = player["resources"]
    await update.message.reply_text(
        f"🧾 پروفایل شما:
"
        f"👤 نام کاربری: @{username}
"
        f"🌍 کشور: {country}
"
        f"💰 ارک: {resources:,}"
    )

async def camp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in players:
        await update.message.reply_text("❌ هنوز ثبت‌نام نکردی! با /register شروع کن.")
        return
    await update.message.reply_text(
        "🏕️ اردوگاه فرمانده:
"
        "🪖 ساخت ارتش
"
        "💰 استخراج منابع
"
        "⬆️ ارتقاء سطح

"
        "🔧 (به‌زودی قابلیت‌های کامل فعال می‌شن...)"
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
