from typing import Mapping, Any
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
from PIL import Image

class TelegramInterface(object):
    def __init__(
        self,
        config: Mapping[str, Any] = {},
        logger=None
    ) -> None:
        """
        Telegram interface constructor.

        Parameters
        ----------
        config : Mapping[str, Any]
            Class configuration map.
        name: str
            name in json file
        """
        self._config = config
        self.logging_chat_id = int(os.getenv(self._config["allowed_users"][0]))
        self._pid = os.getpid()
        self._allowed_users = []
        self._api_key = ""
        self.logger=logger

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
            # Define the directory to store the received images
            self.IMAGES_DIR = self._config["image_dir"]
            os.makedirs(self.IMAGES_DIR, exist_ok=True)
            self._allowed_users = self._get_allowed_users()
            self._api_key = os.getenv(self._config["api"])
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
                MessageHandler(filters.TEXT & ~filters.COMMAND, None)
            )
            # on non command i.e message - echo the message on Telegram
            self.application.add_handler(
                MessageHandler(filters=filters.PHOTO, callback=self._handle_photo)
            )
            
            # logging info
            self.logger.info(f"Telegram bot - {self._pid} successfully initialized")
            
            # Run the bot until the user presses Ctrl-C
            self.application.run_polling(allowed_updates=Update.ALL_TYPES)
        except Exception as error:
            print(f"Process {self._pid} - " + repr(error))
            success = False
        return success

    def _get_allowed_users(self, **kwargs):
        """
        get the user ID env var from config file to read and append the allowed users.
        """
        allowed = []
        for user in self._config["allowed_users"]:
            allowed.append(int(os.getenv(user)))

        return allowed

    async def _check_status(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        This method sends to the bot the system status data
        """
        await update.message.reply_text("System is up and running")
    
    async def _handle_photo(
        self, update: Update, context: CallbackContext
    ) -> None:
        """
        This method sends to the bot the system status data
        """
        # Get the file ID of the received image
        file_id = update.message.photo[-1].file_id

        # Download the image file
        file = context.bot.get_file(file_id)
        file_path = os.path.join(self.IMAGES_DIR, f"{file_id}.jpg")
        file.download(file_path)

        # Open the image using Pillow
        img = Image.open(file_path)
        mywidth = 300
        wpercent = (mywidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((mywidth,hsize), PIL.Image.ANTIALIAS)
        img.save(f"{file_id}.jpg")

        # Process the image (you can add your image processing logic here)

        # Reply to the user
        await update.message.reply_text('Image received and stored successfully!')
    