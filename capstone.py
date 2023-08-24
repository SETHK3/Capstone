import sqlite3
import bcrypt
import csv
from datetime import datetime

# Initialize connection
connection = sqlite3.connect('competency_app.db')
cursor = connection.cursor()
   
# csv_file_path = 'mock_data.csv'
# with open(csv_file_path, 'r') as csv_file:
#     csv_read = csv.DictReader(csv_file)

#     for row in csv_read:
#         hashed_password = bcrypt.hashpw(row.get("password").encode('utf-8'), bcrypt.gensalt())
#         decoded_password = hashed_password.decode('utf-8')
#         sql_command = 'INSERT INTO Users (first_name, last_name, phone, email, password, active, date_created, hire_date, user_type) VALUES("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}");'.format(row.get("first_name"), row.get("last_name"), row.get("phone"), row.get("email"), decoded_password, row.get("active"), row.get("date_created"), row.get("hire_date"), row.get("user_type"))        
#         cursor.execute(sql_command)

#     connection.commit()

# csv_file_path = 'assessment_results.csv'
# with open(csv_file_path, 'r') as csv_file:
#     csv_read = csv.DictReader(csv_file)

#     for row in csv_read:
#         sql_command = "INSERT INTO Assessment_Results (user_id, assessment_id, competency_score, date_taken, manager_id) VALUES('{}', '{}', '{}', '{}', '{}')".format(row.get("user_id"), row.get("assessment_id"), row.get("competency_score"), row.get("date_taken"), row.get("manager_id"))
#         cursor.execute(sql_command)

#     connection.commit()
# Functions below to hash a password/login/logout

def login(password,email):

    sql_command = "SELECT password, user_type, email,user_id FROM Users WHERE email = '{}' LIMIT 1".format(email)

    try:
        results = cursor.execute(sql_command).fetchone()
    except:
        print("The email or password was incorrect.")
        return "",False,""
    hashed_password = results[0]
    user_type = results[1]
    email = results[2]
    user_id = results[3]
  

    if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
        print("Login successful")
        return user_type, email,user_id

    else:
        print("The email or password was incorrect.")
        return "",False,""
    
def logout():
    print("Logged out successfully.")
    return None, None

# Functions for user actions

# View Own Competency Summary Reference Function view_user_competency_summary

def edit_user_info():
    first_name = input('Update first name: ')
    last_name = input('Update last name: ')
    password = input('Input new password: ')

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    decoded_password = hashed_password.decode('utf-8')

    sql_command = "UPDATE Users SET first_name = '{}' and last_name = '{}' and password = '{}'".format(first_name, last_name, decoded_password)
    cursor.execute(sql_command)
    connection.commit
    pass

# Functions for manager actions
def view_all_users():
    sql_command = "SELECT user_id, first_name, last_name, phone, email, active, date_created, hire_date, user_type FROM Users"
    rows = cursor.execute(sql_command).fetchall()
    print(f'\n{"User ID":<10}{"First Name":<15}{"Last Name":<15}{"Phone":<15}{"Email":<30}{"Active":<10}{"Date Created":<15}{"Hire Date":<15}{"User Type":<10}')
    print(f'{"-"*7:<10}{"-"*10:<15}{"-"*9:<15}{"-"*5:<15}{"-"*5:<30}{"-"*6:<10}{"-"*12:<15}{"-"*9:<15}{"-"*9:<10}')

    for row in rows:
        cleaned_list = [x if x is not None else "" for x in row]
        print(f'{cleaned_list[0]:<10}{cleaned_list[1]:<15}{cleaned_list[2]:<15}{cleaned_list[3]:<15}{cleaned_list[4]:<30}{cleaned_list[5]:<10}{cleaned_list[6]:<15}{cleaned_list[7]:<15}{cleaned_list[8]:<10}')
    pass

