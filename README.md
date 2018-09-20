# Recommended Code Editor For UI

[Visual Studio Code](https://code.visualstudio.com/download)

## This document is only for Ubuntu. Code will work onto other OS but i haven't tried running it


# How to setup UI
The project is build on materialize css and simple javascript, you dont need to download libraries specific for the project, you just need apache2.
## How to setup Apache2

- Apache2: 
    Go onto this link [How to install Apache2](https://www.linode.com/docs/web-servers/apache/apache-web-server-on-ubuntu-14-04/) or follow the instructions below.

     -- `sudo apt-get update && sudo apt-get upgrade`

     -- `sudo apt-get install apache2 apache2-doc apache2-utils`

     -- `sudo service apache2 restart`


After completeing the setup go onto your browser and type [localhost](127.0.0.1) you should be able to see the apache2 welcome page.

## NOTE: Apache sometimes conflicts with nginx 

After doing that copy and paste the Dashboard folder in `/var/www/html/`

You can now access UI via `localhost/Dashboard`


# How to setup Database [Couchdb](http://couchdb.apache.org/)

I have used NOSQL [couchdb](http://couchdb.apache.org/) docker image as our database, so you will need to install [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/#os-requirements)

Install docker via following command.

-- `sudo apt-get update` 

-- `sudo apt-get install docker-ce`

After docker is installed run following command.

-- `docker run -t --name db -p 8091-8094:8091-8094 -p 11210:11210 couchbase/server-sandbox:5.5.0`

This will download and run docker image in data persistance mode.

After the command completes, you can access couchdb from [WebConsole](localhost:8091).

The initial username is `Administrator` and password is `password`

After logging in to the console click on `Buckets` from side menu this will get you onto the page where you can create buckets (Consider bucket sort of like a table in RDBMS is just no relations) and you can store few different types of data types their including whole `python` object by pickling it.

Anyway there should be two buckets already available there
1. auth (100mb)
2. data (412mb)

if they are not create them, `auth` is the bucket in which we are storing usernames and passwords and `data` is the one in which we are storing actual data.

After doing that we will need [couchbase python dependency](https://docs.couchbase.com/python-sdk/2.4/start-using-sdk.html). Install it using these commands.

-- `wget http://packages.couchbase.com/releases/couchbase-release/couchbase-release-1.0-4-amd64.deb`

-- `sudo dpkg -i couchbase-release-1.0-4-amd64.deb`

-- `sudo apt-get update`

-- `sudo apt-get install libcouchbase-dev build-essential python-dev python-pip`

-- `sudo pip install couchbase`


# How to setup python environment

Backend of the project is build on python 2.7, if you are a linux user it comes along with all linux distributions so we don't need to download it specifically, but just in case if you dont have it you can install it by following commands.

## Python2.7

   -- `sudo apt-get update`

   -- `sudo apt-get upgrade`

   -- `sudo apt-get install python2.7 python-pip`

## Don't upgrade your python-pip to newer version, the newer version is unstable you wont be able to install any python dependencies via pip, but instead you will have to use python-pip command to install dependencies.

## [Python Flask](http://flask.pocoo.org/)

To connect Backend API to Frontend we are using [Flask](http://flask.pocoo.org/), to install full stack of flask dependencies run following commands.

`sudo pip install flask`

`sudo pip install -U flask-cors` This will install [Flask-Cors](https://flask-cors.readthedocs.io/en/latest/).

`sudo pip install flask-restful` This will install [Flask-Restful](https://flask-restful.readthedocs.io/en/0.3.5/installation.html)

You are all set, go into the `FlaskProj` directory through your terminal and run following command.
`python flasktet.py`

You should see something like this.
 * Serving Flask app "flasktet" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 176-475-588
`

