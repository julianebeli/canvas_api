import json
import re


pattern = re.compile(r'(\w+)\[(\w+)\]')

data = {
    "catagory": "/courses",
    "path": "/v1/courses/{id}",
    "description": "Update an existing course.\n\nArguments are the same as Courses#create, with a few exceptions (enroll_me).\n\nIf a user has content management rights, but not full course editing rights, the only attribute\neditable through this endpoint will be \"syllabus_body\"",
    "action": "PUT",
    "parameters": [{
        "paramType": "path",
        "name": "id",
        "description": "ID",
        "type": "string",
        "format": None,
        "required": True,
        "deprecated": False
    }, {
        "paramType": "query",
        "name": "course[account_id]",
        "description": "The unique ID of the account to move the course to.",
        "type": "integer",
        "format": "int64",
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "course[name]",
        "description": "The name of the course. If omitted, the course will be named \"Unnamed\nCourse.\"",
        "type": "string",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "course[course_code]",
        "description": "The course code for the course.",
        "type": "string",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "course[start_at]",
        "description": "Course start date in ISO8601 format, e.g. 2011-01-01T01:00Z",
        "type": "DateTime",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "course[end_at]",
        "description": "Course end date in ISO8601 format. e.g. 2011-01-01T01:00Z",
        "type": "DateTime",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "query",
        "name": "course[license]",
        "description": "The name of the licensing. Should be one of the following abbreviations\n(a descriptive name is included in parenthesis for reference):\n- 'private' (Private Copyrighted)\n- 'cc_by_nc_nd' (CC Attribution Non-Commercial No Derivatives)\n- 'cc_by_nc_sa' (CC Attribution Non-Commercial Share Alike)\n- 'cc_by_nc' (CC Attribution Non-Commercial)\n- 'cc_by_nd' (CC Attribution No Derivatives)\n- 'cc_by_sa' (CC Attribution Share Alike)\n- 'cc_by' (CC Attribution)\n- 'public_domain' (Public Domain).",
        "type": "string",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "course[is_public]",
        "description": "Set to True if course is public to both authenticated and unauthenticated users.",
        "type": "boolean",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "course[is_public_to_auth_users]",
        "description": "Set to True if course is public only to authenticated users.",
        "type": "boolean",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "course[public_syllabus]",
        "description": "Set to True to make the course syllabus public.",
        "type": "boolean",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "course[public_syllabus_to_auth]",
        "description": "Set to True to make the course syllabus to public for authenticated users.",
        "type": "boolean",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "course[public_description]",
        "description": "A publicly visible description of the course.",
        "type": "string",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "course[allow_student_wiki_edits]",
        "description": "If True, students will be able to modify the course wiki.",
        "type": "boolean",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "course[allow_wiki_comments]",
        "description": "If True, course members will be able to comment on wiki pages.",
        "type": "boolean",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "course[allow_student_forum_attachments]",
        "description": "If True, students can attach files to forum posts.",
        "type": "boolean",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "course[open_enrollment]",
        "description": "Set to True if the course is open enrollment.",
        "type": "boolean",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "course[self_enrollment]",
        "description": "Set to True if the course is self enrollment.",
        "type": "boolean",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "course[restrict_enrollments_to_course_dates]",
        "description": "Set to True to restrict user enrollments to the start and end dates of the\ncourse.",
        "type": "boolean",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "course[term_id]",
        "description": "The unique ID of the term to create to course in.",
        "type": "integer",
        "format": "int64",
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "course[sis_course_id]",
        "description": "The unique SIS identifier.",
        "type": "string",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "course[integration_id]",
        "description": "The unique Integration identifier.",
        "type": "string",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "course[hide_final_grades]",
        "description": "If this option is set to True, the totals in student grades summary will\nbe hidden.",
        "type": "boolean",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "course[time_zone]",
        "description": "The time zone for the course. Allowed time zones are\n{http://www.iana.org/time-zones IANA time zones} or friendlier\n{http://api.rubyonrails.org/classes/ActiveSupport/TimeZone.html Ruby on Rails time zones}.",
        "type": "string",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "course[apply_assignment_group_weights]",
        "description": "Set to True to weight final grade based on assignment groups percentages.",
        "type": "boolean",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "course[storage_quota_mb]",
        "description": "Set the storage quota for the course, in megabytes. The caller must have\nthe \"Manage storage quotas\" account permission.",
        "type": "integer",
        "format": "int64",
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "offer",
        "description": "If this option is set to True, the course will be available to students\nimmediately.",
        "type": "boolean",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "course[event]",
        "description": "The action to take on each course.\n* 'claim' makes a course no longer visible to students. This action is also called \"unpublish\" on the web site.\n  A course cannot be unpublished if students have received graded submissions.\n* 'offer' makes a course visible to students. This action is also called \"publish\" on the web site.\n* 'conclude' prevents future enrollments and makes a course read-only for all participants. The course still appears\n  in prior-enrollment lists.\n* 'delete' completely removes the course from the web site (including course menus and prior-enrollment lists).\n  All enrollments are deleted. Course content may be physically deleted at a future date.\n* 'undelete' attempts to recover a course that has been deleted. (Recovery is not guaranteed; please conclude\n  rather than delete a course if there is any possibility the course will be used again.) The recovered course\n  will be unpublished. Deleted enrollments will not be recovered.",
        "type": "string",
        "format": None,
        "required": False,
        "deprecated": False,
        "enum": ["claim", "offer", "conclude", "delete", "undelete"]
    }, {
        "paramType": "form",
        "name": "course[default_view]",
        "description": "The type of page that users will see when they first visit the course\n* 'feed' Recent Activity Dashboard\n* 'wiki' Wiki Front Page\n* 'modules' Course Modules/Sections Page\n* 'assignments' Course Assignments List\n* 'syllabus' Course Syllabus Page\nother types may be added in the future",
        "type": "string",
        "format": None,
        "required": False,
        "deprecated": False,
        "enum": ["feed", "wiki", "modules", "syllabus", "assignments"]
    }, {
        "paramType": "form",
        "name": "course[syllabus_body]",
        "description": "The syllabus body for the course",
        "type": "string",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "course[grading_standard_id]",
        "description": "The grading standard id to set for the course.  If no value is provided for this argument the current grading_standard will be un-set from this course.",
        "type": "integer",
        "format": "int64",
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "course[course_format]",
        "description": "Optional. Specifies the format of the course. (Should be either 'on_campus' or 'online')",
        "type": "string",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "course[image_id]",
        "description": "This is a file ID corresponding to an image file in the course that will\nbe used as the course image.\nThis will clear the course's image_url setting if set.  If you attempt\nto provide image_url and image_id in a request it will fail.",
        "type": "integer",
        "format": "int64",
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "course[image_url]",
        "description": "This is a URL to an image to be used as the course image.\nThis will clear the course's image_id setting if set.  If you attempt\nto provide image_url and image_id in a request it will fail.",
        "type": "string",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "course[remove_image]",
        "description": "If this option is set to True, the course image url and course image\nID are both set to nil",
        "type": "boolean",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "query",
        "name": "course[blueprint]",
        "description": "Sets the course as a blueprint course. NOTE: The Blueprint Courses feature is in beta",
        "type": "boolean",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "course[blueprint_restrictions]",
        "description": "Sets a default set to apply to blueprint course objects when restricted,\nunless _use_blueprint_restrictions_by_object_type_ is enabled.\nSee the {api:Blueprint_Courses:BlueprintRestriction Blueprint Restriction} documentation",
        "type": "BlueprintRestriction",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "course[use_blueprint_restrictions_by_object_type]",
        "description": "When enabled, the _blueprint_restrictions_ parameter will be ignored in favor of\nthe _blueprint_restrictions_by_object_type_ parameter",
        "type": "boolean",
        "format": None,
        "required": False,
        "deprecated": False
    }, {
        "paramType": "form",
        "name": "course[blueprint_restrictions_by_object_type]",
        "description": "Allows setting multiple {api:Blueprint_Courses:BlueprintRestriction Blueprint Restriction}\nto apply to blueprint course objects of the matching type when restricted.\nThe possible object types are \"assignment\", \"attachment\", \"discussion_topic\", \"quiz\" and \"wiki_page\".\nExample usage:\n  course[blueprint_restrictions_by_object_type][assignment][content]=1",
        "type": "multiple BlueprintRestrictions",
        "format": None,
        "required": False,
        "deprecated": False
    }]
}
params = [{x['name']:1} for x in data['parameters'] if x['paramType'] == "form"]
# print(params)


def stuffer(o, i):
        [parent, child, val] = i
        if parent not in o.keys():
            o[parent] = {}
        o[parent][child] = val
        return o
    # except:
    #     [k, v] = i
    #     o[k] = v
    #     return o


# key_data = []
def reorg_keys(payload):
    output: dict = {}
    for entry in payload:
        k, v = list(entry.items())[0]
        x = pattern.findall(k)
        if x:
            [parent, child, val] = [x[0][0], x[0][1], v]
            if parent not in output.keys():
                output[parent] = {}
            output[parent][child] = val
        else:
            output[k] = v
    return output

# print(key_data)
# print('-'*48)
print(json.dumps(reorg_keys(params)))
