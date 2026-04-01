console.log("CHAT JS LOADED");

document.addEventListener("DOMContentLoaded", function () {

    const chatForm = document.getElementById("chat-form");
    const chatInput = document.querySelector(".chat-textarea");
    const chatBox = document.getElementById("chat-box");

    // ✅ SAFE CHECK (hindari crash)
    if (!chatForm || !chatInput || !chatBox) {
        console.log("❌ Chat element tidak ditemukan");
        return;
    }

    const convoId = chatBox.dataset.convo;
    const username = chatBox.dataset.user;

    if (!convoId) {
        console.log("❌ convoId tidak ada");
        return;
    }

    console.log("✅ Chat siap:", convoId);

    // =========================
    // AUTO SCROLL
    // =========================
    chatBox.scrollTop = chatBox.scrollHeight;

    // =========================
    // AUTO RESIZE TEXTAREA
    // =========================
    chatInput.addEventListener("input", function () {
        this.style.height = "auto";
        this.style.height = this.scrollHeight + "px";
    });

    // =========================
    // ENTER = SEND
    // =========================
    chatInput.addEventListener("keydown", function (e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            chatForm.requestSubmit();
        }
    });

    // =========================
    // WEBSOCKET (REALTIME)
    // =========================
    let socket = null;

    function connectSocket() {
        socket = new WebSocket(
            "ws://" + window.location.host + "/ws/chat/" + convoId + "/"
        );

        socket.onopen = function () {
            console.log("🟢 WebSocket connected");
        };

        
        socket.onmessage = function (e) {
            const data = JSON.parse(e.data);

            // =========================
            // READ RECEIPT
            // =========================
            if (data.type === "read") {
              document.querySelectorAll(".msg.sent .msg-status")
                .forEach(el => {
                  el.innerText = "✔✔";
                });
              return;
            }

            // =========================
            // MESSAGE
            // =========================
            if (!data.message) return;

            const isMe = data.sender === username;

            chatBox.innerHTML += `
                <div class="msg ${isMe ? "sent" : "received"}">
                ${data.message}
                <div style="font-size:11px;opacity:0.6;margin-top:4px;">
                ${data.time}
                </div>
                ${isMe ? '<div class="msg-status">✔</div>' : ''}
                </div>
                `;

                chatBox.scrollTop = chatBox.scrollHeight;
        };

        socket.onclose = function () {
            console.log("🔴 WebSocket closed, reconnecting...");
            setTimeout(connectSocket, 2000);
        };
    }

    connectSocket();

    // =========================
    // SEND MESSAGE (AJAX)
    // =========================
    chatForm.addEventListener("submit", function (e) {
        e.preventDefault();

        const message = chatInput.value.trim();
        if (!message) return;

        fetch(chatForm.action, {
            method: "POST",
            headers: {
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: "content=" + encodeURIComponent(message)
        })
        .then(res => res.json())
        .then(data => {

            // ⚠️ Tambahkan hanya jika websocket belum kirim
            // (hindari double message)
            if (!socket || socket.readyState !== WebSocket.OPEN) {
                chatBox.innerHTML += `
                    <div class="msg sent">
                        ${data.message}
                        <div style="font-size:11px;opacity:0.6;margin-top:4px;">
                            ${data.time}
                        </div>
                    </div>
                `;

                chatBox.scrollTop = chatBox.scrollHeight;
            }

            chatInput.value = "";
            chatInput.style.height = "auto";
        });
    });

});