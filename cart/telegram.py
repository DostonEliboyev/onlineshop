import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_order_notification(order):
    """Send order details to Telegram chat."""
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID

    if not token or not chat_id:
        logger.warning("Telegram bot token or chat ID not configured. Skipping notification.")
        return False

    items_text = ""
    for item in order.items.all():
        items_text += f"  - {item.product_name} x{item.quantity} = ${item.subtotal}\n"

    message = (
        f"🛒 *New Order #{order.pk}*\n"
        f"━━━━━━━━━━━━━━━\n"
        f"👤 *Customer:* {order.full_name}\n"
        f"📞 *Phone:* {order.phone}\n"
        f"🏠 *Address:* {order.address}, {order.city}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"📦 *Items:*\n{items_text}"
        f"━━━━━━━━━━━━━━━\n"
        f"💰 *Total:* ${order.total_price}\n"
        f"💳 *Payment:* Cash on Delivery\n"
    )

    if order.note:
        message += f"📝 *Note:* {order.note}\n"

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown',
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        logger.error(f"Failed to send Telegram notification: {e}")
        return False
