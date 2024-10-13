document.addEventListener('DOMContentLoaded', () => {
    const openModalButton = document.getElementById('openModalButtonJya');
    const jyaModal = document.getElementById('jyaModal');
    const searchJya = document.getElementById('searchJya');
    const jyaList = document.getElementById('jyaList');
    const jyaNameInput = document.getElementById('jya');
    const jyaIdInput = document.getElementById('jya_id');


  // Open modal
  openModalButton.addEventListener('click', (e) => {
      jyaModal.classList.add('is-active');
      e.preventDefault();
  });

  // Close modal
  document.querySelectorAll('.modal-background, .delete, .modal-card-foot .button').forEach(($close) => {
      $close.addEventListener('click', (event) => {
          event.preventDefault();
          jyaModal.classList.remove('is-active');
      });
  });

  // Search jyas
  searchJya.addEventListener('input', () => {
      const query = searchJya.value.toLowerCase();
      fetch(`/equipo/api?search=${query}`)
          .then(response => response.json())
          .then(data => {
              jyaList.innerHTML = '';
              data.forEach(jya => {
                  const row = document.createElement('tr');
                  row.innerHTML = `
                      <td>${jya.name}</td>
                      <td>${jya.email}</td>
                      <td><button class="button is-small is-info select-jya-button" data-id="${jya.id}" data-name="${jya.name}" data-email="${jya.email}">Seleccionar</button></td>
                  `;
                  jyaList.appendChild(row);
              });

              document.querySelectorAll('.select-jya-button').forEach(button => {
                  button.addEventListener('click', (event) => {
                      event.preventDefault();
                      const name = event.target.getAttribute('data-name');
                      const email = event.target.getAttribute('data-email');
                      const id = event.target.getAttribute('data-id');
                      jyaNameInput.value = name + " (Email: " + email + ")";
                      jyaIdInput.value = id;
                      jyaModal.classList.remove('is-active');
                  });
              });
          });
  });
});