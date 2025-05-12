document.addEventListener('DOMContentLoaded', function () {
    const menuIcon = document.querySelector('.menu_icon');
    const sidebar = document.getElementById('sidebar');
    const body = document.querySelector('body');

    // Toggle sidebar on menu icon click
    menuIcon.addEventListener('click', () => {
        sidebar.classList.toggle('active');
    });

    // Close sidebar when clicking outside of it
    body.addEventListener('click', function (e) {
        // Check if the clicked target is outside the sidebar and not the menu icon
        if (!sidebar.contains(e.target) && !menuIcon.contains(e.target)) {
            sidebar.classList.remove('active');
        }
    });
});

