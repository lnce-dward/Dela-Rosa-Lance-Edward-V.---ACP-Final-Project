import mysql.connector
import bcrypt
from tkinter import *
from tkinter import messagebox
import subprocess
import re
import sys
from datetime import datetime

# Database connection function (unchanged)
def get_db_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="MIRAI_DB"
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Connection Error", f"Error: {err}")
        return None

# Function to check if a record exists in the database (unchanged)
def check_record_exists(column, value):
    connection = get_db_connection()
    if connection is None:
        return False

    try:
        with connection.cursor() as cursor:
            query = f"SELECT * FROM User_TB WHERE {column} = %s"
            cursor.execute(query, (value,))
            return cursor.fetchone() is not None
    except mysql.connector.Error as err:
        messagebox.showerror("Query Error", f"Error: {err}")
        return False
    finally:
        connection.close()

# Function to handle user registration (unchanged)
def register_user(username, password, email, full_name, phone_number, gender, dob):
    connection = get_db_connection()
    if connection is None:
        return

    try:
        with connection.cursor() as cursor:
            # Insert into User_TB
            user_query = "INSERT INTO User_TB (username, password, email) VALUES (%s, %s, %s)"
            cursor.execute(user_query, (username, password, email))
            user_id = cursor.lastrowid

            # Insert into userprofile_TB
            profile_query = """
            INSERT INTO userprofile_TB 
            (user_id, full_name, email, phone_number, gender, dob) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(profile_query, (user_id, full_name, email, phone_number, gender, dob))
            
            connection.commit()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        connection.close()

# Entry field creation function (adjusted y-spacing)
def create_entry(parent, x, y, default_text, is_password=False):
    entry = Entry(parent, width=50, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
    entry.place(x=x, y=y)
    entry.insert(0, default_text)

    # Focus-in and focus-out handlers
    entry.bind('<FocusIn>', lambda e: on_focus_in(entry, is_password))
    entry.bind('<FocusOut>', lambda e: on_focus_out(entry, default_text, is_password))

    Frame(parent, width=295, height=2, bg='black').place(x=25, y=y + 27)
    return entry

# Focus-in and focus-out handlers (unchanged)
def on_focus_in(entry, is_password):
    if entry.get() in ['Enter password', 'Confirm Password', 'Enter username', 'Enter email', 'Enter full name', 'Enter phone number', 'Enter gender', 'Enter date of birth (YYYY-MM-DD)']:
        entry.delete(0, 'end')
        if is_password:
            entry.config(show="*")

def on_focus_out(entry, default_text, is_password):
    if entry.get() == '':
        entry.insert(0, default_text)
        if is_password:
            entry.config(show="")
    else:
        if is_password:
            entry.config(show="*")

# Function to handle registration (unchanged)
def handle_register(user, email, code, code1, full_name, phone, gender, dob, username_label, email_label, register_window):
    username = user.get().strip()
    email_address = email.get().strip()
    password = code.get()
    confirm_password = code1.get()
    full_name_value = full_name.get().strip()
    phone_number = phone.get().strip()
    gender_value = gender.get().strip()
    dob_value = dob.get().strip()

    # Validate inputs
    if username in ['', 'Enter username']:
        messagebox.showerror("Input Error", "Please enter a username.")
        return
    if email_address in ['', 'Enter email'] or not is_valid_email(email_address):
        email_label.config(text="Invalid email format.", fg='red')
        return
    email_label.config(text="")  # Clear error if valid

    if password in ['', 'Enter password']:
        messagebox.showerror("Input Error", "Please enter a password.")
        return
    if password != confirm_password:
        messagebox.showerror("Password Error", "Passwords do not match.")
        return

    if full_name_value in ['', 'Enter full name']:
        messagebox.showerror("Input Error", "Please enter your full name.")
        return

    if phone_number in ['', 'Enter phone number']:
        messagebox.showerror("Input Error", "Please enter your phone number.")
        return

    if gender_value in ['', 'Enter gender']:
        messagebox.showerror("Input Error", "Please enter your gender.")
        return

    if dob_value in ['', 'Enter date of birth (YYYY-MM-DD)']:
        messagebox.showerror("Input Error", "Please enter your date of birth.")
        return

    try:
        datetime.strptime(dob_value, '%Y-%m-%d')
    except ValueError:
        messagebox.showerror("Input Error", "Invalid date format. Please use YYYY-MM-DD.")
        return

    # Check if username or email already exists
    if check_record_exists("username", username):
        username_label.config(text="Username is already taken.", fg='red')
        return
    username_label.config(text="")  # Clear error if valid

    if check_record_exists("email", email_address):
        email_label.config(text="Email is already taken.", fg='red')
        return
    email_label.config(text="")  # Clear error if valid

    # Hash the password and register the user
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    register_user(username, hashed_password, email_address, full_name_value, phone_number, gender_value, dob_value)
    messagebox.showinfo("Success", "Registration successful!")
    register_window.destroy()
    open_login()

# Function to validate email format (unchanged)
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

# Open login window after registration (unchanged)
def open_login():
    subprocess.run([sys.executable, 'login.py'])

# Main registration window setup (adjusted size)
register = Tk()
register.title('Mirai - Register')
register.geometry('1000x700+200+50')  # Increased window size
register.config(bg='#fff')
register.resizable(False, False)

try:
    img = PhotoImage(file='login.png')
    Label(register, image=img, bg='white').place(x=50, y=50)
except Exception as e:
    print(f"Image Error: {e}")

# Frame for form fields (adjusted size and position)
frame = Frame(register, width=400, height=600, bg="white")
frame.place(x=550, y=50)

heading = Label(frame, text='Register', fg='#bc6c25', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=100, y=5)

# Adjusted y-coordinates for better spacing
user = create_entry(frame, 30, 80, 'Enter username')
email = create_entry(frame, 30, 140, 'Enter email')
code = create_entry(frame, 30, 200, 'Enter password', is_password=True)
code1 = create_entry(frame, 30, 260, 'Confirm Password', is_password=True)
full_name = create_entry(frame, 30, 320, 'Enter full name')
phone = create_entry(frame, 30, 380, 'Enter phone number')
gender = create_entry(frame, 30, 440, 'Enter gender')
dob = create_entry(frame, 30, 500, 'Enter date of birth (YYYY-MM-DD)')

username_label = Label(frame, text="", fg="red", bg="white")
username_label.place(x=30, y=110)

email_label = Label(frame, text="", fg="red", bg="white")
email_label.place(x=30, y=170)

Button(frame, width=39, pady=7, text='Register', bg='#d4a373', fg='white', border=0,
       command=lambda: handle_register(user, email, code, code1, full_name, phone, gender, dob, username_label, email_label, register)).place(x=35, y=560)

Label(frame, text="After registering, Sign In window will show up", fg='black', bg='white',
      font=('Microsoft YaHei UI Light', 9)).place(x=75, y=600)

register.mainloop()

