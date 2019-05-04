# from bs4 import BeautifulSoup as Soup
# import python_jsonschema_objects as jsob
from typing import List, Set, Dict, Any
import requests
# import requests_cache
import json
import config
from collections import namedtuple
from swagger_spec_validator import validate_spec_url

# requests_cache.install_cache('api_live_cache')
session = requests.session()
url1: str = f'https://{config.servername}/doc/api'
print(f'{url1}/api-docs')
validate_spec_url(f'{url1}')

# h = session.get(f'{url1}/api-docs.json').json()

# resource_urls: List[str] = [f'{url1}{method["path"]}' for method in h['apis']]


# api_data: Dict = {}
# for resource in resource_urls:
#     parser = prance.ResolvingParser(resource)
#     doc: Dict = session.get(resource).json()
#     fname: str = resource.split('/')[-1]
#     with open(f'./api_docs/{fname}', 'w') as g:
#         g.write(json.dumps(doc, indent=4))
#     print(json.dumps(doc, indent=4))
#     # pyjsob = jsob.ObjectBuilder(doc)
#     # ns = pyjsob.build_classes()
#     # method = ns.api
#     for api in doc['apis']:
#         print(api)
#         # pyjsob = jsob.ObjectBuilder(api)
#         # ns = pyjsob.build_classes()
#         # method = ns.api
#         new_doc: Dict = {}
#         # print(json.dumps(doc, indent=4))
#         new_doc['catagory'] = doc['resourcePath']
#         new_doc['path'] = api['path']
#         new_doc['description'] = api['description']

#         operation = api['operations'][0]
#         new_doc['action'] = operation['method']
#         new_doc['parameters'] = operation['parameters']
#         name = operation['nickname']
#         api_data[name] = new_doc

# with open('catalog.json', 'w') as outfile:
#     json.dump(api_data, outfile)

exit()


# def _json_object_hook(d):
#     return namedtuple('X', d.keys())(*d.values())
# def json2obj(data):
#     return json.loads(data, object_hook=_json_object_hook)
# for method in h['apis']:
#     u = f'{url1}{method["path"]}'
#     resource_urls.append(u)
# print(resource_urls)
# doc = session.get(resource_urls[2]).json()
# print(json.dumps(doc, indent=4))
# for api in doc['apis']:
#     print(api['path'])
#     for operation in api['operations']:
#         print(operation['method'])
#         print(operation['nickname'])
#         required = []
#         for param in operation['parameters']:
#             # print(f"REQUIRED: {param['required']}")
#             if param['required'] is True:
#                 required.append([param['name']])
#             # print(param['name'])
#             # print(param['paramType'])
#             # print(param['required'])
#         print(required)
#     print()
