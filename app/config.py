from pydantic import BaseModel, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseModel):
    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10

    dialect: str = "postgresql"
    driver: str = "asyncpg"
    username: str
    password: str
    address: str
    port: int
    db_name: str

    @computed_field(return_type=PostgresDsn)
    @property
    def url(self) -> PostgresDsn:
        return PostgresDsn(
            f"{self.dialect}+{self.driver}://"
            f"{self.username}:{self.password}@"
            f"{self.address}:{self.port}/{self.db_name}"
        )


class LoggerConfig(BaseModel):
    """
    Configuration for setting up the Loguru logger.

    Attributes:
        logbook_path (str): - Path to the log file.
        logs_format (str): - Format string for log messages.
        rotation_time (str): - Time for daily log file rotation.
    """

    logbook_path: str = "/app/logs/logbook.log"
    logs_format: str = "{time} | {level} | {module}:{line} | {message}"
    rotation_time: str = "08:00"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="GF__",
    )

    db: DatabaseConfig
    logger: LoggerConfig = LoggerConfig(
        logbook_path="logs/logbook.log",
        logs_format="{time} | {level} | {module}:{line} | {message}",
        rotation_time="08:00",
    )


settings = Settings()
