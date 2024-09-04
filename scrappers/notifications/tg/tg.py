import requests
from sqlalchemy import select

from config import TG_BOT_TOKEN
from database.database import scoped_session
from database.models import User


async def update_user_tg_ids() -> None:
    """
    Updates the Telegram chat IDs for users in the database.

    Fetches new Telegram chat IDs and associates them with user IDs.
    If a user ID exists in the database, their corresponding Telegram
    chat ID is updated.

    :return: None. The function modifies user records in the database.
    """
    async with scoped_session() as session:
        ids = await get_new_ids()
        for chat_id, user_id in ids.items():
            result = await session.execute(select(User).filter(User.id == user_id))
            user = result.unique().scalars().first()
            if user is not None:
                user.tg_chat_id = chat_id
        await session.commit()


async def get_new_ids() -> dict:
    """
    Fetches new Telegram chat IDs and user IDs from the Telegram API.

    Sends a request to the Telegram Bot API to retrieve updates.
    Extracts chat IDs and user IDs from incoming messages, where
    the user ID is expected to be in the message text.

    :return: A dictionary mapping chat IDs to user IDs.
             Returns an empty dictionary if no valid IDs are found.
    """
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/getUpdates"
    resp = requests.get(url).json()
    ids: dict = {}
    if resp is not None:
        for msg in resp["result"]:
            chat_id = msg["message"]["chat"]["id"]
            text = msg["message"]["text"]
            try:
                user_id = int(text[4:])
            except IndexError:
                continue
            except ValueError:
                continue
            ids[chat_id] = user_id
    return ids

