document.addEventListener('DOMContentLoaded', function () {
    var dropZone = document.getElementById('drop-zone');
    var overlay = document.getElementById('loading-overlay');
    function showLoader() {
        if (overlay) {
            overlay.style.display = 'flex';
        }
    }

    if (!dropZone) return;

    dropZone.addEventListener('dragover', function (e) {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', function () {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', function (e) {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        uploadFiles(e.dataTransfer.files);
    });

    function uploadFiles(files) {
        var formData = new FormData();
        for (var i = 0; i < files.length; i++) {
            formData.append('files', files[i]);
        }
        showLoader();
        fetch('/upload', {
            method: 'POST',
            body: formData
        }).then(function () { window.location.reload(); });
    }

    document.querySelectorAll('.delete-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            var filename = btn.getAttribute('data-filename');
            showLoader();
            fetch('/delete/' + encodeURIComponent(filename), { method: 'POST' })
                .then(function(){ window.location.reload(); });
        });
    });

    var searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function() {
            showLoader();
        });
    }
    var resetBtn = document.getElementById('reset-btn');
    if (resetBtn) {
        resetBtn.addEventListener('click', function() {
            showLoader();
        });
    }
});
