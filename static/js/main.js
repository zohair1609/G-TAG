document.addEventListener('DOMContentLoaded', function() {
    // Drag and drop functionality
    const uploadContainer = document.getElementById('upload-container');
    const fileInput = document.getElementById('file-input');
    const uploadForm = document.getElementById('upload-form');
    const uploadFileName = document.getElementById('upload-filename');
    const loadingOverlay = document.getElementById('loading-overlay');

    if (uploadContainer) {
        // Trigger file input when clicking on the upload container
        uploadContainer.addEventListener('click', function() {
            fileInput.click();
        });

        // Display file name when a file is selected
        fileInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                uploadFileName.textContent = this.files[0].name;
                uploadContainer.classList.add('has-file');
            }
        });

        // Drag and drop events
        uploadContainer.addEventListener('dragover', function(e) {
            e.preventDefault();
            uploadContainer.classList.add('drag-over');
        });

        uploadContainer.addEventListener('dragleave', function() {
            uploadContainer.classList.remove('drag-over');
        });

        uploadContainer.addEventListener('drop', function(e) {
            e.preventDefault();
            uploadContainer.classList.remove('drag-over');
            
            if (e.dataTransfer.files && e.dataTransfer.files[0]) {
                fileInput.files = e.dataTransfer.files;
                uploadFileName.textContent = e.dataTransfer.files[0].name;
                uploadContainer.classList.add('has-file');
            }
        });
    }

    // Handle form submission
    if (uploadForm) {
        uploadForm.addEventListener('submit', function() {
            if (loadingOverlay) {
                loadingOverlay.classList.add('active');
            }
        });
    }

    // Toggle switches for checklist items
    const checklistSwitches = document.querySelectorAll('.checklist-switch');
    checklistSwitches.forEach(function(switchElement) {
        switchElement.addEventListener('change', function() {
            const listItem = this.closest('.checklist-item');
            if (this.checked) {
                listItem.classList.add('passed');
                listItem.classList.remove('failed');
            } else {
                listItem.classList.add('failed');
                listItem.classList.remove('passed');
            }
            updateSummary();
        });
    });

    // Update summary based on checklist items
    function updateSummary() {
        const checklistItems = document.querySelectorAll('.checklist-item');
        const passedItems = document.querySelectorAll('.checklist-item.passed');
        const totalItems = checklistItems.length;
        const passedCount = passedItems.length;
        
        const summaryStatus = document.getElementById('summary-status');
        const summaryBadge = document.getElementById('summary-badge');
        
        if (summaryStatus && summaryBadge) {
            summaryStatus.textContent = `${passedCount}/${totalItems} checks passed`;
            
            if (passedCount === totalItems) {
                summaryBadge.textContent = 'PASS';
                summaryBadge.className = 'summary-badge badge-pass';
            } else {
                summaryBadge.textContent = 'FAIL';
                summaryBadge.className = 'summary-badge badge-fail';
            }
        }
    }

    // Generate report functionality
    const generateReportBtn = document.getElementById('generate-report');
    if (generateReportBtn) {
        generateReportBtn.addEventListener('click', function() {
            // Show toast message
            showToast('Report generated successfully!', 'success');
        });
    }

    // Toast notification function
    function showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast ${type === 'success' ? 'toast-success' : 'toast-error'}`;
        toast.textContent = message;
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.classList.add('show');
        }, 100);
        
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                document.body.removeChild(toast);
            }, 300);
        }, 3000);
    }

    // Initialize any functions that should run on load
    if (document.querySelectorAll('.checklist-item').length > 0) {
        updateSummary();
    }
}); 