from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading


def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    return webdriver.Chrome(options=options)


def get_word_definition(word, semaphore):
    with semaphore:
        driver = setup_driver()
        url = f"https://www.iciba.com/{word}"
        driver.get(url)
        output = parse_page(driver, word)
        write_to_file(output)
        driver.quit()


def parse_page(driver, word):
    output = "{\n"
    try:
        collins_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="DicTab_tab__q1zCE"]//li[2]'))
        )
    except TimeoutException:
        print(f"Timeout while waiting for word: {word}, maybe it isn't included in this dictionary")
        output = ""
        return output
    collins_tab.click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="Collins_collins__E16AT"]'))
    )
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    collins_blocks = soup.find_all('div', class_='Collins_collins__E16AT')
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
    return output


def write_to_file(output):
    if output:
        with open("output.txt", "a") as f:
            f.write(output + "}\n\n")


if __name__ == '__main__':
    words_to_search = ["sexy", "test", "dream", "how", "example", "with", "team", "why", "beauty"]
    thread_count = 4
    semaphore = threading.Semaphore(thread_count)
    threads = [threading.Thread(target=get_word_definition, args=(word, semaphore)) for word in words_to_search]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
