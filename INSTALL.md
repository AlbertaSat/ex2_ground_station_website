# Installation

These instructions are for installing and running the application in development mode on a development machine.

## Docker installation

After cloning the repository, make sure to update the submodules. These are for libCSP and the ground station network software.

```
git submodule init
git submodule update
```

The Docker image is still going to need the git modules. Read the Dockerfile to see what exactly is happening.

To build the docker image:

```
sudo docker build --tag ground_website:latest .
```

To run the docker container:

```
docker run --rm -it --network=host -e FLASK_APP=groundstation/__init__.py -e FLASK_ENV=development -e APP_SETTINGS=groundstation.config.DevelopmentConfig -e SECRET_KEY="\xffY\x8dG\xfbu\x96S\x86\xdfu\x98\xe8S\x9f\x0e\xc6\xde\xb6$\xab:\x9d\x8b" ground_website:latest
```

Using `-e` lets us pass environment variables to the docker container.

To exit the container, type `exit`

The Dockerfile tells docker to start the container in a bash shell, which means that all of the commands in [Usage](#usage) will be the same.

## Manual installation

Ubuntu dependencies for PostgreSQL, libCSP, and scheduling tasks:

```
sudo apt-get install at build-essential wget curl libpq-dev python3-dev gcc-multilib g++-multilib libsocketcan-dev
```

Don't forget to get the latest version of the git submodules:
```
git submodule update --init --recursive --remote --merge
```

To run the app's frontend (i.e. in your web browser), you will need node & npm -- at least version 8. I recommend using the [Node Version Manager](https://github.com/nvm-sh/nvm).

Make sure you have a [Python virtual environment](https://docs.python.org/3/tutorial/venv.html) installed and active! To do this navigate to the root project directory and run the following commands:
```
python3 -m venv env
source env/bin/activate
```

Set the environment variables. These environment variables tell Flask which configuration settings to use. Do this in every terminal window or you'll get database errors.

```
source ./env.sh
```

Install pip and npm libraries by running `update.sh`:

```
source ./update.sh
```  

**Then, to run the app:**

```
flask run
```

## Usage

These commands should be the same regardless of which method of installation you're using.

* `python3 manage.py recreate_db` - delete the database and create a new empty one.

* `python3 manage.py seed_db` - seed the database with sample data.

* `cd groundstation/static && npm run build` - build the React JS frontend.

* `source ./env.sh` - set the environment variables for Flask's config. Without it you'll get weird SQLAlchemy errors.

* `source ./run_comm.sh` - start the comm module. This will enable the app to send data to whatever socket is specified in `comm.py`. For example, [ex2_services](https://github.com/AlbertaSat/ex2_services).

* `source ./automate.sh` - run the automation module. It will automatically send whatever commands are inside `automation.txt` to the socket. (Note: the commands first have to be specified in `manage.py`, which the app refers to as "telecommands"). Not necessary for testing.

* `flask run` - run the app.

* `python3 manage.py test` - run the unit tests.

* `python3 manage.py test frontend_test` - run the GUI frontend tests with Selenium. NOTE: you will need the geckodriver in order to do this. Get it [here](https://github.com/mozilla/geckodriver/releases).

# The Comm Module - comm.py

The comm module is the main point of interaction between this application and the satellite. It acts a client to both, and interprets commands sent from the operator to the satellite, and also interprets telemetry sent from the satellite. To extend the comm module, there are 4 files of interest in the root directory of the project:

**comm.py**
Acts a loop for constantly checking commands sent by an operator in the communications table, and sending them to a socket.  
If no function is defined for that command, the command string will be sent by default.

**gs_commands.py**
Additional functionality for commands can be implemented here. The return value is what is to be sent, or None if nothing is to be sent. Defined functions must be added to the gs_commands dictionary, with the command string as the key, and the function as the value, in order for comm.py to interpret commands properly.
Handling satellite responses is also implemented here, through the function handle_response(). By default the satellite response is posted to the communication table.

**automation.py**
Automation.py is the script ran at the time of the passover. It first reads from **automation.txt**, a file with commands seperated by newlines. The commands in automation.txt will be posted to the communications table, and sent to the satellite automatically.

The script then loads the next passover time, and utlizes the linux `at` program to schedule the next time automation will run. You will need to install `at`, which can be done with `sudo apt-get install at` on Ubuntu.

**seed_passovers.sh**
Run this script to schedule automation.py to run at the next passover time. Only necessary to run if no automation is scheduled (ie. passovers have ran out, or for initially setting up automation).
