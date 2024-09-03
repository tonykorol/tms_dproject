from datetime import UTC, datetime

from database.models import User


async def get_telegram_bot_token(user: User) -> dict:
    message = "fДля подключения уведомлений от бота перейдите по ссылке и отправьте боту код"
    token = await create_token(user)
    link = "https://t.me/CarNotification_bot"
    return {"token": token,
            "link": link,
            "message": message}

async def create_token(user: User) -> str:
    token: str
    user_id = user.id
    token = f"7586{user_id}"
    return token
