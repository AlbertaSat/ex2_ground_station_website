import sys
import unittest

from flask.cli import FlaskGroup

from groundstation import create_app, db
from groundstation.api.models import User

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command('recreate_db')
def recreate_db():
	"""Recreate the database"""
	db.drop_all()
	db.create_all()
	db.session.commit()

@cli.command()
def test():
	"""Runs all tests in tests folder"""
	tests = unittest.TestLoader().discover('groundstation/tests', pattern='test*.py')
	result = unittest.TextTestRunner(verbosity=2).run(tests)
	if result.wasSuccessful():
		return 0
	sys.exit(result)

if __name__ == '__main__':
	cli()
