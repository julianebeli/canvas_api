import json
from pathlib import Path

from jsonschema import validate, Draft7Validator
import re


def traverse(dic, path=None):
    # https://stackoverflow.com/questions/11929904/traverse-a-nested-dictionary-and-get-the-path-in-python#31998950
    if not path:
        path = []
    if isinstance(dic, dict):
        for x in dic.keys():
            local_path = path[:]
            local_path.append(x)
            for b in traverse(dic[x], local_path):
                yield b
    else:
        yield path, dic


def merge(a, b, path=None):
    # https://stackoverflow.com/questions/7204805/dictionaries-of-dictionaries-merge/7205107#7205107
    "merges b into a"
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a


def mergedicts(dict1, dict2):
    for k in set(dict1.keys()).union(dict2.keys()):
        if k in dict1 and k in dict2:
            if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                yield (k, dict(mergedicts(dict1[k], dict2[k])))
            else:
                # If one of the values is not a dict, you can't continue merging it.
                # Value from second dict overrides one in first and we move on.
                yield (k, dict2[k])
                # Alternatively, replace this with exception raiser to alert
                # you of value conflicts
        elif k in dict1:
            yield (k, dict1[k])
        else:
            yield (k, dict2[k])


def get_form_params(method):
    return list(filter(lambda x: x['paramType'] == 'form', method['parameters']))


with open(Path(__file__).parent / 'catalog.json') as f:
    catalog = json.loads(f.read())

# for method in list(catalog.keys()):
#     form = get_form_params(catalog[method])
#     if form:
#         print(method)
#         for param in form:
#             print(param['name'])

#         print('-' * 48)

schema = catalog['update_account']
# print(json.dumps(schema, indent=4))

chars = re.compile(r'[\[\]]')


def get_type(t):
    if t == 'boolean':
        return True
    if t == 'string':
        return "s"
    if t == 'integer':
        return 1
    if t == 'Hash':
        return dict()

    print(f'dont have a typer for {t}')


result: dict = {}
acc: dict = {}
acc2: dict = {}
for input in schema['parameters']:

    s: dict = {}
    if input["paramType"] == "form":
        keys = list(filter(lambda x: x, chars.split(input['name'])))
        keys.reverse()
        s = {keys.pop(0): get_type(input['type'])}
        while keys:
            s = {keys.pop(0): s}

        print(s)
        acc = dict(mergedicts(acc, s))
        acc2 = merge(acc, s)

    #     acc = {**acc, **s}
    #     print(acc)
    # result = {**result, **acc}
    # print(result)
print('results equivalent')
print(acc == acc2)
print(acc)
acc['single'] = 5
print('traverse')


def pathify(a, b):
    path = a.pop(0)
    while a:
        path += f'[{a.pop(0)}]'
    return {path: b}


paths: dict = {}
for x in traverse(acc):
    paths.update(pathify(x[0], x[1]))
print(paths)
exit()
print('is the parameter field valid ?')

print(Draft7Validator.check_schema(schema['parameters']))

exit()

# 'error[subject]'
# 'error[url]'
# 'error[email]'
# 'error[comments]'
# 'error[http_env]'

# error = {
#     "type": "object",
#     "properties": {
#         "subject": {"type": "string"},
#         "email": {"type": "string"},
#         "comments": {"type": "string"},
#         "http_env": {"type": "string"}
#     }
# }
# valid = validate(instance={"subject": 6, }, schema=error)
# print(valid)


# schema = {
#     "type": "object",
#     "properties": {
#         "price": {"type": "number"},
#         "name": {"type": "string"},
#     },
# }
# print(validate(instance={"name": "Eggs", "price": 34.99}, schema=schema))
# validate(instance={"name": "Eggs", "price": "Invalid"}, schema=schema)
account = {"type": "object",
           "properties": {
               "account": {
                   "type": "object",
                   "properties": {
                       "name": {"type": "string"},
                       "sis_account_id": {"type": "string"},
                       "default_time_zone": {"type": "string"},
                       "default_storage_quota_mb": {"type": "integer"},
                       "default_user_storage_quota_mb": {"type": "integer"},
                       "default_group_storage_quota_mb": {"type": "integer"},
                       "services": {"type": "object"},
                       "settings": {
                           "type": "object",
                           "properties": {
                               "restrict_student_past_view": {
                                   "type": "object",
                                   "properties": {
                                       "value": {"type": "boolean"},
                                       "locked": {"type": "boolean"}
                                   }
                               },
                               "restrict_student_future_view": {
                                   "type": "object",
                                   "properties": {
                                       "value": {"type": "boolean"},
                                       "locked": {"type": "boolean"}
                                   }
                               },
                               "lock_all_announcements": {
                                   "type": "object",
                                   "properties": {
                                       "value": {"type": "boolean"},
                                       "locked": {"type": "boolean"}
                                   }
                               },
                               "restrict_student_future_listing": {
                                   "type": "object",
                                   "properties": {
                                       "value": {"type": "boolean"},
                                       "locked": {"type": "boolean"}
                                   }
                               }
                           }
                       }
                   }
               }}}
print(acc)
print(isinstance(account, dict))
# account = json.dumps(account)
print('validating schema')
print(Draft7Validator.check_schema(account))

print(validate(instance=acc, schema=account))
exit()
schema = {"type": "array",
          "minItems": 1,
          "items": {"type": "object",
                    "properties": {
                        "id": {"type": "number"},
                        "name": {"type": "string"}
                    },
                    "required": ["id", "name"]
                    }
          }

print('checking')
print(Draft7Validator.check_schema(account))
# print(validate(instance=[{'id': 4, 'name': "me"}], schema=schema))
