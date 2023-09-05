# -*- coding: utf-8 -*-
import datetime
import math
import os.path
import time

import mirae_appium_extension.mobile_interface
import selenium.common.exceptions

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction


class Android(mirae_appium_extension.mobile_interface.Interface):
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
            TouchAction(self._driver).tap(_target).perform()
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

    def scroll(self, direction="up", times=1, x_position=None) -> None:
        """Scroll the screen.

        :param str direction: Scroll direction string. (up, down)
        :param int times: Scroll repeat times. (default=1)
        :param int x_position: Standard X position. (default=None)
        :raise mirae_appium_extension.exception.AppiumExtensionException: Could not scroll.
        :raise mirae_appium_extension.exception.AppiumExtensionValueException: User input the invalid value.
        """
        if direction.lower() not in ["up", "down"]:
            self._logger.exception(msg := "Please check the 'direction' value. The 'direction' value must be in ['up', 'down']")
            raise mirae_appium_extension.exception.AppiumExtensionValueException(msg)

        _window_size = self._driver.get_window_size()
        _width = _window_size['width']
        _height = _window_size['height']

        if x_position is None:
            x_position = int(_width / 2)

        try:
            for _ in range(times):
                if direction.lower() == "up":
                    TouchAction(self._driver).press(x=x_position, y=int(_height / 2)).wait(100).move_to(x=x_position, y=int(
                        _height / 4)).release().perform()
                elif direction.lower() == "down":
                    TouchAction(self._driver).press(x=x_position, y=int(_height / 2)).wait(100).move_to(x=x_position, y=int(
                        _height / 4 * 3)).release().perform()
            self._logger.debug(f"Scroll to {direction} is finish.")
        except Exception:
            self._logger.exception(msg := f"Could not scroll to {direction}.")
            raise mirae_appium_extension.exception.AppiumExtensionException(msg)

    def swipe(self, direction="right", times=1, y_position=None) -> None:
        """Swipe the screen.

        :param str direction: Swipe direction string. (right, left)
        :param int times: Swipe repeat times. (default=1)
        :param int y_position: Standard Y position. (default=None)
        :raise mirae_appium_extension.exception.AppiumExtensionException: Could not swipe.
        """
        if direction.lower() not in ["right", "left"]:
            self._logger.exception(msg := "Please check the 'direction' value. The 'direction' value must be in ['right', 'left']")
            raise mirae_appium_extension.exception.AppiumExtensionValueException(msg)

        _window_size = self._driver.get_window_size()
        _width = _window_size['width']
        _height = _window_size['height']

        if y_position is None:
            y_position = int(_height / 2)

        try:
            for _ in range(times):
                if direction.lower() == "right":
                    TouchAction(self._driver).press(x=int(_width / 2), y=y_position).wait(100).move_to(x=int(_width / 4), y=y_position).release().perform()
                elif direction.lower() == "left":
                    TouchAction(self._driver).press(x=int(_width / 2), y=y_position).wait(100).move_to(x=int(_width / 4 * 3), y=y_position).release().perform()

            self._logger.debug(f"Swipe to {direction} is finish.")
        except Exception:
            self._logger.exception(msg := f"Could not swipe to {direction}.")
            raise mirae_appium_extension.exception.AppiumExtensionException(msg)

    def pinch_in(self, times=1) -> None:
        """Pinch-In(=to reduce) the current screen.

        :param int times: Pinch times.
        :raise mirae_appium_extension.exception.AppiumExtensionException: Could not Pinch-in.
        """
        _window_size = self._driver.get_window_size()
        standard_x = int(_window_size['width'] / 2)
        standard_y = int(_window_size['height'] / 2)

        _x1_start = int(standard_x + (250 * math.cos(math.radians(45))))
        _y1_start = int(standard_y + (250 * math.sin(math.radians(45))))
        _x1_end = int(standard_x + (50 * math.cos(math.radians(45))))
        _y1_end = int(standard_y + (50 * math.sin(math.radians(45))))

        _finger1 = TouchAction(self._driver)
        _finger1.press(x=_x1_start, y=_y1_start).wait(50).move_to(x=_x1_end, y=_y1_end).release()

        _x2_start = int(standard_x + (250 * math.cos(math.radians(225))))
        _y2_start = int(standard_y + (250 * math.sin(math.radians(225))))
        _x2_end = int(standard_x + (50 * math.cos(math.radians(225))))
        _y2_end = int(standard_y + (50 * math.sin(math.radians(225))))

        _finger2 = TouchAction(self._driver)
        _finger2.press(x=_x2_start, y=_y2_start).wait(50).move_to(x=_x2_end, y=_y2_end).release()

        _multi_touch = MultiAction(self._driver)
        try:
            for _ in range(times):
                _multi_touch.add(_finger1, _finger2)
                _multi_touch.perform()
            self._logger.debug(f"Pinch-In is finish.")
        except Exception:
            self._logger.exception(msg := f"Could not Pinch-In.")
            raise mirae_appium_extension.exception.AppiumExtensionException(msg)

    def pinch_out(self, times=1) -> None:
        """Pinch-Out(=to large) the current screen.

        :param int times: Pinch times.
        :raise mirae_appium_extension.exception.AppiumExtensionException: Could not Pinch-out.
        """
        _window_size = self._driver.get_window_size()
        standard_x = int(_window_size['width'] / 2)
        standard_y = int(_window_size['height'] / 2)

        _x1_start = int(standard_x + (50 * math.cos(math.radians(45))))
        _y1_start = int(standard_y + (50 * math.sin(math.radians(45))))
        _x1_end = int(standard_x + (250 * math.cos(math.radians(45))))
        _y1_end = int(standard_y + (250 * math.sin(math.radians(45))))

        _finger1 = TouchAction(self._driver)
        _finger1.press(x=_x1_start, y=_y1_start).wait(50).move_to(x=_x1_end, y=_y1_end).release()

        _x2_start = int(standard_x + (50 * math.cos(math.radians(225))))
        _y2_start = int(standard_y + (50 * math.sin(math.radians(225))))
        _x2_end = int(standard_x + (250 * math.cos(math.radians(225))))
        _y2_end = int(standard_y + (250 * math.sin(math.radians(225))))

        _finger2 = TouchAction(self._driver)
        _finger2.press(x=_x2_start, y=_y2_start).wait(50).move_to(x=_x2_end, y=_y2_end).release()

        _multi_touch = MultiAction(self._driver)
        try:
            for _ in range(times):
                _multi_touch.add(_finger1, _finger2)
                _multi_touch.perform()
            self._logger.debug(f"Pinch-Out is finish.")
        except Exception:
            self._logger.exception(msg := f"Could not Pinch-Out.")
            raise mirae_appium_extension.exception.AppiumExtensionException(msg)

    def rotate(self, degree=45, direction="clockwise", times=1) -> None:
        """Rotate degree gesture.

        :param int degree: Rotation degree value which is from 5 to 180 and must be divisible by 5. (default=45).
        :param str direction: Rotation direction (clockwise, counterclockwise).
        :param int times: Rotate times.
        :raise mirae_appium_extension.exception.AppiumExtensionException: Could not rotate.
        :raise mirae_appium_extension.exception.AppiumExtensionValueException: User input the invalid value.
        """
        if direction.lower() not in ["clockwise", "counterclockwise"]:
            self._logger.exception(msg := "Please check the 'direction' value. "
                                          "The 'direction' must be in ['clockwise', 'counterclockwise']")
            raise mirae_appium_extension.exception.AppiumExtensionValueException(msg)

        if ((5 <= degree <= 180) and (degree % 5 == 0)) is False:
            self._logger.exception(msg := "Please check the 'degree' value. "
                                          "The 'degree' must be from 5 to 180 and must be divisible by 5.")
            raise mirae_appium_extension.exception.AppiumExtensionValueException(msg)

        _window_size = self._driver.get_window_size()
        standard_x = int(_window_size['width'] / 2)
        standard_y = int(_window_size['height'] / 2)

        # create move position
        _x_list = []
        _y_list = []
        _move_times = int(degree / 5) + 1
        for i in range(_move_times):
            if direction == "counterclockwise":
                _x_list.append(int(standard_x + (200 * math.cos(math.radians(5 * i + 45)))))
                _y_list.append(int(standard_y + (200 * math.sin(math.radians(5 * i + 45)))))
            elif direction == "clockwise":
                _x_list.append(int(standard_x - (200 * math.cos(math.radians(225 - 5 * i)))))
                _y_list.append(int(standard_y - (200 * math.sin(math.radians(225 - 5 * i)))))

        # Init TouchActions
        _finger1 = TouchAction(self._driver)
        _finger2 = TouchAction(self._driver)

        _finger1.press(x=standard_x, y=standard_y).release()
        _finger2.press(x=_x_list[0], y=_y_list[0]).wait(50)
        for i in range(1, _move_times):
            _finger2.move_to(x=_x_list[i], y=_y_list[i])
        _finger2.release()

        _multi_touch = MultiAction(self._driver)
        try:
            for _ in range(times):
                _multi_touch.add(_finger1, _finger2)
                _multi_touch.perform()
            self._logger.debug(f"Rotate {degree} degrees ({direction}) is finish.")
        except Exception:
            self._logger.exception(msg := f"Could not Rotate {degree} degrees ({direction}).")
            raise mirae_appium_extension.exception.AppiumExtensionException(msg)

    def back(self) -> None:
        """Go back."""
        self._driver.back()

    def enter_text(self, xpath, text, timeout=1.0) -> None:
        """Input the text into target elements.

        :param str xpath: Target element xpath expression.
        :param str text: Target text.
        :param float timeout: Waiting the timeout value to find element.
        :raise mirae_appium_extension.exception.AppiumExtensionException: Could not input the text.
        :raise mirae_appium_extension.exception.AppiumExtensionTimeoutException: Could not find element within timeout.
        """
        pass

    def go_to_screen(self, click_xpath, target_screen_xpath) -> bool:
        """Go to screen through click the button.

        :param str click_xpath: Xpath to click.
        :param str target_screen_xpath: Unique Xpath to checking screen is target.
        :return: True if successful, otherwise False.
        :rtype: bool.
        :raise mirae_appium_extension.exception.AppiumExtensionException: Could not click element.
        """
        pass

    def go_to_home(self):
        """Go home."""
        self._driver.press_keycode(3)

    def send_keyevent(self, keycode):
        """Send the keyevent.

        :param """