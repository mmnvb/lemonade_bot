from aiogram.dispatcher.filters.state import StatesGroup, State


class FsmEdit(StatesGroup):
    song_choice = State()
    song_search = State()
    tools_choice = State()
    artist_search = State()


class FsmPost(StatesGroup):
    text = State()
    media = State()
    decide = State()


class FsmLoad(StatesGroup):
    load = State()
    artist = State()
    search_artist_state = State()
    add_artist_state = State()
    vibe = State()