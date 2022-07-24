from core.validator.rule import Rule
from core.validator.validator import Validator


def validator_factory(rule_map):
    validator = Validator()

    for el in rule_map.keys():
        validator = validator.add_rule(Rule(el, rule_map[el][0], rule_map[el][1]))

    return validator
