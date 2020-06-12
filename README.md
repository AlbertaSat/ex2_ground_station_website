# ex2_ground_station_website

In this repository we are attempting to make a functional and extendable groundstation for the operators of the [Ex-Alta 2 satellite](https://albertasat.ca/ex-alta-2/). It is a Flask web app that uses a REST API for the back end (Python), paired with a React MaterialUI interface on the front end (JavaScript). Also included in this repository is a "satellite simulator" python module used to simulate the interaction between our app and a real cubesat. A "comm" (communications) module intermediates this exchange. Finally, a collection of scripts are used to achieve the goal of automating some aspects of the groundstation app. Follow the links below to see the documentation.

[![Build Status](https://travis-ci.com/UAlberta-CMPUT401/AlbertaSat.svg?token=TRHuLXSMdv9x8426GEpU&branch=dev)](https://travis-ci.com/UAlberta-CMPUT401/AlbertaSat)

<hr>

### Links

**[How to Develop and Extend this project](CONTRIBUTING.md)** - A guide to developing this project further. Includes instructions for setting up the development environment, running the app, testing the app, and expanding the `comm.py` module.

**[Generated source code documentation](https://ualberta-cmput401.github.io/AlbertaSat/)** - This is automatically generated documentation from the source code. It lives in `/docs`. Github pages has it served [here](https://ualberta-cmput401.github.io/AlbertaSat/). When you make changes to the Python code, update this documentation to match it using `source ./update_docs.sh`. If you would like to view the docs locally, serve it with `python3 -m http.server` and go to http://0.0.0.0:8000/ in your browser.

**[REST API backend documentation](https://documenter.getpostman.com/view/9298924/SW11YKEd)** - This is documentation for the REST backend API (`groundstation/backend_api`) of this Flask app. There are examples of requests that you can make to the backend and what responses to expect.

**[Glossary](https://github.com/UAlberta-CMPUT401/AlbertaSat/wiki/Glossary)** - Go here if you're confused about a word or phrase that we keep using.

**[Wiki](https://github.com/UAlberta-CMPUT401/AlbertaSat/wiki)** - See more information about the project's design and development.

### Docker commands

To install the app using [Docker](https://docs.docker.com/get-docker/), `cd` into the project and run this command:

`docker build --tag ground_website:latest . --build-arg FLASK_APP=groundstation/__init__.py --build-arg FLASK_ENV=development --build-arg APP_SETTINGS=groundstation.config.DevelopmentConfig --build-arg SECRET_KEY="\xffY\x8dG\xfbu\x96S\x86\xdfu\x98\xe8S\x9f\x0e\xc6\xde\xb6$\xab:\x9d\x8b"`

**NOTE: depending on your installation, you may need to use `sudo` on Docker commands.**

This will build the docker image. It may take several minutes. The --build-args are for setting the app's configuration settings; the above arguments configure the app for developing. Read the Dockerfile to see the build steps.

To run the docker container:

`docker run --rm -it --network=host ground_website:latest`

The Dockerfile tells docker to start the container with a bash shell:  
Do `flask run` to run the app.  
Do `python3 manage.py recreate_db` to erase the database.  
Do `python3 manage.py seed_db` to seed the database with data.  
Do `cd groundstation/static && npm run build` to rebuild the React frontend.  
Do `exit` to exit the container.  

