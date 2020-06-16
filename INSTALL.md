# Installation
---

## Docker installation & usage

To install the app using [Docker](https://docs.docker.com/get-docker/), `cd` into the project (where the Dockerfile is) and run this command to build the docker image:

```
docker build --tag ground_website:latest . --build-arg FLASK_APP=groundstation/__init__.py --build-arg FLASK_ENV=development --build-arg APP_SETTINGS=groundstation.config.DevelopmentConfig --build-arg SECRET_KEY="\xffY\x8dG\xfbu\x96S\x86\xdfu\x98\xe8S\x9f\x0e\xc6\xde\xb6$\xab:\x9d\x8b"
```

*NOTE: depending on your installation, you may need to use* `sudo` *on Docker commands.*

It may take several minutes. The --build-args are for setting the app's configuration settings; the above arguments configure the app for developing. Read the Dockerfile to see the build steps.

To run the docker container:

```
docker run --rm -it --network=host ground_website:latest
```

The Dockerfile tells docker to start the container with a bash shell:  
Do `flask run` to run the app.  
Do `python3 manage.py recreate_db` to erase the database.  
Do `python3 manage.py seed_db` to seed the database with data.  
Do `cd groundstation/static && npm run build` to rebuild the React frontend.  
Do `exit` to exit the container.  

---

## Manual installation

**1. Clone the repository**

```
git clone https://github.com/AlbertaSat/ex2_ground_station_website.git && cd ex2_ground_station_website
```

**2. Install OS dependencies.** These are dependencies for PostgreSQL, libCSP, and scheduling tasks.

**Ubuntu**
```
sudo apt install at build-essential wget curl libpq-dev python3-dev gcc-multilib g++-multilib libsocketcan-dev
```

**3. Get git submodules** for the libCSP and the ground station network software.

```
git submodule init
git submodule update
cd ex2_ground_station_software
git switch feature-website
git pull
cd ..
```

**3. Have node & npm installed**, at least version 8. If you don't have node & npm installed, I recommend using the [Node Version Manager](https://github.com/nvm-sh/nvm).

**4. Make sure you have a [Python virtual environment](https://docs.python.org/3/tutorial/venv.html)** installed and active!

```
source venv/bin/activate
```

**5. Set the environment variables.** These environment variables tell Flask which configuration settings to use.

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

This command works because we set the environment variables earlier to enter the app at `groundstation/__init__.py`

**8. Running with CSP**

First, run the app with `flask run` as normal.  
Also run the [ex2_command_handling_demo repo](https://github.com/AlbertaSat/ex2_command_handling_demo) with docker at the same time. It will start a zmqproxy server.  
Then also run `LD_LIBRARY_PATH=./libcsp/build source ./automate.sh`, which will run whatever commands are inside `automation.txt`. The command first has to be specified in `manage.py`. All of these should be running simultaneously.  
Not yet compatible with docker.

---

## Cheatsheet

**Activate virtual environment (every terminal window):** `source venv/bin/activate`  
Flask won't work if the venv is not activated. You'll know it's active when there is a `(venv)` at the start of your command prompt.

**Set environment variables (every terminal window)** `source ./env.sh`  
You will get strange errors if the environment variables are not set. They specify Flask's configuration file and entry point.

**To install pip libraries, set Flask environment variables, recreate & seed the database, and rebuild frontend:** `source ./update.sh`  
Try doing things manually, step by step, if you run into problems.

**To recreate the database:** `python3 manage.py recreate_db`  

**To seed the database with example data:** `python3 manage.py seed_db`  
Both `recreate_db` and `seed_db` are functions inside `manage.py`; look at them and change them as you see fit (particularly `seed_db`) to initialize the database with different data.

**To rebuild the React frontend code with npm:** `cd groundstation/static && npm run build`  
The code that makes the app look good is written in Javascript, and can be found in `groundstation/static`.

**To start the app in development mode:** `flask run` or `python3 run.py`, then open it in your browser (typically http://127.0.0.1:5000/)

**To run all of the unit tests for the app:** `python3 manage.py test`  
**To run the front end GUI tests with Selenium:** `python3 manage.py test frontend_test` NOTE: you will need the `geckodriver` in order to do this. Get it [here](https://github.com/mozilla/geckodriver/releases).

---

## Extending The Comm Module

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
