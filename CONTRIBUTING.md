# Developing the Groundstation app

To work on this project you will need several tools.
1. First, this guide assumes that you are familiar with the unix-style terminal (eg. bash). If you're on Windows, you can use a [virtual machine](https://www.virtualbox.org/), [git bash for Windows](https://gitforwindows.org/), or the [Windows subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/about). If you are not comfortable using a terminal, we recommend you use [other guides](https://linuxjourney.com/lesson/the-shell) to practice it first.
2. We'll need [`git`](https://git-scm.com/), [Python 3](https://www.python.org/), [`npm`](https://www.npmjs.com/get-npm), and [`pip`](https://pypi.org/project/pip/) installed on your machine. We are also assuming that you [know how to use Git](https://try.github.io/).

## Setting up the local development environment

First, let's download the project from Github using git. We recommend that you fork the repository, but for simplicity's sake we'll just download it.

`git clone https://github.com/UAlberta-CMPUT401/AlbertaSat.git`

The backend uses Python and the pip package manager, and the frontend uses JavaScript and the npm package manager.

### node.js & npm

This project uses [React](https://reactjs.org/), which means we need npm & node.js. If you're unfamiliar, I recommend nvm, the Node Version Manager. [Install it with their install script](https://github.com/nvm-sh/nvm#about). Then install the stable release of node & npm:  

`nvm install stable`

Now activate it:

`nvm use stable`

### Python pip dependencies

We need a virtual environment in the project's root directory. A virtual environment isolates the version of Python and pip packages to this project alone. For more information, [see this guide](https://docs.python.org/3/tutorial/venv.html). You only need to create the virtual environment *once* (it lives inside the project's folder).

`cd AlbertaSat`  
`python3 -m venv venv`

Make sure you **activate** the virtual environment in every terminal window.

`source venv/bin/activate`

Now that the venv is activated, we need to install all of the project's libraries inside the venv. Luckily, we wrote a script to do this for you:

`source ./update.sh`

And to run the app:

`flask run`.

### at

The automation module uses a command line program called `at` to schedule tasks. Install it on Ubuntu with `sudo apt install at`.

## Cheatsheet

**Every time you open the project:** `source venv/bin/activate`  
As mentioned above, none of your tools will work if you're not in the venv.

**In every terminal window:** `source ./env.sh`  
You will get strange errors if the environment variables are not set. They specify the app's configuration file and entry point.

**To install pip libraries, set Flask environment variables, recreate & seed the database, and rebuild frontend:** `source ./update.sh`  
Try doing things manually, step by step if you run into problems.

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

The script then loads the next passover time, and utlizes the linux `at` program to schedule the next time automation will run. You will need to install `at`, which can be done with `sudo apt install at` on Ubuntu.

**seed_passovers.sh**
Run this script to schedule automation.py to run at the next passover time. Only necessary to run if no automation is scheduled (ie. passovers have ran out, or for initially setting up automation).
