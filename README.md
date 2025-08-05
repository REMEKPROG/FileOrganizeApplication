# Files Organizer Program (FOP)

**FOP** is a Python desktop application that automatically organizes
files into subfolders based on their extensions. It features a simple
**Tkinter** graphical interface for quick and intuitive file management.

## Features

-   Select any folder to organize.
-   Automatically creates subfolders:
    -   `.txt` → `documents`
    -   `.png`, `.jpg`, `.jpeg` → `images`
    -   `.mp3`, `.mp4` → `music`
-   Handles duplicate files:
    -   Delete duplicates or save them with a new name.
-   Logs all operations to `log.log`.
-   Warns users about empty folders and irreversible actions.

## How to Run

### Option 1: Using the `.exe` (no Python required)

Download the ready-to-use executable from the **python-organize/dist** section and
run it directly.

### Option 2: Running the Python script

1.  Clone the repository:

    ``` bash
    git clone https://github.com/REMEKPROG/FileOrganizeApplication/tree/main?tab=readme-ov-file
    ```

2.  Install Python 3.

3.  Run the script:

    ``` bash
    python main.py
    ```

## Requirements (for Python version)

-   Python 3
-   Tkinter (comes preinstalled with most Python distributions)
