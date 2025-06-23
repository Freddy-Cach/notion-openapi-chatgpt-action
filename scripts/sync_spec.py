import json
import time
import requests
from bs4 import BeautifulSoup
import yaml

BASE_URL = "https://developers.notion.com"


def gather_endpoints():
    html = requests.get(f"{BASE_URL}/reference").text
    soup = BeautifulSoup(html, "html.parser")
    slugs = sorted({a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('/reference/')})
    endpoints = set()
    for slug in slugs:
        resp = requests.get(BASE_URL + slug)
        time.sleep(0.5)
        s = BeautifulSoup(resp.text, "html.parser")
        script = s.find('script', id='ssr-props')
        if not script:
            continue
        data = json.loads(script['data-initial-props'])
        api = data.get('doc', {}).get('api')
        if api and api.get('url') and api.get('method'):
            path = api['url']
            if path.startswith('/v1'):
                path = path[len('/v1'):] or '/'  # strip version prefix
            endpoints.add((api['method'].upper(), path))
    return endpoints


# explicit operationIds used by the Notion docs
OPERATION_IDS = {
    ("DELETE", "/blocks/{block_id}"): "deleteBlock",
    ("GET", "/blocks/{block_id}"): "retrieveBlock",
    ("PATCH", "/blocks/{block_id}"): "updateBlock",
    ("GET", "/blocks/{block_id}/children"): "retrieveBlockChildren",
    ("PATCH", "/blocks/{block_id}/children"): "appendBlockChildren",
    ("POST", "/comments"): "createComment",
    ("GET", "/comments"): "listComments",
    ("POST", "/databases"): "createDatabase",
    ("GET", "/databases/{database_id}"): "retrieveDatabase",
    ("PATCH", "/databases/{database_id}"): "updateDatabase",
    ("POST", "/databases/{database_id}/query"): "queryDatabase",
    ("POST", "/file_uploads"): "createFileUpload",
    ("GET", "/file_uploads"): "listFileUploads",
    ("GET", "/file_uploads/{file_upload_id}"): "retrieveFileUpload",
    ("POST", "/file_uploads/{file_upload_id}/send"): "sendFileUpload",
    ("POST", "/file_uploads/{file_upload_id}/complete"): "completeFileUpload",
    ("POST", "/oauth/token"): "createAccessToken",
    ("POST", "/oauth/introspect"): "introspectToken",
    ("POST", "/oauth/revoke"): "revokeToken",
    ("POST", "/pages"): "createPage",
    ("GET", "/pages/{page_id}"): "retrievePage",
    ("PATCH", "/pages/{page_id}"): "updatePage",
    ("GET", "/pages/{page_id}/properties/{property_id}"): "retrievePagePropertyItem",
    ("POST", "/search"): "search",
    ("GET", "/users"): "listUsers",
    ("GET", "/users/{user_id}"): "retrieveUser",
    ("GET", "/users/me"): "retrieveBotUser",
}

def main():
    with open('public/notion-openapi.json') as f:
        spec = json.load(f)

    old_paths = spec.get('paths', {})
    old_endpoints = {(m.upper(), p) for p, ops in old_paths.items() for m in ops.keys()}

    new_endpoints = gather_endpoints()

    added = new_endpoints - old_endpoints
    removed = old_endpoints - new_endpoints

    new_paths = {}
    for method, path in sorted(new_endpoints, key=lambda x: (x[1], x[0])):
        op = old_paths.get(path, {}).get(method.lower(), {"responses": {}})
        default_id = f"{method.lower()}_{path.strip('/').replace('/', '_').replace('{', '').replace('}', '')}"
        op["operationId"] = OPERATION_IDS.get((method, path), op.get("operationId", default_id))
        new_paths.setdefault(path, {})[method.lower()] = op

    spec['paths'] = new_paths

    with open('public/notion-openapi.json', 'w') as f:
        json.dump(spec, f, indent=2, ensure_ascii=False)
    with open('public/notion-openapi.yaml', 'w') as f:
        yaml.safe_dump(spec, f, sort_keys=False)

    # update README snippet
    readme = open('README.md').read()
    start = readme.index('```yaml') + len('```yaml')
    end = readme.index('```', start)
    new_readme = readme[:start] + '\n' + yaml.safe_dump(spec, sort_keys=False) + '```' + readme[end+3:]
    with open('README.md', 'w') as f:
        f.write(new_readme)

    print('before', len(old_endpoints))
    print('after', len(new_endpoints))
    print('added', sorted(added))
    print('removed', sorted(removed))


if __name__ == '__main__':
    main()
