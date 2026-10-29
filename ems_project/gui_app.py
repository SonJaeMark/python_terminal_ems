import os
import django
import tkinter as tk
from tkinter import messagebox, ttk

# 1. Initialize Django environment within the script
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ems_project.settings')
django.setup()

# Import model after django.setup()
from employees.models import Employee

# 2. Tkinter GUI Logic
def add_employee():
    name = name_entry.get().strip()
    position = position_entry.get().strip()

    # Input validation
    if not name or not position:
        messagebox.showwarning("Validation Error", "Both Name and Position are required!")
        return

    # Save record to Django ORM
    Employee.objects.create(name=name, position=position)
    
    # Clear input fields
    name_entry.delete(0, tk.END)
    position_entry.delete(0, tk.END)
    
    messagebox.showinfo("Success", f"Employee '{name}' added successfully!")
    refresh_employee_list()

def refresh_employee_list():
    # Clear existing rows in treeview
    for row in tree.get_children():
        tree.delete(row)
        
    # Fetch all records from Django ORM database
    for emp in Employee.objects.all():
        tree.insert("", tk.END, values=(emp.id, emp.name, emp.position, emp.date_hired.strftime("%Y-%m-%d %H:%M")))

# Setup Window
root = tk.Tk()
root.title("Employee Management System")
root.geometry("550x400")

# Form Inputs
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="x")

tk.Label(frame, text="Name:").grid(row=0, column=0, sticky="w", pady=2)
name_entry = tk.Entry(frame, width=30)
name_entry.grid(row=0, column=1, pady=2)

tk.Label(frame, text="Position:").grid(row=1, column=0, sticky="w", pady=2)
position_entry = tk.Entry(frame, width=30)
position_entry.grid(row=1, column=1, pady=2)

add_btn = tk.Button(frame, text="Add Employee", command=add_employee, bg="#4CAF50", fg="white")
add_btn.grid(row=2, column=0, columnspan=2, pady=10)

# Display List (Treeview)
tree = ttk.Treeview(root, columns=("ID", "Name", "Position", "Date Hired"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Position", text="Position")
tree.heading("Date Hired", text="Date Hired")

tree.column("ID", width=40)
tree.column("Name", width=150)
tree.column("Position", width=150)
tree.column("Date Hired", width=150)

tree.pack(padx=10, pady=10, fill="both", expand=True)

# Initial load of records
refresh_employee_list()

root.mainloop()