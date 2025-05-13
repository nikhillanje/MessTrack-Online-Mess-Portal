// DARK MODE TOGGLE
function toggleMode() {
    const body = document.body;
    const icon = document.querySelector(".mode-toggle i");

    body.classList.toggle("dark-mode");

    if (body.classList.contains("dark-mode")) {
        icon.classList.remove("bi-moon-fill");
        icon.classList.add("bi-sun-fill");
    } else {
        icon.classList.remove("bi-sun-fill");
        icon.classList.add("bi-moon-fill");
    }
}

// SIDEBAR TOGGLE
const sidebar = document.getElementById('sidebar');
const menuIcon = document.querySelector('.menu_icon'); // Using class as in HTML

menuIcon.addEventListener('click', function (event) {
    event.stopPropagation(); // Prevent this click from bubbling to the document
    sidebar.classList.toggle('active');
});

// CLOSE SIDEBAR WHEN CLICKING OUTSIDE
document.addEventListener('click', function (event) {
    if (!sidebar.contains(event.target) && !menuIcon.contains(event.target)) {
        sidebar.classList.remove('active');
    }
});
