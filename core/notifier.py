import os
import requests
from dotenv import load_dotenv

load_dotenv()

class TelegramNotifier:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    def send_signal(self, current_price, analysis):
        """
        Katsifet l'message l'Telegram b format wa3r.
        """
        if not self.token or not self.chat_id:
            print("⚠️ Telegram token wla chat_id ma kayninch f .env.")
            return

        decision = analysis.get('decision')
        confidence = analysis.get('confidence')
        reasoning = analysis.get('reasoning')

        # N-zow9ou l'message 3la 7sab l'Action
        emoji = "🟢" if decision == "BUY" else "🔴" if decision == "SELL" else "⏸️"
        
        message = f"🤖 <b>OpenClaw | XAU/USD Proxy</b>\n\n"
        message += f"{emoji} <b>Action :</b> {decision}\n"
        message += f"💲 <b>Prix   :</b> {current_price}$\n"
        message += f"📊 <b>Confiance:</b> {confidence}%\n\n"
        message += f"📝 <b>Raisonnement Cerveau (IA):</b>\n<i>{reasoning}</i>"

        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML"  # Bach y9ra l'Gras w l'Italique
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            print("📲 Signal mcha l'Telegram b naja7!")
        except Exception as e:
            print(f"❌ Mochkil f tsyafat d Telegram: {e}")