from datetime import datetime, timedelta
from logging import Logger
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import platform

OS_BASE = platform.system()


class Actions:
    def __init__(self, driver: WebDriver, wait: WebDriverWait, logger: Logger):
        self._driver = driver
        self._wait = wait
        self._action = ActionChains(self._driver)
        self.logger = logger

    def click_avatar(self):
        self._wait_and_click(By.CSS_SELECTOR, '.p-ia__nav__user__avatar')
        self.logger.debug('click_avatar')

    def get_current_status_emoji(self):
        try:
            wait = WebDriverWait(self._driver, 1)
            wait.until(EC.visibility_of_element_located([By.CSS_SELECTOR, '.p-ia__main_menu__custom_status_emoji']))
            emoji = self._driver.find_element(By.CSS_SELECTOR, '.p-ia__main_menu__custom_status_emoji')
            emoji = emoji.get_attribute('data-stringify-emoji')
            self.logger.debug(f'get_current_status_emoji: {emoji=}')
            return emoji
        except Exception as e:
            self.logger.debug(f'get_current_status_emoji: exception={e}')
            return

    def get_current_status_text(self):
        try:
            wait = WebDriverWait(self._driver, 2)
            wait.until(EC.visibility_of_element_located([By.CSS_SELECTOR, '.p-ia__main_menu__custom_status_text']))
            status = self._driver.find_element(By.CSS_SELECTOR, '.p-ia__main_menu__custom_status_text')
            self.logger.debug(f'get_current_status_text: text={status.text}')
            return status.text
        except Exception as e:
            self.logger.debug(f'get_current_status_text: exception={e}')
            return

    def click_update_status_button(self):
        self._wait_and_click(By.CSS_SELECTOR, '.p-ia__main_menu__custom_status_button')
        self.logger.debug('click_update_status_button')

    def click_emoji_picker_button(self):
        self._wait_and_click(By.CSS_SELECTOR, 'button[data-qa="custom_status_input_emoji_picker"]')
        self.logger.debug('click_emoji_picker_button')

    def select_emoji(self, emoji_name):
        emoji_name = emoji_name.replace(':', '')
        self._wait.until(EC.visibility_of_element_located([By.CSS_SELECTOR, '.p-emoji_picker__input']))
        emoji_picker_input = self._driver.find_element(By.CSS_SELECTOR, '.p-emoji_picker__input')
        emoji_picker_input.send_keys(emoji_name)
        self.logger.debug(f'select_emoji: action=send_keys value={emoji_name}')
        self.logger.debug(f'select_emoji: implicit_wait')
        self._driver.implicitly_wait(2)

        def is_emoji_first(driver: WebDriver):
            first_emoji = driver.find_element(By.CSS_SELECTOR, f'.p-emoji_picker__list_scroller img:first-of-type')
            return first_emoji.get_attribute("data-stringify-emoji") == emoji_name
        self._wait.until(is_emoji_first)
        self.logger.debug(f'select_emoji: wait_until_is_emoji_first')
        if OS_BASE == 'Darwin':
            emoji_picker_input.send_keys(Keys.COMMAND, 'A')
        else:
            emoji_picker_input.send_keys(Keys.CONTROL, 'A')
        emoji_picker_input.send_keys(emoji_name)  # repeat emoji name, because sometimes the list gets reset
        self.logger.debug(f'select_emoji: action=send_keys value={emoji_name}')
        self._wait.until(is_emoji_first)
        self.logger.debug('select_emoji: action=wait_until_is_emoji_first')
        emoji_picker_input.send_keys(Keys.RETURN)

    def update_status(self, status):
        self._wait.until(EC.visibility_of_element_located([By.CSS_SELECTOR, 'div[aria-label="Status"]']))
        update_status_input = self._driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Status"]')

        if OS_BASE == 'Darwin':
            update_status_input.send_keys(Keys.COMMAND, 'A')
        else:
            update_status_input.send_keys(Keys.CONTROL, 'A')
        update_status_input.send_keys(status)
        update_status_input.send_keys(Keys.RETURN)
        self.logger.info(f"Slack status updated (probably - too lazy to check ¯\_(ツ)_/¯). Status: {status}")

    def click_clear_all_button(self):
        self._wait_and_click(By.CSS_SELECTOR, 'button[aria-label="Clear all"]')
        self.logger.debug('click_clear_all_button')

    def click_save_button(self):
        self._wait_and_click(By.CSS_SELECTOR, 'button[data-qa="custom_status_input_go"]')
        self.logger.debug('click_save_button')

    def click_status_duration_dropdown(self):
        self._wait_and_click(By.CSS_SELECTOR, '#custom_status_duration_default_button')
        self.logger.debug('click_status_duration_dropdown')

    def click_choose_date_and_time_option(self):
        self._wait.until(EC.visibility_of_element_located([By.CSS_SELECTOR, '#custom_status_duration_default_listbox']))
        options = self._driver.find_element(By.CSS_SELECTOR, '#custom_status_duration_default_listbox')
        option = options.find_element(By.XPATH, '//div[@role="option"]/*[contains(text(), "Choose date and time")]')
        self._action.move_to_element(option).click().perform()
        self.logger.debug('click_choose_date_and_time_option')

    def update_time_picker(self, song_duration):
        """DOESN'T WORK. Slack only lets you select the times from the dropdown.
        Keeping it in case Slack gets an update.
        Updates the time picker with the time of the song end
        (not accurate, since we don't have the current time of the song - could be done in the future).
        """
        self._wait_and_click(By.CSS_SELECTOR, 'div[data-qa="date_time_picker_time_picker"]')
        time_picker = self._driver.find_element(By.CSS_SELECTOR, 'div[data-qa="date_time_picker_time_picker"]')
        end_time = datetime.now() + timedelta(milliseconds=song_duration)
        end_time = end_time.strftime('%I:%M %p')
        self._action.send_keys_to_element(time_picker, end_time, Keys.ENTER).perform()

    def escape(self, count=1):
        for _ in range(count):
            self._action.send_keys(Keys.ESCAPE).perform()
            self._driver.implicitly_wait(1)
        self.logger.debug(f'press_escape: count={count}')

    def _wait_and_click(self, *locator):
        self._wait.until(EC.visibility_of_element_located(locator))
        element = self._driver.find_element(*locator)
        self._action.move_to_element(element).click().perform()
