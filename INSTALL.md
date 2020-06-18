# Installation

## Docker installation

After cloning the repository, make sure to...

```
git submodule init
git submodule update
```

... since the Docker image is still going to need the git modules.

To install the app using [Docker](https://docs.docker.com/get-docker/), `cd` into the project (where the Dockerfile is) and run this to build the docker image:

```
docker build --tag ground_website:latest .
```

*NOTE: depending on your installation, you may need to use* `sudo` *on Docker commands.*

It may take several minutes. Read the Dockerfile to see the build steps. Read the Dockerfile to see the build steps.

To run the docker container:

```
docker run --rm -it --network=host -e FLASK_APP=groundstation/__init__.py -e FLASK_ENV=development -e APP_SETTINGS=groundstation.config.DevelopmentConfig -e SECRET_KEY="\xffY\x8dG\xfbu\x96S\x86\xdfu\x98\xe8S\x9f\x0e\xc6\xde\xb6$\xab:\x9d\x8b" ground_website:latest
```

The `-e`'s are for setting the app's configuration settings; the above arguments configure the app for developing. This means you don't have to run `env.sh`.

To exit the container, type `exit`

The Dockerfile tells docker to start the container with a bash shell, which means that all of the commands will be the same as when you're not running the app in a docker container. [Skip down to the Usage section to read more](#usage)

## Manual installation

**1. Clone the repository**

```
git clone https://github.com/AlbertaSat/ex2_ground_station_website.git && cd ex2_ground_station_website
```

**2. Install OS dependencies.** These are dependencies for PostgreSQL, libCSP, and scheduling tasks.

On Ubuntu:
```
sudo apt install at build-essential wget curl libpq-dev python3-dev gcc-multilib g++-multilib libsocketcan-dev
```

**3. Get git submodules** for the libCSP and the ground station network software.

```
git submodule init
git submodule update
```

**3. Have node & npm installed**, at least version 8. If you don't have node & npm installed, I recommend using the [Node Version Manager](https://github.com/nvm-sh/nvm).

**4. Make sure you have a [Python virtual environment](https://docs.python.org/3/tutorial/venv.html)** installed and active! Please note that with the manual installation you will need to activate it in every terminal that's running the app.

```
source venv/bin/activate
```

**5. Set the environment variables.** These environment variables tell Flask which configuration settings to use. Do this in every terminal window or you'll get errors.

```
source ./env.sh
```

**6. Install pip and npm libraries.** Luckily, we made a script to do all of this for you. Peek inside `update.sh` to see what it's doing.

```
source ./update.sh
```  

**7. Then, to run the app:**

```
flask run
```

Read on to the Usage section to see what else you can do.

## Usage

These commands should be the same regardless of which method of installation you're using.

* `python3 manage.py recreate_db` - erase the database.

* `python3 manage.py seed_db` - seed the database with data.

* `cd groundstation/static && npm run build` - rebuild the React JS frontend.

* `source ./run_comm.sh` - start the comm module. This will enable the app to send data to whatever socket is specified in `comm.py`, probably [ex2_command_handling_demo repo](https://github.com/AlbertaSat/ex2_command_handling_demo), in which case, run that at the same time as well.

* `source ./automate.sh` - run the automation module. It will execute whatever commands are inside `automation.txt`. (Note: the command first has to be specified in `manage.py`, which the app refers to as "telecommands").

* `flask run` - run the app.

* `python3 manage.py test` - run the unit tests.

* `python3 manage.py test frontend_test` - run the GUI frontend tests with Selenium. NOTE: you will need the geckodriver in order to do this. Get it [here](https://github.com/mozilla/geckodriver/releases).

# Extending The Comm Module

The comm module is the main point of interaction between the groundstation application and the satellite. It acts a client to both, and interprets commands sent from the operator to the satellite, and also interprets telemetry sent from the satellite. To extend the comm module, there are 4 files of interest in the root directory of the project:

**comm.py**
Acts a loop for constantly checking commands sent by an operator in the communications table, and sending them to a socket.
If no function is defined for that command, the command string will be sent by default.

**gs_commands.py**
Additional functionality for commands can be implemented here. The return value is what is to be sent, or None if nothing is to be sent. Defined functions must be added to the gs_commands dictionary, with the command string as the key, and the function as the value, in order for comm.py to interpret commands properly.
Handling satellite responses is also implemented here, through the function handle_response(). By default the satellite response is posted to the communication table.

**automation.py**
Automation.py is the script ran at the time of the passover. It first reads from **automation.txt**, a file with commands seperated by newlines. The commands in automation.txt will be posted to the communications table, and sent to the satellite automatically.

The script then loads the next passover time, and utlizes the linux `at` program to schedule the next time automation will run. You will need to install `at`, which can be done with `sudo apt install at` on Ubuntu.

**seed_passovers.sh**
Run this script to schedule automation.py to run at the next passover time. Only necessary to run if no automation is scheduled (ie. passovers have ran out, or for initially setting up automation).
