# import prance
import json
import re
chars = re.compile(r'[\[\]]')
from typing import List, Dict, Any
# from mypy import Any

data = {
    "methodname": "create_link_outcome_courses",
    "course_id": 8,
    "id": 23101,
    "title": "06 - Students examine sources to determine their origin, purpose and reliability and to identify and describe values and perspectives.",
    "display_name": "[CAC.07P.06]",
    "vendor_guid": "AC_2019_287_[CAC.07P.06]",
    "description": " > Humanities and Social Sciences > Civics and citizenship > Year 7  Primary > [CAC.07P.06]<br>&nbsp;<br>&nbsp;Students examine sources to determine their origin, purpose and reliability and to identify and describe values and perspectives.<br>&nbsp;<br><div style='background-color:#DCDCDC;padding:5;margin:10;font-size:smaller;float:left'>WA: Well Above Standard, AB: Above Standard, AT: At Standard, AP: Approaching Standard, DE: Developing<br></div><br><br>&nbsp;",
    "calculation_method": "n_mastery",
    "calculation_int": 1,
    "mastery_points": 0,
    "ratings": [
        {
            "description": "\ud83d\udde8\ufe0f",
            "points": 5
        },
        {
            "description": "WA",
            "points": 4
        },
        {
            "description": "AB",
            "points": 3
        },
        {
            "description": "AT",
            "points": 2
        },
        {
            "description": "AP",
            "points": 1
        },
        {
            "description": "DE",
            "points": 0
        }
    ],
    "parent": "7492f81db2a925120088fdc5c8f1910f"
}

create_link_outcome_courses = {
    "catagory": "/outcome_groups",
    "path": "/v1/courses/{course_id}/outcome_groups/{id}/outcomes",
    "description": "Link an outcome into the outcome group. The outcome to link can either be\nspecified by a PUT to the link URL for a specific outcome (the outcome_id\nin the PUT URLs) or by supplying the information for a new outcome (title,\ndescription, ratings, mastery_points) in a POST to the collection.\n\nIf linking an existing outcome, the outcome_id must identify an outcome\navailable to this context; i.e. an outcome owned by this group's context,\nan outcome owned by an associated account, or a global outcome. With\noutcome_id present, any other parameters (except move_from) are ignored.\n\nIf defining a new outcome, the outcome is created in the outcome group's\ncontext using the provided title, description, ratings, and mastery points;\nthe title is required but all other fields are optional. The new outcome\nis then linked into the outcome group.\n\nIf ratings are provided when creating a new outcome, an embedded rubric\ncriterion is included in the new outcome. This criterion's mastery_points\ndefault to the maximum points in the highest rating if not specified in the\nmastery_points parameter. Any ratings lacking a description are given a\ndefault of \"No description\". Any ratings lacking a point value are given a\ndefault of 0. If no ratings are provided, the mastery_points parameter is\nignored.",
    "action": "POST",
    "parameters": [{
            "paramType": "path",
            "name": "course_id",
            "description": "ID",
            "type": "string",
            "format": None,
            "required": True,
            "deprecated": False
    }, {
        "paramType": "path",
        "name": "id",
        "description": "ID",
        "type": "string",
        "format": None,
        "required": True,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "outcome_id",
        "description": "The ID of the existing outcome to link.",
        "type": "integer",
        "format": "int64",
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "move_from",
        "description": "The ID of the old outcome group. Only used if outcome_id is present.",
        "type": "integer",
        "format": "int64",
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "title",
        "description": "The title of the new outcome. Required if outcome_id is absent.",
        "type": "string",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "display_name",
        "description": "A friendly name shown in reports for outcomes with cryptic titles,\nsuch as common core standards names.",
        "type": "string",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "description",
        "description": "The description of the new outcome.",
        "type": "string",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "vendor_guid",
        "description": "A custom GUID for the learning standard.",
        "type": "string",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "mastery_points",
        "description": "The mastery threshold for the embedded rubric criterion.",
        "type": "integer",
        "format": "int64",
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "ratings[description]",
        "description": "The description of a rating level for the embedded rubric criterion.",
        "type": "array",
        "format": None,
        "required": False,
        "deprecated": False,
        "items": {
                "type": "string"
        }
    }, {
        "paramType": "form",
        "name": "ratings[points]",
        "description": "The points corresponding to a rating level for the embedded rubric criterion.",
        "type": "array",
        "format": "int64",
        "required": False,
        "deprecated": False,
        "items": {
                "type": "integer"
        }
    }, {
        "paramType": "form",
        "name": "calculation_method",
        "description": "The new calculation method.  Defaults to \"decaying_average\"",
        "type": "string",
        "format": None,
        "required": False,
        "deprecated": False,
        "enum": ["decaying_average", "n_mastery", "latest", "highest"]
    }, {
        "paramType": "form",
        "name": "calculation_int",
        "description": "The new calculation int.  Only applies if the calculation_method is \"decaying_average\" or \"n_mastery\". Defaults to 65",
        "type": "integer",
        "format": "int64",
        "required": False,
        "deprecated": False
    }]
}


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


def get_type(t):
    if t == 'boolean':
        return True
    if t == 'string':
        return "s"
    if t == 'integer':
        return 1
    if t == 'Hash':
        return dict()


def string(p):
    print('found string')
    # print(p)


def integer(p):
    pass


def array(p):
    print(p['items'])
    print(p['name'])
    keys = list(filter(lambda x: x, chars.split(p['name'])))
    keys.reverse()
    s = {keys.pop(0): get_type(p['items']['type'])}
    while keys:
        s = {keys.pop(0): s}

    print(s)


acc: dict = {}
paramlist: List[Dict[str, Any]] = create_link_outcome_courses['parameters']
for i in paramlist:
    s: dict = {}
    keys = list(filter(lambda x: x, chars.split(i['name'])))
    keys.reverse()
    s = {keys.pop(0): get_type(i['type'])}
    while keys:
        s = {keys.pop(0): s}
    print(s)
    acc = merge(acc, s)
print(acc)


for entry in paramlist:
    print(">", entry['type'])
    try:
        globals()[entry['type']](entry)
    except:
        print(f"no function for: {entry['type']}")
