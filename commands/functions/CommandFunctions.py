import discord # We're using PyCord over Discord.py
import asyncio # Here we're using asyncio for better performance
from discord  import Bot, Embed
from commands.components.views import Poll_View, Quiz_View
import handlers.db_handler as db
from datetime import datetime

class CommandsFunctions:
    def __init__(self, bot: discord.Client, db: db):
        self.bot = bot

    async def createPoll(self, bot, ctx, question, options, emojis, descriptions):
        """Creates a poll"""

        await ctx.respond(question, 
            view=Poll_View(
                options=options.split(","), 
                emojis=emojis.split(","), 
                descriptions=descriptions.split(","), 
                bot=bot
            )
        )
        
        results_text = ""
        for i in range(len(options.split(","))):
            results_text += "0 - "
            if i < len(emojis.split(",")): #emoji if there is one
                results_text += emojis.split(",")[i] + ""

            results_text += options.split(",")[i] + "\n"
            

        await bot.get_channel(ctx.channel_id).send(results_text)

        messages = await ctx.channel.history(limit=2).flatten() #get those two sent messages

        poll_id = messages[1].id #the message id of the poll sent by the bot
        results_id = messages[0].id #the message of the results, directly after the poll

        self.db.save_poll(poll_id, results_id)
        print(f"Created poll {poll_id}, results {results_id}")

    async def createQuiz(self, bot, ctx, question, correct : int, options, emojis, descriptions):
        """Creates a quiz"""

        await ctx.respond(question, 
            view=Quiz_View(options=options.split(","), 
                emojis=emojis.split(","), 
                descriptions=descriptions.split(","), 
                bot=bot
            )
        )
        
        results_text = "People who got the correct answer first go:"
            

        await bot.get_channel(ctx.channel_id).send(results_text)

        messages = await ctx.channel.history(limit=2).flatten() #get those two sent messages

        quiz_id = messages[1].id #the message id of the poll sent by the bot
        results_id = messages[0].id #the message of the results, directly after the poll

        db.save_quiz(quiz_id, results_id, correct=correct)
        print(f"Created quiz {quiz_id}, results {results_id}")