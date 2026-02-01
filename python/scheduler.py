import random
from collections import defaultdict
from typing import Dict, List, Set


class EmployeeScheduler:
    
    DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    SHIFTS = ["Morning", "Afternoon", "Evening"]
    MAX_DAYS_PER_WEEK = 5
    MIN_EMPLOYEES_PER_SHIFT = 2
    
    def __init__(self):
        self.employees = []
        self.preferences = defaultdict(lambda: defaultdict(list))
        self.schedule = {day: {shift: [] for shift in self.SHIFTS} for day in self.DAYS}
        self.days_worked = defaultdict(int)
        self.employee_assigned_days = defaultdict(set)
    
    def add_employee(self, name: str):
        if name not in self.employees:
            self.employees.append(name)
            print(f"Added employee: {name}")
        else:
            print(f"Employee {name} already exists.")
    
    def add_preference(self, employee: str, day: str, shifts: List[str]):
        if employee not in self.employees:
            print(f"Error: Employee {employee} not found. Add them first.")
            return
        
        if day not in self.DAYS:
            print(f"Error: Invalid day {day}")
            return
        
        valid_shifts = [s for s in shifts if s in self.SHIFTS]
        if not valid_shifts:
            print(f"Error: No valid shifts provided")
            return
        
        self.preferences[employee][day] = valid_shifts
        print(f"Added preference for {employee} on {day}: {', '.join(valid_shifts)}")
    
    def assign_shifts(self):
        print("\n" + "="*60)
        print("STARTING SHIFT ASSIGNMENT")
        print("="*60)
        
        self.schedule = {day: {shift: [] for shift in self.SHIFTS} for day in self.DAYS}
        self.days_worked = defaultdict(int)
        self.employee_assigned_days = defaultdict(set)
        
        for employee in self.employees:
            for day in self.DAYS:
                if day in self.preferences[employee]:
                    if self.days_worked[employee] >= self.MAX_DAYS_PER_WEEK:
                        continue
                    
                    if day in self.employee_assigned_days[employee]:
                        continue
                    
                    assigned = False
                    for shift in self.preferences[employee][day]:
                        self.schedule[day][shift].append(employee)
                        self.days_worked[employee] += 1
                        self.employee_assigned_days[employee].add(day)
                        print(f"Assigned {employee} to {day} - {shift}")
                        assigned = True
                        break
                    
                    if not assigned:
                        print(f"Could not assign {employee} to {day}")
        
        print("\n" + "-"*60)
        print("FILLING UNDERSTAFFED SHIFTS")
        print("-"*60)
        
        for day in self.DAYS:
            for shift in self.SHIFTS:
                current_count = len(self.schedule[day][shift])
                
                if current_count < self.MIN_EMPLOYEES_PER_SHIFT:
                    needed = self.MIN_EMPLOYEES_PER_SHIFT - current_count
                    print(f"\n{day} - {shift} needs {needed} more employee(s)")
                    
                    available = []
                    for emp in self.employees:
                        if (self.days_worked[emp] < self.MAX_DAYS_PER_WEEK and 
                            day not in self.employee_assigned_days[emp]):
                            available.append(emp)
                    
                    if available:
                        random.shuffle(available)
                        for i in range(min(needed, len(available))):
                            emp = available[i]
                            self.schedule[day][shift].append(emp)
                            self.days_worked[emp] += 1
                            self.employee_assigned_days[emp].add(day)
                            print(f"  Randomly assigned {emp} to {day} - {shift}")
                    else:
                        print(f"  WARNING: No available employees for {day} - {shift}")
        
        print("\n" + "="*60)
        print("SHIFT ASSIGNMENT COMPLETE")
        print("="*60 + "\n")
    
    def resolve_conflicts(self):
        print("\n" + "="*60)
        print("RESOLVING CONFLICTS")
        print("="*60)
        
        conflicts_found = False
        
        for day in self.DAYS:
            employees_today = []
            for shift in self.SHIFTS:
                employees_today.extend(self.schedule[day][shift])
            
            seen = set()
            duplicates = set()
            for emp in employees_today:
                if emp in seen:
                    duplicates.add(emp)
                seen.add(emp)
            
            if duplicates:
                conflicts_found = True
                print(f"CONFLICT on {day}: {', '.join(duplicates)} assigned to multiple shifts")
                
                for emp in duplicates:
                    kept_shift = None
                    for shift in self.SHIFTS:
                        if emp in self.schedule[day][shift]:
                            if kept_shift is None:
                                kept_shift = shift
                                print(f"  Keeping {emp} in {shift}")
                            else:
                                self.schedule[day][shift].remove(emp)
                                self.days_worked[emp] -= 1
                                print(f"  Removed {emp} from {shift}")
        
        if not conflicts_found:
            print("No conflicts detected.")
        
        print("="*60 + "\n")
    
    def display_schedule(self):
        print("\n" + "="*60)
        print("FINAL WEEKLY SCHEDULE")
        print("="*60 + "\n")
        
        for day in self.DAYS:
            print("="*60)
            print(day.upper())
            print("="*60)
            
            for shift in self.SHIFTS:
                employees = self.schedule[day][shift]
                emp_count = len(employees)
                
                if employees:
                    emp_list = ", ".join(employees)
                    status = "✓" if emp_count >= self.MIN_EMPLOYEES_PER_SHIFT else f"⚠ (needs {self.MIN_EMPLOYEES_PER_SHIFT - emp_count} more)"
                    print(f"  {shift:12} ({emp_count} employees) {status}")
                    print(f"               → {emp_list}")
                else:
                    print(f"  {shift:12} (0 employees) ⚠ UNDERSTAFFED")
            
            print()
        
        print("="*60)
        print("EMPLOYEE WORK SUMMARY")
        print("="*60)
        
        for emp in sorted(self.employees):
            days = self.days_worked[emp]
            status = "✓" if days <= self.MAX_DAYS_PER_WEEK else "⚠ OVER LIMIT"
            print(f"  {emp:20} {days} days {status}")
        
        print("="*60 + "\n")
    
    def get_statistics(self):
        print("\n" + "="*60)
        print("SCHEDULING STATISTICS")
        print("="*60)
        
        total_shifts = 0
        filled_shifts = 0
        understaffed_shifts = 0
        
        for day in self.DAYS:
            for shift in self.SHIFTS:
                total_shifts += 1
                emp_count = len(self.schedule[day][shift])
                if emp_count > 0:
                    filled_shifts += 1
                if emp_count < self.MIN_EMPLOYEES_PER_SHIFT:
                    understaffed_shifts += 1
        
        print(f"Total shifts: {total_shifts}")
        print(f"Filled shifts: {filled_shifts}")
        print(f"Understaffed shifts: {understaffed_shifts}")
        print(f"Total employees: {len(self.employees)}")
        
        total_days_assigned = sum(self.days_worked.values())
        avg_days = total_days_assigned / len(self.employees) if self.employees else 0
        print(f"Average days per employee: {avg_days:.2f}")
        
        print("="*60 + "\n")
