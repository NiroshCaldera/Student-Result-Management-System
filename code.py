import customtkinter as ctk
import json, os
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

ACCOUNTS_FILE = "accounts.json"

def load_accounts():
    try:
        with open(ACCOUNTS_FILE, "r") as f:
            return json.load(f)
    except:
        return {"admin":"123"}  # default login

def save_accounts(accounts):
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f, indent=4)

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("450x360")
        self.title("EduTech Solutions - Login")

        self.accounts = load_accounts()

        ctk.CTkLabel(self, text="Teacher Login", font=("Segoe UI", 22, "bold")).pack(pady=15)

        self.username = ctk.CTkEntry(self, width=260, placeholder_text="Username")
        self.username.pack(pady=8)

        self.password = ctk.CTkEntry(self, width=260, placeholder_text="Password", show="*")
        self.password.pack(pady=8)

        ctk.CTkButton(self, text="Login", width=240, command=self.login).pack(pady=18)

        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=8)

        ctk.CTkButton(btn_frame, text="Create Account", width=150, command=self.create_account_window).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="Delete Account", width=150, command=self.delete_account_window).grid(row=0, column=1, padx=5)

    def login(self):
        user = self.username.get()
        pwd = self.password.get()
        if user in self.accounts and self.accounts[user] == pwd:
            self.destroy()
            MainWindow()
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password")

    def create_account_window(self):
        win = ctk.CTkToplevel(self)
        win.title("Create Account")
        win.geometry("380x260")
        ctk.CTkLabel(win, text="New Account", font=("Segoe UI", 20, "bold")).pack(pady=10)
        u = ctk.CTkEntry(win, width=260, placeholder_text="Username")
        u.pack(pady=6)
        p = ctk.CTkEntry(win, width=260, placeholder_text="Password", show="*")
        p.pack(pady=6)
        def create():
            username = u.get()
            password = p.get()
            if username in self.accounts:
                messagebox.showerror("Error", "Username already exists")
                return
            if len(username) < 3 or len(password) < 3:
                messagebox.showerror("Error", "Username & Password must be at least 3 characters")
                return
            self.accounts[username] = password
            save_accounts(self.accounts)
            messagebox.showinfo("Success", "Account Created")
            win.destroy()
        ctk.CTkButton(win, text="Create", command=create).pack(pady=12)

    def delete_account_window(self):
        win = ctk.CTkToplevel(self)
        win.title("Delete Account")
        win.geometry("380x240")
        ctk.CTkLabel(win, text="Delete Account", font=("Segoe UI", 20, "bold")).pack(pady=12)
        u = ctk.CTkEntry(win, width=260, placeholder_text="Username")
        u.pack(pady=6)
        p = ctk.CTkEntry(win, width=260, placeholder_text="Password", show="*")
        p.pack(pady=6)
        def delete():
            username = u.get()
            password = p.get()
            if username not in self.accounts or self.accounts[username] != password:
                messagebox.showerror("Error", "Account not found or incorrect password")
                return
            if username == "admin":
                messagebox.showerror("Error", "Admin account cannot be deleted")
                return
            del self.accounts[username]
            save_accounts(self.accounts)
            messagebox.showinfo("Deleted", "Account Deleted")
            win.destroy()
        ctk.CTkButton(win, text="Delete", command=delete).pack(pady=12)

# ------------------------ Student Class ------------------------
class Student:
    def __init__(self, sid, name, marks):
        self.sid = sid
        self.name = name
        self.marks = marks
        self.total = sum(marks.values())
        self.percentage = (self.total / 500) * 100
        self.grade = ""
        self.gpa = ""

    def grade_calc(self):
        p = self.percentage
        if p >= 90: return "A"
        elif p >= 80: return "B"
        elif p >= 70: return "C"
        elif p >= 60: return "D"
        else: return "F"

    def gpa_calc(self):
        table = {"A":4.0, "B":3.0, "C":2.0, "D":1.0, "F":0.0}
        return table[self.grade]

