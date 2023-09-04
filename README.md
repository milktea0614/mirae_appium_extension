# mirae_appium_extension
Appium Extension library for me

---

## Configuration format

You can set up the configuration using json file or dictionary type value.

### Mandatory key-value.
- appium_server: Input appium server 'IP:Port' information.
- capabilities: Input capabilities information.
    - Please refer to [Capabilities - Appium Documentation](https://appium.io/docs/en/2.1/guides/caps/)
- save_page: Input the directory path to save page information.
### Example
```
{
    "appium_server": "http://localhost:4723",
    "capabilities": {
        "platformName": "Android",
        "automationName": "uiautomator2",
        "deviceName": "emulator-0001",
        "appPackage": "com.android.settings",
        "appActivity": ".Settings"
    },
    "save_page": "D:\\save_page"
}
```

---
