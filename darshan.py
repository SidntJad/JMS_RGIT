


import customtkinter as ctk
import tkinter.messagebox as tkmb
import sqlite3

# Create or connect to the SQLite database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create table for storing user data if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

# Selecting GUI theme - dark, light, system (for system default)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("400x400")
app.title("Modern Login UI using Customtkinter")

# Function for login
def login():
    username_input = user_entry.get()
    password_input = user_pass.get()

    # Check if the username and password match the database
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username_input, password_input))
    result = cursor.fetchone()

    if result:
        tkmb.showinfo(title="Login Successful", message="You have logged in successfully!")
    else:
        tkmb.showerror(title="Login Failed", message="Invalid username or password.")

# Function for sign-up
def sign_up():
    def register():
        new_username = new_user_entry.get()
        new_password = new_user_pass.get()

        if new_username == "" or new_password == "":
            tkmb.showwarning(title="Input Error", message="Both fields are required!")
        else:
            # Insert the new user data into the database
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_username, new_password))
            conn.commit()  # Commit the transaction to save the data
            tkmb.showinfo(title="Sign Up Successful", message="Your account has been created successfully!")
            sign_up_window.quit()  # Close the sign-up window after successful registration

    # Create sign-up window
    sign_up_window = ctk.CTkToplevel(app)
    sign_up_window.title("Sign Up")
    sign_up_window.geometry("350x200")

    # Labels and Entries for sign-up page
    new_user_entry = ctk.CTkEntry(master=sign_up_window, placeholder_text="New Username")
    new_user_entry.pack(pady=12, padx=10)

    new_user_pass = ctk.CTkEntry(master=sign_up_window, placeholder_text="New Password", show="*")
    new_user_pass.pack(pady=12, padx=10)

    sign_up_button = ctk.CTkButton(master=sign_up_window, text="Register", command=register)
    sign_up_button.pack(pady=12, padx=10)

    sign_up_window.mainloop()  # Start the event loop for the sign-up window

# Main Page UI
label = ctk.CTkLabel(app, text="This is the main UI page")
label.pack(pady=20)

frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=40, fill='both', expand=True)

label = ctk.CTkLabel(master=frame, text='Modern Login System UI')
label.pack(pady=12, padx=10)

user_entry = ctk.CTkEntry(master=frame, placeholder_text="Username")
user_entry.pack(pady=12, padx=10)

user_pass = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
user_pass.pack(pady=12, padx=10)

login_button = ctk.CTkButton(master=frame, text='Login', command=login)
login_button.pack(pady=12, padx=10)

checkbox = ctk.CTkCheckBox(master=frame, text='Remember Me')
checkbox.pack(pady=12, padx=10)

# Sign Up Button
sign_up_button = ctk.CTkButton(master=frame, text="Sign Up", command=sign_up)
sign_up_button.pack(pady=12, padx=10)

app.mainloop()

# Close the database connection when the app is closed
conn.close()
