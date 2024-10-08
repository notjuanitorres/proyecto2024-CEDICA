document.addEventListener('DOMContentLoaded', function() {
  const toggleButton = document.querySelector('#toggle-search-button');
  const toggleCard = document.querySelector('#toggle-search');

    toggleButton.addEventListener('click', function() {
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