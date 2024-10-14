document.addEventListener('DOMContentLoaded', () => {
    // Initialize JYA modal search
    createModalSearch({
        openButtonId: 'openModalButtonJya',
        modalId: 'jyaModal',
        searchInputId: 'searchJya',
        listId: 'jyaList',
        nameInputId: 'jya_info',
        idInputId: 'jya_id',
        apiUrl: '/equipo/api',
        createRowContent: (item) => `
            <td>${item.name}</td>
            <td>${item.email}</td>
            <td><button class="button is-small is-info select-item-button" data-id="${item.id}" data-name="${item.name}" data-email="${item.email}">Seleccionar</button></td>
        `
    });

    // Initialize Employee modal search
    createModalSearch({
        openButtonId: 'openModalButton',
        modalId: 'employeeModal',
        searchInputId: 'searchEmployee',
        listId: 'employeeList',
        nameInputId: 'employee_info',
        idInputId: 'employee_id',
        apiUrl: '/equipo/api',
        createRowContent: (item) => `
            <td>${item.name}</td>
            <td>${item.email}</td>
            <td><button class="button is-small is-info select-item-button" data-id="${item.id}" data-name="${item.name}" data-email="${item.email}">Seleccionar</button></td>
        `
    });
});
