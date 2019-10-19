from flask import has_app_context
from groundstation import create_app


def create_context(function):
    def decorate(*args, **kwargs):
        if not has_app_context():
            app = create_app()

            with app.app_context():
                return function(args, **kwargs)

        else:
             return function(args, **kwargs) 

    return decorate


