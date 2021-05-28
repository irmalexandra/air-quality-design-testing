import json
import jsonschema
from jsonschema import validate


def validateJson(jsonData):
    with open("../JsonSchema/loftgaediSchema.json") as fd:
        loftgaedi_schema = json.load(fd)
    try:
        validate(instance=jsonData, schema=loftgaedi_schema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True
