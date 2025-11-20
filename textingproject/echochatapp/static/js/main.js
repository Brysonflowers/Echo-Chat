document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById("dark-toggle");

    // Load saved mode
    if (localStorage.getItem("dark") === "true") {
        document.body.classList.add("dark-mode");
        toggle.textContent = "Light Mode";
    }

    toggle.addEventListener("click", () => {
        document.body.classList.toggle("dark-mode");

        const dark = document.body.classList.contains("dark-mode");
        localStorage.setItem("dark", dark);

        toggle.textContent = dark ? "Light Mode" : "Dark Mode";
    });
})

function home_page () {
    document.location.href = "http://127.0.0.1:8000"
}