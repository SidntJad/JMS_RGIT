import customtkinter
import sqlite3

# Create or connect to the SQLite database
conn = sqlite3.connect('sampleDB.db')
cursor = conn.cursor()

# Create table for storing user data if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobrecpostfinal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jobname TEXT NOT NULL,
        jobdesc TEXT,
        company TEXT,
        w_type TEXT,
        location TEXT,
        j_type TEXT
    );
''')
        
class MyScrollableCheckboxFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, title, values):
        super().__init__(master, label_text=title)
# Configure columns to be stretchable
        gridcol=[0,1,2,3,4]
        self.grid_columnconfigure(gridcol, weight=1)
        
        # Configure rows to be stretchable as well (this is key)
        self.grid_rowconfigure(0, weight=1)  # Adjust the weight for your rows as needed
        
        self.values = values
        
        self.checkboxes = []
        rowc = 0
        col = 0
        for i, value in enumerate(self.values):
            self.grid_columnconfigure(0, weight=1)
            self.val = values
            self.checkboxes = []
            jobframe = customtkinter.CTkFrame(self, border_width=1, fg_color="#3B3B3B")
            
            # Configure jobframe to take available width
            jobframe.grid_columnconfigure([0, 1, 2], weight=1)
            jobframe.grid_rowconfigure(0, weight=1)
            
            if i % 1 == 0:
                col = 0
                rowc += 1
            
            textjobframe = "Job Title Posted - " + value
            jobframe.columnconfigure([0, 1, 2,3,4], weight=1)
            jobframe.rowconfigure([0, 1, 2], weight=1)
            
            # Adjust padding, so the jobframe stretches more
            a = 20
            jobframe.grid(row=rowc, column=col, padx=10, pady=7, sticky="nsew", columnspan=5)
            
            # Label and button inside the jobframe
            labels = customtkinter.CTkLabel(jobframe, text=textjobframe)
            labels.grid(row=0, column=0, padx=10, pady=10, sticky="w", columnspan=3)
            labels = customtkinter.CTkLabel(jobframe, text="Job " + value)
            labels.grid(row=1, column=0, padx=10, sticky="w", columnspan=3)
            
            button = customtkinter.CTkButton(jobframe, text="More Details",width=56,command=lambda val=value: self.get(val)) #+ value, command=lambda val=value: self.get(val))
            self.checkboxes.append({"button": button, "clicked": False})
            button.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")
            
            col += 1
    def get(self,value):
            for checkbox in self.checkboxes:
                if checkbox["button"].cget("text") == value:
                    # Toggle the clicked state
                    checkbox["clicked"] = not checkbox["clicked"]
                    # Print the text of the button that was pressed
                    print(f"Button pressed: {value}")
            print(f"Button pressed: {value}")
            # dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="Test")
            # text=dialog.get_input()
            details=customtkinter.CTkToplevel()
            details.geometry("400x400")
            details.title("Frame Example")
            # Create a frame
            frame = customtkinter.CTkFrame(details,width=300,height=100)
            frame.place(anchor="center",relx=0.5,rely=0.5)
            cursor.execute("SELECT * FROM jobrecpostfinal")
            result = cursor.fetchall()
            i=0
            for row in result:
               firstrow=result[i]
               if value==firstrow[1]: 
                   print(True)
                   break
               i=i+1
            row1=result[i]
            
            labels2= customtkinter.CTkLabel(frame, text="Job Description:"+str(row1[6]))
            labels2.grid(row=2, column=0, padx=10, sticky="w", columnspan=3)
            labels1= customtkinter.CTkLabel(frame, text="Job Name:"+str(row1[1]))
            labels1.grid(row=1, column=0, padx=10, sticky="w", columnspan=3)
            labels3= customtkinter.CTkLabel(frame, text="Job Company:"+str(row1[2]))
            labels3.grid(row=3, column=0, padx=10, sticky="w", columnspan=3)
            labels4= customtkinter.CTkLabel(frame, text="Job Type:"+str(row1[3]))
            labels4.grid(row=4, column=0, padx=10, sticky="w", columnspan=3)
            labels5= customtkinter.CTkLabel(frame, text="Job location:"+str(row1[4]))
            labels5.grid(row=5, column=0, padx=10, sticky="w", columnspan=3)
            labels6= customtkinter.CTkLabel(frame, text="Workspace Type:"+str(row1[5]))
            labels6.grid(row=5, column=0, padx=10, sticky="w", columnspan=3)

            

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Job Post")
        self.geometry("900x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        cursor.execute("SELECT * FROM jobrecpostfinal")
        result = cursor.fetchall()
        self.val=[]
        for rows in result:
             print(rows)
             self.val.append(rows[1])
        values = ["value 1", "value 2", "value 3", "value 4", "value 5", "value 6", "value 7", "value 8", "value 9", "value 10", "value 11"]
        self.scrollable_checkbox_frame = MyScrollableCheckboxFrame(self, title="Values", values=self.val)
        self.scrollable_checkbox_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew",columnspan=2)
        self.search=customtkinter.CTkEntry(self,width=700)
        self.search.grid(row=3,column=0)
        
        self.button2 = customtkinter.CTkButton(self, text="Search", command=self.button_call_back1)
        self.button2.grid(row=3, column=1,sticky="nsew")
        self.button = customtkinter.CTkButton(self, text="Add", command=self.button_callback)
        self.button.grid(row=4, column=0, padx=10, pady=10, sticky="wesn", columnspan=2)

    def button_call_back1(self):
         self.search_result=self.search.get()
         print(self.search_result)
         print(len(self.val))
         val2=[]
         for i in range (len(self.val)):
              if self.val[i]==self.search_result:
                   val2.append(self.val[i])
         self.scrollable_checkbox_frame = MyScrollableCheckboxFrame(self, title="Values", values=val2)
         self.scrollable_checkbox_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew",columnspan=2)
         if self.search_result==" ":
              self.scrollable_checkbox_frame = MyScrollableCheckboxFrame(self, title="Values", values=self.val)
              self.scrollable_checkbox_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew",columnspan=2)
    
              
         
            
    def button_callback(self):
        job_post=customtkinter.CTkToplevel()
        jobdetails=[]
        job_post.title("Job Post")
        job_post.geometry("345x657")
        padding=23
        # titleframe=customtkinter.CTkFrame(job_post)
        # titleframe.pack(anchor="center")
        # title=customtkinter.CTkLabel(job_post,text="Job Posting")
        # title.pack()
        w=178
        main_frame=customtkinter.CTkFrame(job_post)
        main_frame.place(relx=0.1,rely=0.1)
        jobtitle1=customtkinter.CTkLabel(main_frame,text="Job Post")
        jobtitle1.pack(padx=0)
        #jb_entry=customtkinter.CTkEntry(main_frame,width=w)
        #jb_entry.pack()
        jobtitle=customtkinter.CTkLabel(main_frame,text="Job Title")
        jobtitle.pack(padx=padding,anchor="w")
        jb_title=customtkinter.CTkEntry(main_frame,width=w)
        jb_title.pack(padx=padding,anchor="w")
        
        company=customtkinter.CTkLabel(main_frame,text="What is the name of your company?")
        company.pack(padx=padding,anchor="w")
        com_entry=customtkinter.CTkEntry(main_frame,width=w)
        com_entry.pack(padx=padding,anchor="w")
        
        job_type=customtkinter.CTkLabel(main_frame,text="Job Type")
        job_type.pack(padx=padding,anchor="w")
        def combobox_callback(choice):
            print("combobox dropdown clicked:", choice)
            jobdetails.append(choice)
        combobox_var = customtkinter.StringVar(value="Select Choice")
        combobox = customtkinter.CTkComboBox(main_frame, values=["Onsite", "Hybrid","Remote"],
                                            command=combobox_callback, variable=combobox_var)
        combobox_var.set("Select Choice")
        combobox.pack(padx=padding,anchor="w")
        location=customtkinter.CTkLabel(main_frame,text="What is the name of your company?")
        location.pack(padx=padding,anchor="w")
        loc_entry=customtkinter.CTkEntry(main_frame,width=w)
        loc_entry.pack(padx=padding,anchor="w")
        
        work_type=customtkinter.CTkLabel(main_frame,text="Work Type")
        work_type.pack(padx=padding,anchor="w")
        def combobox_callback(choice):
            print("combobox dropdown clicked:", choice)
            jobdetails.append(choice)


        combobox_var = customtkinter.StringVar(value="Select Choice")
        combobox = customtkinter.CTkComboBox(main_frame, values=["Full Time", "Part Time","Internship"],
                                            command=combobox_callback, variable=combobox_var)
        combobox_var.set("Select Choice")
        combobox.pack(padx=padding,anchor="w")
        current_position_ask=customtkinter.CTkLabel(main_frame,text="Please Describe your Current Position")
        current_position_ask.pack(padx=padding,anchor="w")
        current_position_ask_des=customtkinter.CTkTextbox(main_frame)
        current_position_ask_des.pack(padx=padding,anchor="n")
        ok=False
        def confirm():
             ok=True
             jobdetails.append(jb_title.get())
             jobdetails.append(com_entry.get())
             jobdetails.append(loc_entry.get())
             jobdetails.append(current_position_ask_des.get("1.0","end-1c"))
             print(cursor.execute("INSERT INTO jobrecpostfinal(jobname, jobdesc, company, w_type, location, j_type) VALUES (?, ?, ?, ?, ?, ?);", 
                        (jobdetails[2],jobdetails[5],jobdetails[3],jobdetails[0],jobdetails[4],jobdetails[1])))
             conn.commit()
             self.scrollable_checkbox_frame = MyScrollableCheckboxFrame(self, title="Values", values=self.val)
             self.scrollable_checkbox_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew",columnspan=2)
             start()
             for rows in range(len(jobdetails)):
                print(jobdetails)
             
            

        button=customtkinter.CTkButton(main_frame,text="Submit",command=confirm)
        button.pack(padx=padding,anchor="w")


        # dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="Test")
        # text=dialog.get_input()
        # print(text)
        #print(cursor.execute("INSERT INTO jobrecpost(jobname) VALUES (\""+text+"\")"))
        # print(cursor.execute("insert into jobrecpost(jobname) values(?);",(text)))
        # if ok:
        #     print(cursor.execute("INSERT INTO jobrecpostfinal(jobname, jobdesc, company, w_type, location, j_type) VALUES (?, ?, ?, ?, ?, ?);", 
        #                 ("Text", "Text", "Text", "Text", "Text", "Text")))
        #     for rows in range(len(jobdetails)):
        #         print(jobdetails[rows])

        # jobname TEXT NOT NULL,
        # jobdesc TEXT,
        # company TEXT,
        # w_type TEXT,
        # location TEXT,
        # j_type TEXT
        
        
        
def start():
     app = App()
     app.mainloop()
start()