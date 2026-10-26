# pages/base_page.py
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver, timeout = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url):
        self.driver.get(url)

    def find(self, locator):
        return  self.wait.until((EC.presence_of_element_located(locator)))

    def is_present(self, locator):
        return len(self.driver.find_elements(*locator)) > 0

    def get_text(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def type_text(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        element.click()

    def has_class(self, locator, class_name, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element_attribute(locator, "class", class_name)
            )
            return True
        except TimeoutException:
            return False

    def get_current_url(self):
        return self.driver.current_url

    def wait_url_contains(self, part):
        self.wait.until(EC.url_contains(part))

    def is_visible(self, locator, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    # ===== УРОК 42: методы для списков =====
    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def get_texts(self, locator):
        return [element.text for element in self.find_all(locator)]