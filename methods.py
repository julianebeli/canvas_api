import json
from typing import List, Set, Dict, Any
try:
    from . import config
except:
    import config
from pluck import pluck

data: Dict = {}
with open(config.catalog, 'r', encoding="utf8") as f:
    data = json.loads(f.read())


def my_params(data: List[Dict]) -> Dict:
    new_dict = {}
    for p in data:
        new_dict[p['name']] = p

    return new_dict


# def typer(typ, val):
#     if typ == 'string':
#         print(val.isinstance(basestring))
#     else:
#         'not typed'

def pathify(a, b):
    path = a.pop(0)
    while a:
        path += f'[{a.pop(0)}]'
    return {path: b}


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


class Method:

    def __init__(self, methodname: str, **kwargs: Dict[str, Any]) -> None:
        self.data: Dict = {}
        self.action: str = ''
        self.path: str = ''
        self.params: Dict = {}
        self.schema: Dict = data[methodname]

        self.parameters: Dict = my_params(self.schema['parameters'])
        if kwargs:
            print('the kw args')
            print(kwargs)

            self.add_params(**kwargs)
        self.results: List = []

    def add_params(self, **kwargs: Dict[str, Any]):

        # have to deal with deep dictionaries of params being represented as a path string in the docs
        # this function pulls out all those path stings in the params
        # form params need to be sent as a dict but checked against the docs
        # this function converts the params into checkable form
        # print('adding params')
        for x in traverse(kwargs):
            self.params.update(pathify(x[0], x[1]))

    def __repr__(self):
        classname = self.__class__.__name__
        # attrs = ', '.join(['{}={}'.format(attr, val) for attr, val in self.__dict__.items() if attr != 'attributes'])  # noqa
        return '{}\n{}'.format(classname, json.dumps(self.schema, indent=4))

    def streamline(self):
        p: Dict = {}
        for param in self.params:
            if param in self.parameters:
                p[param] = self.params[param]
        return p

    def do(self, **kwargs: dict):
        if kwargs:
            self.add_params(**kwargs)
        self.params = self.streamline()  # remove unnecessary params
        # print()
        # print('-' * 48)
        # print(self.parameters)
        # print('-' * 48)
        # print(self.params)
        # print('-' * 48)
        # print(self.params)

        required_params: Set = set(map(lambda y: y['name'],
                                       filter(lambda x: x['required'] is True,
                                              self.schema['parameters'])))
        # print ('required', required_params)
        # print(set(self.params.keys()))
        if required_params.issubset(set(self.params.keys())):
            d: Dict = {'path': {}, 'query': {}, 'form': {}}
            for p in self.params:
                # print('p', p)
                # print(self.parameters[p])
                if 'enum' in self.parameters[p].keys():
                    if not set(self.params[p]).issubset(set(self.parameters[p]['enum'])):
                    # if not self.params[p] in self.parameters[p]['enum']:  # what about multiple values?
                        # print('subsetting', set(self.params[p]).issubset(set(self.parameters[p]['enum'])))
                        print(f'STOPPED: {self.params[p]} is not valid value for: {p}')
                        exit()
                pname = p
                if self.parameters[p]['type'] == 'array':
                    pname = f'{pname}[]'

                pType = self.parameters[p]['paramType']
                d[pType][pname] = self.params[p]
            # print('query data:', d)
            self.data = d
            self.action = self.schema['action']
            self.path = self.schema['path']

            # api_call = API(server=config.server_to_use, call_object={
            #                'action': ,
            #                'path': self.schema['path'],
            #                'data': self.data})
            # self.make_call()
            # self.results = api_call.results

        else:
            print('STOPPED: missing required parameters')
            print(required_params - set(self.params.keys()))
            exit()


if __name__ == '__main__':

    methodname: str = 'update_account'
    # methodname = 'create_user'

    # param: Dict[str, Any] = dict(course_id=25606)
    param = {'account': {'settings': {'restrict_student_past_view': {'locked': True, 'value': True}, 'restrict_student_future_view': {'locked': True, 'value': True}, 'lock_all_announcements': {'locked': True, 'value': True}, 'restrict_student_future_listing': {
        'locked': True, 'value': True}}, 'services': {}, 'default_user_storage_quota_mb': 1, 'default_time_zone': 's', 'default_group_storage_quota_mb': 1, 'sis_account_id': 's', 'name': 's', 'default_storage_quota_mb': 1}, 'id': 6}

    method = Method(methodname, **param)

    print(method.params)
    method.do()
    print(method.path)
    print(method.data)
    exit()
    # param = dict(user_ids=[6, 12])
    # param = dict(user_id=6)
    # param = dict(include='email')
    # # param = dict(include='oblong')
    # method.add_params(**param)

    # # param = {'pseudonym[unique_id]': 'blahblah'}
    # # method.add_params(**param)

    # method.do()
    # print(pluck(method.results, 'name', 'id'))
    # exit()

    # methodname2:
    #     str = 'get_outcome_results'
    # method2 = Method(methodname2)
    # print(method2.schema['path'])
    # param = dict(account_id=1)
    # method2.add_params(**param)

    # method2.params['course_id'] = 144

    # param = dict(cars=12)
    # method2.add_params(**param)

    # param = dict(dogs=8)
    # print(method2.parameters.keys())
    # method2.do(**param)
    # exit()
