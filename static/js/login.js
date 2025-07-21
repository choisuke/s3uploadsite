document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('login-form');
    var overlay = document.getElementById('loading-overlay');
    if (form) {
        form.addEventListener('submit', function() {
            if (overlay) {
                overlay.style.display = 'flex';
            }
        });
    }
});
