import unittest
from myapp.dao import User

class UserModelTestCase(unittest.TestCase): 
	def test_password_setter(self):
		my_user = User(username='vteste10', email_address='vteste10@t.com', password='vteste10')
		self.assertTrue(my_user.password_hash is not None)

	def test_password_verification(self):
		my_user = User(username='vteste10', email_address='vteste10@t.com', password='vteste10')
		self.assertTrue(my_user.check_password_correction('vteste10') )
		self.assertFalse(my_user.check_password_correction('vteste11') )

loader = unittest.TestLoader()
suite1 = loader.discover('myapp', pattern='tests*.py')
unittest.TextTestRunner(verbosity=2).run(suite1)

# to run via python3 interpreter
# exec(open('/Users/armandosoaressousa/git/sysuploads/myapp/tests.py').read() )


