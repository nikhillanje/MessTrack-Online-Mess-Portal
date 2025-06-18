const otpInputs = document.querySelectorAll('.otp-inputs input');

otpInputs.forEach((input, index) => {
    input.addEventListener('input', () => {
        input.value = input.value.replace(/\D/g, '');
        if (input.value.length === 1 && index < otpInputs.length - 1) {
            otpInputs[index + 1].focus();
        }
    });

    input.addEventListener('keydown', (e) => {
        if (e.key === "Backspace" && input.value === "" && index > 0) {
            otpInputs[index - 1].focus();
        }
    });

    input.addEventListener('click', () => {
        if (input.value.length === 0 && index > 0) {
            otpInputs[index - 1].focus();
        }
    });
});

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

// Full Name Validation
const nameInput = document.getElementById("name");
const nameError = nameInput.nextElementSibling;

nameInput.addEventListener("input", function () {
    nameInput.value = nameInput.value.replace(/[0-9]/g, '');
    const nameValue = nameInput.value.trim();
    const nameRegex = /^[A-Za-z\s]+$/;
    if (nameRegex.test(nameValue) || nameValue === "") {
        nameInput.classList.remove("invalid");
        nameError.style.display = "none";
    } else {
        nameInput.classList.add("invalid");
        nameError.style.display = "block";
    }
});

// Email Validation
const emailInput = document.getElementById("email");
const emailError = emailInput.nextElementSibling;

emailInput.addEventListener("input", function () {
    const emailValue = emailInput.value.trim();
    const emailRegex = /^[a-zA-Z][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (emailRegex.test(emailValue) || emailValue === "") {
        emailInput.classList.remove("invalid");
        emailError.style.display = "none";
    } else {
        emailInput.classList.add("invalid");
        emailError.style.display = "block";
    }
});

// Mobile Number Validation
const mobileInput = document.getElementById("mobile");

mobileInput.addEventListener("input", function () {
    let digits = mobileInput.value.replace(/\D/g, '');
    if (digits.length > 10) {
        digits = digits.slice(0, 10);
    }
    mobileInput.value = digits;
    if (digits.length === 10) {
        mobileInput.classList.remove("invalid");
    } else {
        mobileInput.classList.add("invalid");
    }
});

// Academic Branch Validation (Only characters A-Z, a-z)
const branchInput = document.getElementById("academic_branch");

branchInput.addEventListener("input", function () {
    branchInput.value = branchInput.value.replace(/[^A-Za-z\s]/g, '');
});

// Academic Year Validation (Only allow 1, 2, 3, or 4)
const yearInput = document.getElementById("academic_year");

yearInput.addEventListener("input", function () {
    const validYears = ['1', '2', '3', '4'];
    if (!validYears.includes(yearInput.value)) {
        yearInput.value = ''; // Clear invalid entry
    }
});
