import aiosqlite

from config import DB_PATH

EN_LETTERS = set('qwertyuiopasdfghjklzxcvbnm')
RU_LETTERS = set('ёйцукенгшщзхъфывапролджэячсмитьбю')

def get_cleaned_sentence(word):
    symbols = [',', '.', '?', '!', '@', '#', '$', '%', '^', '&', '*',
    '/', '\\', '|', '~', '`', '-', '+', '=', '"', "'", '№', ';', ':',
    '(', ')', '()', '<', '>',]
    word = word.lower().strip()
    for symbol in symbols:
        word = word.replace(symbol, '') if symbol in word else word
    return word

def is_english(word: str) -> bool:
    letters = set(word.lower())
    return len(letters & EN_LETTERS) > len(letters & RU_LETTERS)

def is_russian(word: str) -> bool:
    letters = set(word.lower())
    return len(letters & RU_LETTERS) > len(letters & EN_LETTERS)

async def translate(word: str) -> str | None:
    word = get_cleaned_sentence(word)
    async with aiosqlite.connect(DB_PATH) as conn, conn.cursor() as cur:
        cur = await conn.execute('SELECT Russian FROM words WHERE English = ?', (word,))
        
        row = await cur.fetchone()
        if row:
            return row[0]
        
        cur = await conn.execute('SELECT English FROM words WHERE Russian = ?', (word,))
        row = await cur.fetchone()
        return row[0] if row else None

async def add(word: str, translation: str) -> bool:
    """True, если слово уже есть (failure)."""
    word = get_cleaned_sentence(word)
    translation = get_cleaned_sentence(translation)
    async with aiosqlite.connect(DB_PATH) as conn, conn.cursor() as cur:
        if is_russian(word):
            await cur.execute('INSERT OR IGNORE INTO words (Russian, English) VALUES (?, ?)', (word, translation))
        elif is_english(word):
            await cur.execute('INSERT OR IGNORE INTO words (English, Russian) VALUES (?, ?)', (word, translation))
        else:
            return True
        
        await conn.commit()
        return cur.rowcount == 0

async def update(word, new_word):
    """"True, если слово не найдено (failure)."""
    word = get_cleaned_sentence(word)
    new_word= get_cleaned_sentence(new_word)
    async with aiosqlite.connect(DB_PATH) as conn, conn.cursor() as cur:
        
        if is_russian(word):
            await cur.execute('UPDATE words SET English = ? WHERE Russian = ?', (new_word, word))
        elif is_english(word):
            await cur.execute('UPDATE words SET Russian = ? WHERE English = ?', (new_word, word))
        else:
            return True
        
        await conn.commit()
        return cur.rowcount == 0

async def delete(word):
    """True, если слово не найдено (failure)."""
    word = get_cleaned_sentence(word)
    async with aiosqlite.connect(DB_PATH) as conn, conn.cursor() as cur:
        if is_russian(word):
            await cur.execute('DELETE FROM words WHERE Russian = ?', (word,))
        elif is_english(word):
            await cur.execute('DELETE FROM words WHERE English = ?', (word,))
        else:
            return True
        
        await conn.commit()
        return cur.rowcount == 0
        




