// static/js/main.js
function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    if (sidebar) {
        sidebar.classList.toggle("active");
    }
}

// Menutup sidebar jika layar diklik (opsional tapi bagus untuk mobile)
document.addEventListener('click', function(event) {
    const sidebar = document.getElementById("sidebar");
    const menuBtn = document.querySelector('button[onclick="toggleSidebar()"]');
    
    if (sidebar && sidebar.classList.contains('active')) {
        if (!sidebar.contains(event.target) && event.target !== menuBtn) {
            sidebar.classList.remove('active');
        }
    }
});