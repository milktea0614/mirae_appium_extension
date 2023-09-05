# -*- coding: utf-8 -*-
"""Exception for Appium extension."""


class AppiumExtensionException(Exception):
    """Raised if an exception occurs."""


class AppiumExtensionTimeoutException(Exception):
    """Raised if a timeout exception occurs."""


class AppiumExtensionConnectionException(Exception):
    """Raised if a connection exception occurs."""


class AppiumExtensionConfigurationException(Exception):
    """Raised if a configuration exception occurs."""


class AppiumExtensionValueException(Exception):
    """Raised if a value exception occurs."""