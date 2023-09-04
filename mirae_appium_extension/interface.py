# -*- coding: utf-8 -*-
"""Interface for control the devices."""

import abc
import json
import os

import mirae_appium_extension.exception
import appium.webdriver.appium_service

import urllib3.exceptions

from logging import DEBUG
from appium import webdriver
from miraelogger import Logger


class Interface:
    """Abstract class for appium extension."""

    def __init__(self, configuration):
        """Initialize class.

        :param dict/path configuration: Configuration dictionary for connect.
        :raise mirae_appium_extension.exception.AppiumExtensionConnectionException: Could not connect service.
        :raise mirae_appium_extension.exception.AppiumExtensionConfigurationException: Configuration information not meet to initialize.
        """
        self._configuration = None
        self._appium_service = None
        self._driver = None
        self._logger = None

        self._init_configuration(configuration)
        self._init_logger()
        self._connect()

    def _init_configuration(self, configuration):
        """Initialize a configuration.

        :param dict/path configuration: Configuration dictionary for connect.
        :raise mirae_appium_extension.exception.AppiumExtensionConfigurationException: Configuration information not meet to initialize.
        """
        if ('.json' in configuration) and (os.path.exists(configuration) is True):
            with open(configuration) as _config:
                self._configuration = json.load(_config)
        elif type(configuration) is dict:
            self._configuration = configuration
        else:
            raise mirae_appium_extension.exception.AppiumExtensionConfigurationException("Configuration does not meet to initialize.")

    def _init_logger(self):
        """Initialize a logger.

        :raise mirae_appium_extension.exception.AppiumExtensionConfigurationException: Configuration information not meet to initialize.
        """
        if self._configuration['save_log_option'] is True:
            if os.path.exists(self._configuration['save_log_path']):
                self._logger = Logger("mirae_appium_extension_logger", self._configuration['save_log_path'])
            else:
                raise mirae_appium_extension.exception.AppiumExtensionConfigurationException("Please check the 'save_log_path' value of configuration.")
        else:
            self._logger = Logger("mirae_appium_extension_logger", stream_log_level=DEBUG)

    def _connect(self):
        """Connect an appium server.

        :raise mirae_appium_extension.exception.AppiumExtensionConnectionException: Could not connect service.
        """
        self._appium_service = appium.webdriver.appium_service.AppiumService()
        self._appium_service.start()
        self._logger.debug("Appium service start successful.")

        try:
            self._driver = webdriver.Remote(self._configuration["appium_server"], self._configuration["capabilities"])
        except urllib3.exceptions.MaxRetryError:
            self._logger.exception(msg := f"Connect the {self._configuration['capabilities']['deviceName']} is failed.")
            raise mirae_appium_extension.exception.AppiumExtensionConnectionException(msg)
        self._logger.info(f"Connect the {self._configuration['capabilities']['deviceName']} is success.")

    def finalize(self) -> None:
        """Disconnect the appium and stop appium service."""
        self._driver.quit()
        self._appium_service.stop()
        self._logger.info(f"Finalize the {self._configuration['capabilities']['deviceName']} is success.")

    @abc.abstractmethod
    def save_page(self) -> None:
        """Save the screenshot and xml file."""

    @abc.abstractmethod
    def touch_element(self, xpath, timeout) -> None:
        """Touch an element in current screen.

        :param str xpath: Target element's xpath expression.
        :param float timeout: Timeout value.
        :raise mirae_appium_extension.exception.AppiumExtensionException: Could not touch element.
        :raise mirae_appium_extension.exception.AppiumExtensionTimeoutException: Could not find element within timeout.
        """

    @abc.abstractmethod
    def double_touch_element(self, xpath, timeout=1.0) -> None:
        """Double tap an element in current screen.

        :param str xpath: Target element's xpath expression.
        :param float timeout: Waiting the timeout value to find element.
        :raise mirae_appium_extension.exception.AppiumExtensionException: Could not touch element.
        :raise mirae_appium_extension.exception.AppiumExtensionTimeoutException: Could not find element within timeout.
        """
    @abc.abstractmethod
    def long_press_element(self, xpath, timeout=1.0) -> None:
        """Long press an element in current screen.

        :param str xpath: Target element's xpath expression.
        :param float timeout: Waiting the timeout value to find element.
        :raise mirae_appium_extension.exception.AppiumExtensionException: Could not long press element.
        :raise mirae_appium_extension.exception.AppiumExtensionTimeoutException: Could not find element within timeout.
        """

    @abc.abstractmethod
    def enter_text(self, xpath, text, timeout=1.0) -> None:
        """Input the text into target elements.

        :param str xpath: Target element xpath expression.
        :param str text: Target text.
        :param float timeout: Waiting the timeout value to find element.
        :raise mirae_appium_extension.exception.AppiumExtensionException: Could not input the text.
        :raise mirae_appium_extension.exception.AppiumExtensionTimeoutException: Could not find element within timeout.
        """

    @abc.abstractmethod
    def scroll(self, direction="up", times=1, x_position=None) -> None:
        """Scroll the screen.

        :param str direction: Scroll direction string.
        :param int times: Scroll repeat times. (default=1)
        :param int x_position: Standard X position. (default=None)
        """

    @abc.abstractmethod
    def swipe(self, direction="right", times=1, y_position=None) -> None:
        """Swipe the screen.

        :param str direction: Swipe direction string.
        :param int times: Swipe repeat times. (default=1)
        :param int y_position: Standard Y position. (default=None)
        """

    @abc.abstractmethod
    def zoom_in(self, direction="vertical", times=1) -> None:
        """Zoom-in the current screen.

        :param str direction: Zoom-in direction. (vertical, horizontal).
        :param int times: Zoom-in times.
        """

    @abc.abstractmethod
    def zoom_out(self, direction="vertical", times=1) -> None:
        """Zoom-out the current screen.

        :param str direction: Zoom-out direction. (vertical, horizontal).
        :param int times: Zoom-out times.
        """

    @abc.abstractmethod
    def go_to_screen(self, click_xpath, target_screen_xpath) -> bool:
        """Go to screen through click the button.

        :param str click_xpath: Xpath to click.
        :param str target_screen_xpath: Unique Xpath to checking screen is target.
        :return: True if successful, otherwise False.
        :rtype: bool.
        :raise mirae_appium_extension.exception.AppiumExtensionException: Could not click element.
        """
