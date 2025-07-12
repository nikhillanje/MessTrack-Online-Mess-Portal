document.addEventListener("DOMContentLoaded", function () {
    const button = document.getElementById("rzp-button");

    const amount = parseInt(button.getAttribute("data-amount")) * 100;  // In paise
    const month = button.getAttribute("data-month");
    const key = button.getAttribute("data-key");

    button.onclick = async function () {
        const response = await fetch("/create_order", {
            method: "POST",
            body: JSON.stringify({ amount: amount }),
            headers: {
                "Content-Type": "application/json"
            }
        });

        const order = await response.json();

        const options = {
            key: key,
            amount: order.amount,
            currency: "INR",
            name: "MessTrack",
            description: "Mess Bill - " + month,
            order_id: order.id,
            handler: async function (response) {
                const verify = await fetch("/verify_payment", {
                    method: "POST",
                    body: JSON.stringify(response),
                    headers: {
                        "Content-Type": "application/json"
                    }
                });

                const result = await verify.json();
                if (result.status === "success") {
                    window.location.href = "/payment_success";
                } else {
                    alert("Payment verification failed!");
                }
            }
        };

        const rzp = new Razorpay(options);
        rzp.open();
    };
});
