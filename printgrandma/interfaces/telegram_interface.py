from typing import Mapping, Any
from logging import Logger, getLogger
from pathlib import Path
from pydantic import ValidationError
import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackContext,
)
import PIL
from PIL import Image, ImageEnhance
from printgrandma.utils.utils import PrinterConfig, TelegramConfig


class TelegramInterface(object):
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
        self._logging_chat_id = int(os.getenv(self._configTelegram.allowed_users[0]))
        self._pid = os.getpid()
        self._allowed_users = []
        self._api_key = ""
        self._logger = logger

    def init(
        self,
    ) -> bool:
        """
        This public function initialises the connection with the telegram bot.

        Returns
        -------
        success : bool
            True if successful initialisation, False otherwise.
        """
        success = True
        try:
            self._logger.info("Starting telegram interface")
            # Define the directory to store the received images
            self.IMAGES_DIR = self._configTelegram.image_dir
            if isinstance(self.IMAGES_DIR, str):
                self.IMAGES_DIR = Path(self.IMAGES_DIR)
            self.IMAGES_DIR.mkdir(parents=True, exist_ok=True)
            self._allowed_users = self._get_allowed_users()
            self._api_key = os.getenv(self._configTelegram.api)
            # Create the Application and pass it your bot's token.
            self.application = Application.builder().token(self._api_key).build()

            # on different commands - answer in Telegram
            self.application.add_handler(
                CommandHandler(
                    command="status",
                    callback=self._check_status,
                    filters=filters.Chat(self._allowed_users),
                )
            )

            # on non command i.e message - echo the message on Telegram
            self.application.add_handler(
                MessageHandler(filters=filters.TEXT & ~filters.COMMAND, callback=None)
            )
            # on non command i.e message - echo the message on Telegram
            self.application.add_handler(
                MessageHandler(
                    filters=filters.PHOTO & filters.Chat(self._allowed_users),
                    callback=self._handle_photo,
                )
            )

            # logging info
            self._logger.info(f"Telegram bot - {self._pid} successfully initialized")

            # Run the bot until the user presses Ctrl-C
            self.application.run_polling(allowed_updates=Update.ALL_TYPES)
        except Exception as error:
            self._logger.error(f"Process {self._pid} - " + repr(error))
            success = False
        return success

    def _get_allowed_users(self, **kwargs):
        """
        get the user ID env var from config file to read and append the allowed users.
        """
        allowed = []
        for user in self._configTelegram.allowed_users:
            allowed.append(int(os.getenv(user)))

        return allowed

    async def _check_status(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        This method sends to the bot the system status data
        """
        await update.message.reply_text("System is up and running")

    async def _handle_photo(self, update: Update, context: CallbackContext) -> None:
        """
        This method sends to the bot the system status data
        """
        # Get the file ID of the received image
        file_id = update.message.photo[-1].file_id
        file = await context.bot.get_file(file_id)
        file_path = self.IMAGES_DIR.joinpath(f"{file_id}.jpg")
        await file.download_to_drive(file_path)

        # Open the image using Pillow and resize to proper printer width
        img = Image.open(file_path)
        wsize = self._configPrinter.image_width
        wpercent = wsize / float(img.size[0])
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((wsize, hsize))
        img = ImageEnhance.Brightness(img)
        img.enhance(1.5)
        img.save(file_path)

        # Reply to the user
        await update.message.reply_text("Image received and stored successfully!")
