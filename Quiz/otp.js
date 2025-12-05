const otpInputs = document.querySelectorAll(".otp-field");
const verifyBtn = document.getElementById("verifyBtn");
const resendBtn = document.getElementById("resendOtp");

// Auto-focus movement
otpInputs.forEach((input, index) => {
  input.addEventListener("keyup", () => {
    if (input.value.length === 1 && index < 5) {
      otpInputs[index + 1].focus();
    }
  });
});

// Verify OTP
verifyBtn.addEventListener("click", async () => {
  let otp = "";
  otpInputs.forEach(i => otp += i.value);

  if (otp.length !== 6) {
    alert("Enter 6-digit OTP");
    return;
  }

  // Call backend API for OTP verification
  try {
    const res = await fetch("http://localhost:8000/verify-otp", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ otp })
    });

    const data = await res.json();
    
    if (data.success) {
      alert("OTP Verified Successfully!");
      window.location.href = "home.html";
    } else {
      alert("Invalid OTP");
    }

  } catch (err) {
    alert("Error verifying OTP");
  }
});

// Resend OTP
resendBtn.addEventListener("click", async () => {
  try {
    const res = await fetch("http://localhost:8000/resend-otp", {
      method: "POST"
    });

    const data = await res.json();
    alert(data.message);

  } catch (error) {
    alert("Error sending OTP");
  }
});