# ------------------------ Main Window ------------------------
class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.students = []
        self.geometry("1000x700")
        self.title("EduTech Solutions - Student Result Management System")
        self.buildUI()
        self.mainloop()

    def buildUI(self):
        header = ctk.CTkLabel(self, text="Student Result Management System",
                              font=("Segoe UI", 24, "bold"))
        header.pack(pady=15)

        # Input Frame
        frame = ctk.CTkFrame(self, corner_radius=12)
        frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(frame, text="Student ID").grid(row=0, column=0, padx=10, pady=8, sticky="e")
        self.sid = ctk.CTkEntry(frame, width=180)
        self.sid.grid(row=0, column=1, padx=10, pady=8)

        ctk.CTkLabel(frame, text="Full Name").grid(row=0, column=2, padx=10, pady=8, sticky="e")
        self.sname = ctk.CTkEntry(frame, width=260)
        self.sname.grid(row=0, column=3, padx=10, pady=8)

        ctk.CTkLabel(
            frame,
            text="Subject Marks",
            font=("Segoe UI", 14, "bold")
        ).grid(row=1, column=0, columnspan=2, pady=(10, 5))

        self.mark_entries = {}
        subjects = ["Maths", "Science", "English", "History", "ICT"]
        start_row = 2  # starts below Student ID / Name row

        for i, sub in enumerate(subjects):
            ctk.CTkLabel(frame, text=f"{sub} Marks").grid(
                row=start_row + i, column=0, padx=10, pady=6, sticky="e"
            )

            e = ctk.CTkEntry(frame, width=180)
            e.grid(
                row=start_row + i, column=1, padx=10, pady=6, sticky="w"
            )
            self.mark_entries[sub] = e

        # Buttons
        ctk.CTkButton(frame, text="Add Student", width=150, command=self.add_student).grid(row=2, column=2, pady=10, padx=5)
        ctk.CTkButton(frame, text="Edit Marks", width=150, command=self.edit_marks).grid(row=2, column=3, padx=5)
        ctk.CTkButton(frame, text="Calculate Grade", width=150, command=self.calculate_grades).grid(row=2, column=4, padx=5)
        ctk.CTkButton(frame, text="View Results", width=150, command=self.view_results).grid(row=3, column=2, padx=5)
        ctk.CTkButton(frame, text="Save CSV", width=150, command=self.save_csv).grid(row=3, column=3, padx=5)
        ctk.CTkButton(frame, text="Load CSV", width=150, command=self.load_csv).grid(row=3, column=4, padx=5)
        ctk.CTkButton(frame, text="Export PDF", width=150, command=self.export_pdf).grid(row=3, column=3, padx=5)
        ctk.CTkButton(frame, text="Logout", width=150, command=self.logout, fg_color="#D68802").grid(row=4, column=3, padx=5)
        ctk.CTkButton(frame, text="Exit", width=150, command=self.destroy, fg_color="#D32F2F").grid(row=4, column=2, padx=5)

        # Treeview
        table_frame = ctk.CTkFrame(self, corner_radius=12)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        cols = ("ID","Name","Total","%","Grade","GPA")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=12)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        self.tree.pack(fill="both", expand=True)

    # ------------------- Actions -------------------
    def add_student(self):
        try:
            sid = int(self.sid.get())
            name = self.sname.get()
            marks = {}
            for sub, entry in self.mark_entries.items():
                val = int(entry.get())
                if val < 0 or val > 100:
                    messagebox.showerror("Invalid Input", "Marks must be 0-100")
                    return
                marks[sub] = val
            s = Student(sid, name, marks)
            self.students.append(s)
            self.refresh()
            self.clear()
            messagebox.showinfo("Success", "Student Added")
        except:
            messagebox.showerror("Input Error", "Enter Valid Data")

    def calculate_grades(self):
        if not self.students:
            messagebox.showwarning("No Data", "No student records available")
            return
        for s in self.students:
            s.grade = s.grade_calc()
            s.gpa = s.gpa_calc()
        self.refresh()
        messagebox.showinfo("Calculated", "Grades Calculated Successfully")

    def edit_marks(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Select Student", "Select a student to edit marks")
            return
        values = self.tree.item(selected, "values")
        sid = int(values[0])
        student = next((s for s in self.students if s.sid == sid), None)
        if not student: return

        win = ctk.CTkToplevel(self)
        win.title(f"Edit Marks - {student.name}")
        win.geometry("400x300")

        entries = {}
        ctk.CTkLabel(win, text=f"Editing Marks for {student.name}", font=("Segoe UI", 16, "bold")).pack(pady=10)

        for sub in student.marks.keys():
            frame = ctk.CTkFrame(win)
            frame.pack(pady=4, padx=10, fill="x")
            ctk.CTkLabel(frame, text=sub, width=100).pack(side="left", padx=5)
            e = ctk.CTkEntry(frame, width=150)
            e.insert(0, str(student.marks[sub]))
            e.pack(side="left", padx=5)
            entries[sub] = e

        def save_changes():
            try:
                for sub, e in entries.items():
                    val = int(e.get())
                    if val < 0 or val > 100:
                        messagebox.showerror("Invalid Input", "Marks must be 0-100")
                        return
                    student.marks[sub] = val
                # Update total and percentage only, do NOT calculate grade
                student.total = sum(student.marks.values())
                student.percentage = (student.total / 500) * 100
                self.refresh()
                messagebox.showinfo("Updated", "Marks Updated Successfully. Click 'Calculate Grade' to update grade and GPA.")
                win.destroy()
            except:
                messagebox.showerror("Error", "Invalid input")

        ctk.CTkButton(win, text="Save", command=save_changes).pack(pady=10)

    def view_results(self):
        if not self.students:
            messagebox.showwarning("No Data", "No student records available")
            return
        win = ctk.CTkToplevel(self)
        win.title("View Student Results")
        win.geometry("800x500")

        cols = ("ID","Name","Total","%","Grade","GPA")
        tree = ttk.Treeview(win, columns=cols, show="headings", height=18)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=120)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        for i,s in enumerate(self.students):
            tag = "evenrow" if i%2==0 else "oddrow"
            tree.insert("", "end", values=(s.sid, s.name, s.total, f"{s.percentage:.2f}%", s.grade, s.gpa), tags=(tag,))
        tree.tag_configure("evenrow", background="#f0f0ff")
        tree.tag_configure("oddrow", background="#ffffff")

        avg_percentage = sum([s.percentage for s in self.students])/len(self.students)
        top_student = max(self.students, key=lambda x:x.percentage)
        summary = f"Total Students: {len(self.students)} | Average %: {avg_percentage:.2f}% | Top Student: {top_student.name} ({top_student.percentage:.2f}%)"
        ctk.CTkLabel(win, text=summary, font=("Segoe UI", 14, "bold")).pack(pady=8)

    # ------------------- Utility Functions -------------------
    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for i, s in enumerate(self.students):
            tag = "evenrow" if i%2==0 else "oddrow"
            self.tree.insert("", "end", values=(s.sid, s.name, s.total, f"{s.percentage:.2f}%", s.grade, s.gpa), tags=(tag,))
        self.tree.tag_configure("evenrow", background="#f0f0ff")
        self.tree.tag_configure("oddrow", background="#ffffff")

    def clear(self):
        self.sid.delete(0,"end")
        self.sname.delete(0,"end")
        for e in self.mark_entries.values(): e.delete(0,"end")

    def save_csv(self):
        file = filedialog.asksaveasfilename(defaultextension=".csv")
        if not file: return
        data = []
        for s in self.students:
            row = {"ID": s.sid, "Name": s.name}
            row.update(s.marks)  # add subject marks individually
            row.update({"Total": s.total, "Percentage": s.percentage, "Grade": s.grade, "GPA": s.gpa})
            data.append(row)
        df = pd.DataFrame(data)
        df.to_csv(file, index=False)
        messagebox.showinfo("Saved","CSV Saved Successfully")


    def load_csv(self):
        file = filedialog.askopenfilename()
        if not file: return
        df = pd.read_csv(file)
        self.students.clear()
        for _, r in df.iterrows():
            marks = {}
            for sub in ["Maths", "Science", "English", "History", "ICT"]:
                try:
                    marks[sub] = int(r[sub])
                except:
                    marks[sub] = 0
            dummy = Student(int(r["ID"]), r["Name"], marks)
            dummy.total = r.get("Total", sum(marks.values()))
            dummy.percentage = r.get("Percentage", (dummy.total / 500) * 100)
            dummy.grade = r.get("Grade", "")
            dummy.gpa = r.get("GPA", "")
            self.students.append(dummy)
        self.refresh()


    def export_pdf(self):
        file = filedialog.asksaveasfilename(defaultextension=".pdf")
        if not file: return
        c = canvas.Canvas(file, pagesize=A4)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50,800,"Student Results Report")
        y=760
        for s in self.students:
            c.setFont("Helvetica",11)
            c.drawString(50,y,f"{s.sid} | {s.name} | Total: {s.total} | %: {s.percentage:.2f} | Grade: {s.grade}")
            y-=22
        c.save()
        messagebox.showinfo("Exported","PDF Exported Successfully")

    def logout(self):
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirm:
            self.destroy()
            LoginWindow()  # reopen login window


if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()
