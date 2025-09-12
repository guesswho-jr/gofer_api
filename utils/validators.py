from typing import Any, Dict
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from jsonschema import validate
import jsonschema

def validate_json(schema: Dict[str, Any], toBeValidated: Dict[str, Any]):
    try:
        validate(toBeValidated, schema)
    except jsonschema.ValidationError:
        raise ValidationError(_("Invalid data"))