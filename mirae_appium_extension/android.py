# -*- coding: utf-8 -*-
import datetime
import os.path

import mirae_appium_extension.interface
import selenium.common.exceptions

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction

class AndroidDevice(mirae_appium_extension.interface.Interface):
    """Class for the device or emulator based on the Android."""

    def __init__(self, configuration):
        """Initialize class.

       :param dict/path configuration: Configuration dictionary for connect.
       :raise mirae_appium_extension.exception.AppiumExtensionConnectionException: Could not connect service.
       """
        super().__init__(configuration)

    def save_page(self) -> None:
        """Save the screenshot and xml file."""
        _current_time = str(datetime.datetime.now().timestamp())
        _page_path = os.path.join(self._configuration['save_page'], f"{_current_time}.xml")
        _screenshot_path = os.path.join(self._configuration['save_page'], f"{_current_time}.png")

        # Save page source (.xml)
        _page = self._driver.page_source
        with open(_page_path, 'w', encoding='utf-8') as f:
            f.write(_page)

        # Save page screenshot (.png)
        self._driver.save_screenshot(_screenshot_path)
        self._logger.info(f"Current screen is saved as the '{_screenshot_path}'")

    def touch_element(self, xpath, timeout=1.0) -> None:
        """Touch an element in current screen.

        :param str xpath: Target element's xpath expression.
        :param float timeout: Waiting the timeout value to find element.
        :raise mirae_appium_extension.exception.AppiumExtensionException: Could not touch element.
        :raise mirae_appium_extension.exception.AppiumExtensionTimeoutException: Could not find element within timeout.
        """
        self._driver.implicitly_wait(timeout)
        try:
            _target = self._driver.find_element(by=AppiumBy.XPATH, value=xpath)
            _target.click()
            self._logger.debug(f"Touch the '{xpath}' is success.")
        except (selenium.common.exceptions.NoSuchElementException, RuntimeError):
            self.save_page()
            self._logger.exception(msg := f"Touch the '{xpath}' is failed")
            raise mirae_appium_extension.exception.AppiumExtensionException(msg)
        except TimeoutError:
            self.save_page()
            self._logger.exception(msg := f"Could not find the '{xpath}' within {timeout} sec.")
            raise mirae_appium_extension.exception.AppiumExtensionTimeoutException(msg)

    def double_touch_element(self, xpath, timeout=1.0) -> None:
        """Double tap an element in current screen.

        :param str xpath: Target element's xpath expression.
        :param float timeout: Waiting the timeout value to find element.
        :raise mirae_appium_extension.exception.AppiumExtensionException: Could not touch element.
        :raise mirae_appium_extension.exception.AppiumExtensionTimeoutException: Could not find element within timeout.
        """
        self._driver.implicitly_wait(timeout)
        try:
            _target = self._driver.find_element(by=AppiumBy.XPATH, value=xpath)
            TouchAction(self._driver).tap(_target).perform()
            TouchAction(self._driver).tap(_target).perform()
            self._logger.debug(f"Double-touch the '{xpath}' is success.")
        except (selenium.common.exceptions.NoSuchElementException, RuntimeError):
            self.save_page()
            self._logger.exception(msg := f"Double-touch the '{xpath}' is failed")
            raise mirae_appium_extension.exception.AppiumExtensionException(msg)
        except TimeoutError:
            self.save_page()
            self._logger.exception(msg := f"Could not find the '{xpath}' within {timeout} sec.")
            raise mirae_appium_extension.exception.AppiumExtensionTimeoutException(msg)

    def long_press_element(self, xpath, timeout=1.0) -> None:
        """Long press an element in current screen.

        :param str xpath: Target element's xpath expression.
        :param float timeout: Waiting the timeout value to find element.
        :raise mirae_appium_extension.exception.AppiumExtensionException: Could not long press element.
        :raise mirae_appium_extension.exception.AppiumExtensionTimeoutException: Could not find element within timeout.
        """
        self._driver.implicitly_wait(timeout)
        try:
            _target = self._driver.find_element(by=AppiumBy.XPATH, value=xpath)
            TouchAction(self._driver).long_press(_target).release().perform()
            self._logger.debug(f"Long-press the '{xpath}' is success.")
        except (selenium.common.exceptions.NoSuchElementException, RuntimeError):
            self.save_page()
            self._logger.exception(msg := f"Long-press the '{xpath}' is failed")
            raise mirae_appium_extension.exception.AppiumExtensionException(msg)
        except TimeoutError:
            self.save_page()
            self._logger.exception(msg := f"Could not find the '{xpath}' within {timeout} sec.")
            raise mirae_appium_extension.exception.AppiumExtensionTimeoutException(msg)

    def enter_text(self, xpath, text, timeout) -> None:
        pass

    def scroll(self, direction="up", times=1, x_position=None) -> None:
        pass

    def swipe(self, direction="right", times=1, y_position=None) -> None:
        pass

    def zoom_in(self, direction="vertical", times=1) -> None:
        pass

    def zoom_out(self, direction="vertical", times=1) -> None:
        pass

    def go_to_screen(self, click_xpath, target_screen_xpath) -> bool:
        pass

    def go_to_home(self):
        """Go home."""
        self._driver.press_keycode(3)

    def send_keyevent(self, keycode):
        """Send the keyevent.

        :param """