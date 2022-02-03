# ex2_ground_station_website

In this repository we are attempting to make a functional and extendable groundstation control panel for the operators of the [Ex-Alta 2 satellite](https://albertasat.ca/ex-alta-2/). This is a Flask web app. It uses a REST API for the back-end application logic (Python), paired with a React MaterialUI interface on the front-end (JavaScript). Also included in this repository is a "satellite simulator" python module used to simulate the interaction between our app and a real cubesat. A communications module, `comm.py`, intermediates this exchange. Finally, the automation module, `automation.py`, and some scripts automate the sending of commands to the satellite. 

## Documentation

**[How to install, run, and develop the project](INSTALL.md)** - Details installation, usage, and notes on important modules.

**[REST API documentation](https://documenter.getpostman.com/view/9298924/SW11YKEd)** - This is documentation for the REST API (`groundstation/backend_api`) of this Flask app. Within are examples of requests that you can make and what responses to expect.

**[Python source code documentation](https://albertasat.github.io/ex2_ground_station_website/)** - These docs are automatically generated from the comments in the Python source code. It lives in `/docs`. When you make changes to backend_api, update this documentation to match it using `update_docs.sh`. You can look at them in your browser if you serve them locally. (i.e. `python3 -m http.server`)  

**[The project wiki](https://github.com/AlbertaSat/ex2_ground_station_website/wiki)** - Running instructions for the satellite simulator and documentation for topics such as the comm.py module.

The documentation above is not guaranteed to be up-to-date or complete so it's recommended that you read the code.
