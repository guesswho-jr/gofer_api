from utils.validators import validate_json

BASIC_RULES = {
    "additionalProperties": False
}

SETTINGS_SCHEMA = {
    "type": "object",
    "properties": {
        "isPushNotificationsEnabled": {"type": "boolean"},
        "areEmailUpdatesEnabled": {"type": "boolean"}
    },
    # "required": ["name"],
    **BASIC_RULES
}

FOLLOWS_SCHEMA = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "action_type": {"type": "string", "enum": ["follow", "unfollow"]}
    },
    "required": ["username", "action_type"],
    **BASIC_RULES
}

LOCATION_SCHEMA = {
    "type": "object",
    "properties": {
         "name": {"type": "string"},
         "latitude": {"type": "string"},
         "longitude": {"type": "string"}
    },
    "required": ["name", "longitude", "latitude"],
    **BASIC_RULES
}

def default_settings():
    return {
    "isPushNotificationsEnabled": True,
    "areEmailUpdatesEnabled": True
}
    
def validate_settings_schema(value):
    # if type(value) == str:
    #     value = json.loads(value)
    return validate_json(SETTINGS_SCHEMA, value)
def validate_follows_schema(value):
    # value = json.loads(value)
    return validate_json(FOLLOWS_SCHEMA, value)
def validate_location_schema(value):
    return validate_json(LOCATION_SCHEMA, value)