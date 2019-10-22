import sys
import unittest
from datetime import datetime
import json

from flask.cli import FlaskGroup

from groundstation import create_app, db
from groundstation.backend_api.models import User, Housekeeping
from groundstation.tests.utils import fakeHousekeepingAsDict
from groundstation.backend_api.housekeeping import HousekeepingLogList

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

@cli.command('seed_db')
def seed_db():
    timestamp = datetime.fromtimestamp(1570749472)
    housekeepingData = fakeHousekeepingAsDict(timestamp)

    housekeeping = Housekeeping(**housekeepingData)
    db.session.add(housekeeping)
    db.session.commit()


if __name__ == '__main__':
    cli()
