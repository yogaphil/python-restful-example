from flask import current_app
from flask_restplus import Namespace, Resource, fields, reqparse, inputs

from models.computer import Computer as ComputerModel
from service.mongo_service import MongoService

api = Namespace('computers', description='Computer related operations')

# this model is used by Flask-RESTPlus for response marshalling and generating swagger docs, but where we can, we will
# use marshmallow for marshalling instead, since Flask-RESTPlus has deprecated their serialization approach
computer = api.model('Computer', {
    '_id': fields.String(required=False,
                         description='A unique identifier for this computer. Created when saved.'),
    'name': fields.String(required=True, description='The common name of this computer.'),
    'cpu_type': fields.String(required=True, description='The type of CPU installed in this computer.'),
    'number_of_cpus': fields.Integer(required=True, description='The number of CPUs in this computer.'),
    'memory_in_mb': fields.Integer(required=True,
                                   description='The amount of memory installed in this computer in megabytes'),
    'is_virtual': fields.Boolean(required=True, description='Indicates whether this computer is a virtual machine')
})

# instead of using @api.expect(computer) and accepting a JSON computer representation, we can use reqparser
# to accept the individual fields, but then they must be parsed manually instead of using the marshmallow
# serialization approach used below, but this is what it would look like:
#
# computer_parser = reqparse.RequestParser()
# computer_parser.add_argument('name', required=True, type=str)
# computer_parser.add_argument('cpu_type', required=True, type=str)
# computer_parser.add_argument('number_of_cpus', required=True, type=int)
# computer_parser.add_argument('memory_in_mb', required=True, type=int)
# computer_parser.add_argument('is_virtual', required=True, type=inputs.boolean) # prefer inputs.boolean instead of bool
#
# then, below, for example on the post() method, you would use:
#
# @api.expect(computer_parser)
#
# instead of:
#
# @api.expect(computer)


# a more complete example might create an abstract base class that extends Resource and handles
# many of the common service interactions with the MongoService, but for now, keeping this example simple

@api.route('/')
class ComputerList(Resource):

    @api.marshal_list_with(computer)
    def get(self):
        """ Returns a list of all stored computers. """
        service = MongoService(current_app.config)
        return [c for c in service.get_all_resource_of_type("computer")]  # NOTE: bad practice, should limit result set

    @api.expect(computer)
    @api.marshal_with(computer)
    def post(self):
        """ Creates a computer in the system. """
        service = MongoService(current_app.config)
        # api.payload should contain valid json for a Computer instance, validate it
        try:
            current_app.logger.debug("request payload: {}".format(api.payload))

            # also could validate the api.payload does not exceed a reasonable size prior to
            # attempting to instantiate from the JSON... for this example, skipping that.

            # construct an instance from the JSON
            c = ComputerModel.from_json(api.payload)

            # ensure we are not given an _Id that might conflict with what is already in mongo
            if c._id is not None:
                raise ValueError("Cannot specify _id when creating an object.")

            # serialize back to JSON to filter out an injected/unexpected fields in
            # the input
            c_as_json = c.to_json()
            current_app.logger.debug("validated json: {}".format(c_as_json))

            # save the instance and grab the created _Id
            new_id = service.save_resource("computer", c_as_json)

            # update the instance with its _Id before returning the result
            c._id = new_id
            return c.to_json(), 201
        except ValueError as ve:
            api.abort(code=400, message=str(ve))


# noinspection PyUnresolvedReferences
@api.route('/<string:computer_id>')
class Computer(Resource):

    @api.doc('computer')
    @api.marshal_with(computer)
    def get(self, computer_id):
        """ Retrieves the computer with the given id. """
        service = MongoService(current_app.config)
        c = service.get_resource_by_id("computer", computer_id)
        if c is None:
            api.abort(code=404, message="Computer with _id {} not found.".format(computer_id))
        return c, 200
