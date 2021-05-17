"""Test alignment with OpenAPI schema."""
from tests.utils import fill_http_refs, strip_extra_properties, update_ref_prefix
import httpx
import json

import yaml

from reasoner_pydantic import components

response = httpx.get("https://raw.githubusercontent.com/NCATSTranslator/ReasonerAPI/edeutsch-operations/TranslatorReasonerAPI.yaml")
reference_schemas = yaml.load(
    response.text,
    Loader=yaml.FullLoader,
)["components"]["schemas"]


def preprocess_schema_object_hook(obj):
    """Object hook for processing a schema into the correct format"""
    obj = fill_http_refs(obj)
    obj = update_ref_prefix(obj)
    obj = strip_extra_properties(obj)
    return obj

reference_schemas = json.loads(
    json.dumps(reference_schemas),
    object_hook=preprocess_schema_object_hook,
)

def test_openapi():
    """Test alignment with OpenAPI schema."""
    for obj in components:
        print(obj.__name__)

        schema = obj.schema_json(
            ref_template = "#/components/schemas/{model}"
        )
        schema = json.loads(schema, object_hook = preprocess_schema_object_hook)

        schema.pop("definitions", None)
        try:
            assert schema == reference_schemas[obj.__name__]
        except AssertionError:
            print("  produced schema: ", schema)
            print("  reference schema: ", reference_schemas[obj.__name__])
            raise
