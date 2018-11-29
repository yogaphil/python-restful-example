import os

from flask import Flask
from flask_seasurf import SeaSurf
from flask_talisman import Talisman

from api_v1 import blueprint as api1


def get_secret_key(length: int = 32):
    """ Generates a sequence of 'length' random bytes suitable for use as a secret key by Flask. """
    return os.urandom(length)


# create the app and set a secure encryption key for Flask
flask_app = Flask(__name__)
flask_app.secret_key = get_secret_key()

# load configuration defaults
flask_app.config.from_object('config')

#
# if an environment variable of APP_CONFIG_FILE points to a file that exists, load that configuration
#
config_env_var = 'APP_CONFIG_FILE'
if config_env_var in os.environ:
    conf_file = os.environ[config_env_var]
    from pathlib import Path

    f = Path(conf_file)
    if not f.is_file():
        flask_app.logger.error("File {} defined in APP_CONFIG_FILE does not exist!".format(conf_file))
    else:
        flask_app.logger.info("Found file {}, loading configuration.".format(conf_file))
        flask_app.config.from_envvar(config_env_var)
else:
    flask_app.logger.info("Define environment variable APP_CONFIG_FILE to point to a configuration file "
                          "to customize configuration from the defaults.")

#
# verify MONGODB_URL has been set successfully in our configuration
#
if "MONGODB_URL" not in flask_app.config:
    flask_app.logger.error("Could not find required setting MONGODB_URL.")
else:
    flask_app.logger.info("Using MongoDB at {}".format(flask_app.config["MONGODB_URL"]))


if 'FLASK_ENV' in flask_app.config and flask_app.config['FLASK_ENV'] != 'development':
    # enable csrf when not using swagger, client must present csrf token
    csrf = SeaSurf(flask_app)
    selected_csp_policy = {
        'font-src': '\'self\'',
        'img-src': '\'self\'',
        'frame-src': '\'self\'',
        'script-src': '\'self\'',
        'style-src': '\'self\'',
        'default-src': '\'self\'',
    }
else:
    #
    # Swagger isn't SeaSurf aware, so do not enable it in development mode.
    #
    # Talisman will prevent the swaggerui from loading in the browser due to unsafe inlines in the swagger web content,
    # so modify the CSP so swagger can work when in development mode.
    #
    flask_app.logger.info("Development environment detected, using modified Talisman configuration.")
    selected_csp_policy = {
        'font-src': '\'self\'',
        'img-src': '\'self\' *',
        'frame-src': '\'self\'',
        'script-src': '\'self\' \'unsafe-inline\'',
        'style-src': '\'self\' \'unsafe-inline\'',
        'default-src': '\'self\'',
    }

talisman = Talisman(flask_app, content_security_policy=selected_csp_policy)

#
# register supported versions of the API here
#
flask_app.register_blueprint(api1)

#
# Don't do this:
#
# if __name__ == '__main__':
#    flask_app.run()
#
# it is no longer encouraged, even in development.  See run-with-builtin-server.sh or run-with-gunicorn.sh for some
# alternatives if not running within PyCharm.
#
# ref: http://flask.pocoo.org/docs/1.0/api/#flask.Flask.run
#     "It is not recommended to use this function for development with automatic reloading as this is badly supported.
#      Instead you should be using the flask command line script’s run support."
#
