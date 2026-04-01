document.addEventListener("DOMContentLoaded", function(){

/* ================= SIDEBAR ================= */

// 1. Fungsi untuk tombol (tetap pakai nama toggleMenu)
window.toggleMenu = function (event) {
    // Tambahkan baris ini agar klik pada tombol tidak dianggap klik 'luar layar'
    if (event) event.stopPropagation(); 

    const sidebar = document.getElementById("sidebar");
    if(sidebar) sidebar.classList.toggle("active");
};

// 2. Fungsi untuk mendeteksi klik di sembarang layar
document.addEventListener('click', function(event) {
    const sidebar = document.getElementById("sidebar");
    
    // Jika sidebar sedang aktif (muncul)
    if (sidebar && sidebar.classList.contains('active')) {
        // Cek apakah yang diklik bukan bagian dari sidebar
        if (!sidebar.contains(event.target)) {
            sidebar.classList.remove('active');
        }
    }
});

/* ================= NOTIFICATION ================= */

const notifBtn = document.getElementById("notifBtn");
const dropdown = document.getElementById("notifDropdown");
const notifData = document.getElementById("notif-data");

if (!notifBtn || !dropdown || !notifData) return;

const notifCountUrl = notifData.dataset.countUrl;
const notifDropdownUrl = notifData.dataset.dropdownUrl;

notifBtn.addEventListener("click", function(){

    dropdown.classList.toggle("show");

    fetch(notifDropdownUrl)
    .then(res => res.json())
    .then(data => {

        document.getElementById("notif-list").innerHTML = data.html;

        const badge = document.getElementById("notif-badge");

        if(!badge) return;

        badge.textContent = data.count;

        if(data.count > 0){
            badge.style.display = "inline-block";
        }else{
            badge.style.display = "none";
        }
    });
});

/* close outside click */
document.addEventListener("click", function(e){
    if(!notifBtn.contains(e.target) && !dropdown.contains(e.target)){
        dropdown.classList.remove("show");
    }
});

/* ================= NOTIF COUNT ================= */

window.updateNotification = function(){

    const badge = document.getElementById("notif-badge");

    if(!badge) return;

    fetch(notifCountUrl)
    .then(res => res.json())
    .then(data => {

        badge.textContent = data.count;

        badge.style.display =
            data.count > 0 ? "inline-flex" : "none";
    })
    .catch(err => console.log("notif error:", err));
};

// load awal
updateNotification();

// polling
setInterval(updateNotification, 8000);

});

/* ================= INFINITE SCROLL ================= */

let page = 2;
let loading = false;
let hasNext = true;

window.addEventListener("scroll", function () {

    if (loading || !hasNext) return;

    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 300) {

        loading = true;
        document.getElementById("loading").style.display = "block";

        fetch(`/accounts/load-posts/?page=${page}`)
            .then(res => res.json())
            .then(data => {

                document
                    .getElementById("post-container")
                    .insertAdjacentHTML("beforeend", data.html);

                hasNext = data.has_next;
                page++;

                loading = false;
                document.getElementById("loading").style.display = "none";
            });
    }
});

/* ================= FOLLOW BUTTON ================= */

document.addEventListener("DOMContentLoaded", function(){

    const followBtns = document.querySelectorAll(".followBtn");

    if (!followBtns.length) return;

    followBtns.forEach(btn => {
        btn.addEventListener("click", function(){

            const username = this.dataset.username;

            if (!username) {
                console.log("❌ username kosong");
                return;
            }

            fetch(`/accounts/follow/${username}/`, {
                method: "POST",
                headers:{
                    "X-CSRFToken": getCookie("csrftoken"),
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(res => res.json())
            .then(data => {

                if(data.success){

                    /* ================= BUTTON ================= */
                    if(data.following){
                        btn.textContent = "Following";
                        btn.classList.remove("btn-primary");
                        btn.classList.add("btn-outline-danger");
                    } else {
                        btn.textContent = "Follow";
                        btn.classList.remove("btn-outline-danger");
                        btn.classList.add("btn-primary");
                    }

                    /* ================= COUNTER ================= */
                    const followersCount = document.getElementById("followers-count");

                    if (followersCount && data.followers_count !== undefined) {
                        followersCount.textContent = data.followers_count;
                    }

                }

            })
            .catch(err => {
                console.log("❌ Error follow:", err);
            });

        });
    });

});

/* ================= CSRF ================= */

function getCookie(name){
    let cookieValue = null;

    document.cookie.split(';').forEach(cookie=>{
        cookie = cookie.trim();

        if(cookie.startsWith(name + '=')){
            cookieValue = decodeURIComponent(cookie.substring(name.length+1));
        }
    });

    return cookieValue;
}

/* containr tab */
function openTab(evt, tabName) {
    // Sembunyikan semua tab
    const contents = document.querySelectorAll('.tab-content');
    contents.forEach(content => content.classList.remove('show'));

    // Hilangkan status active dari semua tombol
    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(btn => btn.classList.remove('active'));

    // Tampilkan tab yang diklik
    document.getElementById(tabName).classList.add('show');
    evt.currentTarget.classList.add('active');
}