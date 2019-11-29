# Developing the Groundstation app

To work on this project you will need several tools.
1. First, this guide assumes that you are familiar with the unix-style terminal (eg. bash). It is included by default with macOS and most Linux distributions. If you're on Windows, you could also use [git bash for Windows](https://gitforwindows.org/), the [Windows subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/about), or a [virtual machine](https://www.virtualbox.org/). If you are not comfortable using a terminal, we recommend you use [other guides](https://linuxjourney.com/lesson/the-shell) to practice it first.
2. You will need [`git`](https://git-scm.com/), [Python 3](https://www.python.org/), [`npm`](https://www.npmjs.com/get-npm), and [`pip`](https://pypi.org/project/pip/) installed on your machine. We are also assuming that you [know how to use Git](https://try.github.io/).

## Setting up the local development environment

First, let's download the project from Github using git. We recommend that you fork the repository, but for simplicity's sake we'll just download it.

`git clone https://github.com/UAlberta-CMPUT401/AlbertaSat.git`

`cd` inside the project's directory and create the virtual environment. A virtual environment is like a laboratory. It has all of the tools and equipment we need to work, away from the rest of your computer. For more information, [see this guide](https://docs.python.org/3/tutorial/venv.html). You only need to create the virtual environment once (it lives inside the project's folder).

`cd AlbertaSat`  
`python3 -m venv venv`

Every time we want to work on the project, we first need to activate the virtual environment (or "venv") before we start working. This is like stepping into the lab. You can't do any work unless you are in the lab.

`source venv/bin/activate`

Now that the virtual environment is activated, we need to install all of the project's libraries inside the venv. Luckily, we wrote a script to do this for you:

`source ./update.sh`

Now you're all set. Start the app in development mode by running `flask run`.

## Cheatsheet

**Every time you open the project:** `source venv/bin/activate`  
As mentioned above, none of your tools will work if you're not in the venv.

**To install libraries, set Flask environment variables, recreate & seed the database, and rebuild React code:** `source ./update.sh`  
When you modify the code, the easiest way to reset the app is just to run this script.

**To recreate the database:** `python3 manage.py recreate_db`  
**To seed the database with example data:** `python3 manage.py seed_db`  
Both `recreate_db` and `seed_db` are functions inside `manage.py`; look at them and change them as you see fit (particularly `seed_db`) to initialize the database with different data.

**To rebuild the React frontend code with npm:** `cd groundstation/static && npm run build`  
The code that makes the app look good is written in Javascript, and can be found in `groundstation/static`.

The logic of the app is written in Python with the help of [Flask](https://flask.palletsprojects.com/en/1.1.x/).

**To start the app in development mode:** `flask run` or `python3 run.py`, then open it in your browser (typically http://127.0.0.1:5000/)

**To run all of the unit tests for the app:** `python3 manage.py test`  
**To run the front end GUI tests with Selenium:** `python3 manage.py test frontend_test` NOTE: you will need the `geckodriver` in order to do this. Get it [here](https://github.com/mozilla/geckodriver/releases).

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

The script then loads the next passover time, and utlizes the linux `at` program to schedule the next time automation will run.

**seed_passovers.sh**
Run this script to schedule automation.py to run at the next passover time. Only necessary to run if no automation is scheduled (ie. passovers have ran out, or for initially setting up automation).

