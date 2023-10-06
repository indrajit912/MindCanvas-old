# MindCanvas - A Journaling Flask Web App

MindCanvas is a simple web application built using Flask that allows you to journal your thoughts, ideas, and experiences. You can create, view, update, and delete journal entries through an easy-to-use web interface.

- Website: [Demo on Render!](https://demo-mindcanvas.onrender.com)
- Default username: `admin`
- Default password: `password`

![Homepage Screenshot](/app/static/images/homepage.png)
![ViewEntries Screenshot](/app/static/images/view_entries.png)

## Author

- **Indrajit Ghosh**
- **Email:** rs_math1902@isibang.ac.in

## Features

- **Create Entries**: Write and save your journal entries with titles, timestamps, and text content.
- **View Entries**: Browse through your previous journal entries with the ability to read, search, and filter.
- **Update Entries**: Edit and update your existing entries to reflect changes or add more details.
- **Delete Entries**: Remove entries you no longer need.
- **Download Data**: You have the option to retrieve the `json` file containing all the data stored on the server.
- **Data Security and Password Management**: All your data is securely encrypted with a password. The default credentials are username=admin and password=password. You have the flexibility to change the password at any time, but it is crucial to ensure you do not lose it. Without this password, you will be unable to access your data. This measure is in place to safeguard your data privacy. 

## Installation and Setup Guide

To get started with MindCanvas, follow these steps to download and run the provided installation script for your operating system. Make sure you have Python 3 and Git installed.

### Installation on Linux/macOS

1. Download the installation script for Linux/macOS by clicking [here](https://minhaskamal.github.io/DownGit/#/home?url=https://github.com/indrajit912/MindCanvas/blob/master/scripts/install.sh).

2. Open your terminal.

3. Navigate to the directory where you downloaded the script.

4. Make the script executable with the following command:

   ```bash
   chmod +x install.sh
   ```
5. Run the script to install the app and its dependencies:
    ```bash
    ./install.sh
    ```
6. Installation is successful! To run the app, use the following command:
    ```bash
    python3 run.py
    ```

## Installation on Windows
1. Download the installation script for Windows by clicking [here](https://minhaskamal.github.io/DownGit/#/home?url=https://github.com/indrajit912/MindCanvas/blob/master/scripts/install.bat).

2. Open your Command Prompt.

3. Navigate to the directory where you downloaded the script.

4. Run the script to install the app and its dependencies:
    ```bash
    install.bat
    ```
5. Installation is successful! To run the app, use the following command:
    ```bash
    python run.py
    ```
That's it! You've successfully installed MindCanvas. Open your web browser and access the app at http://localhost:8080 to start using it.
 
For more information and usage instructions, please refer to the README.md file in the project root.

Enjoy using MindCanvas!


## Usage

- **Home Page**: Visit the home page to start your journaling journey.

- **View Entries**: Click on "View Entries" to see your existing journal entries.

- **Add New Entry**: Use the "Add New Entry" button to create a new journal entry.

- **Update Entry**: Click "Update" on an entry card to edit and update it.

- **Delete Entry**: Use the "Delete" button to remove an entry.


## Contributing

If you'd like to contribute to MindCanvas, feel free to open a pull request or submit issues on the [GitHub repository](https://github.com/indrajit912/MindCanvas). Your contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
