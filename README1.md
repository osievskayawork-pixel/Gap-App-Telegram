# Telegram Mini‑App Example

This project contains a minimal example of a **Telegram Mini‑App** (Web App) and a companion bot built with Python.  It demonstrates how to launch a web interface directly inside Telegram and exchange data between the web page and your bot.

## Structure

- **`bot.py`** – A simple Telegram bot written with `python‑telegram‑bot`.  It sends a button that opens the web app and listens for data returned from it.
- **`webapp/index.html`** – A static HTML page served over HTTPS.  It uses the [Telegram Web Apps JavaScript API](https://core.telegram.org/bots/webapps) to interact with Telegram.  In this example the page implements a tiny to‑do list and sends the list back to the bot.

## Getting started

1. **Create a bot.**  Open @BotFather in Telegram and send `/newbot`.  Follow the prompts to choose a name and username.  BotFather will give you an API token – keep it secret.  You can also set a description, commands and avatar using `/setdescription`, `/setcommands` and `/setuserpic`【548561951460452†L185-L205】.

2. **Choose a domain and hosting.**  The web app must be served over **HTTPS** and accessible via a public URL【548561951460452†L207-L236】.  For static sites you can use services like Vercel, Netlify or GitHub Pages.  For a dynamic backend you might deploy on a cloud provider.  Once hosted, note the full URL of your `index.html` (for example `https://your‑domain.example.com/index.html`).

3. **Allow the domain.**  In BotFather run `/setdomain` on your bot and enter your app’s base URL【548561951460452†L239-L252】.  Telegram will trust this domain and allow it to be opened inside the WebView.

4. **Link the Mini‑App.**  In your bot’s settings (open your bot’s profile → **Mini Apps** → **Create Direct Link**), specify the URL of your web app and fill in the title and description.  You can also enable the main app or menu buttons here.  The screenshots provided show these steps.

5. **Run the bot** locally or on a server:

   ```bash
   cd telegram_mini_app
   pip install -r requirements.txt
   python bot.py
   ```

   Replace `TOKEN_HERE` in `bot.py` with the token from BotFather.  The bot uses long polling for simplicity.  When a user sends `/start`, it replies with a button labelled **Open To‑Do App** that opens your web app.

6. **Test.**  In Telegram open a chat with your bot and tap the **Open To‑Do App** button.  The web page will load inside Telegram.  Add a couple of items and press **Send to Bot**.  The bot will receive the data and reply with your list.  Verify that the data round‑trip works.  If you update the web app, redeploy it and the changes will be visible immediately.

## Limitations

- This example stores data only in memory; for real apps you would persist data on the server or using Telegram’s new CloudStorage/SecureStorage options (introduced in Bot API 9.0)【720412387938700†L110-L115】.
- Error handling and authentication have been kept minimal.  In production you must verify the integrity of the `initData` parameter sent by Telegram to the web app (see the official docs for signature validation).

## References

The official documentation provides comprehensive guidance on designing and implementing Mini Apps, including the latest features such as persistent local storage and full‑screen mode【720412387938700†L80-L117】.  A step‑by‑step overview of creating a Mini App, including setting the domain and linking it via BotFather, can be found in this guide【548561951460452†L170-L252】.