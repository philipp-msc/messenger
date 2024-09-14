document.addEventListener("DOMContentLoaded", function() {
    const conn = new WebSocket("ws://127.0.0.1:8001/ws/chat/");
    const msg = document.getElementById("msg");
    const log = document.getElementById("log");
    const form = document.getElementById("form");
    const sendGeoBtn = document.getElementById("send_geo");
    const usernameInput = document.getElementById("username");
    const avatarInput = document.getElementById("avatar");
    const updateInfoBtn = document.getElementById("update-info");

    function appendLog(item) {
        const doScroll = log.scrollTop > log.scrollHeight - log.clientHeight - 1;
        log.appendChild(item);
        if (doScroll) {
            log.scrollTop = log.scrollHeight - log.clientHeight;
        }
    }

    form.onsubmit = function () {
        if (!conn) {
            return false;
        }
        if (!msg.value) {
            return false;
        }
        conn.send(JSON.stringify({ message: msg.value }));
        msg.value = "";
        return false;
    };

    sendGeoBtn.onclick = function () {
        if (!conn) {
            return false;
        }
        if ("geolocation" in navigator) {
            navigator.geolocation.getCurrentPosition((position) => {
                const { coords } = position;
                conn.send(JSON.stringify({ lat: coords.latitude, lng: coords.longitude }));
            });
        }
        return false;
    };

    if (window["WebSocket"]) {
        conn.onclose = function (evt) {
            const item = document.createElement("div");
            item.innerHTML = "<b>Connection closed.</b>";
            appendLog(item);
        };
        conn.onmessage = function (evt) {
            const messages = evt.data.split('\n');
            for (let i = 0; i < messages.length; i++) {
                const item = document.createElement("div");
                let message = messages[i];
                try {
                    message = JSON.parse(message);
                    if (message.lat && message.lng) {
                        message = `https://www.openstreetmap.org/#map=18/${message.lat}/${message.lng}`;
                    } else {
                        message = message.message;
                    }
                } catch (e) {
                    // Ничего не делать
                }
                item.innerText = message;
                appendLog(item);
            }
        };
    } else {
        const item = document.createElement("div");
        item.innerHTML = "<b>Your browser does not support WebSockets.</b>";
        appendLog(item);
    }
});


