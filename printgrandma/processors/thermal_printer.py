from multiprocessing import Process
from typing import Mapping, Any
from logging import Logger, getLogger
import sys, os
from printgrandma.interfaces.printer_interface import ThermalPrinterInterface
from time import sleep


class ThermalPrinter(Process):
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
