import asyncio

import aiosqlite

from config import DB_PATH
from words_data import get_dicts


async def seed_words():
    async with aiosqlite.connect(DB_PATH) as conn, conn.cursor() as cur:
        en_ru = get_dicts()
        for english, russian in en_ru.items():
            await cur.execute(
                'INSERT OR IGNORE INTO words (English, Russian) VALUES (?, ?)',
                (english, russian)
            )
        await conn.commit()
    print("Слова добавлены (без дублей.)")
    
if __name__ == "__main__":
    asyncio.run(seed_words())
