import asyncio

import requests
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from config import TG_BOT_TOKEN
from database.models import User


async def update_user_tg_ids(session: AsyncSession) -> None:
    ids = await get_new_ids()
    for chat_id, user_id in ids.items():
        result = await session.execute(select(User).filter(User.id == user_id))
        user = result.unique().scalars().first()
        user.tg_chat_id = chat_id
    await session.commit()


async def get_new_ids() -> dict:
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/getUpdates"
    resp = requests.get(url).json()
    ids: dict = {}
    if resp is not None:
        for msg in resp["result"]:
            chat_id = msg["message"]["chat"]["id"]
            text = msg["message"]["text"]
            try:
                user_id = int(text[4:])
                print(user_id)
            except IndexError:
                continue
            except ValueError:
                continue
            ids[chat_id] = user_id
            print(ids)
    return ids

# asyncio.run(get_new_ids())
