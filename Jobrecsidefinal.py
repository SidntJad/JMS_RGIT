import customtkinter
import sqlite3

# Create or connect to the SQLite database
conn = sqlite3.connect('sampleDB.db')
cursor = conn.cursor()

# Create table for storing user data if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobrecpost (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jobname TEXT NOT NULL
    );
''')
        
class MyScrollableCheckboxFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, title, values):
        super().__init__(master, label_text=title)
        gridcol=[0,1,2,3,4]
        self.grid_columnconfigure(gridcol, weight=1)
        self.values = values
        
        self.checkboxes = []
        rowc=0
        col=0
        for i, value in enumerate(self.values):
            self.grid_columnconfigure(0, weight=1)
            self.val = values
            self.checkboxes = []
            jobframe=customtkinter.CTkFrame(self,border_width=1,fg_color="#3B3B3B")
            #jobframe.grid_columnconfigure(1, weight=1)
            if i%5==0:
                col=0
                rowc=rowc+1
            textjobframe="Job Number "+value
            jobframe.grid(row=rowc,column=col,padx=14, pady=7, sticky="w",columnspan=2)
            labels= customtkinter.CTkLabel(jobframe,text=textjobframe)
            labels.grid(row=0,column=0,padx=10,pady=10, sticky="w",columnspan=2)
            labels= customtkinter.CTkLabel(jobframe,text="Job "+value)
            labels.grid(row=1,column=0,padx=10, sticky="w",columnspan=2)
            button = customtkinter.CTkButton(jobframe, text="my button"+value,command=lambda val=value:self.get(val))
            self.checkboxes.append({"button": button, "clicked": False})
            button.grid(row=2, column=0, padx=10,pady=(0,10),sticky="ew",columnspan=2)
            col=col+1
    def get(self,value):
            # for checkbox in self.checkboxes:
            #     if checkbox["button"].cget("text") == value:
            #         # Toggle the clicked state
            #         checkbox["clicked"] = not checkbox["clicked"]
            #         # Print the text of the button that was pressed
            #         print(f"Button pressed: {value}")
            print(f"Button pressed: {value}")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.geometry("900x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        cursor.execute("SELECT * FROM jobrecpost")
        result = cursor.fetchall()
        val=[]
        for rows in result:
             print(rows)
             val.append(rows[1])
        values = ["value 1", "value 2", "value 3", "value 4", "value 5", "value 6", "value 7", "value 8", "value 9", "value 10", "value 11"]
        self.scrollable_checkbox_frame = MyScrollableCheckboxFrame(self, title="Values", values=val)
        self.scrollable_checkbox_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

        self.button = customtkinter.CTkButton(self, text="my button", command=self.button_callback)
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

    def button_callback(self):
        print(cursor.execute("insert into jobrecpost(jobname) values(\"Person\");"))
        conn.commit()
        self.destroy()
        start()
def start():
     app = App()
     app.mainloop()
start()