# Employee Scheduler

The application is a multi-language employee scheduling system that showcases control structures, data structures, and various programming paradigms in both Java and Python. It manages employee schedules for a 7-day week, covering morning, afternoon, and evening shifts. The system enforces scheduling constraints, resolves conflicts, and optimizes shift assignments according to employee preferences.

## Features

- **Shift Management**: 3 shifts/day (Morning, Afternoon, Evening) across 7 days
- **Constraint Enforcement**: 
  - Maximum 5 working days per employee per week
  - Minimum 2 employees per shift
  - No employee works multiple shifts on the same day
- **Conflict Resolution**: Automatically detects and resolves scheduling conflicts
- **Priority-based Preferences**: Employees can specify preferred shifts with priority ordering
- **Interactive Web UI**: Python includes a modern HTML/CSS web interface


## Running the Applications

### Java

```bash
cd java
./compile.sh    
./run.sh       
```

### Python

```bash
cd python
python3 main.py
```

**For UI:**
```bash
cd python
python3 main.py interactive
# Opens web server at http://localhost:8888
```



## Control Structures Demonstrated

### Java
- **Conditionals**: if/else, switch statements
- **Loops**: for, enhanced for, while
- **Nested structures**: nested loops and conditionals
- **Collections**: ArrayList, HashMap, HashSet
- **Exception handling**: try-catch blocks

### Python
- **Conditionals**: if/elif/else
- **Loops**: for, while, list comprehensions
- **Nested structures**: nested iterations
- **Collections**: lists, dictionaries, sets, defaultdict
- **Exception handling**: try/except blocks



## Author

MSCS-632 Advanced Programming Languages Project
