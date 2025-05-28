function downloadPDF() {
    // Use jsPDF from the global window.jspdf
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    doc.text("User Data", 14, 16);

    // AutoTable uses doc.autoTable(), make sure plugin is loaded
    doc.autoTable({
        html: '#userTable',
        startY: 20,
        theme: 'grid',
        headStyles: { fillColor: [242, 242, 242] }
    });

    doc.save('users_data.pdf');
}
