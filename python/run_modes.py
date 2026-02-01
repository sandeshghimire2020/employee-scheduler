import os
from scheduler import EmployeeScheduler
from file_loader import load_from_file


def run_demo():
    print("\n" + "="*70)
    print("EMPLOYEE SCHEDULING SYSTEM - DEMO MODE")
    print("="*70 + "\n")
    
    scheduler = EmployeeScheduler()
    
    print("Adding employees...")
    employees = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry"]
    for emp in employees:
        scheduler.add_employee(emp)
    
    print("\n" + "-"*70)
    print("Adding shift preferences...")
    print("-"*70 + "\n")
    
    scheduler.add_preference("Alice", "Monday", ["Morning", "Afternoon"])
    scheduler.add_preference("Alice", "Wednesday", ["Morning"])
    scheduler.add_preference("Alice", "Friday", ["Afternoon"])
    
    scheduler.add_preference("Bob", "Monday", ["Morning"])
    scheduler.add_preference("Bob", "Tuesday", ["Afternoon"])
    scheduler.add_preference("Bob", "Thursday", ["Evening"])
    scheduler.add_preference("Bob", "Saturday", ["Morning"])
    
    scheduler.add_preference("Charlie", "Tuesday", ["Morning", "Afternoon"])
    scheduler.add_preference("Charlie", "Wednesday", ["Afternoon"])
    scheduler.add_preference("Charlie", "Friday", ["Morning"])
    scheduler.add_preference("Charlie", "Sunday", ["Afternoon"])
    
    scheduler.add_preference("Diana", "Monday", ["Afternoon"])
    scheduler.add_preference("Diana", "Wednesday", ["Evening"])
    scheduler.add_preference("Diana", "Thursday", ["Morning"])
    scheduler.add_preference("Diana", "Saturday", ["Afternoon"])
    
    scheduler.add_preference("Eve", "Tuesday", ["Evening"])
    scheduler.add_preference("Eve", "Thursday", ["Afternoon"])
    scheduler.add_preference("Eve", "Friday", ["Evening"])
    scheduler.add_preference("Eve", "Sunday", ["Morning"])
    
    scheduler.add_preference("Frank", "Monday", ["Evening"])
    scheduler.add_preference("Frank", "Wednesday", ["Morning"])
    scheduler.add_preference("Frank", "Friday", ["Afternoon"])
    scheduler.add_preference("Frank", "Saturday", ["Evening"])
    
    scheduler.add_preference("Grace", "Tuesday", ["Morning"])
    scheduler.add_preference("Grace", "Thursday", ["Morning"])
    scheduler.add_preference("Grace", "Friday", ["Evening"])
    scheduler.add_preference("Grace", "Sunday", ["Afternoon"])
    
    scheduler.add_preference("Henry", "Monday", ["Morning"])
    scheduler.add_preference("Henry", "Wednesday", ["Afternoon"])
    scheduler.add_preference("Henry", "Thursday", ["Evening"])
    scheduler.add_preference("Henry", "Saturday", ["Morning"])
    
    scheduler.assign_shifts()
    scheduler.resolve_conflicts()
    scheduler.display_schedule()
    scheduler.get_statistics()


def run_interactive():
    print("\n" + "="*70)
    print("EMPLOYEE SCHEDULING SYSTEM - INTERACTIVE MODE")
    print("="*70 + "\n")
    
    scheduler = EmployeeScheduler()
    
    while True:
        try:
            num_employees = int(input("How many employees do you want to add? "))
            if num_employees > 0:
                break
            print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")
    
    print("\nEnter employee names:")
    for i in range(num_employees):
        while True:
            name = input(f"  Employee {i+1}: ").strip()
            if name:
                scheduler.add_employee(name)
                break
            print("  Name cannot be empty.")
    
    # Add preferences
    print("\n" + "-"*70)
    print("Add shift preferences for each employee")
    print("Format: Enter shift numbers separated by spaces (1=Morning, 2=Afternoon, 3=Evening)")
    print("Or press Enter to skip a day")
    print("-"*70 + "\n")
    
    shift_map = {"1": "Morning", "2": "Afternoon", "3": "Evening"}
    
    for employee in scheduler.employees:
        print(f"\nPreferences for {employee}:")
        for day in scheduler.DAYS:
            pref_input = input(f"  {day} (1/2/3 or Enter to skip): ").strip()
            if pref_input:
                shift_nums = pref_input.split()
                shifts = [shift_map[num] for num in shift_nums if num in shift_map]
                if shifts:
                    scheduler.add_preference(employee, day, shifts)
    
    scheduler.assign_shifts()
    scheduler.resolve_conflicts()
    scheduler.display_schedule()
    scheduler.get_statistics()


def run_from_file(filename: str = None):
    print("\n" + "="*70)
    print("EMPLOYEE SCHEDULING SYSTEM - FILE IMPORT MODE")
    print("="*70 + "\n")
    
    scheduler = EmployeeScheduler()
    
    if not filename:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(os.path.dirname(script_dir), "sample_data.csv")
        print(f"Using default file: {filename}")
    
    if not load_from_file(scheduler, filename):
        print("\nFailed to load data from file. Exiting...")
        return
    
    if not scheduler.employees:
        print("\nNo employees loaded. Exiting...")
        return
    
    scheduler.assign_shifts()
    scheduler.resolve_conflicts()
    scheduler.display_schedule()
    scheduler.get_statistics()
