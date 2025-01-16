import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.helpers import escape_markdown

BOT_TOKEN = "7311258512:AAHyNQX3QHsHAFh5uIx-ERsCVcK7_WIKwqM"
BOT_OWNER = "@Bhaiya_chips"

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) != 1 or not context.args[0].isdigit():
            await update.message.reply_text(
                escape_markdown(
                    "❌ *Usage*: /check {uid}\n✅ *Example*: /check 123456789",
                    version=2
                ),
                parse_mode="MarkdownV2"
            )
            return

        uid = context.args[0]
        api_url = f"https://amin-belara-api.vercel.app/check_banned?player_id={uid}"

        response = requests.get(api_url)
        response.raise_for_status()
        response_data = response.json()

        if "status" in response_data:
            player_id = response_data.get("player_id", "Unknown")
            player_name = response_data.get("player_name", "Unknown")
            region = response_data.get("region", "Unknown")
            status = response_data.get("status", "Unknown")

            account_status = "🟢 *Not Banned*" if status == "NOT BANNED" else "🔴 *Banned*"

            message = (
                f"👤 *Owner*: {BOT_OWNER}\n"
                f"📌 *UID*: {player_id}\n"                
                f"🛡️ *Status*: {account_status}"
            )
            escaped_message = escape_markdown(message, version=2)
            await update.message.reply_text(escaped_message, parse_mode="MarkdownV2")
        else:
            await update.message.reply_text(
                escape_markdown("⚠️ Unable to retrieve ban status. Please try again later.", version=2),
                parse_mode="MarkdownV2"
            )
    except requests.exceptions.RequestException as e:
        await update.message.reply_text(
            escape_markdown(f"🚨 *Error*: API request failed: {str(e)}", version=2),
            parse_mode="MarkdownV2"
        )
    except Exception as e:
        await update.message.reply_text(
            escape_markdown(f"🚨 *Error*: {str(e)}", version=2),
            parse_mode="MarkdownV2"
        )

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("check", check))
    print("🚀 Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
