# Author: hhennessy20 and Shnabbydoodle
# 2/14/2024
# Copyright MMXXIV :)
# please dont steal!!!
# no copyright infringement intended!!!

import discord
import os
from openai import OpenAI
import asyncio
import random
import datetime

#Returns a channel with the specified server and channel name if exists
async def get_channel(discord_client, server_name, channel_name):
    for guild in discord_client.guilds:
        if guild.name == server_name:
            for channel in guild.channels:
                if isinstance(channel, discord.TextChannel) and channel.name == channel_name:
                    return channel
    return None

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
def run_bot(names, context_message, openai_key, discord_key, repetition_interval = 10, propose_conversation_starters_in = []):
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
    intents.members = True

    # Creates a new Discord client with the specified intents
    discord_client = discord.Client(intents=intents)

    # Event that runs when the bot is ready
    @discord_client.event
    async def on_ready():
        print('Logged in as')
        print(discord_client.user.name)
        print(discord_client.user.id)
        print('------')

        # Fetch all members to ensure the member cache is populated
        for guild in discord_client.guilds:
            async for member in guild.fetch_members():
                pass

        if propose_conversation_starters_in:
            # Schedule the task to send a message once per day
            await send_daily_message()

        # Function to send a message at a random time once per calendar day
    async def send_daily_message():
        global last_message_time

        last_message_time = None

        while True:
            # Check if it's time to send a message
            if last_message_time is None or datetime.datetime.now().date() > last_message_time.date():
                # Calculate a random time within the current day
                #random_hour = random.randint(0, 23)
                #random_minute = random.randint(0, 59)
                #random_second = random.randint(0, 59)
                random_hour = 22
                random_minute = 29
                random_second = 0
                scheduled_time = datetime.datetime.now().replace(hour=random_hour, minute=random_minute, second=random_second)

                # If the scheduled time is in the past, add one day to it
                if scheduled_time < datetime.datetime.now():
                    scheduled_time += datetime.timedelta(days=1)

                # Calculate the time difference to wait until the scheduled time
                time_difference = scheduled_time - datetime.datetime.now()

                # Wait until the scheduled time
                await asyncio.sleep(time_difference.total_seconds())
                for channel_list in propose_conversation_starters_in:
                    channel = await get_channel(discord_client, channel_list[0], channel_list[1])
                    if channel is not None:
                        # Get a random non-bot member from the server
                        member = random.choice([m for m in discord_client.get_all_members() if not m.bot])
                        username = member.name
                        if member.nick is not None:
                            username = member.nick
                        # Generate a message using OpenAI
                        generated_message = openai_client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[{"role": "system", "content": "Come up with an interesting and unique (not boring, something really out there) conversation starting question related to your character and propose it to " + username + ". Mention them by name! Also, frame this message as one of your daily questions!"}]
                        ).choices[0].message.content
                        # Send the message to the randomly chosen member
                        await channel.send(generated_message)
                        # Update the last message time
                        last_message_time = datetime.datetime.now()

            # Wait for 24 hours before checking again
            await asyncio.sleep(24 * 60 * 60)

            
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
                if len(messages) % repetition_interval == 0:
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
