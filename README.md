# Discord_Openai_Chatbot_Template
A simple openai chatbot and template to create and run it, created as a personal project by hhennessy20 and shnabbydoodle.

You'll need to have Python and the discord and openai libraries, as well as asyncio. Use "pip install [package-name]" for these.

This can be done in a virtual environment using the venv command, documentation for which can be found here:
https://docs.python.org/3/library/venv.html

In addition, you'll need to create an OpenAI account and obtain an API key here:
https://platform.openai.com/api-keys

You'll also need to set up a bot on Discord's Application page here:
https://discord.com/developers/applications

Once created, on the bot's page under Privileged Gateway Intents, you'll need to enable SERVER MEMBERS INTENT and MESSAGE CONTENT INTENT.

Then, under the OAuth2 tab, within OAuth2 URL Generator, select "bot", which will open a list of further permissions. Select "Read Messages/View Channels", "Send Messages", and "Read Message History".

With these options checked, copy the generated link and invite the bot to your server of choice.

Once the bot is added to a server, copy the Discord Key from the Developer Portal and the OpenAI key into the template file. Add the names you'd like your bot to be called with to the names array, and add a detailed context statement.

Finally, if you'd like, add in a custom value for the reminder frequency as well as any servers and channels you'd like the bot to post a daily question to. Run the template file, and your bot should come online!
