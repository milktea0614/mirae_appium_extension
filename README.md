# mirae_appium_extension
Appium Extension library for me

---

## Configuration format

You can set up the configuration using json file or dictionary type value.

### Mandatory key-value.
- **appium_server**: Input appium server 'IP:Port' information.
- **capabilities**: Input capabilities information.
    - Please refer to [Capabilities - Appium Documentation](https://appium.io/docs/en/2.1/guides/caps/)
- **save_page**: Input the directory path to save page information.
- **save_log_option**: Save file log option. (true / false)
- **save_log_path**: if you set up the 'save_log_option' as true, it is mandatory key-value.

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
    "save_page": "D:\\save_page",
    "save_log_option": true,
    "save_log_path": "D:\\mirae_appium_extension_log.log" 
}
```

---
