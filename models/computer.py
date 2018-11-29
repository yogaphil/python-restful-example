from bson.objectid import ObjectId
from marshmallow import Schema, fields, post_load, ValidationError


class ComputerSchema(Schema):
    """
    defines a marshmallow schema with the attributes we need in our simple computer model example.
    """
    _id = fields.String()
    name = fields.String()
    cpu_type = fields.String()
    number_of_cpus = fields.Integer()
    memory_in_mb = fields.Integer()
    is_virtual = fields.Boolean()

    @post_load
    def make_computer(self, data: dict):
        return Computer(**data)


class Computer(object):
    """
    a simple example model object representing a few attributes of a computer.
    """
    _schema = ComputerSchema()

    def __init__(self, name, cpu_type, number_of_cpus, memory_in_mb, is_virtual, _id=None):
        self.name = name
        self.cpu_type = cpu_type
        self.number_of_cpus = number_of_cpus
        self.memory_in_mb = memory_in_mb
        self.is_virtual = is_virtual
        if _id is not None:
            self._id = ObjectId(str(_id))
        else:
            self._id = None

    def __repr__(self):
        return ('Computer(_id={x._id}, name="{x.name}", '
                'cpu_type="{x.cpu_type}", number_of_cpus={x.number_of_cpus}, '
                'memory_in_mb={x.memory_in_mb}, is_virtual={x.is_virtual})'.format(x=self))

    def __eq__(self, o: object) -> bool:
        if self is o:
            return True
        if not isinstance(o, self.__class__):
            return NotImplemented
        return self.name == o.name and self.cpu_type == o.cpu_type and self.number_of_cpus == o.number_of_cpus \
            and self.memory_in_mb == o.memory_in_mb and self.is_virtual == o.is_virtual

    def __hash__(self) -> int:
        return hash((self.name,
                     self.cpu_type,
                     self.number_of_cpus,
                     self.memory_in_mb,
                     self.is_virtual))

    @staticmethod
    def from_json(json_data: str):
        try:
            result = Computer._schema.load(json_data)
        except ValidationError as err:
            raise ValueError("Failed to parse json data into a Computer instance: {}".format(err.messages))
        return result

    def to_json(self):
        if self._id is None:
            result = ComputerSchema(exclude=('_id',)).dump(self)
        else:
            result = Computer._schema.dump(self)
        return result
