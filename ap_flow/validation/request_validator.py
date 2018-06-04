from cerberus import Validator
import yaml
import os


class RequestValidator(Validator):
    def _validate_cost(self, cost, field, value):
        if self.root_document['type'] == 4:
            if cost and not isinstance(value, (bool, type(None))):
                self._error(field, 'Invalid cost: should be of type bool')
        else:
            if cost and not (type(value) in (int, float, type(None))):
                self._error(field, 'Invalid cost: should be a number')

    def _validate_costs_row(self, costs_row, field, value):
        tasks = len(self.root_document['tasks'])
        if costs_row and len(value) != tasks:
            self._error(field, 'Wrong number of elements in a costs\' row')

    def _validate_costs_array(self, costs_array, field, value):
        workers = len(self.root_document['workers'])
        if costs_array and len(value) != workers:
            self._error(field, 'Wrong number of rows in the costs\' array')

    def _validate_unique_values(self, unique_values, field, value):
        if unique_values and len(set(value)) != len(value):
            self._error(field, 'Workers are not unique')


def get_request_validator():
    vsf = os.path.join(os.path.dirname(__file__), 'validation_schema.yml')
    with open(vsf, 'r') as stream:
        try:
            schema = yaml.load(stream)
            return RequestValidator(schema)
        except yaml.YAMLError as exc:
            print(exc)
