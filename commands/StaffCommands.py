from typing_extensions import Self
import discord # We're using PyCord over Discord.py
import handlers.zat113_check_in as checkIn
import secrets
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(debug_guilds=["1002547684768485458"])

class StaffCog:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    #Check_ins command
    @commands.slash_command(guild_ids=["973788333169856542"],description = "Get a CSV of all the check ins. (Staff only)")
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
    @commands.slash_command(guild_ids=["973788333169856542"],description = "Manually set a students ID in the database. (Staff only)")
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

        
    @commands.slash_command(guild_ids=["973788333169856542"],description = "Make the bot say something (owner only)")
    async def say(self, ctx, message: discord.Option(str, "What the bot will say", required = True, default = 'Hi!')):
        if ctx.author.id == secrets.owner_id:
            await ctx.respond("Sending message", ephemeral=True)
            await self.bot.get_channel(ctx.channel_id).send(message)
        else:
            await ctx.respond("You are not the owner", ephemeral=True)   