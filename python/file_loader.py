import csv
import os
from scheduler import EmployeeScheduler


def load_from_file(scheduler: EmployeeScheduler, filename: str) -> bool:
    print(f"\nLoading data from {filename}...")
    
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return False
    
    try:
        with open(filename, 'r') as file:
            csv_reader = csv.reader(file)
            
            employees_added = set()
            preferences_count = 0
            
            for line_num, row in enumerate(csv_reader, 1):
                if not row or not any(row):
                    continue
                
                if row[0].strip().startswith('#'):
                    continue
                
                if len(row) < 3:
                    print(f"Warning: Line {line_num} has insufficient data, skipping")
                    continue
                
                employee = row[0].strip()
                day = row[1].strip()
                shifts = [s.strip() for s in row[2:] if s.strip()]
                
                if day not in scheduler.DAYS:
                    print(f"Warning: Line {line_num} has invalid day '{day}', skipping")
                    continue
                
                valid_shifts = [s for s in shifts if s in scheduler.SHIFTS]
                if not valid_shifts:
                    print(f"Warning: Line {line_num} has no valid shifts, skipping")
                    continue
                
                if employee not in employees_added:
                    scheduler.add_employee(employee)
                    employees_added.add(employee)
                
                scheduler.preferences[employee][day] = valid_shifts
                preferences_count += 1
                print(f"  Loaded: {employee} - {day}: {', '.join(valid_shifts)}")
            
            print(f"\n✓ Successfully loaded {len(employees_added)} employees with {preferences_count} preferences")
            return True
            
    except Exception as e:
        print(f"Error reading file: {e}")
        return False
