const switchLink = document.getElementById("switch-link");
const formTitle = document.getElementById("form-title");
const authForm = document.getElementById("auth-form");
const nameInput = document.getElementById("name");
const submitBtn = document.getElementById("submit-btn");

let isLogin = true;

switchLink.addEventListener("click", () => {
  isLogin = !isLogin;
  if(isLogin){
    formTitle.innerText = "Login";
    submitBtn.innerText = "Login";
    nameInput.classList.add("hidden");
    switchLink.innerText = "Register";
  } else {
    formTitle.innerText = "Register";
    submitBtn.innerText = "Register";
    nameInput.classList.remove("hidden");
    switchLink.innerText = "Login";
  }
});

authForm.addEventListener("submit", (e) => {
  e.preventDefault();
  
  const name = nameInput.value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  if(isLogin){
    console.log("Login Attempt:", {email, password});
    // Call your login API here
  } else {
    console.log("Register Attempt:", {name, email, password});
    // Call your registration API here
  }

  alert(isLogin ? "Login API called!" : "Registration API called!");
});
