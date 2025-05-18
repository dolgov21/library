from config import settings
from loguru import logger


def setup_logger():
    logger.add(
        settings.logger.logbook_path,
        format=settings.logger.logs_format,
        rotation=settings.logger.rotation_time,
        compression="zip",
        enqueue=True,
    )
    logger.debug("The logger has been configured")
