# Name: Justice Kane
# OSU Email: kaneju@oregonstate.edu
# Course: CS361 - Software Engineering I
# Assignment: Microservice
# Due Date: 5/23/22
# Description:

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DRIVER_PATH = 'C:/Users/Patrick/Desktop/Scraping/chromedriver_win32/chromedriver'
wd = webdriver.Chrome(service=Service(executable_path=DRIVER_PATH))

# Makes a variable that determines if the search engine is inside the text file.
is_chrome = False
is_bing = False
is_yahoo = False


def fetch_image_urls(query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 1):
    """
    A method that finds a particular phrase and gets the image links.
    :param query: Searches term, like "Dog".
    :param max_links_to_fetch: Number of links the scraper is supposed to collect.
    :param wd: Instantiated Webdriver.
    :param sleep_between_interactions: Amount of time for the method to sleep (default at 1).
    :return: Link(s) of image(s).
    """
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)

    # Build the Google query.
    if is_chrome is True:
        # Build the Google query.
        search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_1=img"
    elif is_yahoo is True:
        search_url = "https://images.search.yahoo.com/images/search?q={q}"

    # Load the page.
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0

    # While the image count is less than the given number of photo links to fetch...
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # Get all image thumbnail results.
        if is_chrome is True:
            # Get all image thumbnail results.
            thumbnail_results = wd.find_elements(by=By.CSS_SELECTOR, value="img.Q4LuWd")
        elif is_yahoo is True:
            # thumbnail_results = wd.find_elements(by=By.XPATH, value='//a[@class="img"]/img[@src]')
            thumbnail_results = wd.find_elements(by=By.CLASS_NAME, value="img")

        number_results = len(thumbnail_results)

        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

        for img in thumbnail_results[results_start:number_results]:
            # Try to click every thumbnail such that we can get the real image behind it.
            try:
                img.click()
                time.sleep(sleep_between_interactions)

            except Exception:
                continue

            # Extract image urls.
            if is_chrome is True:
                # Extract image urls.
                actual_images = wd.find_elements(by=By.CSS_SELECTOR, value='img.n3VNCb')
            elif is_yahoo is True:
                # actual_images = wd.find_elements(by=By.XPATH, value='//li[@class="viewer focused"]/img[@src]')
                actual_images = wd.find_elements(by=By.ID, value="img")

            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))
                    # WebDriverWait(wd, 5).until(EC.element_to_be_clickable((By.XPATH, '//li[@class="ld r0 rn"]//a[@class="img"]'))).click()
                    # WebDriverWait(wd, 1).until(EC.element_to_be_clickable((By.CLASS_NAME, "close")))

            image_count = len(image_urls)

            if len(image_urls) == max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break

        else:
            print("Found:", len(image_urls), "image links, looking for more...")
            time.sleep(30)
            # return
            load_more_button = wd.find_elements_by_css_selector(".mye4qd")
            if load_more_button:
                wd.execture_script("document.querySelector('.mye4qd').click();")

        # Move the result start point further down.
        results_start = len(thumbnail_results)

    return image_urls


def search_and_download(search_term: str, driver_path: str, number_images: int):
    """
    A method that combines the previous two functions to make a web scraper, along with adding resiliency to how the
    ChromeDriver is used.
    :param search_term: The keyword to search the image for (string).
    :param driver_path: The path to where the ChromeDriver is located at in files (string).
    :param number_images: Number of images that is at default 1, but could be set to whatever number
    you desired. An integer.
    :return: Finds the image(s) and its URL, then downloads it to "target_path".
    """
    # Creates a variable that is equal to an empty string.
    new_res = ""

    # 'We are using the ChromeDriver within a "with" context, guaranteeing that the browser closes down ordinarily,
    # even if something within the "with" context raises an error' (quote from Fabian Bosler).
    with webdriver.Chrome(service=Service(executable_path=driver_path)) as wd:
        res = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=0.5)

    for elem in res:
        # Adds the url element onto the variable "new_res".
        new_res += str(elem)
        # Inserts a space afterwards, to differentiate between the two links.
        new_res += " "

    return new_res


while True:
    # Sleeps for 1 second.
    time.sleep(10)

    # Makes the index variable equal to zero.
    index = 0

    # Open file "image-service.txt".
    with open('image-service.txt') as text:
        # Reads file.
        lines = text.readlines()
        print("img_line:", lines)

        for line in lines:
            # If the word "Chrome" is in the line...
            if "Chrome" in line:
                is_chrome = True

                # Then the variable "search_term" will equal to the term after the 9th character.
                search_term = line[9:]
                # Makes the number of images equal to the number between the 7th and 9th character.
                num_img = int(line[7:9])
                # Calls the function with the specified parameters.
                new_res = search_and_download(search_term=search_term, driver_path=DRIVER_PATH, number_images=num_img)
                # Replaces the particular line inside the text file with the url(s) of the photo(s).
                lines[index] = new_res + "\n"
                print("- new lines:", lines)

                # Open file "image-service.txt" as an empty one.
                with open('image-service.txt', 'w') as new_text:
                    # Writes all existing lines, including the updated one, into the file again.
                    new_text.writelines(lines)

                # Closes file.
                new_text.close()

            # If the word "Yahoo" is in the line...
            if "Yahoo" in line:
                is_yahoo = True

                # Then the variable "search_term" will equal to the term after the 8th character.
                search_term = line[8:]
                # Makes the number of images equal to the number between the 6th and 8th character.
                num_img = int(line[6:8])
                # Calls the function with the specified parameters.
                new_res = search_and_download(search_term=search_term, driver_path=DRIVER_PATH, number_images=num_img)
                # Replaces the particular line inside the text file with the url(s) of the photo(s).
                lines[index] = new_res + "\n"
                print("- new lines:", lines)

                # Open file "image-service.txt" as an empty one.
                with open('image-service.txt', 'w') as new_text:
                    # Writes all existing lines, including the updated one, into the file again.
                    new_text.writelines(lines)

                # Closes file.
                new_text.close()

            # Increases the index value by 1.
            index += 1

            # Makes the variable for each search engine become False again.
            is_chrome = False
            is_bing = False
            is_yahoo = False

    # Closes file.
    text.close()

