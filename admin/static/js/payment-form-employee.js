document.addEventListener('DOMContentLoaded', () => {
    const paymentTypeField = document.getElementById('payment_type');
    const beneficiaryField = document.getElementById('beneficiaryField');

  const toggleBeneficiaryField = () => {
    if (paymentTypeField.value === 'HONORARIOS') {
        beneficiaryField.style.display = 'block';
    } else {
        beneficiaryField.style.display = 'none';
    }
  };

  // Initial check
  toggleBeneficiaryField();

});