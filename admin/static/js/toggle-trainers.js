document.addEventListener('DOMContentLoaded', function() {
    const toggle = document.querySelector('.dropdown-toggle');
    const content = document.querySelector('#trainers-content');

    toggle.addEventListener('click', function() {
        content.style.display = content.style.display === 'none' ? '' : 'none';
    });

    content.addEventListener('click', function(event) {
        event.stopPropagation(); // Prevents clicks inside the content from reaching the parent
    });
});