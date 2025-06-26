import json
from pathlib import Path
import sys

def clean(path):
    data = json.loads(Path(path).read_text())
    for ops in data.get('paths', {}).values():
        for op in ops.values():
            if not isinstance(op, dict):
                continue
            body_props = set()
            rb = op.get('requestBody')
            if isinstance(rb, dict):
                content = rb.get('content', {}).get('application/json', {})
                schema = content.get('schema', {})
                if isinstance(schema, dict):
                    props = schema.get('properties')
                    if isinstance(props, dict):
                        body_props = set(props.keys())
            params = op.get('parameters') or []
            new_params = []
            for p in params:
                if isinstance(p, dict):
                    name = p.get('name')
                    if name and name in body_props:
                        continue
                    schema = p.get('schema')
                    if isinstance(schema, dict) and schema.get('type') == 'object' \
                       and 'properties' not in schema and 'additionalProperties' not in schema:
                        schema['additionalProperties'] = True
                new_params.append(p)
            if new_params or 'parameters' in op:
                op['parameters'] = new_params
    Path(path).write_text(json.dumps(data, indent=2))

if __name__ == '__main__':
    for path in sys.argv[1:]:
        clean(path)
