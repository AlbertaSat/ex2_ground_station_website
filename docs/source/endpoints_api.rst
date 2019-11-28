RESTful endpoints Reference
=======================================
These are the endpoints that essentially govern all user interaction/communication. The endpoints are
callable internally through python, which allows for 'local' clients (such as the automator and comm module) to
make api calls. These endpoints are also 'exposed' to the outside world via flask, which allows external clients to
make api requests (such as the react app client).

Authentication
--------------

.. automodule:: groundstation.backend_api.auth
    :members:

Communications
--------------

.. automodule:: groundstation.backend_api.communications
    :members:

Flightschedule
--------------

.. automodule:: groundstation.backend_api.flightschedule
    :members:

Housekeeping
------------

.. automodule:: groundstation.backend_api.housekeeping
    :members:

Passovers
---------

.. automodule:: groundstation.backend_api.passover
    :members:

Telecommands
------------

.. automodule:: groundstation.backend_api.telecommand
    :members:

Users
-----

.. automodule:: groundstation.backend_api.user
    :members:
