import logging


def get_logger(name=__name__):
    """
    get logger object
    """
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


from pydantic import BaseModel, ConfigDict
from typing import List
from pathlib import Path


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
    allowed_users: List[str]
