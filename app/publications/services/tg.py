from database.models import User


async def get_telegram_bot_token(user: User) -> dict:
    """
    Generates a Telegram bot connection token for a user and provides a message with a link.

    :param user: The User object for which the token is being created.

    :return: A dictionary containing the generated token, a link to the Telegram bot,
             and a message instructing the user on how to connect notifications.
    """
    message = "fДля подключения уведомлений от бота перейдите по ссылке и отправьте боту код"
    token = await create_token(user)
    link = "https://t.me/CarNotification_bot"
    return {"token": token, "link": link, "message": message}


async def create_token(user: User) -> str:
    """
    Creates a unique token for a user based on their user ID.

    :param user: The User object for which the token is being created.

    :return: A string representing the generated token.
    """
    token: str
    user_id = user.id
    token = f"7586{user_id}"
    return token
