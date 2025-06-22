import json
import time
import requests
from bs4 import BeautifulSoup

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
        new_paths.setdefault(path, {})[method.lower()] = op

    spec['paths'] = new_paths

    with open('public/notion-openapi.json', 'w') as f:
        json.dump(spec, f, indent=2, ensure_ascii=False)

    print('before', len(old_endpoints))
    print('after', len(new_endpoints))
    print('added', sorted(added))
    print('removed', sorted(removed))


if __name__ == '__main__':
    main()
