// Auto-fill today's date when the page loads
window.onload = function () {
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0'); // Months are 0-indexed
    const dd = String(today.getDate()).padStart(2, '0');
    const formattedDate = `${yyyy}-${mm}-${dd}`;
    document.getElementById('date').value = formattedDate;
};

// Handle attendance form submission
document.getElementById('attendance-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const date = document.getElementById('date').value;
    const message = document.getElementById('message');

    fetch('/mark_attendance', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ date: date })
    })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success') {
                message.innerText = 'Attendance marked successfully!';
                message.style.color = 'green';
            } else if (data.status === 'already_marked') {
                message.innerText = 'Attendance already marked.';
                message.style.color = 'orange';
            } else {
                message.innerText = 'Error marking attendance.';
                message.style.color = 'red';
            }
        })
        .catch(error => {
            message.innerText = 'Network error. Please try again.';
            message.style.color = 'red';
        });
});
