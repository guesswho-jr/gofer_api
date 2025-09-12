
SETTINGS_SCHEMA = {
    "type": "object",
    "properties": {
        "isPushNotificationsEnabled": {"type": "boolean"},
        "areEmailUpdatesEnabled": {"type": "boolean"}
    },
    # "required": ["name"],
    "additionalProperties": False
}

SETTINGS_DEFAULT = {
    "isPushNotificationsEnabled": True,
    "areEmailUpdatesEnabled": True
}