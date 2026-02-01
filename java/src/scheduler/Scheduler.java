package scheduler;

import java.util.*;

public class Scheduler {
    
    public static final String[] DAYS = {
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    };
    public static final String[] SHIFTS = {"Morning", "Afternoon", "Evening"};
    public static final int MAX_DAYS_PER_WEEK = 5;
    public static final int MIN_EMPLOYEES_PER_SHIFT = 2;
    
    public List<String> employees;
    public Map<String, Map<String, List<String>>> preferences;
    private Map<String, Map<String, List<String>>> schedule;
    private Map<String, Integer> daysWorked;
    private Map<String, Set<String>> employeeAssignedDays;
    
    public Scheduler() {
        this.employees = new ArrayList<>();
        this.preferences = new HashMap<>();
        this.schedule = new HashMap<>();
        this.daysWorked = new HashMap<>();
        this.employeeAssignedDays = new HashMap<>();
        
        // Initialize schedule structure
        for (String day : DAYS) {
            Map<String, List<String>> shiftsMap = new HashMap<>();
            for (String shift : SHIFTS) {
                shiftsMap.put(shift, new ArrayList<>());
            }
            schedule.put(day, shiftsMap);
        }
    }
    
    public void addEmployee(String name) {
        if (!employees.contains(name)) {
            employees.add(name);
            preferences.put(name, new HashMap<>());
            daysWorked.put(name, 0);
            employeeAssignedDays.put(name, new HashSet<>());
            System.out.println("Added employee: " + name);
        } else {
            System.out.println("Employee " + name + " already exists.");
        }
    }
    
    public void addPreference(String employee, String day, List<String> shifts) {
        if (!employees.contains(employee)) {
            System.out.println("Error: Employee " + employee + " not found. Add them first.");
            return;
        }
        
        if (!Arrays.asList(DAYS).contains(day)) {
            System.out.println("Error: Invalid day " + day);
            return;
        }
        
        List<String> validShifts = new ArrayList<>();
        for (String shift : shifts) {
            if (Arrays.asList(SHIFTS).contains(shift)) {
                validShifts.add(shift);
            }
        }
        
        if (validShifts.isEmpty()) {
            System.out.println("Error: No valid shifts provided");
            return;
        }
        
        preferences.get(employee).put(day, validShifts);
        System.out.println("Added preference for " + employee + " on " + day + ": " + 
                         String.join(", ", validShifts));
    }
    
    public void assignShifts() {
        System.out.println("\n" + "=".repeat(60));
        System.out.println("STARTING SHIFT ASSIGNMENT");
        System.out.println("=".repeat(60));
        
        // Reset schedule
        for (String day : DAYS) {
            for (String shift : SHIFTS) {
                schedule.get(day).get(shift).clear();
            }
        }
        
        for (String emp : employees) {
            daysWorked.put(emp, 0);
            employeeAssignedDays.put(emp, new HashSet<>());
        }
        
        // Phase 1: Assign based on preferences
        for (String employee : employees) {
            Map<String, List<String>> empPrefs = preferences.get(employee);
            
            for (String day : DAYS) {
                if (!empPrefs.containsKey(day)) continue;
                if (daysWorked.get(employee) >= MAX_DAYS_PER_WEEK) continue;
                if (employeeAssignedDays.get(employee).contains(day)) continue;
                
                boolean assigned = false;
                for (String shift : empPrefs.get(day)) {
                    schedule.get(day).get(shift).add(employee);
                    daysWorked.put(employee, daysWorked.get(employee) + 1);
                    employeeAssignedDays.get(employee).add(day);
                    System.out.println("Assigned " + employee + " to " + day + " - " + shift);
                    assigned = true;
                    break;
                }
                
                if (!assigned) {
                    System.out.println("Could not assign " + employee + " to " + day);
                }
            }
        }
        
        System.out.println("\n" + "-".repeat(60));
        System.out.println("FILLING UNDERSTAFFED SHIFTS");
        System.out.println("-".repeat(60));
        
        Random random = new Random();
        
        for (String day : DAYS) {
            for (String shift : SHIFTS) {
                int currentCount = schedule.get(day).get(shift).size();
                
                if (currentCount < MIN_EMPLOYEES_PER_SHIFT) {
                    int needed = MIN_EMPLOYEES_PER_SHIFT - currentCount;
                    System.out.println("\n" + day + " - " + shift + " needs " + needed + " more employee(s)");
                    
                    List<String> available = new ArrayList<>();
                    for (String emp : employees) {
                        if (daysWorked.get(emp) < MAX_DAYS_PER_WEEK && 
                            !employeeAssignedDays.get(emp).contains(day)) {
                            available.add(emp);
                        }
                    }
                    
                    if (!available.isEmpty()) {
                        Collections.shuffle(available, random);
                        int toAssign = Math.min(needed, available.size());
                        
                        for (int i = 0; i < toAssign; i++) {
                            String emp = available.get(i);
                            schedule.get(day).get(shift).add(emp);
                            daysWorked.put(emp, daysWorked.get(emp) + 1);
                            employeeAssignedDays.get(emp).add(day);
                            System.out.println("  Randomly assigned " + emp + " to " + day + " - " + shift);
                        }
                    } else {
                        System.out.println("  WARNING: No available employees for " + day + " - " + shift);
                    }
                }
            }
        }
        
        System.out.println("\n" + "=".repeat(60));
        System.out.println("SHIFT ASSIGNMENT COMPLETE");
        System.out.println("=".repeat(60) + "\n");
    }
    
