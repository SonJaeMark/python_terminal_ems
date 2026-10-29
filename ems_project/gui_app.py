import os
import django
import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal, InvalidOperation

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ems_project.settings")
django.setup()

from django.db.models import Q
from employees.models import Employee


class EmployeeApp:
    COLUMNS = [
        ("ID", 45), ("Name", 140), ("Position", 120), ("Department", 100),
        ("Email", 170), ("Phone", 100), ("Salary", 90), ("Status", 70), ("Date Hired", 120),
    ]

    def __init__(self, root):
        self.root = root
        root.title("Employee Management System")
        root.geometry("1250x600")
        root.minsize(1000, 500)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=26, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"))
        style.configure("Add.TButton", background="#2e7d32", foreground="white")
        style.configure("Del.TButton", background="#c62828", foreground="white")
        style.map("Add.TButton", background=[("active", "#388e3c")])
        style.map("Del.TButton", background=[("active", "#d32f2f")])

        self.show_inactive = tk.BooleanVar(value=False)
        self.search_var = tk.StringVar()
        self.id_var = tk.StringVar()

        self.build_form()
        self.build_table_area()
        self.refresh()

    # ---------- Layout ----------
    def build_form(self):
        form = ttk.LabelFrame(self.root, text="New Employee", padding=12)
        form.pack(side="left", fill="y", padx=10, pady=10)

        self.entries = {}
        fields = [("Name", "name"), ("Position", "position"),
                  ("Email", "email"), ("Phone", "phone"), ("Salary", "salary")]
        row = 0
        for label, key in fields:
            ttk.Label(form, text=label).grid(row=row, column=0, sticky="w", pady=4)
            entry = ttk.Entry(form, width=28)
            entry.grid(row=row, column=1, pady=4, padx=(8, 0))
            self.entries[key] = entry
            row += 1

        ttk.Label(form, text="Department").grid(row=row, column=0, sticky="w", pady=4)
        self.dept_combo = ttk.Combobox(form, values=Employee.DEPARTMENTS,
                                       state="readonly", width=25)
        self.dept_combo.current(0)
        self.dept_combo.grid(row=row, column=1, pady=4, padx=(8, 0))
        row += 1

        ttk.Button(form, text="Add Employee", style="Add.TButton",
                   command=self.add_employee).grid(row=row, column=0, columnspan=2,
                                                   sticky="ew", pady=(14, 4))
        ttk.Button(form, text="Clear", command=self.clear_form).grid(
            row=row + 1, column=0, columnspan=2, sticky="ew")

    def build_table_area(self):
        right = ttk.Frame(self.root)
        right.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=10)

        ttk.Label(right, text="Employees", style="Title.TLabel").pack(anchor="w")

        # Search + filter bar
        bar = ttk.Frame(right)
        bar.pack(fill="x", pady=6)
        ttk.Label(bar, text="Search:").pack(side="left")
        search = ttk.Entry(bar, textvariable=self.search_var, width=30)
        search.pack(side="left", padx=6)
        search.bind("<KeyRelease>", lambda e: self.refresh())
        ttk.Checkbutton(bar, text="Show inactive", variable=self.show_inactive,
                        command=self.refresh).pack(side="left", padx=10)
        self.count_label = ttk.Label(bar, text="")
        self.count_label.pack(side="right")

        # Table
        wrap = ttk.Frame(right)
        wrap.pack(fill="both", expand=True)
        self.tree = ttk.Treeview(wrap, columns=[c for c, _ in self.COLUMNS],
                                 show="headings", selectmode="browse")
        for col, width in self.COLUMNS:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="w")
        self.tree.tag_configure("inactive", foreground="#9e9e9e")
        self.tree.tag_configure("odd", background="#f5f5f5")
        scroll = ttk.Scrollbar(wrap, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Delete / restore by ID
        actions = ttk.LabelFrame(right, text="Delete / Restore by ID", padding=8)
        actions.pack(fill="x", pady=(8, 0))
        ttk.Label(actions, text="Employee ID:").pack(side="left")
        ttk.Entry(actions, textvariable=self.id_var, width=10).pack(side="left", padx=6)
        ttk.Button(actions, text="Delete (soft)", style="Del.TButton",
                   command=self.delete_by_id).pack(side="left", padx=4)
        ttk.Button(actions, text="Restore",
                   command=self.restore_by_id).pack(side="left", padx=4)

    # ---------- Actions ----------
    def add_employee(self):
        name = self.entries["name"].get().strip()
        position = self.entries["position"].get().strip()
        email = self.entries["email"].get().strip()
        phone = self.entries["phone"].get().strip()
        salary_text = self.entries["salary"].get().strip() or "0"

        if not name or not position:
            messagebox.showwarning("Validation Error", "Name and Position are required.")
            return
        if email and ("@" not in email or "." not in email):
            messagebox.showwarning("Validation Error", "Please enter a valid email.")
            return
        try:
            salary = Decimal(salary_text)
            if salary < 0:
                raise InvalidOperation
        except InvalidOperation:
            messagebox.showwarning("Validation Error", "Salary must be a positive number.")
            return

        Employee.objects.create(
            name=name, position=position, email=email, phone=phone,
            department=self.dept_combo.get(), salary=salary,
        )
        self.clear_form()
        self.refresh()
        messagebox.showinfo("Success", f"Employee '{name}' added.")

    def _get_employee_from_id(self):
        text = self.id_var.get().strip()
        if not text.isdigit():
            messagebox.showwarning("Invalid ID", "Enter a numeric employee ID.")
            return None
        try:
            return Employee.objects.get(pk=int(text))
        except Employee.DoesNotExist:
            messagebox.showerror("Not found", f"No employee with ID {text}.")
            return None

    def delete_by_id(self):
        emp = self._get_employee_from_id()
        if not emp:
            return
        if not emp.is_available:
            messagebox.showinfo("Already inactive", f"{emp.name} is already deleted.")
            return
        if messagebox.askyesno("Confirm", f"Soft delete #{emp.id} - {emp.name}?"):
            emp.soft_delete()
            self.id_var.set("")
            self.refresh()

    def restore_by_id(self):
        emp = self._get_employee_from_id()
        if not emp:
            return
        if emp.is_available:
            messagebox.showinfo("Already active", f"{emp.name} is already active.")
            return
        emp.restore()
        self.id_var.set("")
        self.refresh()

    # ---------- Helpers ----------
    def on_select(self, _event):
        selected = self.tree.selection()
        if selected:
            self.id_var.set(self.tree.item(selected[0])["values"][0])

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.dept_combo.current(0)

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        qs = Employee.objects.all()
        if not self.show_inactive.get():
            qs = qs.filter(is_available=True)
        term = self.search_var.get().strip()
        if term:
            qs = qs.filter(
                Q(name__icontains=term) | Q(position__icontains=term) |
                Q(email__icontains=term) | Q(department__icontains=term)
            )

        for i, emp in enumerate(qs):
            tags = []
            if i % 2:
                tags.append("odd")
            if not emp.is_available:
                tags.append("inactive")
            self.tree.insert("", tk.END, tags=tags, values=(
                emp.id, emp.name, emp.position, emp.department, emp.email,
                emp.phone, f"{emp.salary:,.2f}",
                "Active" if emp.is_available else "Inactive",
                emp.date_hired.strftime("%Y-%m-%d"),
            ))
        self.count_label.config(text=f"{qs.count()} record(s)")


if __name__ == "__main__":
    root = tk.Tk()
    EmployeeApp(root)
    root.mainloop()