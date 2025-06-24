import sys
import yaml
import json
from pathlib import Path


NOTION_SERVER_URL = "https://api.notion.com/v1"


def fix_servers(data):
    """Ensure the servers section matches the official Notion base URL."""
    data["servers"] = [{"url": NOTION_SERVER_URL}]
    return data


def remove_v1_prefix(data):
    """Remove '/v1' prefix from all path keys."""
    paths = data.get("paths", {})
    new_paths = {}
    for path, ops in paths.items():
        if path.startswith("/v1/"):
            path = path[3:]
        new_paths[path] = ops
    data["paths"] = new_paths
    return data


def remove_parameters_component(data):
    comps = data.get("components")
    if isinstance(comps, dict) and "parameters" in comps:
        comps.pop("parameters")
    return data

def inline_headers(data):
    header_notion_version = {
        'name': 'Notion-Version',
        'in': 'header',
        'required': True,
        'description': 'API version',
        'schema': {'type': 'string', 'default': '2022-06-28'}
    }
    header_json_content_type = {
        'name': 'Content-Type',
        'in': 'header',
        'required': True,
        'description': 'Always application/json for Notion POST/PATCH bodies',
        'schema': {'type': 'string', 'enum': ['application/json']}
    }

    for path in data.get('paths', {}).values():
        for op in path.values():
            if not isinstance(op, dict):
                continue
            params = op.get('parameters')
            if not params:
                params = []
            new_params = []
            seen = set()
            for p in params:
                if isinstance(p, dict) and '$ref' in p:
                    ref = p['$ref']
                    if ref == '#/components/parameters/NotionVersion':
                        p = header_notion_version
                    elif ref == '#/components/parameters/JsonContentType':
                        p = header_json_content_type
                name = p.get('name') if isinstance(p, dict) else None
                if name in seen:
                    continue
                if name:
                    seen.add(name)
                new_params.append(p)

            # drop Content-Type if no requestBody
            if 'requestBody' not in op:
                new_params = [p for p in new_params if not (isinstance(p, dict) and p.get('name') == 'Content-Type')]

            if not any(isinstance(p, dict) and p.get('name') == 'Notion-Version' for p in new_params):
                new_params.append(header_notion_version)

            op['parameters'] = new_params
    return data

class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

def process_yaml(path):
    data = yaml.safe_load(Path(path).read_text())
    data = fix_servers(data)
    data = remove_v1_prefix(data)
    data = inline_headers(data)
    data = remove_parameters_component(data)
    Path(path).write_text(
        yaml.dump(data, sort_keys=False, Dumper=NoAliasDumper)
    )


def process_json(path):
    data = json.loads(Path(path).read_text())
    data = fix_servers(data)
    data = remove_v1_prefix(data)
    data = inline_headers(data)
    data = remove_parameters_component(data)
    Path(path).write_text(json.dumps(data, indent=2))


def main():
    for file in sys.argv[1:]:
        if file.endswith('.yaml') or file.endswith('.yml'):
            process_yaml(file)
        elif file.endswith('.json'):
            process_json(file)

if __name__ == '__main__':
    main()
