# Python-RESTFul-Example

This is a simple example showing one approach to using Flask-RESTful to create an API with some
additional secure development options included than what is otherwise available in other sample
projects.  For example, it uses Talisman to provide a CSP and when not running in development mode,
it support CSRF protection using SeaSurf (in development mode, Swagger breaks with SeaSurf enabled).

_Note:  This is a rather hastily thrown together sample.  I pulled it together in a few days as
something to kickstart a github portfolio while interviewing for some jobs.  Before using this as 
an example to base a serious project on, do your due diligence and ensure it meets your needs._

_In particular, some nicer things can be done with the MongoService by creating an abstract base
class that extends Resource to handle persistence more generically._

## Getting Started

This project was created in PyCharm and likely will work best using that.  However, some effort
has been made to ensure it works running at the command line as well.

### Creating Certificates

The first step that should be taken is to create self-signed certificates since the project
uses HTTPS by default.  To create the required certificates, follow the prompts and run:

```
$ ./generate_ssl_cert.sh
```

An example run is shown below:
```
Found OpenSSL, generating cert...

Follow the prompts below for Country, State/Province, and Locality.
For Organization Name, you can use 'python-restful-example' or whatever you like.
For Organizational Unit Name, you can leave this blank.
For Common Name, for most cases, using 'localhost' as the common name should work well.
For Email Address, you may leave this blank.

Generating a 4096 bit RSA private key
.....................++
.......................................................++
writing new private key to 'python-restful-example-key.pem'
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) []:US
State or Province Name (full name) []:Ohio
Locality Name (eg, city) []:Dayton
Organization Name (eg, company) []:python-restful-example                                                   
Organizational Unit Name (eg, section) []:
Common Name (eg, fully qualified host name) []:localhost
Email Address []:
```

This should create two files: **python-restful-example-cert.pem** and **python-restful-example-key.pem**.

### Prepare a virtual environment

```
$ python3 -m venv venv
$ . /venv/bin/activate
$ pip3 install -r requirements.txt
```

### Prepare a MongoDB instance

The project stores and retrieves data from MongoDB.  A **Vagrant** instance that creates a MongoDB
server pre-configured to work with this project can be found in the **mongodb** folder.  It has been
tested with both LXC and Parallels providers for Vagrant.  It should work with minimal changes with
other providers as well.

To use, simply run:

```
$ cd mongodb
$ vagrant up
```

## Running the project

To run from the command line, you can run with the Flask builtin development server, run:

```
$ ./run-with-builtin-server.sh
 * Serving Flask app "app.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on https://127.0.0.1:8443/ (Press CTRL+C to quit)
 * Restarting with stat
[2018-11-28 22:21:15,788] INFO in app: Define environment variable APP_CONFIG_FILE to point to a configuration file to customize configuration from the defaults.
[2018-11-28 22:21:15,789] INFO in app: Using MongoDB at 127.0.0.1:57017
[2018-11-28 22:21:15,789] INFO in app: Development environment detected, using modified Talisman configuration.
 * Debugger is active!
 * Debugger PIN: 789-242-621
[2018-11-28 22:21:16,381] INFO in app: Define environment variable APP_CONFIG_FILE to point to a configuration file to customize configuration from the defaults.
[2018-11-28 22:21:16,382] INFO in app: Using MongoDB at 127.0.0.1:57017
[2018-11-28 22:21:16,382] INFO in app: Development environment detected, using modified Talisman configuration.
```

To run from the command line using gunicorn, run:

```
$ ./run-with-gunicorn.sh
[2018-11-28 22:22:21 -0500] [86823] [INFO] Starting gunicorn 19.9.0
[2018-11-28 22:22:21 -0500] [86823] [INFO] Listening at: https://127.0.0.1:8443 (86823)
[2018-11-28 22:22:21 -0500] [86823] [INFO] Using worker: sync
[2018-11-28 22:22:21 -0500] [86826] [INFO] Booting worker with pid: 86826
[2018-11-28 22:22:21,966] INFO in app: Define environment variable APP_CONFIG_FILE to point to a configuration file to customize configuration from the defaults.
[2018-11-28 22:22:21,966] INFO in app: Using MongoDB at 127.0.0.1:57017
[2018-11-28 22:22:21,967] INFO in app: Development environment detected, using modified Talisman configuration.
```

In PyCharm, you can also run with the builtin Flask server or with gunicorn.  Debugging should
work with either option.

### Configuration

A configuration file can be created outside the project.  Set an environment variable
named **APP_CONFIG_FILE** prior to running the scripts-- you can modify the PyCharm runtime
configuration to add the environment variable or export the variable at the command line.

To view the defaults look in config.py.  These are the two settings that are most likely
to need to be changed:

```
MONGODB_URL = "127.0.0.1:57017"
MONGO_DB_NAME = "python-restful-example-db"
```

The **MONGODB_URL** setting should point to the IP and port of your MongoDB instance.
The default settings should work with no changes if you are using the provided Vagrant
configuration.

The **MONGO_DB_NAME** lets you customize the name of the database in MongoDB.  It can be
any valid name.
