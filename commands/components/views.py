from commands.components.modals import CheckInModal, StudentIDModal
import discord # pycord
import handlers.db_handler as db

# The class for Poll Modal Views
class Poll_View(discord.ui.View):
    selectOptions = []# the list of options from which users can choose, a required field
    bot=None#the bot

    #initialization
    def __init__(self, options=["yes", "no"], emojis=[], descriptions=[], bot=None):
        self.selectOptions.clear()

        for i in range(len(options)):
            option = options[i]

            emoji = None
            if i < len(emojis):
                emoji = emojis[i].strip()
            if emoji == "":
                emoji = None

            description = None
            if i < len(descriptions):
                description = descriptions[i]
            
            self.selectOptions.append(
                discord.SelectOption(
                    label=option, 
                    value=str(i),
                    description=description,
                    emoji=emoji
                )
            )
        super().__init__(timeout=None) #persistent view


    @discord.ui.select(# the decorator that lets you specify the properties of the select menu
        placeholder = "Select", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maxmimum number of values that can be selected by the users
        options = selectOptions,
        custom_id="select-1"
    )
    
    async def select_callback(self, select, interaction: discord.Interaction): # the function called when the user is done selecting options
        await interaction.response.send_message("Thank you for your selection!", ephemeral=True)
        db.save_poll_result(interaction.message.id, interaction.user.id, select.values[0])

        results_id, results = db.get_poll_results(int(interaction.message.id))
        results_msg = await interaction.channel.fetch_message(results_id)

        lines = results_msg.content.split("\n")
        for i in range(len(lines)): #for each line in the message
            line_end = lines[i].split(" - ")[1] if " - " in lines[i] else lines[i] #get the end of the line
            bar = "" #the bar to be added to the line
            if i < len(results):
                for j in range(results[i]): #for each vote
                    bar += "█"
                bar += " " + str(results[i])
            else:
                bar = "0"

            lines[i] = bar + " - " + line_end #update the line


        

        await results_msg.edit(content="\n".join(lines))


#the view for a quiz message
class Quiz_View(discord.ui.View):
    selectOptions = []# the list of options from which users can choose, a required field
    bot=None#the bot

    #initialization
    def __init__(self, options=["yes", "no"], emojis=[], descriptions=[], bot=None):
        self.selectOptions.clear()

        for i in range(len(options)):
            option = options[i]

            emoji = None
            if i < len(emojis):
                emoji = emojis[i].strip()
            if emoji == "":
                emoji = None

            description = None
            if i < len(descriptions):
                description = descriptions[i]
            
            self.selectOptions.append(
                discord.SelectOption(
                    label=option, 
                    value=str(i),
                    description=description,
                    emoji=emoji
                )
            )
        super().__init__(timeout=None) #persistent view


    @discord.ui.select(# the decorator that lets you specify the properties of the select menu
        placeholder = "Select", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maxmimum number of values that can be selected by the users
        options = selectOptions,
        custom_id="select-1"
    )
    
    async def select_callback(self, select, interaction: discord.Interaction): # the function called when the user is done selecting options
        correct:int = db.get_quiz_answer(interaction.message.id)

        #respond to the user depending on if they got the correct answer
        print(f"{interaction.user.id} got {select.values[0]} correct is {correct}") 
        if int(select.values[0]) == int(correct):
            await interaction.response.send_message("Correct!", ephemeral=True)
        else:
            await interaction.response.send_message("Incorrect, try again", ephemeral=True) 


        db.save_quiz_result(interaction.message.id, interaction.user.id, select.values[0]) #save the result

        results_id, winners = db.get_quiz_results(int(interaction.message.id)) #get the results of the quiz

        results_msg = await interaction.channel.fetch_message(results_id) #get the message of the results

        results_text = "People who got the correct answer first go:\n"
        for winner in winners:
            results_text += f"<@{winner}> "

        await results_msg.edit(content=results_text)

#the view for the replies to the check in message
class CheckInView(discord.ui.View):
    check_in_msg = None

    #initialization
    def __init__(self, check_in_msg, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.check_in_msg = check_in_msg
        self.user_id = check_in_msg.author.id

        supportButton = discord.ui.Button(label='What is my student ID?', style=discord.ButtonStyle.url, url='https://askus.utas.edu.au/app/answers/detail/a_id/1060/~/what-is-my-utas-student-id-number%3F')
        self.add_item(supportButton)

    @discord.ui.button(label="Enter student ID", style=discord.ButtonStyle.primary) # Create a button
    async def button_callback(self, button, interaction):
        await interaction.response.send_modal(CheckInModal(title="Enter student ID", check_in_msg=self.check_in_msg, user_id=self.user_id))

class StudentIDView(discord.ui.View):
    @discord.ui.button(label="Enter student ID", style=discord.ButtonStyle.primary) # Create a button
    async def button_callback(self, button, interaction):
        await interaction.response.send_modal(StudentIDModal(title="Enter student ID"))