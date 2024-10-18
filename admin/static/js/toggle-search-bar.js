document.addEventListener('DOMContentLoaded', function() {
  const toggleButtons = document.querySelectorAll('.card-header-icon');

  toggleButtons.forEach(button => {
    button.addEventListener('click', function() {
      const card = this.closest('.card');
      const toggleCard = card.querySelector('.card-content');
      const icon = this.querySelector('.fas');

      if (toggleCard.style.display === "none") {
        toggleCard.style.display = "block";
        icon.classList.replace('fa-angle-down', 'fa-angle-up');
      } else {
        toggleCard.style.display = "none";
        icon.classList.replace('fa-angle-up', 'fa-angle-down');
      }
    });
  });
});