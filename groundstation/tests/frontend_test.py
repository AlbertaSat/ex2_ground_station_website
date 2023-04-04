import unittest
from groundstation.tests.base import BaseTestCaseFrontEnd
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

"""Note these tests must be run manually by python3 manage.py test frontend_test
server must also be running, in addition to a newly seeded database in order to pass
"""


class TestHome(BaseTestCaseFrontEnd):
	"""Test the homepage"""

	def test_housekeeping_displays_last_5_entries(self):
		self.assertTrue(self.driver.find_element_by_id("housekeeping-60"))
		self.assertTrue(self.driver.find_element_by_id("housekeeping-59"))
		self.assertTrue(self.driver.find_element_by_id("housekeeping-58"))
		self.assertTrue(self.driver.find_element_by_id("housekeeping-58"))
		self.assertTrue(self.driver.find_element_by_id("housekeeping-56"))

	def test_housekeeping_dialog(self):
		elemt = self.driver.find_element_by_id("housekeeping-60")
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


class TestHousekeepingPage(BaseTestCaseFrontEnd):
	""""Test the housekeeping page"""

	"""The date picker is too hard to simulate picking a date, however we cab pick an impossible date range
		(now-now) and ensire this returns no logs
	"""
	def test_date_filter_no_matches(self):
		housekeeping = self.get_server_url() + "/housekeeping"
		self.driver.get(housekeeping)

		filter_btn = self.driver.find_element_by_name("filter")

		self.driver.find_element_by_name("startdate").click()
		time.sleep(1)
		self.driver.find_element_by_css_selector("button.MuiButton-textPrimary:nth-child(3)").click()
		time.sleep(1)
		self.driver.find_element_by_name("enddate").click()
		time.sleep(1)
		self.driver.find_element_by_css_selector("button.MuiButton-textPrimary:nth-child(3)").click()
		time.sleep(1)

		filter_btn.click()

		time.sleep(1)

		entries = self.driver.find_elements_by_css_selector("th.MuiTableCell-root")
		self.assertEqual(len(entries), 0)

class TestLiveCommandsPage(BaseTestCaseFrontEnd):
	"""Test the live commands page"""
	def test_input_command(self):
		login = self.get_server_url() + "/login"
		self.driver.get(login)

		user_elmt = self.driver.find_element_by_name("username").send_keys("user1")
		password_elm = self.driver.find_element_by_name("password").send_keys("user1")

		time.sleep(1)
		submit_btn = self.driver.find_element_by_name("submit").click()
		time.sleep(1)

		live_commands = self.get_server_url() + "/livecommands"
		self.driver.get(live_commands)
		time.sleep(1)

		elemt = self.driver.find_element_by_id("user-input-textbox")
		elemt.click()
		elemt.send_keys("ping")
		time.sleep(1)
		elemt.send_keys(Keys.ENTER)
		time.sleep(1)

		div = self.driver.find_element_by_css_selector("div.MuiPaper-root > div:nth-child(2) > div:nth-child(1)")
		self.assertTrue(div)

		message_string = "div.MuiPaper-root > div:nth-child(2) > div:nth-child(1) > p:nth-child(2)"
		message = self.driver.find_element_by_css_selector(message_string).get_attribute("innerText")
		self.assertIn("ping", message)

	def test_invalid_command(self):
		"""Test that an an invalid command isnt sent"""
		login = self.get_server_url() + "/login"
		self.driver.get(login)

		user_elmt = self.driver.find_element_by_name("username").send_keys("user1")
		password_elm = self.driver.find_element_by_name("password").send_keys("user1")

		time.sleep(1)
		submit_btn = self.driver.find_element_by_name("submit").click()
		time.sleep(1)

		live_commands = self.get_server_url() + "/livecommands"
		self.driver.get(live_commands)
		time.sleep(1)

		elemt = self.driver.find_element_by_id("user-input-textbox")
		elemt.click()
		elemt.send_keys("pong")
		time.sleep(1)
		elemt.send_keys(Keys.ENTER)
		time.sleep(1)

		message_string = "div.MuiPaper-root > div:nth-child(2) > div:nth-child(1) > p:nth-child(2)"
		div = self.driver.find_elements_by_css_selector(message_string)
		self.assertEqual(len(div), 0)

class TestLogPage(BaseTestCaseFrontEnd):
	"""Test the logs page"""
	def test_logs_exist(self):
		login = self.get_server_url() + "/login"
		self.driver.get(login)

		user_elmt = self.driver.find_element_by_name("username").send_keys("user1")
		password_elm = self.driver.find_element_by_name("password").send_keys("user1")

		time.sleep(1)
		submit_btn = self.driver.find_element_by_name("submit").click()
		time.sleep(1)

		logs = self.get_server_url() + "/logs"
		self.driver.get(logs)

		time.sleep(1)
		message_string = "div.MuiPaper-root > div:nth-child(1) > div:nth-child(1) > p:nth-child(2)"
		message = self.driver.find_element_by_css_selector(message_string).get_attribute("innerText")
		self.assertIn("ping", message)

