package util;

import java.io.*;
import java.util.*;
import scheduler.Scheduler;

public class FileLoader {
    
    public static boolean loadFromFile(Scheduler scheduler, String filename) {
        System.out.println("\nLoading data from " + filename + "...");
        
        File file = new File(filename);
        if (!file.exists()) {
            System.out.println("Error: File '" + filename + "' not found.");
            return false;
        }
        
        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            Set<String> employeesAdded = new HashSet<>();
            int preferencesCount = 0;
            int lineNum = 0;
            String line;
            
            while ((line = reader.readLine()) != null) {
                lineNum++;
                
                if (line.trim().isEmpty()) continue;
                if (line.trim().startsWith("#")) continue;
                
                String[] parts = line.split(",");
                
                if (parts.length < 3) {
                    System.out.println("Warning: Line " + lineNum + " has insufficient data, skipping");
                    continue;
                }
                
                String employee = parts[0].trim();
                String day = parts[1].trim();
                
                List<String> shifts = new ArrayList<>();
                for (int i = 2; i < parts.length; i++) {
                    String shift = parts[i].trim();
                    if (!shift.isEmpty()) {
                        shifts.add(shift);
                    }
                }
                
                if (!Arrays.asList(Scheduler.DAYS).contains(day)) {
                    System.out.println("Warning: Line " + lineNum + " has invalid day '" + day + "', skipping");
                    continue;
                }
                
                List<String> validShifts = new ArrayList<>();
                for (String shift : shifts) {
                    if (Arrays.asList(Scheduler.SHIFTS).contains(shift)) {
                        validShifts.add(shift);
                    }
                }
                
                if (validShifts.isEmpty()) {
                    System.out.println("Warning: Line " + lineNum + " has no valid shifts, skipping");
                    continue;
                }
                
                if (!employeesAdded.contains(employee)) {
                    scheduler.addEmployee(employee);
                    employeesAdded.add(employee);
                }
                
                scheduler.preferences.get(employee).put(day, validShifts);
                preferencesCount++;
                System.out.println("  Loaded: " + employee + " - " + day + ": " + 
                                 String.join(", ", validShifts));
            }
            
            System.out.println("\n✓ Successfully loaded " + employeesAdded.size() + 
                             " employees with " + preferencesCount + " preferences");
            return true;
            
        } catch (IOException e) {
            System.out.println("Error reading file: " + e.getMessage());
            return false;
        }
    }
}
