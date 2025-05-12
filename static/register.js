const otpInputs = document.querySelectorAll('.otp-inputs input');

otpInputs.forEach((input, index) => {
    // Allow only digits
    input.addEventListener('input', () => {
        input.value = input.value.replace(/\D/g, ''); // Remove non-digits
        if (input.value.length === 1 && index < otpInputs.length - 1) {
            otpInputs[index + 1].focus();
        }
    });

    // Allow moving back with Backspace
    input.addEventListener('keydown', (e) => {
        if (e.key === "Backspace") {
            if (input.value === "" && index > 0) {
                otpInputs[index - 1].focus();
            }
        }
    });

    // Optional: Go to previous on click if empty
    input.addEventListener('click', () => {
        if (input.value.length === 0 && index > 0) {
            otpInputs[index - 1].focus();
        }
    });
});