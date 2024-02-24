# Author: hhennessy20 and Shnabbydoodle
# 2/14/2024
# Copyright MMXXIV :)

import discord
import os
from openai import OpenAI
import asyncio
import random

#Returns true if any name is in message
def name_in_message(names, message):
    name_in_message = False
    for name in names:
        if name.upper() in message.upper():
            name_in_message = True
    return name_in_message

def too_many_bots(message_is_bot):
    counter = 0
    for message in message_is_bot[-4:]:
        if message[0] and not message[1]:
            counter += 1
    # Debug line to print the counter
    # print(counter)
    if counter > 2:
        return True
    return False

# Main command for running bot
def run_bot(names, context_message, openai_key, discord_key):
    openai_client = OpenAI(
        api_key= openai_key
    )

    # Creates the array of messages the bot will receive and initialize its personality
    messages = []
    message_is_bot = []
    messages.append({"role": "system", "content": context_message})
    # Defines the intents your bot will use
    intents = discord.Intents.default()
    intents.message_content = True

    # Creates a new Discord client with the specified intents
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
        # Checks if the message contains name
        if (name_in_message(names, message.content) and message.author != discord_client.user):

            # Debug line to print all messages received by the bot
            # print(message.content)

            # Checks if message is bot
            if message.author.bot and message.author == discord_client.user:
                message_is_bot.append([True, True])
            elif message.author.bot:
                message_is_bot.append([True, False])
            else:
                message_is_bot.append([False, False])

            if message.author.bot and too_many_bots(message_is_bot):
                return
            
            # Gets name or nickname of user to append to bot message
            username = message.author.name
            if (message.channel.type is not (discord.ChannelType.private or discord.ChannelType.group)) and message.author.nick is not None:
                username = message.author.nick

            # Simulates a few seconds of bot reading your message
            await asyncio.sleep(random.randint(0,500)/100)

            # Bot will appear to be typing while it generates your message
            async with message.channel.typing():
                # Reminds the bot about itself every 10 messages
                if len(messages) % 10 == 0:
                    messages.append({"role": "system", "content": "Please remember and adhere to the following: " + context_message})
                
                # Sends your message to openai and gets response
                messages.append({"role": "user", "content": username + " says: " + message.content})
                chgpt_response = openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages)
                response = chgpt_response.choices[0].message.content

                # Adds response to bot context so it remembers
                messages.append({"role": "assistant", "content": response})
                
                # Simulates the bot typing your message, slightly longer depending on the length of the message
                await asyncio.sleep(.01 * len(response))
                await message.channel.send(response)

    # Runs the bot with your Discord token
    discord_client.run(discord_key)
