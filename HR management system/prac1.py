import tkinter as tk
from tkinter import ttk, messagebox
import csv
import matplotlib.pyplot as plt

class Employee:
    def __init__(self, name, emp_id, department, position, salary):
        self.name = name
        self.emp_id = emp_id
        self.department = department
        self.position = position
        self.salary = salary
        self.attendance = 0
        self.leave_days = 0
        self.performance_history = [3]  # Initial performance score is 3

    def update_performance(self, score):
        self.performance_history.append(score)

class HRManagementSystem:
    def __init__(self):
        self.employees = {}

    def add_employee(self, emp: Employee):
        self.employees[emp.emp_id] = emp

    def mark_attendance(self, emp_id):
        if emp_id in self.employees:
            self.employees[emp_id].attendance += 1
            return True
        return False

    def apply_leave(self, emp_id, days):
        if emp_id in self.employees:
            self.employees[emp_id].leave_days += days
            return True
        return False

    def update_performance(self, emp_id, score):
        if emp_id in self.employees:
            self.employees[emp_id].update_performance(score)
            return True
        return False

    def export_data(self, filename='employee_data.csv'):
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Name', 'Department', 'Position', 'Salary', 'Attendance', 'Leaves', 'Performance'])
            for emp in self.employees.values():
                writer.writerow([emp.emp_id, emp.name, emp.department, emp.position, emp.salary,
                                 emp.attendance, emp.leave_days, ','.join(map(str, emp.performance_history))])

    def get_performance_data(self):
        """Fetches performance data for charting."""
        emp_names = []
        emp_performances = []
        for emp in self.employees.values():
            emp_names.append(emp.name)
            emp_performances.append(emp.performance_history)
        return emp_names, emp_performances

class HRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HR Management System")
        self.root.geometry("600x500")
        self.system = HRManagementSystem()
        self.setup_gui()

    def setup_gui(self):
        tabControl = ttk.Notebook(self.root)

        self.tab1 = ttk.Frame(tabControl)
        self.tab2 = ttk.Frame(tabControl)
        self.tab3 = ttk.Frame(tabControl)
        self.tab4 = ttk.Frame(tabControl)

        tabControl.add(self.tab1, text='Add Employee')
        tabControl.add(self.tab2, text='Attendance & Leave')
        tabControl.add(self.tab3, text='Performance')
        tabControl.add(self.tab4, text='Export')

        tabControl.pack(expand=1, fill="both")

        self.setup_add_employee()
        self.setup_attendance_leave()
        self.setup_performance()
        self.setup_export()

    def setup_add_employee(self):
        ttk.Label(self.tab1, text="Name").grid(row=0, column=0, padx=10, pady=10)
        self.name_entry = ttk.Entry(self.tab1)
        self.name_entry.grid(row=0, column=1)

        ttk.Label(self.tab1, text="Employee ID").grid(row=1, column=0, padx=10, pady=10)
        self.id_entry = ttk.Entry(self.tab1)
        self.id_entry.grid(row=1, column=1)

        ttk.Label(self.tab1, text="Department").grid(row=2, column=0, padx=10, pady=10)
        self.dept_entry = ttk.Entry(self.tab1)
        self.dept_entry.grid(row=2, column=1)

        ttk.Label(self.tab1, text="Position").grid(row=3, column=0, padx=10, pady=10)
        self.position_entry = ttk.Entry(self.tab1)
        self.position_entry.grid(row=3, column=1)

        ttk.Label(self.tab1, text="Salary").grid(row=4, column=0, padx=10, pady=10)
        self.salary_entry = ttk.Entry(self.tab1)
        self.salary_entry.grid(row=4, column=1)

        ttk.Button(self.tab1, text="Add", command=self.add_employee).grid(row=5, column=0, columnspan=2, pady=20)

    def setup_attendance_leave(self):
        ttk.Label(self.tab2, text="Employee ID").grid(row=0, column=0, padx=10, pady=10)
        self.attend_id_entry = ttk.Entry(self.tab2)
        self.attend_id_entry.grid(row=0, column=1)

        ttk.Button(self.tab2, text="Mark Attendance", command=self.mark_attendance).grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Label(self.tab2, text="Leave Days").grid(row=2, column=0, padx=10, pady=10)
        self.leave_entry = ttk.Entry(self.tab2)
        self.leave_entry.grid(row=2, column=1)

        ttk.Button(self.tab2, text="Apply Leave", command=self.apply_leave).grid(row=3, column=0, columnspan=2, pady=10)

        # Display current attendance and leave days
        self.attendance_label = ttk.Label(self.tab2, text="Attendance: 0 | Leave Days: 0")
        self.attendance_label.grid(row=4, column=0, columnspan=2)

    def setup_performance(self):
        ttk.Label(self.tab3, text="Employee ID").grid(row=0, column=0, padx=10, pady=10)
        self.perf_id_entry = ttk.Entry(self.tab3)
        self.perf_id_entry.grid(row=0, column=1)

        ttk.Label(self.tab3, text="Performance Score (1-5)").grid(row=1, column=0, padx=10, pady=10)
        self.perf_score_entry = ttk.Entry(self.tab3)
        self.perf_score_entry.grid(row=1, column=1)

        ttk.Button(self.tab3, text="Update", command=self.update_performance).grid(row=2, column=0, columnspan=2, pady=20)

        # Button to display performance chart
        ttk.Button(self.tab3, text="Show Performance Chart", command=self.show_performance_chart).grid(row=3, column=0, columnspan=2, pady=10)

    def setup_export(self):
        ttk.Button(self.tab4, text="Export Data to CSV", command=self.export_data).pack(pady=100)

    def add_employee(self):
        try:
            emp = Employee(
                self.name_entry.get(),
                self.id_entry.get(),
                self.dept_entry.get(),
                self.position_entry.get(),
                float(self.salary_entry.get())
            )
            self.system.add_employee(emp)
            messagebox.showinfo("Success", "Employee added.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def mark_attendance(self):
        emp_id = self.attend_id_entry.get()
        if self.system.mark_attendance(emp_id):
            messagebox.showinfo("Success", "Attendance marked.")
            self.update_attendance_leave_display(emp_id)
        else:
            messagebox.showerror("Error", "Employee not found.")

    def apply_leave(self):
        emp_id = self.attend_id_entry.get()
        try:
            days = int(self.leave_entry.get())
            if self.system.apply_leave(emp_id, days):
                messagebox.showinfo("Success", "Leave applied.")
                self.update_attendance_leave_display(emp_id)
            else:
                messagebox.showerror("Error", "Employee not found.")
        except ValueError:
            messagebox.showerror("Error", "Invalid leave days.")

    def update_attendance_leave_display(self, emp_id):
        emp = self.system.employees.get(emp_id)
        if emp:
            self.attendance_label.config(text=f"Attendance: {emp.attendance} | Leave Days: {emp.leave_days}")

    def update_performance(self):
        emp_id = self.perf_id_entry.get()
        try:
            score = int(self.perf_score_entry.get())
            if 1 <= score <= 5:
                if self.system.update_performance(emp_id, score):
                    messagebox.showinfo("Success", "Performance updated.")
                else:
                    messagebox.showerror("Error", "Employee not found.")
            else:
                messagebox.showerror("Error", "Score must be 1 to 5.")
        except ValueError:
            messagebox.showerror("Error", "Invalid score.")

    def export_data(self):
        self.system.export_data()
        messagebox.showinfo("Export", "Data exported to 'employee_data.csv'.")

    def show_performance_chart(self):
        names, scores = self.system.get_performance_data()

        if not names:
            messagebox.showinfo("No Data", "No performance data available.")
            return

        plt.figure(figsize=(10, 5))

        for i, performance_history in enumerate(scores):
            plt.plot(range(1, len(performance_history) + 1), performance_history, marker='o', label=names[i])

        plt.title('Employee Performance Over Time')
        plt.xlabel('Time')
        plt.ylabel('Performance Score')
        plt.legend()
        plt.grid(True)
        plt.show()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = HRApp(root)
    root.mainloop()
