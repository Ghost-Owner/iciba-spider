# English-Chinese Word Definitions Web Scraper

This Python script now has two versions - spider_playwright.py and spider_selenium.py - which use Playwright and
Selenium WebDriver respectively. Both versions use BeautifulSoup to extract English word definitions and examples along
with their Chinese translations from https://www.iciba.com/.

The spider_playwright.py incorporate asyncio to handle multiple words concurrently.
The spider_selenium.py incorporates multithreading to handle multiple words at the same time.

## Project Description

The scripts fetch a list of words, navigate to their respective pages on iciba.com, and scrape the Collins definitions
and examples for each word. The results are saved to an "output.txt" file.

## Getting Started

### Prerequisites

- Python 3.11.4
- BeautifulSoup4
- Selenium
- Playwright
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
   playwright==1.17.1
   ```
3. Download ChromeDriver from the [official site](https://sites.google.com/chromium.org/driver/) and add its location to
   your system's PATH.
4. Install Playwright browsers with the command:
   ```
   python -m playwright install
   ```

### Usage

Update the `words_to_search` variable in the script with the words you want to search. Adjust the `thread_count`
variable to change the number of concurrent threads. Run the script using the command:

```
python <script_name.py>
```

Replace <script_name.py> with spider_playwright.py or spider_selenium.py depending on the script you want to use.

## Author

Ghost-Owner