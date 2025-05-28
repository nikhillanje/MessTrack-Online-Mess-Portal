const inputs = document.querySelectorAll(".otp-block input");
inputs.forEach((input, index) => {
    input.addEventListener("input", () => {
        if (input.value.length === 1 && index < inputs.length - 1) {
            inputs[index + 1].focus();
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const refreshButton = document.getElementById('refresh-captcha');
    const captchaText = document.getElementById('captcha-text');
    const captchaInput = document.getElementById('captcha-input');
    const form = document.querySelector('form');

    // Refresh captcha on button click by requesting new captcha from server
    refreshButton.addEventListener('click', function () {
        fetch('/refresh_captcha')
            .then(response => response.text())
            .then(newCaptcha => {
                captchaText.textContent = newCaptcha;
                captchaInput.value = ''; // Clear the input for user to re-enter
            })
            .catch(err => {
                console.error('Error refreshing CAPTCHA:', err);
            });
    });

    // Note: CAPTCHA validation must be done on server-side in your Flask POST route

    // Optionally, if you want to prevent submitting empty captcha client side, you can add:
    form.addEventListener('submit', function (e) {
        if (!captchaInput.value.trim()) {
            e.preventDefault();
            alert('Please enter the CAPTCHA.');
        }
    });
});
