import customtkinter as ctk
import sqlite3
conn = sqlite3.connect('sampleDB.db')
cursor = conn.cursor()

# Create table for storing user data if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS userdataprofile (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        location TEXT NOT NULL,
        curr_pos TEXT,
        curr_pos_des TEXT,
        institute TEXT
        degree TEXT
        skill TEXT
        skill_des TEXT
    );
''')
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x400")
        self.title("Frame Example")
        # Create a frame
        self.frame = ctk.CTkFrame(self,width=300,height=100)
        self.frame.place(anchor="center",relx=0.5,rely=0.5)
        #grid(row=0,column=0,padx=distbetnframes,pady=distbetnframes)
        label1=ctk.CTkLabel(self.frame,text="Hello User, You have not made your profile yet")
        label1.place(anchor="s",relx=0.5,rely=0.5)
        def create_profile():
            self.tabview = ctk.CTkTabview(self.frame)
            self.tabview.pack(padx=20, pady=20, expand=True, fill="both")
            tab1=self.tabview.add("Profile")
            tab2=self.tabview.add("Experience")
            tab3=self.tabview.add("Education")
            tab4=self.tabview.add("Skills")
            def next_tab():
                # Get the current selected tab's name
                current_tab = self.tabview.get()

                # Define the tab names in order
                tab_names = ["Profile", "Experience", "Education","Skills"]

                # Find the current tab index
                current_index = tab_names.index(current_tab)

                # Calculate the index of the next tab (wrap around if at the last tab)
                next_index = (current_index + 1) % len(tab_names)

                # Switch to the next tab
                self.tabview.set(tab_names[next_index])
            self.first_name=ctk.CTkLabel(tab1,text="Enter your first name")
            self.first_name.pack(pady=6)
            self.first_name_entry=ctk.CTkEntry(tab1,width=167)
            self.first_name_entry.pack(pady=6)
            self.last_name=ctk.CTkLabel(tab1,text="Enter your last name")
            self.last_name.pack(pady=6)
            self.last_name_entry=ctk.CTkEntry(tab1,width=167)
            self.last_name_entry.pack(pady=6)
            self.location_name=ctk.CTkLabel(tab1,text="Enter your location")
            self.location_name.pack(pady=6)
            self.location_name_entry=ctk.CTkEntry(tab1,width=167)
            self.location_name_entry.pack(pady=6)
            self.button = ctk.CTkButton(tab1, text="Next Tab", command=next_tab)
            self.button.pack(pady=10)
            self.current_position=ctk.CTkLabel(tab2,text="Current Position")
            self.current_position.pack(pady=6)
            self.current_position_des=ctk.CTkLabel(tab2,text="What is your Current Position")
            self.current_position_des.pack(pady=6)
            self.current_position_entry=ctk.CTkEntry(tab2,width=167)
            self.current_position_entry.pack(pady=6)
            self.current_position_ask=ctk.CTkLabel(tab2,text="Please Describe your Current Position")
            self.current_position_ask.pack(pady=6)
            self.current_position_ask_des=ctk.CTkTextbox(tab2)
            self.current_position_ask_des.pack(pady=6)
            self.button2 = ctk.CTkButton(tab2, text="Next Tab/Skip", command=next_tab)
            self.button2.pack(pady=6)
            self.inst_name=ctk.CTkLabel(tab3,text="What Institute Did you go to?")
            self.inst_name.pack()
            self.inst_name_entry=ctk.CTkEntry(tab3)
            self.inst_name_entry.pack()
            self.degree_name=ctk.CTkLabel(tab3,text="What degree do you have?")
            self.degree_name.pack()
            self.degree_name_entry=ctk.CTkEntry(tab3)
            self.degree_name_entry.pack()
            self.button3 = ctk.CTkButton(tab3, text="Next Tab/Skip", command=next_tab)
            self.button3.pack(pady=10)
            self.skill_des=ctk.CTkLabel(tab4,text="Do you you have a skill you would like to mention")
            self.skill_des.pack(pady=6)
            self.skill_des_entry=ctk.CTkEntry(tab4,width=167)
            self.skill_des_entry.pack(pady=6)
            self.skill_ask=ctk.CTkLabel(tab4,text="Please Describe your Current Position")
            self.skill_ask.pack(pady=6)
            self.skill_ask_des=ctk.CTkTextbox(tab4)
            self.skill_ask_des.pack(pady=6)
            self.button4 = ctk.CTkButton(tab4, text="finish", command=next_tab)
            self.button4.pack(pady=10)
            # cursor.execute("INSERT INTO usersdataprofile (id INTEGER PRIMARY KEY AUTOINCREMENT,first_name,last_name,location,curr_pos,curr_pos_des,institute,degree,skill,skill_des TEXT) VALUES (?, ?)", 
            #                ())
        self.button1=ctk.CTkButton(self.frame,text="Make Profile",width=65,command=create_profile)
        self.button1.place(anchor="n",relx=0.5,rely=0.6)
    
        
        

if __name__ == "__main__":
    app = App()
    app.mainloop()
