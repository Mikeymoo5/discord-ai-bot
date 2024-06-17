class DiscordBot:
    def __init__(self, token):
        self.token = token
        # self.client = discord.Client()
        self.client.run(self.token)