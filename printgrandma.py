import sys, os, argparse
from pathlib import Path
from time import sleep
import yaml
from printgrandma.telegram_interface import TelegramInterface

from printgrandma.utils.utils import get_logger
def main() -> int:
    logger = get_logger(__name__)
    success= True
    pid = os.getpid()
    logger.info(f"Starting PrintGrandma app with pid {pid}")
    try:
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
        # Telegram bot
        if config["telegram_bot"]["enable"]:
            teleit=TelegramInterface(config=config["telegram_bot"], logger=logger)
        # printer
        if config["printer"]["enable"]:
            #TODO: printer logic
            pass
        while success:
            sleep(1)
    except Exception as error:
        print(f"Process {pid} - " + repr(error))
        success = False
    finally:
        logger.info("Exiting application")
    return int(not success)

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)