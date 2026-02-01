#!/usr/bin/env python3

import sys
import subprocess
import os
from run_modes import run_demo


def print_usage():
    print("\nEmployee Scheduling System")
    print("\nUsage:")
    print("  python3 main.py [mode]")
    print("\nModes:")
    print("  demo          - Run with sample data (default)")
    print("  interactive   - Launch web UI on http://localhost:8080")
    print("\nExamples:")
    print("  python3 main.py              # Runs demo")
    print("  python3 main.py demo         # Runs demo")
    print("  python3 main.py interactive  # Web UI")
    print()


def main():
    
    if len(sys.argv) == 1:
        run_demo()
    else:
        mode = sys.argv[1].lower()
        
        if mode in ['help', '-h', '--help']:
            print_usage()
        elif mode == 'demo':
            run_demo()
        elif mode == 'interactive':
            script_dir = os.path.dirname(os.path.abspath(__file__))
            web_ui_path = os.path.join(script_dir, "web_ui.py")
            subprocess.run([sys.executable, web_ui_path])
        else:
            print(f"Unknown mode: {mode}")
            print_usage()


if __name__ == "__main__":
    main()
