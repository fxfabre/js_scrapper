#!/usr/bin/env python3

import re
from random import gauss
from time import time, sleep
from typing import Optional
from text_unidecode import unidecode
import unicodedata

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys

MEAN_WAIT_TIME = 5
STD_WAIT_TIME = 1


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # chrome_manager = ChromeDriverManager(
    #     path="/home/chromium", chrome_type=ChromeType.CHROMIUM
    # ).install()
    chrome_manager = ChromeDriverManager(
        path="/home/chrome", chrome_type=ChromeType.GOOGLE
    ).install()
    service = Service(chrome_manager)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_window_size(1920, 1080)

    return ChromeWrapper(driver)


def clean_text(text: str) -> str:
    return unidecode(text.strip()).lower().replace(" ", "")


class ChromeWrapper:
    def __init__(self, driver: webdriver.Chrome):
        super().__init__()
        self.driver = driver
        self.last_query = time()

    def search(self, search_string: str):
        # get_root_google_search
        self.get('https://www.google.com/')

        # Accepter les cookies : "Avant d'accéder à la recherche Google"
        if self._has_accept_cookies_form():
            button = self._find_node_with_text("button", "J'accepte")
            self.click(button)

        # Find search field and fill it
        self._fill_text_box(self.find_element(by=By.NAME, value="q"), search_string)
        return self

    def count_results(self):
        # Read number of results : "Environ 1 080 000 résultats (0,64 secondes)"
        box_count_results = self.find_element(by=By.ID, value="result-stats")
        count_results_str = unicodedata.normalize("NFKC", box_count_results.text)
        return int(re.search(r"\d+", count_results_str.replace(" ", "")).group())

    def __getattr__(self, name):
        return self.driver.__getattribute__(name)

    def wait(self):
        elapsed = time() - self.last_query
        wait_time = gauss(MEAN_WAIT_TIME, STD_WAIT_TIME) - elapsed
        if max(0.0, wait_time) > 0:
            print(f"Waiting {wait_time} seconds")
            sleep(wait_time)
        self.last_query = time()

    def get(self, *args, **kwargs):
        self.wait()
        self.driver.get(*args, **kwargs)

    def click(self, button: WebElement):
        self.wait()
        button.click()

    def _has_accept_cookies_form(self):
        title_cookies = "Avant d'accéder à la recherche Google"
        return self._find_node_with_text("h1", title_cookies) is not None

    def _find_node_with_text(self, node_name: str, content: str) -> Optional[WebElement]:
        content = clean_text(content)
        elements = self.find_elements(by=By.TAG_NAME, value=node_name)
        for element in elements:
            if not element.is_enabled():
                continue
            text = element.get_attribute("innerText")
            if clean_text(text) == content:
                return element
        return None

    def _fill_text_box(self, text_box: WebElement, content: str):
        self.wait()
        text_box.clear()
        text_box.send_keys(content)
        sleep(0.3)
        text_box.send_keys(Keys.RETURN)
        self.wait()
