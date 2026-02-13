from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    # --- API (TMDB) ---
    api_base_url: str = 'https://api.themoviedb.org/3'
    api_token: str = ''

    # --- UI (TMDB Web) ---
    ui_base_url: str = 'https://www.themoviedb.org'
    browser_name: str = 'chrome'
    browser_version: str = '131.0'
    window_width: int = 1920
    window_height: int = 1080
    remote_url: str = ''
    selenoid_login: str = ''
    selenoid_password: str = ''

    # --- Telegram ---
    telegram_bot_token: str = ''
    telegram_chat_id: str = ''


settings = Settings()
