#!/usr/bin/python
"""
A simple functional headless UI test with pyvirtualdisplay and selenium
Links and URLS
"""

import bs4
import sys
import unittest
import copy

from selenium import webdriver
from django.test import Client
from django.conf import settings
from scout_auto import pages
from scout_auto.scout_testing import ScoutTest

class NavigationTestSelenium(ScoutTest):
    """Navigation test set for scout"""

    def go_url(self, urlsuffix=''):
        """Has the driver go to the given URL"""
        self.driver.get(self.baseurl + urlsuffix)

    def clientUrlStatus(self, urlsuffix=''):
        """Returns the status code of the given URL"""
        res = self.client.get(urlsuffix)
        return res.status_code

    def assertLocation(self, exploc):
        """Checks to see if the current url matches the given intended URL"""
        curloc = self.driver.current_url
        if not exploc.startswith('http'):
            exploc = self.baseurl + exploc
        self.assertEqual(curloc, exploc)

    def assertUrlStatus(self, urlsuffix='', code=200):
        """Checks to see if the status code of the given URL matches the
        given status code"""
        self.assertEqual(self.clientUrlStatus(urlsuffix), code)

    def test_main_nav(self):
        """Goes from page to page and verifies that URLs are correct on
        each page """
        self.updateSauceName('Pageflow: Main Navigation')
        self.go_url()
        page = pages.HomePage(self.driver)
        page.click_placestab()
        expLoc = page.placesUrl(0)
        page.click_place(0)
        self.assertLocation(expLoc)
        page.click_placestab()
        self.assertLocation('/food/')
        page.get_filters()
        self.assertLocation('/filter/')
        page.click_home()
        self.assertLocation('/')

    def test_home_content(self):
        """Test that the home page id is present"""
        self.updateSauceName('Pageflow: Home Content')
        self.go_url('/')
        page = pages.HomePage(self.driver)
        self.assertEqual(page.pageId, 'page_discover')

    def test_food_content(self):
        """Test that the food page id is present"""
        self.updateSauceName('Pageflow: Food Content')
        self.go_url('/food/')
        page = pages.PlacesPage(self.driver)
        self.assertEqual(page.pageId, 'page_food')

    def test_detail_content(self):
        """Test that the detail page id is correct"""
        self.updateSauceName('Pageflow: Detail Content')
        self.go_url('/food/')
        page = pages.PlacesPage(self.driver)
        page.click_place(0)
        tempUrl = self.driver.current_url.split('/')
        self.assertEqual('page_' + tempUrl[len(tempUrl) - 2], page.pageId)

    def test_filter_content(self):
        """Test that the content on the filter page is correct"""
        self.updateSauceName('Pageflow: Filter Content')
        self.go_url('/filter/')
        page = pages.FilterPage(self.driver)
        self.assertEqual(page.pageId, 'page_filter')
        filterSections = page.getFilterSections()
        self.assertGreater(len(filterSections.keys()), 0)

    def test_foodtab_notclickable(self):
        """Test that once on the food/places page, the places tab
        isn't clickable"""
        self.updateSauceName('Pageflow: Food Tab Not-Clickable')
        self.go_url('/food/')
        page = pages.PlacesPage(self.driver)
        clickable = page.placesTab
        self.assertEqual(clickable.get_attribute('disabled'), 'true')

    def test_discovertab_notclickable(self):
        """Test that once on the discover/home page, the discover tab
        isn't clickable"""
        self.updateSauceName('Pageflow: Discover Tab Not-Clickable')
        self.go_url('/')
        page = pages.HomePage(self.driver)
        clickable = page.discoverTab
        self.assertEqual(clickable.get_attribute('disabled'), 'true')

