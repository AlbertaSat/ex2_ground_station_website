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

class TestLogin(BaseTestCaseFrontEnd):
	"""Test the logging in UI"""

	def test_login_with_correct_creds(self):
		login = self.get_server_url() + "/login"
		self.driver.get(login)

		user_elmt = self.driver.find_element_by_name("username").send_keys("user1")
		password_elm = self.driver.find_element_by_name("password").send_keys("user1")

		time.sleep(1)
		submit_btn = self.driver.find_element_by_name("submit").click()
		time.sleep(2)

		self.assertEqual(self.driver.current_url, self.get_server_url() + "/")

	def test_login_with_incorrect_creds(self):
		login = self.get_server_url() + "/login"
		self.driver.get(login)

		user_elmt = self.driver.find_element_by_name("username").send_keys("fakeuser")
		password_elm = self.driver.find_element_by_name("password").send_keys("fakeuser")

		time.sleep(1)
		submit_btn = self.driver.find_element_by_name("submit").click()
		time.sleep(2)

		# make sure an incorrect message is displayed
		message = self.driver.find_element_by_css_selector("p.MuiTypography-root:nth-child(1)")
		self.assertTrue(message)
		self.assertEqual(message.get_attribute("innerText"), "Username and/or password is incorrect")










