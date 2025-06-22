import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class Student:
    def __init__(self):
        self.win = tk.Tk()
        self.win.title("Student Panel")
        self.win.geometry("1440x1024")
        self.win.configure(bg="white")

        self.db = sqlite3.connect("students.db")
        self.cur = self.db.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS students (id TEXT PRIMARY KEY, name TEXT, dob TEXT, gender TEXT, address TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS marks (sid TEXT, subject TEXT, marks INTEGER)")

        self.body()
        self.sidebar()
        self.show("Dashboard")
        self.win.mainloop()

    def sidebar(self):
        bar = tk.Frame(self.win, bg="#1E293B")
        bar.place(x=0, y=0, width=240, height=1024)
        tk.Label(bar, text="StudentApp", bg="#1E293B", fg="white", font=("Poppins", 20, "bold")).pack(pady=30, padx=20, anchor="w")
        opts = ["Dashboard", "Add Student", "Add Marks", "Report", "Exit"]
        self.btns = {}
        for name in opts:
            b = tk.Button(bar, text=name, bg="#1E293B", fg="white", font=("Poppins", 13), anchor="w", padx=30,
                          activebackground="#3B82F6", command=lambda x=name: self.show(x))
            b.pack(fill="x", pady=4)
            self.btns[name] = b

    def body(self):
        self.main = tk.Frame(self.win, bg="white")
        self.main.place(x=240, y=0, width=1200, height=1024)

    def clear(self):
        for i in self.main.winfo_children():
            i.destroy()

    def show(self, name):
        if hasattr(self, "cur_btn"):
            self.btns[self.cur_btn].config(bg="#1E293B")
        self.btns[name].config(bg="#3B82F6")
        self.cur_btn = name
        self.clear()

        if name == "Dashboard":
            self.home()
        elif name == "Add Student":
            self.add()
        elif name == "Add Marks":
            self.marks()
        elif name == "Report":
            self.report()
        elif name == "Exit":
            self.win.destroy()

    def home(self):
        tk.Label(self.main, text="Dashboard", font=("Poppins", 18, "bold"), bg="white").place(x=30, y=30)
        s1 = self.cur.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        s2 = self.cur.execute("SELECT COUNT(*) FROM marks").fetchone()[0]
        stats = [(s1, "Students"), ("-", "Classes"), ("-", "Subjects"), (s2, "Marks")]
        for i, (val, txt) in enumerate(stats):
            f = tk.Frame(self.main, bg="#3B82F6", width=220, height=100)
            f.place(x=30 + i*240, y=80)
            tk.Label(f, text=val, font=("Poppins", 20, "bold"), bg="#3B82F6", fg="white").place(x=20, y=10)
            tk.Label(f, text=txt, font=("Poppins", 12), bg="#3B82F6", fg="white").place(x=20, y=55)

    def add(self):
        tk.Label(self.main, text="Add Student", font=("Poppins", 16, "bold"), bg="white").place(x=30, y=30)
        self.entries = {}
        fields = ["ID", "Name", "DOB", "Gender", "Address"]
        y = 80
        for f in fields:
            tk.Label(self.main, text=f, bg="white", font=("Poppins", 12)).place(x=30, y=y)
            e = tk.Entry(self.main, font=("Poppins", 12), width=40)
            e.place(x=180, y=y)
            self.entries[f] = e
            y += 40
        tk.Button(self.main, text="Save", bg="#3B82F6", fg="white", font=("Poppins", 12), command=self.save_stud).place(x=180, y=y)

    def save_stud(self):
        data = {k: v.get().strip() for k, v in self.entries.items()}
        if not data["ID"]:
            return messagebox.showwarning("No ID", "Enter ID")
        if self.cur.execute("SELECT * FROM students WHERE id = ?", (data["ID"],)).fetchone():
            return messagebox.showwarning("Exists", "ID exists already")
        self.cur.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?)",
                         (data["ID"], data["Name"], data["DOB"], data["Gender"], data["Address"]))
        self.db.commit()
        messagebox.showinfo("Saved", "Student added")
        for e in self.entries.values():
            e.delete(0, tk.END)

    def marks(self):
        tk.Label(self.main, text="Add Marks", font=("Poppins", 16, "bold"), bg="white").place(x=30, y=30)
        tk.Label(self.main, text="ID", bg="white", font=("Poppins", 12)).place(x=30, y=80)
        ids = [x[0] for x in self.cur.execute("SELECT id FROM students").fetchall()]
        self.sid = ttk.Combobox(self.main, values=ids, width=40)
        self.sid.place(x=180, y=80)

        tk.Label(self.main, text="Subject", bg="white", font=("Poppins", 12)).place(x=30, y=130)
        self.sub = tk.Entry(self.main, font=("Poppins", 12), width=40)
        self.sub.place(x=180, y=130)

        tk.Label(self.main, text="Marks", bg="white", font=("Poppins", 12)).place(x=30, y=180)
        self.mark = tk.Entry(self.main, font=("Poppins", 12), width=40)
        self.mark.place(x=180, y=180)

        tk.Button(self.main, text="Add", bg="#3B82F6", fg="white", font=("Poppins", 12), command=self.save_mark).place(x=180, y=230)

    def save_mark(self):
        sid = self.sid.get().strip()
        sub = self.sub.get().strip()
        mark = self.mark.get().strip()
        if not sid or not sub or not mark.isdigit():
            return messagebox.showwarning("Error", "Fill all correctly")
        self.cur.execute("INSERT INTO marks VALUES (?, ?, ?)", (sid, sub, int(mark)))
        self.db.commit()
        messagebox.showinfo("Saved", "Mark added")
        self.sub.delete(0, tk.END)
        self.mark.delete(0, tk.END)

    def report(self):
        tk.Label(self.main, text="Report", font=("Poppins", 16, "bold"), bg="white").place(x=30, y=30)
        cols = ("ID", "Name", "Subjects", "Average")
        tree = ttk.Treeview(self.main, columns=cols, show="headings")
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=180)
        for s in self.cur.execute("SELECT * FROM students").fetchall():
            sid, name = s[0], s[1]
            data = self.cur.execute("SELECT subject, marks FROM marks WHERE sid=?", (sid,)).fetchall()
            subs = ", ".join(x[0] for x in data) if data else "-"
            avg = f"{sum(x[1] for x in data)/len(data):.1f}" if data else "-"
            tree.insert("", "end", values=(sid, name, subs, avg))
        tree.place(x=30, y=80, width=800, height=400)

if __name__ == "__main__":
    Student()
