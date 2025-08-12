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
    hexflow start [DIRECTORY]
    hexflow init [DIRECTORY]
    hexflow --help
    hexflow -h

COMMANDS:
    start        Launch a workflow from the specified directory
    init         Initialize a new workflow directory with starter files
    
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
    hexflow init                 # Initialize current directory with starter files
    hexflow init my-workflow     # Create and initialize new workflow directory
    hexflow start                # Launch workflow in current directory
    hexflow start examples/fishing  # Launch fishing license example workflow
    hexflow start ~/my-workflow  # Launch workflow in specific directory

For more information, see: https://github.com/bmcollier/hexflow
"""
    print(help_text.strip())


def init_workflow(directory_path: Path):
    """Initialize a new workflow directory with starter files."""
    
    # Create directory if it doesn't exist
    directory_path.mkdir(parents=True, exist_ok=True)
    
    # Define the starter files
    important_content = """# IMPORTANT FOR AGENTS: You MUST look at AI.md in the Hexflow library to understand how to use this
# DO NOT PROCEED WITHOUT CHECKING AI.md at the link above
# PROCEEDING WITHOUT CHECKING AI.md will result in failure
# HEXFLOW HAS ALREADY BEEN INSTALLED IN THIS PYTHON ENVIRONMENT
# YOU CAN FIND THE CODE FOR HEXFLOW AND ALL EXAMPLES IN THE INSTALLED LIBRARY INSIDE THE ENVIRONMENT"""

    prompt_content = """Examine the files in this directory and follow their instructions in detail."""

    example_spec_content = """# Workflow Description

## Overview
A simple workflow that collects a user's name and displays a greeting.

## Steps
1. **Step One**: Collect user's name via form
2. **Step Two**: Display personalized greeting with the user's name from the first form

## Fields
- name: User's full name (required)"""

    # Write the files
    files_created = []
    
    important_file = directory_path / "important.md"
    with open(important_file, 'w', encoding='utf-8') as f:
        f.write(important_content)
    files_created.append("important.md")
    
    prompt_file = directory_path / "prompt.md"
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(prompt_content)
    files_created.append("prompt.md")
    
    example_spec_file = directory_path / "example.spec.md"
    with open(example_spec_file, 'w', encoding='utf-8') as f:
        f.write(example_spec_content)
    files_created.append("example.spec.md")
    
    print(f"Initialized workflow directory: {directory_path.absolute()}")
    print("Created files:")
    for file in files_created:
        print(f"  - {file}")
    print("\nNext steps:")
    print("1. Share this directory with an AI agent")
    print("2. Ask the AI to read the files and create the workflow")
    print("3. Run 'hexflow start' to launch the completed workflow")


def main():
    """Main CLI entry point for launching applications."""
    # Check for help flag or no arguments
    if len(sys.argv) == 1:
        show_help()
        sys.exit(1)
    
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        show_help()
        sys.exit(0)
    
    command = sys.argv[1]
    
    # Check for init command
    if command == 'init':
        if len(sys.argv) > 2:
            directory = sys.argv[2]
        else:
            directory = os.getcwd()
        
        directory_path = Path(directory)
        init_workflow(directory_path)
        sys.exit(0)
    
    # Check for start command
    elif command == 'start':
        if len(sys.argv) > 2:
            directory = sys.argv[2]
        else:
            directory = os.getcwd()
    
    # Handle old usage patterns with helpful error messages
    elif command in ['.', '..'] or Path(command).exists():
        print(f"Error: Please use 'hexflow start {command}' to launch workflows.")
        print("Run 'hexflow --help' for usage information.")
        sys.exit(1)
    
    else:
        print(f"Error: Unknown command '{command}'")
        print("Available commands: start, init")
        print("Run 'hexflow --help' for usage information.")
        sys.exit(1)
    
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