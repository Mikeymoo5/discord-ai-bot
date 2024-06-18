class BotContainer:
    def __init__(self, bot_token):
        self.token = bot_token

        # Initialize the bot
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.client = discord.Client(intents = self.intents)
        

    def run(self):
        self.client.run(self.token)
        
    @self.client.event
    async def on_ready():
        print(f'{self.client.user} has connected to Discord!')