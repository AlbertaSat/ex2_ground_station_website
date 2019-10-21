# AlbertaSat

>*AlbertaSat is a group of students and faculty at the University of Alberta that have come together to design, build, test, launch and operate satellites. Our goal is to support a commercial space industry, global space culture, global space expansionism and global space education through our missions in space. - https://albertasat.ca/*

In this repository we are attempting to make a smoother, more functional, and extendable ground station experience for the operators of the [Ex-Alta 2 satellite](https://albertasat.ca/ex-alta-2/).

For more information, please visit our [wiki](https://github.com/UAlberta-CMPUT401/AlbertaSat/wiki).

[![Build Status](https://travis-ci.com/UAlberta-CMPUT401/AlbertaSat.svg?token=TRHuLXSMdv9x8426GEpU&branch=dev)](https://travis-ci.com/UAlberta-CMPUT401/AlbertaSat)


## To setup local enviornment:
1. Make sure you have python, npm, and pip installed on your machine
2. Install local enviornment: `./update.sh` 
3. Set environment variables `source env.sh`    
4. To run the local enviornment: `python3 run.py` or simply `flask run`

## For db migrations:
1. `python3 manage.py db migrate`
2. `python3 manage.py db update`

## For db creation:
1. `python3 manage.py recreate_db`
