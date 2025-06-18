// Bootstrap validation
(() => {
    'use strict';
    const form = document.querySelector('form');
    form.addEventListener('submit', event => {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.classList.add('was-validated');
    }, false);
})();

// NAME FIELD VALIDATION
const nameInput = document.getElementById("name");
const nameError = nameInput.nextElementSibling;

// Block number input and show error
nameInput.addEventListener("keydown", function (event) {
    const key = event.key;
    if (!isNaN(key) && key !== " ") {
        event.preventDefault();

        // Show error when number is attempted
        nameInput.classList.add("is-invalid");
        nameError.style.display = "block";
    }
});

// Validate on input (typing or paste)
nameInput.addEventListener("input", function () {
    const nameValue = nameInput.value.trim();
    const nameRegex = /^[A-Za-z\s]*$/;

    if (nameRegex.test(nameValue)) {
        nameInput.classList.remove("is-invalid");
        nameError.style.display = "none";
    } else {
        nameInput.classList.add("is-invalid");
        nameError.style.display = "block";
    }
});

// EMAIL FIELD VALIDATION
const emailInput = document.getElementById("email");
const emailError = emailInput.nextElementSibling;

emailInput.addEventListener("input", function () {
    const emailValue = emailInput.value.trim();
    const emailRegex = /^[a-zA-Z][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    if (emailRegex.test(emailValue) || emailValue === "") {
        emailInput.classList.remove("is-invalid");
        emailError.style.display = "none";
    } else {
        emailInput.classList.add("is-invalid");
        emailError.style.display = "block";
    }
});
