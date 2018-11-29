from flask import Blueprint
from flask_restplus import Api

from namespaces.computers import api as ns1

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint,
          title='Example API',
          version='1.0',
          description='A sample RESTful API that supports versioning and tries to be more secure by default.',
          doc='/doc/')

api.add_namespace(ns1)
