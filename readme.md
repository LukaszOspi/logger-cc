
# Decision Logger Application

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Dependencies](#dependencies)
- [Running the Application](#running-the-application)
- [Creating an Executable](#creating-an-executable)
- [Application Structure](#application-structure)
- [Troubleshooting and Support](#troubleshooting-and-support)

## Overview
The Decision Logger Application is a Python-based tool designed for recording, updating, and managing various decisions. It's built with SQLite for data management and Tkinter for the graphical user interface, offering a responsive and user-friendly experience.

## Features
- **Logging Decisions**: Record decisions with comprehensive details.
- **Updating Decisions**: Modify existing records as needed.
- **Deleting Decisions**: Remove decisions from the log.
- **Filtering and Searching**: Find decisions based on status, date, or keywords.
- **Threaded Operations**: Ensures responsiveness by running database operations in separate threads.
- **Calendar Integration**: Facilitates easy date selection.

## Dependencies
Required libraries and frameworks:
- Python 3.x
- SQLite3
- Tkinter
- tkmacosx (for macOS)
- Tkcalendar
- PIL (Python Imaging Library)

Use pip to install the necessary Python packages:
```bash
pip install tkmacosx tkcalendar Pillow
```

## Running the Application
Execute the application by running the main Python script:
```bash
python decision_logger.py
```

## Creating an Executable
Generate an executable file using PyInstaller:
1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Create the executable:
   ```bash
   pyinstaller --onefile --windowed decision_logger.py
   ```
   Find the executable in the `dist` directory.

3. Distribute the standalone executable across platforms.

## Application Structure
- **Database Management**: Uses SQLite for storing and retrieving decision records.
- **Graphical User Interface**: Built with Tkinter for easy interaction with the data.
- **Multi-threading**: Database operations are handled in separate threads to maintain UI responsiveness.

## Troubleshooting and Support
For assistance or issue resolution, refer to Python and Tkinter documentation, or contact the project maintainers.

## Authors
Brandon
Lukasz Osipiak