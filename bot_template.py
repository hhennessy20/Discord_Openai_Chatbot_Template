import discord_openai_chatbot

#Enter the name(s) you'd like to use to call your bot with
names = ["NAME", "NAME_2", "NAME_N"]

#Give the AI a few sentences about how it should characterize your bot. Example:
# "You are David Lynch. You're a member of a chat server. Keep your responses to around a paragraph or less in length. Try not to mention that you're actually an AI. Stay in character. For 1 tenth of all responses, instead of answering, just reply 'No.'"
context_message = "CONTEXT_MESSAGE"

#Enter your API Key here from: https://platform.openai.com/api-keys
openai_key = 'OPENAI_KEY'

#Enter your Discord bot's key here after setting it up here: https://discord.com/developers/applications
discord_key = 'DISCORD_KEY'

# Optional parameter with default value of 10 to set how often the bot is reminded of its context message
repetition_interval = 10

# Optional parameter with default value of empty. Example input [["My Server", "general"], ["Friend's Server", "bot-chat-channel"]].
propose_conversation_starters_in = []

discord_openai_chatbot.run_bot(names, context_message, openai_key, discord_key)
