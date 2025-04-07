import os
import subprocess

# Get the current working directory (where the master file is)
base_dir = os.getcwd()

# Find all subdirectories that start with "Step "
subfolders = [f for f in os.listdir(base_dir)
              if os.path.isdir(os.path.join(base_dir, f)) and f.startswith("part")]

# Optionally, sort the subfolders to run them in order
subfolders.sort()

# Loop over each subfolder
for folder in subfolders:
    folder_path = os.path.join(base_dir, folder)
    # Look for .py files in the subfolder
    py_files = [f for f in os.listdir(folder_path) if f.endswith('.py')]
    
    # Loop through each .py file found (assuming one per folder if that's your structure)
    for py_file in py_files:
        file_path = os.path.join(folder_path, py_file)
        print(f"Running {file_path}...")
        # Run the Python file. Adjust "python" to "python3" if needed.
        subprocess.run(["python", file_path])