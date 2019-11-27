import unittest
from groundstation.tests.base import BaseTestCaseFrontEnd
import time
from selenium import webdriver

class TestHome(BaseTestCaseFrontEnd):
	"""Test the homepage"""

	def test_housekeeping_displays_last_5_entries(self):
		self.assertTrue(self.driver.find_element_by_id("housekeeping-20"))
		self.assertTrue(self.driver.find_element_by_id("housekeeping-19"))
		self.assertTrue(self.driver.find_element_by_id("housekeeping-18"))
		self.assertTrue(self.driver.find_element_by_id("housekeeping-17"))
		self.assertTrue(self.driver.find_element_by_id("housekeeping-16"))

	def test_housekeeping_dialog(self):
		elemt = self.driver.find_element_by_id("housekeeping-20")
		action = webdriver.ActionChains(self.driver)
		action.move_to_element(elemt).click(elemt)
		action.perform()
		time.sleep(1)
		# find an element in the dialog box
		self.assertTrue(self.driver.find_element_by_class_name("jss209"))

	def test_passovers_exist(self):
		self.assertTrue(self.driver.find_element_by_id("passover-2"))
		self.assertTrue(self.driver.find_element_by_id("passover-3"))
		self.assertTrue(self.driver.find_element_by_id("passover-4"))
		self.assertTrue(self.driver.find_element_by_id("passover-5"))




