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
    Bot = BotContainer(config)  # Create an instance of the BotContainer
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
        api = click.prompt(
            "Choose your API type",
            type=click.Choice(["Ollama", "OpenAI-like"], case_sensitive=False),
        )
        if api == "OpenAI-like":
            base_url = click.prompt(
                "Enter the base URL for the API", default="https://api.openai.com/v1"
            )
            openai_api_key = click.prompt("Enter the OpenAI API key")
        elif api == "Ollama":
            base_url = click.prompt(
                "Enter the base URL for the API", default="http://localhost:11434"
            )
        else:
            click.echo("Exiting...")
            sys.exit(1)
        model = click.prompt("LLM model to use", default="llama3")
    else:
        click.echo("Exiting...")
        sys.exit(1)

    # Base configuration common to all API types
    config = {
        "bot": {
            "token": bot_token,
            "guild_id": guild_id,
        },
        "ai": {
            "type": api,
        },
        "persona": {
            "default": {
                "prompt": "You are a helpful AI assistant.",
                "model": model,
            }
        },
    }

    # Update the configuration with API-specific settings
    if api == "OpenAI-like":
        config["ai"]["base_url"] = base_url
        config["ai"]["key"] = openai_api_key
    elif api == "Ollama":
        config["ai"]["base_url"] = base_url

    with open("config.toml", "w") as f:
        toml.dump(config, f)
    click.echo("Configuration file created.")
    # click.echo("Please edit the file to customize your bot.")
    # click.echo("Exiting...")
    # sys.exit(0)


if __name__ == "__main__":
    main()
