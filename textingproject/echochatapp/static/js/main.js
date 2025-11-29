const menuToggleButton = document.getElementById('menu-toggle-btn');
const navbar = document.getElementById('nav-bar');

document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById("theme-toggle");

    // Load saved mode
    if (localStorage.getItem("dark") === "true") {
        document.body.classList.add("dark-mode");
        toggle.textContent = "Light Mode";
    }

    else if (localStorage.getItem("dark") === "false") {
        toggle.textContent = "Dark Mode";
    }

    toggle.addEventListener("click", () => {
        document.body.classList.toggle("dark-mode");

        const dark = document.body.classList.contains("dark-mode");
        localStorage.setItem("dark", dark);

        toggle.textContent = dark ? "Light Mode" : "Dark Mode";
    });
})

function home_page() {
    document.location.href = "http://127.0.0.1:8000"
}

menuToggleButton.addEventListener('click', () => {
  // Toggle the 'hidden' class to show/hide the navbar
  navbar.classList.toggle('visisble');

  // Alternative using 'visible' class:
  // navbar.classList.toggle('visible');
});