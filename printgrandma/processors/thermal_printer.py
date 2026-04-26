import os
import sys
from collections.abc import Mapping
from logging import Logger, getLogger
from multiprocessing import Process
from time import sleep
from typing import Any

from printgrandma.interfaces.printer_interface import ThermalPrinterInterface


class ThermalPrinter(Process):
    def __init__(self, config: Mapping[str, Any], logger: Logger | None = None) -> None:
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
        self._logger = logger if logger is not None else getLogger()

    def run(self) -> None:
        success = False
        print_if = None
        pid = os.getpid()
        try:
            print_if = ThermalPrinterInterface(
                config=self._config,
                logger=self._logger,
            )

            success = print_if.init()
            while success:
                success = print_if.check_images()
                sleep(2)

        except Exception as error:
            self._logger.error(f"Process {pid} - " + repr(error))
            success = False
        finally:
            pass

        exit_code = int(not success)
        sys.exit(exit_code)
