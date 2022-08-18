import json

from validator import Validator


if __name__ == '__main__':
    validator = Validator(json.loads(input()))
    validator.run()
