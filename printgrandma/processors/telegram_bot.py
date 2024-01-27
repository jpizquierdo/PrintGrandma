from multiprocessing import Process
from typing import Mapping, Any
from logging import Logger, getLogger
import sys, os
from printgrandma.interfaces.telegram_interface import TelegramInterface


class TelegramBot(Process):
    def __init__(self, config: Mapping[str, Any], logger: Logger = getLogger()) -> None:
        """
        Data consumer constructor.

        Parameters
        ----------
        config : Mapping[str, Any]
            Consumer static configuration.
        logger: Logger
            logger object
        ----------
        """
        super().__init__()
        self._config = config.copy()
        self._logger = logger

    def run(self) -> None:
        success = False
        teleti = None
        pid = os.getpid()
        try:
            teleti = TelegramInterface(
                config=self._config,
                logger=self._logger,
            )
            while True:
                # In this case, it wont termine the execution of init, it will be an infinite loop with asyncio functionalities
                success = teleti.init()

        except Exception as error:
            self._logger.error(f"Process {pid} - " + repr(error))
            success = False
        finally:
            pass  # close telegram bot

        exit_code = int(not success)
        sys.exit(exit_code)
