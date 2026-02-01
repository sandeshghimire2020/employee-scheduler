#!/usr/bin/env python3

import http.server
import socketserver
import json
import urllib.parse
from scheduler import EmployeeScheduler

PORT = 8888

class SchedulerHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        try:
            if self.path == '/' or self.path == '/index.html':
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                html_content = self.get_html()
                self.wfile.write(html_content.encode('utf-8'))
            else:
                super().do_GET()
        except Exception as e:
            print(f"Error in do_GET: {e}")
            import traceback
            traceback.print_exc()
    
    def do_POST(self):
        if self.path == '/generate':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            
            import sys
            import io
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
            
            try:
                scheduler = EmployeeScheduler()
                
                for emp_data in data['employees']:
                    name = emp_data['name']
                    scheduler.add_employee(name)
                    
                    for pref in emp_data['preferences']:
                        day = pref['day']
                        shifts = pref['shifts']
                        scheduler.add_preference(name, day, shifts)
                
                scheduler.assign_shifts()
                scheduler.resolve_conflicts()
                
                response = {
                    'schedule': dict(scheduler.schedule),
                    'daysWorked': dict(scheduler.days_worked),
                    'employees': scheduler.employees
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
            finally:
                sys.stdout = old_stdout
    
    def get_html(self):
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Employee Scheduler</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .content {
            padding: 30px;
        }
        
        .employee-section {
            margin-bottom: 30px;
        }
        
        .employee-card {
            background: #f8f9fa;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            border: 2px solid #e9ecef;
        }
        
        .employee-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .employee-name {
            font-size: 1.3em;
            font-weight: bold;
            color: #667eea;
        }
        
        .remove-btn {
            background: #dc3545;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9em;
        }
        
        .remove-btn:hover {
            background: #c82333;
        }
        
        .day-prefs {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }
        
        .day-pref {
            background: white;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid #dee2e6;
        }
        
        .day-name {
            font-weight: bold;
            color: #495057;
            margin-bottom: 8px;
        }
        
        .shifts {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }
        
        .shift-checkbox {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .shift-checkbox input {
            width: 18px;
            height: 18px;
            cursor: pointer;
        }
        
        .shift-checkbox label {
            cursor: pointer;
            font-size: 0.95em;
        }
        
        .btn-group {
            display: flex;
            gap: 15px;
            margin: 20px 0;
        }
        
        .btn {
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .btn-primary {
            background: #667eea;
            color: white;
        }
        
        .btn-primary:hover {
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .btn-secondary {
            background: #6c757d;
            color: white;
        }
        
        .btn-secondary:hover {
            background: #5a6268;
        }
        
        .btn-success {
            background: #28a745;
            color: white;
        }
        
        .btn-success:hover {
            background: #218838;
        }
        
        .add-employee {
            margin-bottom: 20px;
        }
        
        .add-employee input {
            padding: 10px 15px;
            border: 2px solid #dee2e6;
            border-radius: 6px;
            font-size: 1em;
            width: 300px;
            margin-right: 10px;
        }
        
        .add-employee input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .schedule-output {
            background: #f8f9fa;
            border-radius: 12px;
            padding: 25px;
            margin-top: 30px;
            display: none;
        }
        
        .schedule-output.show {
            display: block;
        }
        
        .schedule-day {
            background: white;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        
        .schedule-day h3 {
            color: #667eea;
            margin-bottom: 15px;
        }
        
        .schedule-shift {
            margin-bottom: 12px;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 6px;
        }
        
        .shift-title {
            font-weight: bold;
            color: #495057;
            margin-bottom: 5px;
        }
        
        .shift-employees {
            color: #6c757d;
            padding-left: 15px;
        }
        
        .summary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }
        
        .summary h3 {
            margin-bottom: 15px;
        }
        
        .summary-item {
            padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.2);
        }
        
        .summary-item:last-child {
            border-bottom: none;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            display: none;
        }
        
        .loading.show {
            display: block;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1> Employee Scheduler</h1>
            <p>Interactive Web Interface for Shift Management</p>
        </div>
        
        <div class="content">
            <div class="add-employee">
                <input type="text" id="employeeName" placeholder="Enter employee name" />
                <button class="btn btn-success" onclick="addEmployee()"> Add Employee</button>
            </div>
            
            <div class="btn-group">
                <button class="btn btn-primary" onclick="generateSchedule()"> Generate Schedule</button>
                <button class="btn btn-secondary" onclick="clearAll()">🗑️ Clear All</button>
            </div>
            
            <div class="employee-section" id="employeeList">
                <p style="color: #6c757d; font-style: italic;">Add employees to get started...</p>
            </div>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p style="margin-top: 20px; color: #6c757d;">Generating schedule...</p>
            </div>
            
            <div class="schedule-output" id="scheduleOutput"></div>
        </div>
    </div>
    
    <script>
        const DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
        const SHIFTS = ['Morning', 'Afternoon', 'Evening'];
        let employees = [];
        
        function addEmployee() {
            const nameInput = document.getElementById('employeeName');
            const name = nameInput.value.trim();
            
            if (!name) {
                alert('Please enter an employee name');
                return;
            }
            
            if (employees.some(e => e.name === name)) {
                alert('Employee already exists');
                return;
            }
            
            employees.push({
                name: name,
                preferences: []
            });
            
            nameInput.value = '';
            renderEmployees();
        }
        
        function removeEmployee(index) {
            employees.splice(index, 1);
            renderEmployees();
        }
        
        function renderEmployees() {
            const list = document.getElementById('employeeList');
            
            if (employees.length === 0) {
                list.innerHTML = '<p style="color: #6c757d; font-style: italic;">Add employees to get started...</p>';
                return;
            }
            
            list.innerHTML = employees.map((emp, idx) => `
                <div class="employee-card">
                    <div class="employee-header">
                        <div class="employee-name">${emp.name}</div>
                        <button class="remove-btn" onclick="removeEmployee(${idx})">Remove</button>
                    </div>
                    <div class="day-prefs">
                        ${DAYS.map(day => `
                            <div class="day-pref">
                                <div class="day-name">${day}</div>
                                <div class="shifts">
                                    ${SHIFTS.map(shift => `
                                        <div class="shift-checkbox">
                                            <input type="checkbox" 
                                                   id="emp${idx}_${day}_${shift}"
                                                   onchange="updatePreference(${idx}, '${day}', '${shift}', this.checked)">
                                            <label for="emp${idx}_${day}_${shift}">${shift}</label>
                                        </div>
                                    `).join('')}
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `).join('');
        }
        
        function updatePreference(empIdx, day, shift, checked) {
            const emp = employees[empIdx];
            let dayPref = emp.preferences.find(p => p.day === day);
            
            if (!dayPref) {
                dayPref = { day: day, shifts: [] };
                emp.preferences.push(dayPref);
            }
            
            if (checked) {
                if (!dayPref.shifts.includes(shift)) {
                    dayPref.shifts.push(shift);
                }
            } else {
                dayPref.shifts = dayPref.shifts.filter(s => s !== shift);
            }
            
            emp.preferences = emp.preferences.filter(p => p.shifts.length > 0);
        }
        
        async function generateSchedule() {
            if (employees.length === 0) {
                alert('Please add at least one employee');
                return;
            }
            
            document.getElementById('loading').classList.add('show');
            document.getElementById('scheduleOutput').classList.remove('show');
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ employees: employees })
                });
                
                const data = await response.json();
                displaySchedule(data);
            } catch (error) {
                alert('Error generating schedule: ' + error);
            } finally {
                document.getElementById('loading').classList.remove('show');
            }
        }
        
        function displaySchedule(data) {
            const output = document.getElementById('scheduleOutput');
            
            let html = '<h2 style="color: #667eea; margin-bottom: 20px;"> Weekly Schedule</h2>';
            
            DAYS.forEach(day => {
                html += `<div class="schedule-day">
                    <h3>${day}</h3>`;
                
                SHIFTS.forEach(shift => {
                    const emps = data.schedule[day][shift];
                    const empList = emps.length > 0 ? emps.join(', ') : '<em>No one assigned</em>';
                    const status = emps.length >= 2 ? '✓' : '⚠️';
                    
                    html += `<div class="schedule-shift">
                        <div class="shift-title">${status} ${shift} (${emps.length} employees)</div>
                        <div class="shift-employees">${empList}</div>
                    </div>`;
                });
                
                html += '</div>';
            });
            
            html += '<div class="summary"><h3> Summary</h3>';
            data.employees.forEach(emp => {
                const days = data.daysWorked[emp];
                const status = days <= 5 ? '✓' : '⚠️';
                html += `<div class="summary-item">${status} ${emp}: ${days} days</div>`;
            });
            html += '</div>';
            
            output.innerHTML = html;
            output.classList.add('show');
            output.scrollIntoView({ behavior: 'smooth' });
        }
        
        function clearAll() {
            if (employees.length === 0 || confirm('Clear all employees and data?')) {
                employees = [];
                renderEmployees();
                document.getElementById('scheduleOutput').classList.remove('show');
            }
        }
    </script>
</body>
</html>
"""

def main():
    with socketserver.TCPServer(("", PORT), SchedulerHandler) as httpd:
        print("=" * 70)
        print("Employee Scheduler Web UI")
        print("=" * 70)
        print(f"\n Server running at: http://localhost:{PORT}")
        print("\n Instructions:")
        print("  1. Open the URL above in your web browser")
        print("  2. Add employees and set their preferences")
        print("  3. Click 'Generate Schedule' to create the schedule")
        print("\n  Press Ctrl+C to stop the server\n")
        print("=" * 70 + "\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n Server stopped")

if __name__ == "__main__":
    main()
