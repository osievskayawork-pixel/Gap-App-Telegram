"""
A simple Telegram bot that launches a mini‑app to track shipping containers.

When a user sends `/start`, the bot replies with a message containing a
button labelled "Open Container Tracker".  Tapping the button opens a
web app served at the URL configured in `WEB_APP_URL`.  The web app
collects the container number and shipping line and sends the data back
to the bot via `Telegram.WebApp.sendData()`.

Upon receiving `web_app_data`, this bot parses the JSON payload,
performs a dummy container tracking lookup (see `fetch_container_status`),
and replies to the user with the latest known status.  Real
integrations should call an official tracking API (such as those
offered by Maersk, Portcast, VesselFinder, etc.) using appropriate
authentication.

Dependencies:
  pip install python‑telegram‑bot==21.0 aiohttp

Configuration:
  Set the BOT_TOKEN environment variable or replace TOKEN_HERE below
  with your BotFather token.  Set WEB_APP_URL to the HTTPS URL where
  your mini‑app is hosted.
"""

import os
import json
import logging
from typing import Dict, Any

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    WebAppData,
    WebAppInfo,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Replace the URL below with your deployed web app URL.
WEB_APP_URL = os.environ.get("WEB_APP_URL", "https://your‑domain.example.com/index.html")
# Replace the token below with your BotFather token or set BOT_TOKEN env var.
BOT_TOKEN = os.environ.get("BOT_TOKEN", "TOKEN_HERE")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with a button that opens the container tracker web app."""
    keyboard = [
        [
            InlineKeyboardButton(
                text="Open Container Tracker",
                web_app=WebAppInfo(url=WEB_APP_URL),
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome! Tap the button below to track a shipping container.",
        reply_markup=reply_markup,
    )


async def handle_web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle data returned from the web app."""
    msg = update.message
    if msg is None or msg.web_app_data is None:
        return
    web_app_data: WebAppData = msg.web_app_data
    try:
        data: Dict[str, Any] = json.loads(web_app_data.data)
    except json.JSONDecodeError:
        await msg.reply_text("Sorry, I couldn't parse the data sent from the app.")
        return
    container_number = data.get("container")
    carrier = data.get("carrier")
    if not container_number or not carrier:
        await msg.reply_text(
            "Invalid data received. Please enter both a container number and a carrier."
        )
        return
    # Perform a dummy lookup.  Replace with a call to a real API.
    status_text = await fetch_container_status(container_number, carrier)
    await msg.reply_text(status_text)


async def fetch_container_status(container_number: str, carrier: str) -> str:
    """Dummy implementation of a container tracking lookup.

    In a real implementation, this function would call an external
    container tracking API.  Many carriers (including Maersk) offer
    official APIs for shipment tracking【548561951460452†L170-L252】.  You must
    register for an API key and follow the provider's documentation.

    For demonstration purposes, this function simply echoes the
    parameters and returns a fake status.  Update it with logic to
    query your chosen API.
    """
    # TODO: Replace this with a real API call, e.g. using aiohttp:
    # async with aiohttp.ClientSession() as session:
    #     headers = {"Authorization": f"Bearer {API_KEY}"}
    #     url = f"https://api.example.com/track?number={container_number}&carrier={carrier}"
    #     async with session.get(url, headers=headers) as resp:
    #         data = await resp.json()
    #         # parse status from data
    #         return f"Container {container_number} status: {status}"
    # For now, return a dummy message.
    return (
        f"Carrier: {carrier}\n"
        f"Container: {container_number}\n"
        f"Status: In transit (dummy data)\n"
        f"Last update: {"2026-03-03"}"
    )


def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    # Handler for web_app_data updates
    application.add_handler(
        MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_web_app_data)
    )
    # Start polling
    application.run_polling()


if __name__ == "__main__":
    main()