    public void resolveConflicts() {
        System.out.println("\n" + "=".repeat(60));
        System.out.println("RESOLVING CONFLICTS");
        System.out.println("=".repeat(60));
        
        boolean conflictsFound = false;
        
        for (String day : DAYS) {
            List<String> employeesToday = new ArrayList<>();
            
            for (String shift : SHIFTS) {
                employeesToday.addAll(schedule.get(day).get(shift));
            }
            
            Set<String> seen = new HashSet<>();
            Set<String> duplicates = new HashSet<>();
            
            for (String emp : employeesToday) {
                if (seen.contains(emp)) {
                    duplicates.add(emp);
                }
                seen.add(emp);
            }
            
            if (!duplicates.isEmpty()) {
                conflictsFound = true;
                System.out.println("CONFLICT on " + day + ": " + 
                                 String.join(", ", duplicates) + " assigned to multiple shifts");
                
                for (String emp : duplicates) {
                    String keptShift = null;
                    
                    for (String shift : SHIFTS) {
                        List<String> shiftEmployees = schedule.get(day).get(shift);
                        
                        if (shiftEmployees.contains(emp)) {
                            if (keptShift == null) {
                                keptShift = shift;
                                System.out.println("  Keeping " + emp + " in " + shift);
                            } else {
                                shiftEmployees.remove(emp);
                                daysWorked.put(emp, daysWorked.get(emp) - 1);
                                System.out.println("  Removed " + emp + " from " + shift);
                            }
                        }
                    }
                }
            }
        }
        
        if (!conflictsFound) {
            System.out.println("No conflicts detected.");
        }
        
        System.out.println("=".repeat(60) + "\n");
    }
    
    public void displaySchedule() {
        System.out.println("\n" + "=".repeat(60));
        System.out.println("FINAL WEEKLY SCHEDULE");
        System.out.println("=".repeat(60) + "\n");
        
        for (String day : DAYS) {
            System.out.println("=".repeat(60));
            System.out.println(day.toUpperCase());
            System.out.println("=".repeat(60));
            
            for (String shift : SHIFTS) {
                List<String> shiftEmployees = schedule.get(day).get(shift);
                int empCount = shiftEmployees.size();
                
                if (!shiftEmployees.isEmpty()) {
                    String empList = String.join(", ", shiftEmployees);
                    String status = empCount >= MIN_EMPLOYEES_PER_SHIFT ? 
                                  "✓" : "⚠ (needs " + (MIN_EMPLOYEES_PER_SHIFT - empCount) + " more)";
                    
                    System.out.printf("  %-12s (%d employees) %s%n", shift, empCount, status);
                    System.out.println("               → " + empList);
                } else {
                    System.out.printf("  %-12s (0 employees) ⚠ UNDERSTAFFED%n", shift);
                }
            }
            
            System.out.println();
        }
        
        System.out.println("=".repeat(60));
        System.out.println("EMPLOYEE WORK SUMMARY");
        System.out.println("=".repeat(60));
        
        List<String> sortedEmployees = new ArrayList<>(employees);
        Collections.sort(sortedEmployees);
        
        for (String emp : sortedEmployees) {
            int days = daysWorked.get(emp);
            String status = days <= MAX_DAYS_PER_WEEK ? "✓" : "⚠ OVER LIMIT";
            System.out.printf("  %-20s %d days %s%n", emp, days, status);
        }
        
        System.out.println("=".repeat(60) + "\n");
    }
    
    public void getStatistics() {
        System.out.println("\n" + "=".repeat(60));
        System.out.println("SCHEDULING STATISTICS");
        System.out.println("=".repeat(60));
        
        int totalShifts = 0;
        int filledShifts = 0;
        int understaffedShifts = 0;
        
        for (String day : DAYS) {
            for (String shift : SHIFTS) {
                totalShifts++;
                int empCount = schedule.get(day).get(shift).size();
                
                if (empCount > 0) {
                    filledShifts++;
                }
                if (empCount < MIN_EMPLOYEES_PER_SHIFT) {
                    understaffedShifts++;
                }
            }
        }
        
        System.out.println("Total shifts: " + totalShifts);
        System.out.println("Filled shifts: " + filledShifts);
        System.out.println("Understaffed shifts: " + understaffedShifts);
        System.out.println("Total employees: " + employees.size());
        
        int totalDaysAssigned = 0;
        for (int days : daysWorked.values()) {
            totalDaysAssigned += days;
        }
        
        double avgDays = employees.isEmpty() ? 0.0 : (double) totalDaysAssigned / employees.size();
        System.out.printf("Average days per employee: %.2f%n", avgDays);
        
        System.out.println("=".repeat(60) + "\n");
    }
}
