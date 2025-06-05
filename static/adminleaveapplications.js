document.getElementById('downloadPdfBtn').addEventListener('click', () => {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    const content = document.querySelector('.printable-content').innerText;
    const splitText = doc.splitTextToSize(content, 180);

    doc.text(splitText, 10, 10);
    doc.save('leave-application.pdf');
});