import logging
from pathlib import Path

from pydantic import BaseModel, ConfigDict


def get_logger(name=__name__):
    """
    get logger object
    """
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


class PrinterConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    enable: bool
    image_width: int
    idVendor: int
    idProduct: int
    profile: str


class TelegramConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    enable: bool
    api: str
    image_dir: Path | str
    allowed_users: list[str]
