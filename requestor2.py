from . import config
from .methods import Method
from .requests_logging import debug_requests_on, debug_requests_off
import requests
import json
import re
from functools import partial
from requests_cache import install_cache
from collections import namedtuple


pattern = re.compile(r'(\w+)\[(\w+)\]')
connection = namedtuple('connection', ['name', 'token'])


def reorg_keys(payload):
    # print(f"reorg payload: {payload}")
    output: dict = {}

    for k, v in payload.items():
        x = pattern.findall(k)
        if x:
            [parent, child, val] = [x[0][0], x[0][1], v]
            if parent not in output.keys():
                output[parent] = {}
            output[parent][child] = val
        else:
            output[k] = v
    print(f"reorg keys: {output}")
    return output


def test_complete_url(u, action):
    s = u.split("/")
    t = u.split("//")
    assert(len(s) > 3)
    assert('api' in s)
    assert(len(t) == 2)
    assert('{' not in u)
    print(f"{action} {u}")
    return


def process2(link):
    next = list(filter(lambda x: 'rel="next"' in x, link.split(",")))
    if next:
        m = max(list(map(int, re.findall(r'page=(\d+)&', next[0]))))
    else:
        m = []

    return m


def process(r):
    if not r:
        return []
    else:
        m = max(list(map(int, re.findall(r'page=(\d+)&', r))))
        # print('LINK:', m)
        return list(map(lambda x: x + 1, range(m)))[1:]


def template(url, bulk, page):
    return f'{url}?page={page}&per_page={bulk}'


class API():

    def __init__(self,
                 server=config.server_to_use,
                 act_as=None, 
                 cache=None,
                 trace=False,
                 call_object=None):

        print("LAUNCHING ADAPTER: API2")
        self.server = self.make_connector(server)

        if cache is None:
            print('Didn\'t deal with cache')
        else:
            install_cache('api_cache', backend='sqlite', expire_after=cache)
            print(f'cache_time: {cache}')

        if trace:
            debug_requests_on()
        else:
            debug_requests_off()

        self.method = call_object
        self.results = []
        self.response_error = False
        self.user = act_as
        self.headers = self.make_header(self.server)
        self._session = requests.Session()
        self.method_switch = {'GET': self._get_request,
                              'POST': self._post_request,
                              'DELETE': self._delete_request,
                              'PUT': self._put_request
                              }

    def add_method(self, methodname, **kwargs):
        self.method = Method(methodname, **kwargs)

    def make_connector(self, server):
        if not server or server == 'prod':
            servername = config.servername
            token = config.tokens['prod']
        else:
            serverparts = config.servername.split('.')
            serverparts.insert(1, server)
            servername = ".".join(serverparts)
            token = config.tokens[server]
        return connection(servername, token)

    def process_responses(self, data):
        output = []
        for entry in data:  # entry is a response object
            if isinstance(entry.json(), dict):
                output.append(entry.json())
            else:
                output.extend(entry.json())
        return output

    def response_ok(self):
        if not self.results:
            self.response_error = False
            return

        if isinstance(self.results, dict):
            result = self.results
        else:
            result = self.results[0]

        if 'errors' in result.keys():
            self.response_error = True
        else:
            self.response_error = False

    def do(self, call_object={}):
        if call_object:
            self.method = call_object
        self.method.do()
        # print('method action', self.method.action)
        api_function = self.method_switch[self.method.action]
        url = self.complete_url(
            self.server,
            self.method.path.format(**self.method.data['path']),
            self.method.action)
        if self.user:
            self.method.data['query']['as_user_id'] = f'{self.user}'

        responses = []

        if self.method.action != 'GET':

            response = api_function(url=url,
                                    headers=self.headers,
                                    params=self.method.data['query'],
                                    data=self.method.data['form'])

            responses.append(response)
        else:
            page = 1
            bulk = config.bulk
            calls = partial(template, url, bulk)
            call1 = calls(page)
            response = api_function(url=call1,
                                    headers=self.headers,
                                    params=self.method.data['query'],
                                    data=self.method.data['form'])

            responses.append(response)

            if 'Link' in response.headers.keys():
                next_page = process2(response.headers['Link'])
                while next_page:
                    response = api_function(url=calls(next_page),
                                            headers=self.headers,
                                            params=self.method.data['query'],
                                            data=self.method.data['form'])
                    responses.append(response)
                    next_page = process2(response.headers['Link'])

        self.results = self.process_responses(responses)
        self.response_ok()

    def make_header(self, target):
        return {'Authorization': 'Bearer {}'.format(target.token),
                'Content-Type': 'application/json'}

    def complete_url(self, target, url, action):
        u = "https://{}/api{}".format(target.name, url)
        test_complete_url(u, action)
        return u

    def _get_request(self, url, headers, params=None, data=None):
        return self._session.get(url,
                                 headers=headers,
                                 params=params,
                                 data=json.dumps(data))

    def _post_request(self, url, headers, params=None, data=None):
        print("POSTING")
        print(params)
        print(json.dumps(data))
        return self._session.post(url,
                                  headers=headers,
                                  params=params,
                                  data=json.dumps(reorg_keys(data)))

    def _delete_request(self, url, headers, params=None, data=None):
        return self._session.delete(url,
                                    headers=headers,
                                    params=params,
                                    data=json.dumps(data))

    def _put_request(self, url, headers, params=None, data=None):
        print(f'PUTTING: {url, params, data}')
        new_data = reorg_keys(data)
        return self._session.put(url,
                                 headers=headers,
                                 params=params,
                                 data=json.dumps(new_data))

    def upload_file(self, filename):
        # print('attaching', filename)
        url = 'https://tas.beta.instructure.com/api/v1/accounts/1/outcome_imports'
        data_file = {'file': open(str(filename), 'rb')}
        return self._session.post(url, headers=self.headers, files=data_file)
