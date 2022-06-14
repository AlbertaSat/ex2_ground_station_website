# Installation
These instructions are for installing and running the application in either [Development Mode](#developer-installation) or in [Production Mode](#production-installation).

Prior to starting, please [install docker](https://www.docker.com/get-started) for your operating system if you have not already as both installations require the use of docker. If these methods don't work on your system, try following these [older instructions](INSTALL-OLD.md) which provide a different set instructions which may work on your machine.

---

## Developer Installation
This installation method is for developers who wish to see their website and API changes live as they develop.

1. Clone this repository
    ```bash
    git clone git@github.com:AlbertaSat/ex2_ground_station_website.git
    cd ex2_ground_station_website
    ```

2. Create a copy of `keys-example.sh` and name it `keys.sh`
    ```bash
    cp keys-example.sh keys.sh
    ```
   Feel free to change any of the values inside `keys.sh` but their default values works fine. Note that `SLACK_TOKEN` is used in `automation.py` as a way of notifying users through Slack when a satellite passover occurs. Information on using the Slack API can be found [here](https://api.slack.com/).

3. Start the development environment using:
    ```bash
    docker-compose up
    ```
   It may take a while for the first time but subsequent runs will be much quicker.

4. Visit [http://localhost:8000](http://localhost:8000) to view the webpage

   Note that on Safari and iOS, timestamps render improperly so it is recommended that you use a Chromium browser (Chrome, Edge, etc.) or Firefox.

   Whenever you make a change to the website code (inside `groundstation/static/js`), you would need to hard refresh the page with `Ctrl+Shift+R` on Windows/Linux or `Command+Shift+R` on Mac to empty the cache.

### Accessing the Database
The website uses a PostgreSQL database to store its data. To view all the tables and their entries, you can either use a command line tool like [psql](https://www.postgresql.org/download/) or a GUI tool like [DBeaver](https://dbeaver.io).

With **psql**, you can connect to the database by runnning the following command in a separate terminal window:
```bash
psql postgres://postgres:postgres@localhost:5432/ex2_gs
```

With **DBeaver**, [create a new PostgreSQL database connection](https://github.com/dbeaver/dbeaver/wiki/Create-Connection) and set these fields to:
```
Host: localhost
Database: ex2_gs
Username: postgres
Password: postgres
```

# Useful Commands

These commands should be the same regardless of which method of installation you're using.

* `python3 manage.py recreate_db` - delete the database and create a new empty one.

* `python3 manage.py seed_db` - seed the database with sample data.

* `cd groundstation/static && npm run build` - build the React JS frontend.

* `source ./env.sh` - set the environment variables for Flask's config. Without it you'll get weird SQLAlchemy errors.

* `source ./run_comm.sh` - start the comm module. This will enable the app to send data to whatever socket is specified in `comm.py`. For example, [ex2_services](https://github.com/AlbertaSat/ex2_services).

* `source ./automate.sh` - run the automation module. It will automatically send whatever commands are inside `automation.txt` to the socket. (Note: the commands first have to be specified in `manage.py`, which the app refers to as "telecommands"). Not necessary for testing.

* `flask run` - run the app.

* `python3 manage.py test` - run the unit tests.

* `python3 manage.py test frontend_test` - run the GUI frontend tests with Selenium. Please note that you will need to install the appropriate driver [here](https://selenium-python.readthedocs.io/installation.html#drivers).

* `python3 manage.py test groundstation_test` - run ground station integration testing. Please note that you will need to have built libcsp in this repo's submodule and have set the appropriate env variables with `source ./env.sh`
