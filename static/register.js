// OTP Input Handling
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

// Form Validation on Submit
(() => {
    'use strict';
    const form = document.querySelector('form');

    const emailInput = document.getElementById("email");
    const emailError = emailInput.nextElementSibling;

    const usernameInput = document.getElementById("username");
    const usernameError = usernameInput.nextElementSibling;

    const passwordInput = document.getElementById("password");
    const passwordError = passwordInput.nextElementSibling;

    form.addEventListener('submit', function (event) {
        let valid = true;

        // Email domain check
        const emailValue = emailInput.value.trim();
        const trustedDomains = [
            "gmail.com", "yahoo.com", "outlook.com", "hotmail.com",
            "protonmail.com", "zoho.com", "nic.in", "gov.in", "ac.in"
        ];
        let isEmailValid = false;
        const emailParts = emailValue.split("@");
        if (emailParts.length === 2) {
            const domain = emailParts[1].toLowerCase();
            isEmailValid = trustedDomains.some(allowed =>
                domain === allowed || domain.endsWith("." + allowed)
            );
        }

        if (!isEmailValid) {
            emailInput.classList.add("invalid");
            emailError.textContent = "Only trusted domains like gmail.com, ac.in, gov.in are allowed.";
            emailError.style.display = "block";
            valid = false;
        } else {
            emailInput.classList.remove("invalid");
            emailError.style.display = "none";
        }

        // Username ≥ 5 characters
        if (usernameInput.value.trim().length < 5) {
            usernameInput.classList.add("invalid");
            usernameError.textContent = "Username must be at least 5 characters.";
            usernameError.style.display = "block";
            valid = false;
        } else {
            usernameInput.classList.remove("invalid");
            usernameError.style.display = "none";
        }

        // Password ≥ 8 characters
        if (passwordInput.value.length < 8) {
            passwordInput.classList.add("invalid");
            passwordError.textContent = "Password must be at least 8 characters.";
            passwordError.style.display = "block";
            valid = false;
        } else {
            passwordInput.classList.remove("invalid");
            passwordError.style.display = "none";
        }

        // Final check
        if (!form.checkValidity() || !valid) {
            event.preventDefault();
            event.stopPropagation();
        }

        form.classList.add('was-validated');
    }, false);
})();

// Full Name (only letters & spaces)
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
        nameError.textContent = "Name must contain only letters.";
        nameError.style.display = "block";
    }
});

// Live Email Trusted Domain Validation
const emailInput = document.getElementById("email");
const emailError = emailInput.nextElementSibling;
emailInput.addEventListener("input", function () {
    const emailValue = emailInput.value.trim();
    const trustedDomains = [
        "gmail.com", "yahoo.com", "outlook.com", "hotmail.com",
        "protonmail.com", "zoho.com", "nic.in", "gov.in", "ac.in"
    ];
    const emailParts = emailValue.split("@");

    if (emailParts.length !== 2) {
        setEmailInvalid();
        return;
    }

    const domain = emailParts[1].toLowerCase();
    const isTrusted = trustedDomains.some(allowed =>
        domain === allowed || domain.endsWith("." + allowed)
    );

    if (isTrusted) {
        emailInput.classList.remove("invalid");
        emailError.style.display = "none";
    } else {
        setEmailInvalid();
    }

    function setEmailInvalid() {
        emailInput.classList.add("invalid");
        emailError.textContent = "Only trusted domains like gmail.com, ac.in, gov.in are allowed.";
        emailError.style.display = "block";
    }
});

// Mobile: Only 10 digits
const mobileInput = document.getElementById("mobile");
mobileInput.addEventListener("input", function () {
    let digits = mobileInput.value.replace(/\D/g, '');
    if (digits.length > 10) digits = digits.slice(0, 10);
    mobileInput.value = digits;

    if (digits.length === 10) {
        mobileInput.classList.remove("invalid");
    } else {
        mobileInput.classList.add("invalid");
    }
});

// Academic Branch: Only letters & spaces
const branchInput = document.getElementById("academic_branch");
branchInput.addEventListener("input", function () {
    branchInput.value = branchInput.value.replace(/[^A-Za-z\s]/g, '');
});

// Academic Year: Only 1 to 4
const yearInput = document.getElementById("academic_year");
yearInput.addEventListener("input", function () {
    const validYears = ['1', '2', '3', '4'];
    if (!validYears.includes(yearInput.value)) {
        yearInput.value = '';
    }
});
