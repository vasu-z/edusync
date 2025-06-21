import tkinter as tk
from tkinter import ttk

class EdusyncApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Edusync - Student Grade Management")
        self.root.geometry("1440x1024")
        self.root.configure(bg="white")
        self.root.resizable(False, False)

        self.create_main_area()  # moved this line before create_sidebar to avoid attribute error
        self.create_sidebar()

        self.root.mainloop()

    def create_sidebar(self):
        self.sidebar = tk.Frame(self.root, bg="#1A1D28")
        self.sidebar.place(x=0, y=0, width=240, height=1024)

        logo = tk.Label(self.sidebar, text="Edusync", fg="white", bg="#1A1D28", font=("Poppins", 20, "bold"))
        logo.pack(pady=(40, 30), anchor="w", padx=20)

        self.buttons = {}
        self.screens = {}
        menu_items = ["Dashboard", "Register Student", "Add Grades", "View Report", "Logout"]

        for item in menu_items:
            btn = tk.Button(
                self.sidebar, text=item, fg="white", bg="#1A1D28",
                font=("Poppins", 13), relief="flat",
                anchor="w", padx=30,
                activebackground="#2979FF", activeforeground="white",
                command=lambda name=item: self.show_screen(name)
            )
            btn.pack(fill="x", pady=4)
            self.buttons[item] = btn

        self.active = None
        self.show_screen("Dashboard")

    def create_main_area(self):
        self.main_area = tk.Frame(self.root, bg="white")
        self.main_area.place(x=240, y=0, width=1200, height=1024)

        self.dashboard_screen()
        self.register_screen()
        self.add_grades_screen()
        self.view_report_screen()

    def clear_main_area(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    def show_screen(self, name):
        if self.active:
            self.buttons[self.active].configure(bg="#1A1D28")
        self.buttons[name].configure(bg="#2979FF")
        self.active = name
        self.clear_main_area()

        if name == "Dashboard":
            self.dashboard_screen()
        elif name == "Register Student":
            self.register_screen()
        elif name == "Add Grades":
            self.add_grades_screen()
        elif name == "View Report":
            self.view_report_screen()
        elif name == "Logout":
            self.root.destroy()

    def dashboard_screen(self):
        heading = tk.Label(self.main_area, text="Dashboard", font=("Poppins", 18, "bold"), bg="white")
        heading.place(x=20, y=20)

        stats = [("1,250", "Students"), ("50", "Teachers"), ("30", "Classes"), ("1,180", "Present")]
        for i, (num, label) in enumerate(stats):
            box = tk.Frame(self.main_area, bg="#2979FF", width=220, height=100)
            box.place(x=20 + i * 240, y=70)
            tk.Label(box, text=num, font=("Poppins", 20, "bold"), bg="#2979FF", fg="white").place(x=20, y=10)
            tk.Label(box, text=label, font=("Poppins", 12), bg="#2979FF", fg="white").place(x=20, y=55)

    def register_screen(self):
        tk.Label(self.main_area, text="Register Student", font=("Poppins", 16, "bold"), bg="white").place(x=30, y=30)
        fields = ["Full Name", "Date of Birth", "Gender", "Address"]
        y = 80
        for field in fields:
            tk.Label(self.main_area, text=field, font=("Poppins", 12), bg="white").place(x=30, y=y)
            tk.Entry(self.main_area, font=("Poppins", 12), width=40, bd=1, relief="solid").place(x=180, y=y)
            y += 50
        tk.Button(self.main_area, text="Register", font=("Poppins", 12), bg="#2979FF", fg="white").place(x=180, y=y+10)

    def add_grades_screen(self):
        tk.Label(self.main_area, text="Add Grades", font=("Poppins", 16, "bold"), bg="white").place(x=30, y=30)
        tk.Label(self.main_area, text="Student ID", font=("Poppins", 12), bg="white").place(x=30, y=80)
        ttk.Combobox(self.main_area, values=["#1124", "#1145"], width=37).place(x=180, y=80)
        tk.Label(self.main_area, text="Subject", font=("Poppins", 12), bg="white").place(x=30, y=130)
        tk.Entry(self.main_area, font=("Poppins", 12), width=40, bd=1, relief="solid").place(x=180, y=130)
        tk.Label(self.main_area, text="Marks", font=("Poppins", 12), bg="white").place(x=30, y=180)
        tk.Entry(self.main_area, font=("Poppins", 12), width=40, bd=1, relief="solid").place(x=180, y=180)
        tk.Button(self.main_area, text="Submit", font=("Poppins", 12), bg="#2979FF", fg="white").place(x=180, y=230)

    def view_report_screen(self):
        tk.Label(self.main_area, text="Student Report", font=("Poppins", 16, "bold"), bg="white").place(x=30, y=30)
        cols = ("ID", "Name", "Class", "Grade")
        tree = ttk.Treeview(self.main_area, columns=cols, show="headings")
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=180)
        data = [
            ("#1124", "Chris Gayle", "10A", "92"),
            ("#1145", "Donald Trump", "9B", "88"),
            ("#1138", "Elon Musk", "11C", "95"),
            ("#1261", "Vladimir Putin", "10B", "81")
        ]
        for row in data:
            tree.insert("", "end", values=row)
        tree.place(x=30, y=80, width=800, height=400)

if __name__ == "__main__":
    EdusyncApp()

