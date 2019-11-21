# AlbertaSat

>*AlbertaSat is a group of students and faculty at the University of Alberta that have come together to design, build, test, launch and operate satellites. Our goal is to support a commercial space industry, global space culture, global space expansionism and global space education through our missions in space. - https://albertasat.ca/*

In this repository we are attempting to make a functional and extendable ground station for use by the operators of the [Ex-Alta 2 satellite](https://albertasat.ca/ex-alta-2/).

For more information, please visit our [wiki](https://github.com/UAlberta-CMPUT401/AlbertaSat/wiki).

[![Build Status](https://travis-ci.com/UAlberta-CMPUT401/AlbertaSat.svg?token=TRHuLXSMdv9x8426GEpU&branch=dev)](https://travis-ci.com/UAlberta-CMPUT401/AlbertaSat)


## Setting up the local development environment
1. Make sure you have python, npm, and pip installed on your machine
2. Install local environment: `source ./update.sh`
3. Set environment variables: `source ./env.sh`    
4. To run the local environment: `python3 run.py` or simply `flask run`

To recreate the database: `python3 manage.py recreate_db`
To seed the database with data: `python3 manage.py seed_db`
Both of these commands are included in `update.sh`. If you make changes to the codebase, reset the database and reload the environment by running `source ./update.sh`. Then do `flask run` to run the app in development mode.
