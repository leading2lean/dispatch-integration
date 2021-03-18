# Introduction
The `checklist_answers.py` script downloads checklist answers from L2L's CloudDISPATCH using the API.

# Installation

## 1. Install Python3
1. Download the installation application from the python.org website: https://www.python.org/downloads/
   * Be sure you download Python3, not Python2.
2. Run the installation application to install Python.

## 2. Upgrade Pip
`$ py -m pip install --upgrade pip`

## 3. Install dependencies
`$ py -m pip install -r requirements.txt`

## 4. Enter your URL and API Key
1. Update the `config.json`
2. Enter a value in the `apiurl` setting. Be sure to include the API portion of the URL. e.g. "https://customer.leading2lean.com/api/1.0/",
3. Enter a value in the `apikey` setting. You can get a new API key from your L2L Representative.

# Run the Application

## Windows - Simple
* Double-click the checklist_answers.py file. A new Command Prompt window will open with the application running.

## Windows/macOS/Linux - From the Terminal/Command Prompt
1. Open up a new Terminal/Command Prompt
2. Type in the following
  * `py C:\path\to\checklist_answers.py`
  * make sure to enter the correct path to the `checklist_answers.py` file

# Other options

## Custom Path for the log file and CSV file
Log files and CSV files will automatically get saved in a `log` and `csv` directory next to the `checklist_answers.py` file.

You can save the log files and csv files to a custom directory, if you wish. Just edit the `config.json` file and update the `logdirectory` and `csvdirectory` settings with the full path. e.g. "C:\Checklists\log"

## config.json
You can store the `config.json` file in the same directory as the `checklist_answers.py` file, or in the parent directory. If you are testing the application, you can create a `config-dev.json` file instead and place it anywhere you can place the `config.json` file.