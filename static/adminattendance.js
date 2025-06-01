document.getElementById('dateForm').addEventListener('submit', function () {
    document.getElementById('loading').style.display = 'block';
});

document.addEventListener("DOMContentLoaded", function () {
    const downloadBtn = document.getElementById("downloadPDF");

    if (downloadBtn) {
        downloadBtn.addEventListener("click", function () {
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF();

            // Get selected date from hidden span
            const selectedDate = document.getElementById("selectedDate").innerText || "Unknown Date";

            // Add title
            doc.setFontSize(18);
            doc.text(`Student Attendance - ${selectedDate}`, 14, 20);

            // Collect table data
            const rows = [];
            const table = document.getElementById("studentTable");

            for (let row of table.rows) {
                let cols = row.querySelectorAll("td");
                let rowData = Array.from(cols).map(col => col.innerText);
                rows.push(rowData);
            }

            // Add table
            doc.autoTable({
                head: [["Student Name", "Mobile Number", "Email", "Status"]],
                body: rows,
                startY: 30
            });

            // Save with dynamic filename
            doc.save(`attendance_${selectedDate}.pdf`);
        });
    }
});
