from typing import Mapping, Any
from logging import Logger, getLogger
import os
from pathlib import Path
from pydantic import ValidationError
from escpos.printer import Usb
from printgrandma.utils.utils import PrinterConfig, TelegramConfig
from time import sleep


class ThermalPrinterInterface(object):
    def __init__(
        self, config: Mapping[str, Any] = {}, logger: Logger = getLogger()
    ) -> None:
        """
        Telegram interface constructor.

        Parameters
        ----------
        config : Mapping[str, Any]
            Class configuration map.
        logger: Logger
            logger object
        """
        try:
            self._configTelegram = TelegramConfig(**config["telegram_bot"])
            self._configPrinter = PrinterConfig(**config["printer"])
        except ValidationError as e:
            logger.error(e)
        self._pid = os.getpid()
        self._logger = logger
        self.printer = None

    def init(
        self,
    ) -> bool:
        """
        This public function initialises the connection with the thermal printer.

        Returns
        -------
        success : bool
            True if successful initialisation, False otherwise.
        """
        success = True
        try:
            # Define the directory to store the received images
            self.printer = Usb(
                idVendor=self._configPrinter.idVendor,
                idProduct=self._configPrinter.idProduct,
                usb_args=0,
                profile=self._configPrinter.profile,
            )
            self.IMAGES_DIR = self._configTelegram.image_dir
            if isinstance(self.IMAGES_DIR, str):
                self.IMAGES_DIR = Path(self.IMAGES_DIR)
            self.IMAGES_DIR.joinpath("/print")
            self.IMAGES_DIR.mkdir(parents=True, exist_ok=True)
            self._logger.info(f"Thermal Printher interface successfully initialized with pid {self._pid}")
        except Exception as error:
            self._logger.error(f"Process {self._pid} - " + repr(error))
            success = False
        return success

    def check_images(
        self,
    ) -> bool:
        """
        This method check if there are new images in the folder ready to print
        """
        success = True

        try:
            for image in self.IMAGES_DIR.glob("*.jpg"):
                self.printer.image(image)
                #in order to have more space below the picture
                self.printer.textln()
                self.printer.textln()
                sleep(5)
                image.unlink()
        except Exception as e:
            self._logger.error(e)
            success = False
        return success
