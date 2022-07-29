#The main part of the program. This is where the bot actually starts.
#Check .git for creation and updates information
#Author: Johannes Nicholas, https://github.com/JohannesNicholas

import os
from commands.StaffCommands import StaffCog
from commands.UserCommands import UserCog
import discord
from discord.ext import commands # pycord
import handlers.zat113_check_in as checkIn
from commands.components.views import Quiz_View, Poll_View
import secrets
import handlers.db_handler as db
from discord import Embed
import commands.functions.CommandFunctions as CF
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(debug_guilds=["1002547684768485458"])
db.setup()

@bot.event
async def on_ready():
    # Add persistency to the views
    bot.add_view(Poll_View(bot=bot)) 
    bot.add_view(Quiz_View(bot=bot)) 

    print(f"""
        Logged in as {bot.user}\n
        Bot ID: {bot.user.id}\n
        Guild Count: {len(bot.guilds)}
        Guild Names: {[guild.name for guild in bot.guilds]}
    """)
    print("Loading Commands Handlers...please wait.")
    bot.add_cog(StaffCog(bot, db))
    bot.add_cog(UserCog(bot))
    print("Commands Handlers Loaded!")

#when someone sends a message, any message
@bot.event
async def on_message(message: discord.Message):
    # We do not want the bot to reply to itself or any other bots
    if message.author == bot.user: 
        return
    await checkIn.message(message)

"""
#used to log everything
async def log(message):
    print("Log: " + message)
    await bot.get_channel(994423152924966932).send(message)
"""
class UserCog(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.Modules = CF.CommandsFunctions(bot, db)
        self.bot = bot

    @bot.slash_command(description="About the Bot")
    async def about(self, ctx):
        """About the bot"""
        embed = Embed(
            title="Hi, I am a bot written in python by Johannes (Joey) Nicholas <@282428409685213184>", 
            description="Joey takes all responsibility for my actions", 
            color=0x00ff00
        )
        embed.add_field(name="Contact:", value="johannes.nicholas@utas.edu.au"
        )
        embed.add_field(name="View my source code:", value="https://github.com/JohannesNicholas/RoboJoe"
        )
        embed.set_footer(text="This bot is open source, and is licensed under the Apache (2.0) license"
        )
        embed.timestamp = datetime.now()
        await ctx.respond(embed=embed)

    #poll command
    @bot.slash_command(description = "Creates a poll")
    async def poll(self, ctx, 
        question: discord.Option(str, "The question being asked", required = True, default = 'Do you agree?'),
        options: discord.Option(str, "Selectable options to the question. Separated by a comma (,)", required = False, default = 'Yes,No'),
        emojis: discord.Option(str, "An emoji for each option. Separated by a comma (,)", required = False, default = ''),
        descriptions: discord.Option(str, "A description for each option. Separated by a comma (,)", required = False, default = ''),
    ):
        await self.Modules.createPoll(self.bot, ctx, question, options, emojis, descriptions)

    #quiz command
    @bot.slash_command(description = "Creates a multiple choice quiz")
    async def quiz(self, ctx, 
        question: discord.Option(str, "The question being asked", required = True, default = 'Is this true?'),
        options: discord.Option(str, "Selectable options to the question. Separated by a comma (,)", required = False, default = 'Yes,No'),
        correct: discord.Option(int, "The correct index (starting at 0)", required = True, default = 0),
        emojis: discord.Option(str, "An emoji for each option. Separated by a comma (,)", required = False, default = ''),
        descriptions: discord.Option(str, "A description for each option. Separated by a comma (,)", required = False, default = ''),
    ):
        await self.Modules.createQuiz(self.bot, ctx, question, correct, options, emojis, descriptions)
    
    @bot.slash_command(description="Says Hello!")
    async def hello(self, ctx):
        await ctx.respond("Hello!")

    #ping command
    @bot.slash_command(description = "The delay from the discord server to the bot")
    async def ping(self, ctx):
        await ctx.respond(str(int(self.bot.latency * 1000))+ "ms")
class StaffCog(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    #Check_ins command
    @bot.slash_command(guild_ids=["973788333169856542"],description = "Get a CSV of all the check ins. (Staff only)")
    async def check_ins(self, ctx : discord.ApplicationContext):

        await ctx.defer(ephemeral=True)

        #guard if the user is not staff
        if ctx.author.id not in secrets.zat113_staff:
            await ctx.respond("You are not a staff member.", ephemeral=True)
            return
            
        #send the file privately
        file = await checkIn.get_check_ins(ctx.channel_id, bot=self.bot)
        print(file.fp)
        await ctx.respond("check ins:", file=file, ephemeral=True)


    #Manually set a students ID
    @bot.slash_command(guild_ids=["973788333169856542"],description = "Manually set a students ID in the database. (Staff only)")
    async def set_student_id(self, ctx : discord.ApplicationContext, 
        discord_id: discord.Option(str, "The students Discord ID", required = True, default = ""),
        student_id: discord.Option(str, "The students ID", required = True, default = ""),
        ):
        if ctx.author.id not in secrets.zat113_staff:
            await ctx.respond("You are not a staff member.", ephemeral=True)
            return

        if not discord_id.isdigit():
            await ctx.respond("discord id must be an integer, right click the user and select copy ID.", ephemeral=True)
            return

        if not student_id.isdigit():
            await ctx.respond("student id must be an integer", ephemeral=True)
            return

        self.db.set_student_id(int(discord_id), int(student_id))
        await ctx.respond("Saved!.", ephemeral=True)

        
    @bot.slash_command(guild_ids=["973788333169856542"],description = "Make the bot say something (owner only)")
    async def say(self, ctx, message: discord.Option(str, "What the bot will say", required = True, default = 'Hi!')):
        if ctx.author.id == secrets.owner_id:
            await ctx.respond("Sending message", ephemeral=True)
            await self.bot.get_channel(ctx.channel_id).send(message)
        else:
            await ctx.respond("You are not the owner", ephemeral=True)   

#run the bot
bot.run(secrets.botToken)