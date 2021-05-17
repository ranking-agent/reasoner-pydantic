""" Test utilities """

import httpx
import json

def fill_http_refs(obj):
    """Find any refs that point to a web address and pull in their schemas"""
    if "$ref" in obj and obj["$ref"].startswith("http"):
        with httpx.Client() as client:
            ref_schema = client.get(obj.pop("$ref")).json()
            # Process nested refs
            ref_schema = json.loads(
                json.dumps(ref_schema),
                object_hook = fill_http_refs,
            )
            # TODO Fix ref locations
            # Update the object
            obj |= ref_schema

    return obj

def update_ref_prefix(obj):
    """Update the prefix in the $ref property"""
    if "$ref" in obj:
        if obj["$ref"].startswith("#/definitions/"):
            ref = "#/components/schemas" + obj["$ref"][13:]
        else:
            ref = obj["$ref"]
        return {
            "$ref": ref
        }
    return obj


def strip_extra_properties(obj):
    """Remove extra added properties and update some that are problematic"""

    # This is potentially problematic in general... #
    if "anyOf" in obj:
        obj["oneOf"] = obj.pop("anyOf")
    #################################################

    obj.pop("title", None)
    obj.pop("description", None)
    obj.pop("example", None)
    obj.pop("externalDocs", None)
    if obj.get("additionalProperties", None) is True:
        obj.pop("additionalProperties")
    if list(obj.keys()) == ["allOf"]:
        if len(obj["allOf"]) == 1:
            return obj["allOf"][0]
    return obj
