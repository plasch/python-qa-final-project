import datetime
import os

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from utils import setup_logging

DRIVERS_DIRECTORY = os.path.expanduser("~/Dev/drivers")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    try:
        if rep.when == 'call' and rep.failed:
            if 'browser' in item.fixturenames:
                web_driver = item.funcargs['browser']
            else:
                print('Fail to take screen-shot')
                return
            allure.attach(
                web_driver.get_screenshot_as_png(),
                name='screenshot',
                attachment_type=allure.attachment_type.PNG
            )
    except Exception as e:
        print('Fail to take screen-shot: {}'.format(e))


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", choices=["chrome", "firefox", "opera"])
    parser.addoption("--browser_version", action="store", default="96")
    parser.addoption("--executor", action="store", default="192.168.100.4")
    parser.addoption("--url", action="store", default="https://demo.opencart.com")
    parser.addoption("--log_level", action="store", default="INFO")
    parser.addoption("--videos", default=False)
    parser.addoption("--vnc", default=True)
    parser.addoption("--logs", default=True)


def driver_factory(request):
    browser = request.config.getoption("--browser")
    browser_version = request.config.getoption("--browser_version")
    executor = request.config.getoption("--executor")
    vnc = request.config.getoption("--vnc")
    logs = request.config.getoption("--logs")
    videos = request.config.getoption("--videos")

    if executor == "local":
        if browser == "chrome":
            options = webdriver.ChromeOptions()
            options.headless = True
            service = Service(executable_path=DRIVERS_DIRECTORY + '/chromedriver')
            driver = webdriver.Chrome(service=service, options=options)
        elif browser == "firefox":
            driver = webdriver.Firefox(executable_path=DRIVERS_DIRECTORY + "/geckodriver")
        elif browser == "opera":
            driver = webdriver.Opera(executable_path=DRIVERS_DIRECTORY + "/operadriver")
        else:
            raise Exception("Driver not supported")

    else:
        executor_url = f"http://{executor}:4444/wd/hub"
        caps = {
            "browserName": browser,
            "browserVersion": browser_version,
            "name": "Tester",
            "selenoid:options": {
                "enableVNC": vnc,
                "enableVideo": videos,
                "enableLog": logs
            }
        }
        driver = webdriver.Remote(
            command_executor=executor_url,
            desired_capabilities=caps
        )
    return driver


@pytest.fixture
def browser(request):
    url = request.config.getoption("--url")
    log_level = request.config.getoption("--log_level")
    test_name = request.node.name

    logger = setup_logging(log_level, test_name)
    logger.info("===> Test {} started at {}".format(test_name, datetime.datetime.now()))

    driver = driver_factory(request)
    driver.maximize_window()
    driver.test_name = test_name
    driver.log_level = log_level
    driver.url = url
    driver.logger = logger

    logger.info("Browser: {}".format(driver.capabilities))

    def fin():
        driver.quit()
        logger.info("===> Test {} finished at {}".format(test_name, datetime.datetime.now()))
    request.addfinalizer(fin)
    return driver
