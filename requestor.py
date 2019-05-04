from . import config
from .methods import Method
from .requests_logging import debug_requests, debug_requests_on, debug_requests_off
import requests
import json
import re
from functools import partial
from requests_cache import install_cache
from collections import namedtuple

from .exceptions import (
    BadRequest, CanvasException, Forbidden, InvalidAccessToken,
    ResourceDoesNotExist, Unauthorized
)


connection = namedtuple('connection', ['name', 'token'])


def test_complete_url(u, action):
    print(f"CHECKING: {action} {u}")
    s = u.split("/")
    t = u.split("//")
    assert(len(s) > 3)
    assert('api' in s)
    assert(len(t) == 2)
    assert('{' not in u)
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


def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.
    """
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))


class API():

    def __init__(self, server=config.server_to_use, act_as=None, cache=None, call_object=None):
        print("LAUNCHING IT")
        self.server = self.make_connector(server)
        # self.server = server
        if cache is None:
            print('Didn\'t deal with cache')
        else:
            install_cache('api_cache', backend='sqlite', expire_after=cache)
            print(f'cache_time: {cache}')
        self.method = call_object
        self.results = []
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

    def response_success(self, response):
        # print('In error checking with:')
        # print(response)
        # print(dir(response))
        # print(response.reason)
        # print(response.ok)
        # print(response.json())
        # if not response.ok:
        #     print(f'ERROR: {response.reason} [{response.status_code}]')
        # else:
        #     print(f'{response.reason} [{response.status_code}]')
        # print('_' * 48)

        if response.status_code == 400:
            raise BadRequest(response.text)
        elif response.status_code == 401:
            if 'WWW-Authenticate' in response.headers:
                raise InvalidAccessToken(response.json())
            else:
                raise Unauthorized(response.json())
        elif response.status_code == 403:
            raise Forbidden(response.text)
        elif response.status_code == 404:
            raise ResourceDoesNotExist('Not Found')
        elif response.status_code == 500:
            raise CanvasException(
                "API encountered an error processing your request")

        return response

    def process_responses(self, data):
        print(f'\nSTATUS_CODE: {data[0].status_code}')
        # print(f'\nCONTENT: {data[0].content}\n')

        output = []
        for entry in data:  # entry is a response object
            if isinstance(entry.json(), dict):
                output.append(entry.json())
            else:
                output.extend(entry.json())
        return output

    # def api_call(self, url):
    #     pass

    def do(self, call_object={}):
        if call_object:
            self.method = call_object
        self.method.do()
        print('method action', self.method.action)
        api_function = self.method_switch[self.method.action]

        url = self.complete_url(
            self.server,
            self.method.path.format(**self.method.data['path']),
            self.method.action)
        if self.user:
            print('adding', self.user)
            self.method.data['query']['as_user_id'] = f'{self.user}'
        responses = []
        # with debug_requests():
        # debug_requests_on()
        debug_requests_off()
        if self.method.action != 'GET':
            print('DATA:', self.method.data['form'])

            response = api_function(url=url,
                                    headers=self.headers,
                                    params=self.method.data['query'],
                                    data=self.method.data['form'])
            if not self.response_success(response):
                exit("API call didn't work")

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

            if not self.response_success(response):
                exit("API call didn't work")

            responses.append(response)
            # print('headers', response.headers)
            # print('header keys', list(response.headers.keys()))
            if 'Link' in response.headers.keys():
                # print(response.headers['Link'])
                # calls_to_make = list(map(calls, process(response.headers['Link'])))
                # print('api calls to make', calls_to_make)
                # for c in calls_to_make:
                #     responses.append(
                #         api_function(url=c,
                #                      headers=self.headers,
                #                      params=self.method.data['query'],
                #                      data=self.method.data['form']))
                next_page = process2(response.headers['Link'])
                while next_page:
                    response = api_function(url=calls(next_page),
                                            headers=self.headers,
                                            params=self.method.data['query'],
                                            data=self.method.data['form'])
                    responses.append(response)
                    next_page = process2(response.headers['Link'])

        self.results = self.process_responses(responses)

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
        return self._session.post(url,
                                  headers=headers,
                                  params=params,
                                  data=json.dumps(data))

    def _delete_request(self, url, headers, params=None, data=None):
        return self._session.delete(url,
                                    headers=headers,
                                    params=params,
                                    data=json.dumps(data))

    def _put_request(self, url, headers, params=None, data=None):
        print(f'PUTTING: {url, params, data}')
        return self._session.put(url,
                                 headers=headers,
                                 params=params,
                                 data=json.dumps(data))

    def upload_file(self, filename):
        print('attaching', filename)
        url = 'https://tas.beta.instructure.com/api/v1/accounts/1/outcome_imports'
        data_file = {'file': open(str(filename), 'rb')}
        return self._session.post(url, headers=self.headers, files=data_file)
