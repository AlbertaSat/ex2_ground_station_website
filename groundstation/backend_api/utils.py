from functools import wraps
from flask import has_app_context, request, g, current_app
import jwt
import datetime
from groundstation import create_app
from groundstation.backend_api.models import Telecommands, FlightSchedules, \
    FlightScheduleCommands, FlightScheduleCommandsArgs, User, Passover
from groundstation import db
import operator
from groundstation.backend_api.models import Communications, Housekeeping
import dateutil.parser


def create_context(function):
    """A decorator to handle cases where backend api calls have no app context,
    namely for when locally using the api, db session must be initiated
    in order to access models and database operation. This is required because flask
    requires an 'application context' to exist in order to work.
    """
    @wraps(function)
    def decorate(*args, **kwargs):
        if not has_app_context():
            app = create_app()

            with app.app_context():
                return function(*args, **kwargs)

        else:
             return function(*args, **kwargs)

    return decorate

def add_telecommand(command_name, num_arguments, is_dangerous):
    """Add a new telecommand to the database
    """
    command = Telecommands(command_name=command_name, num_arguments=num_arguments, is_dangerous=is_dangerous)

    db.session.add(command)
    db.session.commit()
    return command

def add_flight_schedule(creation_date, upload_date, status, execution_time):
    """Add a new flight schedule to the database
    """
    flightschedule = FlightSchedules(
        creation_date=creation_date,
        upload_date=upload_date,
        status=status,
        execution_time=execution_time
    )
    db.session.add(flightschedule)
    db.session.commit()
    return flightschedule

def add_command_to_flightschedule(timestamp, flightschedule_id, command_id):
    """Add a new command to a pre-existing flight schedule
    """
    flightschedule_commands = FlightScheduleCommands(
                                timestamp=timestamp,
                                flightschedule_id=flightschedule_id,
                                command_id=command_id
                            )
    db.session.add(flightschedule_commands)
    db.session.commit()
    return flightschedule_commands

def add_user(username, password, is_admin=False):
    """Add a new user to the database
    """
    user = User(username=username, password=password, is_admin=is_admin)
    db.session.add(user)
    db.session.commit()
    return user

def login_required(f):
    """This is a wrapper which can be used to protect endpoints behind authentication
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """Handles authentication logic before calling the wrapped function
        """

        if current_app.config.get('BYPASS_AUTH'):
            # skip authentication, basically for testing
            g.user = None
            return f(*args, **kwargs)

        if (kwargs.get('local_args') is not None) or (kwargs.get('local_data') is not None):
            # TODO: authentication for local calls
            g.user = None
            return f(*args, **kwargs)

        response_object = {
            'status': None,
            'message': None,
        }
        response_header_object = {}
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            response_object['status'] = 'fail'
            response_object['message'] = 'Provide a valid auth token.'
            response_header_object['WWW-Authenticate'] = 'Bearer'
            return response_object, 401, response_header_object
        auth_token = auth_header.split(" ")[1]
        try:
            user_id = User.decode_auth_token(auth_token)
        except jwt.ExpiredSignatureError:
            response_object['status'] = 'fail'
            response_object['message'] = 'Signature expired. Please log in again.'
            response_header_object['WWW-Authenticate'] = 'Bearer'
            return response_object, 401, response_header_object
        except jwt.InvalidTokenError:
            response_object['status'] = 'fail'
            response_object['message'] = 'Invalid token. Please log in again.'
            response_header_object['WWW-Authenticate'] = 'Bearer'
            return response_object, 401, response_header_object
        user = User.query.filter_by(id=user_id).first()
        if not user:
            response_object['status'] = 'fail'
            response_object['message'] = 'Invalid token. Please log in again.'
            response_header_object['WWW-Authenticate'] = 'Bearer'
            return response_object, 401, response_header_object

        g.user = user
        return f(*args, **kwargs)

    return decorated_function

def add_arg_to_flightschedulecommand(index, argument, flightschedule_command_id):
    """Add a new argument to a pre-existing flightschedule command
    """
    flightschedule_command_arg = FlightScheduleCommandsArgs(
                                    index=index,
                                    argument=argument,
                                    flightschedulecommand_id=flightschedule_command_id
                                )

    db.session.add(flightschedule_command_arg)
    db.session.commit()
    return flightschedule_command_arg

def add_message_to_communications(timestamp, message, receiver, sender):
    """Add a new message to the communications table
    """
    message = Communications(
                        timestamp=timestamp,
                        message=message,
                        receiver=receiver,
                        sender=sender)

    db.session.add(message)
    db.session.commit()
    return message

def add_passover(timestamp):
    """Add a new passover to the database
    """
    passover = Passover(timestamp=timestamp)
    db.session.add(passover)
    db.session.commit()
    return passover


def dynamic_filters_communications(filters):
    """Build a filter dynamically for communications table from query paramaters

    :param dict filters: Dictionary of arg-value pairs

    :returns: a list of filters which can be passed into SQL alchemy filter queries.
    :rtype: list
    """
    filter_ops = []

    for arg, value in filters.items():
        if arg == 'last_id':
            filter_ops.append(operator.gt(Communications.id, value))
        elif arg == 'receiver':
            filter_ops.append(operator.eq(Communications.receiver, value))
        elif arg =='sender':
            filter_ops.append(operator.eq(Communications.sender, value))
        elif arg =='ignore_sender':
            filter_ops.append(operator.ne(Communications.sender, value))
        elif arg == 'max':
            max_comm = Communications.query.order_by(Communications.id.desc()).limit(1).first()
            max_id = -1 if max_comm is None else max_comm.id
            filter_ops.append(operator.eq(Communications.id, max_id))
        else:
            pass

    return filter_ops


def dynamic_filters_housekeeping(filters, ignore_keys=[]):
    """Build a filter dynamically for housekeeping from query paramaters.

    :param werkzeug.datastructures.MultiDict filters: Dictionary of key-value pairs, using a multi dict allows
        users to have filters which overload the keys, ex.) if you want a filter like: ?current_in>5&current_in<10
    :param list ignore_keys: Optional list, any keys in this list will not be used when building the filter

    :returns: a list of filters which can be passed into SQL alchemy filter queries.
    :rtype: list
    """
    filter_ops = []
    # NOTE: cant search channels rn, maybe do later but also not a big concern
    for arg, values in filters.lists():
        # arg will be an attribute of housekeeping like 'temp_1'
        # value will be of form '<operation>-<value>', eg.) 'gt-5'
        if arg in ignore_keys:
            continue

        if not hasattr(Housekeeping, arg):
            return None

        for value in values:
            if '-' in value:
                operation, value = value.split('-', 1)
                if not hasattr(operator, operation):
                    return None

                if arg == 'last_beacon_time':
                    try:
                        value = dateutil.parser.parse(value)
                    except ValueError as e:
                        return None

                filter_ops.append(getattr(operator, operation)(getattr(Housekeeping, arg), value))

    return filter_ops
