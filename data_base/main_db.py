import sqlite3 as sql

location = 'memory.db'


async def db_start():
    base = sql.connect(location)
    if base:
        print('Data base activated')
    base.execute('''CREATE TABLE IF NOT EXISTS audios(
    id TEXT PRIMARY KEY,
    song TEXT,
    artist TEXT,
    vibe INT,
    date TEXT,
    admin TEXT,
    FOREIGN KEY(artist) REFERENCES configures(artists)
    )''')
    base.execute('''CREATE TABLE IF NOT EXISTS users(
    id INT PRIMARY KEY,
    user_artists TEXT,
    user_vibe TEXT,
    active INT,
    lang TEXT
    )''')
    base.execute('''CREATE TABLE IF NOT EXISTS configures(
    artists TEXT PRIMARY KEY
    )''')
    base.commit()


async def get_artists(order):
    base = sql.connect(location)
    cursor = base.cursor()
    cursor.execute(f'''SELECT artists FROM configures {order}''')
    return cursor.fetchmany(7)


async def search_artist_db(text):
    base = sql.connect(location)
    cursor = base.cursor()
    cursor.execute(f'''SELECT artists FROM configures WHERE artists LIKE '%{text}%' ''')
    return cursor.fetchall()


async def add_artist_db(artist):
    base = sql.connect(location)
    cursor = base.cursor()
    cursor.execute(f'''INSERT INTO configures VALUES ("{artist}")''')
    base.commit()


async def add_song_db(data):
    base = sql.connect(location)
    cursor = base.cursor()
    cursor.execute('''INSERT INTO audios VALUES (?,?,?,?,?,?)''', data)
    base.commit()


async def get_random_song_db():
    base = sql.connect(location)
    cursor = base.cursor()
    cursor.execute('''SELECT id FROM audios ORDER BY RANDOM() LIMIT 1''')
    return cursor.fetchone()


async def get_songs_db(start, finish):
    base = sql.connect(location)
    cursor = base.cursor()
    cursor.execute(f'''SELECT song, artist, ROWID FROM audios WHERE ROWID > {start} and\
     ROWID <= {finish} ORDER by ROWID DESC''')
    return cursor.fetchmany(10)


async def search_song_db(text):
    base = sql.connect(location)
    cursor = base.cursor()
    cursor.execute(f'''SELECT song, artist, ROWID FROM audios WHERE artist LIKE "%{text}%" OR song LIKE "%{text}%"\
    ORDER by ROWID DESC''')
    return cursor.fetchmany(20)


async def get_song_db(text):
    base = sql.connect(location)
    cursor = base.cursor()
    cursor.execute(f'''SELECT id FROM audios WHERE ROWID = {text}''')
    return cursor.fetchone()[0]


async def get_song_title_db(text):
    base = sql.connect(location)
    cursor = base.cursor()
    cursor.execute(f'''SELECT id FROM audios WHERE song = "{text}" ''')
    return cursor.fetchone()[0]


async def get_vibe_db(title):
    base = sql.connect(location)
    cursor = base.cursor()
    cursor.execute(f'''SELECT vibe FROM audios WHERE song LIKE "%{title}%" ''')
    return cursor.fetchone()[0]


async def edit_vibe_db(vibes, title):
    base = sql.connect(location)
    cursor = base.cursor()
    cursor.execute(f"""UPDATE audios SET vibe='{vibes}' WHERE song LIKE "%{title}%" """)
    base.commit()


async def delete_song_db(title):
    base = sql.connect(location)
    cursor = base.cursor()
    cursor.execute(f"""DELETE FROM audios WHERE song = "{title}" """)
    base.commit()


async def get_artist_db(title):
    base = sql.connect(location)
    cursor = base.cursor()
    cursor.execute(f'''SELECT artist FROM audios WHERE song LIKE "%{title}%" ''')
    return cursor.fetchone()[0]


async def remove_artist_db(artist):
    base = sql.connect(location)
    cursor = base.cursor()
    cursor.execute(f"""DELETE FROM configures WHERE artists = "{artist}" """)
    base.commit()


async def select_artist_db(artist, title):
    base = sql.connect(location)
    cursor = base.cursor()
    cursor.execute(f"""UPDATE audios SET artist = "{artist}" WHERE song="{title}" """)
    base.commit()


async def register_user_db(user_id, lang):
    base = sql.connect(location)
    cursor = base.cursor()
    cursor.execute(f"""INSERT INTO users VALUES (?,?,?,?,?)""", (user_id, None, None, 1, lang))
    base.commit()


async def check_user_db(user_id):
    base = sql.connect(location)
    cursor = base.cursor()
    cursor.execute(f"""SELECT ROWID FROM users WHERE id = {user_id}""")
    return False if cursor.fetchone() is None else True


async def get_user_lang(user_id):
    base = sql.connect(location)
    cursor = base.cursor()
    cursor.execute(f"""SELECT lang FROM users WHERE id = {user_id}""")
    return 'RU' if cursor.fetchone()[0] == 'RU' else 'ENG'


async def register_user_activity(user_id):
    base = sql.connect(location)
    cursor = base.cursor()
    cursor.execute(f'''UPDATE users SET active = 1 WHERE id = {user_id}''')
    base.commit()


async def get_all_users_db():
    base = sql.connect(location)
    cursor = base.cursor()
    cursor.execute("SELECT id FROM users")
    return [r[0] for r in cursor.fetchall()]
