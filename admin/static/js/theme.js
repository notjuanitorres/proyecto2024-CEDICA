document.addEventListener('DOMContentLoaded', () => {
    const $themeToggle = document.getElementById('themeToggle');
    const $html = document.documentElement;

    const currentTheme = localStorage.getItem('theme') || 'light';

    setTheme(currentTheme);
  
    if ($themeToggle) {
      $themeToggle.addEventListener('click', () => {
        const newTheme = $html.getAttribute('data-theme')
        setTheme(newTheme);
        localStorage.setItem('theme', newTheme);
      });
    }
  
    function setTheme(theme) {
      if (theme === 'dark') {
        $html.setAttribute('data-theme', "light")
      } else {
        $html.setAttribute('data-theme', "dark")
      }
      if ($themeToggle) { 
        updateButtonAppearance(theme);
      }
    }
  
    function updateButtonAppearance(theme) {
      const svgPath = $themeToggle.querySelector('path');
      if (theme === 'dark') {
        svgPath.setAttribute('d', 'M12,22 C17.52,22 22,17.52 22,12 C22,6.48 17.52,2 12,2 C6.48,2 2,6.48 2,12 C2,17.52 6.48,22 12,22 Z M12,20.5 L12,3.5 C16.69,3.5 20.5,7.31 20.5,12 C20.5,16.69 16.69,20.5 12,20.5 Z');
      } else {
        svgPath.setAttribute('d', 'M12,22 C17.52,22 22,17.52 22,12 C22,6.48 17.52,2 12,2 C6.48,2 2,6.48 2,12 C2,17.52 6.48,22 12,22 Z M12,20 C7.58,20 4,16.42 4,12 C4,7.58 7.58,4 12,4 C16.42,4 20,7.58 20,12 C20,16.42 16.42,20 12,20 Z');
      }
    }
  });