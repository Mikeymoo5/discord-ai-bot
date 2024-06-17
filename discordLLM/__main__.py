import discord
import click
import sys
from discordLLM.BotContainer import BotContainer
@click.command()
@click.option("--config-path", help="Path to the config file")
def main(config_path):
    if config_path:
        click.echo("Using config file")
    else:
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
            f.write(f"bot_token = \"{bot_token}\"\n")
            f.write(f"api = \"{api}\"\n")
            if api == "OpenAI":
                f.write(f"openai_api_key = \"{openai_api_key}\"\n")
            f.close()
    # Create the bot object
    Container = BotContainer(1) # TODO: Automatically parse the token from the config file

if __name__ == "__main__":
    main()