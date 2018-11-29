import unittest

from bson.objectid import ObjectId
from models.computer import Computer


class ComputerTests(unittest.TestCase):

    @staticmethod
    def get_computer_input_dict():
        return {'_id': ObjectId(b'testdata1234'), 'name': 'test', 'cpu_type': '8086', 'number_of_cpus': 1,
                'memory_in_mb': 0, 'is_virtual': False}

    def test_constructFromDict(self):
        input_data = self.get_computer_input_dict()
        c = Computer(**input_data)
        self.assertIsNotNone(c)

    def test_incompleteDict(self):
        """
        test that a error is raised if any of the required arguments are not present when creating an instance
        :return:
        """
        input_data = self.get_computer_input_dict()
        for key in input_data.keys():
            test_dict = input_data.copy().pop(key)
            with self.assertRaises(TypeError):
                c = Computer(**test_dict)
                self.assertIsNotNone(c)

    def test_eval_repr_construction(self):
        """
        tests that eval(repr(x)) == x, which tests both __repr__ and __eq__
        :return:
        """
        c = Computer(**self.get_computer_input_dict())
        s = repr(c)
        self.assertIsNotNone(s)
        self.assertGreater(len(s), 0, "repr of test computer should be greater than 0")
        c2 = eval(s)
        self.assertEqual(c, c2, "constructed object should be equal to the original")
        # or as a one liner...
        # self.assertEqual(c, eval(repr(c)), "constructed object should be equal to the original")

    def test_hash(self):
        c = Computer(**self.get_computer_input_dict())
        c2 = Computer(**self.get_computer_input_dict())
        c2.is_virtual = True
        self.assertNotEqual(c, c2, "objects should be be equal")
        self.assertNotEqual(hash(c), hash(c2), "hash of unequal objects must be different")
