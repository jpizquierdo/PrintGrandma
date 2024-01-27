import argparse
from pathlib import Path
from pydantic import ValidationError
import yaml
from printgrandma.utils.utils import PrinterConfig, TelegramConfig
import os


# Get static configuration for the program
parser = argparse.ArgumentParser()
parser.add_argument(
    "-c",
    "--config",
    default="./config/config.yaml",
    help="Path to static configuration",
)
with open(Path(parser.parse_args().config), "r") as configfile:
    config = yaml.safe_load(configfile)
    try:
        telegramconfig = TelegramConfig(**config["telegram_bot"])
        printerconfig = PrinterConfig(**config["printer"])
    except ValidationError as e:
        print(e)
    print("validator check")
    # you can not set them from python
    # os.environ[telegramconfig.api]= "bh65uny567n45747n"
    # os.environ[telegramconfig.allowed_users[0]]= "9999999999"
    # os.environ[telegramconfig.allowed_users[1]]= "1231231239"
    # os.environ[telegramconfig.allowed_users[2]]= "3213123123"
    print("checking environment variables")
    print(os.environ[telegramconfig.api])
    print(os.environ[telegramconfig.allowed_users[0]])
