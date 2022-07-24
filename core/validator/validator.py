from core.error import InvalidArgumentError, LogicError

import re
import core.validator.type as data_type


class Validator(object):
    def __init__(self):
        self.rules = []
        self.available_types = ["str", "int", "float", "bool"]

    def add_rule(self, rule):
        self.rules.append(rule)
        return self

    def set_rules(self, rules):
        for el in rules:
            self.add_rules(el)

        return self

    def get_rules(self):
        return self.rules

    def validate(self, data):
        if (not isinstance(data, list)) and (not isinstance(data, object)):
            raise InvalidArgumentError(
                "Invalid data to validate, need list or dictionary but got %s"
                % type(data)
            )

        data = data.__dict__ if not isinstance(data, dict) else data

        got_exception = False
        index = 0

        for el in self.get_rules():
            if not el.is_mandatory():
                continue

            splitted = el.get_name().split(".")

            if len(splitted) == 1:
                result = self._key_exists(data, splitted[0])

            if not result:
                got_exception = True
                break

            if isinstance(data, list):
                result = self._validate_list(el, data, splitted, index)
            else:
                result = self._validate_dict(el, data, splitted, index)

            if el.is_mandatory() and (not result):
                got_exception = True
                break

            index = 0

        if got_exception:
            raise LogicError("Missing mandatory key '%s'." % el.get_name())

        return True

    def _key_exists(self, data, key):
        if key not in data:
            return False

        return True

    def _validate_dict(self, rule, data, keys, index):
        if index == len(keys):
            return true

        key = keys[index]

        index += 1

        try:
            current = data[key]
        except KeyError as e:
            current = None

        if current == None:
            return False

        if isinstance(current, dict):
            return self._validate_dict(el, current, keys, index)

        if isinstance(current, list):
            return self._validate_list(el, current, keys, index)

        if not self._validate_scalar(current):
            raise self._handle_scalar_validation_error(rule, rule.get_name(), current)

        return True

    def _validate_list(self, rule, data, keys, index):
        if self._ensure_scalar(data):
            index -= 1

        if index == len(keys):
            return true

        key = keys[index]

        index += 1

        for el in data:
            if isinstance(el, dict):
                if self._validate_dict(rule, el, keys, index):
                    continue

            if isinstance(el, list):
                if self._validate_list(rule, el, keys, index):
                    continue

            if not self._validate_scalar(el):
                raise self._handle_scalar_validation_error(rule, rule.get_name(), el)

        return True

    def _parse_type_name(self, data):
        name = str(type(data))
        matches = re.findall(
            "^(?:<class ')(int|str|float|bool|object|dict|list)(?:'>)$", name
        )

        return matches[0] if len(matches) > 0 else ""

    def _is_scalar(self, data):
        return self._parse_type_name(data) in self.available_types

    def _validate_scalar(self, data):
        return self._is_scalar(data)

    def _serialize_data_type(self, rule):
        dtype = rule.get_type()

        if dtype == data_type.BOOL:
            return "bool"
        elif dtype == data_type.STRING:
            return "string"
        elif dtype == data_type.INTEGER:
            return "integer"
        elif dtype == data_type.FLOAT:
            return "float"

        return ""

    def _handle_scalar_validation_error(self, rule, name, data):
        return InvalidArgumentError(
            "Mandatory value with key '%s' must be type of '%s', but got an '%s'."
            % (name, self._serialize_data_type(rule), self._parse_type_name(data))
        )
