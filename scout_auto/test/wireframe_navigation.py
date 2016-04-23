#!/usr/bin/python
"""
Tests the Wireframe of scout, this particular file incorperates
mock data and tests the navigation incorporating that data
"""

import os
import sys
import os.path
from scout_auto import pages

from selenium import webdriver
from django.test import LiveServerTestCase
from django.conf import settings
from scout_auto.scout_testing import ScoutTest

class AdvNavigationTest(ScoutTest):

    def go_url(self, urlsuffix = ''):
        self.driver.get(self.baseurl + urlsuffix)

    def test_breakfast(self):
        """SCOUT-70, testing to see if user can bring up list of b-fast
        places by clicking view more results"""

        self.updateSauceName("Wireframe: Home to Filter Breakfast")
        self.go_url()
        page = pages.HomePage(self.driver)
        page.click_results('breakfast')
        self.assertEqual('page_food', page.pageId)
        self.assertEqual(page.filterBy.text, "Open Period")
        self.assertEqual(page.placesCount.text, "4")

    def test_coffee(self):
        """SCOUT-71, testing to see if user can bring up list of coffee
        places by clicking view more results"""

        self.updateSauceName("Wireframe: Home to Filter Coffee")
        self.go_url()
        page = pages.HomePage(self.driver)
        page.click_results('coffee')
        self.assertEqual('page_food', page.pageId)
        self.assertEqual(page.filterBy.text, "Food Served")
        self.assertEqual(page.placesCount.text, "2")

    def test_open_nearby(self):
        """SCOUT-72, testing to see if user can bring up list of
        places open nearby by clicking view more results"""

        self.updateSauceName("Wireframe: Home to Filter Open Nearby")
        self.go_url()
        page = pages.HomePage(self.driver)
        page.click_results('open')
        self.assertEqual('page_food', page.pageId)
        self.assertEqual(page.filterBy.text, "Open Now")
        self.assertEqual(page.placesCount.text, "8")

    def test_late(self):
        """SCOUT-73, testing to see if user can bring up list of
        places open late by clicking view more results"""

        self.updateSauceName("Wireframe: Home to Filter Open Late")
        self.go_url()
        page = pages.HomePage(self.driver)
        page.click_results('late')
        self.assertEqual('page_food', page.pageId)
        self.assertEqual(page.filterBy.text, "Open Period")
        self.assertEqual(page.placesCount.text, "2")

    def test_details(self):
        """SCOUT-74 testing to see if user can click on a place and
        then see more details from the home page"""

        self.updateSauceName("Wireframe: Home to Details")
        self.go_url()
        page = pages.HomePage(self.driver)
        page.click_place('open', 2)
        tempHref = self.driver.current_url.split('/')
        self.assertIn('page_' + tempHref[len(tempHref) - 2], page.pageId)
        self.assertEqual(page.foodName.text, "Banh & Naan, Husky Den")
        self.assertEqual(page.foodType.text, "FOOD COURT")

    def test_details2(self):
        """SCOUT-75 testing to see if user can click on a place and
        then see more details from the "places" page"""

        self.updateSauceName("Wireframe: Places to Details")
        self.go_url('/food/')
        page = pages.PlacesPage(self.driver)
        page.click_place(3)
        tempHref = self.driver.current_url.split('/')
        self.assertIn('page_' + tempHref[len(tempHref) - 2], page.pageId)
        self.assertEqual(page.foodName.text, "Banh & Naan, Husky Den")
        self.assertEqual(page.foodType.text, "FOOD COURT")
