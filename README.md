# Project Title

Automated Notepad File Management Script

## Description

This Python script automates the creation, handling, and content insertion of text files using a combination of Python's `asyncio` for asynchronous execution and automation tools like `pyautogui`. The script achieves the following key tasks:

- Creates a specified number of text files in a user-defined directory.
- Opens these files in Notepad.
- Fills each text file with data fetched from a web API (https://jsonplaceholder.typicode.com).
- Automates file management tasks such as opening directories, locating icons, and interacting with Notepad windows.

The script uses asynchronous methods for a more efficient workflow, making it suitable for automating large repetitive tasks with minimal human intervention.

## Features

- **Directory Creation**: Creates a directory on the desktop to store generated text files.
- **Asynchronous API Requests**: Retrieves data from an API endpoint asynchronously.
- **Automated GUI Interaction**: Uses `pyautogui` to locate and interact with Notepad files.
- **Queue Management**: Uses `asyncio.Queue` to manage the flow of tasks such as adding files and posts.

## Prerequisites

To run this script, you'll need:

- **Python 3.7+**: The script utilizes `asyncio` and `httpx`, which work best with newer Python versions.
- **Required Packages**: Install the following packages using `pip`:
  
  ```sh
  pip install httpx aiofiles aioconsole pyautogui
  ```

- **Notepad Icon Image**: Ensure you have an image of the Notepad icon (`notepad_icon.png`) in the script's directory for locating the icons on the desktop.

## Installation

1. **Clone the Repository**:
   
   ```sh
   git clone <repository-url>
   ```

2. **Navigate to the Project Directory**:

   ```sh
   cd <project-directory>
   ```

3. **Install Dependencies**:

   ```sh
   pip install -r requirements.txt
   ```

## Usage

To run the script:

```sh
python script.py
```

- **Enter the number of files**: The script will prompt you to enter how many text files you want to create.
- **Enter the directory name**: Provide a directory name where the text files will be created (it will be located on your desktop).

### Main Functionalities:

1. **Directory & File Creation**: The script will create a specified number of text files in the specified directory on your desktop.
2. **Data Fetching**: The script will fetch data from a placeholder API to populate each text file.
3. **Automated Interaction**: The script will open each file, write the fetched data, save it, and close it automatically.

## Code Overview

- **create_directory**: Creates a directory on the desktop.
- **fetch_json_from_url**: Retrieves JSON data from a given URL.
- **open_directory_in_explorer**: Opens the specified directory in the system's file explorer.
- **create_text_files**: Creates empty text files.
- **add_post_to_queue**: Adds fetched data from API to a queue.
- **locate_icon_positions**: Uses `pyautogui` to locate the position of text files on the desktop.
- **handle_notepad_interaction**: Opens Notepad files and writes content fetched from the API.

## Known Issues & Limitations

- **Icon Detection**: If the desktop icons are in a non-standard view or too crowded, the icon location detection may not work correctly.
- **Failsafe Mechanism**: `pyautogui` has a failsafe mechanism (move the mouse to the top-left corner to stop the script). Make sure to keep this in mind while testing.
- **Windows OS**: The script is designed to work with Notepad on Windows. It may require modifications for other platforms.

## Contributing

If you'd like to contribute:

1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request with a description of your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Author

- **Your Name**: Provide your contact information here.

## Acknowledgments

- Placeholder API used: [JSONPlaceholder](https://jsonplaceholder.typicode.com/).
- Thanks to [PyAutoGUI](https://pyautogui.readthedocs.io/) for simplifying GUI automation in Python.

