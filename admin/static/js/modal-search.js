function createModalSearch({
    openButtonId,
    modalId,
    searchInputId,
    listId,
    nameInputId,
    idInputId,
    apiUrl,
    createRowContent
}) {
    const openModalButton = document.getElementById(openButtonId);
    const modal = document.getElementById(modalId);
    const searchInput = document.getElementById(searchInputId);
    const list = document.getElementById(listId);
    const nameInput = document.getElementById(nameInputId);
    const idInput = document.getElementById(idInputId);

    // Open modal
    openModalButton.addEventListener('click', (e) => {
        modal.classList.add('is-active');
        e.preventDefault();
    });

    // Close modal
    document.querySelectorAll('.modal-background, .delete, .modal-card-foot .button').forEach(($close) => {
        $close.addEventListener('click', (event) => {
            event.preventDefault();
            modal.classList.remove('is-active');
        });
    });

    // Search items
    searchInput.addEventListener('input', () => {
        const query = searchInput.value.toLowerCase();
        fetch(`${apiUrl}?search=${query}`)
            .then(response => response.json())
            .then(data => {
                list.innerHTML = '';
                data.forEach(item => {
                    const row = document.createElement('tr');
                    row.innerHTML = createRowContent(item);
                    list.appendChild(row);
                });

                document.querySelectorAll('.select-item-button').forEach(button => {
                    button.addEventListener('click', (event) => {
                        event.preventDefault();
                        const name = event.target.getAttribute('data-name');
                        const email = event.target.getAttribute('data-email');
                        const id = event.target.getAttribute('data-id');
                        nameInput.value = `${name} (Email: ${email})`;
                        idInput.value = id;
                        modal.classList.remove('is-active');
                    });
                });
            });
    });
}