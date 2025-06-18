document.getElementById('downloadPdfBtn').addEventListener('click', () => {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    const heading = document.querySelector('.form-container h2').innerText;
    const paragraphs = document.querySelectorAll('.form-container p');

    let y = 20;
    const lineHeight = 7;
    const margin = 10;
    const pageHeight = doc.internal.pageSize.height;

    // Add Heading
    doc.setFontSize(18);
    doc.text(heading, margin, y);
    y += 10;

    // Add Paragraphs
    doc.setFontSize(12);
    paragraphs.forEach(p => {
        const lines = doc.splitTextToSize(p.innerText, 180);

        // Check if text will overflow the page
        if (y + lines.length * lineHeight > pageHeight - margin) {
            doc.addPage();
            y = margin;
        }

        doc.text(lines, margin, y);
        y += lines.length * lineHeight;
    });

    doc.save('leave-application.pdf');
});
