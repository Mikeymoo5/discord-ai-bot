import discord
from discord_llm.llm import LLMHandler
import toml


class BotContainer:
    def __init__(self, config: dict):
        self.bot = discord.Client()
        self.token = config["bot"]["token"]
        self.guild_id = config["bot"]["guild_id"]
        self.llm_api = config["ai"]["type"]
        self.llm_base_url = config["ai"]["base_url"]
        self.llm_key = config["ai"].get("key")
        # This shouldn't be needed as long as create_persona is called and it instantiates the LLM
        # self.LLM = LLMHandler(
        #     api=self.llm_api,
        #     base_url=self.llm_base_url,
        #     key=self.llm_key,
        #     model=config["ai"]["model"],
        #     prompt=config["persona"]["default"]["prompt"],
        # )
        # Create the persona
        self.create_persona(self.llm_api, "default")
        # Initialize the bot
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.bot = discord.Bot(intents=self.intents)

    def run(self):
        self.bot.run(self.token)

    def create_persona(self, api, persona_name):
        config = toml.load("config.toml")  # TODO: CHANGE THIS TO USER PROVIDED PATH
        try:
            name = persona_name.lower()
            model = config["persona"][name]["model"]
            prompt = config["persona"][name]["prompt"]
        except KeyError:
            print(f"Persona {persona_name} not found in config.toml")
            return
        self.LLM = LLMHandler(
            api=api,
            base_url=self.llm_base_url,
            key=self.llm_key,
            model=model,
            prompt=prompt,
        )

    def register_events(self):
        @self.bot.event
        async def on_ready():
            print(f"{self.bot.user} has connected to Discord!")

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
