# bot/handlers.py (Final Robust Version)

import logging
import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logger = logging.getLogger(__name__)

# --- Get Environment Variable ---
WEB_APP_URL = os.getenv("WEBHOOK_URL")


# --- 1. Defensively Create the Keyboard Layout ---
# This new code checks if the URL exists before creating the button.
keyboard_layout = []

if WEB_APP_URL:
    # If the URL is found, create the real Web App button
    logger.info(f"Successfully found WEBHOOK_URL. Creating Web App button.")
    web_app_info = WebAppInfo(url=f"{WEB_APP_URL}/lobby/index.html")
    keyboard_layout.append(
        [KeyboardButton("Play Ludo Games 🎮", web_app=web_app_info)]
    )
else:
    # If the URL is MISSING, create a simple text button as a fallback.
    # This prevents the application from crashing.
    logger.error("CRITICAL ERROR: WEBHOOK_URL environment variable not found!")
    keyboard_layout.append(
        [KeyboardButton("Play 🎮 (Error: URL not configured)")]
    )

# Add the rest of the buttons to the layout
keyboard_layout.extend([
    [KeyboardButton("My Wallet 💰"), KeyboardButton("Support 📞")]
])

# Create the final keyboard object
REPLY_MARKUP = ReplyKeyboardMarkup(keyboard_layout, resize_keyboard=True)


# --- 2. Define Command Handlers (No other changes needed) ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays the main menu keyboard."""
    await update.message.reply_text(
        "Welcome to Yeab Game Zone! Tap below to see open games or manage your account.", 
        reply_markup=REPLY_MARKUP
    )

async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles data sent back from the Web App (e.g., when a user clicks 'Join')."""
    data_str = update.effective_message.web_app_data.data
    logger.info(f"Received data from Web App: {data_str}")
    
    if data_str.startswith("join_game_"):
        game_id = data_str.split('_')[-1]
        await update.message.reply_text(f"You are attempting to join game #{game_id}. Please wait...")
        # TODO: Add the full logic to join the game.

def setup_handlers(ptb_app: Application) -> Application:
    """Attaches all handlers."""
    ptb_app.add_handler(CommandHandler("start", start_command))
    ptb_app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))
    return ptb_app