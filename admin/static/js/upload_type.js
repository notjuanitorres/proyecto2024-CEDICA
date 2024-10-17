document.addEventListener('DOMContentLoaded', function() {
    const radioButtons = document.querySelectorAll('input[name="upload_type"]');
    const urlField = document.getElementById('url-field');
    const fileField = document.getElementById('file-field');

    function toggleFields() {
        const selectedValue = document.querySelector('input[name="upload_type"]:checked').value;
        if (selectedValue === 'file') {
            urlField.style.display = 'none';
            fileField.style.display = 'block';
        } else if (selectedValue === 'url') {
            urlField.style.display = 'block';
            fileField.style.display = 'none';
        }
    }

    radioButtons.forEach(button => {
        button.addEventListener('change', toggleFields);
    });

    // Initial toggle based on the default selected radio button
    toggleFields();
});