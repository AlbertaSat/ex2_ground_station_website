# Installation
These instructions are for installing and running the application in development mode on a development machine. There are two installation methods below, one uses [docker](https://www.docker.com/) and the other is manual. The docker installation is the recommended method.

## Docker Installation - website and satellite simulator (recommended)
The docker installation methods below are compatible with any operating system that is supported by [docker](https://www.docker.com/). If you are just looking to use the web app and don't plan on making any changes to the source code, then choose the `User Installation` method below. Otherwise, choose the `Developer Installation` method below. 

Prior to starting, please [install docker](https://www.docker.com/get-started) for your operating system if you have not already.

### User Installation
This installation method will install a docker image that will be run as a container and used to host the ground station web app.

All you need to do is open a terminal instance on your operating system and enter the following commands:

```bash
docker pull albertasat/ground-station-website:user-latest
docker run --rm -it -p 8000:8000 albertasat/ground-station-website:user-latest
```

Now, open Google Chrome and navigate to [http://localhost:8000](http://localhost:8000).

## Developer Installation
This installation method it will allow you to immediately see any modifications you have made to the source code on your host machine in the docker container (and vice versa). As a result, you will not have to rebuild the docker image every time you make a change to the source code on your host machine. 

### Developer Installation on MacOS and Ubuntu

Start by cloning this repository and pulling the albertasat/ground-station-website:dev-latest docker image using the commands below.

```bash
cd <cloned-repo-location>
docker pull albertasat/ground-station-website:dev-latest
```

You can then run a container off the updated image using:

```bash
export GS_HOMEDIR=$(pwd)
docker run --rm -it -v $GS_HOMEDIR:/home/ex2_ground_station_website -p 8000:8000 albertasat/ground-station-website:dev-latest
```

This will open a bash terminal within the docker container.

Install pip and npm libraries by running `update.sh`.

```bash
source ./update.sh
```

Then, run the app.

```bash
flask run --host=0.0.0.0 --port=8000
```

Finally, open Google Chrome and navigate to [http://localhost:8000](http://localhost:8000).

### Developer Installation on Windows

Start by cloning this repository and pulling the albertasat/ground-station-website:dev-latest docker image using the commands below.

```bash
cd <cloned-repo-location>
docker pull albertasat/ground-station-website:dev-latest
```

You can then run a container off the updated image using:

```bash
docker run --rm -it -v %cd%:/home/ex2_ground_station_website -p 8000:8000 albertasat/ground-station-website:dev-latest
```

This will open a bash terminal within the docker container.

The `update.sh` and `env.sh` files will need to be converted to use LF line endings. This can be done in [VSCode](https://qvault.io/clean-code/line-breaks-vs-code-lf-vs-crlf/) or [Notepad++](http://www.sql313.com/index.php/43-main-blogs/maincat-dba/62-using-notepad-to-change-end-of-line-characters), or by running the following commands from the `ex2_ground_station_website` directory (while in the bash terminal).

```bash
sed -i 's/\r//g' update.sh
sed -i 's/\r//g' env.sh
```

Install pip and npm libraries by running `update.sh` (while in the bash terminal).

```bash
source ./update.sh
```

Then, run the app.

```bash
flask run --host=0.0.0.0 --port=8000
```

Finally, open Google Chrome and navigate to [http://localhost:8000](http://localhost:8000).


## Manual installation
This installation method will work on an Ubuntu operating system.

First please clone the repository and then update the submodules using the following commands:

```bash
cd <cloned-repo-location>
git submodule update --init --recursive
```

Ubuntu dependencies for PostgreSQL, libCSP, and scheduling tasks:

```bash
sudo apt-get install at build-essential wget curl libpq-dev python3-dev gcc-multilib g++-multilib libsocketcan-dev
```

To run the app's frontend (i.e. in your web browser), you will need node & npm -- at least version 8. I recommend using the [Node Version Manager](https://github.com/nvm-sh/nvm). 

Make sure you have a [Python virtual environment](https://docs.python.org/3/tutorial/venv.html) installed and active! To do this navigate to the root project directory and run the following commands:

```bash
python3 -m venv env
source env/bin/activate
```

Set the environment variables. These environment variables tell Flask which configuration settings to use. Do this in every terminal window or you'll get database errors.

```bash
source ./env.sh
```

Install pip and npm libraries by running `update.sh`.

```bash
source ./update.sh
```  

Finally, run the app.

```bash
flask run
```

# Useful commands

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

# The Comm Module - [comm.py](./comm.py)

The comm module is the main point of interaction between this application and the satellite. It acts a client to both, and interprets commands sent from the operator to the satellite, and also interprets telemetry sent from the satellite. To extend the comm module, there are 4 files of interest in the root directory of the project:

**[comm.py](./comm.py)**
Acts a loop for constantly checking commands sent by an operator in the communications table, and sending them to a socket.  
If no function is defined for that command, the command string will be sent by default.

**[gs_commands.py](./gs_commands.py)**
Additional functionality for commands can be implemented here. The return value is what is to be sent, or None if nothing is to be sent. Defined functions must be added to the gs_commands dictionary, with the command string as the key, and the function as the value, in order for [comm.py](./comm.py) to interpret commands properly.
Handling satellite responses is also implemented here, through the function handle_response(). By default the satellite response is posted to the communication table.

**[automation.py](./automation.py)**
This is the script ran at the time of the passover. It first reads from **[automation.txt](./automation.txt)**, a file with commands seperated by newlines. The commands in [automation.txt](./automation.txt) will be posted to the communications table, and sent to the satellite automatically.

The script then loads the next passover time, and utlizes the linux `at` program to schedule the next time automation will run. You will need to install `at`, which can be done with `sudo apt-get install at` on Ubuntu.

**[seed_passover.sh](./seed_passover.sh)**
Run this script to schedule [automation.py](./automation.py) to run at the next passover time. Only necessary to run if no automation is scheduled (ie. passovers have ran out, or for initially setting up automation).
