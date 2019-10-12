import unittest

from groundstation.tests.base import BaseTestCase

class TestGroundstation(BaseTestCase):
	"""Test the testing"""
	def testTesting(self):
		self.assertEqual(200, 200)
	
	def test_interface(self):
		# Don't know how to write this test TBH
		pass



if __name__ == '__main__':
    unittest.main()