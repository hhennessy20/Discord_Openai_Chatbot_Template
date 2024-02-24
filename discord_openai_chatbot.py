import discord
import os
from openai import OpenAI
import asyncio
import random

# [name.upper() for name in names]


def run_bot(name, context_message, openai_key, discord_key):
    openai_client = OpenAI(
        # This is the default and can be omitted
        api_key= openai_key
    )

    # Create the array of messages the bot will receive and initialize its personality
    messages = []
    messages.append({"role": "system", "content": context_message})
    # Define the intents your bot will use
    intents = discord.Intents.default()
    intents.message_content = True

    # Create a new Discord client with the specified intents
    discord_client = discord.Client(intents=intents)

    # Event that runs when the bot is ready
    @discord_client.event
    async def on_ready():
        print('Logged in as')
        print(discord_client.user.name)
        print(discord_client.user.id)
        print('------')

    # Event that runs whenever a message is sent in a channel the bot can see
    @discord_client.event
    async def on_message(message):
        # Check if the message contains name
        if name.upper() in message.content.upper() and message.author != discord_client.user:
            username = message.author.name
            if (message.channel.type is not (discord.ChannelType.private or discord.ChannelType.group)) and username is not None:
                username = message.author.nick
            await asyncio.sleep(random.randint(0,500)/100)
            async with message.channel.typing():
                if len(messages) % 10 == 0:
                    messages.append({"role": "system", "content": "Please remember and adhere to the following: " + context_message})
                messages.append({"role": "user", "content": username + " says: " + message.content})
                chgpt_response = openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages)
                # Respond with a generated message
                response = chgpt_response.choices[0].message.content
                messages.append({"role": "assistant", "content": response})
                await asyncio.sleep(.01 * len(response))
                await message.channel.send(response)

    # Run the bot with your Discord token
    discord_client.run(discord_key)
