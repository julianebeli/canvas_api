import re

input = {
    "paramType": "form",
    "name": "account[settings][restrict_student_future_listing][value]",
    "description": "Restrict students from viewing future enrollments in course list",
    "type": "boolean",
    "format": None,
    "required": False,
    "deprecated": False
}

chars = re.compile(r'[\[\]]')


def get_type(t):
    if t == 'boolean':
        return True


keys = list(filter(lambda x: x, chars.split(input['name'])))
keys.reverse()
s = {keys.pop(0): get_type(input['type'])}
while keys:
    s = {keys.pop(0): s}

print(s)

class validator:
    def __init__(self, scheme):
        pass
        self.model = {}

