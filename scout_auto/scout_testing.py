import sys
from django.test import LiveServerTestCase, Client
from django.conf import settings
from sauceclient import SauceClient
from selenium.webdriver import Firefox, Remote

useSauce = getattr(settings, 'SAUCE_ENABLED', False)

USERNAME = getattr(settings, 'SAUCE_USERNAME', None)
ACCESS_KEY = getattr(settings, 'SAUCE_ACCESS_KEY', None)

if useSauce:
    sauce_client = SauceClient(USERNAME, ACCESS_KEY)

class ScoutTest(LiveServerTestCase):

    def setUp(self):

        self.useSauce = useSauce
        self.client = Client()
        self.baseurl = self.live_server_url

        self.driver = self.get_driver()

    def get_driver(self):
        if useSauce:
            return self.get_sauce_driver()
        else:
            return Firefox()

    def get_sauce_driver(self):
        desired_cap = {
            'platform': 'Mac OS X 10.9',
            'browserName': 'chrome',
            'version': '31',
            'tags': ['ui']
        }
        sauceUrl = 'http://%s:%s@ondemand.saucelabs.com:80/wd/hub' \
            % (USERNAME, ACCESS_KEY)

        driver = Remote(
            command_executor=sauceUrl,
            desired_capabilities=desired_cap)

        return driver

    def updateSauceName(self, name):
        """Sets the saucelabs job name"""
        if self.useSauce:
            sauce_client.jobs.update_job(self.driver.session_id, name=name)

    def tearDown(self):
        # print('https://saucelabs.com/jobs/%s \n' % self.driver.session_id)
        if self.useSauce:
            if sys.exc_info() == (None, None, None):
                sauce_client.jobs.update_job(
                    self.driver.session_id,
                    passed=True)
            else:
                sauce_client.jobs.update_job(
                    self.driver.session_id,
                    passed=False)
        self.driver.quit()

