# Installation
These instructions are for installing and running the application in either [Development Mode](#developer-installation) or in [Production Mode](#production-installation).

Prior to starting, please [install docker](https://www.docker.com/get-started) for your operating system if you have not already as both installations require the use of docker. If these methods don't work on your system, try following these [older instructions](INSTALL-OLD.md) which provide a different set instructions which may work on your machine.

---

## Developer Installation
This installation method is for developers who wish to see their website and API changes live as they develop.

1. Install [NodeJS (LTS)](https://nodejs.org/en/) and [autopep8](https://pypi.org/project/autopep8/) locally on your computer. These two will help autoformat your code when you commit.

2. Clone this repository and enter it by running:
    ```bash
    git clone git@github.com:AlbertaSat/ex2_ground_station_website.git
    cd ex2_ground_station_website
    ```

3. Clone this repository's submodules (ex2_ground_station_software/ and libcsp/) by running:
    ```bash
    git submodule update --init --recursive
    ```

4. Create a copy of `keys-example.sh` and name it `keys.sh`
    ```bash
    cp keys-example.sh keys.sh
    ```
   Feel free to change any of the values inside `keys.sh` but their default values works fine. Note that `SLACK_TOKEN` is used in `automation.py` as a way of notifying users through Slack when a satellite passover occurs. Information on using the Slack API can be found [here](https://api.slack.com/).

5. Start the development environment by running:
    ```bash
    docker-compose up
    ```
   It may take a while for the first time but subsequent runs will be much quicker.

6. Visit [http://localhost:8000](http://localhost:8000) to view the webpage

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

### Command Responses
The website's [comm.py](comm.py) script communicates with the database and with [ex2_ground_station_software](https://github.com/AlbertaSat/ex2_ground_station_software) in order to communicate with the satellite. In order to recieve command responses:

1. Open a seperate terminal inside the website container by running:
    ```bash
    docker exec -it ex2_ground_station_website_web_1 bash
    ```

2. Build libcsp by running `./build_libcsp.sh`. This only needs to be done whenever the [libcsp](https://github.com/AlbertaSat/libcsp) submodule or the script itself updated.

3. Run `comm.py` with the appropriate command-line arguments according to [ex2_ground_station_software](https://github.com/AlbertaSat/ex2_ground_station_software/blob/cb4db3a0ff24fdd61973888c864b429ad4995261/src/groundStation/groundStation.py#L365)

   If you want to test responses **without being connected to an OBC**, run:
   ```bash
   python3 comm.py -I dummy
   ```

   If you have GNURadio open, run:
   ```bash
   python3 comm.py -I sdr -u
   ```
   the command **outside** of the Docker container, and on the host PC that is running GNURadio.

4. You will then be prompted with:
    ```
    Would like to communicate with the satellite simulator (if not, the program will attempt to communicate with the satellite) [Y/n]:
    ```
    Respond with 'n' and let the script run in the background.

---

## Production Installation
These instructions assume that the production server is running Ubuntu 20.04 with docker and docker-compose installed. Follow these instructions if you want to deploy the website on a web server.

1. Clone this repository and enter it:
    ```bash
    git clone git@github.com:AlbertaSat/ex2_ground_station_website.git
    cd ex2_ground_station_website
    ```

2. Clone this repository's submodules (ex2_ground_station_software/ and libcsp/) by running:
    ```bash
    git submodule update --init --recursive
    ```

3. Create a copy of `keys-example.sh` and name it `keys.sh`
    ```bash
    cp keys-example.sh keys.sh
    ```
   Feel free to change any of the values inside `keys.sh`, particularly `POSTGRES_USER` and `POSTGRES_PASSWORD` which act as the credentials for the database and `SECRET_KEY` which is used for authentication. These three environment variables should be kept secure.

   Note that `SLACK_TOKEN` is used in `automation.py` as a way of notifying users through Slack when a satellite passover occurs. Information on using the Slack API can be found [here](https://api.slack.com/).

4. Set the system's environment variables by running:
    ```bash
    source ./env.sh
    source ./keys.sh
    ```

5. Inside the repo, create a folder called `db_backups` and give initialize its permissions as followed:
    ```bash
    mkdir db_backups
    sudo chown -R 999:999 db_backups/
    ```

6. Create a Python virtual environment and install the website's Python dependencies by running:
    ```bash
    python3 -m venv .venv # Creates python virtual environment in .venv/
    source .venv/bin/activate # Activates virtual environment
    pip install -r requirements.txt # Installs dependencies
    ```

7. Start the production environment by running:
    ```bash
    sudo -E docker-compose -f docker-compose.prod.yml up -d
    ```
   To view the logs of the production server, run the following in a separate terminal window:
   ```bash
   sudo docker-compose logs -f -t
   ```

8. Ensure that port 80 is port-forwarded on the web server and you can now access the website by visiting [http://localhost](http://localhost) if using a browser on the webserver or by visiting `http://<server ip here>` on a different device

### Updating Production
When there is a new update to master, follow these instructions to update the server:

1. Shutdown the server by running:
    ```bash
    sudo docker-compose down --remove-orphans
    ```

2. Pull the latest changes with `git pull`

3. Reopen the server by running:
    ```bash
    source ./env.sh
    source ./keys.sh
    sudo -E docker-compose -f docker-compose.prod.yml up -d
    ```

4. If there were any changes to the database schema (ie. new table, column, etc.) open a bash terminal inside the website docker container with:
    ```bash
    sudo docker exec -it ex2_ground_station_website_web_1 bash
    ```

    Then run the following commands to update the database schema without deleting existing rows:
    ```bash
    flask db migrate
    flask db upgrade
    ```

### Accessing the Database
The website uses a PostgreSQL database to store its data. To view all the tables and their entries, you can either use a command line tool like [psql](https://www.postgresql.org/download/) or a GUI tool like [DBeaver](https://dbeaver.io).

For security purposes (for now), these commands only work when ran on the server computer itself locally.

With **psql**, you can connect to the database by runnning the following command in a separate terminal window:
```
psql -U <POSTGRES_USER> -h localhost -d ex2_gs -W
```
which will then prompts you for the database password.

With **DBeaver**, [create a new PostgreSQL database connection](https://github.com/dbeaver/dbeaver/wiki/Create-Connection) and set these fields to:
```
Host: localhost
Database: ex2_gs
Username: <POSTGRES_USER>
Password: <POSTGRES_PASSWORD>
```

### Restoring a Database Backup
A database backup is scheduled to be created daily and backups can be found in the `db_backups/` folder.
To restore a backup, follow these steps in the server's terminal:

1. Open a bash terminal inside the website container by running:
    ```bash
    sudo docker exec -it ex2_ground_station_webste_web_1 bash
    ```

2. Run `python3 manage.py recreate_db`

   **WARNING:** This will **_completely wipe_** the database  so that a backup can be restored. Please run it with caution!

3. Restore the a backup by running:
    ```bash
    zcat db_backups/<path to backup file> | psql -U <POSTGRES_USER> -h db -d ex2_gs -W
    ```
   which will then prompt you for the database password.

---

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
