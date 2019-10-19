from flask import has_app_context
from groundstation import create_app


# a decorator to handle cases where backend api calls have no app context
# namely for when locally using the api, db session must be initiated 
# in order to access models and database operation
def create_context(function):
    def decorate(*args, **kwargs):
        if not has_app_context():
            app = create_app()

            with app.app_context():
                return function(args, **kwargs)

        else:
             return function(args, **kwargs) 

    return decorate
