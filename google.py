from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class GoogleKeywordScreenshooter:
    def __init__(self, keyword, screenshots_dir, max_page=1):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.keyword = keyword
        self.screenshots_dir = screenshots_dir
        self.max_page = max_page

    def start(self):
        self.browser.get("https://google.com")
        search_bar = self.browser.find_element_by_class_name("gLFyf")
        search_bar.send_keys(self.keyword)
        search_bar.send_keys(Keys.ENTER)
        for page in range(1, int(self.max_page + 1)):
            try:
                useless_element = WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "g-blk"))
                )
                self.browser.execute_script(
                    """
                const useless = arguments[0];
                useless.parentElement.removeChild(useless)
                """,
                    useless_element,
                )
            except Exception:
                pass
            search_results = self.browser.find_elements_by_class_name("g")
            for index, search_result in enumerate(search_results):
                search_result.screenshot(
                    f"{self.screenshots_dir}/{self.keyword}_page{page}_{index}.png"
                )
            try:
                next_page = self.browser.find_element_by_id("pnnext")
            except NoSuchElementException:
                break
            else:
                if page != int(self.max_page):
                    next_page.click()

    def finish(self):
        self.browser.quit()


domain_competitors = GoogleKeywordScreenshooter("buy domain", "screenshots", 5)
domain_competitors.start()
domain_competitors.finish()
python_competitors = GoogleKeywordScreenshooter("python book", "screenshots", 3)
python_competitors.start()
python_competitors.finish()
