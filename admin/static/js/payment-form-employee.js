document.addEventListener('DOMContentLoaded', () => {
  const paymentTypeField = document.getElementById('payment_type');
  const beneficiaryField = document.getElementById('beneficiaryField');
  const openModalButton = document.getElementById('openModalButton');
  const employeeModal = document.getElementById('employeeModal');
  const searchEmployee = document.getElementById('searchEmployee');
  const employeeList = document.getElementById('employeeList');
  const selectEmployeeButton = document.getElementById('selectEmployee');
  const beneficiaryInput = document.getElementById('beneficiary');

  const toggleBeneficiaryField = () => {
      if (paymentTypeField.value === 'HONORARIOS') {
          beneficiaryField.style.display = 'block';
      } else {
          beneficiaryField.style.display = 'none';
      }
  };

  // Initial check
  toggleBeneficiaryField();

  // Add event listener
  paymentTypeField.addEventListener('change', toggleBeneficiaryField);

  // Open modal
  openModalButton.addEventListener('click', () => {
      employeeModal.classList.add('is-active');
  });

  // Close modal
  document.querySelectorAll('.modal-background, .delete, .modal-card-foot .button').forEach(($close) => {
      $close.addEventListener('click', () => {
          employeeModal.classList.remove('is-active');
      });
  });

  // Search employees
  searchEmployee.addEventListener('input', () => {
      const query = searchEmployee.value.toLowerCase();
      // fetch(`/api/employees?search=${query}`)
      //     .then(response => response.json())
      //     .then(data => {
      //         employeeList.innerHTML = '';
      //         data.forEach(employee => {
      //             const row = document.createElement('tr');
      //             row.innerHTML = `
      //                 <td>${employee.name}</td>
      //                 <td>${employee.email}</td>
      //                 <td><button class="button is-small is-primary select-employee-button" data-id="${employee.id}" data-name="${employee.name}">Seleccionar</button></td>
      //             `;
      //             employeeList.appendChild(row);
      //         });

      //         document.querySelectorAll('.select-employee-button').forEach(button => {
      //             button.addEventListener('click', (event) => {
      //                 const name = event.target.getAttribute('data-name');
      //                 beneficiaryInput.value = name;
      //                 employeeModal.classList.remove('is-active');
      //             });
      //         });
      //     });
  });
});