def search_users():
    user_search = input('\nType first or last name to search: \n')

    sql_command = "SELECT user_id, first_name, last_name, phone, email, active, date_created, hire_date, user_type FROM Users WHERE first_name LIKE '%{}%' OR last_name LIKE '%{}%'".format(user_search,user_search)
    rows = cursor.execute(sql_command).fetchall()
    print(f'\n{"User ID":<10}{"First Name":<15}{"Last Name":<15}{"Phone":<15}{"Email":<30}{"Active":<10}{"Date Created":<15}{"Hire Date":<15}{"User Type":<10}')
    print(f'{"-"*7:<10}{"-"*10:<15}{"-"*9:<15}{"-"*5:<15}{"-"*5:<30}{"-"*6:<10}{"-"*12:<15}{"-"*9:<15}{"-"*9:<10}')

    for row in rows:
        cleaned_list = [x if x is not None else "" for x in row]
        print(f'{cleaned_list[0]:<10}{cleaned_list[1]:<15}{cleaned_list[2]:<15}{cleaned_list[3]:<15}{cleaned_list[4]:<30}{cleaned_list[5]:<10}{cleaned_list[6]:<15}{cleaned_list[7]:<15}{cleaned_list[8]:<10}')
    pass

def view_competency_result_summary():
    sql_command = "SELECT name, competency_id FROM Competencies"
    rows = cursor.execute(sql_command).fetchall()
    print(f'\n{"Name":<20}{"Competency ID":<15}')
    print(f'{"-"*4:<20}{"-"*12:<15}')

    for row in rows:
        cleaned_list = [x if x is not None else "" for x in row]
        print(f'{cleaned_list[0]:<10}{cleaned_list[1]:<15}')
    competency_id = input('Input Competency ID to view Summary')

    sql_command = """
    SELECT name, AVG(competency_score) AS average_score
    FROM Competency_Assessments c
    JOIN Assessment_Results a on c.assessment_id = c.assessment_id
    WHERE c.competency_id = {}
    """.format(competency_id)
    
    rows = cursor.execute(sql_command).fetchall()
    print(f'{"Name":<20}{"Average Score":<10}')
    for row in rows:
        print(f'{row[0]:<20}{row[1]:<10}')
    pass

    sql_command = """
    SELECT first_name, last_name, competency_score, name, date_taken
    FROM Users u
    JOIN Assessment_Results r on u.user_id = r.user_id
    JOIN Competency_Assessments a on a.assessment_id = r.assessment_id
    """.format(user_id)
    
    rows = cursor.execute(sql_command).fetchall()
    print(f'{"First Name":<10}{"Last Name":<10}{"Score":<10}{"Assessment Name":<10}{"Date Taken":<10}')
    
    for row in rows:
        print(f'{row[0]:<10}{row[1]:<10}{row[2]:<10}{row[3]:<10}{row[4]:<10}')
    pass

def view_user_competency_summary(flag,user_id):
    if flag:
        user_id = int(input("What is the User ID: "))

    sql_command = "SELECT first_name, last_name, email FROM Users WHERE user_id = {}".format(user_id)
    user_rows = cursor.execute(sql_command).fetchone()

    sql_command = "SELECT name FROM Competencies".format(user_id)
    rows = cursor.execute(sql_command).fetchall()
    competency_list =[]
    for row in rows:
        competency_list.append(row[0])

    sql_command = """
    SELECT c.name, competency_score, date_taken 
    FROM Competencies c
    JOIN Competency_Assessments  ca on c.competency_id = ca.competency_id
    JOIN Assessment_Results a on a.assessment_id = ca.assessment_id
    WHERE a.user_id = {}""".format(user_id)
    
    try:
        rows = cursor.execute(sql_command).fetchall()
        
        count = 0
        total = 0
        for row in rows:
            count += 1
            total += int(row[1])
        average_score = total/count
    except:
        print("That was not a valid User ID.")
        return

    values = {}
    values_dates = {}

    for row in rows:
        if values.get(row[0]):
            print(values.get(row[0]))
            print(values[row[0]])
            print(values[row[0]][1])
            if datetime.strptime(values[row[0]][1], '%m/%d/%Y')<datetime.strptime(row[2], '%m/%d/%Y'):
                values[row[0]]= [int(row[1]),row[2]]
        else:
            values[row[0]]=int(row[1]),row[2]

    print(f'\n{"First Name":<15}{"Last Name":<15}{"Email":<20}{"Total Average Score":<10}')
    print(f'{"-"*12:<15}{"-"*11:<15}{"-"*7:<20}{"-"*21:<10}')
    print(f'{user_rows[0]:<15}{user_rows[1]:<15}{user_rows[2]:<20}{average_score:<10}')
    print(f'\n{"Competency Name":<20}{"Competency Score":<15}')
    print(f'{"-"*17:<20}{"-"*18:<15}')

    for x in competency_list:
        if values.get(x):
            print(f'{x:<20}{values[x][0]:<15}')
        else:
            print(f'{x:<20}{0:<15}') 
    pass

