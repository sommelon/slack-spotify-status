from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Actions:
    def __init__(self, driver: WebDriver):
        self._driver = driver
        self._wait = WebDriverWait(self._driver, 10)
        self._action = ActionChains(self._driver)

    def click_avatar(self):
        self._wait_and_click(By.CSS_SELECTOR, '.p-ia__nav__user__avatar')

    def get_current_status_emoji(self):
        try:
            self._wait.until(EC.visibility_of_element_located([By.CSS_SELECTOR, '.p-ia__main_menu__custom_status_emoji']))
            emoji = self._driver.find_element(By.CSS_SELECTOR, '.p-ia__main_menu__custom_status_emoji')
            emoji = emoji.get_attribute('data-stringify-emoji')
            return emoji
        except Exception:
            pass

    def get_current_status_text(self):
        try:
            self._wait.until(EC.visibility_of_element_located([By.CSS_SELECTOR, '.p-ia__main_menu__custom_status_text']))
            status = self._driver.find_element(By.CSS_SELECTOR, '.p-ia__main_menu__custom_status_text')
            return status.text
        except Exception:
            return

    def click_update_status_button(self):
        self._wait_and_click(By.CSS_SELECTOR, '.p-ia__main_menu__custom_status_button')

    def click_emoji_picker_button(self):
        self._wait_and_click(By.CSS_SELECTOR, 'button[data-qa="custom_status_input_emoji_picker"]')

    def select_emoji(self, emoji_name):
        emoji_name = emoji_name.replace(':', '')
        self._wait.until(EC.visibility_of_element_located([By.CSS_SELECTOR, '.p-emoji_picker__input']))
        emoji_picker_input = self._driver.find_element(By.CSS_SELECTOR, '.p-emoji_picker__input')
        emoji_picker_input.send_keys(emoji_name)

        def is_emoji_first(driver: WebDriver):
            first_emoji = driver.find_element(By.CSS_SELECTOR, f'.p-emoji_picker__list_scroller img:first-of-type')
            return first_emoji.get_attribute("data-stringify-emoji") == emoji_name

        self._wait.until(is_emoji_first)
        emoji_picker_input.send_keys(Keys.RETURN)

    def update_status(self, status):
        self._wait.until(EC.visibility_of_element_located([By.CSS_SELECTOR, 'div[aria-label="Status"]']))
        update_status_input = self._driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Status"]')
        update_status_input.send_keys(Keys.CONTROL, 'A')
        update_status_input.send_keys(status)
        update_status_input.send_keys(Keys.RETURN)
        print(f"Slack status updated (probably - too lazy to check ¯\_(ツ)_/¯). Status: {status}")

    def click_clear_all_button(self):
        self._wait_and_click(By.CSS_SELECTOR, 'button[aria-label="Clear all"]')

    def click_save_button(self):
        self._wait_and_click(By.CSS_SELECTOR, 'button[data-qa="custom_status_input_go"]')

    def escape(self, count=1):
        for _ in range(count):
            self._driver.implicitly_wait(1)
            self._action.send_keys(Keys.ESCAPE).perform()

    def _wait_and_click(self, *locator):
        self._wait.until(EC.visibility_of_element_located(locator))
        element = self._driver.find_element(*locator)
        self._action.move_to_element(element).click().perform()