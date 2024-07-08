import json
import re
from inflect import engine


def resolve_schema_ref(spec, schema):
    if isinstance(schema, dict):
        if '$ref' in schema:
            ref = schema['$ref']
            parts = ref.split('/')
            current = spec
            for part in parts[1:]:  # Skip the first '#' part
                current = current[part]
            return resolve_schema_ref(spec, current)

        resolved_schema = {}
        for key, value in schema.items():
            if key in ['oneOf', 'allOf', 'anyOf']:
                resolved_schema[key] = [resolve_schema_ref(spec, item) for item in value]
            elif isinstance(value, dict):
                resolved_schema[key] = resolve_schema_ref(spec, value)
            elif isinstance(value, list):
                resolved_schema[key] = [resolve_schema_ref(spec, item) if isinstance(item, dict) else item for item in value]
            else:
                resolved_schema[key] = value
        return resolved_schema
    elif isinstance(schema, list):
        return [resolve_schema_ref(spec, item) for item in schema]
    else:
        return schema


def standardize_asset_name(name: str) -> str:
    p = engine()

    # clean
    name = name.lower().replace('_', '-')
    name = name.lower().replace(' ', '-')
    name = re.sub(r'[^a-z0-9-]', '', name)

    # Split the name into parts
    parts = name.split('-')

    # singularize
    invariant_words = {'synthesis', 'analysis', 'basis', 'thesis'}
    parts = [part if part in invariant_words else (p.singular_noun(part) or part) for part in parts]

    # Join the parts back together
    standardized_name = '-'.join(parts)

    # filter id/ids
    standardized_name = re.sub(r'-ids?$', '', standardized_name)
    return standardized_name


def get_last_route_segment(route: str) -> str:
    segments = route.strip('/').split('/')
    last_segment = segments[-1] if segments else ''
    return re.sub(r'^\{(.*)\}$', r'\1', last_segment)


def last_part_has_id(route: str) -> bool:
    parts = route.strip('/').split('/')
    last_part = parts[-1] if parts else ''

    return bool(re.match(r'^\{.*\}$', last_part) or last_part.endswith('_id'))


def parse_spec(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)