def add_user():
    first_name = input('First name: ')
    last_name = input('Last name: ')
    phone = input('Phone number: ')
    email = input('Email: ')
    password = input('Password: ')
    active = input('Active status (0 or 1): ')
    date_created = input('Date Account Created (mm/dd/yyyy): ')
    hire_date = input('Date of hire (mm/dd/yyyy): ')
    user_type = input('User or Manager: ').lower()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    decoded_password = hashed_password.decode('utf-8')
    
    sql_command = 'INSERT INTO Users (first_name, last_name, phone, email, password, active, date_created, hire_date, user_type) VALUES("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}");'.format(first_name, last_name, phone, email, decoded_password, active, date_created, hire_date, user_type)
    print(sql_command)
    cursor.execute(sql_command)
    if user_type == 'manager':
        sql_command = "SELECT user_id FROM Users ORDER BY user_id DESC LIMIT 1"
        results = cursor.execute(sql_command).fetchone()
        user_id = results[0]
        sql_command = "INSERT INTO Managers (user_id, promotion_date) VALUES({}, '08/14/22')".format(user_id)
        cursor.execute(sql_command)
    connection.commit()
    pass

def add_competency():
    name = input('Competency name: ')
    date_created = input('Date of creation (mm/dd/yyyy): ')

    sql_command = "INSERT INTO Competencies (name, date_created) VALUES('{}', '{}')".format(name, date_created)
    
    cursor.execute(sql_command)
    connection.commit()

    print(f'\nCompetency has been added: {name}, {date_created}')
    pass

def add_assessment():
    competency_name = input("Which Competency is this for? Enter the Name: ")
    name = input('Assessment name: ')
    date_created = input('Date of creation (mm/dd/yyyy): ')
    
    sql_command = "SELECT competency_id FROM Competencies WHERE name = '{}' LIMIT 1".format(competency_name)
    print(sql_command)
    try:
        results = cursor.execute(sql_command).fetchone()
        print(results)
        competency_id = results[0]

    except:
        print("The Competency could not be found.")
        pass
    
    competency_id = results[0]

    sql_command = "INSERT INTO Competency_Assessments(competency_id, name, date_created) VALUES({},'{}', '{}')".format(competency_id, name, date_created)
    cursor.execute(sql_command)
    connection.commit()

    print(f'\nAssessment has been added: {name}, {date_created}')
    pass

def add_assessment_result():
    user_id = int(input("What is the User ID: "))

    sql_command = "SELECT name, assessment_id FROM Competency_Assessments"
    rows = cursor.execute(sql_command).fetchall()
    print(f'\n{"Name":<20}{"Assessment ID":<15}')
    print(f'{"-"*4:<20}{"-"*12:<15}')

    for row in rows:
        cleaned_list = [x if x is not None else "" for x in row]
        print(f'{cleaned_list[0]:<10}{cleaned_list[1]:<15}')
    
    
    assessment_id = input('Input Assessment ID: ')
    competency_score = input('Input given Competency Score (0-4): ')
    date_taken = input('Date Assessment was taken (mm/dd/yyyy): ')
    manager_id = input('Input ID of Manager present: ')

    sql_command = "INSERT INTO Assessment_Results (user_id, assessment_id, competency_score, date_taken, manager_id) VALUES('{}', '{}', '{}', '{}', '{}')".format(user_id, assessment_id, competency_score, date_taken, manager_id)
    cursor.execute(sql_command)
    connection.commit()
    pass

