
from utils.validators import validate_json


SETTINGS_SCHEMA = {
    "type": "object",
    "properties": {
        "isPushNotificationsEnabled": {"type": "boolean"},
        "areEmailUpdatesEnabled": {"type": "boolean"}
    },
    # "required": ["name"],
    "additionalProperties": False
}

def default_settings():
    return {
    "isPushNotificationsEnabled": True,
    "areEmailUpdatesEnabled": True
}
    
def validate_settings_schema(value):
    return validate_json(SETTINGS_SCHEMA, value)