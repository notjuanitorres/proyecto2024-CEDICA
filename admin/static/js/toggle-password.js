document.addEventListener('DOMContentLoaded', () => {
  const togglePasswords = document.querySelectorAll('.toggle-password');
  const passwordInput = document.querySelectorAll('.password');

  togglePasswords.forEach((togglePassword, i) => {
    togglePassword.addEventListener('click', () => {
      // Alternar el tipo entre 'password' y 'text'
      const isPassword = passwordInput[i].getAttribute('type') === 'password';
      passwordInput[i].setAttribute('type', isPassword ? 'text' : 'password');

      togglePassword.querySelector('i').classList.toggle('fa-eye');
      togglePassword.querySelector('i').classList.toggle('fa-eye-slash');
    });
  });
});