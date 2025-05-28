document.addEventListener("DOMContentLoaded", function () {
    const cells = document.querySelectorAll("td:not(.day)");
    let isEditing = false;

    cells.forEach(cell => {
        cell.addEventListener("click", function () {
            if (!isEditing) {
                cell.contentEditable = true;
                cell.focus();
                isEditing = true;

                cell.addEventListener("blur", function () {
                    cell.contentEditable = false;
                    isEditing = false;

                    if (cell.textContent.trim() === "") {
                        cell.textContent = "NULL";
                    }
                }, { once: true });
            }
        });
    });

    const submitBtn = document.getElementById("submit");
    if (submitBtn) {
        submitBtn.addEventListener("click", function () {
            alert("Change successful!");
        });
    }

    const downloadBtn = document.getElementById("download");
    if (downloadBtn) {
        downloadBtn.addEventListener("click", function () {
            const container = document.querySelector(".container");
            if (!container) {
                alert("Container not found!");
                return;
            }

            html2canvas(container).then(canvas => {
                const imgData = canvas.toDataURL("image/png");
                const pdf = new window.jspdf.jsPDF("p", "mm", "a4");

                const imgWidth = 190;
                const pageHeight = 297;
                const imgHeight = canvas.height * imgWidth / canvas.width;

                pdf.addImage(imgData, "PNG", 10, 10, imgWidth, imgHeight);
                pdf.save("Mess-Timetable.pdf");
            }).catch(err => {
                console.error("PDF generation failed:", err);
                alert("Failed to generate PDF.");
            });
        });
    }
});
