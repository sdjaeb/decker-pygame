from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Manages game configuration.

    Settings can be loaded from a .env file or environment variables.

    Attributes:
        screen_width (int): Width of the game window.
        screen_height (int): Height of the game window.
        fullscreen (bool): Whether to run in fullscreen mode.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Display settings
    screen_width: int = 1280
    screen_height: int = 720
    fullscreen: bool = False

    # You could add other settings like difficulty, asset paths, etc.


# A single, global instance of the settings that can be imported elsewhere.
settings = Settings()
