![](https://raw.githubusercontent.com/irc-glory/evil-proxy/refs/heads/main/proxy/panel/EvilProxyBanner.png) v0.1
# Evil Proxy
An HTTP proxy designed to perform MITM phishing attacks, allowing users to inject JavaScript payloads into the victim's browser in the background, while displaying the live content of the target domain used to attack the victim.
<br><br>
The project is still under development, and any contributions are welcome. There are currently some limitations to Cloudflare DDoS protection pages and other related services, but many patches will be coming soon.
# Setup
1. Install project:<br>
`gh repo clone irc-glory/evil-proxy`<br>
`cd evil-proxy`
2. Install modules:<br>
`pip install -r requirements.txt`
3. Launch tool:<br>
`python main.py`

**TIP:** To edit, remove or add a payload, go to the root directory, and configure the evil-script.js script from the panel folder as you wish.
# Showcase
![image](https://github.com/user-attachments/assets/2b6b92ea-48c1-4cfb-b758-82496647e2af)<br>
<br>
![image](https://github.com/user-attachments/assets/e757d3ca-6fa9-4d67-8041-64ea65c75295)