class TestFlightScheduleBuilder(BaseTestCaseFrontEnd):
	"""Test the flightschedule builder"""
	def test_open_builder(self):
		login = self.get_server_url() + "/login"
		self.driver.get(login)

		user_elmt = self.driver.find_element_by_name("username").send_keys("user1")
		password_elm = self.driver.find_element_by_name("password").send_keys("user1")

		time.sleep(1)
		submit_btn = self.driver.find_element_by_name("submit").click()
		time.sleep(1)

		flightschedule = self.get_server_url() + "/flightschedule"
		self.driver.get(flightschedule)

		self.driver.find_element_by_css_selector(".MuiFab-root").click()
		time.sleep(1)

		header = self.driver.find_element_by_css_selector("h2.MuiTypography-root")
		self.assertTrue(header)
		self.assertEqual(header.get_attribute("innerText"), "Add/Edit Flightschedule")

	def test_create_flightschedule(self):
		"""Test building a flight schedule"""
		login = self.get_server_url() + "/login"
		self.driver.get(login)

		user_elmt = self.driver.find_element_by_name("username").send_keys("user1")
		password_elm = self.driver.find_element_by_name("password").send_keys("user1")

		time.sleep(1)
		submit_btn = self.driver.find_element_by_name("submit").click()
		time.sleep(1)

		flightschedule = self.get_server_url() + "/flightschedule"
		self.driver.get(flightschedule)

		self.driver.find_element_by_css_selector(".MuiFab-root").click()
		time.sleep(1)

		execution_inp = ".MuiGrid-grid-xs-5 > form:nth-child(1) > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)"
		self.driver.find_element_by_css_selector(execution_inp).click()
		time.sleep(1)

		self.driver.find_element_by_css_selector("div.MuiDialogActions-root:nth-child(2) > button:nth-child(2)").click()
		time.sleep(1)

		self.driver.find_element_by_css_selector(".basic-single").click()
		time.sleep(1)

		menu = self.driver.find_element_by_id("react-select-2-input")
		menu.send_keys("ping")
		time.sleep(1)
		menu.send_keys(Keys.ENTER)
		time.sleep(1)

		timestamp_string = "table.MuiTable-root:nth-child(3) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > form:nth-child(1) > div:nth-child(1) > div:nth-child(2)"
		timestamp = self.driver.find_element_by_css_selector(timestamp_string)
		timestamp.click()
		time.sleep(1)
		self.driver.find_element_by_css_selector("#outlined-basic").send_keys("300")
		time.sleep(1)

		self.driver.find_element_by_css_selector("button.MuiButton-textPrimary:nth-child(2)").click()
		time.sleep(1)

		div_str = "div.MuiExpansionPanel-root"
		fs_str = "div.MuiPaper-root:nth-child(2) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > th:nth-child(1) > div:nth-child(1)"
		self.assertEqual(self.driver.find_element_by_css_selector(fs_str).get_attribute("innerText"),
			"Flight Schedule #2"
		)
		self.assertEqual(len(self.driver.find_elements_by_css_selector(div_str)), 2)

	def test_edit_flightschedule(self):
		login = self.get_server_url() + "/login"
		self.driver.get(login)

		user_elmt = self.driver.find_element_by_name("username").send_keys("user1")
		password_elm = self.driver.find_element_by_name("password").send_keys("user1")

		time.sleep(1)
		submit_btn = self.driver.find_element_by_name("submit").click()
		time.sleep(1)

		flightschedule = self.get_server_url() + "/flightschedule"
		self.driver.get(flightschedule)

		time.sleep(3)

		btn_str = "div.MuiPaper-root:nth-child(2) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > div:nth-child(1) > button:nth-child(1)"
		self.driver.find_element_by_css_selector(btn_str).click()
		time.sleep(1)


		self.driver.find_element_by_css_selector(".basic-single").click()
		time.sleep(1)

		menu = self.driver.find_element_by_id("react-select-2-input")
		menu.send_keys("get-hk")
		time.sleep(1)
		menu.send_keys(Keys.ENTER)
		time.sleep(1)

		self.driver.find_element_by_css_selector("button.MuiButton-textPrimary:nth-child(2)").click()
		time.sleep(1)

		self.driver.find_element_by_css_selector("div.MuiPaper-root:nth-child(2) > div:nth-child(1)").click()
		time.sleep(2)

		elmt = ".MuiCollapse-entered > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(1) > th:nth-child(1)"
		name = self.driver.find_element_by_css_selector(elmt).get_attribute("innerText")

		self.assertEqual(name, "get-hk")





















