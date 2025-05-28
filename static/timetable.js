document.addEventListener("DOMContentLoaded", () => {
    const downloadBtn = document.getElementById("download");

    if (!downloadBtn) return;

    downloadBtn.addEventListener("click", () => {
        const container = document.querySelector(".container");
        if (!container) {
            alert("Container not found!");
            return;
        }

        // Use html2canvas to capture container as image
        html2canvas(container).then(canvas => {
            const imgData = canvas.toDataURL("image/png");

            // Create a new jsPDF instance
            const pdf = new window.jspdf.jsPDF("p", "mm", "a4");

            const pageWidth = pdf.internal.pageSize.getWidth();
            const pageHeight = pdf.internal.pageSize.getHeight();

            const imgWidth = pageWidth - 20; // 10 mm margin left and right
            const imgHeight = (canvas.height * imgWidth) / canvas.width;

            let position = 10; // start 10mm from top

            // Add image to pdf
            pdf.addImage(imgData, "PNG", 10, position, imgWidth, imgHeight);

            // Save PDF with filename
            pdf.save("Mess-Timetable.pdf");
        }).catch(err => {
            console.error("PDF generation failed:", err);
            alert("Failed to generate PDF.");
        });
    });
});
