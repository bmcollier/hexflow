"""CLI entry point for the launcher."""

import sys
import os
from pathlib import Path
from .app_launcher import AppLauncher


def show_help():
    """Display help information."""
    help_text = """
Hexflow - AI-aware modular application framework

USAGE:
    hexflow [DIRECTORY]
    hexflow --help
    hexflow -h

ARGUMENTS:
    DIRECTORY    Path to workflow directory (default: current directory)

OPTIONS:
    -h, --help   Show this help message and exit

DESCRIPTION:
    Hexflow launches orchestrated workflows from a directory containing:
    - A .dag file defining the workflow structure
    - Application directories with app.py files
    
    The launcher will:
    1. Discover all applications in the directory
    2. Start each application on its assigned port
    3. Launch the router to orchestrate the workflow
    4. Provide a single entry point at http://localhost:8000/start

EXAMPLES:
    hexflow .                    # Launch workflow in current directory
    hexflow examples/government  # Launch government example workflow
    hexflow ~/my-workflow        # Launch workflow in specific directory

For more information, see: https://github.com/bmcollier/hexflow
"""
    print(help_text.strip())


def main():
    """Main CLI entry point for launching applications."""
    # Check for help flag
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        show_help()
        sys.exit(0)
    
    # Use current directory by default, or accept directory as argument
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = os.getcwd()
    
    directory_path = Path(directory)
    
    if not directory_path.exists():
        print(f"Error: Directory {directory} does not exist")
        sys.exit(1)
    
    if not directory_path.is_dir():
        print(f"Error: {directory} is not a directory")
        sys.exit(1)
    
    print(f"Launching applications from: {directory_path.absolute()}")
    
    launcher = AppLauncher(str(directory_path))
    
    try:
        running_apps = launcher.launch_all_apps()
        
        if not running_apps:
            print("No applications were launched")
            sys.exit(1)
        
        print("Press Ctrl+C to stop all applications")
        
        # Keep the main thread alive
        while True:
            import time
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping all applications...")
        launcher.stop_all_apps()
        print("All applications stopped")
    except Exception as e:
        print(f"Error: {e}")
        launcher.stop_all_apps()
        sys.exit(1)


if __name__ == "__main__":
    main()