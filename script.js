// Initialize the Telegram WebApp API
const tg = window.Telegram.WebApp;
tg.ready();

const form = document.getElementById('tracker-form');
const statusMessage = document.getElementById('status-message');

form.addEventListener('submit', function (event) {
  event.preventDefault();
  const containerInput = document.getElementById('container');
  const carrierInput = document.getElementById('carrier');
  const container = containerInput.value.trim();
  const carrier = carrierInput.value.trim();
  if (!container || !carrier) {
    statusMessage.textContent = 'Both fields are required.';
    statusMessage.classList.remove('hidden');
    return;
  }
  // Prepare the payload
  const payload = {
    container: container,
    carrier: carrier,
  };
  // Disable the button and show a message
  const sendBtn = document.getElementById('send-btn');
  sendBtn.disabled = true;
  sendBtn.textContent = 'Sending…';
  // Send data to the bot.  The data will be delivered via update.message.web_app_data
  tg.sendData(JSON.stringify(payload));
  statusMessage.textContent = 'Data sent to the bot. You can close this window.';
  statusMessage.classList.remove('hidden');
  // Optionally close the web app after a short delay
  setTimeout(() => {
    tg.close();
  }, 1500);
});