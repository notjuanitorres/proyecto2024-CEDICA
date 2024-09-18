document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('themeToggle');
    const body = document.body;
    const navbar = document.querySelector('.navbar');
  
    const currentTheme = localStorage.getItem('theme') || 'light';
    setTheme(currentTheme);
  
    themeToggle.addEventListener('click', () => {
      const newTheme = body.classList.contains('light-theme') ? 'dark' : 'light';
      setTheme(newTheme);
      localStorage.setItem('theme', newTheme);
    });
  
    function setTheme(theme) {
      if (theme === 'dark') {
        body.classList.remove('light-theme');
        body.classList.add('dark-theme');
        navbar.classList.remove('is-light');
        navbar.classList.add('is-dark');
      } else {
        body.classList.remove('dark-theme');
        body.classList.add('light-theme');
        navbar.classList.remove('is-dark');
        navbar.classList.add('is-light');
      }
      updateButtonAppearance(theme);
    }
  
    function updateButtonAppearance(theme) {
      const svgPath = themeToggle.querySelector('path');
      if (theme === 'dark') {
        svgPath.setAttribute('d', 'M12,22 C17.52,22 22,17.52 22,12 C22,6.48 17.52,2 12,2 C6.48,2 2,6.48 2,12 C2,17.52 6.48,22 12,22 Z M12,20.5 L12,3.5 C16.69,3.5 20.5,7.31 20.5,12 C20.5,16.69 16.69,20.5 12,20.5 Z');
      } else {
        svgPath.setAttribute('d', 'M12,22 C17.52,22 22,17.52 22,12 C22,6.48 17.52,2 12,2 C6.48,2 2,6.48 2,12 C2,17.52 6.48,22 12,22 Z M12,20 C7.58,20 4,16.42 4,12 C4,7.58 7.58,4 12,4 C16.42,4 20,7.58 20,12 C20,16.42 16.42,20 12,20 Z');
      }
    }
  });