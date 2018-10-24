#!/usr/bin/python
"""
Tests the filter functionality, using the mock data
"""

import sys
import unittest
import copy
import os

from selenium import webdriver
from django.test import Client
from django.conf import settings

from scout_auto.scout_testing import ScoutTest
from scout_auto import pages


class FilterTest(ScoutTest):
    """Filter Tests set for scout"""

    def go_url(self, urlsuffix=''):
        """Has the driver go to the given URL"""
        self.driver.get(self.baseurl + urlsuffix)


    def test_filter_set2(self):
        """SCOUT-82 Filters out the foods that accept cash and serve American
        cuisine asserts the right data of places show up"""
        self.updateSauceName('UI: Filter Cash + American')
        self.go_url('/filter/')
        page = pages.FilterPage(self.driver)
        page.setFilters({
            'PAYMENT ACCEPTED': {'s_pay_cash': True},
            'CUISINE': {'s_cuisine_american': True}
        })
        page.search()
        self.assertEqual(page.placesNum, 2)
        self.assertEqual(page.filterBy.text, 'Payment Accepted, Cuisine')

    def test_filter_set3(self):
        """SCOUT-83 Filters out the food truck, asserts the right data shows up"""
        self.updateSauceName('UI: Filter Food Truck')
        self.go_url('/filter/')
        page = pages.FilterPage(self.driver)
        page.setFilters({'TYPE': {'food_truck': True}})
        page.search()
        self.assertEqual(page.placesNum, 1)
        self.assertEqual(page.filterBy.text, 'Restaurant Type')
        self.assertEqual(page.placesName(0).text, 'Truck of Food')


    def test_filter_set4(self):
        """SCOUT-84 Filters out the foods that are open now, accept husky/master
        cards and serves burgers"""
        self.updateSauceName('UI: Open + HuskyCard + MasterCard + Burgers')
        self.go_url('/filter/')
        page = pages.FilterPage(self.driver)
        page.setFilters({
            'PAYMENT ACCEPTED': {'s_pay_husky': True, 's_pay_mastercard': True},
            'FOOD SERVED': {'s_food_burgers': True},
            'OPEN PERIOD': {'open_now': True}
        })
        page.search()
        self.assertEqual(page.filterBy.text, 'Payment Accepted, Food Served, Open Now')
        self.assertEqual(page.placesNum, 3)

    def test_filter_set5(self):
        """SCOUT-85 Filters out the places that are in the Seattle Campus,
        Cafes, and open for breakfast"""
        self.updateSauceName('UI: Seattle + Cafe + Breakfast')
        self.go_url('/filter/')
        page = pages.FilterPage(self.driver)
        page.setFilters({
            'CAMPUS': {'seattle': True},
            'TYPE': {'cafe': True},
            'OPEN PERIOD': {'breakfast': True}
        })
        page.search()
        self.assertEqual(page.filterBy.text, 'Campus, Restaurant Type, Open Period')
        self.assertEqual(page.placesNum, 2)

    def test_filter_reset_places_page(self):
        """SCOUT-86 Filters out places that accept cash, then resets filters on
        the places page"""
        self.updateSauceName('UI: Reset Filter on Places Page')
        self.go_url('/filter/')
        page = pages.FilterPage(self.driver)
        page.setFilters({'PAYMENT ACCEPTED': {'s_pay_cash': True}})
        page.search()
        self.assertEqual(page.placesNum, 4)
        self.assertEqual(page.filterBy.text, 'Payment Accepted')
        page.reset_filters()
        self.assertEqual(page.placesNum, 8)
        self.assertEqual(page.filterBy.text, '--')

    def test_filter_reset_filter_page(self):
        """SCOUT-87 Filters out places that accept cash and serve American
        cuisine, then resets on the filter page and filters out places with
        just cash and searches"""
        self.updateSauceName('UI: Reset Filters on Filter Page')
        self.go_url('/filter/')
        page = pages.FilterPage(self.driver)
        page.setFilters({
            'PAYMENT ACCEPTED': {'s_pay_cash': True},
            'CUISINE': {'s_cuisine_american': True}
        })
        page.reset()
        page.get_filters()
        page.setFilters({'PAYMENT ACCEPTED': {'s_pay_cash': True}})
        page.search()
        self.assertEqual(page.placesNum, 4)
        self.assertEqual(page.filterBy.text, 'Payment Accepted')

    def test_filter_remembered(self):
        """SCOUT-88 Filters out the places that accept cash, searches, returns
        to filter page to add a filter of American Cuisine, searches (cash
        should still be checked off)"""
        self.updateSauceName('UI: Filter Remembered')
        self.go_url('/filter/')
        page = pages.FilterPage(self.driver)
        page.setFilters({'PAYMENT ACCEPTED': {'s_pay_cash': True}})
        page.search()
        page.click_home()
        page.click_placestab()
        self.assertEqual(page.placesNum, 4)
        self.assertEqual(page.filterBy.text, 'Payment Accepted')
        page.get_filters()
        page.setFilters({'CUISINE': {'s_cuisine_american': True}})
        page.search()
        self.assertEqual(page.placesNum, 2)
        self.assertEqual(page.filterBy.text, 'Payment Accepted, Cuisine')

    def test_filter_vs_viewmoreresults(self):
        """SCOUT-89 Filters out the places that accept cash, then goes to the
        home page and clicks on a preset filter (breakfast), then returns to
        the filter page to see if the original cash filter is present"""
        self.updateSauceName('UI: Filter vs. View More Results')
        self.go_url('/filter/')
        page = pages.FilterPage(self.driver)
        page.setFilters({'PAYMENT ACCEPTED': {'s_pay_cash': True}})
        page.search()
        page.click_home()
        page.click_results('breakfast')
        page.get_filters()
        page.search()
        self.assertEqual(page.filterBy.text, 'Payment Accepted')
