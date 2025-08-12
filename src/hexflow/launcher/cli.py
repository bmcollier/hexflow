"""CLI entry point for the launcher."""

import sys
import os
from pathlib import Path
from .app_launcher import AppLauncher


def main():
    """Main CLI entry point for launching applications."""
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