<!--0.2-->
![](https://raw.githubusercontent.com/irc-glory/evil-proxy/refs/heads/main/proxy/panel/EvilProxyBanner.png) v0.2
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
`python main.py`<br>(or)<br>`python main.py <target> <host> <port>`

**TIP:** To edit, remove or add a payload, go to the root directory, and configure the evil-script.js script from the panel folder as you wish.
# Showcase
![image](https://github.com/user-attachments/assets/2b6b92ea-48c1-4cfb-b758-82496647e2af)<br>
<br>
![image](https://github.com/user-attachments/assets/88ccfaea-7751-4e26-a055-0c1e1bd546d1)<br>
<br>
![image](https://github.com/user-attachments/assets/8408a264-58c3-4452-a5f3-85079c53d9da)
