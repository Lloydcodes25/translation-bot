import asyncio

import aiosqlite

from config import DB_PATH


async def init_db():
    async with aiosqlite.connect(DB_PATH) as conn, conn.cursor() as cur:
        await cur.execute("""CREATE TABLE IF NOT EXISTS words (
                            WordId INTEGER PRIMARY KEY AUTOINCREMENT,
                            English TEXT NOT NULL UNIQUE,
                            Russian TEXT NOT NULL UNIQUE
            )
            """)
        await conn.commit()
    print(f"База данных {DB_PATH} создана!")   

if __name__ == '__main__':
    asyncio.run(init_db())
    