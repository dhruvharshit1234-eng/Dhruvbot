import random
import string
import requests
import phonenumbers

from phonenumbers import (
    geocoder,
    carrier,
    timezone,
)

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)

# ================= CONFIG ================= #

TOKEN = "8768832791:AAGU6gWjgHfELni0-EbcgWIrfi5lF4H5ulI"

ADMINS = [
    8602292776,
    8602292776
]

FORCE_CHANNEL = "jiodhruv"

OWNER_USERNAME = "DHRUVSNIFINDER"

LOG_CHANNEL = -1001234567890

API_KEY = "paid-key-by-ft-and-bronx"

# ================= DATABASE (NO MONGODB) ================= #

users_db = []

premium_db = []

keys_db = []

ban_db = []

broadcast_mode = {}

# ================= SAVE USER ================= #

def save_user(user_id):

    if user_id not in users_db:

        users_db.append(user_id)

# ================= FORCE JOIN ================= #

async def force_join(bot, user_id):

    try:

        member = await bot.get_chat_member(
            f"@{FORCE_CHANNEL}",
            user_id
        )

        return member.status in [
            "member",
            "administrator",
            "creator"
        ]

    except:

        return False

# ================= KEYBOARD ================= #

from telegram import ReplyKeyboardMarkup

# ================= START ================= #

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    save_user(user.id)

    keyboard = [

        ["📞 INFO", "💎 REDEEM"],

        ["👑 PANEL", "📊 STATUS"],

        ["ℹ️ HELP"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    text = f"""
╔══════════════════╗
      PREMIUM INFO BOT
╚══════════════════╝

👤 User : {user.first_name}

📱 Send Any Number To Get Info
"""

    await update.message.reply_text(
        text,
        reply_markup=reply_markup
    )

# ================= BUTTON COMMANDS ================= #

async def keyboard_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    user = update.effective_user

    # ===== HELP ===== #

    if text == "ℹ️ HELP":

        msg = """
╔═══〔 📚 COMMANDS 〕═══╗

/start - Start Bot

/panel - Admin Panel

/redeem KEY - Redeem Premium

/ban USER_ID - Ban User

/unban USER_ID - Unban User

━━━━━━━━━━━━━━
👑 OWNER : @Amarstarx
"""

        await update.message.reply_text(msg)

        return

    # ===== STATUS ===== #

    elif text == "📊 STATUS":

        premium = "YES" if user.id in premium_db else "NO"

        msg = f"""
╔═══〔 👤 STATUS 〕═══╗

🆔 ID : {user.id}

💎 Premium : {premium}

🚫 Banned : {"YES" if user.id in ban_db else "NO"}

━━━━━━━━━━━━━━
⚡ BY GM TUSHAR
"""

        await update.message.reply_text(msg)

        return

    # ===== PANEL ===== #

    elif text == "👑 PANEL":

        if user.id not in ADMINS:

            await update.message.reply_text(
                "❌ Admin Only"
            )

            return

        await panel(update, context)

        return

    # ===== REDEEM ===== #

    elif text == "💎 REDEEM":

        await update.message.reply_text(
            "Use:\n/redeem KEY"
        )

        return

    # ===== INFO ===== #

    elif text == "📞 INFO":

        await update.message.reply_text(
            "📱 Send Any Number"
        )

        return

    # ===== BAN CHECK ===== #

    if user.id in ban_db:
        return

    number = update.message.text.strip()

    try:

        # ===== PHONENUMBERS ===== #

        parsed = phonenumbers.parse(number)

        valid = phonenumbers.is_valid_number(parsed)

        country = geocoder.description_for_number(
            parsed,
            "en"
        )

        sim = carrier.name_for_number(
            parsed,
            "en"
        )

        tz = ", ".join(
            timezone.time_zones_for_number(parsed)
        )

        international = phonenumbers.format_number(
            parsed,
            phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )

        # ===== API ===== #

        url = f"https://ft-osint-api.duckdns.org/api/number?key={API_KEY}&num={number}"

        response = requests.get(url)

        data = response.json()

        print("API RESPONSE =", data)

        # ===== RESULTS ===== #

        results = data.get("results", [])

        if len(results) > 0:

            api_data = results[0]

        else:

            api_data = {}

        # ===== GET VALUES ===== #

        name = api_data.get(
            "name",
            "Not Found"
        )

        email = api_data.get(
            "email",
            "Not Found"
        )

        region = api_data.get(
            "circle",
            "Not Found"
        )

        address = api_data.get(
            "address",
            "Not Found"
        )

        father = api_data.get(
            "fname",
            "Not Found"
        )

        truecaller = api_data.get(
            "truecaller_name",
            "Not Found"
        )

        # ===== RESULT FORMAT ===== #

        result = f"""
╔═══〔 📞 NUMBER INTEL 〕═══╗
📱 Number: {number}
"""

        if len(results) == 0:

            result += """

❌ No Records Found
"""

        else:

            for i, x in enumerate(results, start=1):

                result += f"""

🔴 RECORD {i}

👤 Name     : {x.get("name", "N/A")}

👨 Father   : {x.get("fname", "N/A")}

📍 Address  : {x.get("address", "N/A")}

📡 Circle   : {x.get("circle", "N/A")}

☎️ Alt      : {x.get("alt", "N/A")}

🆔 Aadhar   : {x.get("id", "N/A")}

✉️ Email    : {x.get("email", "N/A")}
"""

        result += """

━━━━━━━━━━━━━━
👑 Owner : @Amarstarx
⚡ Status: ACTIVE
"""

        await update.message.reply_text(result)

        await update.message.reply_text(result)

        # ===== LOG ===== #

        try:

            await context.bot.send_message(
                LOG_CHANNEL,
                f"📢 {user.id} searched {number}"
            )

        except:
            pass

    except Exception as e:

        await update.message.reply_text(
            f"❌ Error\n\n{e}"
        )

# ================= PANEL ================= #

async def panel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id not in ADMINS:
        return

    buttons = [

        [
            InlineKeyboardButton(
                "📊 Stats",
                callback_data="stats"
            ),

            InlineKeyboardButton(
                "📢 Broadcast",
                callback_data="broadcast"
            )
        ],

        [
            InlineKeyboardButton(
                "🔑 Generate Key",
                callback_data="genkey"
            ),

            InlineKeyboardButton(
                "👥 Users",
                callback_data="users"
            )
        ],

        [
            InlineKeyboardButton(
                "🚫 Ban",
                callback_data="ban"
            ),

            InlineKeyboardButton(
                "✅ Unban",
                callback_data="unban"
            )
        ]
    ]

    await update.message.reply_text(
        "⚡ ADMIN PANEL",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ================= BUTTONS ================= #

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    data = query.data

    user_id = query.from_user.id

    # ===== STATS ===== #

    if data == "stats":

        text = f"""
📊 BOT STATS

👥 Users : {len(users_db)}
💎 Premium : {len(premium_db)}
🚫 Banned : {len(ban_db)}
"""

        await query.message.reply_text(text)

    # ===== USERS ===== #

    elif data == "users":

        await query.message.reply_text(
            f"👥 Total Users : {len(users_db)}"
        )

    # ===== GENKEY ===== #

    elif data == "genkey":

        key = "GM-" + ''.join(
            random.choices(
                string.ascii_uppercase +
                string.digits,
                k=10
            )
        )

        keys_db.append(key)

        await query.message.reply_text(
            f"🔑 Generated Key\n\n{key}"
        )

    # ===== BROADCAST ===== #

    elif data == "broadcast":

        broadcast_mode[user_id] = True

        await query.message.reply_text(
            "📢 Send Broadcast Message"
        )

    # ===== BAN ===== #

    elif data == "ban":

        await query.message.reply_text(
            "/ban USER_ID"
        )

    # ===== UNBAN ===== #

    elif data == "unban":

        await query.message.reply_text(
            "/unban USER_ID"
        )

# ================= REDEEM ================= #

async def redeem(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    if not context.args:

        await update.message.reply_text(
            "/redeem KEY"
        )

        return

    key = context.args[0]

    if key not in keys_db:

        await update.message.reply_text(
            "❌ Invalid Key"
        )

        return

    if user.id not in premium_db:

        premium_db.append(user.id)

    keys_db.remove(key)

    await update.message.reply_text(
        "💎 Premium Activated"
    )

# ================= BAN ================= #

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id not in ADMINS:
        return

    if not context.args:
        return

    user_id = int(context.args[0])

    if user_id not in ban_db:

        ban_db.append(user_id)

    await update.message.reply_text(
        "🚫 User Banned"
    )

# ================= UNBAN ================= #

async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id not in ADMINS:
        return

    if not context.args:
        return

    user_id = int(context.args[0])

    if user_id in ban_db:

        ban_db.remove(user_id)

    await update.message.reply_text(
        "✅ User Unbanned"
    )

# ================= INFO ================= #

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    if user.id in ban_db:
        return

    number = update.message.text.strip()

    if not number.replace("+", "").isdigit():
        return

    try:

        parsed = phonenumbers.parse(number)

        valid = phonenumbers.is_valid_number(parsed)

        country = geocoder.description_for_number(
            parsed,
            "en"
        )

        sim = carrier.name_for_number(
            parsed,
            "en"
        )

        tz = ", ".join(
            timezone.time_zones_for_number(parsed)
        )

        url = f"https://ft-osint-api.duckdns.org/api/number?key={API_KEY}&num={number}"

        response = requests.get(url)

        data = response.json()

        results = data.get("results", [])

        result = f"""
╔═══〔 📞 NUMBER INTEL 〕═══╗
📱 Number: {number}

🌍 Country : {country}
📡 Carrier : {sim}
🕒 Timezone : {tz}
✅ Valid : {valid}
"""

        if len(results) == 0:

            result += """

❌ No Records Found
"""

        else:

            for i, x in enumerate(results, start=1):

                result += f"""

🔴 RECORD {i}

👤 Name     : {x.get("name", "N/A")}

👨 Father   : {x.get("fname", "N/A")}

📍 Address  : {x.get("address", "N/A")}

📡 Circle   : {x.get("circle", "N/A")}

☎️ Alt      : {x.get("alt", "N/A")}

🆔 Aadhar   : {x.get("id", "N/A")}

✉️ Email    : {x.get("email", "N/A")}
"""

        result += """

━━━━━━━━━━━━━━
👑 Owner : @Amarstarx
⚡ Status: ACTIVE
"""

        await update.message.reply_text(result)

    except Exception as e:

        await update.message.reply_text(
            f"❌ Error\n\n{e}"
        )

# ================= MAIN ================= #

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("panel", panel))
app.add_handler(CommandHandler("redeem", redeem))
app.add_handler(CommandHandler("ban", ban))
app.add_handler(CommandHandler("unban", unban))

app.add_handler(
    CallbackQueryHandler(buttons)
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        keyboard_handler
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        info
    )
)

print("BOT RUNNING...")
app.run_polling()