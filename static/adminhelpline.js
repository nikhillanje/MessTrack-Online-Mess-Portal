function validateForm() {
    const number = document.forms["helplineForm"]["helpline"].value;
    const pattern = /^\d{10}$/;

    if (!pattern.test(number)) {
        alert("Please enter a valid 10-digit number.");
        return false; // prevent form submission
    }
    return true; // allow form submission
}
