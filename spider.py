from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading


def get_word_definition(word, semaphore):
    with semaphore:
        url = f"https://www.iciba.com/{word}"
        # Use a headless browser like Chrome in headless mode. It loads much faster without GUI.
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        # Create an output string, printing that string all at once
        output = "{\n"

        try:
            # Wait and click on the Collins tab
            collins_tab = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@class="DicTab_tab__q1zCE"]//li[2]'))
            )
            collins_tab.click()

            # Wait for the Collins content to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="Collins_collins__E16AT"]'))
            )

            # Parse the page source with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            collins_blocks = soup.find_all('div', class_='Collins_collins__E16AT')

            # Add to output string
            output += f"Collins Definitions and Examples for {word}:\n"

            for count, block in enumerate(collins_blocks, 1):
                title = block.find('h5')
                if title:
                    output += f'{count}. {title.text.strip()}\n'
                definition = block.find('p')
                if definition:
                    output += "Definition: " + definition.text.strip() + "\n"

                examples = block.find_all('li')
                for i, example in enumerate(examples, 1):
                    en_example = example.find('span')
                    cn_example = example.find('p')

                    if en_example and cn_example:
                        output += f"Example {i}: {en_example.text.strip()} {cn_example.text.strip()}\n"
        finally:
            driver.quit()

        # Open the file in append mode
        with open("output.txt", "a") as f:
            f.write(output + '}\n' + "\n")


if __name__ == '__main__':
    # input for test, you can change it as you need
    words_to_search = ["sexy", "test", "dream", "how", "example", "with", "team", "why", "beauty"]
    thread_count = 4
    semaphore = threading.Semaphore(thread_count)
    # Create and start a thread for each word
    threads = []
    for word in words_to_search:
        thread = threading.Thread(target=get_word_definition, args=(word, semaphore))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()