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
            endpoints.add((api['method'].upper(), api['url']))
    return endpoints


# explicit operationIds used by the Notion docs
OPERATION_IDS = {
    ("DELETE", "/v1/blocks/{block_id}"): "deleteBlock",
    ("GET", "/v1/blocks/{block_id}"): "retrieveBlock",
    ("PATCH", "/v1/blocks/{block_id}"): "updateBlock",
    ("GET", "/v1/blocks/{block_id}/children"): "retrieveBlockChildren",
    ("PATCH", "/v1/blocks/{block_id}/children"): "appendBlockChildren",
    ("POST", "/v1/comments"): "createComment",
    ("GET", "/v1/comments"): "listComments",
    ("POST", "/v1/databases"): "createDatabase",
    ("GET", "/v1/databases/{database_id}"): "retrieveDatabase",
    ("PATCH", "/v1/databases/{database_id}"): "updateDatabase",
    ("POST", "/v1/databases/{database_id}/query"): "queryDatabase",
    ("POST", "/v1/file_uploads"): "createFileUpload",
    ("GET", "/v1/file_uploads"): "listFileUploads",
    ("GET", "/v1/file_uploads/{file_upload_id}"): "retrieveFileUpload",
    ("POST", "/v1/file_uploads/{file_upload_id}/send"): "sendFileUpload",
    ("POST", "/v1/file_uploads/{file_upload_id}/complete"): "completeFileUpload",
    ("POST", "/v1/oauth/token"): "createAccessToken",
    ("POST", "/v1/oauth/introspect"): "introspectToken",
    ("POST", "/v1/oauth/revoke"): "revokeToken",
    ("POST", "/v1/pages"): "createPage",
    ("GET", "/v1/pages/{page_id}"): "retrievePage",
    ("PATCH", "/v1/pages/{page_id}"): "updatePage",
    ("GET", "/v1/pages/{page_id}/properties/{property_id}"): "retrievePagePropertyItem",
    ("POST", "/v1/search"): "search",
    ("GET", "/v1/users"): "listUsers",
    ("GET", "/v1/users/{user_id}"): "retrieveUser",
    ("GET", "/v1/users/me"): "retrieveBotUser",
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
        if "operationId" not in op:
            op["operationId"] = OPERATION_IDS.get((method, path)) or (
                f"{method.lower()}_{path.strip('/').replace('/', '_').replace('{', '').replace('}', '')}"
            )
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
