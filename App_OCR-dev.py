import sqlite3
import streamlit as st
from streamlit_option_menu import option_menu
from ultralytics import YOLO
import cv2
from your_module import main_func, speak, main_func_ped, main_func_alert  # Import your functions here

# Establish a connection to the database
conn = sqlite3.connect('my_database.sqlite3')
cursor = conn.cursor()

# SQL command to create a table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);''')
conn.commit()

# Function to create a new user
def create_user(username, email, password):
    try:
        cursor.execute('''
        INSERT INTO users (name, email, password) VALUES (?, ?, ?);
        ''', (username, email, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # This happens if the email is not unique

# Function to check user credentials
def authenticate_user(email, password):
    cursor.execute('''
    SELECT * FROM users WHERE email = ? AND password = ?;
    ''', (email, password))
    return cursor.fetchone() is not None

# Authentication state
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# If authenticated, show the main app (Third Eye interface)
if st.session_state['authenticated']:
    # Your existing Third Eye code goes here...
    # (Make sure to indent the code correctly to fit inside this if block)
    pass
else:
    # Authentication flow
    selected_action = st.radio("Choose action", ["Login", "Sign Up"])
    
    # Sign Up Form
    if selected_action == "Sign Up":
        with st.form("signup_form"):
            username = st.text_input("Username")
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")
            password_confirmation = st.text_input("Confirm Password", type="password")
            submit_button = st.form_submit_button("Create my account")
            
            if submit_button:
                if password == password_confirmation:
                    if create_user(username, email, password):
                        st.success("Your account has been created successfully!")
                        st.session_state['authenticated'] = True
                    else:
                        st.error("A user with this email already exists.")
                else:
                    st.error("The passwords do not match.")
    
    # Login Form
    elif selected_action == "Login":
        with st.form("login_form"):
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                if authenticate_user(email, password):
                    st.success("You have successfully logged in!")
                    st.session_state['authenticated'] = True
                else:
                    st.error("Invalid email or password.")
