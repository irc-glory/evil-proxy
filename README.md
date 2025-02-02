![](https://raw.githubusercontent.com/irc-glory/evil-proxy/refs/heads/main/proxy/panel/EvilProxyBanner.png) v0.3
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

**TIP:** To edit, remove or add a payload, go to the proxy directory, and configure them from the payloads folder as you wish.
# Showcase
![image](https://github.com/user-attachments/assets/2b6b92ea-48c1-4cfb-b758-82496647e2af)<br>
<br>

<p align="center">
<h1 align="center">Sponsorship</h1>

<p align="center">If you find my work valuable, you can show your support by sponsoring me. 
  Your contribution will help me maintain and improve my projects, and it will encourage me to create more useful content.</p>

<p align="center">
  <a href="https://buymeacoffee.com/irc.glory"><img src="https://img.shields.io/badge/-Buy%20me%20a%20coffee-orange?style=for-the-badge&logo=buy-me-a-coffee&logoColor=white" alt="Buy me a coffee"></a>
</p>


<p align="center">Thank you to the following people for their support:</p>

<div align="center">
  <a href="https://github.com/irc-glory/evil-proxy/stargazers">
    <img src="https://reporoster.com/stars/dark/irc-glory/evil-proxy" alt="Stargazers" title="Stargazers" width="400" height="auto">
  </a>
</div>