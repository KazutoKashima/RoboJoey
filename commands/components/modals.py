import discord # pycord
import handlers.db_handler as db

# the modal for entering student IDs
class CheckInModal(discord.ui.Modal):
    check_in_msg = None

    def __init__(self, check_in_msg, user_id, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.check_in_msg = check_in_msg
        self.user_id = user_id #the user id of the user who checked in
    
        self.add_item(discord.ui.InputText(label="Student id", placeholder="123456", min_length=6, max_length=6))

    async def callback(self, interaction: discord.Interaction):
        
        #check the student id
        sid = self.children[0].value
        if not sid.isdigit() or len(sid) != 6:
            #tell the user they entered an invalid student id
            await interaction.response.send_message(f"'{sid}' does not seem to be a student ID", ephemeral=True)
            return 


        db.set_student_id(interaction.user.id, int(sid))#save the student id
        await interaction.response.send_message(f"Thank you <@{interaction.user.id}> for your student ID", ephemeral=True)
        
        #if the user who checked in entered their student id
        if interaction.user.id == self.user_id:
            await interaction.message.delete()
            await self.check_in_msg.add_reaction('🎫')

class StudentIDModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Student id", placeholder="123456"))

    async def callback(self, interaction: discord.Interaction):
        print(self.children[0].value)
        await interaction.response.send_message("Thank you!", ephemeral=True) 

