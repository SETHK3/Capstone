import sqlite3
import hashlib
from datetime import datetime

# Initialize connection
connection = sqlite3.connect('competency_app.db')
cursor = connection.cursor()

# def create_schema(cursor):
#     sql_file = open('capstone_queries.txt')
#     sql_as_string = sql_file.read()
#     result = cursor.executescript(sql_as_string)

#     connection.commit()

#     return result

# result = create_schema(cursor)jklkj

# with open("MOCK_DATA1.sql", "r") as sql_file:
#     sql_commands = sql_file.read()

# cursor.executescript(sql_commands)    

# Function to hash a password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to check if a given email and password match
def authenticate(email, password):
    hashed_password = hash_password(password)
    # Implement authentication logic here
    pass

# Function to get user type based on user's email
def get_user_type(email):
    # Implement logic to fetch user type
    pass

def login():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    
    if authenticate(email, password):
        user_type = get_user_type(email)
        return email, user_type
    else:
        print("Authentication failed. Please try again.")
        return None, None

def logout():
    print("Logged out successfully.")
    return None, None

# Functions for user actions
def view_own_competency(user_id):
    user_id = input('Input your User ID: ')

    sql_command = "SELECT * FROM Competency_Assessments WHERE user_id = {}".format(user_id)
    rows = cursor.execute(sql_command)
    print(f'{"Assessment ID":<15}{"Competency ID":<15}{"User ID":<10}{"Date Taken":<15}{"Competency Score":<20}{"Manager ID":<15}')

    for row in rows:
        print(f'{row[0]:<15}{row[1]:<15}{row[2]:<10}{row[3]:<15}{row[4]:<20}{row[5]:<15}')
    pass

def edit_user_info(user_id, first_name, last_name, password):
    user_id = ('Input user_id to edit: ')
    first_name = input('Update first name: ')
    last_name = input('Update last name: ')
    password = input('Input new password: ')

    sql_command = "UPDATE Users SET first_name = {} and last_name = {} and password = {} WHERE user_id = {}".format(first_name, last_name, password, user_id)
    cursor.execute(sql_command)
    connection.commit
    pass
    pass

# Function for manager actions
def view_all_users():
    sql_command = "SELECT * FROM Users"
    rows = cursor.execute(sql_command)
    print(f'{"User ID":<10}{"First Name":<25}{"Last Name":<40}{"Phone":<20}{"Email":<12}{"Password":<15}{"Active":<13}{"Date Created":<15}{"Hire Date":<12}{"User Type":<15}')
    
    for row in rows:
        print(f'{row[0]:<10}{row[1]:<25}{row[2]:<40}{row[3]:<20}{row[4]:<12}{row[5]:<15}{row[6]:<13}{row[7]:<15}{row[8]:<12}{row[9]:<15}')
    pass

def search_users():
    user_search = input('Type first or last name to search: ')

    sql_command = "SELECT user_id, first_name, last_name, phone, email, active, date_created, hire_date, user_type FROM Users WHERE first_name LIKE '%{}%' OR last_name LIKE '%{}%'".format(user_search)
    rows = cursor.execute(sql_command)
    print(f'{"User ID":<10}{"First Name":<25}{"Last Name":<40}{"Phone":<20}{"Email":<12}{"Active":<13}{"Date Created":<15}{"Hire Date":<12}{"User Type":<15}')
    
    for row in rows:
        print(f'{row[0]:<10}{row[1]:<25}{row[2]:<40}{row[3]:<20}{row[4]:<12}{row[5]:<13}{row[6]:<15}{row[7]:<12}{row[8]:<15}')
    pass

def view_user_competency_report(user_id, competency_id):
    user_id = input('Input User ID: ')
    competency_id = input('Input Competency ID to view: ')
    
    sql_command = "SELECT * FROM User_Competency_Summary WHERE user_id = {} and competency_id = {}".format(user_id, competency_id)
    rows = cursor.execute(sql_command)
    print(f'{"Report ID":<10}{"User ID":<10}{"Competency ID":<15}{"Competency Score":<20}{"Average Competency Score":<30}')

    for row in rows:
        print(f'{row[0]:<10}{row[1]:<10}{row[2]:<15}{row[3]:<20}{row[4]:<30}')
    pass

def view_user_assessments(user_id):
    user_id = input('Input User ID to view Assessment Results: ')

    sql_command = "SELECT * FROM Assessment_Results WHERE user_id = {}".format(user_id)
    rows = cursor.execute(sql_command)
    print(f'{"Result ID":<10}{"Assessment ID":<15}{"User ID":<10}{"Score":<10}{"Date Taken":<15}')

    for row in rows:
        print(f'{row[0]:<10}{row[1]:<15}{row[2]:<10}{row[3]:<10}{row[4]:<15}')
    pass

