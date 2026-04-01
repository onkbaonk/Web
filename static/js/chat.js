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
            (window.location.protocol === 'https:' ? 'wss://' : 'ws://') + 
            window.location.host + "/ws/chat/" + convoId + "/"
        );

        socket.onopen = function () {
            console.log("🟢 WebSocket connected");
        };

        socket.onmessage = function (e) {
            console.log("📩 Data diterima:", e.data); // Debugging
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

            // Gunakan insertAdjacentHTML agar lebih performant dan tidak merusak event listener lain
            const messageHtml = `
                <div class="msg ${isMe ? "sent" : "received"}">
                    ${data.message}
                    <div style="font-size:11px;opacity:0.6;margin-top:4px;">
                        ${data.time}
                    </div>
                    ${isMe ? '<div class="msg-status">✔</div>' : ''}
                </div>
            `;

            chatBox.insertAdjacentHTML('beforeend', messageHtml);
            chatBox.scrollTop = chatBox.scrollHeight;
        }; // <--- Tutup onmessage di sini setelah semua logika selesai

        socket.onclose = function (e) {
            console.log("🔴 WebSocket closed, reconnecting in 2s...", e.reason);
            setTimeout(connectSocket, 2000);
        };

        socket.onerror = function(err) {
            console.error("❌ WebSocket Error:", err);
        };
    }

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
    // =========================
    // WA MESSAGE
    // =========================
let selectedMsgId = null;
let pressTimer;
const msgMenu = document.getElementById('msg-menu');

// 1. Fungsi Long Press
document.addEventListener('touchstart', function(e) {
    const msgElement = e.target.closest('.msg');
    if (msgElement) {
        pressTimer = setTimeout(() => {
            selectedMsgId = msgElement.dataset.msgId; // Simpan ID pesan yang ditahan
            const isSent = msgElement.classList.contains('sent');
            
            // Munculkan menu di titik jari menyentuh
            msgMenu.style.display = 'flex';
            msgMenu.style.top = (e.touches[0].clientY - 20) + 'px';
            msgMenu.style.left = e.touches[0].clientX + 'px';

            // Sembunyikan Edit jika bukan pesan kita
            document.getElementById('btn-edit').style.display = isSent ? 'block' : 'none';
        }, 600); // Tahan sedikit lebih lama agar tidak bentrok dengan scroll
    }
});

document.addEventListener('touchend', () => clearTimeout(pressTimer));

// 2. Klik di mana saja untuk tutup menu
document.addEventListener('click', function(e) {
    if (!msgMenu.contains(e.target)) {
        msgMenu.style.display = 'none';
    }
});

// 3. Logika Tombol HAPUS
document.getElementById('btn-delete').addEventListener('click', function() {
    if (!selectedMsgId) return;
    
    if (confirm("Hapus pesan ini?")) {
        fetch(`/chat/delete-message/${selectedMsgId}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
            }
        }).then(res => {
            if (res.ok) {
                document.getElementById(`msg-${selectedMsgId}`).remove();
                msgMenu.style.display = 'none';
            }
        });
    }
});

// 4. Logika Tombol EDIT
document.getElementById('btn-edit').addEventListener('click', function() {
    if (!selectedMsgId) return;

    const msgDiv = document.querySelector(`#msg-${selectedMsgId} .msg-content`);
    const oldText = msgDiv.innerText;
    const newText = prompt("Edit pesan:", oldText);

    if (newText && newText !== oldText) {
        fetch(`/chat/edit-message/${selectedMsgId}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: "content=" + encodeURIComponent(newText)
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success') {
                msgDiv.innerText = data.content;
                msgMenu.style.display = 'none';
            }
        });
    }
});
});