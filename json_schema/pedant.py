from datetime import datetime
from typing import List
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name = 'John Doe'
    signup_ts: datetime = None
    friends: List[int] = []


external_data = {'id': '123', 'signup_ts': '2017-06-01 12:22', 'friends': [1, '2', b'3']}
user = User(**external_data)
print(user)
# > User id=123 name='John Doe' signup_ts=datetime.datetime(2017, 6, 1, 12, 22) friends=[1, 2, 3]
print(user.id)
# > 123

account = {
    "type": "object",
    "properties": {
        'name': 'string',
        'sis_account_id': 'string',
        'default_time_zone': 'string',
        'default_storage_quota_mb': 'intger',
        'default_user_storage_quota_mb': 'integer',
        'default_group_storage_quota_mb': 'integer',
        "settings": "Hash",
        'settings': {
            "type": "object",
            "properties": {
                "restrict_student_past_view": {
                    "type": "object",
                    "properties": {
                        "value": "boolean",
                        "locked": "boolean"
                    }
                },
                "restrict_student_future_view": {
                    "type": "object",
                    "properties": {
                        "value": "boolean",
                        "locked": "boolean"
                    }
                },
                "lock_all_announcements": {
                    "type": "object",
                    "properties": {
                        "value": "boolean",
                        "locked": "boolean"
                    }
                },
                "restrict_student_future_listing": {
                    "type": "object",
                    "properties": {
                        "value": "boolean",
                        "locked": "boolean"
                    }
                }
            }
        }
    }
}

print(account)