def add_user(first_name, last_name, phone, email, password, active, hire_date, user_type):
    first_name = input('First name: ')
    last_name = input('Last name: ')
    phone = input('Phone number: ')
    email = input('Email: ')
    password = input('Password: ')
    active = input('Active status: ')
    hire_date = input('Date of hire: ')
    user_type = input('User or Manager: ')

    sql_command = "INSERT INTO Users (first_name, last_name, phone, email, password, active, hire_date, user_type) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(first_name, last_name, phone, email, password, active, hire_date, user_type)
    cursor.execute(sql_command)
    connection.commit()
    pass

def add_manager(first_name, last_name, phone, email, password, active, hire_date, user_type):
    first_name = input('First name: ')
    last_name = input('Last name: ')
    phone = input('Phone number: ')
    email = input('Email: ')
    password = input('Password: ')
    active = input('Active status: ')
    hire_date = input('Date of hire: ')
    user_type = input('User or Manager: ')

    sql_command = "INSERT INTO Managers (first_name, last_name, phone, email, password, active, hire_date, user_type) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(first_name, last_name, phone, email, password, active, hire_date, user_type)
    cursor.execute(sql_command)
    connection.commit()
    pass

def add_competency():
    name = input('Competency name: ')
    date_created = input('Date of creation: ')

    sql_command = "INSERT INTO Competencies (name, date_created) VALUES('{}}', '{}')".format(name, date_created)
    cursor.execute(sql_command)
    connection.commit()
    pass

def add_assessment_to_competency():
    # Implement logic to add a new assessment to a competency
    pass

def add_assessment_result(user_id, assessment_id, score):
    # Implement logic to add an assessment result
    pass

def edit_user(user_id, first_name, last_name, password):
    user_id = ('Input user_id to edit: ')
    first_name = input('Update first name: ')
    last_name = input('Update last name: ')
    password = input('Input new password: ')

    sql_command = "UPDATE Users SET first_name = {} and last_name = {} and password = {} WHERE user_id = {}".format(first_name, last_name, password, user_id)
    cursor.execute(sql_command)
    connection.commit()
    pass

def edit_competency(competency_id, name):
    competency_id = input('Input Competency ID to edit: ')
    name = input('Update Competency name: ')

    sql_command = "UPDATE Competencies SET name = {} WHERE competency_id = {}".format(name, competency_id)
    rows = cursor.execute(sql_command)
    connection.commit()

    for x in rows:
        print(f'Competency name has been updated: {x}')
    pass

def edit_assessment(assessment_id, name):
    assessment_id = input('Input Assessment ID to edit: ')
    name = input('Update Assessment name: ')

    sql_command = "UPDATE Assessments SET name = {} WHERE assessment_id = {}".format(name, assessment_id)
    rows = cursor.execute(sql_command)
    connection.commit()

    for x in rows:
        print(f'Assessment name has been updated: {x}')
    pass

def edit_assessment_result(result_id, score):
    result_id = input('Input Result ID to edit: ')
    score = input('Update score: ')

    sql_command = "UPDATE Assessment_Results SET score = {} WHERE result_id = {}".format(score, result_id)
    rows = cursor.execute(sql_command)
    connection.commit()

    for x in rows:
        print(f'Updated score: {x}')
    pass

def delete_assessment_result(result_id):
    result_id = input('Input Result ID that you would like to DELETE: ')

    sql_command = "DELETE FROM Assessment_Results WHERE result_id = {}".format(result_id)
    rows = cursor.execute(sql_command)
    connection.commit()

    for x in rows:
        print(f'Result ID: {x} has been deleted from Assessment Results.')
    pass

# Start the terminal app while loop
email = None
user_type = None

while True:
    if email is None:
        print("1. Login")
    else:
        print("1. Logout")
    print("2. Exit")

    if email is not None:
        if user_type == 'user':
            print("3. View Own Competency")
            print("4. Edit User Information")
        elif user_type == 'manager':
            print("3. View All Users")
            print("4. Search Users")
            print("5. View User Competency Report")
            print("6. View User Assessments")
            print("7. Add User")
            print("8. Add Competency")
            print("9. Add Assessment to Competency")
            print("10. Add Assessment Result")
            print("11. Edit User")
            print("12. Edit Competency")
            print("13. Edit Assessment")
            print("14. Edit Assessment Result")
            print("15. Delete Assessment Result")
            
    choice = input("Enter your choice: ")

    if choice == '1':
        if email is None:
            email, user_type = login()
        else:
            email, user_type = logout()
    elif choice == '2':
        break
    elif choice == '3':
        if user_type == 'user':
            view_own_competency(user_id)
        elif user_type == 'manager':
            view_all_users()
    # Implement other choices based on user type
    else:
        print("Invalid choice. Please select a valid option.")

# Close the database connection
connection.close()