import discord # We're using PyCord over Discord.py
from datetime import datetime
from discord import Embed
import commands.functions.CommandFunctions as CF
import handlers.db_handler as db
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(debug_guilds=["1002547684768485458"])

"""
    Cog is just the common name for Command Classes
    in Python bots.
"""
class UserCog:
    def __init__(self, bot: discord.Client):
        self.Modules = CF.CommandsFunctions(bot, db)
        self.bot = bot

    @commands.slash_command(description="About the Bot")
    async def about(self, ctx):
        """About the bot"""
        embed = Embed(
            title="Hi, I am a bot written in python by Johannes (Joey) Nicholas <@282428409685213184>", 
            description="Joey takes all responsibility for my actions", 
            color=0x00ff00
        ).add_field(name="Contact:", value="johannes.nicholas@utas.edu.au"
        ).add_field("View my source code:", value="https://github.com/JohannesNicholas/RoboJoe"
        ).set_footer(text="This bot is open source, and is licensed under the Apache (2.0) license"
        ).timestamp = datetime.now()
        await ctx.respond(embed=embed)

    #poll command
    @commands.slash_command(description = "Creates a poll")
    async def poll(self, ctx, 
        question: discord.Option(str, "The question being asked", required = True, default = 'Do you agree?'),
        options: discord.Option(str, "Selectable options to the question. Separated by a comma (,)", required = False, default = 'Yes,No'),
        emojis: discord.Option(str, "An emoji for each option. Separated by a comma (,)", required = False, default = ''),
        descriptions: discord.Option(str, "A description for each option. Separated by a comma (,)", required = False, default = ''),
    ):
        await self.Modules.createPoll(self.bot, ctx, question, options, emojis, descriptions)

    #quiz command
    @commands.slash_command(description = "Creates a multiple choice quiz")
    async def quiz(self, ctx, 
        question: discord.Option(str, "The question being asked", required = True, default = 'Is this true?'),
        options: discord.Option(str, "Selectable options to the question. Separated by a comma (,)", required = False, default = 'Yes,No'),
        correct: discord.Option(int, "The correct index (starting at 0)", required = True, default = 0),
        emojis: discord.Option(str, "An emoji for each option. Separated by a comma (,)", required = False, default = ''),
        descriptions: discord.Option(str, "A description for each option. Separated by a comma (,)", required = False, default = ''),
    ):
        await self.Modules.createQuiz(self.bot, ctx, question, correct, options, emojis, descriptions)
    
    @commands.slash_command(description="Says Hello!")
    async def hello(self, ctx):
        await ctx.respond("Hello!")

    #ping command
    @commands.slash_command(description = "The delay from the discord server to the bot")
    async def ping(self, ctx):
        await ctx.respond(str(int(self.bot.latency * 1000))+ "ms")