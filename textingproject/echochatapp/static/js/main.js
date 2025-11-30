const menuToggleButton = document.getElementById('menu-toggle-btn');
const navbar = document.getElementById('nav-bar');

function home_page() {
    document.location.href = "http://127.0.0.1:8000"
}

menuToggleButton.addEventListener('click', () => {
  // Toggle the 'hidden' class to show/hide the navbar
  navbar.classList.toggle('visisble');

  // Alternative using 'visible' class:
  // navbar.classList.toggle('visible');
});