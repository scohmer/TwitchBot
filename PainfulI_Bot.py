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
        if message.echo:
            return

        # Print the content of the message if author exists
        if message.author:
            print(f'{message.author.name}: {message.content}')
        else:
            print(f'Unknown author: {message.content}')

        # Process commands if any
        await self.handle_commands(message)

#    @commands.command(name='commmands')
#        """
#        A command that responds with all the commands available
#        """
#        # Send a message in chat with all the commands available
#        await ctx.send(f'@{ctx.author.name} the commmads available are 'hello' 'commands' 'd20' 'uptime' ')

    @commands.command(name='hello')
    async def hello(self, ctx):
        """
        A command that responds with a greeting when a user types '!hello' in chat.
        """
        # Send a greeting message in the chat, mentioning the user who invoked the command
        await ctx.send(f'Hello @{ctx.author.name}!')

    @commands.command(name='d20')
    async def dice(self, ctx):
        """
        A command that mimicks rolling a d20 dice
        """
        # Sends a message in chat with the result of a d20 die
        import random
        num = random.randint(1,20)
        await ctx.send(f'@{ctx.author.name} you rolled a {num}')

    @commands.command(name='uptime')
    async def uptime(self, ctx):
        import aiohttp
        headers = {
            'Client-ID': CLIENT_ID,
            'Authorization': f'Bearer {TOKEN}'
        }
        url = f'https://api.twitch.tv/helix/streams?user_login={os.environ["CHANNEL"]}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                data = await response.json()
                print(data)
                if data['data']:
                    print(data)
                    import datetime
                    start_time = data['data'][0]['started_at']
                    start_time = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ')
                    now = datetime.datetime.utcnow()
                    uptime = now - start_time
                    hours, remainder = divmod(int(uptime.total_seconds()), 3600)
                    minutes, seconds = divmod(remainder, 60)
                    await ctx.send(f'Stream has been live for {hours}h {minutes}m {seconds}s')
                else:
                    await ctx.send('The stream is currently offline.')


# Entry point of the script
if __name__ == '__main__':
    # Create an instance of your bot
    bot = Bot()
    # Run the bot, which connects it to Twitch
    bot.run()
