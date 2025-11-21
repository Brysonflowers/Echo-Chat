const button = document.getElementById('theme-toggle')

function light_theme(){
    if (document.body.classList.contains("dark")) {
        document.body.classList.remove("dark");
        document.body.classList.add("light");
    } else {
        document.body.classList.remove("light");
        document.body.classList.add("dark");
    }
}

button.addEventListener('click', light_theme)
