from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from functools import lru_cache
import os
from dotenv import load_dotenv
load_dotenv()

class BaseConfig(BaseSettings):
    ENV_STATE: Optional[str] =None
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )


class GlobalConfig(BaseConfig):
    DATABASE_URL: Optional[str] = None
    DB_FORCE_ROLL_BACK: bool = True

class DevConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="DEV_")


class ProdConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="PROD_")


class TestConfig(GlobalConfig):
    DATABASE_URL: str = "sqlite:///test.db"
    DB_FORCE_ROLL_BACK: bool = True
    model_config = SettingsConfigDict(env_prefix="TEST_")


@lru_cache()
def get_config(env_state: Optional[str]):
    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}

    # Default to 'dev' if env_state is None
    if env_state is None:
        print("ENV_STATE is not set. Using default 'dev' configuration.")
        env_state = "dev"

    try:
        return configs[env_state]()
    except KeyError:
        raise ValueError(f"Invalid ENV_STATE: {env_state}. Must be one of {list(configs.keys())}.")


config = get_config(BaseConfig().ENV_STATE)



