package runner;

import scheduler.Scheduler;
import util.FileLoader;
import java.util.*;
import java.io.File;

public class RunModes {
    
    public static void runDemo() {
        System.out.println("\n" + "=".repeat(70));
        System.out.println("EMPLOYEE SCHEDULING SYSTEM - DEMO MODE");
        System.out.println("=".repeat(70) + "\n");
        
        Scheduler scheduler = new Scheduler();
        
        System.out.println("Adding employees...");
        String[] employeeNames = {"Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry"};
        for (String emp : employeeNames) {
            scheduler.addEmployee(emp);
        }
        
        System.out.println("\n" + "-".repeat(70));
        System.out.println("Adding shift preferences...");
        System.out.println("-".repeat(70) + "\n");
        
        scheduler.addPreference("Alice", "Monday", Arrays.asList("Morning", "Afternoon"));
        scheduler.addPreference("Alice", "Wednesday", Arrays.asList("Morning"));
        scheduler.addPreference("Alice", "Friday", Arrays.asList("Afternoon"));
        
        scheduler.addPreference("Bob", "Monday", Arrays.asList("Morning"));
        scheduler.addPreference("Bob", "Tuesday", Arrays.asList("Afternoon"));
        scheduler.addPreference("Bob", "Thursday", Arrays.asList("Evening"));
        scheduler.addPreference("Bob", "Saturday", Arrays.asList("Morning"));
        
        scheduler.addPreference("Charlie", "Tuesday", Arrays.asList("Morning", "Afternoon"));
        scheduler.addPreference("Charlie", "Wednesday", Arrays.asList("Afternoon"));
        scheduler.addPreference("Charlie", "Friday", Arrays.asList("Morning"));
        scheduler.addPreference("Charlie", "Sunday", Arrays.asList("Afternoon"));
        
        scheduler.addPreference("Diana", "Monday", Arrays.asList("Afternoon"));
        scheduler.addPreference("Diana", "Wednesday", Arrays.asList("Evening"));
        scheduler.addPreference("Diana", "Thursday", Arrays.asList("Morning"));
        scheduler.addPreference("Diana", "Saturday", Arrays.asList("Afternoon"));
        
        scheduler.addPreference("Eve", "Tuesday", Arrays.asList("Evening"));
        scheduler.addPreference("Eve", "Thursday", Arrays.asList("Afternoon"));
        scheduler.addPreference("Eve", "Friday", Arrays.asList("Evening"));
        scheduler.addPreference("Eve", "Sunday", Arrays.asList("Morning"));
        
        scheduler.addPreference("Frank", "Monday", Arrays.asList("Evening"));
        scheduler.addPreference("Frank", "Wednesday", Arrays.asList("Morning"));
        scheduler.addPreference("Frank", "Friday", Arrays.asList("Afternoon"));
        scheduler.addPreference("Frank", "Saturday", Arrays.asList("Evening"));
        
        scheduler.addPreference("Grace", "Tuesday", Arrays.asList("Morning"));
        scheduler.addPreference("Grace", "Thursday", Arrays.asList("Morning"));
        scheduler.addPreference("Grace", "Friday", Arrays.asList("Evening"));
        scheduler.addPreference("Grace", "Sunday", Arrays.asList("Afternoon"));
        
        scheduler.addPreference("Henry", "Monday", Arrays.asList("Morning"));
        scheduler.addPreference("Henry", "Wednesday", Arrays.asList("Afternoon"));
        scheduler.addPreference("Henry", "Thursday", Arrays.asList("Evening"));
        scheduler.addPreference("Henry", "Saturday", Arrays.asList("Morning"));
        
        scheduler.assignShifts();
        scheduler.resolveConflicts();
        scheduler.displaySchedule();
        scheduler.getStatistics();
    }
    
    public static void runInteractive() {
        System.out.println("\n" + "=".repeat(70));
        System.out.println("EMPLOYEE SCHEDULING SYSTEM - INTERACTIVE MODE");
        System.out.println("=".repeat(70) + "\n");
        
        Scanner scanner = new Scanner(System.in);
        Scheduler scheduler = new Scheduler();
        
        int numEmployees = 0;
        while (numEmployees <= 0) {
            System.out.print("How many employees do you want to add? ");
            try {
                numEmployees = Integer.parseInt(scanner.nextLine().trim());
                if (numEmployees <= 0) {
                    System.out.println("Please enter a positive number.");
                }
            } catch (NumberFormatException e) {
                System.out.println("Please enter a valid number.");
            }
        }
        
        System.out.println("\nEnter employee names:");
        for (int i = 0; i < numEmployees; i++) {
            String name = "";
            while (name.isEmpty()) {
                System.out.print("  Employee " + (i + 1) + ": ");
                name = scanner.nextLine().trim();
                if (name.isEmpty()) {
                    System.out.println("  Name cannot be empty.");
                }
            }
            scheduler.addEmployee(name);
        }
        
        System.out.println("\n" + "-".repeat(70));
        System.out.println("Add shift preferences for each employee");
        System.out.println("Format: Enter shift numbers separated by spaces (1=Morning, 2=Afternoon, 3=Evening)");
        System.out.println("Or press Enter to skip a day");
        System.out.println("-".repeat(70) + "\n");
        
        Map<String, String> shiftMap = new HashMap<>();
        shiftMap.put("1", "Morning");
        shiftMap.put("2", "Afternoon");
        shiftMap.put("3", "Evening");
        
        for (String employee : scheduler.employees) {
            System.out.println("\nPreferences for " + employee + ":");
            
            for (String day : Scheduler.DAYS) {
                System.out.print("  " + day + " (1/2/3 or Enter to skip): ");
                String prefInput = scanner.nextLine().trim();
                
                if (!prefInput.isEmpty()) {
                    String[] shiftNums = prefInput.split("\\s+");
                    List<String> shifts = new ArrayList<>();
                    
                    for (String num : shiftNums) {
                        if (shiftMap.containsKey(num)) {
                            shifts.add(shiftMap.get(num));
                        }
                    }
                    
                    if (!shifts.isEmpty()) {
                        scheduler.addPreference(employee, day, shifts);
                    }
                }
            }
        }
        
        scheduler.assignShifts();
        scheduler.resolveConflicts();
        scheduler.displaySchedule();
        scheduler.getStatistics();
        
        scanner.close();
    }
    
    public static void runFromFile(String filename) {
        System.out.println("\n" + "=".repeat(70));
        System.out.println("EMPLOYEE SCHEDULING SYSTEM - FILE IMPORT MODE");
        System.out.println("=".repeat(70) + "\n");
        
        Scheduler scheduler = new Scheduler();
        
        if (filename == null) {
            String currentDir = System.getProperty("user.dir");
            File parentDir = new File(currentDir).getParentFile();
            filename = new File(parentDir, "sample_data.csv").getAbsolutePath();
            System.out.println("No file specified. Using default: " + filename + "\n");
        }
        
        if (FileLoader.loadFromFile(scheduler, filename)) {
            if (!scheduler.employees.isEmpty()) {
                scheduler.assignShifts();
                scheduler.resolveConflicts();
                scheduler.displaySchedule();
                scheduler.getStatistics();
            } else {
                System.out.println("\nNo employees loaded.");
            }
        } else {
            System.out.println("\nFailed to load data from file.");
        }
    }
}
