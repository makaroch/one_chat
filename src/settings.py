from os import getenv

from dotenv import load_dotenv

load_dotenv()


class AppSettings:
    """
        Application settings
    """
    TG_BOT_TOKEN = getenv("TG_BOT_TOKEN", None)
    ROOT_USER_ID = int(getenv("ROOT_USER_ID", None))

    POSTGRES_DB = getenv("POSTGRES_DB", None)
    POSTGRES_USER = getenv("POSTGRES_USER", None)
    POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD", None)
    POSTGRES_HOST = getenv("POSTGRES_HOST", None)
    POSTGRES_PORT = getenv("POSTGRES_PORT", None)
    DB_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    def __post_init__(self):
        self.validate()

    @classmethod
    def validate(cls) -> None:
        for key, value in cls.__dict__.items():
            if value is None:
                raise ValueError(f"Environment variable {key} is not set")


APP_SETTINGS = AppSettings()
