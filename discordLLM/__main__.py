import discord
import click
import sys
@click.command()
@click.option("--bot-token", prompt="Your discord bot token", help="Discord Bot Token", hide_input=True, confirmation_prompt=True)


def main(token):
    print("Your bot token is: ", token)
    pass

if __name__ == "__main__":
    main()