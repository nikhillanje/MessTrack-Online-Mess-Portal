function downloadPDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    doc.text("User Data", 14, 16);
    doc.autoTable({
        html: '#userTable',
        startY: 20,
        theme: 'grid',
        headStyles: { fillColor: [242, 242, 242] }
    });
    doc.save('users_data.pdf');
}

function deleteUser(userId) {
    if (confirm("Are you sure you want to delete this user?")) {
        fetch(`/delete_user/${userId}`, {
            method: 'DELETE'
        })
            .then(response => {
                if (response.ok) {
                    alert("User deleted successfully.");
                    location.reload();
                } else {
                    alert("Failed to delete user.");
                }
            });
    }
}

