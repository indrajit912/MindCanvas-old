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

## Getting Started

To get started with MindCanvas, follow these steps:

1. Clone the repository from GitHub:

   ```bash
   git clone https://github.com/indrajit912/MindCanvas.git
   ```
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the app
    ```bash
    python3 run.py
    ```

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
