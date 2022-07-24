import core.validator.type as data_type

from core.error import RuleTypeError

_rule_type_error = "Invalid data type."


class Rule(object):
    def __init__(self, name, data_type, required=True):
        try:
            self._type_assertion(data_type)
        except RuleTypeError as e:
            raise e

        self.name = name
        self.data_type = data_type
        self.mandatory = required

    def get_name(self):
        return self.name

    def get_type(self):
        return self.data_type

    def is_mandatory(self):
        return self.mandatory

    def _type_assertion(self, dtype):
        options = {
            data_type.BOOL: True,
            data_type.STRING: True,
            data_type.INTEGER: True,
            data_type.FLOAT: True,
            data_type.UNDEFINED: False,
        }

        val = options.get(dtype, None)

        if val == False or val == None:
            raise RuleTypeError(_rule_type_error)

        return True
