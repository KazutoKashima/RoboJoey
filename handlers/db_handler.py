#The main part of the program. This is where the bot actually starts.
#Check .git for creation and updates information
#Author: Johannes Nicholas, https://github.com/JohannesNicholas

import sqlite3


#executes an sql query on the database and returns the result
def execute(query, args=()):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute(query, args)
    result = c.fetchall()
    conn.commit()
    conn.close()
    return result



#ensures the database is setup
def setup():

    #poll tables
    execute("""CREATE TABLE IF NOT EXISTS polls ( 
        id INTEGER NOT NULL,
        results_id INTEGER NOT NULL,
        PRIMARY KEY (id)
    );""")

    execute("""CREATE TABLE IF NOT EXISTS poll_results (
        poll_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        selection INTEGER,
        FOREIGN KEY (poll_id) REFERENCES polls(id),
        PRIMARY KEY (poll_id, user_id)
    );""")


    #quiz tables
    execute("""CREATE TABLE IF NOT EXISTS quizzes ( 
        id INTEGER NOT NULL,
        results_id INTEGER NOT NULL,
        correct INTEGER NOT NULL,
        PRIMARY KEY (id)
    );""")

    execute("""CREATE TABLE IF NOT EXISTS quiz_selections (
        quiz_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        selection INTEGER,
        FOREIGN KEY (quiz_id) REFERENCES quizzes(id),
        PRIMARY KEY (quiz_id, user_id)
    );""")


    #table for zat113 check-ins
    execute("""CREATE TABLE IF NOT EXISTS student_ids (
        user_id INTEGER NOT NULL,
        student_id INTEGER NOT NULL,
        PRIMARY KEY (user_id)
    );""")




#saves a quiz into the database
def save_quiz(poll_id:int, results_id:int, correct:int):
    execute("INSERT INTO quizzes VALUES (?, ?, ?)", (poll_id, results_id, correct))

#saves a quiz selection into the database, selections can only be made once as this stores first time selections
def save_quiz_result(quiz_id:int, user_id:int, selection:int):
    execute("INSERT INTO quiz_selections VALUES (?, ?, ?)", (quiz_id, user_id, selection))

def get_quiz_answer(quiz_id:int):
    #Gets the correct answer for a quiz
    return execute("SELECT correct FROM quizzes WHERE id = ?", (quiz_id,))[0][0]

def get_quiz_results(quiz_id:int):
    """Gets the winners discord ids from a quiz
    returns winners as a list of ints representing the discord ids of the winners"""

    #get the correct answer
    correct = get_quiz_answer(quiz_id)

    #get the users who have selected the correct answer
    correct_users_query = execute("SELECT user_id FROM quiz_selections WHERE quiz_id = ? AND selection = ?", (quiz_id, correct))

    correct_users = []
    for row in correct_users_query:
        correct_users.append(row[0])

    #get the id of the message that contains the results
    results_id = execute("SELECT results_id FROM quizzes WHERE id = ?", (quiz_id,))[0][0]

    return results_id, correct_users
    




#saves a poll into the database
def save_poll(poll_id:int, results_id:int):
    execute("INSERT INTO polls VALUES (?, ?)", (poll_id, results_id))

#saves a poll result into the database
def save_poll_result(poll_id:int, user_id:int, selection:int):
    #if the user has not already voted, insert their selection
    if execute("SELECT * FROM poll_results WHERE poll_id = ? AND user_id = ?", (poll_id, user_id)) == []:
        execute("INSERT INTO poll_results VALUES (?, ?, ?)", (poll_id, user_id, selection))
    else:
        #if the user has already voted, update their selection
        execute("UPDATE poll_results SET selection = ? WHERE poll_id = ? AND user_id = ?", (selection, poll_id, user_id))

#gets the poll results for a poll
#returns result_id, counts. Where result_id is the id of the message that contains the results, and counts is a list of the number of votes for each option
def get_poll_results(poll_id:int):
    query_result = execute("SELECT selection FROM poll_results WHERE poll_id = ?", (poll_id,))
    counts = []
    for row in query_result:
        s = row[0] #the selection

        #if needed, expand counts to fit the selected option
        while len(counts) < s + 1:
            counts.append(0)

        counts[s] += 1

    #get the message id of the results message
    results_id = execute("SELECT results_id FROM polls WHERE id = ?", (poll_id,))[0][0]

    return results_id, counts


#sets the student id for a user
def set_student_id(user_id:int, student_id:int):
    #if the student already exists, update the id
    if execute("SELECT * FROM student_ids WHERE user_id = ?", (user_id,)) != []:
        execute("UPDATE student_ids SET student_id = ? WHERE user_id = ?", (student_id, user_id))
    #if the student does not exist, insert the id
    else:
        execute("INSERT INTO student_ids VALUES (?, ?)", (user_id, student_id))

#gets the student id for a user, returns -1 if not found
def get_student_id(user_id:int):
    result = execute("SELECT student_id FROM student_ids WHERE user_id = ?", (user_id,))
    if result == []:
        return -1
    else:
        return result[0][0]
        
