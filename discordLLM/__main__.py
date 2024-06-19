import click
import sys
from BotContainer.BotContainer import BotContainer
import toml
@click.command()
@click.option("--config-path", help="Path to the config file")
def main(config_path):
    if config_path:
        click.echo("Using config file")
    else:
        create_config()

    # Load the configuration file
    config = toml.load("config.toml")
    Bot = BotContainer(config["BOT"]["bot_token"]) # Create an instance of the BotContainer
    Bot.create_persona(config["BOT"]["api"], "llama3") # Create an instance of the LLMHandler
    Bot.register_events() # Register the events that the bot will respond to
    Bot.run() # Run the bot!

def create_config():
    if click.prompt("No config file provided. Create one now? (y/n)").lower() == "y":
            bot_token = click.prompt("Enter your bot token")
            while not bot_token:
                bot_token = click.prompt("Enter your bot token")
            if click.prompt("Use the OpenAI api? (y/n)").lower() == "y":
                openai_api_key = click.prompt("Enter your OpenAI api key")
                while not openai_api_key:
                    openai_api_key = click.prompt("Enter your OpenAI api key")
                api = "OpenAI"
            else:
                click.echo("Defaulting to Ollama")
                api = "Ollama"
    else:
        click.echo("Exiting...")
        sys.exit(1)

    #Create the TOML configuration file
    with open("config.toml", "w") as f:
        f.write("[BOT]\n")
        f.write(f"bot_token = \"{bot_token}\"\n")
        f.write(f"api = \"{api}\"\n")
        if api == "OpenAI":
            f.write(f"openai_api_key = {openai_api_key}\n")
        f.write("\n[PERSONAS]")
        f.close()

if __name__ == "__main__":
    main()