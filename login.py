import mysql.connector
from tkinter import *
from tkinter import messagebox
import subprocess
import bcrypt
import sys


# Establish a connection to the database
def get_db_connection():
    try:
        print("Attempting to connect to the database...")  # Debug log
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  
            password="",  
            database="MIRAI_DB"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        messagebox.showerror("Database Error", "Failed to connect to the database.")
        return None


# Function to handle the login process
def sign_in():
    username = user.get().strip()  # Get the username input
    password = code.get().strip()  # Get the password input

    # Validate the inputs (username and password cannot be empty)
    if not validate_username() or not validate_password():
        return

    try:
        # Get database connection
        connection = get_db_connection()
        if connection is None:
            return  # If the connection failed, return from the function

        cursor = connection.cursor()

        # Query to fetch hashed password for the username
        cursor.execute("SELECT password FROM User_TB WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result is None:
            messagebox.showerror("Invalid Credentials", "Username not found.")
            return

        stored_password = result[0]
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            print('Login Successful')
            open_dashboard()
        else:
            messagebox.showerror("Invalid Credentials", "Username or password is incorrect")

        # Close the cursor and connection after use
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        messagebox.showerror("Database Error", "An error occurred while accessing the database.")


# Functions for handling the username field behavior
def on_enter(e):
    if user.get() == 'Username':
        user.delete(0, 'end')


def on_leave(e):
    if user.get().strip() == '':
        user.insert(0, 'Username')


def validate_username():
    if user.get().strip() in ['Username', '']:
        messagebox.showerror("Input Error", "Username cannot be empty.")
        return False
    return True


# Functions for handling the password field behavior
def on_enter_password(e):
    if code.get() == 'Password':
        code.delete(0, 'end')
        code.config(show='*')


def on_leave_password(e):
    if code.get().strip() == '':
        code.insert(0, 'Password')
        code.config(show='')


def validate_password():
    if code.get().strip() in ['Password', '']:
        messagebox.showerror("Input Error", "Password cannot be empty.")
        return False
    return True


# UI setup
login = Tk()
login.title('Mirai - Login')
login.geometry('925x500+300+200')
login.config(bg='#fff')
login.resizable(False, False)

try:
    img = PhotoImage(file='login.png')  # Ensure the correct path
    Label(login, image=img, bg='white').place(x=50, y=50)
except Exception as e:
    print(f"Error loading image: {e}")

frame = Frame(login, width=350, height=350, bg="white")
frame.place(x=480, y=70)

heading = Label(frame, text='Sign in', fg='#bc6c25', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=100, y=5)

# User input field for username
user = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
user.place(x=30, y=80)
user.insert(0, 'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

# Password field setup
code = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
code.place(x=30, y=150)
code.insert(0, 'Password')
code.bind('<FocusIn>', on_enter_password)
code.bind('<FocusOut>', on_leave_password)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

# Button for SignIn
Button(frame, width=39, pady=7, text='Sign In', bg='#d4a373', fg='white', border=0, command=sign_in).place(x=35, y=204)

# Sign-up label and button
label = Label(frame, text="Don't have an account?", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
label.place(x=75, y=270)


def open_registration():
    login.destroy()
    subprocess.Popen([sys.executable, "register.py"])


def open_dashboard():
    login.destroy()
    subprocess.Popen([sys.executable, 'dashboard.py'])


sign_up = Button(frame, width=6, text='Sign Up', border=0, bg='white', cursor='hand2', fg='#d4a373',
                 command=open_registration)
sign_up.place(x=215, y=270)

login.mainloop()
