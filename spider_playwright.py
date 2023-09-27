import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from playwright._impl._api_types import TimeoutError

sem = asyncio.Semaphore(10)  # Limit the number of concurrent tasks to 10


# Create a new function to handle page fetching and parsing
async def fetch_and_parse(page, word):
    await page.goto(f"https://www.iciba.com/{word}")
    try:
        await page.click('xpath=//div[@class="DicTab_tab__q1zCE"]//li[2]', timeout=7000)  # Click the Collins tab
    except TimeoutError:
        print(f"Timeout while waiting for word: {word}, maybe it isn't included in this dictionary")
        return False
    await page.wait_for_selector('xpath=//div[@class="Collins_collins__E16AT"]')  # Wait for the Collins content to load
    content = await page.content()  # Get the page content
    return BeautifulSoup(content, 'html.parser')  # Parse the page source with BeautifulSoup


async def get_word_definition(word):
    async with sem, async_playwright() as playwright:  # This will block if there are already 10 running tasks
        browser = await playwright.chromium.launch(headless=True)  # Launch the browser
        context = await browser.new_context()  # Create a new browser context
        page = await context.new_page()  # Open a new page
        soup = await fetch_and_parse(page, word)  # Call the newly created function to fetch and parse the page
        await browser.close()
        if not soup:
            return
        else:
            collins_blocks = soup.find_all('div', class_='Collins_collins__E16AT')
            output = f"Collins Definitions and Examples for {word}:\n"
            for count, block in enumerate(collins_blocks, 1):
                title = block.find('h5').text.strip() if block.find('h5') else ''
                definition = f"Definition: {block.find('p').text.strip()}\n" if block.find('p') else ''
                examples = block.find_all('li')
                example_texts = [
                    f"Example {i + 1}: {example.find('span').text.strip()} {example.find('p').text.strip()}\n"
                    for i, example in enumerate(examples)
                    if example.find('span') and example.find('p')]
                output += f'{count}. {title}\n{definition}{"".join(example_texts)}'

            with open("output.txt", "a") as f:  # Open the file in append mode
                f.write(output + '}\n' + "\n")


# Main function to get definitions of all words in parallel
async def main(words_to_search):
    await asyncio.gather(*(get_word_definition(word) for word in words_to_search))


if __name__ == '__main__':
    words_to_search = ["sexy", "test", "dream", "how", "example", "with", "team", "why",
                       "beauty"]
    asyncio.run(main(words_to_search))
