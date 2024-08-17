import os
import time
from appium.webdriver.appium_service import AppiumService
from appium import webdriver
from appium.options.android import UiAutomator2Options
from app_management.models import AppManagement
from selenium.common.exceptions import WebDriverException, InvalidSessionIdException

def automate_app(app: AppManagement):
    appium_service = AppiumService()
    appium_service.start()

    desired_caps = {
        "platformName": "Android",
        "platformVersion": "7.0",
        "deviceName": "Nexus_5X_API_24",
        "automationName": "UiAutomator2",
        "app": app.apk_file_path.path
    }

    try:
        capabilities_options = UiAutomator2Options().load_capabilities(desired_caps)
        appium_server_url = 'http://localhost:4723'
        driver = webdriver.Remote(command_executor=appium_server_url, options=capabilities_options)

        print("Starting....")

        time.sleep(10)

        first_ui = driver.page_source

        first_screenshot_path = os.path.join('apk/images/first_screen_screenshot_path/', f'first_screenshot_{app.pk}.png')
        driver.save_screenshot(first_screenshot_path)
        app.first_screen_screenshot_path.name = first_screenshot_path

        time.sleep(5)  

        second_screenshot_path = os.path.join('apk/images/second_screen_screenshot_path/', f'second_screenshot_{app.pk}.png')
        driver.save_screenshot(second_screenshot_path)
        app.second_screen_screenshot_path.name = second_screenshot_path

        second_ui = driver.page_source

        # Check API level before attempting to record video
        api_level = driver.capabilities.get('platformVersion')
        if int(api_level.split('.')[0]) >= 27:
            video_path = os.path.join('apk/video/', f'app_video_{app.pk}.mp4')
            driver.start_recording_screen()

            time.sleep(1)

            raw_video_data = driver.stop_recording_screen()
            with open(video_path, "wb") as video_file:
                video_file.write(raw_video_data.encode('latin1'))
            app.video_recording_path.name = video_path
        else:
            print("Skipping video recording due to unsupported API level")

        ui_hierarchy = driver.page_source
        app.ui_hierarchy = ui_hierarchy

        app.screen_changed = first_ui != second_ui

        app.save()

    except InvalidSessionIdException as e:
        print(f"Session ended unexpectedly: {e}")
        
    except WebDriverException as e:
        print(f"WebDriverException occurred: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()
        appium_service.stop()

    print(f"Automation completed for app: {app.name}")
