import click
import sys
from discord_llm.bot import BotContainer
import toml
import os


@click.command()
@click.option("--config-path", help="Path to the config file")
def main(config_path):
    # Check for a config file
    config_path = check_config(config_path)

    # Load the configuration file
    config = toml.load(config_path)
    Bot = BotContainer(
        config["BOT"]["bot_token"],
        config["BOT"]["guild_id"],
        config["BOT"]["api"],
        config["BOT"]["key"],
        config["BOT"]["default_persona"],
    )  # Create an instance of the BotContainer
    # Persona creation is handled automagically by BotContainer
    Bot.register_events()  # Register the events that the bot will respond to
    Bot.run()  # Run the bot!


def check_config(config_path):
    if config_path:
        if os.path.exists(config_path):
            click.echo("The provided config file exists. Continuing...")
            return config_path
        else:
            click.echo("The provided config file does not exist.")
            create_config()
            return "config.toml"
    elif os.path.exists("config.toml"):
        click.echo("Found config.toml in working directory. Continuing...")
        return "config.toml"
    else:
        click.echo("No config file provided.")
        click.echo("No config file found in working directory.")
        create_config()
        return "config.toml"


def create_config():
    if click.prompt("Create one in working directory? (y/n)").lower() == "y":
        bot_token = click.prompt("Enter your bot token")
        guild_id = click.prompt("Enter your guild id")
        if click.prompt("Use the OpenAI api? (y/n)").lower() == "y":
            openai_api_key = click.prompt("Enter your OpenAI api key")
            api = "OpenAI"
        else:
            click.echo("Defaulting to Ollama")
            api = "Ollama"
    else:
        click.echo("Exiting...")
        sys.exit(1)

    # Create the TOML configuration file
    with open("config.toml", "w") as f:
        f.write("[BOT]\n")
        f.write(f'bot_token = "{bot_token}"\n')
        f.write(f"guild_id = {guild_id}\n")
        f.write(f'api = "{api}"\n')
        f.write('default_persona = "ASSISTANT"\n')
        if api == "OpenAI":
            f.write(f'key = "{openai_api_key}"\n')
            f.write("\n[PERSONAS]\n")
            f.write("[PERSONA-ASSISTANT]")
            f.write('model = "gpt-3.5-turbo"\n')
            f.write('prompt = "You are a helpful AI assistant."\n')
        else:
            f.write(f'key = "0"\n')
            f.write("\n[PERSONAS]\n")
            f.write("[PERSONA-ASSISTANT]\n")
            f.write('model = "llama3"\n')
            f.write('prompt = "You are a helpful AI assistant."\n')

        f.close()


if __name__ == "__main__":
    main()
