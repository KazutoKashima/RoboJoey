#Handles most of the code for the checking in assignment in ZAT113 
#Check .git for creation and updates information
#Author: Johannes Nicholas, https://github.com/JohannesNicholas

import discord # pycord
import handlers.db_handler as db
import csv
from commands.components.views import CheckInView as View

# When a message is sent anywhere
async def message(message):

    #ignore messages in other channels
    if message.channel.id not in [994167372942413906, 994121873816293407]:
        return

    #ignore messages from bots
    if message.author.bot:
        return

    #if we don't have the student id
    if db.get_student_id(message.author.id) == -1:
        #ask the user for their student id
        await message.channel.send(f"""Thank you <@{message.author.id}> for your check in!
I don't seem to have your student ID yet.""", 
        view=View(check_in_msg=message))

    else:
        await message.add_reaction('🎫')

#returns a csv file of all the check ins
async def get_check_ins(channel_id:int, bot:discord.Bot):
    file_path = 'check_ins.csv' # a temporary file to store the check ins

    with open(file_path, 'w', encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Student ID', 'Message', 'Time', 'Link to message', 'student discord name', 'student discord ID'])

        channel = bot.get_channel(channel_id)

        async for message in channel.history(limit=None, oldest_first=True):
            time = message.created_at.strftime("%d/%m/%Y %H:%M:%S")
            if message.edited_at is not None:
                time = message.edited_at.strftime("%d/%m/%Y %H:%M:%S")

            
            writer.writerow([db.get_student_id(message.author.id), message.content, time, message.jump_url, message.author.display_name, message.author.id])


    print("compiled all messages")

    return discord.File(fp=file_path)

