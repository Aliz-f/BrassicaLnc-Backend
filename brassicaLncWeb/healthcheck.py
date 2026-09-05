"""Probe Gunicorn, Django, and PostgreSQL using only the standard library."""
import os
from urllib.request import ProxyHandler, Request, build_opener


host = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')[0].strip().lstrip('.')
if host == '*':
    host = 'localhost'
request = Request('http://127.0.0.1:8000/healthz/', headers={
    'Host': host,
    # Exercise HTTPS behavior without redirecting the internal probe to nginx.
    'X-Forwarded-Proto': 'https',
})
with build_opener(ProxyHandler({})).open(request, timeout=4) as response:
    if response.status != 200:
        raise SystemExit(1)
