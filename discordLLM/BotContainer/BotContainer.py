import discord
from LLMHandler.LLMHandler import LLMHandler
import toml
import os
class BotContainer:
    def __init__(self, bot_token, guild_id, llm_api, llm_key, default_persona):
        self.token = bot_token
        self.guild_id = guild_id
        self.llm_api = llm_api
        self.llm_key = llm_key
        # Create the persona
        self.create_persona(self.llm_api, default_persona)
        # Initialize the bot
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.bot = discord.Bot(intents=self.intents)
        
    def run(self):
        self.bot.run(self.token)

    def create_persona(self, api, persona_name):
        config = toml.load("config.toml")  #TODO: CHANGE THIS TO USER PROVIDED PATH
        try:
            persona_name = persona_name.upper()
            model = config[f"PERSONA-{persona_name}"]["model"]
            prompt = config[f"PERSONA-{persona_name}"]["prompt"]
        except KeyError:
            print(f"Persona {persona_name} not found in config.toml")
            return
        self.LLM = LLMHandler(api, self.llm_key, model, prompt)

    def register_events(self):
        @self.bot.event
        async def on_ready():
            print(f'{self.bot.user} has connected to Discord!')
        
        @self.bot.event
        async def on_message(message):
            # Prevent the bot from responding to itself
            if message.author == self.bot.user:
                return
            
            # If the bot is mentioned, respond with the LLM
            if self.bot.user in message.mentions: 
                await message.reply(self.LLM.request(message.content))

        @self.bot.slash_command(guild_ids=[self.guild_id])
        async def changepersona(ctx, persona):
            await ctx.respond(f"Switching persona to: {persona}")
            self.create_persona(self.llm_api, persona)