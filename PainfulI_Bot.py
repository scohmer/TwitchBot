import os
from twitchio.ext import commands
from dotenv import load_dotenv

# Load environment variables from the .env file into the program's environment
load_dotenv()

# Retrieve credentials and settings from environment variables
BOT_NICK = os.environ['BOT_NICK']           # The bot's Twitch username
CLIENT_ID = os.environ['CLIENT_ID']         # Your Twitch application's Client ID
CLIENT_SECRET = os.environ['CLIENT_SECRET'] # Your Twitch application's Client Secret
TOKEN = os.environ['TOKEN']                 # OAuth token for the bot to authenticate with Twitch
PREFIX = os.environ.get('PREFIX', '~')      # Command prefix (defaults to '!' if not set)
CHANNEL = os.environ['CHANNEL']             # The name of the Twitch channel to join

# Define a class for your bot, inheriting from twitchio's commands.Bot
class Bot(commands.Bot):

    def __init__(self):
        # Initialize the bot with required parameters
        super().__init__(
            token=TOKEN,                     # Authentication token for Twitch IRC
            client_id=CLIENT_ID,             # Client ID of your Twitch application
            nick=BOT_NICK,                   # The bot's username on Twitch
            prefix=PREFIX,                   # Command prefix for your bot (e.g., '!' for '!command')
            initial_channels=[CHANNEL]       # The channel(s) the bot should join upon connecting
        )

    async def event_ready(self):
        """
        Called once when the bot successfully connects to Twitch.
        Useful for initialization tasks and confirming the bot is online.
        """
        print(f'Logged in as | {self.nick}')    # Output the bot's username
        print(f'User id is | {self.user_id}')   # Output the bot's user ID

    async def event_message(self, message):
        """
        Called whenever a message is received in chat.
        """
        # Ignore messages sent by the bot itself                                                                                                           
