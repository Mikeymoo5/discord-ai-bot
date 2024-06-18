class BotContainer:
    def __init__(self, bot_token):
        self.token = bot_token
        # self.client = discord.Client()
        print("BotContainer initialized with token: " + self.token)
        