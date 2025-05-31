document.addEventListener('DOMContentLoaded', function () {
    const dateInput = document.getElementById('date');
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const dd = String(today.getDate()).padStart(2, '0');
    const todayStr = `${yyyy}-${mm}-${dd}`;

    dateInput.value = todayStr;

    document.getElementById('attendance-form').addEventListener('submit', function (e) {
        e.preventDefault();

        const date = dateInput.value;
        const username = document.getElementById('username').value;
        const message = document.getElementById('message');

        fetch('/mark_attendance', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ date: date, username: username })
        })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    message.innerText = 'Attendance marked successfully!';
                    message.style.color = 'green';
                } else if (data.status === 'already_marked') {
                    message.innerText = 'You have already marked attendance today.';
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
});
