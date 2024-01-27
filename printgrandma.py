import sys, os, argparse
from pathlib import Path
from time import sleep
import yaml

from printgrandma.utils.utils import get_logger
from printgrandma.processors.telegram_bot import TelegramBot
from printgrandma.processors.thermal_printer import ThermalPrinter


def main() -> int:
    logger = get_logger(__name__)
    success = True
    processes = None
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

        # Creation of processes
        processes = []
        # Telegram bot
        if config["telegram_bot"]["enable"]:
            processes.append(TelegramBot(config=config, logger=logger))
        # printer
        if config["printer"]["enable"]:
            processes.append(ThermalPrinter(config=config, logger=logger))

        # Start processes
        for process in processes:
            process.start()

        while success:
            for process in processes:
                if process.exitcode == 1:
                    raise Exception(
                        "A critical process exited with error, terminating all other processes"
                    )
            sleep(1)
    except Exception as error:
        logger.error(f"Process {pid} - " + repr(error))
        success = False
    finally:
        logger.info("Exiting application")
        if processes is not None:
            [p.kill() for p in processes if p.is_alive()]
    return int(not success)


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
