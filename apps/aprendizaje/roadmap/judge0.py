import base64
import time

import requests
from django.conf import settings

JUDGE0_BASE = 'https://judge0-ce.p.rapidapi.com'
LANG_IDS    = {'python': 71, 'javascript': 63}


def run_code(source_code: str, language: str = 'python', stdin: str = '') -> dict:
    lang_id = LANG_IDS.get(language, 71)
    key     = getattr(settings, 'JUDGE0_API_KEY', '')

    headers = {'Content-Type': 'application/json'}
    if key:
        headers['X-RapidAPI-Host'] = 'judge0-ce.p.rapidapi.com'
        headers['X-RapidAPI-Key']  = key

    payload = {
        'source_code':    base64.b64encode(source_code.encode()).decode(),
        'language_id':    lang_id,
        'stdin':          base64.b64encode(stdin.encode()).decode() if stdin else '',
        'base64_encoded': True,
    }

    try:
        resp  = requests.post(
            f'{JUDGE0_BASE}/submissions?base64_encoded=true&wait=false',
            json=payload,
            headers=headers,
            timeout=10,
        )
        token = resp.json().get('token')
        if not token:
            return _err('No se pudo crear el submission en Judge0')

        for _ in range(12):
            time.sleep(1)
            result = requests.get(
                f'{JUDGE0_BASE}/submissions/{token}?base64_encoded=true',
                headers=headers,
                timeout=10,
            ).json()
            if result.get('status', {}).get('id', 0) not in (1, 2):
                break

        return _parse(result)

    except requests.Timeout:
        return _err('Tiempo de espera agotado al conectar con Judge0')
    except Exception as e:
        return _err(f'Error: {e}')


def _decode(val):
    if not val:
        return ''
    try:
        return base64.b64decode(val).decode('utf-8', errors='replace')
    except Exception:
        return val


def _parse(raw):
    return {
        'stdout':    _decode(raw.get('stdout')),
        'stderr':    _decode(raw.get('stderr')),
        'status':    raw.get('status', {}).get('description', 'Unknown'),
        'status_id': raw.get('status', {}).get('id', 0),
        'time':      raw.get('time'),
        'memory':    raw.get('memory'),
        'accepted':  raw.get('status', {}).get('id') == 3,
    }


def _err(msg):
    return {
        'stdout': '', 'stderr': msg, 'status': 'Error',
        'status_id': 0, 'time': None, 'memory': None, 'accepted': False,
    }