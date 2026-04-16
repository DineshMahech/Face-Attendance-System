import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import pandas as pd
import os
import winsound
from datetime import datetime

from capture import capture_images
from train import train_model
from recognize import recognize_faces
from main import delete_employee


# ==============================
# FUNCTIONS
# ==============================

def update_status(msg):
    status_label.config(text=msg)


def register_student():
    Id = simpledialog.askstring("Input", "Enter ID:")
    name = simpledialog.askstring("Input", "Enter Name:")

    if Id and name:
        capture_images(Id, name)
        update_status(f"Registered {name}")
    else:
        messagebox.showerror("Error", "Invalid input!")


def train():
    train_model()
    update_status("Training Completed")
    winsound.Beep(1000, 300)


def start_attendance():
    recognize_faces()
    update_status("Attendance session completed")
    winsound.Beep(1200, 300)


def delete_emp():
    Id = simpledialog.askstring("Delete", "Enter ID to delete:")

    if not Id:
        return

    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete?")
    if confirm:
        delete_employee(Id)
        update_status(f"Deleted ID {Id}")


def view_students():
    file = "EmployeeDetails/EmployeeDetails.csv"

    if not os.path.isfile(file):
        messagebox.showerror("Error", "No student data found!")
        return

    df = pd.read_csv(file)

    win = tk.Toplevel(root)
    win.title("Registered Students")

    tree = ttk.Treeview(win, columns=("ID", "Name"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")

    for _, row in df.iterrows():
        tree.insert("", "end", values=(row["ID"], row["Name"]))

    tree.pack(fill="both", expand=True)


def export_excel():
    csv_file = "Attendance/Attendance.csv"

    if not os.path.isfile(csv_file):
        messagebox.showerror("Error", "No attendance data found!")
        return

    df = pd.read_csv(csv_file)

    date = datetime.now().strftime("%Y-%m-%d")
    excel_file = f"Attendance/Attendance_{date}.xlsx"

    df.to_excel(excel_file, index=False)

    update_status("Exported to Excel")
    winsound.Beep(1500, 300)


def open_attendance_folder():
    path = os.path.abspath("Attendance")
    os.startfile(path)


# ==============================
# GUI DESIGN
# ==============================

root = tk.Tk()
root.title("Face Attendance System")
root.geometry("450x550")
root.configure(bg="#2c3e50")

title = tk.Label(root, text="FACE ATTENDANCE SYSTEM",
                 bg="#2c3e50", fg="white",
                 font=("Arial", 16, "bold"))
title.pack(pady=20)

btn_style = {
    "width": 25,
    "font": ("Arial", 11, "bold"),
    "fg": "white",
    "padx": 5,
    "pady": 5
}

tk.Button(root, text="Register Student",
          bg="#3498db", command=register_student, **btn_style).pack(pady=5)

tk.Button(root, text="Train Model",
          bg="#9b59b6", command=train, **btn_style).pack(pady=5)

tk.Button(root, text="Start Attendance",
          bg="#27ae60", command=start_attendance, **btn_style).pack(pady=5)

tk.Button(root, text="Delete Employee",
          bg="#e74c3c", command=delete_emp, **btn_style).pack(pady=5)

tk.Button(root, text="View Students",
          bg="#16a085", command=view_students, **btn_style).pack(pady=5)

tk.Button(root, text="Export to Excel",
          bg="#f39c12", command=export_excel, **btn_style).pack(pady=5)

tk.Button(root, text="Open Attendance Folder",
          bg="#34495e", command=open_attendance_folder, **btn_style).pack(pady=5)

tk.Button(root, text="Exit",
          bg="black", command=root.quit, **btn_style).pack(pady=20)


# ==============================
# STATUS LABEL
# ==============================

status_label = tk.Label(root, text="Welcome!",
                        bg="#2c3e50", fg="yellow",
                        font=("Arial", 10))
status_label.pack(pady=10)


# ==============================
# RUN GUI
# ==============================

root.mainloop()