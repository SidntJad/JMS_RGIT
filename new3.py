import customtkinter as ctk
import sqlite3
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Database setup
conn = sqlite3.connect("user_data.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    full_name TEXT,
    age INTEGER,
    dob TEXT,
    mobile TEXT,
    email TEXT UNIQUE,
    otp TEXT
)
""")
conn.commit()

# Email OTP Sender
SMTP_SERVER = "smtp.gmail.com"  # Update with your SMTP server
SMTP_PORT = 587  # SMTP port
EMAIL_SENDER = "jobsearchwebsite4@gmail.com"  # Update with sender email
EMAIL_PASSWORD = "njmh nqvw idjb mmjw"  # Use app password if needed

def send_otp(email):
    otp = str(random.randint(100000, 999999))
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = email
    msg['Subject'] = "Your OTP Verification Code"
    msg.attach(MIMEText(f"Your OTP is: {otp}", 'plain'))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, email, msg.as_string())
        server.quit()
        return otp
    except Exception as e:
        print("Error sending OTP:", e)
        return None

# GUI Application
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x400")
        self.title("Login System")
        self.current_user = None
        self.login_page()
    
    def login_page(self):
        for widget in self.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(self, text="Login").pack(pady=10)
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=5)
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=5)
        
        ctk.CTkButton(self, text="Sign In", command=self.check_login).pack(pady=5)
        ctk.CTkButton(self, text="Create Account", command=self.create_account_page).pack(pady=5)
    
    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        if user:
            self.current_user = user
            self.profile_button_page()
        else:
            ctk.CTkLabel(self, text="Invalid credentials", text_color="red").pack()
    
    def create_account_page(self):
        for widget in self.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(self, text="Create Account").pack(pady=10)
        self.new_username_entry = ctk.CTkEntry(self, placeholder_text="New Username")
        self.new_username_entry.pack(pady=5)
        self.new_password_entry = ctk.CTkEntry(self, placeholder_text="New Password", show="*")
        self.new_password_entry.pack(pady=5)
        
        ctk.CTkButton(self, text="Register", command=self.register_user).pack(pady=5)
        ctk.CTkButton(self, text="Login", command=self.login_page).pack(pady=5)
    
    def register_user(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            self.login_page()
        except sqlite3.IntegrityError:
            ctk.CTkLabel(self, text="Username already taken", text_color="red").pack()
    
    def profile_button_page(self):
        for widget in self.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(self, text="Welcome").pack(pady=10)
        ctk.CTkButton(self, text="Profile", command=self.profile_page).pack(pady=5)
        ctk.CTkButton(self, text="Log Out", command=self.LogOut).pack(pady=5)
    
    

    def profile_page(self):
        for widget in self.winfo_children():
            widget.destroy()
        
        cursor.execute("SELECT full_name, age, dob, mobile, email FROM users WHERE username=?", (self.current_user[1],))
        profile = cursor.fetchone()
        
        if profile and profile[0]:  # Profile exists
            ctk.CTkLabel(self, text=f"Full Name: {profile[0]}").pack()
            ctk.CTkLabel(self, text=f"Age: {profile[1]}").pack()
            ctk.CTkLabel(self, text=f"DOB: {profile[2]}").pack()
            ctk.CTkLabel(self, text=f"Mobile: {profile[3]}").pack()
            ctk.CTkLabel(self, text=f"Email: {profile[4]}").pack()

            ctk.CTkButton(self, text="<--", command=self.profile_button_page).pack(pady=5)
        else:
            self.create_profile_page()
    
    def create_profile_page(self):
        for widget in self.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(self, text="Create Profile").pack(pady=10)
        self.full_name_entry = ctk.CTkEntry(self, placeholder_text="Full Name")
        self.full_name_entry.pack(pady=5)
        self.age_entry = ctk.CTkEntry(self, placeholder_text="Age")
        self.age_entry.pack(pady=5)
        self.dob_entry = ctk.CTkEntry(self, placeholder_text="Date of Birth")
        self.dob_entry.pack(pady=5)
        self.mobile_entry = ctk.CTkEntry(self, placeholder_text="Mobile Number")
        self.mobile_entry.pack(pady=5)
        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email")
        self.email_entry.pack(pady=5)
        
        ctk.CTkButton(self, text="Submit", command=self.verify_email).pack(pady=5)
        ctk.CTkButton(self, text="<--", command=self.profile_button_page).pack(pady=5)
    
    def verify_email(self):
        email = self.email_entry.get()
        self.otp = send_otp(email)  # Store OTP only if successfully sent

        if self.otp:
            self.otp_entry = ctk.CTkEntry(self, placeholder_text="Enter OTP")
            self.otp_entry.pack(pady=5)
            self.verify_button = ctk.CTkButton(self, text="Verify", command=self.save_profile)
            self.verify_button.pack(pady=5)
        else:
            ctk.CTkLabel(self, text="Failed to send OTP. Check email and try again.", text_color="red").pack()

    def save_profile(self):
        if not hasattr(self, 'otp') or self.otp_entry.get() != self.otp:
            ctk.CTkLabel(self, text="Invalid OTP", text_color="red").pack()
            return

        # Ensure all fields are filled before saving
        full_name = self.full_name_entry.get()
        age = self.age_entry.get()
        dob = self.dob_entry.get()
        mobile = self.mobile_entry.get()
        email = self.email_entry.get()

        if not all([full_name, age, dob, mobile, email]):
            ctk.CTkLabel(self, text="All fields are required!", text_color="red").pack()
            return

        cursor.execute("UPDATE users SET full_name=?, age=?, dob=?, mobile=?, email=? WHERE username=?", 
                    (full_name, age, dob, mobile, email, self.current_user[1]))
        conn.commit()
        self.profile_button_page()

    
    def save_profile(self):
        if self.otp_entry.get() == self.otp:
            cursor.execute("UPDATE users SET full_name=?, age=?, dob=?, mobile=?, email=? WHERE username=?", 
                           (self.full_name_entry.get(), self.age_entry.get(), self.dob_entry.get(), self.mobile_entry.get(), self.email_entry.get(), self.current_user[1]))
            conn.commit()
            self.profile_button_page()
        else:
            ctk.CTkLabel(self, text="Invalid OTP", text_color="red").pack()
    
    def LogOut(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.login_page()

if __name__ == "__main__":
    app = App()
    app.mainloop()
    
