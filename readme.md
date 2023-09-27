# English-Chinese Word Definitions Web Scraper
This Python script uses Selenium WebDriver and BeautifulSoup to extract English word definitions and examples along with their Chinese translations from https://www.iciba.com/. The script incorporates multithreading to handle multiple words at the same time.
## Project Description
The script fetches a list of words, navigates to their respective pages on iciba.com, and scrapes the Collins definitions and examples for each word. The results are saved to an "output.txt" file.
## Getting Started
### Prerequisites
- Python 3.11.4
- BeautifulSoup4
- Selenium
- ChromeDriver (compatible with your Chrome version)
### Installation
1. Install Python 3.11.4 from the [official site](https://www.python.org/downloads/release/python-3114/).
2. Install the necessary Python packages using pip:
   
   ```
   pip install -r requirements.txt
   ```
   
   The `requirements.txt` file should contain:
   ```
   beautifulsoup4==4.12.2
   selenium==4.13.0
   ```
3. Download ChromeDriver from the [official site](https://sites.google.com/chromium.org/driver/) and add its location to your system's PATH.
### Usage
Update the `words_to_search` variable in the script with the words you want to search. Adjust the `thread_count` variable to change the number of concurrent threads. Run the script using the command:
```
python <script_name.py>
```
Replace `<script_name.py>` with the actual name of your script.
## Author
Ghost-owner