def edit_user():
    sql_command = "SELECT user_id, first_name, last_name, phone, active, user_type FROM Users"
    rows = cursor.execute(sql_command).fetchall()
    print(f'\n{"User ID":<10}{"First Name":<15}{"Last Name":<15}{"Phone":<15}{"Active":<10}{"User Type":<10}')
    print(f'{"-"*7:<10}{"-"*10:<15}{"-"*9:<15}{"-"*5:<15}{"-"*6:<10}{"-"*9:<10}')

    for row in rows:
        cleaned_list = [x if x is not None else "" for x in row]
        print(f'{cleaned_list[0]:<10}{cleaned_list[1]:<15}{cleaned_list[2]:<15}{cleaned_list[3]:<15}{cleaned_list[4]:<10}{cleaned_list[5]:<10}')

    user_id = input('\nInput User ID to edit: ')
    first_name = input('Update first name: ')
    last_name = input('Update last name: ')
    active = input('Active Status (0 or 1): ')

    sql_command = "UPDATE Users SET first_name = '{}', last_name = '{}', active = '{}' WHERE user_id = {}".format(first_name, last_name, active, user_id)
    cursor.execute(sql_command)
    connection.commit()
    pass

def edit_competency():
    sql_command = "SELECT * FROM Competencies"
    rows = cursor.execute(sql_command).fetchall()
    print(f'\n{"Competency ID":<15}{"Name":<20}{"Date Created":<20}')
    print(f'{"-"*13:<15}{"-"*8:<20}{"-"*12:<20}')

    for row in rows:
        print(f'{row[0]:<15}{row[1]:<20}{row[2]:<20}')
        
    competency_id = input('\nInput Competency ID to edit: ')
    name = input('Update Competency Name: ')
    date_created = input('Input new date created (mm/dd/yyyy): ')


    sql_command = "UPDATE Competencies SET name = '{}', date_created = '{}' WHERE competency_id = {}".format(name, date_created, competency_id)
    cursor.execute(sql_command)
    connection.commit()

    print(f'\nCompetency has been updated: {name}, {date_created}')
    pass

def edit_assessment():
    sql_command = "SELECT * FROM Competency_Assessments"
    rows = cursor.execute(sql_command).fetchall()
    print(f'\n{"Competency ID":<15}{"Assessment ID":<15}{"Name":<20}{"Date Created":<20}')
    print(f'{"-"*13:<15}{"-"*13:<15}{"-"*8:<20}{"-"*12:<20}')

    for row in rows:
        print(f'{row[0]:<15}{row[1]:<15}{row[2]:<20}{row[3]:<20}')

    assessment_id = input('\nInput Assessment ID to edit: ')
    name = input('Update Assessment name: ')
    date_created = input('Input new date created (mm/dd/yyyy): ')

    sql_command = "UPDATE Competency_Assessments SET name = '{}', date_created = '{}' WHERE assessment_id = {}".format(name, date_created, assessment_id)
    rows = cursor.execute(sql_command)
    connection.commit()

    print(f'\nAssessment has been updated: {name}, {date_created}')
    pass

