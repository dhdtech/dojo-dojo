from flask import Flask, request, Response
import requests
import json
import os

app = Flask(__name__)

SITE_NAME = os.getenv("RANDOM_PROXY_URL")


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>", methods=["POST", "GET"], strict_slashes=False)
def _proxy(*args, **kwargs):
    if request.method == "GET":
        resp = requests.request(
            method=request.method,
            url=request.url.replace(request.host_url, SITE_NAME),
            headers={key: value for (key, value) in request.headers if key != "Host"},
            cookies=request.cookies,
            allow_redirects=False,
            timeout=300,
        )
    else:
        resp = requests.request(
            method=request.method,
            url=request.url.replace(request.host_url, SITE_NAME),
            headers={key: value for (key, value) in request.headers if key != "Host"},
            json=json.loads(request.data),
            cookies=request.cookies,
            allow_redirects=False,
            timeout=300,
        )

    excluded_headers = ["content-encoding", "content-length", "transfer-encoding", "connection"]
    headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]

    return Response(resp.content, resp.status_code, headers)
