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

nameInput.addEventListener("keydown", function (event) {
    const key = event.key;
    if (!isNaN(key) && key !== " ") {
        event.preventDefault();
        nameInput.classList.add("is-invalid");
        nameError.style.display = "block";
    }
});

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

// MOBILE NUMBER VALIDATION
const mobileInput = document.getElementById("mobile");
const mobileError = mobileInput.nextElementSibling;

mobileInput.addEventListener("input", function () {
    const mobileValue = mobileInput.value.trim();
    const mobileRegex = /^\d{10}$/;

    if (mobileRegex.test(mobileValue)) {
        mobileInput.classList.remove("is-invalid");
        mobileError.style.display = "none";
    } else {
        mobileInput.classList.add("is-invalid");
        mobileError.style.display = "block";
    }
});

// (Optional) Block non-numeric input
mobileInput.addEventListener("keydown", function (event) {
    const allowedKeys = ["Backspace", "ArrowLeft", "ArrowRight", "Tab"];
    if (!/[0-9]/.test(event.key) && !allowedKeys.includes(event.key)) {
        event.preventDefault();
    }
});