def edit_assessment_result():
    sql_command = "SELECT * FROM Assessment_Results"
    rows = cursor.execute(sql_command).fetchall()
    print(f'\n{"Result ID":<10}{"User ID":<10}{"Assessment ID":<15}{"Competency Score":<20}{"Date Taken":<15}{"Manager ID":<15}')
    print(f'{"-"*9:<10}{"-"*7:<10}{"-"*13:<15}{"-"*16:<20}{"-"*10:<15}{"-"*10:<15}')

    for row in rows:
        print(f'{row[0]:<10}{row[1]:<10}{row[2]:<15}{row[3]:<20}{row[4]:<15}{row[5]:<15}')

    result_id = input('\nInput Result ID to edit: ')
    competency_score = input('Update score: ')

    sql_command = "UPDATE Assessment_Results SET competency_score = {} WHERE result_id = {}".format(competency_score, result_id)
    rows = cursor.execute(sql_command)
    connection.commit()

    print(f'\nYou have successfully updated the score to: {competency_score}')
    pass

def delete_assessment_result():
    sql_command = "SELECT * FROM Assessment_Results"
    rows = cursor.execute(sql_command).fetchall()
    print(f'\n{"Result ID":<10}{"User ID":<10}{"Assessment ID":<15}{"Competency Score":<20}{"Date Taken":<15}{"Manager ID":<15}')
    print(f'{"-"*9:<10}{"-"*7:<10}{"-"*13:<15}{"-"*16:<20}{"-"*10:<15}{"-"*10:<15}')

    for row in rows:
        print(f'{row[0]:<10}{row[1]:<10}{row[2]:<15}{row[3]:<20}{row[4]:<15}{row[5]:<15}')

    result_id = input('\nInput Result ID that you would like to DELETE: ')

    sql_command = "DELETE FROM Assessment_Results WHERE result_id = {}".format(result_id)
    rows = cursor.execute(sql_command)
    connection.commit()

    print(f'\nResult ID: {result_id} has been deleted from Assessment Results.')
    pass

# Start the terminal app while loop

email = None
user_type = None
user_id = None
while True:
    if email is None:
        print("\n1. Login")
    else:
        print("\n1. Logout")
    print("2. Exit")

    if email is not None:
        if user_type == 'user':
            print("3. View Own Competency Summary")
            print("4. Edit User Information")
        elif user_type == 'manager':
            print("3. View All Users")
            print("4. Search Users")
            print("5. View Competency Results Summary")
            print("6. View User Competency Summary")
            print("7. Add User")
            print("8. Add Competency")
            print("9. Add Assessment")
            print("10. Add Assessment Result")
            print("11. Edit User")
            print("12. Edit Competency")
            print("13. Edit Assessment")
            print("14. Edit Assessment Result")
            print("15. Delete Assessment Result")
            
    choice = input("\nEnter your choice: ")

    if choice == '1':
        if email is None:
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            user_type, email,user_id = login(password,email)
            if not email:
                email = None
        else:
            email, user_type = logout()
    elif choice == '2':
        break
    elif choice == '3':
        if user_type == 'user':
            view_user_competency_summary(False,user_id)
        elif user_type == 'manager':
            view_all_users()
    elif choice == '4':
        if user_type == 'user':
            edit_user_info()
        elif user_type == 'manager':
            search_users()
    elif choice == '5':
        if user_type == 'manager':
            view_competency_result_summary()
    elif choice == '6':
        if user_type == 'manager':
            view_user_competency_summary(True,user_id)
    elif choice == '7':
        if user_type == 'manager':
            add_user()
    elif choice == '8':
        if user_type == 'manager':
            add_competency()
    elif choice == '9':
        if user_type == 'manager':
            add_assessment()
    elif choice == '10':
        if user_type == 'manager':
            add_assessment_result()
    elif choice == '11':
        if user_type == 'manager':
            edit_user()        
    elif choice == '12':
        if user_type == 'manager':
            edit_competency()
    elif choice == '13':
        if user_type == 'manager':
            edit_assessment()
    elif choice == '14':
        if user_type == 'manager':
            edit_assessment_result()
    elif choice == '15':
        if user_type == 'manager':
            delete_assessment_result()
    else:
        print("Invalid choice. Please select a valid option.")

# Close the database connection
connection.close()